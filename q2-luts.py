#!/usr/bin/env python3

import logging
from enum import Enum
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

# Bsearch

class Bsearch(Enum):
    ALL_BIGGER = 1
    ALL_LOWER = 2
    AT = 3
    EMPTY = 4
    JUST_AFTER = 5

# TODO: combine with Bsearch class
def bsearch(s, x, start=0, end=None):
    if not end:
        end = len(s)
    n = end - start
    if n <= 0:
        return (Bsearch.EMPTY, None)
    elif s[start] > x:
        return (Bsearch.ALL_BIGGER, None)
    elif s[end - 1] < x:
        return (Bsearch.ALL_LOWER, None)
    i, j = start, end - 1
    while True:
        if i > j:
            return (Bsearch.JUST_AFTER, i)
        else:
            m = i + (j - i) // 2
            if x < s[m]:
                j = m - 1
            elif x > s[m]:
                i = m + 1
            else:
                return (Bsearch.AT, m)

# RNA str utils

def findall(s, sub, start=0):
    while True:
        start = s.find(sub, start)
        if start != -1:
            yield start
            start += len(sub)
        else:
            break

comp = {'A': 'U', 'C': 'G', 'G': 'C', 'U': 'A'}

# Count table

class RNACount:
    def makecounttab(s, c):
        ans = [0] * len(s)
        ans[0] = int(s[0] == c)
        for i in range(1, len(s)):
            ans[i] = int(s[i] == c) + ans[i - 1]
        return tuple(ans)

    def __init__(self, s):
        self.counttab = {c: RNACount.makecounttab(s, c) for c in 'ACGU'}

    def __str__(self):
        return str(self.counttab)

    def count(self, c, start=0, end=None):
        tab = self.counttab[c]
        if not end:
            end = len(tab)
        ans = tab[end - 1]
        if start > 0:
            ans -= tab[start - 1]
        # debug('count(%s, start=%s, end=%s) = %s', c, start, end, ans)
        return ans

    def balanced(self, start=0, end=None):
        return (self.count('A', start, end) == self.count('U', start, end) and
                self.count('C', start, end) == self.count('G', start, end))

# Pos table

class RNAPos:
    def __init__(self, s):
        self.end = len(s)
        self.postable = {c: tuple(findall(s, c)) for c in 'ACGU'}

    def __str__(self):
        return str(self.postable)

    def pos2(self, c, start=0, end=None):
        if not end:
            end = self.end
        tab = self.postable[c]
        ret, nextpos = bsearch(tab, start)
        if ret == Bsearch.EMPTY or ret == Bsearch.ALL_LOWER:
            return
        elif ret == Bsearch.ALL_BIGGER:
            nextpos = 0
        for pos in tab[nextpos:]:
            if pos >= end:
                break
            yield pos

    def pos(self, c, start=0, end=None):
        if not end:
            end = self.end
        tab = self.postable[c]
        # debug('c %s', c)
        for pos in tab:
            if pos < start:
                continue
            elif pos >= end:
                break
            else:
                # debug('yield %s', pos)
                yield pos

#-------------------------------------------------------------------------

s = stdin.readline().strip().upper()
# debug('s %s', s)

count = RNACount(s)
# debug('count %s', count)

pos = RNAPos(s)
# debug('pos %s', pos)

def perfect(start=0, end=None):
    if not end:
        end = len(s)
    if (end - start) == 0:
        return True
    if not count.balanced(start, end):
        # debug('not balanced in %s to %s', start, end)
        return False
    for i in pos.pos(comp[s[start]], start + 1, end):
        if perfect(start + 1, i) and perfect(i + 1, end):
            # debug('bond (%d, %d)', start, i)
            return True
    return False

if len(s) % 2 == 0:
    print('perfect' if perfect() else 'imperfect')
else:
    print('TODO')
