#!/usr/bin/env python3

import logging

from bisect import bisect
from logging import debug
from sys import stdin
from time import time

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

def edit_dist(s, t):
    n = len(s)
    m = len(t)
    d = [[0] * (m + 1) for _ in range(2)]
    for j in range(1, m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        d[i % 2][0] = i
        for j in range(1, m + 1):
            cost = 0 if s[i - 1] == t[j - 1] else 1
            delt = d[(i - 1) % 2][j] + 1
            ins = d[i % 2][j - 1] + 1
            subst = d[(i - 1) % 2][j - 1] + cost
            dist = min(delt, ins, subst)
            d[i % 2][j] = dist
    return d[n % 2][m]

def gc_content(s):
    return (s.count("G") + s.count("C")) / len(s)

def purine_content(s):
    return (s.count("A") + s.count("G")) / len(s)

def read_fasta(f):
    ans = []
    while True:
        ident = f.readline().lstrip("> ").rstrip()
        seq = f.readline().strip().upper()
        if ident == "" and seq == "":
            break
        ans.append((ident, seq))
    return ans

def gc_content_clusters():
    ans = dict()
    for ident, seq in read_fasta(stdin):
        # c = round(100 * gc_content(seq))
        c = round(1000 * gc_content(seq))
        ans.setdefault(c, set()).add(ident)
    return ans

def content_clusters(content_func):
    clusters = [(i / 1000) for i in range(0, 100 * 1000, 30)]
    ans = dict()
    for ident, seq in read_fasta(stdin):
        c = bisect(clusters, content_func(seq))
        ans.setdefault(c, set()).add(ident)
    return ans

def dumb_clusters():
    ans = dict()
    for ident, seq in read_fasta(stdin):
        ans.setdefault(ident, set()).add(ident)
    return ans

if __name__ == "__main__":
    # ans = gc_content_clusters()
    # ans = dumb_clusters()
    ans = content_clusters(gc_content)
    # ans = content_clusters(purine_content)
    for cluster, ident_set in ans.items():
        for ident in ident_set:
            print(ident, cluster)
