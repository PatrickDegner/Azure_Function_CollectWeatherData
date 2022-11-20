import logging
from datetime import datetime, timedelta
from meteostat import Daily
import pandas as pd
from azure.storage.blob import BlobServiceClient
import os
import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Set time period to beginning 2022
    start = datetime(2022, 1, 1)
    # set end to today + 7 days
    end = (datetime.now() + timedelta(days=7))
    # set file name
    file_name = 'weatherdata.parquet'

    # Get daily data from Munich Station
    df = Daily('10865', start, end)
    df = df.fetch()

    # Set city
    df['city'] = 'Munich'

    # Rename index from time to date
    df.index.name = 'date'

    # Rename other columns and drop wpgt column
    df = df.rename(columns={'tavg': 'average_temperature', 'tmin': 'min_temperature', 'tmax': 'max_temperature',
                            'prcp': 'precipitation', 'wdir': 'wind_direction', 'wspd': 'wind_speed', 'pres': 'pressure', 'tsun': 'sunshine_minutes'})
    df = df.drop(columns=['wpgt'])

    # convert to parquet in temp folder
    df.to_parquet('/tmp/' + file_name)

    # set container name and connection string
    container_name = 'weatherdata'

    # Get connection string from keyvault
    key_vault_Uri = 'https://patricksvault.vault.azure.net/'
    blob_secret_name = 'weatherdata-storage-connection-string'
    az_credential = ManagedIdentityCredential()

    secret_client = SecretClient(
        vault_url=key_vault_Uri, credential=az_credential)
    secret = secret_client.get_secret(blob_secret_name).value

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(
        secret)

    # create new container if not exists
    if not blob_service_client.get_container_client(container_name).exists():
        blob_service_client.create_container(container_name)

    # if exists delete old blob 'weatherdata.parquet' in container 'weatherdata'
    if blob_service_client.get_blob_client(container=container_name, blob=file_name).exists():
        blob_service_client.get_blob_client(
            container=container_name, blob=file_name).delete_blob()

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=file_name)

    # Upload the created file
    with open('/tmp/' + file_name, "rb") as data:
        blob_client.upload_blob(data)

    # Delete local file
    os.remove('/tmp/' + file_name)

    # return success message to http request
    return func.HttpResponse("Weatherdata successfully uploaded to Azure Blob Storage", status_code=200)
