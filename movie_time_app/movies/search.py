import operator
from functools import reduce

from django.db.models import Q

from movie_time_app.models import Movie

SEARCH_TEMPLATE_NAME = 'search.html'


def _combine_filters(all_movies, query_elems):
    filtered = all_movies.filter(
        reduce(operator.and_,
               (Q(title__icontains=q) for q in query_elems))
    )
    return filtered


def _prepare_as_context(filtered):
    context = {'search_results': filtered}
    return context


def _filter_for_query(query):
    all_movies = Movie.objects.all()
    query_elems = query.split()
    filtered = _combine_filters(all_movies, query_elems)
    result = _prepare_as_context(filtered)
    return result


def search_for_query(request):
    query = request.get('q')
    result = _filter_for_query(query)
    return result, SEARCH_TEMPLATE_NAME
