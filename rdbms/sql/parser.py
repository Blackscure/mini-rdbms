from rdbms.sql.ast import *

def parse(tokens):
    if not tokens:
        raise Exception("Empty query")

    # SHOW DATABASES
    if tokens[:2] == ["SHOW", "DATABASES"]:
        return ShowDatabases()

    # SHOW TABLES
    if tokens[:2] == ["SHOW", "TABLES"]:
        return ShowTables()

    # CREATE DATABASE dbname
    if tokens[:2] == ["CREATE", "DATABASE"]:
        if len(tokens) < 3:
            raise Exception("Missing database name")
        return CreateDatabase(tokens[2].upper())

    # USE database
    if tokens[0] == "USE":
        if len(tokens) < 2:
            raise Exception("Missing database name")
        return UseDatabase(tokens[1].upper())

    # CREATE TABLE name [ (col1 type, col2 type, ...) ]
    if tokens[:2] == ["CREATE", "TABLE"]:
        if len(tokens) < 3:
            raise Exception("Missing table name")

        name = tokens[2].upper()
        cols = {}

        # No parentheses → empty table
        if "(" not in tokens:
            return CreateTable(name, cols)

        # With parentheses → parse columns
        try:
            open_paren_idx = tokens.index("(")
            # Find the matching closing parenthesis (simple version - assumes no nested parens)
            close_paren_idx = tokens.index(")", open_paren_idx)
        except ValueError:
            raise Exception("Syntax error: Missing or unbalanced parentheses in CREATE TABLE")

        i = open_paren_idx + 1

        # Empty parentheses: CREATE TABLE name ()
        if i >= close_paren_idx:
            return CreateTable(name, cols)

        while i < close_paren_idx:
            if i + 1 >= close_paren_idx:
                raise Exception("Incomplete column definition near: " + " ".join(tokens[i-2:i+3]))

            col_name = tokens[i].upper()
            col_type = tokens[i + 1]

            cols[col_name] = {
                "type": col_type,
                "primary": False,
                "unique": False
            }

            i += 2

            # Handle comma separator or end of list
            if i < close_paren_idx:
                if tokens[i] == ",":
                    i += 1
                else:
                    raise Exception(f"Expected ',' or ')' after column but found '{tokens[i]}'")

        return CreateTable(name, cols)

    # INSERT INTO table VALUES (...)
    if tokens[0] == "INSERT" and tokens[1] == "INTO":
        if len(tokens) < 4:
            raise Exception("Incomplete INSERT statement")

        table = tokens[2].upper()

        try:
            values_start = tokens.index("(") + 1
            values_end = tokens.index(")", values_start)
            values = tokens[values_start:values_end]
        except ValueError:
            raise Exception("Invalid INSERT syntax: missing or unbalanced parentheses")

        return Insert(table, values)

    # SELECT * FROM table
    if tokens[0] == "SELECT":
        if "JOIN" in tokens:
            # Very basic JOIN support - improve later as needed
            try:
                from_idx = tokens.index("FROM")
                join_idx = tokens.index("JOIN")
                on_idx = tokens.index("ON")
                return Join(
                    tokens[from_idx + 1].upper(),     # left table
                    tokens[join_idx + 1].upper(),     # right table
                    tokens[on_idx + 1],               # left.col
                    tokens[on_idx + 3]                # right.col (assumes = was skipped in tokenizer)
                )
            except (ValueError, IndexError):
                raise Exception("Invalid JOIN syntax")

        # Simple SELECT FROM
        try:
            from_idx = tokens.index("FROM")
            table_name = tokens[from_idx + 1].upper()
            return Select(table_name)
        except ValueError:
            raise Exception("SELECT statement missing FROM clause")

    # UPDATE and DELETE not fully implemented yet
    if tokens[0] in ("UPDATE", "DELETE"):
        raise Exception(f"{tokens[0]} command parsing is not implemented yet")

    raise Exception(f"Unsupported SQL: {' '.join(tokens[:8])} ...")