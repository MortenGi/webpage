from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from views import views

#This is a playground for flask

db = SQLAlchemy()
DB_NAME = "database.db"

app = Flask(__name__)
app.register_blueprint(views, url_prefix="")
app.secret_key = 'dasda'
app.config['SQLALCHEMY_DATA_URI'] = f'sqlite:///{DB_NAME}'


if __name__ == '__main__':
    app.run(debug=True, port= 8000)