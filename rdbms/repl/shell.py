from rdbms.executor.dispatcher import execute

def start_repl():
    print("MiniRDBMS v1.0")
    while True:
        try:
            sql = input("sql> ").strip()
            if sql.lower() in ("exit", "quit"):
                break
            print(execute(sql))
        except Exception as e:
            print("Error:", e)