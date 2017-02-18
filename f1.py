#!/usr/bin/env python3

from sys import stdin

def intervals(l):
    return [(l[2 * i], l[2 * i + 1]) for i in range(len(l) // 2)]

n, m = map(int, stdin.readline().split())
genes = [intervals(list(map(int, stdin.readline().split()))) for _ in range(n)]
reads = [intervals(list(map(int, stdin.readline().split()))) for _ in range(m)]
# print('genes', genes)
# print('reads', reads)

def intersects0(a, b):
    return a[0] <= b[1] and b[0] <= a[1]

def intersects(gene, read):
    for g in gene:
        for r in read:
            if intersects0(r, g):
                # print('gene', gene, 'read', read, True)
                return True
    # print('gene', gene, 'read', read, False)
    return False

intersects_tab = [[False] * n for _ in range(m)]
for i in range(len(genes)):
    for j in range(len(reads)):
        intersects_tab[j][i] = intersects(genes[i], reads[j])
# print(intersects_tab)

ans = [0] * n
for j in range(len(reads)):
    try:
        i = intersects_tab[j].index(True, 0)
        try:
            intersects_tab[j].index(True, i + 1)
        except ValueError:
            ans[i] += 1
    except ValueError:
        pass
print('\n'.join(map(str, ans)))
