from azure.data.tables import TableServiceClient
import os
from dotenv import load_dotenv
from time import gmtime, strftime

load_dotenv()
CONNECTION_STRING = os.getenv('STORAGE_CONNECTION_STRING')


def get_table_client():
    return TableServiceClient.from_connection_string(conn_str=CONNECTION_STRING)


def add_event(value: float, description: str):
    with get_table_client() as client:
        table = client.get_table_client('events')
        entity = {
            'PartitionKey': 'wallet',
            'RowKey': strftime("%Y%m%d%H%M%S", gmtime()),
            'Value': value,
            'Description': description
        }
        table.create_entity(entity=entity)


def get_events(number: int):
    with get_table_client() as client:
        table = client.get_table_client('events')
        events = table.query_entities("PartitionKey eq 'wallet'")
        data = [{'Value': e['Value'], 'Time': e['RowKey'], 'Description': e['Description']} for e in events]
        data.sort(key=lambda x: x['Time'], reverse=True)
        return data[:number]  # TODO: check if it can be done in the query


def get_balance():
    with get_table_client() as client:
        table = client.get_table_client('events')
        events = table.query_entities("PartitionKey eq 'wallet'")
        balance = sum([e['Value'] for e in events])
        return balance
