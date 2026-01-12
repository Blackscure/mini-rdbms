from rdbms.core.index import Index

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []
        self.indexes = {}

        for col, meta in columns.items():
            if meta.get("primary") or meta.get("unique"):
                self.indexes[col] = Index(unique=True)

    def insert(self, row):
        for col, idx in self.indexes.items():
            idx.add(row[col], row)
        self.rows.append(row)

    def select(self, where=None):
        if not where:
            return self.rows
        col, val = where
        if col in self.indexes:
            return self.indexes[col].find(val)
        return [r for r in self.rows if r[col] == val]

    def update(self, where, updates):
        col, val = where
        rows = self.select(where)
        for row in rows:
            for k, v in updates.items():
                row[k] = v
        return len(rows)

    def delete(self, where):
        col, val = where
        rows = self.select(where)
        for row in rows:
            for c, idx in self.indexes.items():
                idx.remove(row[c], row)
            self.rows.remove(row)
        return len(rows)