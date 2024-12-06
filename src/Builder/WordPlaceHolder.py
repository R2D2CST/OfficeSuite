# Python native libraries
import os

# Third party libraries

# Self build libraries
from Func.Word.Word import Word


class WordPlaceHolder(Word):

    def __init__(
        self,
        templatePath: str,
        placeholdersDirectory: str = False,
    ) -> None:
        # We inherit all Parent class attributes and methods
        super().__init__(filePath=templatePath)
        # We write and Save the content file
        self.__buildDummyContent()
        self.placeholdersDirectory = placeholdersDirectory
        # ! We disable this function until its working
        # if self.placeholdersDirectory:
        #   self.__addPlaceholders()
        self.saveAndClose()
        pass

    def __buildDummyContent(self):
        self.document.add_heading(
            text="Instructions of Use:",
        )
        content = [
            "Welcome! This is a sample template to automate your reports or documents "
            "using keywords and placeholders. Follow these instructions to set up the database and assets:",
            "",
            "## General Instructions",
            "1. **Keywords**: Keywords are placeholders enclosed in double curly brackets, e.g., `{{Key_Word_1}}`.",
            "2. **Database File**: Use the provided Excel file (`database.xlsx`) to populate data for rendering documents.",
            "3. **Placeholders**: Placeholders for images must be specified in the `Placeholders` sheet of the database.",
            "",
            "## Setting Up the Database for Word Templates",
            "1. **Header Row**: The first row (Row 1) in the Excel database defines the keywords. "
            "Write the keywords without curly brackets (e.g., `Key_Word_1`).",
            "2. **Data Rows**: Each subsequent row represents a set of values that replace the keywords.",
            "   - Example:",
            "     |   Key_Header  | Key_Word_1  | Key_Word_2  |",
            "     |---------------|-------------|-------------|",
            "     | Run 1 DocName | Value 1     | Value 2     |",
            "     | Run 2 DocName | Value 3     | Value 4     |",
            "",
            "## Setting Up the Database for Excel Templates",
            "1. **File Header**: The first column in the database defines the file and directory headers.",
            "2. **Pointer Rows**:",
            "   - Row 1: Headers (content doesn't matter).",
            "   - Row 2: Cell pointers indicating where to insert values.",
            "   - Row 3: Sheet pointers specifying the sheet where the cell pointer applies.",
            "3. **Data Rows**: Rows below the pointers provide values for replacement.",
            "   - Ensure all pointers are accurate to avoid rendering errors.",
            "",
            "## Adding Images as Placeholders",
            "1. **Image Directory**: Place all replacement images in the specified `Assets` directory.",
            "2. **Image References**: In the `Placeholders` sheet of the database, specify the image filenames with their extensions (e.g., `image1.png`).",
            "3. **Placeholder Cleanup**: Remove any unused placeholders from the database to prevent errors.",
            "",
            "## Rendering the Documents",
            "1. Populate the database as per the instructions above.",
            "2. Run the program with the template and database to generate the final document.",
            "3. Inspect the output to verify that all replacements have been correctly applied.",
            "",
            "Feel free to experiment with this template and see how the system works!",
            "",
            "Below these keywords, the program will read each row as the value associated with that keyword as example.",
            "",
            "Key_Word_1\t:\t{{Key_Word_1}}",
            "Key_Word_2\t:\t{{Key_Word_2}}",
            "Key_Word_3\t:\t{{Key_Word_3}}",
            "Key_Word_4\t:\t{{Key_Word_4}}",
            "Key_Word_5\t:\t{{Key_Word_5}}",
            "Key_Word_6\t:\t{{Key_Word_6}}",
            "Key_Word_7\t:\t{{Key_Word_7}}",
            "Key_Word_8\t:\t{{Key_Word_8}}",
            "Key_Word_9\t:\t{{Key_Word_9}}",
            "Place_Holder_1\t:\t{{Place_Holder_1}}",
            "Place_Holder_2\t:\t{{Place_Holder_2}}",
            "Place_Holder_3\t:\t{{Place_Holder_3}}",
            "Place_Holder_4\t:\t{{Place_Holder_4}}",
            "Place_Holder_5\t:\t{{Place_Holder_5}}",
            "Place_Holder_9\t:\t{{Place_Holder_6}}",
            "Place_Holder_7\t:\t{{Place_Holder_7}}",
            "Place_Holder_8\t:\t{{Place_Holder_8}}",
            "Place_Holder_9\t:\t{{Place_Holder_9}}",
            "Place_Holder_10\t:\t{{Place_Holder_10}}",
            "Place_Holder_11\t:\t{{Place_Holder_11}}",
            "Place_Holder_12\t:\t{{Place_Holder_12}}",
            "Place_Holder_13\t:\t{{Place_Holder_13}}",
            "Place_Holder_14\t:\t{{Place_Holder_14}}",
            "Place_Holder_15\t:\t{{Place_Holder_15}}",
            "Place_Holder_16\t:\t{{Place_Holder_16}}",
            "Place_Holder_17\t:\t{{Place_Holder_17}}",
            "Place_Holder_18\t:\t{{Place_Holder_18}}",
            "Place_Holder_19\t:\t{{Place_Holder_19}}",
            "Place_Holder_20\t:\t{{Place_Holder_20}}",
            "Place_Holder_21\t:\t{{Place_Holder_21}}",
            "Place_Holder_22\t:\t{{Place_Holder_22}}",
            "Place_Holder_23\t:\t{{Place_Holder_23}}",
            "Place_Holder_24\t:\t{{Place_Holder_24}}",
            "Place_Holder_25\t:\t{{Place_Holder_25}}",
        ]
        for paragraph in content:
            self.document.add_paragraph(text=paragraph)
        pass

    def __addPlaceholders(self) -> None:
        # Validate if the directory exists
        if not self.placeholdersDirectory or not os.path.exists(
            self.placeholdersDirectory
        ):
            raise FileNotFoundError("Placeholder Directory cant't be found")

        # We get all dummy images inside the directory
        listOfContents = [
            os.path.join(self.placeholdersDirectory, item)
            for item in os.listdir(self.placeholdersDirectory)
            if item.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        if not listOfContents:
            raise ValueError(
                "Placeholder dummy images can't be found inside the directory"
            )

        # We add each image into the document
        for imagePath in listOfContents:
            try:
                self.document.add_picture(imagePath)
            except Exception as e:
                print(f"Image could not get placed {imagePath}: {e}")
        pass

    pass
