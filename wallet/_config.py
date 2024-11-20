from .env import load_env, get_env

load_env()

INPUT_DATE_FORMAT = get_env('INPUT_DATE_FORMAT')
STORAGE_CONNECTION_STRING = get_env('STORAGE_CONNECTION_STRING')
STORAGE_DATE_FORMAT = get_env('STORAGE_DATE_FORMAT')
