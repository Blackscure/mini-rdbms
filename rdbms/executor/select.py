def execute_select(stmt, manager):
    table = manager.current.get_table(stmt.table)
    return table.select_all()