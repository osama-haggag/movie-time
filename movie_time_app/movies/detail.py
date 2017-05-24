from movie_time_app.models import Movie, OnlineLink, Similarity
from movie_time_app.movies.loader import load_similar_movies

DETAIL_TEMPLATE_NAME = 'movie_detail.html'
DETAIL_TOP_N_SIMILARITIES = 40


def _prepare_context(movie_object, similar_movies):
    links = OnlineLink.objects.get(movie_id=movie_object.movie_id)
    context = {
        'movie': {
            'name': movie_object.title,
            'id': movie_object.movie_id,
            'movielens_rating': movie_object.rating_mean,
            'movielens_num_ratings': movie_object.num_ratings,
            'liked_or_not': movie_object.liked_or_not,
        },
        'links': {
            'imdb': links.imdb_id
        },
        'similarities': similar_movies
    }
    return context


def load_movie_detail(movie_id):
    movie_object = Movie.objects.get(movie_id=movie_id)
    similar_movies = load_similar_movies(movie_object, DETAIL_TOP_N_SIMILARITIES)
    detail = _prepare_context(movie_object, similar_movies)
    return detail, DETAIL_TEMPLATE_NAME