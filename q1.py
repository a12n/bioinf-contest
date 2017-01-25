#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def parsechems(s, sep=None):
    return set(map(int, s.split(sep)))

def parsereaction(s):
    return tuple(map(lambda t: parsechems(t, '+'), s.split('->')))

chems = parsechems(stdin.readline().strip())
reactions = []
requires = dict()
for line in stdin:
    subs, prods = parsereaction(line.strip())
    i = len(reactions)
    reactions.append((subs, prods))
    for sub in subs:
        requires.setdefault(sub, set()).add(i)

newchems = chems.copy()
while newchems:
    chem = newchems.pop()
    if not chem in requires:
        continue
    for i in list(requires[chem]):
        reaction = reactions[i]
        reaction[0].discard(chem)
        if not reaction[0]:
            chems.update(reaction[1])
            newchems.update(reaction[1])
            requires[chem].discard(i)

print(' '.join(map(str, sorted(chems))))
