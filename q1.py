#!/usr/bin/env python3

from sys import stdin

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
        subs, prods = reactions[i]
        subs.discard(chem)
        if not subs:
            chems.update(prods)
            newchems.update(prods)
            requires[chem].discard(i)

print(' '.join(map(str, sorted(chems))))
