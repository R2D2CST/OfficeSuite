# Python native libraries
import string

# Third party libraries
from Func.Excel import Excel

# Self build libraries


class DatabaseBuilder(Excel):
    """
    Class builds a data base example of an excel file for rendering the document projects into the Office Suite Render
    Args:
        > databasePath (str): path where the database will be stored
    Attr: None
    Raises: None
    """

    def __init__(self, databasePath: str) -> None:
        # We inherit all the parent attributes an methods
        super().__init__(filePath=databasePath)

        # We build the dummy information as example into rendering projects
        self.__buildWordDummyData()
        self.__buildExcelDummyData()
        self.__buildPlaceholderDummyData()

        # We write into the excel file and save the changes
        self.__overwriteIn()
        self.saveAndClose()
        pass

    def __buildWordDummyData(self) -> None:

        sheetData = list()

        headers = ["Key_Header"]
        for i in range(1, 10, 1):  # We subtract the Key_Header
            headers.append(f"Key_Word_{i}")

        sheetData.append(headers)

        for rowNumber in range(1, 11, 1):
            rowList = list()
            for columnNumber in range(1, 11, 1):
                rowList.append(f"Row {rowNumber} Data {columnNumber}")
            sheetData.append(rowList)

        self.__wordSheet = sheetData

        pass

    def __buildExcelDummyData(self) -> None:

        sheetData = list()

        headers = ["Key Header"]
        for i in range(1, 10, 1):
            headers.append(f" Header {i}")

        pointers = ["Cell Pointer"]
        # We get the first 10 capital letters from A to J
        cells = [f"{col}" for col in string.ascii_uppercase[:9]]
        for index, cell in enumerate(cells):
            pointers.append(f"{cell}{index+1}")

        sheetPointer = ["Sheet Pointer"]
        for i in range(1, 10, 1):
            sheetPointer.append("Sheet 1")

        sheetData.append(headers)
        sheetData.append(pointers)
        sheetData.append(sheetPointer)

        for rowNumber in range(1, 11, 1):
            rowList = list()
            for columnNumber in range(1, 11, 1):
                rowList.append(f"Row {rowNumber} Data {columnNumber}")
            sheetData.append(rowList)

        self.__excelSheet = sheetData

        pass

    def __buildPlaceholderDummyData(self) -> None:
        sheetData = list()
        sheetData.append(
            [
                "!!!Remember to delete excessive placeholders and type Titles with file extension¡¡¡",
            ]
        )
        sheetData.append([f"Place_Holder_{i}" for i in range(1, 26, 1)])

        for _ in range(1, 11, 1):
            row = list()
            for j in range(1, 26, 1):
                row.append(f"Replace_Image_{j}.png")
            sheetData.append(row)
        self.__placeHolderSheet = sheetData
        pass

    def __overwriteIn(self) -> None:

        # Parent object class attribute.
        # workbook (workbook) : file object class.
        # We add the new Excel Sheets where to dump our information
        wordDataSheet = self.workbook.create_sheet(title="Word Data")
        excelDataSheet = self.workbook.create_sheet(title="Excel Data")
        placeholderDataSheet = self.workbook.create_sheet(title="Place Holders")

        # We errase the default sheets in the excel file
        self._erraseDefaultSheets()

        # We write over the recently added spreadsheets
        for i in self.__excelSheet:
            excelDataSheet.append(i)
        for j in self.__wordSheet:
            wordDataSheet.append(j)
        for k in self.__placeHolderSheet:
            placeholderDataSheet.append(k)
        pass

    pass
