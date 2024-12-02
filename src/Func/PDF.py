# Python native libraries
import os

# Third-party libraries
import fitz  # PyMuPDF

# Self-build libraries
from Func.AbstractDocument import AbstractDocument


class PDF(AbstractDocument):

    def __init__(self, filePath: str) -> None:
        """
        Initialize the PDF class with a file path.

        Args:
            filePath (str): The path to the PDF file.
        """
        self.filePath = filePath

        # Validate the file type
        self.__validateFiletype()

        # Attempt to read the file
        try:
            self.__readFile()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.filePath}")

    def __validateFiletype(self) -> bool:
        """
        Validates that the file is a valid PDF file.

        Raises:
            ValueError: If the file is not a PDF.
        """
        if ".pdf" not in self.filePath:
            raise ValueError(
                f"Given file path: {self.filePath} is not a valid PDF file."
            )
        return True

    def __readFile(self) -> None:
        """
        Reads the content of the PDF file and stores it as class attributes.

        Attributes:
        document (list[str]): List of text paragraphs from the PDF.
        """
        pdf = fitz.open(self.filePath)

        self.document = []
        for page in pdf:
            # Extract text from each page
            text = page.get_text("text").strip()
            if text:
                self.document.append(text)

        pdf.close()

    def printDocumentContent(self) -> None:
        """
        Print the entire content of the PDF document.
        """
        print(f"--- PDF Document Content ---")
        for pageIndex, content in enumerate(self.document, start=1):
            print(f"\n** Page {pageIndex} **")
            print(content)

    pass
