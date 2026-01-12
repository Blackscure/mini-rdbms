from rdbms.core.table import Table

def execute_create(stmt, manager):
    if manager.current is None:
        raise Exception("No database selected")

    table = Table(stmt.name, stmt.columns)
    manager.current.create_table(stmt.name, table)

    return "Table created"


def execute_create_database(stmt, manager):
    manager.create_database(stmt.name)
    return f"Database '{stmt.name}' created"
