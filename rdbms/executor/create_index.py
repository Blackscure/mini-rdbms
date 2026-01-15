from rdbms.core.index import Index

def execute_create_index(stmt, manager):
    if manager.current is None:
        raise Exception("No database selected")

    table = manager.current.get_table(stmt.table)

    if stmt.column not in table.columns:
        raise Exception(
            f"Column '{stmt.column}' does not exist in table '{stmt.table}'"
        )

    # Create index
    idx = Index(unique=False)

    # Build index from existing rows
    for row in table.rows:
        value = row.get(stmt.column)
        if value is not None:
            idx.add(value, row)

    table.indexes[stmt.column] = idx
    return f"Index created on {stmt.table}.{stmt.column}"
