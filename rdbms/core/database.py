class Database:
    def __init__(self, name):
        self.name = name.upper()
        self.tables = {}

    def create_table(self, name, table):
        name = name.upper()
        if name in self.tables:
            raise Exception("Table already exists")
        self.tables[name] = table

    def get_table(self, name):
        name = name.upper()
        if name not in self.tables:
            raise Exception(f"Table not found: {name}")
        return self.tables[name]


class DatabaseManager:
    def __init__(self):
        self.databases = {}
        self.current = None

    def create_database(self, name):
        name = name.upper()
        if name in self.databases:
            raise Exception("Database already exists")
        self.databases[name] = Database(name)

    def use_database(self, name):
        name = name.upper()
        if name not in self.databases:
            raise Exception("Unknown database")
        self.current = self.databases[name]