# Python native libraries
from typing import List, Tuple

# Third party libraries
import matplotlib.pyplot as plt
import numpy as np

# Self build libraries
from Func.Graphs.AbstractGraph import AbstractGraph


class Graphs2D(AbstractGraph):
    """
    Class to handle the generation of 2D graphs like scatter plots and heatmap.
    Args:
        > outputPath (str): Directory where the user desaires to dump the generated graph.
        > data (List[Tuple[float, float]]): list of tuple paired data.
        > fileName (str, optional): Graph file name for saving the graph. Defaults to "graph2D.png".
    Raises:
        ValueError: Data for 2D graphs must be a list of tuples or a NumPy array
        ValueError: If data is not valid for 2D graphs.
    """

    def __init__(
        self,
        outputPath: str,
        data: List[Tuple[float, float]],
        fileName: str = "graph2D.png",
    ):
        """
        Args:
            > outputPath (str): Directory where the user desaires to dump the generated graph.
            > data (List[Tuple[float, float]]): list of tuple paired data.
            > fileName (str, optional): Graph file name for saving the graph. Defaults to "graph2D.png".
        """
        super().__init__(outputPath=outputPath, fileName=fileName, data=data)
        self.__rawData: List[Tuple[float, float]] = data

    def _validateData(self) -> bool:
        """
        Check if data is valid for 2D graphs (list of tuples for scatter, numpy array for heatmap).
        Raises:
            ValueError: Data for 2D graphs must be a list of tuples or a NumPy array
            ValueError: If data is not valid for 2D graphs.
        """
        if not isinstance(self.__rawData, (list, np.ndarray)):
            raise ValueError(
                "Data for 2D graphs must be a list of tuples or a NumPy array."
            )

        if isinstance(self.__rawData, list):
            for point in self.__rawData:
                if not isinstance(point, tuple) or len(point) != 2:
                    raise ValueError(
                        "Each data point for scatter must be a tuple of two floats."
                    )
        return True

    def __generateScatterPlot(self) -> None:
        self.title = self.title or "Scatter Plot"
        self.xLabel = self.xLabel or "X-Axis"
        self.yLabel = self.yLabel or "Y-Axis"
        x, y = zip(*self.__rawData)  # Unpack the data into x and y
        plt.figure()
        plt.scatter(x, y, label="Scatter Plot")
        plt.legend()
        plt.title(self.title)
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)

    def __generateHeatmap(self) -> None:
        self.title = self.title or "Heatmap"
        if not isinstance(self.__rawData, np.ndarray):
            raise ValueError("Heatmap requires a NumPy array as input.")
        plt.figure()
        plt.imshow(self.__rawData, cmap="hot", interpolation="nearest")
        plt.colorbar(label="Intensity")
        plt.title(self.title or "Heatmap")

    def generateGraph(
        self,
        graphType: str,
        title: str = None,
        xLabel: str = None,
        yLabel: str = None,
    ) -> None:
        """
        Generate the graph based on the type specified.
        Args:
            graphType (str): Type of graph ('scatter' or 'heatmap').
        Raise:
            ValueError : Unsupported 2D graph type: {graphType}
        """
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        if graphType.lower() == "scatter":
            self.__generateScatterPlot()
        elif graphType.lower() == "heatmap":
            self.__generateHeatmap()
        else:
            raise ValueError(f"Unsupported 2D graph type: {graphType}")

        self.saveGraph()
