#!/usr/bin/env python3

import sys
# stop __pyache__ from being created
sys.dont_write_bytecode = True 

from data.project import Project
from reader.reader import Reader

# main program
def main():
    infile = sys.argv[1]
    proj = Project()
    reader = Reader()
    reader.read_file(infile, proj)
    
    print(proj)

if __name__ == "__main__":
    main()

