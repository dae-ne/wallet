from benchmarks.time import time_log
from wallet.cli import run_app
from wallet.env import load_env, get_env

MAX_EXECUTION_TIME = 200


if __name__ == '__main__':
    load_env()
    environment = get_env('ENVIRONMENT')

    if environment == 'development':
        print('*** Running in development mode ***')
        time_log(MAX_EXECUTION_TIME)(run_app)(standalone_mode=False)
    else:
        run_app()
