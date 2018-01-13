#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin

level = logging.DEBUG
# level = logging.WARNING
logging.basicConfig(format='%(message)s', level=level)

def readseq():
    return stdin.readline().strip().upper()

s = readseq()
reads = tuple([readseq() for i in range(int(stdin.readline()))])

debug('s = %s', s)
debug('%d reads = %s', len(reads), reads)

# nstates = 2**len(reads) - 1
# states = ([reads[i] if (k >> i) & 1 != 0 else None for i in range(len(reads))] for k in range(nstates, 0, -1))
# debug('nstates = %s', nstates)
# debug('states = %s', states)
# for s in states:
#     debug(s)

def findsubseqstart(s, t, start=None):
    ans = s.find(t[0], start)
    return ans if ans != -1 else None

def findsubseq(s, t, start=None):
    ans = []
    p = start
    for c in t:
        q = s.find(c, p)
        if q == -1:
            return None
        ans.append(q)
        p = q + 1
    return ans

def issubseq(s, t, start=None):
    p = start
    for c in t:
        q = s.find(c, p)
        if q == -1:
            return False
        p = q + 1
    return True

def findallsubseq(s, t):
    start = 0
    while True:
        p = findsubseq(s, t, start)
        if p == None:
            break
        yield p
        start = p[0] + 1

def overlap(s, t):
    ans = 0
    n = min(len(s), len(t)) - 1
    for i in range(n):
        if s[-i:] == t[0:i]:
            ans = i
    # debug('overlap "%s" "%s" = %d', s, t, ans)
    return ans

def combine(s, t, l=None):
    # debug('combine: "%s" "%s" %s', s, t, l)
    n = len(s)
    if not l:
        l = overlap(s, t)
    assert l >= 0 and l <= n
    return s[0:(n - l)] + t

# def longestoverlap(seqs):
#     ians, jans, lans = -1, -1, -1
#     for i in range(len(seqs)):
#         for j in range(len(seqs)):
#             if i == j:
#                 continue
#             l = overlap(seqs[i], seqs[j])
#             if l > lans:
#                 ians = i
#                 jans = j
#                 lans = l
#     return (ians, jans, lans)

def findoverlaps(seqs):
    debug('len(seqs) = %s', len(seqs))
    for i1, t1 in seqs.items():
        yield (i1, t1)
        for i2, t2 in seqs.items():
            if len(set(i1) & set(i2)) == 0:
                t = combine(t1, t2)
                if issubseq(s, t):
                    yield (i1 + i2, t)

def maxk(seqs):
    return max(seqs.keys(), key=len)

def printsolution(seqs):
    k = maxk(seqs)
    # Output
    print('-' * 80)
    print(seqs[k])
    for i in range(len(reads)):
        if i in k:
            print(seqs[k].find(reads[i]) + 1)
        else:
            print(-1)
    print('-' * 80)

def assembly(seqs):
    prev = {(i,): seqs[i] for i in range(len(seqs))}
    prevk = maxk(prev)
    while True:
        printsolution(prev)
        cur = dict(findoverlaps(prev))
        curk = maxk(cur)
        if len(curk) <= len(prevk):
            return cur
        prev = cur
        prevk = curk

#
# def scs(seqs):
#     debug('seqs = %s', seqs)
#     i, j, l = longestoverlap(seqs)
#     debug('i j l = %d %d %d', i, j, l)
#     if l == -1:
#         return seqs[0]
#     s = combine(seqs[i], seqs[j], l)
#     i, j = min(i, j), max(i, j)
#     del(seqs[j])
#     seqs[i] = s
#     return scs(seqs)
#
# t = scs(r.copy())
# print(t)
# for x in r:
#     p = t.find(x)
#     print(p + 1 if p != -1 else -1)

# x = {(i,): reads[i] for i in range(len(reads))}
# print(len(x), x)
#
# x = dict(findoverlaps(x))
# print(len(x), x)
#
# x = dict(findoverlaps(x))
# print(len(x), x)
#
# x = dict(findoverlaps(x))
# print(len(x), x)

assembly(reads)
