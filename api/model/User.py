from api.model import Registry

import uuid

class User:

    def __init__(self, username):
        self.username = username
        self.id = uuid.uuid4().hex
        self.claimedItems = []

    def claim_item(self, item):
        self.claimedItems.append(item)

    def add_registry(self):
        self.registry = Registry.Registry()

    def to_dict(self):
        doc = {}
        doc['username'] = self.username
        return doc