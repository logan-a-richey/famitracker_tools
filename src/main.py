#!/usr/bin/env python3

import sys
from .dataclasses.project import Project
from .reader.reader import Reader

# stop __pyache__ from being created
sys.dont_write_bytecode = True 

# main program
def main():
    infile = sys.argv[1]
    proj = Project()
    reader = Reader()
    reader.read_file(infile, proj)
    proj.print_self()

if __name__ == "__main__":
    main()

