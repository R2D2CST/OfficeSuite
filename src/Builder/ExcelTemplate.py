# Python native libraries
import string

# Third party libraries
from Func.Excel.Excel import Excel

# Self build libraries


class ExcelTemplate(Excel):
    """
    Class builds a empty excel file with the labels where to dump the rendering information
    Args:
        > databasePath (str): path where the database will be stored
    """

    def __init__(self, templatePath: str):

        # We inherit the parent attributes and methods
        super().__init__(filePath=templatePath)

        # We write the dummy content into the excel file and save changes
        self.__buildDummyContent()
        self.saveAndClose()

        pass

    def __buildDummyContent(self):

        sheet = self.workbook.create_sheet(title="Sheet 1")
        self._erraseDefaultSheets()
        cells = [f"{col}" for col in string.ascii_uppercase[:9]]
        for index, cell in enumerate(cells):
            sheet[f"{cell}{index+2}"] = "Watch Above"

        pass

    pass
