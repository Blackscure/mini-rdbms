def execute_delete(stmt, db):
    table = db.get_table(stmt.table)
    return f"{table.delete(stmt.where)} rows deleted"