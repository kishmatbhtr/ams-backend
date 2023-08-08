from io import BytesIO
import json

from fileupload.object_storage import ObjectStorage
from utils.singleton import Singleton
from minio import Minio

from fileupload.constants import (
    MINIO_SERVICE_URL,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET_NAME,
    MINIO_URL,
)

MINIO_POLICY: dict = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:GetObject"],
            "Resource": [f"arn:aws:s3:::{MINIO_BUCKET_NAME}/*"],
        },
        {
            "Effect": "Allow",
            "Principal": {"AWS": ["*"]},
            "Action": ["s3:DeleteObject", "s3:PutObject"],
            "Resource": [f"arn:aws:s3:::{MINIO_BUCKET_NAME}/*"],
            "Condition": {"StringEquals": {"aws:username": ["access-key-value"]}},
        },
    ],
}


class MinioSingletonClass(Singleton, Minio):
    pass


class MinioFactory:
    def generate(self):
        MinioSingletonClass(
            MINIO_SERVICE_URL,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,
        )


class MinioObjectStorage(ObjectStorage):
    client = None

    def __init__(self, factory_obj: MinioFactory) -> None:
        self.client = factory_obj.generate()

    def configure_minio(self):
        if not self.client.bucket_exists(MINIO_BUCKET_NAME):
            self.client.make_bucket(MINIO_BUCKET_NAME)
            self.client.set_bucket_policy(MINIO_BUCKET_NAME, json.dumps(MINIO_POLICY))

    def save_object(self, object_data: bytes, file_name: str, content_type: str) -> str:
        self.configure_minio()
        file_stream = BytesIO(object_data)
        self.client.put_object(
            MINIO_BUCKET_NAME,
            object_name=file_name,
            data=file_stream,
            length=len(object_data),
            content_type=content_type,
        )

        return f"{MINIO_URL}{MINIO_BUCKET_NAME}/{file_name}"
