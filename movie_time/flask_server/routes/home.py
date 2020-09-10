from flask import Blueprint, render_template

from flask_server.models.users import UserLikes
from flask_server.models.movies import RelatableMovie, UnrelatableMovie, MovieSimilarity

home_bp = Blueprint('home', __name__, template_folder='templates')

#
# def _get_similar_movies(movies):
#     all_similar_movies = []
#     for movie in movies:
#         all_similar_movies.extend(load_similar_movies(movie, TOP_N))
#     movie_ids = [movie_id for _, movie_id in all_similar_movies]
#     return Movie.objects.filter(movie_id__in=movie_ids)
#
#
# def _load_similar_to_disliked_movies(watched_movies):
#     not_liked_movies = watched_movies.filter(liked_or_not=False, relatable=True)
#     similar_movies = _get_similar_movies(not_liked_movies)
#     return similar_movies.order_by('-rating_mean')
#
#
# def _load_similar_to_liked_movies(watched_movies):
#     liked_movies = watched_movies.filter(liked_or_not=True, relatable=True)
#     similar_movies = _get_similar_movies(liked_movies)
#     return similar_movies.order_by('?')
#
#
# def _exclude_movies_in_similar_to_liked(similar_to_non_liked_movies, similar_to_liked_movies):
#     similar_to_liked_ids = similar_to_liked_movies.values_list('movie_id', flat=True)
#     from_disliked = similar_to_non_liked_movies.exclude(movie_id__in=similar_to_liked_ids)[:TOP_N]
#     from_liked = similar_to_liked_movies[:TOP_N]
#     return from_liked, from_disliked
#
#
def _load_watched_movies():
    watched_movies = DB_MANAGER.query_as_df('SELECT movie_id FROM user_likes;')
    return watched_movies
#
#
# def load_homepage_recommendations():
#     watched_movies = _load_watched_movies()
#     similar_to_liked_movies = _load_similar_to_liked_movies(watched_movies)
#     similar_to_disliked_movies = _load_similar_to_disliked_movies(watched_movies)
#     random_recommendations_from_unrelatable = load_unrelatable_movies(TOP_N)
#
#
# def load_homepage_recommendations():
#     from_liked, from_disliked = _exclude_movies_in_similar_to_liked(similar_to_non_liked_movies, similar_to_liked_movies)
#     return from_liked, from_disliked, random_recommendations_from_unrelatable


def _recommend_similar_to_liked_movies(all_watched_movies):
    pass


def _recommend_similar_to_disliked_movies(all_watched_movies):
    pass


def _recommend_movies_from_unrelatable_liked(all_watched_movies):
    pass


@home_bp.route('/')
def page():
    #all_watched_movies = _load_watched_movies()
    all_watched_movies = UserLikes.query.first()
    print(all_watched_movies)
    recommendations_similar_to_liked = _recommend_similar_to_liked_movies(all_watched_movies)
    recommendations_similar_to_disliked = _recommend_similar_to_disliked_movies(all_watched_movies)
    random_movies_from_unrelatable_liked = _recommend_movies_from_unrelatable_liked(all_watched_movies)
    return render_template(
        'home.html',
        liked_recommendations=recommendations_similar_to_liked,
        disliked_recommendations=recommendations_similar_to_disliked,
        surprise_recommendations=random_movies_from_unrelatable_liked
    )
