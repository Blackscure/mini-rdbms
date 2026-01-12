def execute_select(stmt, db):
    table = db.get_table(stmt.table)
    return table.rows