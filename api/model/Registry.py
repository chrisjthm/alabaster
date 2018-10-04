from api.model import Item

class Registry:

    def __init__(self):
        self.items = []

    def add_item(self, name, link):
        item = Item.Item(name, link)
        self.items.append(item)

    def to_dict(self):
        doc = {}
        doc['items'] = []
        for item in self.items:
            doc['items'].append(item.toDict())
        return doc
