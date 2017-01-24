#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)


def cat(n):
    if n == 0:
        return 1
    c = [0] * (n + 1)
    c[0] = 1
    c[1] = 1
    for i in range(2, n + 1):
        for k in range(1, i + 1):
            c[i] =  c[i] + c[k - 1] * c[i - k]
    return c[n]

comp = {'A': 'U', 'C': 'G', 'G': 'C', 'U': 'A'}

def findall(s, sub, start=0):
    while True:
        start = s.find(sub, start)
        if start != -1:
            yield start
            start += len(sub)
        else:
            break

def maybeperfect(s, start, end):
    a = s.count('A', start, end)
    c = s.count('C', start, end)
    g = s.count('G', start, end)
    u = s.count('U', start, end)
    debug('maybeperfect: "%s" %d %d %d %d', s[start:end], a, c, g, u)
    return a == u and c == g

s = stdin.readline().strip().upper()
# t = {nt: list(findall(s, nt)) for nt in 'ACGU'}
# debug('t = %s', t)

# def isperfect(s, start, end):
#     debug('s = %s', s[start:end])
#     if (end - start) < 3:
#         return True
#     if not maybeperfect(s, start, end):
#         return False
#     # Try to find bonding nucleotide for the first nucleotide.
#     pos = []
#     for i in range(start + 2, end):
#         debug('i = %s', i)
#         if s[i] == comp[s[start]] and maybeperfect(s, start + 2, i):
#             pos.append(i)
#     debug('pos = %s', pos)
#     for i in pos:
#         if isperfect(s, start + 1, i) and isperfect(s, i + 1, end):
#             return True
#     return False

bonds = dict()
singles = set()

def isperfect(s, start, end, level=0):
    n = end - start
    debug('%ss = "%s", start = %d, end = %d, n = %s',
          ' ' * level, s[start:end], start, end, n)
    if n == 0:
        return True
    if n == 1:
        singles.add(start)
        return True
    if n == 2:
        if s[start] == comp[s[start + 1]]:
            bonds[start] = start + 1
            debug('bond (%d, %d)', start, start + 1)
            return True
        else:
            return False
    if not maybeperfect(s, start, end):
        return False
    for i in range(start + 1, end): # +2
        if s[i] == comp[s[start]]:
            if isperfect(s, start + 1, i, level + 1) and isperfect(s, i + 1, end, level + 1):
                bonds[start] = i
                debug('bond (%d, %d)', start, i)
                return True
    return False

ok = isperfect(s, 0, len(s))
debug('bonds = %s', bonds)
debug('singles = %s', singles)
if ok:
    if len(s) % 2 == 0:
        if len(singles) == 0:
            print('perfect')
        else:
            print('imperfect')
    else:
        if len(singles) > 0:
            print('almost perfect')
        else:
            print('imperfect')
else:
    print('imperfect')

# s = stdin.readline().strip()
# debug(s)
#
# basepair = dict()
# for i in range(len(s) - 2):
#     e = set(findall(s, comp(s[i]), i + 2))
#     if e:
#         basepair[i] = e
# debug(basepair)

# TODO
