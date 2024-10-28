import typer
import storage as st
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def income(
        amount: Annotated[float, typer.Option('--amount', '-a', help="Amount of the income.")],
        description: Annotated[str, typer.Option('--description', '-d', help="Description of the income.")]
):
    st.add_event(amount, description)


@app.command()
def expense(
        amount: Annotated[float, typer.Option('--amount', '-a', help="Amount of the expense.")],
        description: Annotated[str, typer.Option('--description', '-d', help="Description of the expense.")]
):
    st.add_event(-amount, description)


@app.command()
def log(
        number: Annotated[int, typer.Option('--number', '-n', help="Limit the number of events to output.")] = 10
):
    data = st.get_events(number)
    print()
    for event in data:
        print(f"time: {event['Time']}")
        print(f"value: {event['Value']}")
        print(f"description: {event['Description']}")
        print()


@app.command()
def balance():
    print(st.get_balance())


# @app.command()
# def weekly():
#     print("Weekly stats")
#
#
# @app.command()
# def monthly():
#     print("Monthly stats")


def create_table_if_not_exists():
    if not st.table_exists():
        st.create_table()


if __name__ == '__main__':
    create_table_if_not_exists()
    app()
