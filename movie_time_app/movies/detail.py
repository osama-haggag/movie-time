from movie_time_app.models import Movie, OnlineLink, Similarity, Tag
from movie_time_app.movies.loader import load_similar_movies

DETAIL_TEMPLATE_NAME = 'movie_detail.html'
DETAIL_TOP_N_SIMILARITIES = 40


def _load_movie_tags(movie_object):
    tag_objects = Tag.objects.filter(movie_id=movie_object.movie_id).order_by('-relevance')[:10]
    tags = ', '.join([tag_obj.tag for tag_obj in tag_objects])
    return tags


def _prepare_context(movie_object, similar_movies):
    links = OnlineLink.objects.get(movie_id=movie_object.movie_id)
    movie_tags = _load_movie_tags(movie_object)
    context = {
        'movie': {
            'name': movie_object.title,
            'id': movie_object.movie_id,
            'movielens_rating': movie_object.rating_mean,
            'movielens_num_ratings': movie_object.num_ratings,
            'liked_or_not': movie_object.liked_or_not,
            'relatable': movie_object.relatable,
            'tags': movie_tags
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