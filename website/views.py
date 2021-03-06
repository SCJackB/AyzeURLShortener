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
    # If the website sends data...
    if request.method == "POST":
        # Check if the long url input box has data
        long_url = request.form.get("longURL")
        # if it does contain data...
        if long_url:
            # Try to shorten the input with the isgd api
            try:
                shortened_url = pyshorteners.Shortener().isgd.short(long_url)
            # If it cant...
            except:
                # Prompt the user to enter a valid long url
                return render_template(
                    "home.html", formMessage="badURL", user=current_user
                )
            # Try to commit the urls to the database
            try:
                new_urls = urls(
                    shorturl=shortened_url, longurl=long_url, user_id=current_user.id
                )
                db.session.add(new_urls)
                db.session.commit()
                return redirect(url_for("views.manager"))
            # If it cant...
            except:
                # Prompt the user to login
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


# Create a route for the url expander
@views.route("/expander", methods=["POST", "GET"])
def expander():
    # If the website sends data...
    if request.method == "POST":
        # Check if the short url input box has data
        shortURL = request.form.get("shortURL")
        # If the input box contains data...
        if shortURL:
            # Try to expand the data in the input box into a long url with the urlexpander module
            try:
                expandedurl = urlexpander.expand(shortURL)
                return render_template(
                    "expanded.html",
                    user=current_user,
                    expandedurl=expandedurl,
                )
            # If it cant...
            except:
                # Prompt the user to enter a valid short url
                return render_template(
                    "expander.html",
                    user=current_user,
                    formMessage="badURL",
                )
        # If the input box is empty...
        else:
            # Prompt the user to enter a valid short url
            return render_template(
                "expander.html",
                user=current_user,
                formMessage="fieldError",
            )
    # If the website doesn't send any data, return the expander.html template
    else:
        return render_template("expander.html", user=current_user)


# defign a route for the url manager
@views.route("/manager")
# this page is only accessable if the user is logged in
@login_required
def manager():
    # Return the manager.html template
    return render_template("manager.html", user=current_user)
