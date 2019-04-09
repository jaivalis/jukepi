##########################################
#  RUN THIS TO CREATE THE DATABASE FILE  #
##########################################
from flask import Flask

app = Flask(__name__)

from jukepi.dao import db, DB
from jukepi.dao.dao import persist_library

database = DB()
database.create_all()

persist_library(db.session, rebuild=True)
