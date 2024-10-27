import typer
import storage as st

app = typer.Typer()


@app.command()
def income(amount: float, description: str):
    st.add_event(amount, description)


@app.command()
def expenses(amount: float, description: str):
    st.add_event(-amount, description)


@app.command()
def balance():
    print(st.get_balance())


@app.command()
def log():
    data = st.get_events()
    print()
    for event in data:
        print(f"time: {event['Time']}")
        print(f"value: {event['Value']}")
        print(f"description: {event['Description']}")
        print()


# @app.command()
# def weekly():
#     print("Weekly stats")
#
#
# @app.command()
# def monthly():
#     print("Monthly stats")


if __name__ == '__main__':
    app()
