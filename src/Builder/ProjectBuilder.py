# Python native libraries
import os

# Third party libraries
from tqdm import tqdm

# Self build libraries
from Builder.DatabaseBuilder import DatabaseBuilder
from Builder.ExcelTemplate import ExcelTemplate
from Builder.WordTemplate import WordTemplate
from Builder.WordPlaceHolder import WordPlaceHolder
from Func.Images.Placeholder import Placeholder
from Func.Images.PlaceholderModel import PlaceholderModel


class ProjectBuilder:
    """
    Class builds the basic project architecture for rendering template documents with given database context.

    Args:
        > projectPath (str): Destination where user desires to build a new project
        > projectName (str, optional): Project name the user desire to build. Defaults to "RenderProject".
    """

    def __init__(self, projectPath: str, projectName: str = "RenderProject") -> None:
        """
        Initializes de class procedure for building a new project.
        """
        self.projectPath: str = projectPath
        self.projectName: str = projectName
        steps = [
            self.__buildConstants,
            self.__buildProjectArchitecture,
            self.__buildAssets,
        ]
        totalSteps = len(steps)
        with tqdm(
            total=totalSteps,
            desc="Building Project",
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
        Method only states several private attributes that shall be used as constants in the rendering project.
        """
        # File type names and respective extensions
        self.__databaseFileName: str = "database.xlsx"
        self.__excelTemplateFileName: str = "excelTemplate.xlsx"
        self.__wordTemplateFileName: str = "wordTemplate.docx"

        # Project directory architecture names
        self.__templateDirectory: str = "Templates"
        self.__databaseDirectory: str = "Database"

        self.__placeholdersDirectory: str = "Placeholders"

        self.__assetsDirectory: str = "Assets"
        pass

    def __buildProjectArchitecture(self):
        """
        Method builds the basic architecture for a brand new rendering project.
        """
        self.projectDirPath: str = os.path.join(
            self.projectPath,
            self.projectName,
        )
        if not os.path.exists(self.projectDirPath):
            os.mkdir(self.projectDirPath)
        else:
            counter = 1
            while True:
                if os.path.exists(self.projectDirPath):
                    self.projectDirPath = os.path.join(
                        self.projectPath,
                        f"{self.projectName} {counter}",
                    )
                else:
                    os.mkdir(self.projectDirPath)
                    self.projectName = f"{self.projectName} {counter}"
                    break
                counter += 1
                continue

        self.templateDirPath = os.path.join(
            self.projectDirPath,
            self.__templateDirectory,
        )
        self.databaseDirPath = os.path.join(
            self.projectDirPath,
            self.__databaseDirectory,
        )

        self.placeholderDirPath = os.path.join(
            self.projectDirPath,
            self.__placeholdersDirectory,
        )

        self.assetsDirPath = os.path.join(
            self.projectDirPath,
            self.__assetsDirectory,
        )
        for directory in [
            self.templateDirPath,
            self.databaseDirPath,
            self.placeholderDirPath,
            self.assetsDirPath,
        ]:
            os.mkdir(directory)

        self.xlTemplatePath = os.path.join(
            self.templateDirPath,
            self.__excelTemplateFileName,
        )
        self.docTemplatePath = os.path.join(
            self.templateDirPath,
            self.__wordTemplateFileName,
        )
        self.databasePath = os.path.join(
            self.databaseDirPath,
            self.__databaseFileName,
        )

        pass

    def __buildAssets(self) -> None:
        """
        Private method builds the assets in a brand new project.
        """

        DatabaseBuilder(databasePath=self.databasePath)

        Placeholder(
            outputPath=self.placeholderDirPath,
            number=25,
            width=300,
            height=300,
        )

        PlaceholderModel(
            outputPath=self.assetsDirPath,
            number=25,
            width=300,
            height=300,
        )
        ExcelTemplate(templatePath=self.xlTemplatePath)
        WordTemplate(
            templatePath=self.docTemplatePath,
            placeholdersDirectory=self.placeholderDirPath,
        )
        WordPlaceHolder(
            templatePath=self.docTemplatePath,
            placeholdersDirectory=self.placeholderDirPath,
        )
        pass

    pass
