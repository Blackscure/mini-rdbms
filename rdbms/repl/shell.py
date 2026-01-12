from rdbms.core.database import DatabaseManager
from rdbms.executor.dispatcher import execute

def start_repl():
    manager = DatabaseManager()
    manager.create_database("default")
    manager.use_database("default")

    print("MiniRDBMS v1.0")
    print("Type 'exit' to quit\n")

    while True:
        try:
            sql = input("sql> ")
            if sql.lower() in ("exit", "quit"):
                break
            print(execute(sql, manager))
        except Exception as e:
            print("Error:", e)