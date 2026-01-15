class CreateDatabase:
    def __init__(self, name): self.name = name

class UseDatabase:
    def __init__(self, name): self.name = name

class CreateIndex:
    def __init__(self, table, column):
        self.table = table
        self.column = column


class ShowDatabases:
    pass

class ShowTables:
    pass
class CreateTable:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns

class Insert:
    def __init__(self, table, values):
        self.table = table
        self.values = values

class Select:
    def __init__(self, table, where=None):
        self.table = table
        self.where = where

class Update:
    def __init__(self, table, updates, where):
        self.table = table
        self.updates = updates
        self.where = where

class Delete:
    def __init__(self, table, where):
        self.table = table
        self.where = where


class Join:
    def __init__(self, left, right, left_col, right_col):
        self.left = left
        self.right = right
        self.left_col = left_col
        self.right_col = right_col