import os
import logging
from logging import Logger
from typing import Optional


class LoggerFactory:
    """
    Factory class for creating and configuring loggers.
    """

    def __init__(self, log_dir: str, log_format: Optional[str] = None, enable_console: bool = True):
        """
        Initialize the LoggerFactory with configuration.

        Args:
            log_dir (str): Directory where log files will be saved.
            log_format (str, optional): Format for log messages. Defaults to a standard format.
            enable_console (bool): Whether to enable console logging.
        """
        self.log_dir = log_dir
        self.log_format = log_format or '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.enable_console = enable_console

    def ensure_log_directory_exists(self) -> None:
        """
        Ensure that the log directory exists. Create it if necessary.
        """
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir, exist_ok=True)
            except OSError as e:
                raise RuntimeError(f"Failed to create log directory '{self.log_dir}': {e}")

    def create_file_handler(self, log_file: str, formatter: logging.Formatter) -> logging.FileHandler:
        """
        Create a file handler for logging.

        Args:
            log_file (str): Path to the log file.
            formatter (logging.Formatter): Formatter for log messages.

        Returns:
            logging.FileHandler: Configured file handler.
        """
        try:
            file_handler = logging.FileHandler(log_file, mode='a')  # Append mode
            file_handler.setFormatter(formatter)
            return file_handler
        except Exception as e:
            raise RuntimeError(f"Failed to create file handler for log file '{log_file}': {e}")

    def create_console_handler(self, formatter: logging.Formatter) -> logging.StreamHandler:
        """
        Create a console handler for logging.

        Args:
            formatter (logging.Formatter): Formatter for log messages.

        Returns:
            logging.StreamHandler: Configured console handler.
        """
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        return console_handler

    def get_logger(self, name: str, log_file_name: str, level: int = logging.INFO) -> Logger:
        """
        Configure and return a logger with a file handler and optional console handler.

        Args:
            name (str): Name of the logger.
            log_file_name (str): Name of the log file.
            level (int): Logging level.

        Returns:
            logging.Logger: Configured logger instance.
        """
        # Ensure the log directory exists
        self.ensure_log_directory_exists()

        # Create full path for log file
        log_file = os.path.join(self.log_dir, log_file_name)

        # Create logger
        logger = logging.getLogger(name)

        # Prevent duplicate handlers
        if not logger.hasHandlers():
            # Set log level
            logger.setLevel(level)

            # Create formatter
            formatter = logging.Formatter(self.log_format)

            # Add file handler
            file_handler = self.create_file_handler(log_file, formatter)
            logger.addHandler(file_handler)

            # Add console handler (if enabled)
            if self.enable_console:
                console_handler = self.create_console_handler(formatter)
                logger.addHandler(console_handler)

        return logger
