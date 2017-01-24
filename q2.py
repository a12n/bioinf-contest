#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)


comp = {'A': 'U', 'C': 'G', 'G': 'C', 'U': 'A'}

def findall(s, sub, start=0):
    while True:
        start = s.find(sub, start)
        if start != -1:
            yield start
            start += len(sub)
        else:
            break

s = stdin.readline().strip().upper()
debug('s = "%s"', s)

NO_SKIP = 0xFFFFFF

def counts(s, start, end, skip=NO_SKIP):
    hasskip = (skip >= start and skip < end)
    return (
        s.count('A', start, end) - int(hasskip and s[skip] == 'A'),
        s.count('C', start, end) - int(hasskip and s[skip] == 'C'),
        s.count('G', start, end) - int(hasskip and s[skip] == 'G'),
        s.count('U', start, end) - int(hasskip and s[skip] == 'U')
    )

def maybeperfect(s, start, end, skip=NO_SKIP):
    a, c, g, u = counts(s, start, end, skip)
    debug('maybeperfect: "%s" %s %d %d %d %d', s[start:end], skip, a, c, g, u)
    return a == u and c == g

cache = dict()

def isperfect2(s, start, end, skip=NO_SKIP):
    hasskip = (skip >= start and skip < end)
    n = end - start - int(hasskip)
    if n == 0:
        return True
    if not maybeperfect(s, start, end, skip):
        return False
    for i in range(start + 1, end):
        if i == skip:
            continue
        if s[i] == comp[s[start]]:
            if isperfect2(s, start + 1, i, skip) and isperfect2(s, i + 1, end, skip):
                debug('bond (%d, %d)', start, i)
                return True
    return False

tryremove = None

if len(s) % 2 == 0:
    if isperfect2(s, 0, len(s)):
        print('perfect')
    else:
        print('imperfect')
else:
    a, c, g, u = counts(s, 0, len(s))
    debug('%d %d %d %d', a, c, g, u)
    if a == u:
        if c - g == 1:
            # Try remove C
            tryremove = 'C'
        elif g - c == 1:
            # Try remove G
            tryremove = 'G'
        else:
            print('imperfect')
    elif c == g:
        if a - u == 1:
            # Try remove A
            tryremove = 'A'
        elif u - a == 1:
            # Try remove U
            tryremove = 'U'
        else:
            print('imperfect')
    else:
        print('imperfect')


if tryremove:
    found = False
    debug('tryremove %s', tryremove)
    for pos in findall(s, tryremove):
        debug('pos = %s', pos)
        if isperfect2(s, 0, len(s), pos):
            found = True
            break
    if found:
        print('almost perfect')
    else:
        print('imperfect')

# TODO: bytearray
# TODO: isperfect2 cache
