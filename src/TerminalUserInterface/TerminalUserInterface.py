# Python native libraries
import os
from datetime import datetime

# Third party libraries

# Self build libraries
from Builder.ProjectBuilder import ProjectBuilder
from SystemOperations.SystemOperations import SystemOperations
from Render.ExcelRender import ExcelRenderer
from Render.WordRender import WordRender
from Render.WordImageRender import WordImageRenderer


class TerminalUserInterface:
    """
    Class manages the main terminal application for automate Office Suite documents.
    """

    def __init__(self):
        self.__buildConstants()
        if not os.path.exists(self.PROJECTS_DIR):
            os.mkdir(self.PROJECTS_DIR)
        self.__printHeader()
        self.__mainMenuLoop()
        pass

    def __buildConstants(self):
        """
        Method builds the constants the application will be using during a normal operation.
        """
        sysObj = SystemOperations()
        self.__APP_PATH = sysObj.getAppPath()
        self.PROJECTS_DIR = os.path.join(self.__APP_PATH, "Projects")
        self.__OS_KERNEL = sysObj.operativeSystem
        self.__TEMPLATE_DIR = "Templates"
        self.__DATABASE_DIR = "Database"
        self.__DATABASE_FILE_NAME = "database.xlsx"
        self.__ASSETS_DIR = "Assets"
        self.__APP_NAME = "Office Suite"
        self.__VERSION = "3.0.0"
        self.__SUPPORT = "qfbarturocastella@gmail.com"
        self.__MAIN_MENU_OPTIONS = [
            "Exit program",
            "Build new project",
            "Work on existing project",
            "Enable monitoring performance",
            "Enable high performance (User Discretion Advised)",
        ]
        pass

    @staticmethod
    def __exitProcedure() -> None:
        input("Until next time (Please type [Enter] to exit...")
        exit()

    @staticmethod
    def __askForString() -> str:
        """
        Asks for a string type selection to the user until user gets it done.
        Returns:
            selection (str): string selected by the user
        """
        return input("Please type in an response: ")

    @staticmethod
    def __askNumericSelection() -> int:
        """
        Asks for a numeric selection to the user until user gets it done.
        Returns:
            selection (int): integer number selected by the user
        """
        while True:
            print("Please select an option")
            selection = input("Type in a round number: ")
            try:
                selection = int(selection)
            except ValueError:
                print(
                    "ValueError: You must select a integer number examples (1,2,3...)."
                )
                continue
            return selection

    @staticmethod
    def __askYesNo() -> bool:
        """
        Ask the user for a Yes or No question and returns (true) if yes is answered (false) otherwise.
        Returns:
            answer (bool): True if "yes" false otherwise.
        """
        trueOptions = ["yes", "si", "y"]
        falseOptions = ["no", "n"]
        while True:
            print("Do you want to procede...")
            selection = input("Type [Yes/Y] to continue [No/N] to cancel: ")
            if selection.lower() in trueOptions:
                return True
            elif selection.lower() in falseOptions:
                return False
            else:
                print("Invalid options you must answer yes or no [Y/N].")
                continue

    def __printHeader(self) -> None:
        print("--------------------------------------------------")
        print(f"|  App: {self.__APP_NAME}  Version: {self.__VERSION}             |")
        print(f"|  Support: {self.__SUPPORT}          |")
        print("--------------------------------------------------")
        pass

    def __printMainMenu(self) -> None:
        print("---------- MAIN MENU ----------")
        for index, option in enumerate(self.__MAIN_MENU_OPTIONS):
            print(f"{index}.- {option}")
        pass

    def __mainMenuLoop(self) -> None:
        while True:
            self.__printMainMenu()
            selection = self.__askNumericSelection()
            if selection == 0:
                self.__exitProcedure()
                break
            elif selection == 1:
                self.__buildNewProject()
                continue
            elif selection == 2:
                self.__projectSelection()
                continue
            elif selection == 3:
                self.loggerPath = os.path.join(
                    self.__APP_PATH,
                    f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}performanceLog.csv",
                )
                SystemOperations().startMonitoringPerformance_DAEMON(
                    outputLogger=self.loggerPath,
                    printRecord=False,
                )
                continue
            elif selection == 4:
                try:
                    SystemOperations().elevateToHighPerformance()
                except PermissionError:
                    print(
                        PermissionError(
                            "You need administrator privileges to enable function"
                        )
                    )
                    input("Press [Enter] to continue ...")
                continue
            else:
                input(
                    "InvalidSelection: Please select a valid option (Please type [Enter] to continue)..."
                )
                continue

    def __buildNewProject(self) -> None:
        while True:
            print("---------- PROJECT  BUILDER (SELECTION) ----------")

            print("Existing Projects:")
            for path in SystemOperations().listDir(
                path=self.PROJECTS_DIR,
            ):
                print(f"{os.path.basename(path)}")

            print("Please enter the new project name...")
            projectName: str = self.__askForString()

            try:
                SystemOperations.isValidPathString(projectName)
                break
            except ValueError:
                print(
                    f"ValueError: Project Name {projectName} contains invalid characters."
                )
                input("Please type [Enter] to continue...")
                continue

        project = ProjectBuilder(
            projectPath=self.PROJECTS_DIR,
            projectName=projectName,
        )
        print(f"Project Built Successfully at :{project.projectDirPath}")
        print(f"Wold you like to continue working on the builded project?")
        answer = self.__askYesNo()
        if answer:
            self.selectedProject = projectName
            self.selectedProjectPath = project.projectDirPath
            self.__workOnProject()
            pass
        else:
            pass

    def __projectSelection(self) -> None:
        while True:
            print("---------- PROJECT SELECTION (OPTION MENU) ----------")
            print("Existing Projects:")
            projects = SystemOperations().listDir(path=self.PROJECTS_DIR)
            if projects == []:
                print("Error: No existing projects found.")
                print(
                    "Would you rather go to Main Menu [Yes], or build a new project [No]?..."
                )
                selection = self.__askYesNo()
                if selection:
                    self.__mainMenuLoop()
                    break
                else:
                    self.__buildNewProject()
                    break
            for index, path in enumerate(projects):
                print(f"{index}.- {os.path.basename(path)}")
            print("Please select a the project...")
            selection = self.__askNumericSelection()
            try:
                self.selectedProjectPath = projects[selection]
                self.selectedProject = os.path.basename(projects[selection])
                break
            except IndexError:
                print("Invalid selection, you must choose a project by its index")
            continue
        self.__workOnProject()
        pass

    def __workOnProject(self) -> None:
        options = [
            "Return to main menu",
            "Open project directory",
            "Render documents (Traditional)",
            # "Render documents (By Recipe)",
        ]
        while True:
            print("---------- WORK ON PROJECT (OPTION MENU) ----------")
            [print(f"{i}.- {option}") for i, option in enumerate(options)]
            print("Please select an action to take...")
            selection = self.__askNumericSelection()
            if selection == 0:
                self.__mainMenuLoop()
                break
            elif selection == 1:
                SystemOperations().openPath(path=self.selectedProjectPath)
                continue
            elif selection == 2:
                templatesPath = os.path.join(
                    self.selectedProjectPath,
                    self.__TEMPLATE_DIR,
                )
                databasePath = os.path.join(
                    self.selectedProjectPath,
                    self.__DATABASE_DIR,
                    self.__DATABASE_FILE_NAME,
                )
                assetsPath = os.path.join(self.selectedProjectPath, self.__ASSETS_DIR)
                try:
                    WordImageRenderer(
                        templatesDirectory=templatesPath,
                        databasePath=databasePath,
                        outputRenders=self.selectedProjectPath,
                        assetsDirectory=assetsPath,
                    )
                except Exception as e:
                    print(
                        f"While rendering Word Documents following \nException Occurred ({e}): Review manual for Error details"
                    )
                    input("Please type [Enter] to continue...")
                    continue
                try:
                    ExcelRenderer(
                        templatesDirectory=templatesPath,
                        databasePath=databasePath,
                        outputRenders=self.selectedProjectPath,
                    )
                except Exception as e:
                    print(
                        f"While rendering Excel Documents following \nException Occurred ({e}): Review manual for Error details"
                    )
                    input("Please type [Enter] to continue...")
                    continue
                input("Success rendering the documents.\nType [Enter] to continue...")
                continue
            else:
                print("Invalid Selection you must choose the action by index")
                continue
        pass

    pass
