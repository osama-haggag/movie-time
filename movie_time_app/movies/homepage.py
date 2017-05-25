from movie_time_app.models import Movie
from movie_time_app.movies.loader import load_unrelatable_movies, load_similar_movies

TOP_N = 10


def _get_similar_movies(movies):
    all_similar_movies = []
    for movie in movies:
        all_similar_movies.extend(load_similar_movies(movie, TOP_N))
    movie_ids = [movie_id for _, movie_id in all_similar_movies]
    return Movie.objects.filter(movie_id__in=movie_ids)


def _load_similar_to_not_liked_movies(watched_movies):
    not_liked_movies = watched_movies.filter(liked_or_not=False, relatable=True)
    similar_movies = _get_similar_movies(not_liked_movies)
    return similar_movies.order_by('-rating_mean')


def _load_similar_to_liked_movies(watched_movies):
    liked_movies = watched_movies.filter(liked_or_not=True, relatable=True)
    similar_movies = _get_similar_movies(liked_movies)
    return similar_movies.order_by('?')


def _exclude_movies_in_similar_to_liked(similar_to_non_liked_movies, similar_to_liked_movies):
    similar_to_liked_ids = similar_to_liked_movies.values_list('movie_id', flat=True)
    from_disliked = similar_to_non_liked_movies.exclude(movie_id__in=similar_to_liked_ids)[:TOP_N]
    from_liked = similar_to_liked_movies[:TOP_N]
    return from_liked, from_disliked


def load_homepage_recommendations():
    watched_movies = Movie.objects.filter(liked_or_not__isnull=False)
    similar_to_liked_movies = _load_similar_to_liked_movies(watched_movies)
    similar_to_non_liked_movies = _load_similar_to_not_liked_movies(watched_movies)
    random_recommendations_from_unrelatable = load_unrelatable_movies(TOP_N)

    from_liked, from_disliked = _exclude_movies_in_similar_to_liked(similar_to_non_liked_movies, similar_to_liked_movies)
    return from_liked, from_disliked, random_recommendations_from_unrelatable