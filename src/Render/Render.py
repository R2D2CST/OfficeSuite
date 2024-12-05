# Python native libraries
from typing import Dict, Any
import os

# Third party libraries
import openpyxl
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# Self build libraries
from Func.Excel import Excel


class Renderer:

    def __init__(
        self,
        templatesDirectory: str,
        databasePath: str,
        outputRenders: str,
        assetsDirectory: str = False,
    ) -> None:
        # we set our principal attributes
        self.templatesDirectory = templatesDirectory
        self.databasePath = databasePath
        self.outputRenders = outputRenders
        self.assetsDirectory = assetsDirectory

        # Initial validations
        if not os.path.exists(self.templatesDirectory):
            raise FileNotFoundError("Templates directory does not exist.")
        if not os.path.exists(self.databasePath):
            raise FileNotFoundError("Database path does not exist.")
        if self.assetsDirectory and not os.path.exists(self.assetsDirectory):
            raise FileNotFoundError("Assets directory does not exist.")

        # We execute the main procedures for rendering documents
        self.__buildConstants()
        self.__readDatabase()
        self.__transformWordMatrix()
        self.__transformExcelMatrix()
        if self.assetsDirectory:
            self.__transformPlaceholderMatrix()
        self.__getTemplatesList()

        pass

    def __buildConstants(self):
        self.rendersDirectory: str = "Renders"
        pass

    def __readDatabase(self) -> None:

        excel = Excel(self.databasePath)

        # workbookData (list[list[list[any]]]): 3D __matrix (sheet, row, column)
        self.__matrix = excel.workbookData
        self.__sheets = excel.sheets
        for index, sheetName in enumerate(self.__sheets):
            if sheetName == "Word Data":
                self.__wordMatrix = self.__matrix[index]
            elif sheetName == "Excel Data":
                self.__excelMatrix = self.__matrix[index]
            elif sheetName == "Place Holders":
                self.__placeholdersMatrix = self.__matrix[index]

        # Validation of database integrity
        if (
            not self.__wordMatrix
            or not self.__excelMatrix
            or not self.__placeholdersMatrix
        ):
            raise ValueError(
                "Missing required sheets: Word Data, Excel Data, or Place Holders."
            )
        pass

    def __transformPlaceholderMatrix(self) -> None:
        if not self.assetsDirectory:
            return

        # We build the placeholders context
        self.keyWordsPlaceholders = self.__placeholdersMatrix[0]  # Header row
        self.placeholderContext = {}

        # Iterate through the data rows
        for runIndex, row in enumerate(self.__placeholdersMatrix[2:]):  # Skip header
            runDictionary = {}

            # Iterate through each column (matching keywords to images)
            for columnIndex, columnKeyword in enumerate(self.keyWordsPlaceholders):
                value = row[columnIndex]

                # Skip if no value for the placeholder
                if not value:
                    continue

                # Construct image path
                imagePath = os.path.join(self.assetsDirectory, value)
                if not os.path.exists(imagePath):
                    raise FileNotFoundError(
                        f"Rendering image not found: {imagePath} (Placeholder: {value})"
                    )

                # Create InlineImage object for Word rendering
                runDictionary[columnKeyword] = InlineImage(
                    DocxTemplate(
                        "dummy.docx"
                    ),  # Temporary template for inline image creation
                    imagePath,
                    width=Mm(50),  # Adjust image size as needed
                )

            # Use the same "run" keys from wordContext
            runKey = self.wordKeyHeaders[runIndex]
            self.placeholderContext[runKey] = runDictionary

    def __transformWordMatrix(self) -> None:
        # We get all the key words in the matrix
        self.keyWords = self.__wordMatrix[0]

        # We get all the key headers or "runs" we will render
        self.wordKeyHeaders = [row[0] for row in self.__wordMatrix]

        # We build the context dictionary structure for rendering templates
        self.wordContext = dict()  # We build the main dictionary
        for runIndex, runKey in enumerate(self.wordKeyHeaders):
            runDictionary = dict()
            runRowData = self.__wordMatrix[runIndex]

            for columnIndex, columnKeyword in enumerate(self.keyWords):
                runDictionary[columnKeyword] = runRowData[columnIndex]

            self.wordContext[runKey] = runDictionary
        pass

    def __transformExcelMatrix(self) -> None:

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
        self.__templatesPaths = [
            os.path.join(self.templatesDirectory, item)
            for item in os.listdir(self.templatesDirectory)
        ]
        self.wordTemplatesPaths = [
            path for path in self.__templatesPaths if path.endswith(".docx")
        ]
        self.excelTemplatesPaths = [
            path for path in self.__templatesPaths if path.endswith(".xlsx")
        ]
        pass

    def renderWordDocuments(self) -> None:

        def renderPlaceholders(document: any, context: dict):
            for key in context.keys():
                value = context.get(key)
                document.replace_pic(key, value)
            pass

        for templatePath in self.wordTemplatesPaths:
            documentTemplate = DocxTemplate(template_file=templatePath)
            # We skip the first key that corresponds for key values
            for run in self.wordKeyHeaders[1:]:

                # We build the destination directory where we will store the rendered document version
                runOutputDirectory = os.path.join(
                    self.outputRenders,
                    self.rendersDirectory,
                    run,
                )
                os.makedirs(runOutputDirectory, exist_ok=True)

                # We strip from the template path the original document name and append it to the intended destination adding the key header
                fileName = os.path.basename(templatePath)
                renderName = f"{run}_{fileName}"
                renderOutput = os.path.join(runOutputDirectory, renderName)

                # We merge the word with placeholder context
                context = self.wordContext.get(run, {}).copy()
                placeholders = self.placeholderContext.get(run, {})
                # ! Cant render images into document need separate value.
                # context.update(placeholders)  # Merge both contexts

                # We actually render the document
                documentTemplate.render(context=context)

                """
                ! Cant render images by the moment.
                # We render the document replacing the placeholders images
                if self.assetsDirectory:
                    renderPlaceholders(
                        document=documentTemplate,
                        context=self.placeholderContext,
                    )
                """

                # We save the changes
                documentTemplate.save(renderOutput)
        pass

    def renderExcelDocuments(self) -> None:

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
