from flask import Flask
import logging
import sys

log_format = '%(asctime)s %(levelname)s %(name)s | %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)

app = Flask(__name__)

from jukepi.dao import DB

# database = DB()
# database.create_all()
