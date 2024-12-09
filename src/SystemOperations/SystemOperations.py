# Native python libraries
from multiprocessing import Process, Event
import subprocess
import platform
import sys
import os
import re
import csv
import time

# Third party libraries
import psutil
from pynput import keyboard

# Self build libraries


class SystemOperations:
    """
    Class for handling operative system ordinary actions.
        Args: None
        Return: None
        Raises: None
    """

    def __init__(self) -> None:
        """
        Class initializes and auto detects on witch operative system user is running the application.
            Args: None
            Return: None
            Raises: None
        """
        self.operativeSystem: str = self.getOperativeSystem()

        pass

    def getOperativeSystem(self) -> str:
        """
        Returns the actual running operative system.
            Args: None
            Returns: platform system (str): Linux, Windows, Java, Darwin
            Raises: None
        """
        return platform.system()

    def openPath(self, path: str):
        """
        Method opens in the operative system explorer or predtermined application the file or directory path.
        Raises:
            ValueError: The specified path does not exist: {path}
            NotImplementedError: Unsupported operating system: {self.operativeSystem}
        """

        if not os.path.exists(path):
            raise ValueError(f"The specified path does not exist: {path}")

        if self.operativeSystem == "Windows":
            os.startfile(path)
        elif self.operativeSystem == "Darwin":
            subprocess.run(["open", path], check=True)
        elif self.operativeSystem == "Linux":
            subprocess.run(["xdg-open", path], check=True)
            pass
        else:
            raise NotImplementedError(
                f"Unsupported operating system: {self.operativeSystem}"
            )

    def elevateToHighPerformance(self) -> None:
        """
        Elevates the program to high performance mode by adjusting process priority.

        Raises:
            NotImplementedError: If the operation is not supported on the current OS.
        """
        if self.operativeSystem == "Windows":
            # Set process priority to high
            p = psutil.Process(os.getpid())
            p.nice(psutil.HIGH_PRIORITY_CLASS)
            print("Process priority set to high.")
        elif self.operativeSystem in ["Linux", "Darwin"]:  # macOS is 'Darwin'
            # Use nice to adjust priority
            try:
                os.nice(-20)  # Set to highest priority
                print("Process priority set to high.")
            except PermissionError:
                raise PermissionError(
                    "You need administrator privileges to enable this function."
                )
        else:
            raise NotImplementedError(
                f"High-performance mode is not supported on this OS: {self.operativeSystem}"
            )
        pass

    def startMonitoringPerformance_DAEMON(
        self,
        outputLogger: str,
        printRecord=True,
    ) -> None:
        """
        Starts a daemon process to record system performance in a CSV file every 3 seconds.

        Args:
            outputLogger (str): Path to save the CSV file.

        Raises:
            ValueError: If the specified path is invalid.
        """
        # Event to signal stopping the daemon process
        self.performanceStopEvent = Event()
        # Holds the reference to the performance daemon process
        self.performanceProcess = None

        if not os.path.isdir(os.path.dirname(outputLogger)):
            raise ValueError(f"Invalid directory for output file: {outputLogger}")

        if self.performanceProcess and self.performanceProcess.is_alive():
            raise RuntimeError("Performance daemon is already running.")

        # Ensure the stop event is cleared
        self.performanceStopEvent.clear()
        self.performanceProcess = Process(
            target=self._recordPerformanceDaemon,
            args=(outputLogger, self.performanceStopEvent, printRecord),
            daemon=True,
        )
        self.performanceProcess.start()
        print("Performance daemon started.")
        pass

    def stopMonitoringPerformance_DAEMON(self) -> None:
        """
        Signals the daemon process to stop and waits for it to terminate.
        """
        if self.performanceProcess and self.performanceProcess.is_alive():
            self.performanceStopEvent.set()  # Signal the process to stop
            self.performanceProcess.join()  # Wait for the process to terminate
            print("Performance daemon stopped.")
        else:
            print("No active performance daemon to stop.")

    @staticmethod
    def _recordPerformanceDaemon(
        outputCsvPath: str,
        stopEvent,
        printRecord: bool,
    ) -> None:
        """
        Daemon process function to record detailed system performance to two CSV files
        (specific and general) every 3 seconds.

        Args:
            outputCsvPath (str): Base path for the CSV files.
            stopEvent (Event): Event object to signal when to stop the process.
            printRecord (bool): Whether to print records to the console.
        """

        # Generate specific and general filenames
        basePath, extension = os.path.splitext(outputCsvPath)
        specificCsvPath = f"{basePath} (specific){extension}"
        generalCsvPath = f"{basePath} (general){extension}"

        with open(specificCsvPath, mode="w", newline="") as specificFile, open(
            generalCsvPath, mode="w", newline=""
        ) as generalFile:
            specificWriter = csv.writer(specificFile)
            generalWriter = csv.writer(generalFile)

            # Headers for system-wide metrics (specific)
            specificWriter.writerow(
                [
                    "Timestamp",
                    "CPU Usage (%)",
                    "Memory Usage (%)",
                    "Available Memory (MB)",
                    "Disk Usage (%)",
                    "Read Speed (MB/s)",
                    "Write Speed (MB/s)",
                    "Network Sent (MB)",
                    "Network Received (MB)",
                ]
            )

            # Headers for per-process metrics (general)
            generalWriter.writerow(
                [
                    "Timestamp",
                    "PID",
                    "Process Name",
                    "CPU Usage (%)",
                    "Memory Usage (%)",
                ]
            )

            while not stopEvent.is_set():
                # Collect system-wide performance metrics
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                cpuUsage = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                memoryUsage = memory.percent
                availableMemory = memory.available / (1024 * 1024)  # Convert to MB
                disk = psutil.disk_usage("/")
                diskUsage = disk.percent
                ioCounters = psutil.disk_io_counters()
                readSpeed = ioCounters.read_bytes / (1024 * 1024)  # Convert to MB
                writeSpeed = ioCounters.write_bytes / (1024 * 1024)  # Convert to MB
                netIo = psutil.net_io_counters()
                netSent = netIo.bytes_sent / (1024 * 1024)  # Convert to MB
                netReceived = netIo.bytes_recv / (1024 * 1024)  # Convert to MB

                # Write system-wide metrics to specific CSV
                specificWriter.writerow(
                    [
                        timestamp,
                        cpuUsage,
                        memoryUsage,
                        availableMemory,
                        diskUsage,
                        readSpeed,
                        writeSpeed,
                        netSent,
                        netReceived,
                    ]
                )
                specificFile.flush()  # Ensure data is written to disk

                # Collect per-process performance metrics
                for process in psutil.process_iter(
                    attrs=["pid", "name", "cpu_percent", "memory_percent"]
                ):
                    try:
                        generalWriter.writerow(
                            [
                                timestamp,
                                process.info["pid"],
                                process.info["name"],
                                process.info["cpu_percent"],
                                process.info["memory_percent"],
                            ]
                        )
                        generalFile.flush()  # Ensure data is written to disk
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        # Handle processes that might terminate during iteration
                        continue

                if printRecord:
                    # Print system-wide metrics for debugging (optional)
                    print(
                        f"{timestamp} | CPU: {cpuUsage}% | Memory: {memoryUsage}% | "
                        f"Available Mem: {availableMemory}MB | Disk: {diskUsage}% | "
                        f"Read: {readSpeed}MB/s | Write: {writeSpeed}MB/s | "
                        f"Net Sent: {netSent}MB | Net Recv: {netReceived}MB"
                    )

                # Wait for 3 seconds before the next recording
                time.sleep(3)

    @staticmethod
    def getAppPath() -> str:
        """
        This function gets the path where the current code is been executed, this path will be an absolute path to the file in order to get files and saving elements.
        Returns:
            > script_directory (str): string containing the directory path absolute path.
        """
        # We get the absolute path where the program will be executed.
        if getattr(sys, "frozen", False):
            # If the program has been packed for distribution follows this path.
            script_directory = os.path.dirname(sys.executable)
        else:
            # If program is been executed as a python file.
            script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
            """
            When this is not main:
            script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 
            When this is main or we desire the module path:
            script_directory = os.path.dirname(os.path.abspath(__file__) 
            """
        # Returns the script directory.
        return script_directory

    @staticmethod
    def listDir(path: str) -> list[str]:
        """
        Returns a list of file paths and path directories contained in a given path. Simulates the Dir function in bash.
            Returns:
                > listDir (str): list of file paths and directories contained in the given path.
            Args:
                > path (str): path where the function will return ints content, if empty returns an empty list.
            Raises: None
        """
        if not os.path.exists(path):
            raise ValueError(f"Path '{path}' does not exist.")
        if not os.path.isdir(path):
            raise ValueError(f"Path '{path}' is not a directory.")

        # Get all items in the directory (files and subdirectories)
        return [os.path.join(path, item) for item in os.listdir(path)]

    @staticmethod
    def stripPath(path: str) -> str:
        """
        Returns the file name with it's file extension and strips the entire path chain.
            Return:
                > filename (str): file name with extension.
            Args:
                > path (str): file path to strip the path chain.
            Raises:
                > Error, not a file type path.
                > Error, empty path given.
        """
        if not path:
            raise ValueError("Empty path given.")

        # Extract the base name (file name with extension)
        filename = os.path.basename(path)

        if not filename:
            raise ValueError("Provided path does not contain a file name.")

        return filename

    @staticmethod
    def stripFileExtension(file: str) -> tuple[str]:
        """
        Returns the file name and its extension.
            Returns:
                > filename (str): file name with out extension
                > extension (str): from the file extension
            Args:
                > file (str): filename with extension
            Raises:
                > Error, not a file type path.
                > Error, empty file name given.
        """
        if not file:
            raise ValueError("Empty file name given.")

        # Split the file into name and extension
        filename, extension = os.path.splitext(file)

        if not filename:
            raise ValueError("Provided file name is invalid.")

        return filename, extension

    @staticmethod
    def isValidPathString(pathSegment: str) -> bool:
        """
        Validates if a string is safe and valid to be joined into a file path.
        Ensures compatibility with Linux, macOS, and Windows.

        Args:
            pathSegment (str): The string to validate.

        Returns:
            bool: True if valid, False otherwise.

        Raises:
            ValueError: If the pathSegment is not a valid string for a file path.
        """
        # Check if input is a string
        if not isinstance(pathSegment, str):
            raise ValueError("The provided path segment must be a string.")

        # Check if the string is empty or whitespace
        if not pathSegment.strip():
            raise ValueError("The path segment cannot be empty or only whitespace.")

        # Define invalid characters for file paths
        invalidChars = r'[<>:"/\\|?*\x00-\x1F]'  # Windows invalid characters
        if re.search(invalidChars, pathSegment):
            raise ValueError(
                f"The path segment contains invalid characters: {pathSegment}"
            )

        # Linux/macOS: Avoid '/' and NULL
        if "/" in pathSegment or "\x00" in pathSegment:
            raise ValueError(
                "The path segment contains invalid characters for Linux/macOS."
            )

        # Avoid reserved names (Windows, Linux, macOS devices)
        reservedNames = {
            "CON",
            "PRN",
            "AUX",
            "NUL",  # Windows reserved
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",  # Windows COM ports
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",  # Windows LPT ports
            ".",
            "..",  # Current and parent directory
            "tty",
            "null",
            "zero",
            "random",
            "urandom",  # Linux/macOS devices
        }
        baseName = os.path.basename(pathSegment).split(".")[0].lower()
        if baseName in reservedNames:
            raise ValueError(
                f"The path segment uses a reserved or problematic name: {pathSegment}"
            )

        # Check for excessive length (255 characters for most OS)
        if len(pathSegment) > 255:
            raise ValueError(
                "The path segment exceeds the maximum length of 255 characters."
            )

        return True

    pass
