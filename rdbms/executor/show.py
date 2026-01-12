def execute_show_databases(manager):
    return "\n".join(manager.databases.keys())
