from flask import Blueprint         #to organize views so that they can be registered outside of the application
from flask import render_template   #to render e.g. html from templates (!) folder
from flask import request           #to accept and work with params
from flask import jsonify           #convert dict to json for a flask response
from flask import url_for
from flask import flash
import json
import pickle

views = Blueprint(__name__,'views')

@views.route('/', methods= ['GET', 'POST'])
def home():
    #show stuff on groundpage
    return render_template('home.html', name = "Morti")

@views.route('/login', methods= ['GET', 'POST'])
def login():
    data = request.form
    return render_template('login.html')

@views.route('/signup', methods= ['GET', 'POST'])
def signup():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        pw1=request.form.get('password1')
        pw2=request.form.get('password2')
        if len(email)<4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(firstName)<2:
            flash('first Name too short', category='error')
        elif pw1 != pw2:
            flash('passwords do not align', category='error')
        elif len(pw1)<7:
            flash('password too short', category='error')
        else:
            flash('user added', category='success')

    return render_template('singup.html')

@views.route('/user/<username>')
def profile(username):
    #show dynamic content
    #on dynamic endpoint
    args = request.args
    age = args.get('age', default="YOU DIDNT TELL ME")
    return  render_template('base.html', name = username, age = age)

@views.route('/json')
def output():
    #return a json
    with open('jsons/data.js') as json_file:
        data = json.load(json_file)
    return jsonify(data)

@views.route('/send_here',  methods=['POST'])
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
@views.route('/url',  methods=['GET'])
def url():
    return url_for('static', filename='index.js')
