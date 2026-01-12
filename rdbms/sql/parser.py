from rdbms.sql.ast import *

def parse(tokens):
    if not tokens:
        raise Exception("Empty SQL")

    # 🔥 MUST BE FIRST
    if tokens[0] == "SHOW" and tokens[1] == "DATABASES":
        return ShowDatabases()

    if tokens[0] == "CREATE" and tokens[1] == "DATABASE":
        return CreateDatabase(tokens[2])

    if tokens[0] == "USE":
        return UseDatabase(tokens[1])

    if tokens[0] == "CREATE" and tokens[1] == "TABLE":
        table_name = tokens[2]
        columns = {}

        i = tokens.index("(") + 1
        while tokens[i] != ")":
            col_name = tokens[i]
            col_type = tokens[i + 1]
            columns[col_name] = {"type": col_type}
            i += 2
            if tokens[i] == ",":
                i += 1

        return CreateTable(table_name, columns)

    raise Exception("Unsupported SQL")
