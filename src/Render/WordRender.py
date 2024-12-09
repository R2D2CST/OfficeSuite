# Python native libraries
import os

# Third party libraries
from docxtpl import DocxTemplate
from tqdm import tqdm

# Self build libraries
from Func.Excel.Excel import Excel


class WordRender:
    """
    Class builds the methods into rendering word documents with given context by a certain excel database.
    Args:
        > templatesDirectory (str): directory where the word documents are found
        > databasePath (str): path of the excel database information
        > outputRenders (str): directory where the class will dump render documents
    Raises:
        > FileNotFoundError: Templates directory does not exist.
        > FileNotFoundError: Database path does not exist.
        > ValueError: Missing required sheets: Word Data.
    """

    def __init__(
        self,
        templatesDirectory: str,
        databasePath: str,
        outputRenders: str,
    ) -> None:
        """
        Method initializes the class procedures into rendering a word document.

        Args:
            > templatesDirectory (str): directory where the word documents are found
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
            self.__transformWordMatrix,
            self.__getTemplatesList,
            self.__renderWordDocuments,
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
        pass

    def __buildConstants(self):
        """
        Method build constants used locally in the class
        """
        self.rendersDirectory: str = "Renders"
        pass

    def __readDatabase(self) -> None:
        """
        Procedure reads the content within the given data base.
        Raises:
            ValueError: Missing required sheets: Word Data
        """

        excel = Excel(self.databasePath)

        # workbookData (list[list[list[any]]]): 3D __matrix (sheet, row, column)
        self.__matrix = excel.workbookData
        self.__sheets = excel.sheets
        for index, sheetName in enumerate(self.__sheets):
            if sheetName == "Word Data":
                self.__wordMatrix = self.__matrix[index]

        # Validation of database integrity
        if not self.__wordMatrix:
            raise ValueError("Missing required sheets: Word Data.")
        pass

    def __transformWordMatrix(self) -> None:
        """
        Method gives the excel file table a proper data structure for rendering documents.
        """
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

    def __getTemplatesList(self):
        """
        Method obtains the file paths of the templates we desire to render.
        """
        self.__templatesPaths = [
            os.path.join(self.templatesDirectory, item)
            for item in os.listdir(self.templatesDirectory)
        ]
        self.wordTemplatesPaths = [
            path for path in self.__templatesPaths if path.endswith(".docx")
        ]
        pass

    def __renderWordDocuments(self) -> None:
        """
        Method renders the actual document templates and dumps them into the given output directory.
        """

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

                # We actually render the document
                documentTemplate.render(context=context)

                # We save the changes
                documentTemplate.save(renderOutput)
        pass

    pass
