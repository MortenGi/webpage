from flask import Flask
from homepage import homepage

#This is a playground for flask

app = Flask(__name__)
app.register_blueprint(homepage, url_prefix="")

if __name__ == '__main__':
    app.run(debug=True, port= 8000)