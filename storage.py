from azure.data.tables import TableServiceClient
from datetime import datetime
from dotenv import load_dotenv
from time import gmtime, strftime
import os
import sys

APP_NAME = 'wallet'
CONNECTION_STRING_KEY = 'STORAGE_CONNECTION_STRING'
ID_DATE_FORMAT = '%Y%m%d%H%M%S'
TABLE_NAME = 'events'

exe_file = sys.executable
exe_file_name = os.path.basename(exe_file)

if APP_NAME in exe_file_name:
    env_path = os.path.join(os.path.dirname(exe_file), '.env')
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

connection_string = os.getenv(CONNECTION_STRING_KEY)

if not connection_string:
    connection_string_key = f'{APP_NAME.upper()}_{CONNECTION_STRING_KEY}'
    connection_string = os.getenv(connection_string_key)

if not connection_string:
    raise ValueError(f'Connection string not found in environment variables. Key: {CONNECTION_STRING_KEY}')


def get_table_client():
    return TableServiceClient.from_connection_string(conn_str=connection_string)


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
        id = date.strftime(ID_DATE_FORMAT) if date else strftime(ID_DATE_FORMAT, gmtime())
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
