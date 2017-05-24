from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from movie_time_app.models import Movie
from movie_time_app.movies.detail import load_movie_detail
from movie_time_app.movies.homepage import load_homepage_recommendations
from movie_time_app.movies.search import search_for_query

INDEX_TEMPLATE_NAME = 'index.html'


def detail(request, movie_id):
    movie_detail, template_name = load_movie_detail(movie_id)
    return render(request, template_name, context=movie_detail)


def search(request):
    search_results, template_name = search_for_query(request.GET)
    return render(request, template_name, context=search_results)

def update(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if 'liked' in request.POST:
        movie.liked_or_not = True
    elif 'disliked' in request.POST:
        movie.liked_or_not = False
    elif 'reset' in request.POST:
        movie.liked_or_not = None

    movie.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def index(request):
    liked, not_liked, random = load_homepage_recommendations()
    context = {
        'liked': liked,
        'not_liked': not_liked,
        'random': random
    }
    response = render(request, 'index.html', context=context)
    return response
