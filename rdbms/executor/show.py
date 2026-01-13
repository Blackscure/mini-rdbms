def execute_show_databases(manager):
    return "\n".join(manager.databases.keys())

def execute_show_tables(manager):
    if manager.current is None:
        raise Exception("No database selected")

    if not manager.current.tables:
        return "No tables found"

    return "\n".join(manager.current.tables.keys())