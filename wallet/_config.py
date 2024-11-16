from ._env import load_env, get_env

load_env()

STORAGE_CONNECTION_STRING = get_env('STORAGE_CONNECTION_STRING')
