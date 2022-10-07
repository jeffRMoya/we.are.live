from cgitb import text
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import requests
import random

auth = Blueprint('auth', __name__)
avatar_url = "https://api.unsplash.com/"
api_key = "&client_id=mj5PFE4ahehmfQbuAf6ct5mFI3UFKxGNpe_Wq9Yq8yQ"


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist in database.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        avatar = request.form.get('avatar')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters', category='error')
        else:
            if len(avatar) == 0:
                rand_num = random.randint(0, 9)
                resp = requests.get(
                    f'{avatar_url}search/photos?query=cat{api_key}')
                avatar = resp.json()['results'][rand_num]['urls']['thumb']
            new_user = User(email=email, avatar=avatar, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            if new_user.id:
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Error, account creation failed', category='error')

    return render_template("sign_up.html", user=current_user)
