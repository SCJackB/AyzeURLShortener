from flask import Blueprint, render_template, request, redirect, url_for
import smtplib
import os
from flask_login import login_required, current_user
import pyshorteners
import urlexpander
from .models import urls
from . import db

# set up the views blueprint
views = Blueprint("views", __name__)

# defining home view
@views.route("/", methods=["POST", "GET"])
def homePage():
    if request.method == "POST":
        long_url = request.form.get("longURL")
        if long_url:
            try:
                shortened_url = pyshorteners.Shortener().isgd.short(long_url)
            except:
                return render_template(
                    "home.html", formMessage="badURL", user=current_user
                )
            try:
                new_urls = urls(
                    shorturl=shortened_url, longurl=long_url, user_id=current_user.id
                )
                db.session.add(new_urls)
                db.session.commit()
                return redirect(url_for("views.manager"))
            except:
                return render_template(
                    "home.html", formMessage="loginError", user=current_user
                )

        # creating the variables for the different input scenarios for the email form
        # get value from first name input
        firstName = request.form.get("firstName")
        # get value from last name input
        lastName = request.form.get("lastName")
        # get email address
        emailAddress = request.form.get("emailAddress")
        # get email subject
        emailSubject = request.form.get("emailSubject")
        # get email message
        emailMessage = request.form.get("emailMessage")

        # check if any of the input fields are blank
        if (
            not firstName
            or not lastName
            or not emailAddress
            or not emailSubject
            or not emailMessage
        ):
            # if they are blank, set the form message to 'field error' and run the render the 'home' webpage
            formMessage = "fieldError"
            return render_template(
                "home.html",
                formMessage=formMessage,
                emailMessage=emailMessage,
                user=current_user,
            )
        # if all fields have data...
        else:
            # check if the email address is valid
            if "@" in emailAddress and "." in emailAddress:
                # if the email address is valid...
                # format the gathered data for the email
                messageFormat = (
                    "Subject: "
                    + emailSubject
                    + "\n\n"
                    + "Name: "
                    + firstName
                    + " "
                    + lastName
                    + "\nEmail: "
                    + emailAddress
                    + "\nMessage:\n"
                    + emailMessage
                )
                # create an email server
                server = smtplib.SMTP("smtp.gmail.com", 587)
                # Identify self to server
                server.ehlo()
                # encrypt the connection to the server
                server.starttls()
                # re-identify
                server.ehlo()
                # store the email address that will send and recieve the emails as a string
                serverAddress = "ayze.xyz@gmail.com"
                # get the environmental variable that stores the password and store it as a string
                serverPassword = os.environ.get("AYZE_EMAILACC_PASSWORD")
                # try to log in to gmail
                server.login(serverAddress, serverPassword)
                # and try to send the email
                try:
                    server.sendmail(
                        "ayze.xyz@gmail.com", "ayze.xyz@gmail.com", messageFormat
                    )
                    # if both of those work, set form message to 'success'
                    formMessage = "success"
                    # and render the webpage
                    return render_template(
                        "home.html", formMessage=formMessage, user=current_user
                    )

                    # if login, or email fails...
                except Exception:
                    # set the form message to 'internal error'
                    formMessage = "internalError"
                    # and render the webpage
                    return render_template(
                        "home.html", formMessage=formMessage, user=current_user
                    )

            else:
                # if the email is invalid, set the form message to emailError
                formMessage = "emailError"
                # and render the webpage
                return render_template(
                    "home.html",
                    formMessage=formMessage,
                    emailMessage=emailMessage,
                    user=current_user,
                )
    else:
        # if no form submission, render the home template
        return render_template("home.html", user=current_user)


@views.route("/expander", methods=["POST", "GET"])
def expander():
    if request.method == "POST":
        shortURL = request.form.get("shortURL")
        if shortURL:
            expandedurl = urlexpander.expand(shortURL)
            print(expandedurl)
            return render_template(
                "expanded.html",
                user=current_user,
                expandedurl=expandedurl,
            )
        else:
            return render_template(
                "expander.html",
                user=current_user,
                formMessage="fieldError",
            )
    else:
        return render_template("expander.html", user=current_user)


@views.route("/manager")
@login_required
def manager():
    return render_template("manager.html", user=current_user)
