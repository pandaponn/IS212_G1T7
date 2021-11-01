import flask
import time

app = flask.Flask(__name__)
# test

@app.route("/")
def index():
    return "Welcome!!! ", time.localtime