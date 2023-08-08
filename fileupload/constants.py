from os import environ

MINIO_SERVICE_URL = "minio:9000"
MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")

MINIO_BUCKET_NAME = environ.get("MINIO_BUCKET_NAME")

MINIO_URL = "http://127.0.0.1:9001/"

FILE_STORAGE_TYPE = "Minio"
