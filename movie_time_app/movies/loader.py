from movie_time_app.models import Movie


def load_unrelatable_movies(n):
    return Movie.objects.filter(relatable=False).order_by('?')[:n]