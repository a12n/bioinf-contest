#!/usr/bin/env python3

from itertools import filterfalse
from sys import stdin

def parsechems(s, sep=None):
    return set(map(int, s.split(sep)))

def parsereaction(s):
    return tuple(map(lambda t: parsechems(t, '+'), s.split('->')))

chems = parsechems(stdin.readline().strip())
reactions = [parsereaction(line) for line in stdin]

def react(reaction):
    chemsok = chems.issuperset(reaction[0])
    if chemsok:
        chems.update(reaction[1])
    return chemsok

while True:
    nchems = len(chems)
    reactions[:] = filterfalse(react, reactions)
    if len(chems) == nchems:
        break

print(' '.join(map(str, chems)))
