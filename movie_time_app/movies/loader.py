from movie_time_app.models import Movie, LikedOrNot, Similarity


TOP_N = 10

def load_unrelatable_movies(n):
    return Movie.objects.filter(relatable=False).order_by('?')[:n]


def _get_similar_movies(movies):
    top_movies = []
    for movie in movies:
        similar_movies = Similarity.objects.filter(first_movie=movie.movie_id)
        unseen_similar_movies = similar_movies.filter(movie_id__not_in=movies).order_by('similarity_score')[:TOP_N]
        top_movies.append(unseen_similar_movies)
    return top_movies


def _load_similar_to_liked_movies():
    liked_movies = LikedOrNot.objects.all().order_by('?')
    similar_movies = _get_similar_movies(liked_movies)
    print(similar_movies)


    #movies = Movie.objects.filter(relatable=True).order_by('')


def load_recommendations():
    similar_movies = _load_similar_to_liked_movies()