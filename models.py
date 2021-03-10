from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect db to Flask app"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User table."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    bio = db.Column(db.Text)
    likes = db.relationship("Lyrics", secondary="likes")

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user by Hashing password and adding user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Lyric(db.Model):
    """An individual set of Lyrics and it's info."""

    __tablename__ = "lyrics"

    id = db.Column(db.Integer, primary_key=True)
    lyrics = db.Column(db.Text, nullable=False)
    track_name = db.Column(db.Text, nullable=False)
    artist_name = db.Column(db.Text, nullable=False)
    album_name = db.Column(db.Text, nullable=False)
    album_image = db.Column(db.Text, nullable=False) 