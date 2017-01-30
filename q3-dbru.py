#!/usr/bin/env python3

import functools
import itertools
import logging
from logging import debug
from sys import argv, stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def kmers(s, k):
    for i in range(len(s) - k + 1):
        yield s[i:(i + k)]

def left(s, k):
    return s[0:k]

def right(s, k):
    return s[-k:]

def printans(reads, t):
    print(t)
    for read in reads:
        p = t.find(read)
        print((p + 1) if p != -1 else -1)

s = stdin.readline().strip().upper()
reads = tuple([stdin.readline().strip().upper() for i in range(int(stdin.readline()))])
debug('num reads %s', len(reads))
debug('min read len %s', min(map(len, reads)))
debug('max read len %s', max(map(len, reads)))
debug('avg read len %s', float(sum(map(len, reads))) / len(reads))
# debug('reads %s', reads)

k = int(argv[1]) if len(argv) > 1 else None
debug('k %s', k)

# Build graph

class DeBruijnGraph:
    def __init__(self, reads, k=None):
        if not k:
            k = min(map(len, reads)) - 1
            if k % 2 == 0:
                k -= 1
            k = max(k, 2)
        self._incoming = dict()
        self._outgoing = dict()
        self._indeg = dict()
        self._outdeg = dict()
        debug('Building graph for %d reads, k %d', len(reads), k)
        for read in reads:
            for kmer in kmers(read, k):
                l = left(kmer, k - 1)
                r = right(kmer, k - 1)
                froml = self._outgoing.setdefault(l, dict())
                tor = self._incoming.setdefault(r, dict())
                froml[r] = froml.setdefault(r, 0) + 1
                tor[l] = tor.setdefault(l, 0) + 1
                self._outdeg[l] = self._outdeg.setdefault(l, 0) + 1
                self._indeg[r] = self._indeg.setdefault(r, 0) + 1
        self._compress()

    def _compress(self):
        debug('Compressing graph, %d nodes', self.order())
        # TODO
        pass

    def order(self):
        return len(self._outgoing)

    def nodes(self):
        return self._outgoing.keys()

    def edges(self):
        for v, ws in self._outgoing.items():
            for w, n in ws.items():
                for i in range(n):
                    yield (v, w)

    def indeg(self, v):
        return self._indeg.get(v, 0)

    def outdeg(self, v):
        return self._outdeg.get(v, 0)

    def printdot(self):
        print('digraph {')
        for v, ws in self._outgoing.items():
            for w, n in ws.items():
                print(v, '->', w, '[label=' + v + w[-1] + ']', ';')
                for _ in range(1, n):
                    print(v, '->', w, ';')
        print('}')

g = DeBruijnGraph(reads, k)

debug('nodes:')
for v in g.nodes():
    debug('%d -> %s -> %d', g.indeg(v), v, g.outdeg(v))

g.printdot()

# debug('edges:')
# for e in g.edges():
#     debug('%s -> [%s] -> %s', e[0], e[0] + e[1][1:], e[1])

# TODO

# for aag in list(outgoinf.keys()):
#     if len(outgoing[aag]) == 1:
#         aga = outgoing[aag].pop()
#         gac = outgoing[aga]
#         aaga = k + k2[0]
#         outgoing[aaga] = gac
#         for
#         del(outgoing[aag])
#         del(outgoing[aga])
#
# debug('dbru %s', dbru)
# print('digraph {')
# for k, v in dbru.items():
#     for vv in v:
#         print(k, '->', vv, ';')
# print('}')
