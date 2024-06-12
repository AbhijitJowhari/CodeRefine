import logging
from yachalk import chalk
import os
import logging


class GraphLogger:

    def __init__(self, name="Graph Logger", color="white"):
        "Set the log level (optional, can be DEBUG, INFO, WARNING, ERROR, CRITICAL)"

        log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
        logging.basicConfig(level=log_level)

        ## Formatter
        self.time_format = "%Y-%m-%d %H:%M:%S"
        format = self.format(color)
        self.formatter = logging.Formatter(
            fmt=format,
            datefmt=self.time_format,
        )

        ## Handler
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter)

        ## Logger
        self.logger = logging.getLogger(name)
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def getLogger(self):
        return self.logger

    def format(self, color: str):
        
        if(color == "black"):
            format = chalk.black(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "red"):
            format = chalk.red(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "green"):
        
        
            format = chalk.green(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "yellow"):
            format = chalk.yellow(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "blue"):
            format = chalk.blue(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "magenta"):
            format = chalk.magenta(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "cyan"):
            format = chalk.cyan(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "white"):
            format = chalk.white(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "black_bright"):
            format = chalk.black_bright(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "red_bright"):
            format = chalk.red_bright(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "green_bright"):
            format = chalk.green_bright(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color ==  "yellow_bright"):
            format = chalk.yellow_bright(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "blue_bright"):
            format = chalk.blue_bright(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color ==  "magenta_bright"):
            format = chalk.magenta_bright(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "cyan_bright"):
            format = chalk.cyan_bright(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color == "white_bright"):
            format = chalk.white_bright(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )
        elif(color ==  "grey"):
            format = chalk.grey(
                "\n▶︎ %(name)s - %(asctime)s - %(levelname)s \n%(message)s\n"
            )

        return format
