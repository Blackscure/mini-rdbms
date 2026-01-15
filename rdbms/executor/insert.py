def execute_insert(stmt, manager):
    table = manager.current.get_table(stmt.table)
    col_names = list(table.columns.keys())
    
    if len(stmt.values) > len(col_names):
        raise Exception(f"Too many values: expected at most {len(col_names)}, got {len(stmt.values)}")
    
    row = {}
    for i, value in enumerate(stmt.values):
        col_name = col_names[i]
        row[col_name] = value
    
    # Remaining columns get None/null
    for remaining_col in col_names[len(stmt.values):]:
        row[remaining_col] = None
    
    table.insert(row)
    return "1 row inserted"