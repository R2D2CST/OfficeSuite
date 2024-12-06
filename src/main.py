from Builder.ProjectBuilder import ProjectBuilder
from Render.ExcelRender import ExcelRenderer
from Render.WordRender import WordRender
from Render.WordImageRender import WordImageRenderer

ProjectBuilder(
    projectPath="/home/r2d2cst/Documents/OfficeSuite/tests",
    projectName="Project Test",
)


renderWord = WordRender(
    templatesDirectory="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test/Templates",
    databasePath="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test/Database/database.xlsx",
    outputRenders="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test",
)


renderExcel = ExcelRenderer(
    templatesDirectory="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test/Templates",
    databasePath="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test/Database/database.xlsx",
    outputRenders="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test",
)

"""
renderObject = WordImageRenderer(
    templatesDirectory="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test/Templates",
    databasePath="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test/Database/database.xlsx",
    outputRenders="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test",
    assetsDirectory="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test/Assets",
)
"""
