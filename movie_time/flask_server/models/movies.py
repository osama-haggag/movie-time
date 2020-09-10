from flask_server.models import DB


class RelatableMovie(DB.Model):
    __tablename__ = 'relatable_movies'
    movie_id = DB.Column(DB.INT, primary_key=True)
    title = DB.Column(DB.TEXT)
    year = DB.Column(DB.INT)
    title = DB.Column(DB.TEXT)
    num_ratings = DB.Column(DB.INT)
    ratings_mean = DB.Column(DB.REAL)
    ratings_median = DB.Column(DB.REAL)
    ratings_std = DB.Column(DB.REAL)
    movie_tags = DB.Column(DB.TEXT)


class UnrelatableMovie(DB.Model):
    __tablename__ = 'unrelatable_movies'
    movie_id = DB.Column(DB.INT, primary_key=True)
    title = DB.Column(DB.TEXT)
    year = DB.Column(DB.INT)
    title = DB.Column(DB.TEXT)
    num_ratings = DB.Column(DB.INT)
    ratings_mean = DB.Column(DB.REAL)
    ratings_median = DB.Column(DB.REAL)
    ratings_std = DB.Column(DB.REAL)
    movie_tags = DB.Column(DB.TEXT)


class MovieSimilarity(DB.Model):
    __tablename__ = 'movie_similarity'
    first_movie_id = DB.Column(DB.INT, primary_key=True)
    second_movie_id = DB.Column(DB.INT, primary_key=True)
    similarity_score = DB.Column(DB.REAL)
