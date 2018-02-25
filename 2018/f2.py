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
        debug("reading from %s", f)
        try:
            self.n, self.m = map(int, f.readline().split())
        except ValueError:
            raise EOFError
        debug("n %s, m %s", self.n, self.m)
        self.outgoing = dict()
        self.incoming = dict()
        for _ in range(self.m):
            u, v = map(int, f.readline().split())
            self.outgoing.setdefault(u, set()).add(v)
            self.incoming.setdefault(v, set()).add(u)
        univ = set(range(1, self.n + 1))
        self.leaves = univ.difference(self.outgoing.keys())
        self.sources = univ.difference(self.incoming.keys())
        debug("sources %s, leaves %s", self.sources, self.leaves)
        self.coloring = list(map(int, f.readline().split()))
        self.avail_colors = univ.difference(self.coloring)
        debug("unassigned colors %s", self.avail_colors)
        self._depth = dict()
        self._path = dict()
        self._lca = dict()

    def path(self, u):
        s = next(iter(self.sources))
        if (s, u) not in self._path:
            def loop(ans, v):
                if v == u:
                    return ans + (v,)
                for child in self.children(v):
                    child_ans = loop(ans + (v,), child)
                    if child_ans:
                        return child_ans
                return None
            self._path[(s, u)] = loop(tuple(), s)
        return self._path[(s, u)]

    def lca(self, u, v):
        if (u, v) not in self._lca:
            def loop(ans, path_u, path_v):
                if path_u and path_v and path_u[0] == path_v[0]:
                    return loop(path_u[0], path_u[1:], path_v[1:])
                else:
                    return ans, [ans] + path_u, [ans] + path_v
            s = next(iter(self.sources))
            ans, path_u, path_v = loop(s, list(self.path(u)), list(self.path(v)))
            self._lca[(u, v)] = (path_u, path_v)
        return self._lca[(u, v)]

    def parents(self, u):
        try:
            return self.incoming[u]
        except KeyError:
            return set()

    def children(self, u):
        try:
            return self.outgoing[u]
        except KeyError:
            return set()

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

    def depth(self, u):
        if u not in self._depth:
            try:
                # XXX: max?
                self._depth[u] = max((self.depth(v) for v in self.parents(u))) + 1
            except ValueError:
                # No parents
                self._depth[u] = 0
        return self._depth[u]

    ##

    def color2(self, u):
        if self.coloring[u - 1] == -1:
            debug("coloring %s", u)
            children = self.children(u)
            if children:
                # Inner node
                debug("inner node, children %s", children)
                child_colors = set()
                for c in children:
                    cc = self.color2(c)
                    if cc:
                        child_colors.add(cc)
                debug("child_colors %s", child_colors)
                if len(child_colors) == 1:
                    self.coloring[u - 1] = child_colors.pop()
                    debug("used children color %s", self.coloring[u - 1])
                    for c in children:
                        if not self.color(c):
                            debug("forcing uncolored children %s to color", c)
                            self.force_coloring(c, self.coloring[u - 1])
                elif self.avail_colors:
                    self.coloring[u - 1] = self.avail_colors.pop()
                    debug("used unassigned color %s, avail_colors %s",
                          self.coloring[u - 1], self.avail_colors)
            else:
                # Leaf
                siblings = self.siblings(u)
                debug("leaf node, siblings %s", siblings)
                sibling_colors = set()
                for s in siblings:
                    sc = self.color2(s)
                    if sc:
                        sibling_colors.add(sc)
                debug("sibling_colors %s", sibling_colors)
                if len(sibling_colors) == 1:
                    self.coloring[u - 1] = sibling_colors.pop()
                    debug("used sibling color %s", self.coloring[u - 1])
                elif self.avail_colors:
                    self.coloring[u - 1] = self.avail_colors.pop()
                    debug("used unassigned color %s, avail_colors %s",
                          self.coloring[u - 1], self.avail_colors)
        return self.coloring[u - 1]

    def force_coloring(self, u, c):
        self.coloring[u - 1] = c
        debug("forced color of %s to %s", u, c)
        for v in self.children(u):
            self.force_coloring(v, c)

    ##

    def child_colors(self, ui):
        # return set((self.coloring[vi - 1] for vi in self.outgoing.get(ui, set())))
        return set((self.color(vi) for vi in self.outgoing.get(ui, set())))

    def dot(self):
        ans = "digraph {\n"
        for u, vs in self.outgoing.items():
            u_color = self.color(u)
            for v in vs:
                v_color = self.color(v)
                ans += "\""
                ans += str(u)
                ans += " "
                ans += str(u_color) if u_color else "_"
                ans += "\""
                ans += "->"
                ans += "\""
                ans += str(v)
                ans += " "
                ans += str(v_color) if v_color else "_"
                ans += "\""
                ans += ";\n"
        ans += "}"
        return ans

# If all the children have no color, pick an available color, color itself and all the children
# If there's only one color used in children, color itself and all uncolored children to this color
# If there are multiple colors used in children, pick available colors for itself and uncolored children

# If is leaf and no color, stay uncolored

def species_recovering():
    n = Network(stdin)
    debug(n.dot())
    debug("depth(5) %s", n.depth(5))
    debug("uncolored %s", n.uncolored())
    debug("avail_colors %s", n.avail_colors)
    # debug("uncolored leaves %s", n.uncolored() & n.leaves)
    # debug("uncolored by depth %s", sorted(n.uncolored(), key = n.depth, reverse = True))
    leaves_by_color = dict()
    for u in n.leaves:
        leaves_by_color.setdefault(n.color(u), set()).add(u)
    debug("leaves_by_color %s", leaves_by_color)
    for color in range(1, n.n + 1):
        leaves = leaves_by_color.get(color, set())
        if leaves:
            leaves_iter = iter(leaves)
            u = next(leaves_iter)
            for v in leaves_iter:
                path_u, path_v = n.lca(u, v)
                for w in path_u:
                    n.coloring[w - 1] = color
                for w in path_v:
                    n.coloring[w - 1] = color
    debug("colors after initial coloring %s", n.coloring)

    for u in n.uncolored():
        if n.avail_colors:
            n.coloring[u - 1] = n.avail_colors.pop()
    debug("colors after dumb coloring %s", n.coloring)

    # # Enqueue colored leaves first
    # q = deque()
    # q.extend(n.colored().intersection(n.leaves))
    # debug("initial queue %s", q)
    # # Visit vertices from the queue
    # while q:
    #     debug("queue before %s", q)
    #     u = q.popleft()
    #     color = n.color(u)
    #     parents = n.parents(u)
    #     siblings = n.siblings(u)
    #     debug("u %s, color %s, parents %s, siblings %s", u, color, parents, siblings)
    #     if color:
    #         # Self has color
    #         pass
    #     else:
    #         # Self has no color
    #         sibling_colors = set((n.color(v) for v in siblings))
    #         pass
    #
    #     if parents:
    #         pass
    #     else:
    #         pass
    #     parent = parents.pop()  # XXX: tree specific
    #     parent_color = n.color(parent)
    #     if parent_color:
    #         pass
    #     else:
    #         pass
    #     # q.extend(iter(parents))
    #     q.append(parent)
    #     debug("queue after %s", q)
    # for i, c in enumerate(n.coloring):
    #     if n.coloring[i] == -1 and n.avail_colors:
    #         n.coloring[i] = n.avail_colors.pop()
    # Print result
    if not n.uncolored():
        print("YES")
        print(" ".join(map(str, n.coloring)))
    else:
        print("NO")
    # raise EOFError

if __name__ == "__main__":
    while True:
        try:
            species_recovering()
        except EOFError:
            break
