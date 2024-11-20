from .cli import run_app
from .env import load_env, get_env

__all__ = ['run_app', 'load_env', 'get_env']

from .storage import table_exists, create_table

if not table_exists():
    print('Table does not exist. Creating table.')
    create_table()
