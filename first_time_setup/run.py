import argparse

from first_time_setup.data_loader import load_dataset
from first_time_setup.movie_similarity import compute_movie_to_movie_similarity
from first_time_setup.database import create_and_populate_database


def main(dataset_path, database_path):
    dataset = load_dataset(dataset_path)
    movie_to_movie_similarity = compute_movie_to_movie_similarity(dataset)
    create_and_populate_database(dataset, movie_to_movie_similarity, database_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download MovieLens dataset & fill database with movie similarity matrix")
    parser.add_argument('-i', '--input-dataset', type=str, help="Path to dataset folder if already downloaded")
    parser.add_argument('-d', '--database', type=str, help="Path to the sqlite DB if not in default path in the django project")
    args = parser.parse_args()
    main(args.input_dataset, args.database)
