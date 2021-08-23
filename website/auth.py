from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "login"

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("emailSignup")
        password1 = request.form.get("createPassword")
        password2 = request.form.get("confirmPassword")

        if not username or not email or not password1 or not password2:
            formMessage = 'fieldError'
            return render_template('sign_up.html',formMessage=formMessage)
        elif '@' not in email and '.' not in email:
            formMessage = 'emailError'
            return render_template('sign_up.html',formMessage=formMessage)
        elif len(username) < 3:
            formMessage = 'usernameError'
            return render_template('sign_up.html',formMessage=formMessage)
        elif password1 != password2:
            formMessage = 'matchError'
            return render_template('sign_up.html',formMessage=formMessage)
        elif len(password1) < 8:
            formMessage = 'passwordError'
            return render_template('sign_up.html',formMessage=formMessage)
        else:
            formMessage = 'success'
            return render_template('sign_up.html',formMessage=formMessage)

    return render_template('sign_up.html')