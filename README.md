![](/movie_time_app/static/logo.png)

A movie recommendation system based on the GroupLens dataset of MovieLens data.
The dataset contains about 40,000 movies, and around 11,000 of those have tags
associated with them and could be related to one another.

Movie Time uses these tagged movies to relate them to each other, and presents
random recommendations from the other 29,000 unrelatable movies.

[Screenshots!](https://imgur.com/a/cH3cs)

## Installation

### Virtual Environment
**0- Install python virtual env**

On ubuntu:

    $ apt-get install virtualenvwrapper

or via pip (for Linux, Mac and Linux subsystem for Windows) given you have python installed:
   
    $ pip install virtualenv virtualenvwrapper
    
Reset your terminal and the commands below should be available to use

**1- Create a *python 3* virtualenv for the project**

    $ mkvirtualenv movie-time -p /usr/bin/python3

**1.1- Activate the virtualenv if it's not automatically activated**

    $ workon movie-time

**2- Install the required dependencies**

    (movie-time) $ pip install -r requirements.txt

### Getting the movie database ready

#### Building the DB yourself

**1- Preferrably download the dataset manually from [here](http://files.grouplens.org/datasets/movielens/ml-latest.zip)
then extract it to a folder**

**2- Run the first time setup script from the project's root directory to populate a
local database with the data needed for the recommendations.** 

This takes between 50 minutes (on a MacBook Pro) to 
5 hours (on an MSI gaming laptop) and the database amounts to about 7 GB. Just point the script to the directory where
you extracted the dataset, and optionally (but not preferrably) the path of the DB, but then you'd have to change it in 
the django settings too.

    (movie-time) $ PYTHONPATH=. python first_time_setup/run.py -i /path/to/extracted/dataset

#### Downloading the DB from the cloud

The DB is also backed up on Google Drive, and can be downloaded directly from there but may be slow in case Google sets
bandwidth limits. 

Either download it to the default
path, which is the project root. Or, download it to a specific path but be sure to change the django settings to point
to that path.

Download it from [here](https://drive.google.com/file/d/0B4oaUOQPKT44QzhacnBjSkw1Tjg/view), the download is about 6GB.

### Starting the server

**1- Start the django server**

    (movie-time) $ python manage.py runserver
    
**2- Open the server in a browser, by default it's at: [127.0.0.1:8000](http://127.0.0.1:8000/) and rate away!**
    
## Usage
You can either: search for movies you watched and like/dislike them to see more candidates on the homepage, or you can
search for a movie you know you enjoyed and manually find yourself a promising candidate from the list of similar movies.

In the detail view it only shows the 40 most similar movies to the selected movie.
    
## How it works
The "science" behind the system can be found in the 
[investigation notebook](/movie_time_investigation.ipynb)

Recommendations on the homepage are presented in 3 categories, 2 of which are based on the calculated movie-to-movie similarity using
the provided genome tags.

**1. Movies similar to movies you have liked**

These are the movies that are the most similar to the ones you've liked. Recommendations on the homepage are presented
as follows: each movie you liked adds N (default 10) of its most similar movies to a pool of recommendations, which will
have `N * number of liked movies` movies in it. Out of this pool N movies (again 10) are randomly selected to ensure 
some mixture of your tastes.

**2. Movies similar to what you have disliked**

These are the highest rated movies that are the most similar to movies you disliked. The recommendations are presented
simply as a list of movies sorted by their mean_rating descendingly. The assumption is if a movie you didn't like got
something "wrong", maybe a high-rated and very similar movie to it got it "right".

**3. A random selection from the 29,000 that have no tags and can't be related due to them not having tags**
