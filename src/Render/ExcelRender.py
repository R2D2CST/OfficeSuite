# Python native libraries
import os

# Third party libraries
import openpyxl
from tqdm import tqdm

# Self build libraries
from Func.Excel.Excel import Excel


class ExcelRenderer:
    """
    Class builds the methods into rendering excel file type documents with given context by a certain excel database.
    Args:
        > templatesDirectory (str): directory where the excel documents are found
        > databasePath (str): path of the excel database information
        > outputRenders (str): directory where the class will dump render documents
    Raises:
        > FileNotFoundError: Templates directory does not exist.
        > FileNotFoundError: Database path does not exist.
        > ValueError: Missing required sheets: Word Data, Excel Data, or Place Holders.
        > ValueError: Matrix should have Header, cell and sheet pointers.
        > ValueError: Pointes should have same length for rendering.
        > IndexError: Matrix size not uniform, Index out of range.
    """

    def __init__(
        self,
        templatesDirectory: str,
        databasePath: str,
        outputRenders: str,
    ) -> None:
        """_summary_

        Args:
            > templatesDirectory (str): directory where the excel documents are found
            > databasePath (str): path of the excel database information
            > outputRenders (str): directory where the class will dump render documents

        Raises:
            FileNotFoundError: Templates directory does not exist.
            FileNotFoundError: Database path does not exist.
        """
        # we set our principal attributes
        self.templatesDirectory = templatesDirectory
        self.databasePath = databasePath
        self.outputRenders = outputRenders

        # Initial validations
        if not os.path.exists(self.templatesDirectory):
            raise FileNotFoundError("Templates directory does not exist.")
        if not os.path.exists(self.databasePath):
            raise FileNotFoundError("Database path does not exist.")

        # We execute the main procedures for rendering documents
        steps = [
                self.__buildConstants,
                self.__readDatabase,
                self.__transformExcelMatrix,
                self.__getTemplatesList,
                self.__renderExcelDocuments,
            ]
        totalSteps = len(steps)
        with tqdm(
            total=totalSteps,
            desc="Rendering Excel templates in project",
            unit="step",
        ) as progressBar:
            for index, step in enumerate(iterable=steps):
                progressBar.set_description(f"Step {index+1} of {totalSteps}")
                step()
                progressBar.update(1)
            pass
        pass

    def __buildConstants(self):
        """
        We build the the inner class constants
        """
        self.rendersDirectory: str = "Renders"
        pass

    def __readDatabase(self) -> None:
        """
        Method reads the database excel content for rendering the excel type files

        Raises:
            ValueError: Missing required sheets: Word Data, Excel Data, or Place Holders.

        """

        excel = Excel(self.databasePath)

        # workbookData (list[list[list[any]]]): 3D __matrix (sheet, row, column)
        self.__matrix = excel.workbookData
        self.__sheets = excel.sheets
        for index, sheetName in enumerate(self.__sheets):
            if sheetName == "Excel Data":
                self.__excelMatrix = self.__matrix[index]

        # Validation of database integrity
        if not self.__excelMatrix:
            raise ValueError(
                "Missing required sheets: Word Data, Excel Data, or Place Holders."
            )
        pass

    def __transformExcelMatrix(self) -> None:
        """
        Method builds the excel table content into a proper data structure for rendering documents

        Raises:
            ValueError: Matrix should have Header, cell and sheet pointers.
            ValueError: Pointes should have same length for rendering.
            IndexError: Matrix size not uniform, Index out of range.
        """

        if len(self.__excelMatrix) < 3:
            raise ValueError("Matrix should have Header, cell and sheet pointers")

        # We get all the cell pointers
        self.cellPointers = self.__excelMatrix[1][1:]

        # We get all the sheet pointers
        self.sheetPointers = self.__excelMatrix[2][1:]
        if len(self.cellPointers) != len(self.sheetPointers):
            raise ValueError("Pointes should have same length for rendering.")

        # We get the Key Headers "Run" names
        self.excelKeyHeaders = [row[0] for row in self.__excelMatrix[3:]]

        self.excelContext = {}
        # We get row values from 4th row or index 3 onwards
        for row in self.__excelMatrix[3:]:
            keyHeader = row[0]
            value = []
            # We skip the first column (Key Header) as it's not rendering data
            for colIndex, data in enumerate(row[1:]):
                if colIndex >= len(self.cellPointers):
                    raise IndexError("Matrix size not uniform, Index out of range")
                elif colIndex >= len(self.sheetPointers):
                    raise IndexError("Matrix size not uniform, Index out of range")

                cellPointer = self.cellPointers[colIndex]
                sheetPointer = self.sheetPointers[colIndex]

                # Data structure: (cellPointer, sheetPointer, data)
                value.append((cellPointer, sheetPointer, data))

            # We dump the values for the respective key "run name"
            self.excelContext[keyHeader] = value
        pass

    def __getTemplatesList(self):
        """
        Method gets all the templates files in the given directory.
        """
        self.__templatesPaths = [
            os.path.join(self.templatesDirectory, item)
            for item in os.listdir(self.templatesDirectory)
        ]
        self.excelTemplatesPaths = [
            path for path in self.__templatesPaths if path.endswith(".xlsx")
        ]
        pass

    def __renderExcelDocuments(self) -> None:
        """
        Method renders the documents contained in the directory path.
        """
        for templatePath in self.excelTemplatesPaths:
            excelTemplate = openpyxl.load_workbook(templatePath)
            for key, valueList in self.excelContext.items():

                # We build the destination directory where we will store the rendered document version
                runOutputDirectory = os.path.join(
                    self.outputRenders,
                    self.rendersDirectory,
                    key,
                )
                os.makedirs(runOutputDirectory, exist_ok=True)

                # We strip from the template path the original document name and append it to the intended destination adding the key header
                fileName = os.path.basename(templatePath)
                renderName = f"{key}_{fileName}"
                renderOutput = os.path.join(runOutputDirectory, renderName)

                # We actually render the file and save the changes
                for cellPointer, sheetPointer, data in valueList:
                    excelSheet = excelTemplate[sheetPointer]
                    excelSheet[cellPointer] = data
                excelTemplate.save(renderOutput)
                excelTemplate.close()

        pass

    pass
