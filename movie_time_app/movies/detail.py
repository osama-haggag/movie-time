from movie_time_app.models import Movie

DETAIL_TEMPLATE_NAME = 'movie_detail.html'


def _prepare_context(movie_object):
    context = {
        'movie': {
            'name': movie_object.title,
            'genres': movie_object.genres.split('|'),
            'rating': movie_object.rating_mean
        }
    }
    return context


def load_movie_detail(movie_id):
    movie_object = Movie.objects.get(movie_id=movie_id)
    detail = _prepare_context(movie_object)
    return detail, DETAIL_TEMPLATE_NAME