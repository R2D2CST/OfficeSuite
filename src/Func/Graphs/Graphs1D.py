# Python native libraries
from typing import List, Any

# Third party libraries
import matplotlib.pyplot as plt

# Self build libraries
from Func.Graphs.AbstractGraph import AbstractGraph


class Graphs1D(AbstractGraph):
    """
    Args:
        outputPath (str): Directory where we will save the built graph
        data (List[Any]): Information we will graph as a homogenous List [Any]
        fileName (str, optional): File name for the PNG graph file type. Defaults to "graph.png".
        Raise:
        > ValueError : Data for 1D graphs must be a list type List[Any]
        > TypeError : Data for 1D graphs must be homogeneous
    Meth:
        > generateGraph : Method that builds the graph type specified by the user.
    Parent:
        AbstractGraph (_type_): _description_
    """

    def __init__(
        self,
        outputPath: str,
        data: Any,
        fileName: str = "graph1D.png",
    ):
        """
        Initializes the class preparing the raw data for making a graph.

        Args:
            outputPath (str): Directory where we will save the built graph
            data (List[Any]): Information we will graph as a homogenous List [Any]
            fileName (str, optional): File name for the PNG graph file type. Defaults to "graph.png".
        """
        self.outputPath = outputPath
        self.fileName = fileName
        self.__rawData: List[Any] = data
        pass

    def _validateData(self) -> bool:
        """
        Check if data is valid for 1D graphs (e.g., numeric or categorical).
            Raise:
            > ValueError : Data for 1D graphs must be a list type List[Any]
            > TypeError : Data for 1D graphs must be homogeneous
        """
        if not isinstance(self.__rawData, list):
            raise ValueError("Data for 1D graphs must be a list type List[Any].")
        for element in self.rawData:
            if not isinstance(element, type(self.rawData[0])):
                raise TypeError("Data for 1D graphs must be homogeneous")
        return True

    def __generateLineGraph(self) -> None:
        """
        Generates a Line Graph
        """

        self.title = self.title or "Line Graph"
        self.xLabel = self.xLabel or "Index"
        self.yLabel = self.yLabel or "Values"

        plt.figure()
        plt.plot(self.__rawData, label="Line Graph")
        plt.legend()
        plt.title(self.title)
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        pass

    def __generateBarGraph(self) -> None:
        """
        Generates a Bar Graph type
        """

        self.title = self.title or "Bar Graph"
        self.xLabel = self.xLabel or "Index"
        self.yLabel = self.yLabel or "Values"

        plt.figure()
        plt.bar(range(len(self.__rawData)), self.__rawData, label="Bar Graph")
        plt.legend()
        plt.title(self.title)
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        pass

    def __generateHistogramGraph(self) -> None:
        """
        Generates a Histogram graph type
        """

        self.title = self.title or "Histogram Graph"
        self.xLabel = self.xLabel or "Bins"
        self.yLabel = self.yLabel or "Frequency"

        plt.figure()
        plt.hist(self.__rawData, bins=10, label="Histogram")
        plt.legend()
        plt.title(self.title)
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        pass

    def generateGraph(
        self,
        graphType: str,
        title: str = None,
        xLabel: str = None,
        yLabel: str = None,
    ) -> None:
        """
        Method generates the graph type specified by the user and saves the Graph into the output path.
        Args:
            > graphType (str): Line, Bar, Histogram type graph.
        Raises:
            ValueError: Unsupported 1D graph type: {graphType}
        """

        self.graphType = graphType
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel

        if self.graphType.lower() == "line":
            self.__generateLineGraph()
            pass
        elif self.graphType.lower() == "bar":
            self.__generateBarGraph()
            pass
        elif self.graphType.lower() == "histogram":
            self.__generateHistogramGraph()
            pass
        else:
            raise ValueError(f"Unsupported 1D graph type: {self.graphType}")

        self.saveGraph()

    pass
