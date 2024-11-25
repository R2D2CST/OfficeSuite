# Python native libraries
import os

# Third party libraries
import openpyxl

# Self build libraries

from Func.AbstractDocument import AbstractDocument


class Excel(AbstractDocument):

    def __init__(self, filePath: str):
        """
        We build the class starting object attributes.
            Args:
                > filePath (str) : file path where the workbook exists
            Returns: None
            Attributes:
                > filePath (str) : file path where the workbook exists
                > workbook (workbook) : file object class
                > sheets (list[str]) : list of sheets contained in the workbook
            Raises: None
        """

        # Class main attribute file path location
        self.filePath = filePath

        # We validate the given path corresponds with an .xlsx file type
        self.__validateFiletype()

        # We generate our first workbook attributes
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
            f: Given file path: {self.filePath} Not a valid excel file type.

        Returns:
            bool: True if given path is a valid file path and an excel filetype, False otherwise.
        """
        if ".xlsx" not in self.filePath:
            raise f"Given file path: {self.filePath}\n Not a valid excel file type."

        else:
            return True

    def __readFile(self) -> any:
        """
        Method reads a Excel file and stores as object attributes
            Args: None
            Returns: None
            Attributes:
                > workbook (workbook) : file object class
                > sheets (list[str]) : list of sheets contained in the workbook
            Raises: None
        """
        self.workbook = openpyxl.load_workbook(filename=self.filePath)
        self.sheets = self.workbook.get_sheet_names()
        pass

    def __createNewFile(self) -> None:
        """
        Method builds a new empty excel file type.
            Args: None
            Returns: None
            Raises: None
        """
        workbook = openpyxl.Workbook()
        workbook.save(filename=self.filePath)
        del workbook
        pass

    def __readSheet(self) -> None:
        pass

    pass
