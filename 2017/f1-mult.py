#!/usr/bin/env python3

from bisect import bisect_left, bisect_right
from sys import stdin
import logging

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

def intersects(a, b):
    return a[0] <= b[1] and b[0] <= a[1]

class DIS2:
    def __init__(self, ivlists):
        self.mapping = dict()

        self.first = []
        self.last = []
        for i in range(len(ivlists)):
            for iv in ivlists[i]:
                self.first.append(iv)
                self.last.append(iv)
                self.mapping[iv] = i
        self.first.sort(key=lambda t: t[0])
        self.last.sort(key=lambda t: t[1])

        self.first_last = [t[1] for t in self.first]
        # self.first_index = [t[2] for t in self.first]
        self.first = [t[0] for t in self.first]

        self.last_first = [t[0] for t in self.last]
        # self.last_index = [t[2] for t in self.last]
        self.last = [t[1] for t in self.last]

        logging.debug('first %s %s', self.first, self.first_last)
        logging.debug('last %s %s', self.last_first, self.last)

    def __len__(self):
        return len(self.first)

    def _intersects1(self, iv):
        i = bisect_right(self.first, iv[1])
        logging.debug('first %s, iv[1] %s, i %s', self.first, iv[1], i)
        if i == 0:
            return 0
        if not intersects((self.first[i - 1], self.first_last[i - 1]), iv):
            logging.debug('no intersection %s %s', (self.first[i - 1], self.first_last[i - 1]), iv)
            return 0
        j = bisect_left(self.last, iv[0])
        logging.debug('last %s, iv[0] %s, j %s', self.last, iv[0], j)
        if j == len(self.last):
            return 0
        if not intersects((self.last_first[j], self.last[j]), iv):
            logging.debug('no intersection %s %s', (self.last_first[j], self.last[j]), iv)
            return 0
        logging.debug('i %d, j %d = %d', i, j, i - j)
        # TODO
        return i - j

    def intersects(self, ivs):
        logging.debug('ivs %s', ivs)
        ans = 0
        for iv in ivs:
            logging.debug('iv %s', iv)
            ans += self._intersects1(iv)
            logging.debug('ans %s', ans)
        return ans

# --------------------------------------------------------------------------------------

def ivsoflist(l):
    return [(l[2 * i], l[2 * i + 1]) for i in range(len(l) // 2)]

def ivsofstr(s):
    return ivsoflist(list(map(int, s.split())))

if __name__ == '__main__':
    n, m = map(int, stdin.readline().split())
    logging.debug('n %s, m %s', n, m)
    genes = DIS2([ivsofstr(stdin.readline()) for _ in range(n)])
    reads = [ivsofstr(stdin.readline()) for _ in range(m)]

    ans = [0] * n
    # tmp = [-1] * m
    #
    tmp = [genes.intersects(reads[j]) for j in range(len(reads))]
    logging.debug('tmp %s', tmp)
    # for x in tmp:
    #     if len(x) == 1:
    #         ans[x[0]] += 1
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
