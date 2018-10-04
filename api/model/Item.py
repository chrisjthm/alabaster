class Item:

    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.claimed = False

    def claim_item(self):
        self.claimed = True

    def claimed(self):
        return self.claimed

    def to_dict(self):
        doc = {}
        doc['name'] = self.name
        doc['link'] = self.link
        doc['claimed'] = self.claimed
        return doc