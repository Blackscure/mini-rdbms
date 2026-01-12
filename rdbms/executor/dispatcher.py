from rdbms.sql.tokenizer import tokenize
from rdbms.sql.parser import parse
from rdbms.sql.ast import *
from rdbms.executor.create import execute_create, execute_create_database
from rdbms.executor.insert import execute_insert
from rdbms.executor.select import execute_select
from rdbms.executor.update import execute_update
from rdbms.executor.delete import execute_delete
from rdbms.executor.join import execute_join
from rdbms.executor.show import execute_show_databases

def execute(sql, manager):
    stmt = parse(tokenize(sql))

    if isinstance(stmt, ShowDatabases):
        return execute_show_databases(manager)

    if isinstance(stmt, CreateDatabase):
        return execute_create_database(stmt, manager)

    if isinstance(stmt, UseDatabase):
        manager.use_database(stmt.name)
        return f"Using database '{stmt.name}'"

    if isinstance(stmt, CreateTable):
        return execute_create(stmt, manager)

    if isinstance(stmt, Insert):
        return execute_insert(stmt, manager)

    if isinstance(stmt, Select):
        return execute_select(stmt, manager)

    if isinstance(stmt, Update):
        return execute_update(stmt, manager)

    if isinstance(stmt, Delete):
        return execute_delete(stmt, manager)

    if isinstance(stmt, Join):
        return execute_join(stmt, manager)

    raise Exception("Unsupported SQL")
