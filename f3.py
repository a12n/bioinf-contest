#!/usr/bin/env python3

import sys
import logging

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def readchromosome(f):
    n = int(f.readline())
    def readmatrix():
        return [list(map(int, f.readline().split())) for _ in range(n)]
    h00 = readmatrix()
    f.readline()
    h01 = readmatrix()
    f.readline()
    h10 = readmatrix()
    f.readline()
    h11 = readmatrix()
    return (h00, h01, h10, h11)

def genesorder(ch):
    n = len(ch[0b00])
    logging.debug('n %d', n)
    # TODO
    return list(range(n))

for _ in range(int(sys.stdin.readline())):
    order = genesorder(readchromosome(sys.stdin))
    print(' '.join(map(str, order)))
