from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from movie_time_app.models import Movie,UserDetails
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

def registerUser(request):
    u = UserDetails(fName = request.POST['name'], password = request.POST['password'], email = request.POST['email'])
    
    u.save()
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

def index2(request):
    response = render(request, 'index3.html')
    return response

def loginSuccess(request):
    response = render(request, 'loginSucess.html')
    return response
def dashboard(request):
    response = render(request, 'dashboard.html')
    return response


# def form(request):

    # if request.method == 'POST':

        # form = UserCreationForm(request.POST)

        # if form.is_valid():

            # form.save()

            # username = form.cleaned_data.get('username')

            # raw_password = form.cleaned_data.get('password1')

            # user = authenticate(username=username, password=raw_password)

            # login(request, user)

            # return redirect('home')

    # else:

        # form = UserCreationForm()

    # return render(request, 'signup.html', {'form': form})

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})