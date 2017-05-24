from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    poster = models.ImageField(null=True, blank=True)
    year = models.IntegerField(null=True)
    genres = models.CharField(max_length=200)
    num_ratings = models.IntegerField(null=True)
    rating_median = models.FloatField(null=True)
    rating_mean = models.FloatField(null=True)
    relatable = models.BooleanField(default=True)
    liked_or_not = models.NullBooleanField(null=True, blank=True)

    def __str__(self):
        return self.title


class Similarity(models.Model):
    first_movie = models.ForeignKey(Movie, related_name='first_movie')
    second_movie = models.ForeignKey(Movie, related_name='second_movie')
    similarity_score = models.FloatField()


class Tag(models.Model):
    movie = models.ForeignKey(Movie)
    tag = models.CharField(max_length=50)
    relevance = models.FloatField()


class OnlineLink(models.Model):
    movie = models.ForeignKey(Movie)
    imdb_id = models.CharField(max_length=50)
