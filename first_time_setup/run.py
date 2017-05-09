import argparse
import os

from movie_time.settings import BASE_DIR

PATH_TO_MOVIE_LENS_DB = "http://files.grouplens.org/datasets/movielens/ml-latest.zip"
DEFAULT_PATH_TO_DB = os.path.join(BASE_DIR, 'db.sqlite3')


def _load_dataset_from_internet():
    pass


def _load_dataset_from_local_path(input_dataset_path):
    pass


def _load_dataset(input_dataset_path):
    if input_dataset_path is not None:
        dataset = _load_dataset_from_local_path(input_dataset_path)
    else:
        dataset = _load_dataset_from_internet()
    return dataset


def main(input_dataset_path, database_path):
    dataset = _load_dataset(input_dataset_path)
    if database_path is not None:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download MovieLens dataset & fill database with movie similarity graph")
    parser.add_argument('-i', '--input-dataset', type=str, help="Path to dataset folder if already downloaded")
    parser.add_argument('-d', '--database', type=str, help="Path to the sqlite DB if not in default path in the django project")
    args = parser.parse_args()
    main(args.input_dataset, args.database)