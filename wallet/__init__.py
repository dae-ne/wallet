from .cli import run_app

__all__ = ['run_app']

from .storage import table_exists, create_table

if not table_exists():
    print('Table does not exist. Creating table.')
    create_table()
