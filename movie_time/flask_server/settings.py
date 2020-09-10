import os

# Default DB path, can be changed
CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///movie-time.db' #os.path.join('sqlite:///', os.getcwd(), 'flask_server', 'movie-time.db')
}
