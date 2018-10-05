from flask import Flask
from flask import request
from flask import abort
from bson.json_util import dumps
from model import User
from model import Item
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
    except ValueError:
        abort(400)
    return user.username


@app.route("/users/<username>/items", methods=['POST'])
def add_item(username):
    data = request.json
    client = ABMongoClient.ABMongoClient('localhost', 27017)
    if not client.get_user(username):
        return abort(400)
    item = Item.Item(username, data["name"], data["link"])
    try:
        client.add_item(item)
    except ValueError:
        abort(400)
    return item.id


@app.route("/users", methods=['GET'])
def get_user():
    client = ABMongoClient.ABMongoClient('localhost', 27017)
    return dumps(client.get_user(request.args['username']))


@app.route("/users/<username>/items", methods=['GET'])
def get_item(username):
    query = {"user": username}
    if 'name' in request.args:
        query["name"] = request.args["name"]
    if 'link' in request.args:
        query["link"] = request.args["link"]
    client = ABMongoClient.ABMongoClient('localhost', 27017)
    return dumps(client.get_items(query))