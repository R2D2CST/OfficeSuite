# Python native libraries
import os

# Third party libraries
from docx import Document

# Self build libraries

from Func.AbstractDocument import AbstractDocument


class Word(AbstractDocument):

    def __init__(self, filePath: str) -> None:

        # Class main attribute file path location
        self.filePath = filePath

        # We validate the given path corresponds with an .docx file type
        self.__validateFiletype()

        # We generate our first document attributes
        try:
            self.__readFile()

        # If file does not exists we build a new one
        except FileNotFoundError:
            self.__createNewFile()
            self.__readFile()
        pass

    def __validateFiletype(self) -> bool:
        """
        Method is private not intended to use outside this class type.
        Raises:
            f: Given file path: {self.filePath} Not a valid word file type.

        Returns:
            bool: True if given path is a valid file path and an word filetype, False otherwise.
        """
        if ".docx" not in self.filePath:
            raise f"Given file path: {self.filePath}\n Not a valid word file type."

        else:
            return True

    def __readFile(self) -> None:
        self.document = Document(self.filePath)
        pass

    def __createNewFile(self) -> None:
        self.document = Document()
        self.document.save(self.filePath)
        pass

    pass
