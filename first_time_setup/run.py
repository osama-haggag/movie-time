import argparse
import logging
import os
import zipfile

import pandas as pd
import requests
import sqlite3
from tqdm import tqdm

from first_time_setup.downloads import path
from first_time_setup.movie_similarity import movie_to_movie
from movie_time.settings import BASE_DIR

LINK_TO_MOVIE_LENS_DATASET = "http://files.grouplens.org/datasets/movielens/ml-latest.zip"
DEFAULT_PATH_TO_DB = os.path.join(BASE_DIR, 'db.sqlite3')


def _load_dataset_from_local_path(input_dataset_path):
    movie_ratings = pd.read_csv(os.path.join(input_dataset_path, 'ratings.csv'), usecols=['movieId', 'rating'])
    genome_scores = pd.read_csv(os.path.join(input_dataset_path, 'genome-scores.csv'))
    genome_tags = pd.read_csv(os.path.join(input_dataset_path, 'genome-tags.csv'))
    movie_names = pd.read_csv(os.path.join(input_dataset_path, 'movies.csv'))
    links = pd.read_csv(os.path.join(input_dataset_path, 'links.csv'))
    return genome_scores, genome_tags, movie_names, movie_ratings, links


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
    download_path = str(path)
    _download_data(download_path)
    _extract_dataset_from_zip(download_path)
    dataset = _load_dataset_from_local_path(download_path)
    return dataset


def _load_dataset(input_dataset_path):
    print("loading dataset...")
    if input_dataset_path is not None:
        dataset = _load_dataset_from_local_path(input_dataset_path)
    else:
        dataset = _download_dataset()
    return dataset


def _connect_to_database(database_path):
    if database_path is None:
        database_path = DEFAULT_PATH_TO_DB
    db = sqlite3.connect(database_path)
    return db


def _conform_to_db_model(dataset_with_tags, unrelatable_movies, links_to_imdb):
    links_col_order = ['movie_id', 'imdb_id']
    links_to_imdb.rename(columns={'movieId': 'movie_id', 'imdbId': 'imdb_id'}, inplace=True)

    dataset_col_order = ['movie_id', 'title', 'year', 'genres', 'num_ratings', 'rating_median', 'rating_mean', 'relatable']
    dataset_with_tags['relatable'] = True
    unrelatable_movies['relatable'] = False
    return dataset_with_tags[dataset_col_order], unrelatable_movies[dataset_col_order], links_to_imdb[links_col_order]


def _populate_database_tables(db_connection, movie_to_movie_similarity, dataset_with_tags, unrelatable_movies, links_to_imdb):
    with_tags, without_tags, links = _conform_to_db_model(dataset_with_tags, unrelatable_movies, links_to_imdb)

    print("writing movies with tags to DB...")
    with_tags.to_sql('movie_time_app_movie', db_connection, if_exists='append', index=False)

    print("writing movies without tags to DB...")
    without_tags.to_sql('movie_time_app_movie', db_connection, if_exists='append', index=False)

    print("writing online links to DB...")
    links.to_sql('movie_time_app_onlinelink', db_connection, if_exists='append', index=False)


def main(input_dataset_path, database_path):
    genome_scores, genome_tags, movie_names, movie_ratings, links_to_imdb = _load_dataset(input_dataset_path)
    db_connection = _connect_to_database(database_path)
    movie_to_movie_similarity, dataset_with_tags, unrelatable_movies = movie_to_movie(genome_scores, genome_tags,
                                                                                      movie_names, movie_ratings)
    _populate_database_tables(db_connection, movie_to_movie_similarity, dataset_with_tags, unrelatable_movies, links_to_imdb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download MovieLens dataset & fill database with movie similarity matrix")
    parser.add_argument('-i', '--input-dataset', type=str, help="Path to dataset folder if already downloaded")
    parser.add_argument('-d', '--database', type=str, help="Path to the sqlite DB if not in default path in the django project")
    args = parser.parse_args()
    main(args.input_dataset, args.database)
