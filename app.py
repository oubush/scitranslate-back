import yaml
import uuid
from minio import Minio
from urllib3.exceptions import MaxRetryError
import logging

logging.basicConfig(level=logging.INFO)

# Чтение credentials
with open('credentials.yaml', 'r') as file:
    credentials = yaml.safe_load(file)

MINIO_HOST = credentials['host']
MINIO_PORT = credentials['minio_api']['port']
MINIO_ACCESS_KEY = credentials['minio_api']['access_key']
MINIO_SECRET_KEY = credentials['minio_api']['secret_key']


# Подключение к Minio
minio_client = Minio(
    endpoint=f"{MINIO_HOST}:{MINIO_PORT}",
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

bucket_name = 'mlflow'
# object_uuid = str(uuid.uuid4())
# file_path = 'Библиотека.docx'
# minio_client.fput_object(bucket_name, object_uuid, file_path)

result = minio_client.get_object(bucket_name, "c908e6e6-a909-4d4d-a26a-051e46a7c4f9")
print(result.read())
# try:
#     print(minio_client.list_buckets())
# except MaxRetryError:
#     logging.critical("Object storage not reachable")