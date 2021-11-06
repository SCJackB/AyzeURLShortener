from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("usernameEmail")
        password = request.form.get("password")
        if not email or not password:
            formMessage = "fieldError"
            return render_template("login.html", formMessage=formMessage)
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect(url_for("views.homePage"))
                else:
                    formMessage = "incorrectPassword"
                    return render_template("login.html", formMessage=formMessage)
            else:
                formMessage = "noUser"
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

        user = User.query.filter_by(email=email).first()
        if user:
            formMessage = "alreadyExists"
            return render_template("sign_up.html", formMessage=formMessage)
        elif not username or not email or not password1 or not password2:
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
            login_user((User.query.filter_by(email=email).first()), remember=True)

            return redirect(url_for("views.homePage"))

    else:
        return render_template("sign_up.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.homePage"))
