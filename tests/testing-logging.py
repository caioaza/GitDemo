import logging

logging.basicConfig(level=logging.DEBUG, filename="logfile2.log",
                    format="%(asctime)s : %(levelname)s : %(name)s : %(message)s")

logger = logging.getLogger("TestLogger")

logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")