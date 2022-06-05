from flask import Blueprint         #to organize views so that they can be registered outside of the application
from flask import render_template   #to render e.g. html from templates (!) folder
from flask import request           #to accept and work with params
from flask import jsonify           #convert dict to json for a flask response
import json
import pickle

homepage = Blueprint(__name__,'homepage')

@homepage.route('/')
def home():
    #show stuff on groundpage
    return render_template('some_data.html', name = "Morti")

@homepage.route('/user/<username>')
def profile(username):
    #show dynamic content
    #on dynamic endpoint
    args = request.args
    age = args.get('age', default="YOU DIDNT TELL ME")
    return  render_template('some_data.html', name = username, age = age)

@homepage.route('/json')
def output():
    #return a json
    with open('jsons/data.js') as json_file:
        data = json.load(json_file)
    return jsonify(data)

@homepage.route('/send_here',  methods=['POST'])
def accept():
    #accept data on POST
    #example here: save the POSTed json locally
    #example for the POST request:
    #data = {"Value": 222, "pilot": 'Morten'}
    #x = requests.post("http://127.0.0.1:8000/send_here", json = data)

    data = request.json
    res_file = 'output/retreived_data.pkl'
    pickle.dump(data, open(res_file, 'wb'))
    return "saved"


