from flask import Flask
from flask import request
from bson.json_util import dumps
from model import User
from service import ABMongoClient

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world"


@app.route("/users", methods=['POST'])
def add_user():
    data = request.json
    client = ABMongoClient.ABMongoClient('localhost', 27017)
    user = User.User(data['username'])
    try:
        client.add_user(user)
    except ValueError as e:
        return str(e)
    return user.id


@app.route("/users", methods=['GET'])
def get_user():
    client = ABMongoClient.ABMongoClient('localhost', 27017)
    return dumps(client.get_user(request.args['username']))