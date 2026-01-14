def execute_select(stmt, manager):
    if manager.current is None:
        raise Exception("No database selected")

    table = manager.current.get_table(stmt.table)
    return table.select()