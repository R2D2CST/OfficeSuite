# Python native libraries
import os

# Third party libraries
from Func.Excel import Excel
from Func.Word import Word

# Self build libraries


class Renderer:

    def __init__(self, templatesDirectory: str, databasePath: str) -> None:
        self.templatesDirectory: str = templatesDirectory
        self.databasePath: str = databasePath
        pass

    def __readDatabase (self)->None:
        
        excel = Excel(self.databasePath)
        
        # workbookData (list[list[list[any]]]): 3D matrix (sheet, row, column)
        self.matrix = excel.workbookData
        self.sheets = excel.sheets

        pass

    pass
