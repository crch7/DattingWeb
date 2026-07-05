from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from . import model

from pathlib import Path
from flask import current_app

bp = Blueprint("auth", __name__)


@bp.route("/signup")
def signup():
    return render_template("auth/signup.html")


@bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    password = request.form.get("password")
    # Check that passwords are equal
    if password != request.form.get("password_repeat"):
        flash("Sorry, passwords are different")
        return redirect(url_for("auth.signup"))
    # Check if the email is already at the database
    query = db.select(model.User).where(model.User.email == email)
    user = db.session.execute(query).scalar_one_or_none()
    if user:
        flash("Sorry, the email you provided is already registered")
        return redirect(url_for("auth.signup"))
    password_hash = generate_password_hash(password)
    new_user = model.User(email=email,  password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    flash("You've successfully signed up!")
    return redirect(url_for("main.create_profile"))


@bp.route("/login")
def login():
    return render_template("auth/login.html")


@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    query = db.select(model.User).where(model.User.email == email)
    user = db.session.execute(query).scalar_one_or_none()
    db.session.commit()
    
    if user and check_password_hash(user.password, password):
        # The user exists and the password is correct
        login_user(user)
        if user.profile:  # Assuming 'profile' is a relationship or attribute in the User model
            return redirect(url_for("main.search_matches"))
        else:
            return redirect(url_for("main.create_profile"))
    elif user:
        # The email exists, but the password is incorrect
        flash("Incorrect password. Please try again.")
        return redirect(url_for("auth.login"))
    else:
        # The email does not exist
        flash("There is no account for this email.")
        return redirect(url_for("auth.login"))

    
@bp.route('/logout') 
@login_required
def logout(): 
    logout_user() 
    return redirect(url_for('main.enter'))  
    






