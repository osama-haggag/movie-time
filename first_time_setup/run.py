import argparse
import os
import zipfile
import re
from functools import reduce

import pandas as pd
import numpy as np
import requests
import sqlite3
from tqdm import tqdm

from downloads import path as path_to_downloads
from movie_similarity import movie_to_movie
#from movie_time.settings import BASE_DIR

RELEVANCE_CUTOFF = 0.3
LINK_TO_MOVIE_LENS_DATASET = "http://files.grouplens.org/datasets/movielens/ml-latest.zip"
DEFAULT_PATH_TO_DB = os.path.join(os.getcwd(), 'db.sqlite3')


def _get_avg_movie_rating(dataset_path):
    movie_ratings = pd.read_csv(os.path.join(dataset_path, 'ratings.csv'), usecols=['movieId', 'rating'])
    avg_ratings = movie_ratings \
        .groupby('movieId')['rating'] \
        .agg(rating_mean='mean', rating_median='median', rating_std='std', num_ratings='size')\
        .reset_index()

    del movie_ratings
    return avg_ratings


def _concatenate_tags_of_movie(tags):
    tags_as_str = '; '.join(set(tags))
    return tags_as_str


def _get_movie_tags(dataset_path):
    genome_scores = pd.read_csv(os.path.join(dataset_path, 'genome-scores.csv'))
    genome_tags = pd.read_csv(os.path.join(dataset_path, 'genome-tags.csv'))
    movie_tags_as_text = pd.merge(genome_scores, genome_tags, on='tagId')[['movieId', 'tag', 'relevance']]
    top_tags_per_movie = movie_tags_as_text[movie_tags_as_text.relevance > RELEVANCE_CUTOFF]\
        .sort_values(by='relevance', ascending=False)\
        .groupby('movieId')['tag']\
        .agg(movie_tags=_concatenate_tags_of_movie)

    del movie_tags_as_text, genome_scores, genome_tags
    return top_tags_per_movie


def _extract_year_from_movie_title(movie_title):
    matches = re.findall(r'\d{4}', movie_title)
    if len(matches) > 1:
        return int(matches[-1])
    if len(matches) < 1:
        return np.nan
    return int(matches[0])


def _collect_data_from_local_path(dataset_path):
    avg_ratings = _get_avg_movie_rating(dataset_path)
    movie_tags = _get_movie_tags(dataset_path)
    movie_names = pd.read_csv(os.path.join(dataset_path, 'movies.csv'))
    links = pd.read_csv(os.path.join(dataset_path, 'links.csv'))

    all_dfs = [movie_names, avg_ratings, links, movie_tags]
    dataset = reduce(lambda left, right: pd.merge(left, right, on='movieId', how='left'), all_dfs)
    dataset['year'] = dataset.title.apply(_extract_year_from_movie_title)
    return dataset


def _download_data(download_path):
    file_path = os.path.join(download_path, 'ml-latest.zip')
    response = requests.get(LINK_TO_MOVIE_LENS_DATASET, stream=True)
    with open(file_path, 'wb') as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)


def _extract_dataset_from_zip(download_path):
    file_path = os.path.join(download_path, 'ml-latest.zip')
    zip_ref = zipfile.ZipFile(file_path, 'rb')
    zip_ref.extractall(download_path)
    zip_ref.close()


def _download_dataset():
    print("downloading dataset...")
    path_as_string = str(path_to_downloads)
    _download_data(path_as_string)
    _extract_dataset_from_zip(path_as_string)
    dataset = _collect_data_from_local_path(path_as_string)
    return dataset


def _load_dataset(dataset_path):
    print("loading dataset...")
    if dataset_path is not None:
        dataset = _collect_data_from_local_path(dataset_path)
    else:
        dataset = _download_dataset()
    return dataset


def _connect_to_database(database_path):
    if database_path is None:
        database_path = DEFAULT_PATH_TO_DB
    db = sqlite3.connect(database_path)
    return db


def _conform_to_db_model(dataset_with_tags, unrelatable_movies, links_to_imdb, movie_tags_as_text):
    links_col_order = ['movie_id', 'imdb_id']
    links_to_imdb.rename(columns={'movieId': 'movie_id', 'imdbId': 'imdb_id'}, inplace=True)

    tags_col_order = ['movie_id', 'tag', 'relevance']
    movie_tags_as_text.rename(columns={'movieId': 'movie_id'}, inplace=True)

    dataset_col_order = ['movie_id', 'title', 'year', 'genres', 'num_ratings', 'rating_median', 'rating_mean', 'relatable']
    dataset_with_tags['relatable'] = True
    unrelatable_movies['relatable'] = False
    return (dataset_with_tags[dataset_col_order], unrelatable_movies[dataset_col_order],
            links_to_imdb[links_col_order], movie_tags_as_text[tags_col_order])


def _write_to_db_with_progress_bar(df, table_name, db_connection):
    total_length = len(df)
    step = int(total_length / 100)

    with tqdm(total=total_length) as pbar:
        for i in range(0, total_length, step):
            subset = df[i: i + step]
            subset.to_sql(table_name, db_connection, if_exists='append', index=False)
            pbar.update(step)


def _populate_database_tables(dataset, movie_to_movie_similarity, database_path):
    db_connection = _connect_to_database(database_path)
    with_tags, without_tags, links, tags = _conform_to_db_model(dataset_with_tags, unrelatable_movies,
                                                                links_to_imdb, movie_tags_as_text)

    print("writing movies with tags to DB...")
    _write_to_db_with_progress_bar(with_tags, 'movie_time_app_movie', db_connection)

    print("writing movies without tags to DB...")
    _write_to_db_with_progress_bar(without_tags, 'movie_time_app_movie', db_connection)

    print("writing online links to DB...")
    _write_to_db_with_progress_bar(links, 'movie_time_app_onlinelink', db_connection)

    print("writing movie tags to DB...")
    _write_to_db_with_progress_bar(tags, 'movie_time_app_tag', db_connection)

    print("writing movie similarities to DB...")
    _write_to_db_with_progress_bar(movie_to_movie_similarity, 'movie_time_app_similarity', db_connection)


def main(dataset_path, database_path):
    dataset = _load_dataset(dataset_path)
    movie_to_movie_similarity = movie_to_movie(dataset)
    _populate_database_tables(movie_to_movie_similarity, dataset, database_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download MovieLens dataset & fill database with movie similarity matrix")
    parser.add_argument('-i', '--input-dataset', type=str, help="Path to dataset folder if already downloaded")
    parser.add_argument('-d', '--database', type=str, help="Path to the sqlite DB if not in default path in the django project")
    args = parser.parse_args()
    main(args.input_dataset, args.database)
