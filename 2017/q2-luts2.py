#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

class RNA:
    _comp = {'A': 'U',
             'C': 'G',
             'G': 'C',
             'U': 'A'}

    def _makecount(s, c):
        ans = [0] * len(s)
        if s[0] == c:
            ans[0] += 1
        for i in range(1, len(s)):
            ans[i] = ans[i - 1]
            if s[i] == c:
                ans[i] += 1
        return ans

    def _makepos(s, c):
        ans = [-1] * (len(s) + 1)
        for i in range(len(s) - 2, -1, -1):
            ans[i] = (i + 1) if s[i + 1] == c else ans[i + 1]
        ans[-1] = 0 if s[0] == c else ans[0]
        return ans


    def __init__(self, s):
        self._s = s.upper()
        self._x = bytearray(' ' * len(self._s), 'ascii')
        debug('_s %s', self._s)
        self._count = {c: RNA._makecount(self._s, c) for c in 'ACGU'}
        self._pos = {c: RNA._makepos(self._s, c) for c in 'ACGU'}
        for c in 'ACGU':
            debug('positions %s %s', c, list(self.positions(c)))


    def __len__(self):
        return len(self._s)

    def __str__(self):
        return self._s


    def count(self, c, start=0, end=None):
        if not end:
            end = len(self._s)
        tab = self._count[c]
        ans = tab[end - 1]
        if start > 0:
            ans -= tab[start - 1]
        return ans

    def counts(self, start=0, end=None):
        return (self.count('A', start, end),
                self.count('C', start, end),
                self.count('G', start, end),
                self.count('U', start, end))

    def positions(self, c, start=0, end=None):
        if not end:
            end = len(self._s)
        tab = self._pos[c]
        pos = tab[start - 1]
        while pos != -1 and pos < end:
            yield pos
            pos = tab[pos]


    def balanced(self, start=0, end=None):
        if not end:
            end = len(self._s)
        if (end - start) % 2 == 0:
            return (self._balanced2(start, end), None)
        else:
            return self._balanced3(start, end)

    def _balanced2(self, start, end):
        assert (end - start) % 2 == 0
        a, c, g, u = self.counts(start, end)
        debug('_balanced2: "%s" %d %d %d %d', self._s[start:end], a, c, g, u)
        return a == u and c == g

    def _balanced3(self, start, end):
        assert (end - start) % 2 != 0
        a, c, g, u = self.counts(start, end)
        debug('_balanced3: "%s" %d %d %d %d', self._s[start:end], a, c, g, u)
        if a == u:
            if c - g == 1:
                return (True, 'C')
            elif g - c == 1:
                return (True, 'G')
        elif c == g:
            if a - u == 1:
                return (True, 'A')
            elif u - a == 1:
                return (True, 'U')
        return (False, None)


    def perfect(self, start=0, end=None):
        if not end:
            end = len(self._s)
        if (end - start) % 2 == 0:
            return (self._perfect2(start, end), None)
        else:
            return self._perfect3(start, end)

    def _perfect2(self, start, end):
        assert (end - start) % 2 == 0
        debug('_perfect2: "%s" %d %d', self._s[start:end], start, end)
        if (end - start) == 0:
            debug('_perfect2: True')
            return True
        if not self._balanced2(start, end):
            debug('_perfect2: False')
            return False
        for i in self.positions(RNA._comp[self._s[start]], start + 1, end):
            debug('_perfect2: i %d', i)
            nleft = i - (start + 1)
            nright = end - (i + 1)
            if nleft % 2 == 0 and nright % 2 == 0:
                if self._perfect2(start + 1, i) and self._perfect2(i + 1, end):
                    self._x[start] = ord(b'(')
                    self._x[i] = ord(b')')
                    debug('_perfect2: bond %d %d "%s"', start, i, self._s)
                    debug('_perfect2: bond %d %d "%s"', start, i, self._x.decode())
                    return True
        debug('_perfect2: False')
        return False

    def _perfect3(self, start, end):
        assert (end - start) % 2 != 0
        debug('_perfect3: "%s" %d %d', self._s[start:end], start, end)
        almost, nt = self._balanced3(start, end)
        if not almost:
            debug('_perfect3: False')
            return (False, None)
        for i in self.positions(nt, start, end):
            debug('_perfect3: i %d', i)
            nleft = i - start
            nright = end - (i + 1)
            if nleft % 2 == 0 and nright % 2 == 0:
                # XXX: parts may be unbalaned by their own, but balanced together
                if self._perfect2(start, i) and self._perfect2(i + 1, end):
                    debug('_perfect3: True')
                    return (True, i)
        debug('_perfect3: False')
        return (False, None)

#-------------------------------------------------------------------------

perfect, pos = RNA(stdin.readline().strip()).perfect()
if perfect:
    if not pos:
        print('perfect')
    else:
        print('almost perfect')
else:
    print('imperfect')
