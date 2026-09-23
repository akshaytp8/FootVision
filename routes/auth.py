from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, session)
from extensions import db
from models import User, UserScore

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    # Always go to dashboard first — no login wall
    return redirect(url_for("prediction.dashboard"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        security_answer = request.form.get("security_answer","").strip()

        if not username or not password:
            flash("Username and PIN are required.", "danger")
            return render_template("register.html")

        if not password.isdigit() or len(password) != 4:
            flash("PIN must be exactly 4 digits.", "danger")
            return render_template("register.html")

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "warning")
            return render_template("register.html")

        user = User(username=username)
        user.set_password(password)
        if security_answer:
            user.set_security_answer(security_answer)
        db.session.add(user)
        db.session.flush()
        db.session.add(UserScore(user_id=user.id))
        db.session.commit()

        # Log the user in right away — no need to sign in again
        session["user_id"]  = user.id
        session["username"] = user.username

        flash(f"Welcome, {user.username}! Account created ⚽", "success")
        return redirect(url_for("prediction.dashboard"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Wrong username or PIN.", "danger")
            return render_template("login.html")

        session["user_id"]  = user.id
        session["username"] = user.username
        flash(f"Welcome, {user.username}! ⚽", "success")
        return redirect(url_for("prediction.dashboard"))

    return render_template("login.html")

@auth_bp.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        answer = request.form.get("answer", "").strip()
        new_password = request.form.get("new_password", "").strip()

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User not found.", "danger")
            return render_template("forgot_password.html")

        if not user.security_answer_hash:
            flash(
                "Recovery not enabled for this account.",
                "warning"
            )
            return render_template("forgot_password.html")

        if not user.check_security_answer(answer):
            flash("Wrong answer.", "danger")
            return render_template("forgot_password.html")

        if not new_password.isdigit() or len(new_password) != 4:
            flash(
                "PIN must be exactly 4 digits.",
                "danger"
            )
            return render_template("forgot_password.html")

        user.set_password(new_password)

        db.session.commit()

        flash(
            "PIN changed successfully. Please login.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("forgot_password.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("prediction.dashboard"))  # goes to dashboard, not login