from django.shortcuts import render

from movie_time_app.movies.loader import load_unrelatable_movies


def index(request):
    unrelatable = load_unrelatable_movies(5)
    context = {
        'unrelatable': unrelatable
    }
    return render(request, 'index.html', context=context)