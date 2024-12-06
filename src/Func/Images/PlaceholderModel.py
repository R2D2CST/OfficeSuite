from PIL import Image, ImageDraw
import os


class PlaceholderModel:
    """
    Class generates placeholder images to replace in document templates
    Args:
        > outputPath (str): _description_
        > number (int, optional): _description_. Defaults to 1.
        > width (int, optional): _description_. Defaults to 400.
        > height (int, optional): _description_. Defaults to 400.
    """

    def __init__(
        self,
        outputPath: str,
        number: int = 1,
        width: int = 400,
        height: int = 400,
    ) -> None:
        """
        Method executes the procedure to build an image placeholder for our rendering document templates

        Args:
            outputPath (str): _description_
            number (int, optional): _description_. Defaults to 1.
            width (int, optional): _description_. Defaults to 400.
            height (int, optional): _description_. Defaults to 400.
        """
        # We set our class attributes for building our place holders
        self.__outputPath = outputPath
        self.__number = number
        self.__size = width, height
        self.__buildPlaceholders()
        pass

    def __buildImage(self, placeholderText: str, outputFilePath: str) -> None:
        """
        Private Method describes the procedure in order to build a single place holder.
        Args:
            placeholderText (str): _description_
            outputFilePath (str): _description_
        """
        # Draw base image
        image = Image.new(mode="RGB", size=self.__size, color="gray")
        draw = ImageDraw.Draw(image)

        # Draw red borders
        borderColor = "red"
        borderWidth = 5
        width, height = self.__size
        draw.rectangle(
            [
                (borderWidth, borderWidth),
                (width - borderWidth, height - borderWidth),
            ],
            outline=borderColor,
            width=borderWidth,
        )

        # Draw a red cross (X)
        draw.line(
            [
                (0, 0),
                (width, height),
            ],
            fill=borderColor,
            width=borderWidth,
        )
        draw.line(
            [
                (0, height),
                (width, 0),
            ],
            fill=borderColor,
            width=borderWidth,
        )

        # Save the recently draw image
        image.save(outputFilePath)

    def __buildPlaceholders(self) -> None:
        """
        Method describes the procedure to build the amount of placeholders asked in need by the user.
        """
        # +1 in order to build as many placeholders indicated by the user
        for index in range(1, self.__number + 1, 1):
            placeholderText = f"Replace_Image_{index}"
            outputFilePath = os.path.join(
                self.__outputPath,
                f"{placeholderText}.png",
            )
            self.__buildImage(
                placeholderText=placeholderText,
                outputFilePath=outputFilePath,
            )
        pass

    pass
