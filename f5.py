#!/usr/bin/env python3

import logging
import sys

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

NUM_DESCRS = 96

def parsechems(s, sep=None):
    return set(map(str.strip, s.split(sep)))

def parsereaction(s):
    return tuple(map(lambda t: parsechems(t, '+'), s.split('<=>')))

def printreq(descrs):
    print('?')
    for c, p in descrs:
        print(' '.join(c))
        print(' '.join(p))

def readresp(n):
    return [parsechems(sys.stdin.readline()) for _ in range(n)]

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

def experiment():
    try:
        i = next((i for i in range(len(reactions)) if not catalyze[i]))
    except StopIteration:
        # All reactions have known catalyzers
        return None
    logging.debug('i %d, reactions[i] %s', i, reactions[i])
    # TODO
    return None

while True:
    try:
        descrs = experiment()
        if not descrs:
            # No more experiments
            break
    except KeyboardInterrupt:
        break

printans(catalyze)
