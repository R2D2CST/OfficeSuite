# Native python modules
from abc import ABC, abstractmethod

# Third party modules

# Self build modules


class AbstractDocument(ABC):

    @abstractmethod
    def __init__(self, filePath: str) -> None:
        self.filePath = filePath
        pass

    pass
