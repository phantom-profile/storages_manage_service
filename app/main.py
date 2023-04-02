from sqlite3 import Connection

from flask import Flask
from config import DB_PATH

db = Connection(DB_PATH).cursor()
app = Flask(__name__)


@app.get('/')
def main_page():
    return "<h1>Hello, World!</h1>"
