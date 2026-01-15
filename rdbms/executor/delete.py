def execute_delete(stmt, manager):
    table = manager.current.get_table(stmt.table)
    count = table.delete(stmt.where)
    return f"{count} row(s) deleted"