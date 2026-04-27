"""
routes/auth.py
--------------
Register, login, and logout.
"""

from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, session)
from extensions import db
from models import User, UserScore

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("prediction.dashboard"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "warning")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "warning")
            return render_template("register.html")

        # Create user and their leaderboard entry
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        db.session.add(UserScore(user_id=user.id))
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password   = request.form.get("password", "")

        # Allow login with username OR email
        user = (User.query.filter_by(username=identifier).first() or
                User.query.filter_by(email=identifier).first())

        if not user or not user.check_password(password):
            flash("Wrong username or password.", "danger")
            return render_template("login.html")

        session["user_id"]  = user.id
        session["username"] = user.username
        flash(f"Welcome, {user.username}! ⚽", "success")
        return redirect(url_for("prediction.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
