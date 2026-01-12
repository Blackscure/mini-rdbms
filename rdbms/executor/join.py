def execute_join(stmt, manager):
    left = manager.current.get_table(stmt.left)
    right = manager.current.get_table(stmt.right)

    result = []
    for l in left.rows:
        for r in right.rows:
            if l[stmt.left_col] == r[stmt.right_col]:
                result.append({**l, **r})

    return result
