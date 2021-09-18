from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import time

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usernameEmail = request.form.get("usernameEmail")
        password = request.form.get("password")
        if not usernameEmail or not password:
            formMessage = "fieldError"
            return render_template("login.html", formMessage=formMessage)
    else:
        return render_template("login.html")


@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("emailSignup")
        password1 = request.form.get("createPassword")
        password2 = request.form.get("confirmPassword")

        if not username or not email or not password1 or not password2:
            formMessage = "fieldError"
            return render_template("sign_up.html", formMessage=formMessage)
        elif "@" not in email and "." not in email:
            formMessage = "emailError"
            return render_template("sign_up.html", formMessage=formMessage)
        elif len(username) < 3:
            formMessage = "usernameError"
            return render_template("sign_up.html", formMessage=formMessage)
        elif password1 != password2:
            formMessage = "matchError"
            return render_template("sign_up.html", formMessage=formMessage)
        elif len(password1) < 8:
            formMessage = "passwordError"
            return render_template("sign_up.html", formMessage=formMessage)
        else:
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("views.homePage"))

    else:
        return render_template("sign_up.html")
