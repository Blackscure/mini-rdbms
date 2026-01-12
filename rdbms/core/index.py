class Index:
    def __init__(self, unique=False):
        self.unique = unique
        self.map = {}

    def add(self, key, row):
        if self.unique and key in self.map:
            raise Exception("Unique constraint violation")
        self.map.setdefault(key, []).append(row)

    def remove(self, key, row):
        if key in self.map:
            self.map[key].remove(row)
            if not self.map[key]:
                del self.map[key]

    def find(self, key):
        return self.map.get(key, [])
