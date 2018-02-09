#!/usr/bin/env python3

import logging
from logging import debug
from sys import stdin

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

codon_to_aa = {
    "GCU": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",

    "CGU": "R",
    "CGC": "R",
    "CGA": "R",
    "CGG": "R",
    "AGA": "R",
    "AGG": "R",

    "AAU": "N",
    "AAC": "N",

    "GAU": "D",
    "GAC": "D",

    "UGU": "C",
    "UGC": "C",

    "CAA": "Q",
    "CAG": "Q",

    "GAA": "E",
    "GAG": "E",

    "GGU": "G",
    "GGC": "G",
    "GGA": "G",
    "GGG": "G",

    "CAU": "H",
    "CAC": "H",

    "AUU": "I",
    "AUC": "I",
    "AUA": "I",

    "UUA": "L",
    "UUG": "L",
    "CUU": "L",
    "CUC": "L",
    "CUA": "L",
    "CUG": "L",

    "AAA": "K",
    "AAG": "K",

    "AUG": "M",

    "UUU": "F",
    "UUC": "F",

    "CCU": "P",
    "CCC": "P",
    "CCA": "P",
    "CCG": "P",

    "UCU": "S",
    "UCC": "S",
    "UCA": "S",
    "UCG": "S",
    "AGU": "S",
    "AGC": "S",

    "ACU": "T",
    "ACC": "T",
    "ACA": "T",
    "ACG": "T",

    "UGG": "W",

    "UAU": "Y",
    "UAC": "Y",

    "GUU": "V",
    "GUC": "V",
    "GUA": "V",
    "GUG": "V",

    "UAA": "-",
    "UAG": "-",
    "UGA": "-"
}

aa_to_codon = {}
for k, v in codon_to_aa.items():
    aa_to_codon.setdefault(v, set()).add(k)

# print(codon_to_aa)
# print(aa_to_codon)

def hamm_dist(s, t):
    assert(len(s) == len(t))
    return sum(si != ti for si, ti in zip(s, t))

def codon_equivs(codon):
    return aa_to_codon[codon_to_aa[codon]]

def codon_equivs_list(codons):
    return [sorted(map(lambda x: (hamm_dist(x, c), x), codon_equivs(c))) for c in codons]

def affected_codons(interval):
    return range(interval[0] // 3, interval[1] // 3 + 1)

def codons(s):
    n = len(s)
    assert(n % 3 == 0)
    return [s[i:i + 3] for i in range(0, n, 3)]

def changeable_codons(rna, intervals):
    rf = codons(rna)
    ans = dict()
    for (x, y) in intervals:
        for i in range((x - 1) // 3, (y - 1) // 3 + 1):
            ans[i] = rf[i]
    return ans

def within_interval(pos, interval):
    return pos >= interval[0] and pos <= interval[1]

def codon_positions_affected_by_interval(codon_index, interval):
    return filter(lambda i: within_interval(codon_index * 3 + i, interval), range(3))

def eliminates_interval(codon_index, prev_codon, next_codon, positions):
    return any((prev_codon[i] != next_codon[i] for i in positions))

def n_changes(rna, intervals):
    rf = codons(rna)
    eq = codon_equivs_list(rf)
    # debug("equivs %s", eq)
    codons_by_interval = dict()
    intervals_by_codon = dict()
    for interval_index, interval in enumerate(intervals):
        for codon_index in affected_codons(interval):
            codons_by_interval.setdefault(interval_index, set()).add(codon_index)
            intervals_by_codon.setdefault(codon_index, set()).add(interval_index)
    # debug("codons_by_interval %s", codons_by_interval)
    # debug("intervals_by_codon %s", intervals_by_codon)
    # equivs = codon_equivs_list(codons)
    # equivs2 = []
    # for codon_index, eq in enumerate(equivs):
    #     for dist, codon in eq:
    #         for i in intervals_by_codon[ci]:
    #             pass
    # TODO
    return -1

if __name__ == "__main__":
    t = int(stdin.readline())
    for _ in range(t):
        rna = stdin.readline().strip().upper()
        n = int(stdin.readline())
        intervals = []
        for i in range(n):
            x, y = tuple(map(int, stdin.readline().split()))
            intervals.append((x - 1, y - 1))
        debug("rna %s, intervals %s", rna, intervals)
        print(n_changes(rna, intervals))

# list of alternatives for each codon

# interval queue, take by one, change nucleotide

# number of changes, for non-intersecting intervals:
# min bound = number of intervals
# max bound = len(rna) - 3

# number of changes, for arbitrary intervals:
# min bound = 1
# max bound = len(rna) - 3

# intervals affected by codon, for non-intersecting intervals:
# min bound = 0
# max bound = 3

# codons affected by interval, for non-intersecting intervals:
# min bound = 1
# max bound = len(rna) / 3


# data = codon_equivs_list(codons(rna))
# data = list(map(lambda e: {'equivs': e, 'intervals': set()}, data))
# for ii, aff in enumerate(map(affected_codons, intervals)):
#     for ci in aff:
#         data[ci]['intervals'].add(ii)
# print(data)
