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
reactions = dict()
for line in stdin:
    subs, prods = parsereaction(line)
    node = reactions
    for chem in subs:
        node = node.setdefault(chem, dict())
    node.setdefault(None, set()).update(prods)
debug('reactions = %s', reactions)

def react(chems, node):
    for sub, prodsornode in node.items():
        if sub == None:
            chems.update(prodsornode)
        elif sub in chems:
            react(chems, prodsornode)

while True:
    nchems = len(chems)
    react(chems, reactions)
    if len(chems) == nchems:
        break

print(' '.join(map(str, chems)))
