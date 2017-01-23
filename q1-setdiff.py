#!/usr/bin/env python3

from itertools import filterfalse
from sys import stdin

def parsechems(s, sep=None):
    return set(map(int, s.split(sep)))

def parsereaction(s):
    return tuple(map(lambda t: parsechems(t, '+'), s.split('->')))

chems = parsechems(stdin.readline().strip())
reactions = [parsereaction(line) for line in stdin]

def updatereaction(reaction):
    reaction[0].difference_update(chems)
    if not reaction[0]:
        chems.update(reaction[1])
        return True
    else:
        return False

while True:
    nchems = len(chems)
    reactions[:] = filterfalse(updatereaction, reactions)
    if len(chems) == nchems:
        break

print(' '.join(map(str, chems)))
