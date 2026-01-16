from rdbms.core.database import DatabaseManager
from rdbms.sql.ast import CreateDatabase, CreateTable
from rdbms.executor.create import execute_create_database, execute_create

manager = DatabaseManager()

def init_db():
    execute_create_database(CreateDatabase("webdb"), manager)
    manager.use_database("webdb")

    execute_create(
        CreateTable(
            "users",
            {
                "id": {"type": "INT", "primary": True, "unique": True},
                "name": {"type": "TEXT", "primary": False, "unique": False}
            }
        ),
        manager
    )

init_db()