from rdbms.core.database import db
from rdbms.core.index import HashIndex

def execute_create_index(stmt):
    table = db.get_table(stmt.table)
    idx = HashIndex()

    for i, row in enumerate(table.rows):
        idx.add(row[stmt.column], i)

    table.indexes[stmt.column] = idx
    return "Index created"
