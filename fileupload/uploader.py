from os import environ
from typing import Literal

from fileupload.object_storage import ObjectStorage
from fileupload.constants import FILE_STORAGE_TYPE
from fileupload.aws import S3ObjectStorage, S3Factory
from fileupload.minio import MinioObjectStorage, MinioFactory
from utils.singleton import Singleton

FILE_STORAGE_TYPE: Literal["minio", "s3"] = environ.get("FILE_STORAGE_TYPE", "minio")


class ObjectUploader(Singleton):
    def __init__(self, storage: ObjectStorage):
        self.object_uploader = storage

    def upload_object(self, object_data: bytes, file_name: str) -> str:
        return self.object_uploader.save_object(object_data, file_name)


class ObjectUploaderFactory:
    @staticmethod
    def generate():

        if FILE_STORAGE_TYPE == "S3":
            return ObjectUploader(S3ObjectStorage(S3Factory()))
        return ObjectUploader(MinioObjectStorage(MinioFactory()))
