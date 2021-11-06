from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

# Create the routing blueprint for the sub domains of the website
auth = Blueprint("auth", __name__)

# Define the subdomain for the login page as '/login'
@auth.route("/login", methods=["POST", "GET"])
def login():
    # If the website sends data to the flask server...
    if request.method == "POST":
        # Gather data from the input boxes
        email = request.form.get("usernameEmail")
        password = request.form.get("password")
        # If the input boxes are empty...
        if not email or not password:
            # Return the webpage with a field error
            formMessage = "fieldError"
            return render_template("login.html", formMessage=formMessage)
        # if the input boxes are both full
        else:
            # Check if a user with this email exists
            user = User.query.filter_by(email=email).first()
            # If they do exist...
            if user:
                # Hash the password they entered, and check if it matches the hash stored in the database
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    # if the password matches, redirect to the homepage
                    return redirect(url_for("views.homePage"))
                # If the password Doesnt Match...
                else:
                    # Return the login form with an error message
                    formMessage = "incorrectPassword"
                    return render_template("login.html", formMessage=formMessage)
            # If the user Does not exist, Return the login form with an error message
            else:
                formMessage = "noUser"
                return render_template("login.html", formMessage=formMessage)
    # If the website does not send data, render the webpage as usual
    else:
        return render_template("login.html")


# Create a route for the signup page under '/sign-up'
@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    # if the website sends data...
    if request.method == "POST":
        # Gather data from the input boxes
        username = request.form.get("username")
        email = request.form.get("emailSignup")
        password1 = request.form.get("createPassword")
        password2 = request.form.get("confirmPassword")

        # Check if a user with this email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            # If they do, Dont let them create a new account
            formMessage = "alreadyExists"
            return render_template("sign_up.html", formMessage=formMessage)
        # Check if the input boxes are all full
        elif not username or not email or not password1 or not password2:
            # If not, prompt them with a message asking for the input boxes to be filled in
            formMessage = "fieldError"
            return render_template("sign_up.html", formMessage=formMessage)
        # check if the email adress is valid
        elif "@" not in email and "." not in email:
            # if it isnt, Prompt them to enter a valid email
            formMessage = "emailError"
            return render_template("sign_up.html", formMessage=formMessage)
        # Check the length of the username
        elif len(username) < 3:
            # if the username is shorter than 3 chharacters, ask the user to enter a longer username
            formMessage = "usernameError"
            return render_template("sign_up.html", formMessage=formMessage)
        # Check if the both the password entry boxes match
        elif password1 != password2:
            # If they dont, prompt the user that the passwords dont match
            formMessage = "matchError"
            return render_template("sign_up.html", formMessage=formMessage)
        # Check the length of the password
        elif len(password1) < 8:
            # If the password is too short, Promt the user that the password is too short
            formMessage = "passwordError"
            return render_template("sign_up.html", formMessage=formMessage)
        # If everything is entered correctly...
        else:
            # Commit the new user to the database
            new_user = User(
                email=email,
                username=username,
                # Generate a hash for the password so that the raw password isnt stored in the database
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            # login the user
            login_user((User.query.filter_by(email=email).first()), remember=True)
            # and redirect to teh homepage
            return redirect(url_for("views.homePage"))

    # if the website doesnt send any data, render the signup form
    else:
        return render_template("sign_up.html")


# Defign a route to logout the user
@auth.route("/logout")
# User authentication is required to access this route
@login_required
def logout():
    # User the logout user function for the flask_login module to logout the user
    logout_user()
    # Redirect to the homepage
    return redirect(url_for("views.homePage"))
