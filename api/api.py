from flask import Flask
from flask import request
from flask import abort
from bson.json_util import dumps
import logging
from model import User
from model import Item
from service import ABMongoClient

app = Flask(__name__)

white = ['http://localhost:4200']


@app.route("/users", methods=['GET'])
def get_users():
    client = ABMongoClient.ABMongoClient('localhost', 27017)
    output = {"users": client.get_users()}
    return dumps(output)


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


@app.route("/users/<username>/items", methods=['GET'])
def get_items(username):
    query = {"user": username}
    if 'name' in request.args:
        query["name"] = request.args["name"]
    if 'link' in request.args:
        query["link"] = request.args["link"]
    client = ABMongoClient.ABMongoClient('localhost', 27017)
    return dumps(client.get_items(query))


@app.route("/users/<username>/items/<itemname>", methods=['GET'])
def get_item(username, itemname):
    client = ABMongoClient.ABMongoClient('localhost', 27017)
    return dumps(client.get_item(username, itemname))


@app.route("/users/<username>/items/<itemname>", methods=["PUT"])
def update_item(username, itemname):
    print("updating item")
    client = ABMongoClient.ABMongoClient('localhost', 27017)
    data = request.json
    current_item = client.get_item(username, itemname)
    if not current_item:
        logging.error("item " + username + itemname + " does not exist")
        abort(400)
    if 'claimed' in data:
        if data["claimed"].lower() == "true":
            current_item["claimed"] = True
        if data["claimed"].lower() == "false":
            current_item["claimed"] = False
    if 'link' in data:
        current_item["link"] = data["link"]
    logging.info("item will be updated with: " + str(current_item))
    return dumps(client.update_item(current_item))


@app.after_request
def add_cors_headers(response):
    if request.referrer:
        r = request.referrer[:-1]
        if r in white:
            response.headers.add('Access-Control-Allow-Origin', r)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
            response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
            response.headers.add('Access-Control-Allow-Headers', 'Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    return response