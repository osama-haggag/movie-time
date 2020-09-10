from flask_server.models import DB


class UserLikes(DB.Model):
    __tablename__ = 'user_likes'
    movie_id = DB.Column(DB.INT, primary_key=True)
    movie_liked = DB.Column(DB.INT, nullable=False)
