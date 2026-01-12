from rdbms.core.database import DatabaseManager
from rdbms.sql.parser import parse
from rdbms.sql.tokenizer import tokenize
from rdbms.sql.ast import *

from rdbms.executor.create import execute_create
from rdbms.executor.insert import execute_insert
from rdbms.executor.select import execute_select
from rdbms.executor.update import execute_update
from rdbms.executor.delete import execute_delete

db_manager = DatabaseManager()
db_manager.create_database("default")
db_manager.use_database("default")

def execute(sql):
    stmt = parse(tokenize(sql.upper()))

    if isinstance(stmt, CreateDatabase):
        db_manager.create_database(stmt.name)
        return "Database created"

    if isinstance(stmt, UseDatabase):
        db_manager.use_database(stmt.name)
        return f"Using database {stmt.name}"

    if isinstance(stmt, CreateTable):
        return execute_create(stmt, db_manager.current)

    if isinstance(stmt, Insert):
        return execute_insert(stmt, db_manager.current)

    if isinstance(stmt, Select):
        return execute_select(stmt, db_manager.current)

    if isinstance(stmt, Update):
        return execute_update(stmt, db_manager.current)

    if isinstance(stmt, Delete):
        return execute_delete(stmt, db_manager.current)

    raise Exception("Unsupported SQL")