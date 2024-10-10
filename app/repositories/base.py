from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @staticmethod
    @abstractmethod
    async def find_one_or_none(**filter_by):
        pass

    @staticmethod
    @abstractmethod
    async def find_all(**filter_by):
        pass

    @staticmethod
    @abstractmethod
    async def create(**values):
        pass

    @staticmethod
    @abstractmethod
    async def update(id_, **values):
        pass

    @staticmethod
    @abstractmethod
    async def delete(**filter_by):
        pass
