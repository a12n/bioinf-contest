#!/usr/bin/env python3

import sys

def parsechems(s, sep=None):
    return set(map(int, s.split(sep)))

def parsereact(s):
    return tuple([parsechems(t, '+') for t in s.split('->')])

chems = parsechems(sys.stdin.readline())
reacts = []

for line in sys.stdin:
    reacts.append(parsereact(line))

while True:
    n = len(chems)
    prods = set()
    for rsubs, rprods in reacts:
        if rsubs.issubset(chems):
            prods.update(rprods)
    chems.update(prods)
    if len(chems) == n:
        break

print(' '.join(map(str, chems)))
