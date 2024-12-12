# Python native libraries
import os
from datetime import datetime

# Third party libraries

# Self build libraries
from Builder.ProjectBuilder import ProjectBuilder
from SystemOperations.SystemOperations import SystemOperations
from Render.ExcelRender import ExcelRenderer
from Render.WordImageRender import WordImageRenderer
from TerminalUserInterface.Requests import Requests
from TerminalUserInterface.Procedures import Procedures


class TerminalUserInterface(Requests, Procedures):
    """
    Class manages the main terminal application for automate Office Suite documents.
    """

    def __init__(self):

        # We initialize our class constants and attributes.
        self.initializeProcedures()
        self.__buildConstants()

        # We initialize our main loop.
        self.__mainMenuLoop()
        pass

    def __buildConstants(self):
        """
        Method builds the constants the application will be using during a normal operation.
        """
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
        self.__WORK_ON_PROJECT_OPTIONS = [
            "Return to main menu",
            "Open project directory",
            "Render documents (All)",
            # "Render documents (By Recipe)",
        ]
        pass

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
        self.__printHeader()
        while True:
            self.__printMainMenu()
            selection = self.askForInteger()
            # Exit program
            if selection == 0:
                self.exitProcedure()
                break
            # Build new project
            elif selection == 1:
                self.__buildNewProjectMenu()
                continue
            # Select a previous built project
            elif selection == 2:
                self.__projectSelection()
                continue
            elif selection == 3:
                self.__DAEMON = True
                self.loggerPath = os.path.join(
                    self._Procedures__APP_PATH,
                    f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}performanceLog.csv",
                )
                self._Procedures__SYS_OBJ.startMonitoringPerformance_DAEMON(
                    outputLogger=self.loggerPath,
                    printRecord=False,
                )
                input("Press [Enter] to continue ...")
                continue
            elif selection == 4:
                try:
                    self._Procedures__SYS_OBJ.elevateToHighPerformance()
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

    def __buildNewProjectMenu(self) -> None:
        while True:
            print("---------- PROJECT  BUILDER (SELECTION) ----------")
            self.printExistingProjects()
            print("Please enter the new project name...")
            projectName: str = self.askForString()
            try:
                self._Procedures__SYS_OBJ.isValidPathString(projectName)
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
        answer = self.askForYesNo()
        if answer:
            self.selectedProject = projectName
            self.selectedProjectPath = project.projectDirPath
            self.__workOnProject()
            pass
        else:
            pass
        pass

    def __projectSelection(self) -> None:
        while True:
            print("---------- PROJECT SELECTION (OPTION MENU) ----------")
            self.printExistingProjects()
            print("Existing Projects:")
            if self._Procedures__projectsList == []:
                print("Error: No existing projects found.")
                print(
                    "Would you rather go to Main Menu [Yes], or build a new project [No]?..."
                )
                selection = self.askForYesNo()
                if selection:
                    self.__mainMenuLoop()
                    break
                else:
                    self.__buildNewProjectMenu()
                    break
            print("Please select a the project...")
            selection = self.askForInteger()
            try:
                self.selectedProjectPath = self._Procedures__projectsList[selection]
                self.selectedProject = os.path.basename(
                    self._Procedures__projectsList[selection]
                )
                break
            except IndexError:
                print("Invalid selection, you must choose a project by its index")
            continue
        self.__workOnProject()
        pass

    def __workOnProject(self) -> None:
        while True:
            print("---------- WORK ON PROJECT (OPTION MENU) ----------")
            [
                print(f"{i}.- {option}")
                for i, option in enumerate(self.__WORK_ON_PROJECT_OPTIONS)
            ]
            print("Please select an action to take...")
            selection = self.askForInteger()
            if selection == 0:
                self.__mainMenuLoop()
                break
            elif selection == 1:
                self._Procedures__SYS_OBJ.openPath(
                    path=self.selectedProjectPath,
                )
                continue
            elif selection == 2:
                templatesPath = os.path.join(
                    self.selectedProjectPath,
                    self._Procedures__TEMPLATE_DIR,
                )
                databasePath = os.path.join(
                    self.selectedProjectPath,
                    self._Procedures__DATABASE_DIR,
                    self._Procedures__DATABASE_FILE_NAME,
                )
                assetsPath = os.path.join(
                    self.selectedProjectPath,
                    self._Procedures__ASSETS_DIR,
                )
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
