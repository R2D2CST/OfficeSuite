from Func.Excel import Excel
from Func.Word import Word
from Func.PDF import PDF

excel = Excel(filePath="/home/r2d2cst/Documents/OfficeSuite/tests/testFile1.xlsx")
print(excel.filePath)
print(excel.workbook)
print(excel.sheets)
print(excel.workbookData)
excel.printWorkbookData()

print()

word = Word(filePath="/home/r2d2cst/Documents/OfficeSuite/tests/testFile1.docx")
print(word.filePath)
print(word.document)
print(word.paragraphsContent)
print(word.tablesContent)
word.printDocumentContent()

pdf = PDF(filePath="/home/r2d2cst/Documents/OfficeSuite/tests/pdftest.pdf")
print(pdf.filePath)
print(pdf.document)
pdf.printDocumentContent()
