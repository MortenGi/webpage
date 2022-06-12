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
from flask_login import login_user, login_required, logout_user, current_user #manages what pages we can access and cant

auth = Blueprint('auth', __name__,)


@auth.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method=='POST':
        email       =request.form.get('email')
        pw          = request.form.get('password')
        if email!='mortengiese@gmx.de':
            flash('Not Admin Login', category = 'neutral')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.pw, pw):
                flash('Logged in!', category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Try again', category="error")
        else:
            flash('User does not exist', category="error")


    return render_template('login.html', user=current_user) #if else in base.html ensures that we can access or cant access e.g. home and logout by passing user=current_user

@auth.route('/signup', methods= ['GET', 'POST'])
def signup():
    if request.method=='POST':
        email       =request.form.get('email')
        firstName   =request.form.get('firstName')
        pw1         =request.form.get('password1')
        pw2         =request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category='error')
        elif len(email)<4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(firstName)<2:
            flash('First Name must be greater than 1 character', category='error')
        elif pw1 != pw2:
            flash('Passwords do not align', category='error')
        elif len(pw1)<7:
            flash('Password too short', category='error')
        else:
            new_user = User(email=email, first_name=firstName, pw=generate_password_hash(pw1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account added!', category='success')
            return redirect(url_for('views.home'))
    return render_template('singup.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
