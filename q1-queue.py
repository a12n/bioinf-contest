#!/usr/bin/env python3

from itertools import filterfalse
from sys import stdin

def parsechems(s, sep=None):
    return set(map(int, s.split(sep)))

def parsereaction(s):
    return tuple(map(lambda t: parsechems(t, '+'), s.split('->')))

chems = parsechems(stdin.readline().strip())
reactions = [parsereaction(line) for line in stdin]
state = list(chems)

def reactiondone(reaction):
    done = not reaction[0]
    if done:
        state.extend(reaction[1].difference(chems))
        chems.update(reaction[1])
    return done

while state:
    chem = state.pop(0)
    for subs, prods in reactions:
        subs.discard(chem)
    reactions[:] = filterfalse(reactiondone, reactions)

print(' '.join(map(str, chems)))
