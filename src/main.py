from Builder.ProjectBuilder import ProjectBuilder
from Render.ExcelRender import ExcelRenderer
from Render.WordRender import WordRender
from Render.WordImageRender import WordImageRenderer

from Func.Graphs.Graphs1D import Graphs1D
from Func.Graphs.Graphs2D import Graphs2D
from Func.Graphs.Graphs3D import Graphs3D

# Test libraries
import os
import numpy as np

"""
ProjectBuilder(
    projectPath="/home/r2d2cst/Documents/OfficeSuite/tests",
    projectName="Nuevo Proyecto",
)
"""
"""
ExcelRenderer(
    templatesDirectory="/home/r2d2cst/Documents/OfficeSuite/tests/Nuevo Proyecto/Templates",
    databasePath="/home/r2d2cst/Documents/OfficeSuite/tests/Nuevo Proyecto/Database/database.xlsx",
    outputRenders="/home/r2d2cst/Documents/OfficeSuite/tests/Nuevo Proyecto",
)

WordImageRenderer(
    templatesDirectory="/home/r2d2cst/Documents/OfficeSuite/tests/Nuevo Proyecto/Templates",
    databasePath="/home/r2d2cst/Documents/OfficeSuite/tests/Nuevo Proyecto/Database/database.xlsx",
    outputRenders="/home/r2d2cst/Documents/OfficeSuite/tests/Nuevo Proyecto",
    assetsDirectory="/home/r2d2cst/Documents/OfficeSuite/tests/Nuevo Proyecto/Assets",
)
"""


def test_graphs1D():
    """
    Test the Graphs1D class with line, bar, and histogram graphs.
    """
    outputPath = "/home/r2d2cst/Documents/OfficeSuite/tests"
    data = [1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 9, 10]

    # Test line graph
    graph = Graphs1D(outputPath=outputPath, data=data, fileName="line_graph.png")
    graph.generateGraph(graphType="Line")
    assert os.path.exists(
        os.path.join(outputPath, "line_graph.png")
    ), "Line graph not created."

    # Test bar graph
    graph = Graphs1D(outputPath=outputPath, data=data, fileName="bar_graph.png")
    graph.generateGraph(graphType="Bar")
    assert os.path.exists(
        os.path.join(outputPath, "bar_graph.png")
    ), "Bar graph not created."

    # Test histogram graph
    graph = Graphs1D(outputPath=outputPath, data=data, fileName="histogram_graph.png")
    graph.generateGraph(graphType="Histogram")
    assert os.path.exists(
        os.path.join(outputPath, "histogram_graph.png")
    ), "Histogram graph not created."


def test_graphs2D():
    """
    Test the Graphs2D class with scatter and heatmap graphs.
    """
    outputPath = "/home/r2d2cst/Documents/OfficeSuite/tests"

    # Scatter data
    scatterData = [(1, 2), (2, 4), (3, 6), (4, 8)]
    graph = Graphs2D(
        outputPath=outputPath, data=scatterData, fileName="scatter_plot.png"
    )
    graph.generateGraph(graphType="Scatter")
    assert os.path.exists(
        os.path.join(outputPath, "scatter_plot.png")
    ), "Scatter plot not created."

    # Heatmap data
    heatmapData = np.random.rand(10, 10)
    graph = Graphs2D(outputPath=outputPath, data=heatmapData, fileName="heatmap.png")
    graph.generateGraph(graphType="Heatmap")
    assert os.path.exists(
        os.path.join(outputPath, "heatmap.png")
    ), "Heatmap not created."


def test_graphs3D():
    """
    Test the Graphs3D class with scatter and surface plots.
    """
    outputPath = "/home/r2d2cst/Documents/OfficeSuite/tests"

    # Scatter data
    scatterData = [(1, 2, 3), (2, 4, 6), (3, 6, 9), (4, 8, 12)]
    graph = Graphs3D(outputPath=outputPath, data=scatterData, fileName="scatter_3d.png")
    graph.generateGraph(graphType="Scatter")
    assert os.path.exists(
        os.path.join(outputPath, "scatter_3d.png")
    ), "3D Scatter plot not created."

    # Surface data
    x = np.linspace(-5, 5, 30)
    y = np.linspace(-5, 5, 30)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x**2 + y**2))
    graph = Graphs3D(outputPath=outputPath, data=z, fileName="surface_plot.png")
    graph.generateGraph(graphType="Surface")
    assert os.path.exists(
        os.path.join(outputPath, "surface_plot.png")
    ), "3D Surface plot not created."


if __name__ == "__main__":
    test_graphs1D()
    test_graphs2D()
    test_graphs3D()
    print("All tests passed!")
