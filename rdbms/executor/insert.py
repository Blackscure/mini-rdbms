def execute_insert(stmt, manager):
    table = manager.current.get_table(stmt.table)
    table.insert(stmt.values)
    return "Row inserted"
