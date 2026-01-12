def execute_update(stmt, db):
    table = db.get_table(stmt.table)
    return f"{table.update(stmt.where, stmt.updates)} rows updated"