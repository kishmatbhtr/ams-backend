from abc import ABC, abstractmethod
from utils.singleton import Singleton


class ObjectStorage(ABC, Singleton):
    @abstractmethod
    def save_object(self, object_data: bytes, file_name: str, content_type: str):
        pass
