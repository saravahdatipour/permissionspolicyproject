import logging
logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)

# create a new file handler to write log messages to a file
file_handler = logging.FileHandler("my_log_file.txt")

# set the logging level for the file handler
file_handler.setLevel(logging.INFO)

# create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# set the formatter for the file handler
file_handler.setFormatter(formatter)

# add the file handler to the logger
logger.addHandler(file_handler)

# use the logger to write log messages
logger.info("This is an informational message.")
logger.warning("This is a warning message.")