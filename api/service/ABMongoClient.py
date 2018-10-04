from pymongo import MongoClient

import datetime

class ABMongoClient:

    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.db = self.client.alabaster

    def add_registry(self, registry):
        doc = registry.to_dict()
        doc['inUTC'] = datetime.datetime.utcnow()
        doc['version'] = 1
        registries = self.db.registries
        return registries.insert_one(registry).inserted_id

    def add_user(self, user):
        doc = user.to_dict()
        if self.get_user(doc["username"]):
            raise ValueError("Username " + doc["username"] + " already used.")
        doc['inUTC'] = datetime.datetime.utcnow()
        doc['version'] = 1
        users = self.db.users
        return users.insert_one(doc).inserted_id

    def get_user(self, username):
        users = self.db.users
        return users.find_one({"username": username})
