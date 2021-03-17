from app import db
from models import User, Lyric, Rating, Save


db.drop_all()
db.create_all()