import re

def tokenize(sql: str):
    return re.findall(
        r"[A-Za-z_][A-Za-z0-9_]*|\d+|\(|\)|,|;|=",
        sql.upper()
    )
