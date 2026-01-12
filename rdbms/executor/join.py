from rdbms.core.database import db

def execute_join(stmt):
    left = db.get_table(stmt.left)
    right = db.get_table(stmt.right)
    results = []

    if stmt.right_key in right.indexes:
        idx = right.indexes[stmt.right_key]
        for l in left.rows:
            for rid in idx.map.get(l[stmt.left_key], []):
                results.append({**l, **right.rows[rid]})
    else:
        for l in left.rows:
            for r in right.rows:
                if l[stmt.left_key] == r[stmt.right_key]:
                    results.append({**l, **r})

    return results