# Python native libraries
from typing import List, Tuple
from mpl_toolkits.mplot3d import Axes3D  # Import for 3D plotting

# Third party libraries
import matplotlib.pyplot as plt
import numpy as np

# Self build libraries
from Func.Graphs.AbstractGraph import AbstractGraph


class Graphs3D(AbstractGraph):
    """
    Class to handle the generation of 3D graphs like surface plots and scatter plots.
    Args:
        > outputPath (str): Directory where the user desaires to dump the generated graph.
        > data (List[Tuple[float, float, float]]): Data in a structure of tuple of three values
        > fileName (str, optional): Graph file nave for saving the graph. Defaults to "graph3D.png".
    Raises:
        ValueError: Data for 3D graphs must be a list of tuples or 2D NumPy arrays
        ValueError: Each data point for 3D scatter must be a tuple of three floats
    """

    def __init__(
        self,
        outputPath: str,
        data: List[Tuple[float, float, float]],
        fileName: str = "graph3D.png",
    ):
        """

        Args:
            > outputPath (str): Directory where the user desaires to dump the generated graph.
            > data (List[Tuple[float, float, float]]): Data in a structure of tuple of three values
            > fileName (str, optional): Graph file nave for saving the graph. Defaults to "graph3D.png".
        """
        super().__init__(outputPath=outputPath, fileName=fileName, data=data)
        self.__rawData: List[Tuple[float, float, float]] = data

    def _validateData(self) -> bool:
        """
        Check if data is valid for 3D graphs (list of tuples for scatter, 2D arrays for surface).
        Raises:
            ValueError: Data for 3D graphs must be a list of tuples or 2D NumPy arrays
            ValueError: Each data point for 3D scatter must be a tuple of three floats
        """
        if not isinstance(self.__rawData, (list, np.ndarray)):
            raise ValueError(
                "Data for 3D graphs must be a list of tuples or 2D NumPy arrays."
            )

        if isinstance(self.__rawData, list):
            for point in self.__rawData:
                if not isinstance(point, tuple) or len(point) != 3:
                    raise ValueError(
                        "Each data point for 3D scatter must be a tuple of three floats."
                    )
        return True

    def __generateScatterPlot3D(self) -> None:
        self.title = self.title or "3D Scatter Plot"
        self.xLabel = self.xLabel or "X-Axis"
        self.yLabel = self.yLabel or "Y-Axis"
        self.zLabel = self.zLabel or "Z-Axis"
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        x, y, z = zip(*self.__rawData)  # Unpack the data into x, y, and z
        ax.scatter(x, y, z, label="3D Scatter Plot")
        ax.legend()
        ax.set_title(self.title)
        ax.set_xlabel(self.xLabel)
        ax.set_ylabel(self.yLabel)
        ax.set_zlabel(self.zLabel)

    def __generateSurfacePlot(self) -> None:
        """
        Raises:
            ValueError: Surface plot requires a 2D NumPy array as input.
        """
        self.title = self.title or "3D Surface Plot"
        self.xLabel = self.xLabel or "X-Axis"
        self.yLabel = self.yLabel or "Y-Axis"
        self.zLabel = self.zLabel or "Z-Axis"
        if not isinstance(self.__rawData, np.ndarray) or len(self.__rawData.shape) != 2:
            raise ValueError("Surface plot requires a 2D NumPy array as input.")
        x = np.linspace(0, 1, self.__rawData.shape[0])
        y = np.linspace(0, 1, self.__rawData.shape[1])
        x, y = np.meshgrid(x, y)
        z = self.__rawData
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(x, y, z, cmap="viridis")
        ax.set_title(self.title)
        ax.set_xlabel(self.xLabel)
        ax.set_ylabel(self.yLabel)
        ax.set_zlabel(self.zLabel)

    def generateGraph(
        self,
        graphType: str,
        title: str = None,
        xLabel: str = None,
        yLabel: str = None,
        zLabel: str = None,
    ) -> None:
        """
        Generate the graph based on the type specified.
        Args:
            graphType (str): Type of graph ('scatter' or 'surface').
        Raise:
            ValueError:Unsupported 3D graph type: {graphType}
            ValueError: Surface plot requires a 2D NumPy array as input.
        """
        self.title = title
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.zLabel = zLabel
        if graphType.lower() == "scatter":
            self.__generateScatterPlot3D()
        elif graphType.lower() == "surface":
            self.__generateSurfacePlot()
        else:
            raise ValueError(f"Unsupported 3D graph type: {graphType}")

        self.saveGraph()
