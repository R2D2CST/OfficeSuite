from PIL import Image, ImageDraw, ImageFont
import os


class Placeholder:
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
        image = Image.new(mode="RGB", size=self.__size, color="white")
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

        # Adjust font size dynamically to fit the image
        fontColor = "black"
        maxFontSize = 20  # Initial font size
        try:
            font = ImageFont.truetype("arial.ttf", maxFontSize)
            text_bbox = draw.textbbox((0, 0), placeholderText, font=font)
            textWidth, textHeight = (
                text_bbox[2] - text_bbox[0],
                text_bbox[3] - text_bbox[1],
            )
        except IOError:
            # Fallback to a basic Pillow font if TrueType font is unavailable
            font = ImageFont.load_default()
            text_bbox = draw.textbbox(
                (0, 0),
                placeholderText,
                font=font,
                font_size=20,
            )
            textWidth, textHeight = (
                text_bbox[2] - text_bbox[0],
                text_bbox[3] - text_bbox[1],
            )

        # Calculate position to center the text
        textX = (width - textWidth) // 2
        textY = (height - textHeight) // 2

        # Draw the text on the image
        draw.text((textX, textY), placeholderText, fill=fontColor, font=font)

        # Save the recently draw image
        image.save(outputFilePath)

    def __buildPlaceholders(self) -> None:
        """
        Method describes the procedure to build the amount of placeholders asked in need by the user.
        """
        # +1 in order to build as many placeholders indicated by the user
        for index in range(1, self.__number + 1, 1):
            placeholderText = f"Place_Holder_{index}"
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
