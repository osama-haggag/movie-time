from django.http import HttpResponse
from django.shortcuts import render

from movie_time_app.movies.detail import load_movie_detail
from movie_time_app.movies.loader import load_unrelatable_movies
from movie_time_app.movies.search import search_for_query

INDEX_TEMPLATE_NAME = 'index.html'


def detail(request, movie_id):
    movie_detail, template_name = load_movie_detail(movie_id)
    return render(request, template_name, context=movie_detail)


def index(request):
    if request.method == 'GET' and len(request.GET) > 0:
        search_results, template_name = search_for_query(request.GET)
        return render(request, template_name, context=search_results)

    unrelatable = load_unrelatable_movies(5)
    context = {
        'unrelatable': unrelatable
    }
    return render(request, 'index.html', context=context)
