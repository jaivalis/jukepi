##########################################
#  RUN THIS TO CREATE THE DATABASE FILE  #
##########################################
from flask import Flask

app = Flask(__name__)

from JukePi.dao import DB
from JukePi.dao import db
from JukePi.dao.dao import persist_library

database = DB()
database.create_all()

persist_library(db.session, rebuild=True)
