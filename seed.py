from app import app
from models import db User, Lyric, Rating, Save


db.drop_all()
db.create_all()