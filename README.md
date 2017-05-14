# Movie Time
A movie recommendation system based on the GroupLens dataset of MovieLens data.
The dataset contains about 40,000 movies, and around 11,000 of those have tags
associated with them.

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
