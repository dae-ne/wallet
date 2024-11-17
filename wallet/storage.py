from azure.data.tables import TableServiceClient
from datetime import datetime
from time import gmtime, strftime

from ._config import STORAGE_CONNECTION_STRING, STORAGE_DATE_FORMAT

TABLE_NAME = 'events'


def get_table_client():
    return TableServiceClient.from_connection_string(conn_str=STORAGE_CONNECTION_STRING)


def table_exists():
    with get_table_client() as client:
        return TABLE_NAME in [table.name for table in client.list_tables()]


def create_table():
    with get_table_client() as client:
        table = client.create_table(TABLE_NAME)
        return table


def add_event(value: float, description: str, date: datetime):
    with get_table_client() as client:
        table = client.get_table_client(TABLE_NAME)
        id = date.strftime(STORAGE_DATE_FORMAT) if date else strftime(STORAGE_DATE_FORMAT, gmtime())
        entity = {
            'PartitionKey': 'wallet',
            'RowKey': id,
            'Value': value,
            'Description': description
        }
        table.create_entity(entity=entity)


def get_events(number: int):
    with get_table_client() as client:
        table = client.get_table_client(TABLE_NAME)
        events = table.query_entities("PartitionKey eq 'wallet'")
        data = [{'Value': e['Value'], 'Time': e['RowKey'], 'Description': e['Description']} for e in events]
        data.sort(key=lambda x: x['Time'], reverse=True)
        return data[:number]  # TODO: check if it can be done in the query


def get_balance():
    with get_table_client() as client:
        table = client.get_table_client(TABLE_NAME)
        events = table.query_entities("PartitionKey eq 'wallet'")
        balance = sum([e['Value'] for e in events])
        return balance
