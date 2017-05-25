# Movie Time
A movie recommendation system based on the GroupLens dataset of MovieLens data.
The dataset contains about 40,000 movies, and around 11,000 of those have tags
associated with them and could be related to one another.

Movie Time uses these tagged movies to relate them to each other, and presents
random recommendations from the other 29,000 unrelatable movies.

## Installation

**1- Create a *python 3* virtualenv for the project**

    $ mkvirtualenv movie-time -p /usr/bin/python3

**1.1- Activate the virtualenv if it's not automatically activated**

    $ workon movie-time

**2- Install the required dependencies**

    (movie-time) $ pip install -r requirements.txt

**3- Preferrably download the dataset manually from [here](http://files.grouplens.org/datasets/movielens/ml-latest.zip)
then extract it to a folder**

**4- Run the first time setup script from the project's root directory to populate a
local database with the data needed for the recommendations. This takes about 30 minutes
and the database amounts to about 7 GB.**

    (movie-time) $ PYTHONPATH=. python first_time_setup/run.py -i /path/to/extracted/dataset

**5- Start the django server**

    (movie-time) $ python manage.py runserver
    
## Usage
You can either: search for movies you watched and like/dislike them to see more candidates on the homepage, or you can
search for a movie you know you enjoyed and manually find yourself a promising candidate from the list of similar movies
    
## How it works
Recommendations on the homepage are presented in 3 categories, 2 of which are based on the calculated movie-to-movie similarity using
the provided genome tags.

**1. Movies similar to movies you have liked**

These are the movies that are the most similar to the ones you've liked. Recommendations on the homepage are presented
as follows: each movie you liked adds N (default 10) of its most similar movies to a pool of recommendations, out of
which N movies (again 10) are randomly selected to ensure some mixture of your tastes.

**2. Movies similar to what you have disliked**

These are the highest rated movies that are the most similar to movies you disliked. The recommendations are presented
simply as a list of movies sorted by their mean_rating descendingly. The assumption is if a movie you didn't like got
something "wrong", maybe a high-rated and very similar movie to it got it "right".

**3. A random selection from the 29,000 that have no tags and can't be related based on that**