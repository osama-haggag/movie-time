import re

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RELEVANCE_CUTOFF = 0.3


def _concatenate_tags_of_movie(tags):
    tags_as_str = ' '.join(set(tags))
    return tags_as_str


def _get_tags_per_movie(genome_scores, genome_tags):
    relevant_tags = genome_scores[genome_scores.relevance > RELEVANCE_CUTOFF][['movieId', 'tagId']]
    movie_id_to_relevant_tags = pd.merge(relevant_tags, genome_tags, on='tagId', how='left')[['movieId', 'tagId']]
    movie_id_to_relevant_tags['tagId'] = movie_id_to_relevant_tags.tagId.astype(str)
    relevant_tags_per_movie = movie_id_to_relevant_tags.groupby('movieId')['tagId'].agg({
        'movie_tags': _concatenate_tags_of_movie
    })
    return relevant_tags_per_movie.reset_index()


def _calculate_avg_movie_ratings(movie_ratings):
    avg_ratings = movie_ratings.groupby('movieId')['rating'].agg({
        'rating_mean': 'mean',
        'rating_median': 'median',
        'num_ratings': 'size'
    })
    return avg_ratings.reset_index()


def _extract_year_from_movie_title(movie_title):
    matches = re.findall(r'\d{4}', movie_title)
    if len(matches) > 1:
        return int(matches[-1])
    if len(matches) < 1:
        return np.nan
    return int(matches[0])


def _gather_dataset(movie_names, avg_movie_ratings, tags_per_movie):
    print("merging files into one dataset dataframe...")
    movies_with_ratings = pd.merge(movie_names, avg_movie_ratings, on='movieId')
    dataset = pd.merge(movies_with_ratings, tags_per_movie, on='movieId', how='left')

    dataset['year'] = dataset.title.apply(_extract_year_from_movie_title)
    dataset.rename(columns={'movieId': 'movie_id'}, inplace=True)

    movies_with_tags_mask = dataset.movie_tags.notnull()
    movies_without_ratings_mask = dataset.movie_tags.isnull()
    dataset_with_tags = dataset[movies_with_tags_mask].reset_index(drop=True)
    unrelatable_movies = dataset[(~movies_with_tags_mask) | (movies_without_ratings_mask)]
    return dataset_with_tags, unrelatable_movies


def _vectorize_dataset(dataset):
    tf_idf = TfidfVectorizer()
    movies_tfidf_vectorized = tf_idf.fit_transform(dataset.movie_tags)
    return movies_tfidf_vectorized


def _match_indices_and_columns_to_ids(dataset, movie_to_movie_matrix):
    index_to_movie_id = dataset['movie_id']
    movie_to_movie_matrix.columns = [str(index_to_movie_id[int(col)]) for col in movie_to_movie_matrix.columns]
    movie_to_movie_matrix.index = [index_to_movie_id[idx] for idx in movie_to_movie_matrix.index]
    return movie_to_movie_matrix


def _stack_matrix_to_db_model(movie_to_movie_matrix):
    movie_to_movie_stacked = movie_to_movie_matrix.stack().reset_index()
    movie_to_movie_stacked.columns = ['first_movie_id', 'second_movie_id', 'similarity_score']
    return movie_to_movie_stacked


def _calculate_movie_similarity(dataset, vectorized):
    print("calculating movie to movie similarity...")
    movie_to_movie_matrix = pd.DataFrame(cosine_similarity(vectorized))
    movie_to_movie_matrix = _match_indices_and_columns_to_ids(dataset, movie_to_movie_matrix)
    movie_to_movie_stacked = _stack_matrix_to_db_model(movie_to_movie_matrix)
    return movie_to_movie_stacked


def movie_to_movie(genome_scores, genome_tags, movie_names, movie_ratings):
    tags_per_movie = _get_tags_per_movie(genome_scores, genome_tags)
    avg_movie_ratings = _calculate_avg_movie_ratings(movie_ratings)
    dataset_with_tags, unrelatable_movies = _gather_dataset(movie_names, avg_movie_ratings, tags_per_movie)
    vectorized = _vectorize_dataset(dataset_with_tags)
    movie_to_movie_similarity = _calculate_movie_similarity(dataset_with_tags, vectorized)
    return movie_to_movie_similarity, dataset_with_tags, unrelatable_movies
