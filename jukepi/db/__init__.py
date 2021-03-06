# from flask import session
import logging

from flask_sqlalchemy import SQLAlchemy

from jukepi import app


logger = logging.getLogger(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
db_session = db.session


class DB:
    def create_all(self):
        db.drop_all()
        db.create_all()
        logger.info("done")
