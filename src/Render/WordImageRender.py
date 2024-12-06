# Python native libraries
import os

# Third party libraries
import openpyxl
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

# Self build libraries
from Func.Excel.Excel import Excel
from Render.WordRender import WordRender


class WordImageRenderer(WordRender):

    def __init__(
        self,
        templatesDirectory: str,
        databasePath: str,
        outputRenders: str,
        assetsDirectory: str,
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
        self.__transformPlaceholderMatrix()
        self.__getTemplatesList()
        self.__renderWordImageDocuments()
        pass

    def __readDatabase(self) -> None:

        excel = Excel(self.databasePath)

        # workbookData (list[list[list[any]]]): 3D __matrix (sheet, row, column)
        self.__matrix = excel.workbookData
        self.__sheets = excel.sheets
        for index, sheetName in enumerate(self.__sheets):
            if sheetName == "Place Holders":
                self.__placeholdersMatrix = self.__matrix[index]

        # Validation of database integrity
        if not self.__placeholdersMatrix:
            raise ValueError(
                "Missing required sheets: Word Data, Excel Data, or Place Holders."
            )
        pass

    def __transformPlaceholderMatrix(self) -> None:
        if not self.assetsDirectory:
            return

        # We build the placeholders context
        self.keyWordsPlaceholders = self.__placeholdersMatrix[1]  # Header row
        self.placeholderContext = {}

        # Iterate through the data rows
        for runIndex, row in enumerate(
            iterable=self.__placeholdersMatrix[2:],  # Skip note and headers
            start=1,  # Skip Header
        ):
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

    def __renderWordImageDocuments(self) -> None:

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

                # We actually render the document
                documentTemplate.render(context=context)

                # We render the document replacing the placeholders images
                if self.assetsDirectory:
                    self.__renderPlaceholders(
                        document=documentTemplate,
                        context=placeholders,
                    )

                # We save the changes
                documentTemplate.save(renderOutput)
        pass

    @staticmethod
    def __renderPlaceholders(document: any, context: dict):
        for key in context.keys():
            value = context.get(key)
            document.replace_pic(key, value)
        pass

    pass
