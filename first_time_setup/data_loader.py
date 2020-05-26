import os
import zipfile
import re
from functools import reduce

import pandas as pd
import numpy as np
import requests
from tqdm import tqdm

from .downloads import path as path_to_downloads

LINK_TO_MOVIE_LENS_DATASET = "http://files.grouplens.org/datasets/movielens/ml-latest.zip"
RELEVANCE_CUTOFF = 0.3

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


def load_dataset(dataset_path):
    print("loading dataset...")
    if dataset_path is not None:
        dataset = _collect_data_from_local_path(dataset_path)
    else:
        dataset = _download_dataset()
    return dataset
