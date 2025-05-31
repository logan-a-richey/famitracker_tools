#!/usr/bin/env python3
# color_logger.py

import logging
import sys
import os

class ColorFormatter(logging.Formatter):
    # base_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    base_format = "[%(levelname)s] - %(message)s (%(filename)s:%(lineno)d)"

    def __init__(self, colors=None):
        super().__init__(self.base_format)
        self.colors = colors or {}

    def format(self, record):
        color = self.colors.get(record.levelname, self.colors.get("RESET", ""))
        message = super().format(record)
        return f"{color}{message}{self.colors.get('RESET', '')}"

class ColorLogger:
    # ANSI color codes (class attribute)
    COLORS = {
        "VERBOSE"  : "\033[34m",        # Blue
        "DEBUG"    : "\033[32m",        # Green
        "INFO"     : "\033[37m",        # White
        "WARNING"  : "\033[33m",        # Yellow
        "ERROR"    : "\033[31;1m",      # Bold Red
        "CRITICAL" : "\033[31;1;47m",   # Bold Red text on White background
        "RESET"    : "\033[0m"
    }

    VERBOSE_LEVEL   = 5
    DEBUG           = 10       
    INFO            = 20
    WARNING         = 30
    ERROR           = 40
    CRITICAL        = 50

    def __init__(self, name="app_logger", log_file="/tmp/log.log"):
        self.name = name
        self.log_file = log_file
        self._patch_verbose_level()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.VERBOSE_LEVEL)

        if not getattr(self.logger, "_color_logger_initialized", False):
            self._setup_handlers()
            self.logger._color_logger_initialized = True

    @classmethod
    def _patch_verbose_level(cls):
        """Add VERBOSE level and method to logging.Logger if not already patched."""
        # add subtle verbose level
        if not hasattr(logging, 'VERBOSE'):
            logging.VERBOSE = cls.VERBOSE_LEVEL
            logging.addLevelName(cls.VERBOSE_LEVEL, "VERBOSE")
        
        if not hasattr(logging.Logger, "verbose"):
            def verbose(self, message, *args, **kwargs):
                if self.isEnabledFor(cls.VERBOSE_LEVEL):
                    self._log(cls.VERBOSE_LEVEL, message, args, stacklevel=2, **kwargs)
            logging.Logger.verbose = verbose
        

    
    def _setup_handlers(self):
        self.logger.propagate = False

        # Terminal handler with colors
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(self.VERBOSE_LEVEL)
        stream_handler.setFormatter(ColorFormatter(colors=self.COLORS))
        self.logger.addHandler(stream_handler)

        # File handler (plain format)
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(self.VERBOSE_LEVEL)
        file_handler.setFormatter(logging.Formatter(ColorFormatter.base_format))
        self.logger.addHandler(file_handler)

    def get(self):
        return self.logger


if __name__ == "__main__":
    logger = ColorLogger("MainApp").get()
    logger.setLevel(ColorLogger.VERBOSE_LEVEL)

    logger.verbose("This is a VERBOSE message")
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.critical("This is a CRITICAL message")

