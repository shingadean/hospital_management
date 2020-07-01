from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restplus import Api
from werkzeug.utils import cached_property

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = "b'vY\x12\xe9$\xa2\xa8M\\d\xa9+\xf3\x1c\xec8'"

db =MongoEngine()
db.init_app(app)


from application import routes