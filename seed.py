from app import db
from models import User, Lyric, Like, Save


db.drop_all()
db.create_all()