import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _make_indices_and_columns_movie_ids(movies_with_tags, movie_to_movie_matrix):
    matrix_index_to_movie_id = movies_with_tags['movie_id']
    movie_to_movie_matrix.columns = [str(matrix_index_to_movie_id[int(col)]) for col in movie_to_movie_matrix.columns]
    movie_to_movie_matrix.index = [matrix_index_to_movie_id[idx] for idx in movie_to_movie_matrix.index]
    return movie_to_movie_matrix


def _stack_matrix_to_db_model(movie_to_movie_matrix):
    movie_to_movie_stacked = movie_to_movie_matrix.stack().reset_index()
    movie_to_movie_stacked.columns = ['first_movie_id', 'second_movie_id', 'similarity_score']
    return movie_to_movie_stacked


def _calculate_movie_similarity(movies_with_tags):
    print("calculating movie to movie similarity...")
    tf_idf = TfidfVectorizer()
    vectorized_movies = tf_idf.fit_transform(movies_with_tags.movie_tags)
    movie_to_movie_matrix = pd.DataFrame(cosine_similarity(vectorized_movies))
    movie_to_movie_matrix = _make_indices_and_columns_movie_ids(movies_with_tags, movie_to_movie_matrix)
    # movie_to_movie_stacked = _stack_matrix_to_db_model(movie_to_movie_matrix)
    return movie_to_movie_matrix


def compute_movie_to_movie_similarity(dataset):
    movies_with_tags = dataset[~dataset.movie_tags.isnull()].reset_index(drop=True)
    m2m_matrix = _calculate_movie_similarity(movies_with_tags)
    return m2m_matrix
