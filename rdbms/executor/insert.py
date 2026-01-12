def execute_insert(stmt, db):
    table = db.get_table(stmt.table)
    row = dict(zip(table.columns.keys(), stmt.values))
    table.insert(row)
    return "Row inserted"
