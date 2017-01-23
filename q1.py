#!/usr/bin/env python3

from sys import stdin

def parsechems(s, sep=None):
    return set(map(int, s.split(sep)))

def parsereaction(s):
    return tuple(map(lambda t: parsechems(t, '+'), s.split('->')))

chems = parsechems(stdin.readline().strip())
reactions = {}
for line in stdin:
    subs, prods = parsereaction(line)
    node = reactions
    for chem in subs:
        node = node.setdefault(chem, dict())
    node.setdefault(None, set()).update(prods)

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
