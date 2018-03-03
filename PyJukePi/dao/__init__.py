# from flask import session
from flask_sqlalchemy import SQLAlchemy

from PyJukePi import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
db_session = db.session

from PyJukePi.dao.models import Artist, Album, Track, CoverArt


class DB:
    def create_all(self):
        db.drop_all()
        db.create_all()
        print("done")
