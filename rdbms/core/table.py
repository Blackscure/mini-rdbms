from rdbms.core.index import Index

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns  # dict: column_name → metadata dict
        self.rows = []          # list of dicts: each row is {col_name: value, ...}
        self.indexes = {}

        for col, meta in columns.items():
            if meta.get("primary") or meta.get("unique"):
                self.indexes[col] = Index(unique=meta.get("unique", False))

    def insert(self, row):
        # row must be a dict {column_name: value, ...}
        for col, idx in self.indexes.items():
            value = row.get(col)
            if value is not None:
                idx.add(value, row)
        self.rows.append(row)
        return 1

    def select(self, where=None):
        if not where:
            return self.rows[:]

        col, val = where
        if col in self.indexes:
            return self.indexes[col].find(val)

        # fallback scan
        return [r for r in self.rows if r.get(col) == val]

    def update(self, where, updates):
        """
        where:   None or tuple (column_name, value)
        updates: dict {column_name: new_value, ...}
        Returns: number of rows affected
        """
        if where is None:
            rows_to_update = self.rows[:]
        else:
            col, val = where
            if col in self.indexes:
                rows_to_update = self.indexes[col].find(val)
            else:
                rows_to_update = [r for r in self.rows if r.get(col) == val]

        affected_rows = 0
        for row in rows_to_update:
            for col_name, new_value in updates.items():
                if col_name not in self.columns:
                    continue
                old_value = row.get(col_name)
                row[col_name] = new_value
                affected_rows += 1

                # Maintain index if this column is indexed
                if col_name in self.indexes:
                    if old_value is not None:
                        self.indexes[col_name].remove(old_value, row)
                    self.indexes[col_name].add(new_value, row)

        return affected_rows

    def delete(self, where):
        """
        where: tuple (column_name, value) or None (delete all)
        Returns: number of rows deleted
        """
        if where is None:
            count = len(self.rows)
            self.rows.clear()
            for idx in self.indexes.values():
                idx.clear()  # assuming Index has clear() method
            return count

        col, val = where
        rows_to_delete = self.select(where)
        for row in rows_to_delete:
            for c, idx in self.indexes.items():
                value = row.get(c)
                if value is not None:
                    idx.remove(value, row)
            self.rows.remove(row)
        return len(rows_to_delete)