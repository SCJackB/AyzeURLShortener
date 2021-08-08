from flask import Blueprint, render_template

#set up the views blueprint
views = Blueprint('views', __name__)

#defining home view
@views.route('/')
def homePage():
    return render_template("base.html")