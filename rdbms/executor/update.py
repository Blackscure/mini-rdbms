def execute_update(stmt, manager):
    table = manager.current.get_table(stmt.table)
    table.update(stmt.col, stmt.val, stmt.where_col, stmt.where_val)
    return "Row(s) updated"
