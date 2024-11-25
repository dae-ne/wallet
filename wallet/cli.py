import datetime
import typer
from typing_extensions import Annotated

import wallet.storage as st
from ._config import INPUT_DATE_FORMAT

app = typer.Typer()


def run_app(*args, **kwargs):
    app(*args, **kwargs)


@app.command()
def income(
        amount: Annotated[float, typer.Argument(help="Amount of the income.")],
        description: Annotated[str, typer.Option('--message', '-m', help="Description of the income.")],
        date_str: Annotated[
            str, typer.Option('--date', '-d', help=f"Date of the income. Format: {INPUT_DATE_FORMAT}")] = ''
):
    date = _get_date_from_string(date_str) if date_str else datetime.datetime.now()
    key = st.add_event(amount, description, date)
    new_event = st.get_event(key)
    print()
    _print_event(new_event)


@app.command()
def expense(
        amount: Annotated[float, typer.Argument(help="Amount of the expense.")],
        description: Annotated[str, typer.Option('--message', '-m', help="Description of the expense.")],
        date_str: Annotated[
            str, typer.Option('--date', '-d', help=f"Date of the expense. Format: {INPUT_DATE_FORMAT}")] = ''
):
    date = _get_date_from_string(date_str) if date_str else datetime.datetime.now()
    key = st.add_event(-amount, description, date)
    new_event = st.get_event(key)
    print()
    _print_event(new_event)


@app.command()
def delete(
        event_id: Annotated[str, typer.Argument(help="ID of the event to delete.")]
):
    st.delete_event(event_id)
    print(f"Event with ID {event_id} was deleted.")


@app.command()
def log(
        number: Annotated[int, typer.Option('--number', '-n', help="Limit the number of events to output.")] = 5
):
    data = st.get_events(number)
    print()
    for event in data:
        _print_event(event)


@app.command()
def balance():
    print(st.get_balance())


def _print_event(event):
    print(f"id: {event['Time']}")
    print(f"value: {event['Value']}")
    print(f"description: {event['Description']}")
    print()


def _get_date_from_string(date_str: str):
    return datetime.datetime.strptime(date_str, INPUT_DATE_FORMAT)
