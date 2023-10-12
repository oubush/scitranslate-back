import io
import yaml
import uuid
from minio import Minio
from urllib3.exceptions import MaxRetryError
import logging

logging.basicConfig(level=logging.INFO)

# Чтение credentials
with open('credentials_genomai.yaml', 'r') as file:
    credentials = yaml.safe_load(file)

MINIO_HOST = credentials['host']
MINIO_PORT = credentials['minio_api']['port']
MINIO_ACCESS_KEY = credentials['minio_api']['access_key']
MINIO_SECRET_KEY = credentials['minio_api']['secret_key']

BUCKET_NAME = 'scitranslate'

# Подключение к Minio
minio_client = Minio(
    endpoint=f"{MINIO_HOST}:{MINIO_PORT}",
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)


def put_file(file: io.BytesIO):
    """
    """
    object_uuid = str(uuid.uuid4())
    minio_client.put_object(BUCKET_NAME, object_uuid, file, file.getbuffer().nbytes)
    return object_uuid


def get_file(object_uuid):
    response = minio_client.get_object(BUCKET_NAME, object_uuid)
    return response.read()

# 
# file_path = 'Библиотека.docx'
# minio_client.fput_object(bucket_name, object_uuid, file_path)

# result = minio_client.get_object(bucket_name, "842dded5-9b4e-4ce8-a6f3-5c7ceefdbb0e")
# with open("output.docx", "wb") as f:
#     f.write(result.read())
# print(result.read())
# try:
#     print(minio_client.list_buckets())
# except MaxRetryError:
#     logging.critical("Object storage not reachable")