from movie_time_app.models import Movie, OnlineLink

DETAIL_TEMPLATE_NAME = 'movie_detail.html'


def _prepare_context(movie_object):
    links = OnlineLink.objects.get(movie_id=movie_object.movie_id)
    context = {
        'movie': {
            'name': movie_object.title,
            'movielens_rating': movie_object.rating_mean,
            'movielens_num_ratings': movie_object.num_ratings
        },
        'links': {
            'imdb': links.imdb_id
        }
    }
    return context


def load_movie_detail(movie_id):
    movie_object = Movie.objects.get(movie_id=movie_id)
    detail = _prepare_context(movie_object)
    return detail, DETAIL_TEMPLATE_NAME