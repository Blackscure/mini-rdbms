def execute_update(stmt, manager):
    table = manager.current.get_table(stmt.table)
    
    rows_updated = table.update(
        where=stmt.where,
        updates=stmt.updates
    )
    
    return f"{rows_updated} row(s) updated"