from flask import Blueprint, flash, render_template, request, redirect, url_for
from app import db
from app.models import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


# ================= SIGNUP =================

@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if (
            not username
            or not email
            or "@" not in email
            or any(character.isspace() for character in email)
            or not password
            or len(username) > 20
            or len(email) > 120
            or len(password) > 1024
        ):
            flash("Enter valid account details and try again.", "error")
            return render_template("signup.html"), 400

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("That username is already in use.", "error")
            return render_template("signup.html"), 409

        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            flash("An account with that email already exists.", "error")
            return render_template("signup.html"), 409

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("signup.html")


# ================= LOGIN =================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and password and check_password_hash(user.password, password):

            login_user(user)

            return redirect(url_for("main.home"))

        flash("Invalid email or password.", "error")
        return render_template("login.html"), 401

    return render_template("login.html")


# ================= LOGOUT =================

@auth.route("/logout", methods=["POST"])
@login_required
def logout():

    logout_user()

    return redirect(url_for("main.home"))