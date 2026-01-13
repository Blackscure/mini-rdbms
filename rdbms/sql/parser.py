from rdbms.sql.ast import *

def parse(tokens):
    if tokens[:2] == ["SHOW", "DATABASES"]:
        return ShowDatabases()
    
    if tokens[:2] == ["SHOW", "TABLES"]:
        return ShowTables()

    if tokens[:2] == ["CREATE", "DATABASE"]:
        return CreateDatabase(tokens[2])

    if tokens[0] == "USE":
        return UseDatabase(tokens[1])

    if tokens[:2] == ["CREATE", "TABLE"]:
        name = tokens[2]
        cols = {}

        i = tokens.index("(") + 1
        while tokens[i] != ")":
            col_name = tokens[i]
            col_type = tokens[i + 1]

            cols[col_name] = {
                "type": col_type,
                "primary": False,
                "unique": False
            }

            i += 2
            if tokens[i] == ",":
                i += 1

        return CreateTable(name, cols)


    if tokens[0] == "INSERT":
        table = tokens[2]
        values = tokens[tokens.index("(")+1 : tokens.index(")")]
        return Insert(table, values)

    if tokens[0] == "SELECT" and "JOIN" in tokens:
        return Join(tokens[3], tokens[5], tokens[7], tokens[9])

    if tokens[0] == "SELECT":
        return Select(tokens[3])

    if tokens[0] == "UPDATE":
        return Update(tokens[1], tokens[3], tokens[5], tokens[7], tokens[9])

    if tokens[0] == "DELETE":
        return Delete(tokens[2], tokens[4], tokens[6])

    raise Exception("Unsupported SQL")