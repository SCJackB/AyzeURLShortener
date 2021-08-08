from flask import Flask


def create_app():
    #define 'app' as a Flask app
    app = Flask(__name__)
    #Cookie encryption key
    app.config['SECRET_KEY'] = 'OG57vlTo0k'

    #import the views blueprint from the 'website' package
    from .views import views

    #register the home URL
    app.register_blueprint(views, url_prefix='/')

    #run app
    return app