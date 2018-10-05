from api.model import Registry

import uuid

class User:

    def __init__(self, username):
        self.username = username
        self.claimedItems = []
        self.items = []

    def claim_item(self, item):
        self.claimedItems.append(item)

    def add_item(self, item):
        self.items.append(item)

    def to_dict(self):
        doc = {}
        doc['username'] = self.username
        return doc