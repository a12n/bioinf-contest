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

s = stdin.readline().strip().upper()
reads = tuple([stdin.readline().strip().upper() for i in range(int(stdin.readline()))])
debug('Number of reads = %s', len(reads))
debug('Min read len = %s', min(map(len, reads)))
debug('Max read len = %s', max(map(len, reads)))
debug('Avg read len = %s', float(sum(map(len, reads))) / len(reads))
debug('reads %s', reads)

k = int(argv[1])
debug('k = %s', k)

# Build graph

incoming = dict()
outgoing = dict()
dbru = outgoing
for read in reads:
    for kmer in kmers(read, k):
        l = left(kmer, k - 1)
        r = right(kmer, k - 1)
        froml = outgoing.setdefault(l, dict())
        tor = incoming.setdefault(r, dict())
        froml[r] = froml.setdefault(r, 0) + 1
        tor[l] = tor.setdefault(l, 0) + 1
debug('dbru %s', dbru)

def indeg(v):
    return sum(incoming.get(v, dict()).values())

def outdeg(v):
    return sum(outgoing.get(v, dict()).values())

for v in dbru.keys():
    debug('%s in %d, out %d', v, indeg(v), outdeg(v))

# Compress graph

# TODO

print('digraph {')
for a, b in dbru.items():
    for c, n in b.items():
        print(a, '->', c, '[label=' + a + c[1:] + ']', ';')
        for _ in range(1, n):
            print(a, '->', c, ';')
print('}')

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
