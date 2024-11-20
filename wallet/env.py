from dotenv import load_dotenv
import sys
import os

APP_NAME = 'wallet'


def load_env():
    if not _is_executable():
        load_dotenv()
        return

    env_path = os.path.join(os.path.dirname(sys.executable), '.env')
    load_dotenv(dotenv_path=env_path)


def get_env(key: str):
    env = os.getenv(key)

    if env:
        return env

    key_with_prefix = f'{APP_NAME.upper()}_{key}'
    env = os.getenv(key_with_prefix)

    if env:
        return env

    raise ValueError(f'Environment variable not found. Key: {key}')


def _is_executable():
    exe_file_name = os.path.basename(sys.executable)
    return APP_NAME in exe_file_name
