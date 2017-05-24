from movie_time_app.models import Movie, Similarity


def load_unrelatable_movies(n):
    return Movie.objects.filter(relatable=False).order_by('?')[:n]


def _filter_movies(similarities, n):
    similar_movies = []
    for similarity in similarities[:n]:
        similar_movie = similarity.second_movie
        similar_movies.append((similar_movie.title, similar_movie.movie_id))
    return similar_movies


def load_similar_movies(movie, n):
    similarities = Similarity.objects.filter(
        first_movie=movie.movie_id,
        second_movie__liked_or_not=None
    ).exclude(
        second_movie__movie_id=movie.movie_id
    ).order_by('-similarity_score')

    relevant_similar_movies = _filter_movies(similarities, n)
    return relevant_similar_movies