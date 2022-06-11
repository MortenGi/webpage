from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.secret_key = 'dasda'
    app.config['SQLALCHEMY_DATA_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix="")

    from .models import User, Note
    create_db(app)
    return app

def create_db(app):
    if not path.exists('webpage/'+ DB_NAME):
        db.create_all(app=app)
        print('created database')