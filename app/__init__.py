from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder=".", template_folder=".")

TOKEN = "637218572:AAGmOxtvixXYH2KIL9cLA79Rt6dTMCYOjmc"
DEV_TOKEN = "718901828:AAFWTD6weU4c9KHrbpkmTd9Y-RRClVpSZXQ"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TELEGRAM_TOKEN'] = TOKEN

db = SQLAlchemy(app)

from . import main
