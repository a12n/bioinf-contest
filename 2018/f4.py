#!/usr/bin/env python3

import logging

from bisect import bisect
from logging import debug
from sys import stdin
from time import time

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

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
    clusters = [(i / 1000) for i in range(0, 100 * 1000, 50)]
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
