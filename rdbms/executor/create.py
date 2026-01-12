from rdbms.core.table import Table

def execute_create(stmt, db):
    db.create_table(stmt.name, Table(stmt.name, stmt.columns))
    return "Table created"
