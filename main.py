import typer

from storage import create_table, get_table


app = typer.Typer()


@app.command()
def create_table_test(table_name: str):
    create_table(table_name)


@app.command()
def get_table_test(table_name: str):
    get_table(table_name)


@app.command()
def init(name: str, value: float):
    print(f"Initializing a new account for {name} with a value of {value}")


@app.command()
def income(amount: float):
    print(f"Your income is {amount}")


@app.command()
def expenses(amount: float):
    print(f"Your expenses are {amount}")


@app.command()
def balance():
    print("Your balance is 1000")


@app.command()
def recent():
    print("Recent operations")


@app.command()
def weekly():
    print("Weekly stats")


@app.command()
def monthly():
    print("Monthly stats")


if __name__ == '__main__':
    app()
