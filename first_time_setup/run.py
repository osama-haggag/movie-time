import argparse
import os

import pandas as pd

from first_time_setup.movie_similarity import movie_to_movie
from movie_time.settings import BASE_DIR

PATH_TO_MOVIE_LENS_DB = "http://files.grouplens.org/datasets/movielens/ml-latest.zip"
DEFAULT_PATH_TO_DB = os.path.join(BASE_DIR, 'db.sqlite3')


def _download_dataset():
    pass


def _load_dataset_from_local_path(input_dataset_path):
    movie_ratings = pd.read_csv(os.path.join(input_dataset_path, 'ratings.csv'), usecols=['movieId', 'rating'])
    genome_scores = pd.read_csv(os.path.join(input_dataset_path, 'genome-scores.csv'))
    genome_tags = pd.read_csv(os.path.join(input_dataset_path, 'genome-tags.csv'))
    movie_names = pd.read_csv(os.path.join(input_dataset_path, 'movies.csv'))
    return genome_scores, genome_tags, movie_names, movie_ratings


def _load_dataset(input_dataset_path):
    if input_dataset_path is not None:
        dataset = _load_dataset_from_local_path(input_dataset_path)
    else:
        dataset = _download_dataset()
    return dataset


def main(input_dataset_path, database_path):
    genome_scores, genome_tags, movie_names, movie_ratings = _load_dataset(input_dataset_path)
    if database_path is not None:
        pass
    movie_to_movie_matrix = movie_to_movie(genome_scores, genome_tags, movie_names, movie_ratings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download MovieLens dataset & fill database with movie similarity matrix")
    parser.add_argument('-i', '--input-dataset', type=str, help="Path to dataset folder if already downloaded")
    parser.add_argument('-d', '--database', type=str, help="Path to the sqlite DB if not in default path in the django project")
    args = parser.parse_args()
    main(args.input_dataset, args.database)