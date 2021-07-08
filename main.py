#improt flask app function from __init__
from website import create_app

#define 'app' as the flask app without running it
app = create_app()

#run the flask app w/ debugging
if __name__ == '__main__':
    app.run(debug=True)