from Func.Excel import Excel
from Func.Word import Word

excel = Excel(filePath="/home/r2d2cst/Documents/OfficeSuite/tests/testFile1.xlsx")
print(excel.filePath)
print(excel.workbook)
print(excel.sheets)

print()

word = Word(filePath="/home/r2d2cst/Documents/OfficeSuite/tests/testFile1.docx")
print(word.filePath)
print(word.document)
