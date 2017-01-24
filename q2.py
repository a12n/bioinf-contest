#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)


# def cat(n):
#     if n == 0:
#         return 1
#     c = [0] * (n + 1)
#     c[0] = 1
#     c[1] = 1
#     for i in range(2, n + 1):
#         for k in range(1, i + 1):
#             c[i] =  c[i] + c[k - 1] * c[i - k]
#     return c[n]

comp = {'A': 'U', 'C': 'G', 'G': 'C', 'U': 'A'}
# comp = {ord(b'A'): ord(b'U'),
#         ord(b'C'): ord(b'G'),
#         ord(b'G'): ord(b'C'),
#         ord(b'U'): ord(b'A')}

def findall(s, sub, start=0):
    while True:
        start = s.find(sub, start)
        if start != -1:
            yield start
            start += len(sub)
        else:
            break

s = stdin.readline().strip().upper()
# s = bytearray(stdin.readline().strip().upper(), 'ascii')
debug('s = "%s"', s)

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

# bonds = dict()
# singles = set()
#
# def isperfect(s, start, end, level=0):
#     n = end - start
#     debug('%ss = "%s", start = %d, end = %d, n = %s',
#           ' ' * level, s[start:end], start, end, n)
#     if n == 0:
#         return True
#     if n == 1:
#         singles.add(start)
#         return True
#     if n == 2:
#         if s[start] == comp[s[start + 1]]:
#             bonds[start] = start + 1
#             debug('bond (%d, %d)', start, start + 1)
#             return True
#         else:
#             return False
#     for i in range(start + 1, end): # +2
#         if s[i] == comp[s[start]]:
#             if isperfect(s, start + 1, i, level + 1) and isperfect(s, i + 1, end, level + 1):
#                 bonds[start] = i
#                 debug('bond (%d, %d)', start, i)
#                 return True
#     return False

# ok = isperfect(s, 0, len(s))
# debug('bonds = %s', bonds)
# debug('singles = %s', singles)
# if ok:
#     if len(s) % 2 == 0:
#         if len(singles) == 0:
#             print('perfect')
#         else:
#             print('imperfect')
#     else:
#         if len(singles) > 0:
#             print('almost perfect')
#         else:
#             print('imperfect')
# else:
#     print('imperfect')

#-----------------------------------------------------------------------------

# def counts(s, start=0, end=None):
#     if isinstance(s, bytearray):
#         return (s.count(b'A', start, end),
#                 s.count(b'C', start, end),
#                 s.count(b'G', start, end),
#                 s.count(b'U', start, end))
#     else:
#         return (s.count('A', start, end),
#                 s.count('C', start, end),
#                 s.count('G', start, end),
#                 s.count('U', start, end))
#
# def maybeperfect(s, start=0, end=None):
#     a, c, g, u = counts(s, start, end)
#     debug('maybeperfect: "%s" %d %d %d %d', s[start:end], a, c, g, u)
#     return a == u and c == g
#
# def isperfect2(s, start, end):
#     if (end - start) == 0:
#         return True
#     if not maybeperfect(s, start, end):
#         return False
#     for i in range(start + 1, end):
#         if s[i] == comp[s[start]]:
#             if isperfect2(s, start + 1, i) and isperfect2(s, i + 1, end):
#                 debug('bond (%d, %d)', start, i)
#                 return True
#     return False
#
# tryremove = None
#
# if len(s) % 2 == 0:
#     if isperfect2(s, 0, len(s)):
#         print('perfect')
#     else:
#         print('imperfect')
# else:
#     a, c, g, u = counts(s)
#     debug('%d %d %d %d', a, c, g, u)
#     if a == u:
#         if c - g == 1:
#             # Try remove C
#             tryremove = b'C'
#         elif g - c == 1:
#             # Try remove G
#             tryremove = b'G'
#         else:
#             print('imperfect')
#     elif c == g:
#         if a - u == 1:
#             # Try remove A
#             tryremove = b'A'
#         elif u - a == 1:
#             # Try remove U
#             tryremove = b'U'
#         else:
#             print('imperfect')
#     else:
#         print('imperfect')
#
#
# if tryremove:
#     found = False
#     debug('tryremove %s', tryremove)
#     for pos in findall(s, tryremove):
#         debug('pos = %s', pos)
#         s[pos], s[0] = s[0], s[pos]
#         if isperfect2(s, 1, len(s)):
#             found = True
#             break
#         s[pos], s[0] = s[0], s[pos]
#     if found:
#         print('almost perfect')
#     else:
#         print('imperfect')

#-----------------------------------------------------------------------------

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
