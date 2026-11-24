"""Compare two MutKill TLC outputs (adequacy/RESULTS.md).

usage: python3 -I adequacy/compare.py <base.out> <large.out>

Prints, per output, the kill table, the signature-equivalent set and the
classes, and whether they are equal. The nested property comes from
"nested-kills" (NestedSym) when "kills" lacks it.
"""
import re
import sys


def flat(path):
    with open(path, encoding="utf-8") as f:
        return " ".join(f.read().split())


def strings(s):
    return set(re.findall(r'"([^"]*)"', s))


def section(text, tag, nxt):
    i = text.index('"%s"' % tag)
    j = text.index('"%s"' % nxt, i) if nxt else len(text)
    return text[i:j]


def parse(path):
    t = flat(path)
    kills = {}
    direct = set()
    for m, props in re.findall(r'<< ?"([^"]+)", \{([^}]*)\} ?>>', section(t, "kills", "equiv-none")):
        kills[m] = strings(props) - {"COIOnlyWithOptInNested"}
        if "COIOnlyWithOptInNested" in strings(props):
            direct.add(m)
    kills = {m: p for m, p in kills.items() if p}
    nested = strings(section(t, "nested-kills", None).split("}")[0]) - {"nested-kills"}
    if direct:
        print(path, "NestedSym kills = COIOnlyWithOptInNested kills:", direct == nested)
    for m in nested:
        kills.setdefault(m, set()).add("COIOnlyWithOptInNested")
    equiv = strings(section(t, "equiv-none", "nclasses")) - {"equiv-none"}
    ncl = int(re.search(r'"nclasses", (\d+)', t).group(1))
    cls = section(t, "classes>1", None).split("Warning")[0]
    classes = {frozenset(strings(c)) for c in re.findall(r"\{([^{}]*)\}", cls)}
    dom = re.search(r'"domain", (\d+), "sigdom", (\d+)', t).groups()
    return dom, kills, equiv, ncl, classes


def main(a, b):
    pa, pb = parse(a), parse(b)
    for p in (pa, pb):
        print("domain", p[0], "killed", len(p[1]), "equiv-none", len(p[2]), "classes", p[3])
    print("kills equal:", pa[1] == pb[1])
    for m in sorted(set(pa[1]) | set(pb[1])):
        if pa[1].get(m, set()) != pb[1].get(m, set()):
            print("  differs", m, sorted(pa[1].get(m, set())), sorted(pb[1].get(m, set())))
    print("equiv-none equal:", pa[2] == pb[2], sorted(pa[2] ^ pb[2]))
    print("classes equal:", pa[4] == pb[4] and pa[3] == pb[3])


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
