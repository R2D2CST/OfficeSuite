from Render.ProjectBuilder import ProjectBuilder
from Render.Render import Renderer

ProjectBuilder(
    projectPath="/home/r2d2cst/Documents/OfficeSuite/tests",
    projectName="Project Test",
)


renderObject = Renderer(
    templatesDirectory="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test/Templates",
    databasePath="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test/Database/database.xlsx",
    outputRenders="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test",
    assetsDirectory="/home/r2d2cst/Documents/OfficeSuite/tests/Project Test/Assets",
)

renderObject.renderWordDocuments()
renderObject.renderExcelDocuments()
