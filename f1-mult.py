#!/usr/bin/env python3

from bisect import bisect_left, bisect_right
from sys import stdin
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)

def intersects(a, b):
    return a[0] <= b[1] and b[0] <= a[1]

class DIS2:
    def __init__(self, ivlists):
        tmp = []
        for i in range(len(ivlists)):
            for iv in ivlists[i]:
                tmp.append((iv[0], iv[1], i))
        tmp.sort(key=lambda e: e[0])
        self.first = [iv[0] for iv in tmp]
        self.last = [iv[1] for iv in tmp]
        self.index = [iv[2] for iv in tmp]
        logging.debug('first %s', self.first)
        logging.debug('last %s', self.last)
        logging.debug('index %s', self.index)

    def _intersects1(self, iv):
        i = bisect_right(self.first, iv[1])
        logging.debug('first %s, iv[1] %s, i %s', self.first, iv[1], i)
        if i == 0:
            return []
        if not intersects((self.first[i - 1], self.last[i - 1]), iv):
            return []
        j = bisect_left(self.last, iv[0])
        logging.debug('last %s, iv[0] %s, j %s', self.last, iv[0], j)
        if j == len(self.last):
            return []
        if not intersects((self.first[j], self.last[j]), iv):
            return []
        logging.debug('index[%d:%d] %s', j, i, self.index[j:i])
        return self.index[j:i]

    def intersects(self, ivs):
        logging.debug('ivs %s', ivs)
        ans = set()
        for iv in ivs:
            logging.debug('iv %s', iv)
            ans.update(self._intersects1(iv))
        return ans

# --------------------------------------------------------------------------------------

def ivsoflist(l):
    return [(l[2 * i], l[2 * i + 1]) for i in range(len(l) // 2)]

def ivsofstr(s):
    return ivsoflist(list(map(int, s.split())))

if __name__ == '__main__':
    n, m = map(int, stdin.readline().split())
    genes = DIS2([ivsofstr(stdin.readline()) for _ in range(n)])
    reads = [ivsofstr(stdin.readline()) for _ in range(m)]

    ans = [0] * n
    # tmp = [-1] * m
    #
    tmp = [list(genes.intersects(reads[j])) for j in range(len(reads))]
    for x in tmp:
        if len(x) == 1:
            ans[x[0]] += 1
    #         if tmp[j] == -1:
    #             if reads[j].intersects(genes[i]):
    #                 tmp[j] = i
    #         elif tmp[j] != -2:
    #             if reads[j].intersects(genes[i]):
    #                 tmp[j] = -2
    #
    # for i in tmp:
    #     if i >= 0:
    #         ans[i] += 1

    print('\n'.join(map(str, ans)))
