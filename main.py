from typer import Typer
from storage import table_exists, create_table
from cli import register_commands

app = Typer()


def create_table_if_not_exists():
    if not table_exists():
        create_table()


if __name__ == '__main__':
    create_table_if_not_exists()
    register_commands(app)
    app()
