#!/usr/bin/env python3

import logging
import sys

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def parsechems(s, sep=None):
    return set(map(str.strip, s.split(sep)))

def parsereaction(s):
    return tuple(map(lambda t: parsechems(t, '+'), s.split('<=>')))

def printreq(descrs):
    print('?')
    for c, p in descrs:
        print(' '.join(c))
        print(' '.join(p))

def printans(cats):
    print('+')
    for p in cats:
        print(' '.join(p) if p else '-')

with open(sys.argv[1], 'r') as f:
    reactions = list(map(parsereaction, f))

with open(sys.argv[2], 'r') as f:
    proteins = parsechems(next(f))

logging.debug('%d reactions %s', len(reactions), reactions)
logging.debug('%d proteins %s', len(proteins), proteins)

catalyze = [set()] * len(reactions)

# TODO

printans(catalyze)
