from abc import ABC, abstractmethod


class InterfaceCallback(ABC):

    @abstractmethod
    async def callback_data(self, *args):
        pass

    @abstractmethod
    def get_data(self, *args):
        pass

    @abstractmethod
    def validate_data(self, *args):
        pass
