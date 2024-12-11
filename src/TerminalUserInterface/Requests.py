# Python native libraries

# Third party libraries

# Self build libraries


class Requests:
    """
    Class handles the terminal user interface common requests and data validation.
    Methods:
        > askForString: ask the user for a string and returns its response.
        > askForInteger: ask the user for a integer number and returns its response.
        > askForBoolean: ask the user for a True or False answer and returns True or False.
        > askForYesNo: ask the user for a Yes or No answer and returns True or False.
    Raises: None, class handles errors until proper response is given.
    """

    @staticmethod
    def askForString() -> str:
        """
        Method ask the user to type in a response and returns the response validated as a valid string.
        Returns:
            str: user response as a valid string.
        """
        while True:
            request = input("Please type in: ")
            try:
                request = str(request)
            except ValueError:
                print(
                    f"ValueError: Please type a valid string (str).\nYou entry was: {request}"
                )
                input("Type [Enter] to continue ...")
                continue
            except TypeError:
                print(
                    f"TypeError: Please type a valid string (str).\nYou entry was: {request}"
                )
                input("Type [Enter] to continue ...")
                continue
            if request == "":
                print(f"EmptyString: Please type a string not empty.")
                input("Type [Enter] to continue ...")
                continue
            else:
                break
        return request

    @staticmethod
    def askForInteger() -> int:
        """
        Method ask for the user for a valid integer response.
        Returns:
            int: user response or selection
        """
        while True:
            request = input("Please type in: ")
            try:
                request = int(request)
                break
            except ValueError:
                print(
                    f"ValueError: Please type a valid integer (int).\nYou entry was: {request}"
                )
                input("Type [Enter] to continue ...")
                continue
            except TypeError:
                print(
                    f"TypeError: Please type a valid integer (int).\nYou entry was: {request}"
                )
                input("Type [Enter] to continue ...")
                continue
        return request

    @staticmethod
    def askForBoolean() -> bool:
        """
        Method ask for the user for a True or False answer

        Returns:
            bool: True/False user response
        """
        while True:
            request = input("Please type in True (T) / False (F): ")
            trueOptions = ["True", "T"]
            falseOptions = ["False", "F"]
            if request.capitalize() in trueOptions:
                return True
            elif request.capitalize() in falseOptions:
                return False
            else:
                print(
                    "InvalidResponse: Please type a valid response (bool) True / False or T/F.\nYour Entry was: {request}"
                )
                input("Type [Enter] to continue ...")
                continue

    @staticmethod
    def askForYesNo() -> bool:
        """
        Method asks the user for a Yes or No response, if answer is Yes returns True, False otherwise.
        Returns:
            bool: True fro Yes and False otherwise.
        """
        while True:
            request = input("Please tye in Yes (Y) / No (N): ")
            trueOptions = ["Yes", "Y"]
            falseOptions = ["No", "N"]
            if request in trueOptions:
                return True
            elif request in falseOptions:
                return False
            else:
                print(
                    f"InvalidResponse: Please type a valid response Yes (Y) or No (N).\nYour Entry was: {request}"
                )
                input("Type [Enter] to continue ...")
                continue

    pass
