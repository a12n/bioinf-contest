#!/usr/bin/env python3

from collections import deque
from logging import debug
from sys import stdin
from time import time
import itertools
import logging

logging.basicConfig(format="%(message)s", level=logging.DEBUG)

class Network:
    def __init__(self, f):
        self.n, self.m = map(int, f.readline().split())
        self.outgoing = dict()
        self.incoming = dict()
        for _ in range(self.m):
            u, v = map(int, f.readline().split())
            self.outgoing.setdefault(u, set()).add(v)
            self.incoming.setdefault(v, set()).add(u)
        univ = set(range(1, self.n + 1))
        self.leaves = univ.difference(self.outgoing.keys())
        self.sources = univ.difference(self.incoming.keys())
        self.coloring = list(map(int, f.readline().split()))
        self.avail_colors = u.difference(self.coloring)

    def parents(self, u):
        return self.incoming[u]

    def children(self, u):
        return self.outgoing[u]

    def siblings(self, u):
        ans = set()
        for v in self.parents(u):
            ans.update(self.children(v))
        ans.discard(u)
        return ans

    def color(self, u):
        return self.coloring[u - 1] if self.coloring[u - 1] != -1 else None

    def colored(self):
        return set((i + 1 for i, c in enumerate(self.coloring) if c != -1))

    def uncolored(self):
        return set((i + 1 for i, c in enumerate(self.coloring) if c == -1))

    ##

    def child_colors(self, ui):
        # return set((self.coloring[vi - 1] for vi in self.outgoing.get(ui, set())))
        return set((self.color(vi) for vi in self.outgoing.get(ui, set())))

    def color(self, ui):
        if self.coloring[ui - 1] == -1:
            # TODO
            pass
        return self.coloring[ui - 1]

    def dot(self):
        ans = "digraph {\n"
        for ui, v in self.outgoing.items():
            for vi in v:
                ans += "\""
                ans += str(ui)
                ans += " "
                ans += "?" if self.coloring[ui - 1] == -1 else str(self.coloring[ui - 1])
                ans += "\""
                ans += "->"
                ans += "\""
                ans += str(vi)
                ans += " "
                ans += "?" if self.coloring[vi - 1] == -1 else str(self.coloring[vi - 1])
                ans += "\""
                ans += ";\n"
        ans += "}\n"
        return ans

# If all the children have no color, pick an available color, color itself and all the children
# If there's only one color used in children, color itself and all uncolored children to this color
# If there are multiple colors used in children, pick available colors for itself and uncolored children

# If is leaf and no color, stay uncolored

def species_recovering():
    n = Network(stdin)
    debug("coloring %s, uncolored %s", n.coloring, n.uncolored())
    debug("child_colors(1) %s", n.child_colors(1))
    debug("siblings(3) %s", n.siblings(3))
    # Enqueue colored leaves first
    q = deque()
    for u in n.leaves:
        c = n.color(u)
        if c:
            q.append(u)
    # Visit vertices from the queue
    while not q.empty():
        pass
    # Print result
    if not n.uncolored():
        print("YES")
        print(" ".join(map(str, n.coloring)))
    else:
        print("NO")

if __name__ == "__main__":
    while True:
        try:
            species_recovering()
        except ValueError:
            break
