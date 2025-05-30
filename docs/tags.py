#!/usr/bin/env python3

import sys

infile = sys.argv[1]
with open(infile, 'r') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        if line[0] == '#':
            continue
        first_word = line.split()[0]
        if first_word[0].isupper():
            print(first_word)

