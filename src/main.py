#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True # stop __pyache__

from data.project import Project
from reader.reader import Reader

from core.color_logger import ColorLogger
logger = ColorLogger("Main").get()
logger.setLevel(ColorLogger.INFO)

# main program
def main():
    try:
        infile = sys.argv[1]
    except Exception as e:
        logger.error("Could not open file. Usage: ./main <input.txt>")
        sys.exit(1)

    proj = Project()
    reader = Reader()
    reader.read_file(infile, proj)
    
    # print(proj)
    logger.info("Program ran successfully.")

if __name__ == "__main__":
    main()

