import datetime
import typer
from typing_extensions import Annotated

import wallet.storage as st

app = typer.Typer()


def run_app():
    app()


@app.command()
def income(
        amount: Annotated[float, typer.Argument(help="Amount of the income.")],
        description: Annotated[str, typer.Option('--message', '-m', help="Description of the income.")],
        date_str: Annotated[
            str, typer.Option('--date', '-d', help="Date of the income. Format: %Y-%m-%d %H:%M:%S")] = ''
):
    date = _get_date_from_string(date_str) if date_str else datetime.datetime.now()
    st.add_event(amount, description, date)


@app.command()
def expense(
        amount: Annotated[float, typer.Argument(help="Amount of the expense.")],
        description: Annotated[str, typer.Option('--message', '-m', help="Description of the expense.")],
        date_str: Annotated[
            str, typer.Option('--date', '-d', help="Date of the expense. Format: %Y-%m-%d %H:%M:%S")] = ''
):
    date = _get_date_from_string(date_str) if date_str else datetime.datetime.now()
    st.add_event(-amount, description, date)


@app.command()
def log(
        number: Annotated[int, typer.Option('--number', '-n', help="Limit the number of events to output.")] = 10
):
    data = st.get_events(number)
    print()
    for event in data:
        print(f"id: {event['Time']}")
        print(f"value: {event['Value']}")
        print(f"description: {event['Description']}")
        print()


@app.command()
def balance():
    print(st.get_balance())


def _get_date_from_string(date_str: str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')