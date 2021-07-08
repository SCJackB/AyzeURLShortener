from flask import Flask


def create_app():
    #run 'app' as a Flask app
    app = Flask(__name__)
    #Cookie encryption key
    app.config['SECRET_KEY'] = 'OG57vlTo0k'

    #run flask app
    return app