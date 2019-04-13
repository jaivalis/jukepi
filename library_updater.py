##########################################
#  RUN THIS TO CREATE THE DATABASE FILE  #
##########################################
from flask import Flask

app = Flask(__name__)

import jukepi.db as db
import jukepi.db.dao as dao

database = db.DB()
database.create_all()

dao.persist_library(db.db_session, rebuild=True)
