import re

def tokenize(sql: str):
    sql = sql.strip()

    tokens = re.findall(
        r"[A-Za-z_][A-Za-z0-9_]*|\d+|\(|\)|,|;",
        sql
    )

    return [t.upper() for t in tokens]