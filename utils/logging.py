import argparse
import logging
import sys

# ANSI escape sequences for colors
COLORS = {
    'DEBUG': "\033[34m",    # Blue
    'INFO': "\033[32m",     # Green
    'WARNING': "\033[33m",  # Yellow
    'ERROR': "\033[31m",    # Red
    'CRITICAL': "\033[1;31m"  # Bold Red
}
RESET = "\033[0m"

class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter to add colors to log level names.
    """
    def format(self, record):
        # Use the original level name
        levelname = record.levelname
        if levelname in COLORS:
            record.levelname = f"{COLORS[levelname]}{levelname}{RESET}"
        return super().format(record)

def setup_logging(log_level):
    """
    Set up logging with a colored formatter.
    
    Args:
        log_level (str): The logging level as a string (e.g., 'DEBUG', 'INFO')
    
    Returns:
        logging.Logger: The root logger configured with the colored formatter.
    """
    # Create stream handler for standard output
    handler = logging.StreamHandler(sys.stdout)
    formatter = ColoredFormatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    # Get the root logger and configure it
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Remove any default handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False

    return logger

def get_logger(name=None):
    """
    Get a logger with the specified name.
    
    Args:
        name (str, optional): Logger name, typically __name__ from the calling module.
                              If None, returns the root logger.
    
    Returns:
        logging.Logger: A logger instance.
    """
    return logging.getLogger(name)

# Parse command-line arguments for log level
parser = argparse.ArgumentParser(description="Colored Logging Example")
parser.add_argument("--log-level", default="INFO",
                    help="Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
args = parser.parse_args()

# Initialize logging with the chosen level
logger = setup_logging(args.log_level)

if __name__ == "__main__":

    app_logger = get_logger(__name__)

    # Log messages at various levels to demonstrate the colored output
    app_logger.debug("This is a debug message.")
    app_logger.info("This is an info message.")
    app_logger.warning("This is a warning message.")
    app_logger.error("This is an error message.")
    app_logger.critical("This is a critical message.")
