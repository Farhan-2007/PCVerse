from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

# Signup
@auth.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            return "Username already exists!"

        user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template("signup.html")


# Login
@auth.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.password == password:

            login_user(user)

            return redirect(url_for('main.home'))

        return "Invalid Email or Password"

    return render_template("login.html")


# Logout
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for('main.home'))