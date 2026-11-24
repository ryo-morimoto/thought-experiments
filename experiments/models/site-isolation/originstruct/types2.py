"""Relational types of the richer origin domain (originstruct/RESULTS.md).

usage: python3 -I originstruct/types2.py [--search]   (from site-isolation/)

Extends adequacy/types.py. An origin is ("op", id) (opaque) or
("t", scheme, host, port). A PSL is an abstract function reg: host -> domain
or None, and pt: host -> bool says whether the host alone makes a tuple origin
potentially trustworthy (loopback IP, localhost, *.localhost). The operators
of OriginStruct.tla see an origin only through:
  unary : opaque?, scheme, reg(host) is None, pt(host)
  pairs : equal (opaque ids, or scheme+host+port), same host, same port,
          reg(hostA) = reg(hostB) non-null
(schemelessly same site, obtain a site, KeyR, same origin and the CORP
scheme condition are all functions of these). The type of a k-tuple is
that vector. The possible types are those of a universe with k of every
host class, k hosts per registrable domain, k ports and k opaque origins.
"""
import itertools
import sys

# host -> (registrable domain or None, potentially trustworthy host), for the
# hosts of OriginStruct.tla under PSL "A" (only "test" and "localhost" are
# public suffixes) or PSL "B" ("a.test" is a public suffix too).
NORMAL = ("a.test", "x.a.test", "y.a.test", "b.test", "c.test")
LOCALREG = ("a.localhost", "x.a.localhost", "y.a.localhost", "b.localhost", "c.localhost")
NULL_PT = ("127.0.0.2", "127.0.0.1", "localhost")
NULL_NPT = ("198.51.100.1", "test", "192.0.2.1")   # "test" is itself a public suffix
# adequacy/Domains.tla's D18 hosts (3 sites x apex, www1, www2), for comparison
D18_HOSTS = tuple(p + s for s in ("a.test", "b.test", "c.test") for p in ("", "www1.", "www2."))


def base(h):
    return h if h.count(".") == 1 else h.split(".", 1)[1]


def host_table(psl):
    t = {}
    for h in NORMAL:
        t[h] = (base(h), False)
    for h in LOCALREG:
        t[h] = (base(h), True)
    for h in NULL_PT:
        t[h] = (None, True)
    for h in NULL_NPT:
        t[h] = (None, False)
    for h in D18_HOSTS:
        t.setdefault(h, (base(h), False))
    if psl == "B":  # "a.test" is also a public suffix (like a shared hosting suffix)
        t["a.test"] = (None, False)
        t["x.a.test"] = ("x.a.test", False)
        t["y.a.test"] = ("y.a.test", False)
    return t


def ty(tup, H):
    unary, pairs = [], []
    for o in tup:
        unary.append(("op",) if o[0] == "op" else ("t", o[1], H[o[2]][0] is None, H[o[2]][1]))
    for i in range(len(tup)):
        for j in range(i + 1, len(tup)):
            a, b = tup[i], tup[j]
            if a[0] == "op" or b[0] == "op":
                pairs.append(("eq", a == b))
            else:
                ra, rb = H[a[2]][0], H[b[2]][0]
                pairs.append((a == b, a[2] == b[2], a[3] == b[3], ra is not None and ra == rb))
    return tuple(unary), tuple(pairs)


def universe(k):
    H, hosts = {}, []
    for cls, pt in (("n", False), ("l", True)):
        for g in range(k):
            for i in range(k):
                h = "%s%d.r%d.%s" % (cls, i, g, cls)
                H[h] = ("r%d.%s" % (g, cls), pt)
                hosts.append(h)
    for cls, pt in (("z", False), ("p", True)):
        for i in range(k):
            h = "%s%d" % (cls, i)
            H[h] = (None, pt)
            hosts.append(h)
    org = [("t", s, h, p) for s in ("https", "http") for h in hosts for p in range(k)]
    org += [("op", i) for i in range(k)]
    return org, H


def possible(k):
    org, H = universe(k)
    return {ty(t, H) for t in itertools.product(org, repeat=k)}


def realized(dom, H, k):
    return {ty(t, H) for t in itertools.product(sorted(dom), repeat=k)}


def twin(o):
    return ("t", "https", o[2], o[3]) if o[0] == "t" else o


# The domain used in OriginStruct.tla (DomRich, HostPorts): kept in sync by hand.
# It is --minimize's k=3 result with the abstract hosts renamed and the ports
# renamed 2 -> "", 1 -> "8443", 0 -> "8444".
PORTS = ("", "8443", "8444")
STAIR = (1, 2, 3, 1, 2)   # number of ports per host, in the order of NORMAL / LOCALREG
def dom_rich():
    d = set()
    hp = list(zip(NORMAL, STAIR)) + list(zip(LOCALREG, STAIR)) + \
        list(zip(NULL_PT, (1, 2, 3))) + list(zip(NULL_NPT, (1, 2, 3)))
    for s in ("https", "http"):
        for h, n in hp:
            for p in PORTS[:n]:
                d.add(("t", s, h, p))
    d |= {("op", "n1"), ("op", "n2"), ("op", "n3")}
    return d


def dom_small():
    """OriginStruct's DomSmall: --minimize 2's result, renamed (1 -> "", 0 -> "8443")."""
    d = set()
    stair2 = (1, 2, 0, 1, 0)
    hp = list(zip(NORMAL, stair2)) + list(zip(LOCALREG, stair2)) + \
        list(zip(NULL_PT, (0, 1, 2))) + list(zip(NULL_NPT, (0, 1, 2)))
    for s in ("https", "http"):
        for h, n in hp:
            for p in PORTS[:n]:
                d.add(("t", s, h, p))
    d |= {("op", "n1"), ("op", "n2")}
    return d


def minimize(k=3):
    """Reverse-delete from universe(k): drop an origin (an https origin together
    with its http twins, so the result stays twin-closed) whenever every type of
    k-tuples is still realized. Returns an abstract domain realizing all types."""
    from collections import Counter
    org, H = universe(k)
    D = set(org)
    cnt = Counter(ty(t, H) for t in itertools.product(sorted(D), repeat=k))
    order = sorted(D, key=lambda o: (o[0] == "t" and o[1] == "https", o))
    for o in order:
        if o not in D:
            continue
        rm = {o}
        if o[0] == "t" and o[1] == "https":
            rm |= {x for x in D if x[0] == "t" and x[1] == "http" and x[2:] == o[2:]}
        lost = Counter(ty(t, H) for t in itertools.product(sorted(D), repeat=k)
                       if any(x in rm for x in t))
        if all(cnt[t] - lost[t] > 0 for t in lost):
            D -= rm
            cnt -= lost
    return D, H


def main():
    if "--minimize" in sys.argv:
        k = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 3
        D, H = minimize(k)
        print("minimized abstract domain realizing all k=%d types:" % k, len(D))
        for o in sorted(D, key=str):
            print("  ", o, H.get(o[2]) if o[0] == "t" else "")
        return 0
    want = {k: possible(k) for k in (1, 2, 3)}
    for k in (1, 2, 3):
        print("possible types k=%d: %d" % (k, len(want[k])))
    d18 = {("t", s, h, "") for s in ("https", "http") for h in D18_HOSTS}
    for name, d in (("adequacy D18 (no port/opaque)", d18), ("DomSmall", dom_small()),
                    ("DomRich", dom_rich())):
        closed = all(twin(o) in d for o in d)
        for psl in ("A", "B"):
            H = host_table(psl)
            row = ["%d/%d" % (len(realized(d, H, k) & want[k]), len(want[k])) for k in (1, 2, 3)]
            print("%-32s |D|=%3d PSL %s twin-closed=%s k=1,2,3: %s" % (name, len(d), psl, closed, " ".join(row)))
    if "--search" in sys.argv:
        H = host_table("A")
        miss = want[3] - realized(dom_rich(), H, 3)
        print("missing k=3 types in DomRich (PSL A):", len(miss))
        for m in sorted(miss)[:10]:
            print("  ", m)


if __name__ == "__main__":
    sys.exit(main())
