from flask import Blueprint         #to organize views so that they can be registered outside of the application
from flask import render_template   #to render e.g. html from templates (!) folder
from flask import request           #to accept and work with params
from flask import jsonify           #convert dict to json for a flask response
from flask import url_for           #better to find url for eg function to avoid manual changing urls if one changes links to this function
from flask import flash
from flask import redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
import json
import pickle
from . import db
from flask_login import login_required, current_user
from .models import Note
import json #used to get notes via post and java

views = Blueprint('views', __name__,)

@views.route('/', methods= ['GET', 'POST'])
@login_required
def home():
    #show stuff on groundpage

    if request.method == 'POST':
        note = request.form.get('note')
        name = current_user.first_name

        if len(note) < 1:
            flash('Note must be greater than 1 character', category='error')
        else:
            new_note=Note(data = note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash(f'Note to user {name} is saved', category='success')



    return render_template('home.html', user=current_user)

@views.route('/delete-note',  methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({}) #need to response something


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
