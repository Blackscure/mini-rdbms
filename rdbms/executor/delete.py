def execute_delete(stmt, manager):
    table = manager.current.get_table(stmt.table)
    table.delete(stmt.where_col, stmt.where_val)
    return "Row(s) deleted"
