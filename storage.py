from azure.data.tables import TableServiceClient
import os
from dotenv import load_dotenv


load_dotenv()
CONNECTION_STRING = os.getenv('STORAGE_CONNECTION_STRING')


def get_table_client():
    return TableServiceClient.from_connection_string(conn_str=CONNECTION_STRING)


def create_table(table_name: str):
    with get_table_client() as client:
        table = client.create_table(table_name)
        return table


def get_table(table_name: str):
    with get_table_client() as client:
        table = client.get_table_client(table_name)
        return table
