# Python native libraries
import os

# Third party libraries
from docxtpl import DocxTemplate, InlineImage
from tqdm import tqdm

# Self build libraries
from Func.Excel.Excel import Excel
from Render.WordRender import WordRender

"""
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
        super().__buildConstants()
        super().__readDatabase()
        self.__readDatabase()
        super().__transformWordMatrix()
        self.__transformPlaceholderMatrix()
        super().__getTemplatesList()
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
                    raise IndexError(f"Empty Place Holder Error in {columnKeyword}")

                # Create InlineImage object for Word rendering
                runDictionary[columnKeyword] = value

            # Use the same "run" keys from wordContext
            runKey = self.wordKeyHeaders[runIndex]
            self.placeholderContext[runKey] = runDictionary

    def __imagePathBuilder(self, partialPath: str) -> str:
        imagePath = os.path.join(self.assetsDirectory, partialPath)
        if not os.path.exists(imagePath):
            raise FileNotFoundError(
                f"Rendering image not found: {imagePath} (Placeholder: {partialPath})"
            )
        return imagePath

    @staticmethod
    def __inLineImageBuilder(template, imagePath: str) -> InlineImage:
        return InlineImage(
            template,
            imagePath,
        )

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
                placeholdersStructure = self.placeholderContext.get(run, {})
                secondContext = {}
                for key, value in placeholdersStructure.items():
                    imagePath = self.__imagePathBuilder(value)
                    inlineImageObject = self.__inLineImageBuilder(
                        template=documentTemplate,
                        imagePath=imagePath,
                    )
                    secondContext[key] = inlineImageObject
                context.update(secondContext)

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
"""


class WordImageRenderer(WordRender):
    """
    Specialized class for rendering Word documents with image placeholders.

    Args:
        templatesDirectory (str): Directory where Word templates are stored.
        databasePath (str): Path to the Excel database file.
        outputRenders (str): Directory where rendered documents will be saved.
        assetsDirectory (str): Directory containing image assets for placeholders.

    Raises:
        FileNotFoundError: If any of the directories or files do not exist.
        ValueError: If required sheets are missing in the database.
    """

    def __init__(
        self,
        templatesDirectory: str,
        databasePath: str,
        outputRenders: str,
        assetsDirectory: str,
    ) -> None:
        # Principal attributes
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

        # Main procedures for rendering documents
        steps = [
            self._WordRender__buildConstants,
            self._WordRender__readDatabase,
            self.__readDatabase,
            self._WordRender__transformWordMatrix,
            self.__transformPlaceholderMatrix,
            self._WordRender__getTemplatesList,
            self.__renderWordImageDocuments,
        ]
        totalSteps = len(steps)
        with tqdm(
            total=totalSteps,
            desc="Rendering Word templates in project",
            unit="step",
        ) as progressBar:
            for index, step in enumerate(iterable=steps):
                progressBar.set_description(f"Step {index+1} of {totalSteps}")
                step()
                progressBar.update(1)
            pass

    def __readDatabase(self) -> None:
        """
        Reads the placeholders sheet from the database and validates its content.
        Raises:
            ValueError: If the "Place Holders" sheet is missing.
        """
        excel = Excel(self.databasePath)
        self.__matrix = excel.workbookData
        self.__sheets = excel.sheets

        for index, sheetName in enumerate(self.__sheets):
            if sheetName == "Place Holders":
                self.__placeholdersMatrix = self.__matrix[index]

        if not self.__placeholdersMatrix:
            raise ValueError("Missing required sheet: Place Holders.")

    def __transformPlaceholderMatrix(self) -> None:
        """
        Transforms the placeholders matrix into a structured context dictionary.
        """
        self.keyWordsPlaceholders = self.__placeholdersMatrix[1]  # Header row
        self.placeholderContext = {}

        for runIndex, row in enumerate(self.__placeholdersMatrix[2:], start=1):
            runDictionary = {}
            for columnIndex, columnKeyword in enumerate(self.keyWordsPlaceholders):
                value = row[columnIndex]
                if not value:
                    raise IndexError(f"Empty placeholder found in {columnKeyword}")
                runDictionary[columnKeyword] = value

            runKey = self.wordKeyHeaders[runIndex]
            self.placeholderContext[runKey] = runDictionary

    def __imagePathBuilder(self, partialPath: str) -> str:
        """
        Constructs the full image path from a partial path.
        """
        imagePath = os.path.join(self.assetsDirectory, partialPath)
        if not os.path.exists(imagePath):
            raise FileNotFoundError(
                f"Rendering image not found: {imagePath} (Placeholder: {partialPath})"
            )
        return imagePath

    @staticmethod
    def __inLineImageBuilder(template: DocxTemplate, imagePath: str) -> InlineImage:
        """
        Builds an InlineImage object for rendering in Word.
        """
        return InlineImage(template, imagePath)

    def __renderWordImageDocuments(self) -> None:
        """
        Renders Word documents by merging text and image placeholders.
        """
        for templatePath in self.wordTemplatesPaths:
            documentTemplate = DocxTemplate(template_file=templatePath)

            for run in self.wordKeyHeaders[1:]:
                runOutputDirectory = os.path.join(
                    self.outputRenders, self.rendersDirectory, run
                )
                os.makedirs(runOutputDirectory, exist_ok=True)

                fileName = os.path.basename(templatePath)
                renderName = f"{run}_{fileName}"
                renderOutput = os.path.join(runOutputDirectory, renderName)

                context = self.wordContext.get(run, {}).copy()
                placeholdersStructure = self.placeholderContext.get(run, {})
                secondContext = {}

                for key, value in placeholdersStructure.items():
                    imagePath = self.__imagePathBuilder(value)
                    inlineImageObject = self.__inLineImageBuilder(
                        template=documentTemplate, imagePath=imagePath
                    )
                    secondContext[key] = inlineImageObject

                context.update(secondContext)
                documentTemplate.render(context=context)
                documentTemplate.save(renderOutput)
