from azure.data.tables import TableEntity, TableServiceClient
from datetime import datetime
from time import gmtime, strftime

from ._config import STORAGE_CONNECTION_STRING, STORAGE_DATE_FORMAT

TABLE_NAME = 'events'
SELECT_PROPERTIES = ['Value', 'RowKey', 'Description']


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
        key = date.strftime(STORAGE_DATE_FORMAT) if date else strftime(STORAGE_DATE_FORMAT, gmtime())
        entity = {
            'PartitionKey': 'wallet',
            'RowKey': key,
            'Value': value,
            'Description': description
        }
        table.create_entity(entity=entity)
        return key


def get_events(number: int):
    with get_table_client() as client:
        table = client.get_table_client(TABLE_NAME)
        events = table.query_entities("PartitionKey eq 'wallet'", select=SELECT_PROPERTIES)
        data = [_get_domain_event_object(e) for e in events]
        data.sort(key=lambda x: x['Time'], reverse=True)
        return data[:number]


def get_event(key: str):
    with get_table_client() as client:
        table = client.get_table_client(TABLE_NAME)
        event = table.get_entity(partition_key='wallet', row_key=key, select=SELECT_PROPERTIES)
        return _get_domain_event_object(event)


def get_balance():
    with get_table_client() as client:
        table = client.get_table_client(TABLE_NAME)
        events = table.query_entities("PartitionKey eq 'wallet'")
        balance = sum([e['Value'] for e in events])
        return balance


def _get_domain_event_object(entity: TableEntity):
    return {
        'Value': entity['Value'],
        'Time': entity['RowKey'],
        'Description': entity['Description']
    }
