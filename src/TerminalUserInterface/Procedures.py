# Python native libraries
import os

# Third party libraries

# Self build libraries
from SystemOperations.SystemOperations import SystemOperations


class Procedures:
    """
    Class handles the procedures for execution in our interface.
    """

    def initializeProcedures(self) -> None:
        """
        Procedure initializes the class variables for executing the terminal user interface procedures.
        """
        self.__Daemon = False  # Variable measure if a DAEMON is active.
        self.__SYS_OBJ = SystemOperations()
        self.__APP_PATH = self.__SYS_OBJ.getAppPath()
        self.PROJECTS_DIR = os.path.join(self.__APP_PATH, "Projects")
        if not os.path.exists(self.PROJECTS_DIR):
            os.mkdir(self.PROJECTS_DIR)
        self.__OS_KERNEL = self.__SYS_OBJ.operativeSystem
        self.__TEMPLATE_DIR = "Templates"
        self.__DATABASE_DIR = "Database"
        self.__DATABASE_FILE_NAME = "database.xlsx"
        self.__ASSETS_DIR = "Assets"
        self.__updateProjectList()
        pass

    def __updateProjectList(self) -> None:
        """
        Method updates the content in the project list private variable.
        """
        self.__projectsList = self.__SYS_OBJ.listDir(path=self.PROJECTS_DIR)

    def exitProcedure(self) -> None:
        """
        Method checks if a Daemon process has been initiated and closes it and then exits the application.
        """
        if self.__Daemon:
            self.__SYS_OBJ.stopMonitoringPerformance_DAEMON()
            print("----- Daemon process stop with success -----")
            input("Until next time (Please type [Enter] to exit...")
            exit()
        else:
            input("Until next time (Please type [Enter] to exit...")
            exit()
        pass

    def printExistingProjects(self) -> None:
        print("Existing Projects:")
        for index, path in enumerate(self.__projectsList):
            print(f"{index}.- {os.path.basename(path)}")
        if self.__projectsList == []:
            print("-----There are no project built inside-----")
        pass

    pass
