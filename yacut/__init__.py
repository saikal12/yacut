from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from settings import Config

app = Flask('__name__')
app.config.from_object(Config)
db = SQLAlchemy(app)
migration = Migrate(app, db)
