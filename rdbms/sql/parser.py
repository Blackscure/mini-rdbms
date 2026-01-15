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

        if "(" not in tokens:
            return CreateTable(name, cols)

        try:
            open_paren_idx = tokens.index("(")
            close_paren_idx = tokens.index(")", open_paren_idx)
        except ValueError:
            raise Exception("Syntax error: Missing or unbalanced parentheses in CREATE TABLE")

        i = open_paren_idx + 1
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
            raw_tokens = tokens[values_start:values_end]
        except ValueError:
            raise Exception("Invalid INSERT syntax: missing or unbalanced parentheses")

        # Filter out commas and clean quotes/strings
        values = []
        i = 0
        while i < len(raw_tokens):
            token = raw_tokens[i].strip()

            if token == ",":
                i += 1
                continue

            # Handle quoted strings
            if (token.startswith("'") and token.endswith("'")) or \
               (token.startswith('"') and token.endswith('"')):
                cleaned = token[1:-1]
            else:
                cleaned = token

            values.append(cleaned)
            i += 1

        if not values:
            raise Exception("No values provided in INSERT statement")

        return Insert(table, values)

    # SELECT * FROM table [JOIN ...]
    if tokens[0] == "SELECT":
        if "JOIN" in tokens:
            try:
                from_idx = tokens.index("FROM")
                join_idx = tokens.index("JOIN")
                on_idx = tokens.index("ON")
                return Join(
                    tokens[from_idx + 1].upper(),
                    tokens[join_idx + 1].upper(),
                    tokens[on_idx + 1],
                    tokens[on_idx + 3]
                )
            except (ValueError, IndexError):
                raise Exception("Invalid JOIN syntax")

        try:
            from_idx = tokens.index("FROM")
            table_name = tokens[from_idx + 1].upper()
            return Select(table_name)
        except ValueError:
            raise Exception("SELECT statement missing FROM clause")

    # UPDATE table SET col = value [, col = value ...] [WHERE col = value]
    if tokens[0] == "UPDATE":
        if len(tokens) < 5:
            raise Exception("Incomplete UPDATE statement")

        table = tokens[1].upper()
        if tokens[2] != "SET":
            raise Exception("Expected SET after table name")

        updates = {}
        i = 3

        while i < len(tokens):
            col = tokens[i].upper()
            if i + 1 >= len(tokens) or tokens[i + 1] != "=":
                raise Exception(f"Expected = after {col}")

            i += 2
            if i >= len(tokens):
                raise Exception("Value missing after =")

            value = tokens[i]
            # Clean string literal
            if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
                value = value[1:-1]

            updates[col] = value
            i += 1

            if i < len(tokens) and tokens[i] == ",":
                i += 1
            elif i < len(tokens) and tokens[i].upper() == "WHERE":
                break
            else:
                break

        if not updates:
            raise Exception("No SET clauses found")

        where = None
        if i < len(tokens) and tokens[i].upper() == "WHERE":
            i += 1
            if i + 2 >= len(tokens):
                raise Exception("Incomplete WHERE")
            if tokens[i + 1] != "=":
                raise Exception("Only col = value supported in WHERE")
            where_col = tokens[i].upper()
            where_val = tokens[i + 2]
            if (where_val.startswith("'") and where_val.endswith("'")) or (where_val.startswith('"') and where_val.endswith('"')):
                where_val = where_val[1:-1]
            where = (where_col, where_val)
            i += 3

        if i < len(tokens) and tokens[i] != ";":
            raise Exception(f"Unexpected tokens: {' '.join(tokens[i:])}")

        return Update(table, updates, where)

    # DELETE FROM table [WHERE col = value]
    if tokens[0] == "DELETE":
        if len(tokens) < 4 or tokens[1] != "FROM":
            raise Exception("Expected: DELETE FROM table [WHERE ...]")

        table = tokens[2].upper()

        where = None
        i = 3

        if i < len(tokens) and tokens[i].upper() == "WHERE":
            i += 1
            if i + 2 >= len(tokens):
                raise Exception("Incomplete WHERE clause in DELETE")

            where_col = tokens[i].upper()
            if tokens[i + 1] != "=":
                raise Exception("Only simple 'col = value' supported in WHERE for now")

            where_val = tokens[i + 2]
            if (where_val.startswith("'") and where_val.endswith("'")) or (where_val.startswith('"') and where_val.endswith('"')):
                where_val = where_val[1:-1]
            where = (where_col, where_val)
            i += 3

        if i < len(tokens) and tokens[i] != ";":
            raise Exception(f"Extra tokens after DELETE: {' '.join(tokens[i:])}")

        return Delete(table, where)

    raise Exception(f"Unsupported SQL: {' '.join(tokens[:8])} ...")