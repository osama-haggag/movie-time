from django.contrib import admin

# Register your models here.
from movie_time_app.models import Movie, Similarity, Tag

admin.site.register(Movie)
admin.site.register(Similarity)
admin.site.register(Tag)