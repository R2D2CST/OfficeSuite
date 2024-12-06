# Python native libraries
import os
from abc import ABC, abstractmethod
from typing import Any

# Third party libraries
import matplotlib.pyplot as plt

# Self build libraries


class AbstractGraph(ABC):
    """
    Class handles the abstraction of the main functions and attributes required for graph building, while rendering documents.
    Args:
        > outputPath (str): Directory where the graph will be saved.
        > fileName (str, optional): Graph title name. Defaults to "graph.png".
    Attr:
        > outputPath (str): Directory where the graph will be saved.
        > fileName (str, optional): Graph title name. Defaults to "graph.png".
    Meth:
        > saveGraph ()->None: Method saves the graph into a png file type.
    Parent:
        > ABC (Abstract): abstract class
    """

    def __init__(
        self,
        outputPath: str,
        data: Any,
        fileName: str = "graph.png",
    ) -> None:
        """
        Method that initializes the main attributes required for the graphs generation

        Args:
            outputPath (str): Directory where the graph will be saved.
            fileName (str, optional): Graph title name. Defaults to "graph".
        """
        self.outputPath = outputPath
        self.fileName = fileName
        self.rawData = data

        pass

    @abstractmethod
    def _validateData(self) -> bool:
        """
        Validate the data format for the specific type of graph.
        Raises: TypeError : Invalid Data {data}
        """
        if not self.rawData:
            raise TypeError(f"Invalid Data: {self.rawData}")

        return True

    def _validateSavingPath(self) -> str:
        """
        Validates if a previous file exists in the given path and adds a marker to prevent overwriting a previos file.
        Returns:
            str: savingPath (str): file path where to save the  generated graph
        """
        if not os.path.exists(self.outputPath):
            os.mkdir(self.outputPath)
        savingPath = os.path.join(self.outputPath, self.fileName)

        while True:
            i = 1  # Reference Counter
            if os.path.exists(savingPath):
                fileName = os.path.basename(self.fileName).split(".")
                fileName = f"{self.fileName} {i}.png"
                i += 1
                savingPath = os.path.join(self.outputPath, fileName)
                continue

            else:
                break

        return savingPath

    def saveGraph(self) -> None:
        """
        Save the graph to the specified output path.
        Args: None
        Returns: None
        Raises: None
        """
        plt.savefig(self._validateSavingPath())
        plt.close()

        pass

    pass
