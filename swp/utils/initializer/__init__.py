from .base import DatabaseInitializerException
from .postgres import PostgresInitialiser
from .sqlite import SQLiteInitialiser

__all__ = [
    'ENGINES',
    'DatabaseInitializerException',
]

ENGINES = {
    'postgresql': PostgresInitialiser,
    'postgresql_psycopg2': PostgresInitialiser,
    'postgis': PostgresInitialiser,
    'sqlite3': SQLiteInitialiser,
}
