import os

import sqlite3

from tqdm import tqdm


DEFAULT_PATH_TO_DB = os.path.join(os.getcwd(), 'db.sqlite3')


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


def _prepare_dataset_for_db(dataset):
    dataset.rename(columns={'movieId': 'movie_id', 'imdbId': 'imdb_id'}, inplace=True)
    dataset_col_order = [
        'movie_id', 'title', 'year', 'genres',
        'num_ratings', 'rating_median', 'rating_mean', 'rating_std',
        'imdb_id', 'movie_tags'
    ]
    return dataset[dataset_col_order]


def _create_tables_if_not_exist(db_connection):
    db_connection.execute(
        """
        CREATE TABLE IF NOT EXISTS relatable_movies (
            movie_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            year INTEGER,
            genres TEXT,
            num_ratings INTEGER,
            rating_mean REAL,
            rating_median REAL,
            rating_std REAL,
            imdb_id TEXT,
            movie_tags TEXT
        ) 
        """
    ).fetchall()

    db_connection.execute(
        """
        CREATE TABLE IF NOT EXISTS unrelatable_movies (
            movie_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            year INTEGER,
            genres TEXT,
            num_ratings INTEGER,
            rating_mean REAL,
            rating_median REAL,
            rating_std REAL,
            imdb_id TEXT,
            movie_tags TEXT
        ) 
        """
    ).fetchall()

    db_connection.execute(
        """
        CREATE TABLE IF NOT EXISTS movie_similarity (
            first_movie_id INTEGER NOT NULL,
            second_movie_id INTEGER NOT NULL,                    
            similarity_score REAL,
            PRIMARY KEY (first_movie_id, second_movie_id)         
        ) 
        """
    ).fetchall()

    db_connection.execute(
        """
        CREATE TABLE IF NOT EXISTS user_likes (
            movie_id INTEGER PRIMARY KEY,
            movie_liked INTEGER         
        ) 
        """
    ).fetchall()


def _write_to_db_with_progress_bar(df, table_name, db_connection):
    total_length = len(df)
    step = int(total_length / 100)

    with tqdm(total=total_length) as pbar:
        for i in range(0, total_length, step):
            subset = df[i: i + step]
            subset.to_sql(table_name, db_connection, if_exists='append', index=False)
            pbar.update(step)


def create_and_populate_database(dataset, movie_to_movie_similarity, database_path):
    dataset_prepared = _prepare_dataset_for_db(dataset)
    has_movie_tag = ~dataset_prepared.movie_tags.isnull()
    relatable_movies = dataset_prepared[has_movie_tag]
    unrelatable_movies = dataset_prepared[~has_movie_tag]

    # CREATE TABLE WITH PKs BEFORE WRITING
    db_connection = _connect_to_database(database_path)

    _create_tables_if_not_exist(db_connection)

    print("writing movies with tags to DB...")
    _write_to_db_with_progress_bar(relatable_movies, 'relatable_movies', db_connection)

    print("writing movies without tags to DB...")
    _write_to_db_with_progress_bar(unrelatable_movies, 'unrelatable_movies', db_connection)

    print("writing movie similarities to DB...")
    _write_to_db_with_progress_bar(movie_to_movie_similarity, 'movie_similarity', db_connection)
