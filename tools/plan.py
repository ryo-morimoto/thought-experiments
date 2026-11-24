"""作業の木（plan/<name>/tree.toml）を検査し、TREE.md を生成し、次の候補を出す。依存は標準ライブラリだけ（Python 3.11+）。

    python3 tools/plan.py check            # すべての木と、思考実験の記録の「木の節」の宣言を検査する
    python3 tools/plan.py render           # plan/<name>/TREE.md を生成する
    python3 tools/plan.py next [name]      # 次の候補（未完了の葉を impact の順に）を出す

正本は tree.toml。根拠は、記録の見出しの「- 木の節: <name>/<id>, ...」（または「- 木の節: なし」）から集める。
子を持つ節の状態は、子の状態から計算する（保存しない）。
"""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN_DIR = ROOT / "plan"
RECORD_GLOBS = ["experiments/*.md"]  # experiments/prereg/ は事前登録で固定するので、宣言を足さず evidence で結ぶ
RECORD_EXCLUDE = {"experiments/README.md"}
NODE_LINE = re.compile(r"^- 木の節:\s*(.+?)\s*$", re.M)
STATE_LINE = re.compile(r"^- 状態:\s*(\S+)", re.M)

STATUSES = ["done", "partial", "todo", "out", "parked"]
LABEL = {"done": "済", "partial": "一部", "todo": "未", "out": "外", "parked": "保留"}
IMPACTS = {"high": 0, "mid": 1, "low": 2}
LEAF_FIELDS = {"status", "impact", "done_when"}
ALLOWED_FIELDS = {"id", "parent", "title", "status", "impact", "done_when", "note", "evidence"}


def load_trees() -> dict[str, dict]:
    trees = {}
    for path in sorted(PLAN_DIR.glob("*/tree.toml")):
        with path.open("rb") as f:
            data = tomllib.load(f)
        trees[path.parent.name] = {"path": path, "meta": data.get("meta", {}), "nodes": data.get("node", [])}
    return trees


def load_records() -> list[dict]:
    """記録ごとに、宣言した節（[(木, id)]、または 'none'）と状態を返す。"""
    recs = []
    for pattern in RECORD_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            rel = path.relative_to(ROOT).as_posix()
            if rel in RECORD_EXCLUDE:
                continue
            text = path.read_text(encoding="utf-8")
            head = text.split("\n## ", 1)[0]
            m = NODE_LINE.search(head)
            st = STATE_LINE.search(head)
            decl: list[tuple[str, str]] | str | None
            if m is None:
                decl = None
            elif m.group(1) == "なし":
                decl = "none"
            else:
                decl = []
                for item in re.split(r"[、,]\s*", m.group(1)):
                    item = item.strip()
                    if "/" not in item:
                        decl.append(("", item))
                    else:
                        tree, nid = item.split("/", 1)
                        decl.append((tree.strip(), nid.strip()))
            recs.append({"path": rel, "decl": decl, "state": st.group(1) if st else None})
    return recs


def children_of(nodes: list[dict]) -> dict[str, list[str]]:
    ch: dict[str, list[str]] = {n["id"]: [] for n in nodes}
    for n in nodes:
        if "parent" in n and n["parent"] in ch:
            ch[n["parent"]].append(n["id"])
    return ch


def derived_status(nid: str, by_id: dict, ch: dict) -> str:
    kids = ch[nid]
    if not kids:
        return by_id[nid].get("status", "todo")
    st = {derived_status(k, by_id, ch) for k in kids}
    active = st - {"out", "parked"}
    if not active:
        return "out" if st == {"out"} else "parked"
    if active == {"done"}:
        return "done"
    if active == {"todo"}:
        return "todo"
    return "partial"


def evidence_for(name: str, nid: str, recs: list[dict]) -> list[str]:
    return [r["path"] for r in recs if isinstance(r["decl"], list) and (name, nid) in r["decl"]]


def check(trees: dict, recs: list[dict]) -> list[str]:
    errs: list[str] = []
    for name, t in trees.items():
        rel = t["path"].relative_to(ROOT).as_posix()
        nodes = t["nodes"]
        ids = [n.get("id") for n in nodes]
        if len(ids) != len(set(ids)):
            errs.append(f"{rel}: id が重複している")
        by_id = {n["id"]: n for n in nodes if "id" in n}
        roots = [n for n in nodes if "parent" not in n]
        if len(roots) != 1:
            errs.append(f"{rel}: 根（parent の無い節）はちょうど 1 つ（今は {len(roots)}）")
        for n in nodes:
            nid = n.get("id", "?")
            for k in n:
                if k not in ALLOWED_FIELDS:
                    errs.append(f"{rel}: {nid} の欄 {k!r} は使えない")
            if "title" not in n:
                errs.append(f"{rel}: {nid} に title が無い")
            if "parent" in n and n["parent"] not in by_id:
                errs.append(f"{rel}: {nid} の parent {n['parent']!r} が無い")
            for p in n.get("evidence", []):
                if not (ROOT / p).exists():
                    errs.append(f"{rel}: {nid} の evidence {p} が無い")
        # 循環
        for n in nodes:
            seen, cur = set(), n
            while "parent" in cur:
                if cur["id"] in seen:
                    errs.append(f"{rel}: {n['id']} から親をたどると循環する")
                    break
                seen.add(cur["id"])
                cur = by_id.get(cur["parent"], {})
                if not cur:
                    break
        ch = children_of([n for n in nodes if "id" in n])
        for nid, kids in ch.items():
            n = by_id[nid]
            if kids:
                for k in LEAF_FIELDS:
                    if k in n:
                        errs.append(f"{rel}: {nid} は子を持つので {k} を書かない（子から計算する）")
            elif "parent" in n:
                for k in LEAF_FIELDS:
                    if k not in n:
                        errs.append(f"{rel}: 葉 {nid} に {k} が無い")
                if n.get("status") not in STATUSES:
                    errs.append(f"{rel}: {nid} の status {n.get('status')!r} は {STATUSES} のどれかにする")
                if n.get("impact") not in IMPACTS:
                    errs.append(f"{rel}: {nid} の impact {n.get('impact')!r} は {list(IMPACTS)} のどれかにする")
                if n.get("status") in ("done", "partial"):
                    if not evidence_for(name, nid, recs) and not n.get("evidence"):
                        errs.append(f"{rel}: {nid} は {n['status']} だが根拠（記録の宣言か evidence）が無い")
        # 生成物が最新か
        out = t["path"].parent / "TREE.md"
        if not out.exists() or out.read_text(encoding="utf-8") != render_tree(name, t, recs):
            errs.append(f"{out.relative_to(ROOT).as_posix()} が tree.toml と記録に一致しない。render で再生成する")
    # 記録の宣言
    for r in recs:
        if r["decl"] is None:
            errs.append(f"{r['path']}: 見出しに「- 木の節: <木>/<id>」か「- 木の節: なし」が無い")
            continue
        if r["decl"] == "none":
            continue
        for tree, nid in r["decl"]:
            if tree not in trees:
                errs.append(f"{r['path']}: 木 {tree!r} が plan/ に無い")
            elif nid not in {n["id"] for n in trees[tree]["nodes"]}:
                errs.append(f"{r['path']}: 節 {tree}/{nid} が木に無い")
    return errs


def render_tree(name: str, t: dict, recs: list[dict]) -> str:
    nodes = [n for n in t["nodes"] if "id" in n]
    by_id = {n["id"]: n for n in nodes}
    ch = children_of(nodes)
    meta = t["meta"]
    lines = [
        f"<!-- 自動生成: python3 tools/plan.py render。手で編集しない（元は plan/{name}/tree.toml と記録の「木の節」）。 -->",
        f"# 作業の木: {meta.get('question', name)}",
        "",
        f"今の答え: {meta.get('answer', '')}",
        "",
        "状態の印: [済] 結論が出た、[一部] 進めたが完了の条件を満たしていない、[未] 手を付けていない、[外] 範囲の外、[保留] 止めている。子を持つ節の状態は子から計算する。",
        "",
        "## 木",
        "",
    ]

    def walk(nid: str, depth: int) -> None:
        n = by_id[nid]
        st = LABEL[derived_status(nid, by_id, ch)]
        imp = f"（効き: {n['impact']}）" if not ch[nid] and "impact" in n else ""
        lines.append(f"{'  ' * depth}- **{nid}** [{st}] {n['title']}{imp}")
        pad = "  " * (depth + 1)
        if n.get("done_when"):
            lines.append(f"{pad}- 完了の条件: {n['done_when']}")
        if n.get("note"):
            lines.append(f"{pad}- 今: {n['note']}")
        ev = evidence_for(name, nid, recs) + n.get("evidence", [])
        if ev:
            links = "、".join(f"[{Path(p).name}](../../{p})" for p in ev)
            lines.append(f"{pad}- 根拠: {links}")
        for k in ch[nid]:
            walk(k, depth + 1)

    root = next(n["id"] for n in nodes if "parent" not in n)
    walk(root, 0)
    lines += ["", "## 次の候補", "", "未完了（未・一部）の葉を、効きの大きい順に並べた。", ""]
    for n in next_candidates(t):
        lines.append(f"- **{n['id']}** [{LABEL[n['status']]}・効き {n['impact']}] {n['title']}: {n['done_when']}")
    return "\n".join(lines) + "\n"


def next_candidates(t: dict) -> list[dict]:
    nodes = [n for n in t["nodes"] if "id" in n]
    ch = children_of(nodes)
    leaves = [n for n in nodes if not ch[n["id"]] and n.get("status") in ("todo", "partial")]
    return sorted(leaves, key=lambda n: (IMPACTS.get(n.get("impact"), 9), n["status"] != "partial", n["id"]))


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "check"
    trees, recs = load_trees(), load_records()
    if cmd == "render":
        for name, t in trees.items():
            out = t["path"].parent / "TREE.md"
            out.write_text(render_tree(name, t, recs), encoding="utf-8")
            print(f"書き出し: {out.relative_to(ROOT).as_posix()}")
        return 0
    if cmd == "next":
        names = argv[2:] or list(trees)
        for name in names:
            print(f"== {name}")
            for n in next_candidates(trees[name]):
                print(f"{n['id']}\t{LABEL[n['status']]}\t{n['impact']}\t{n['title']}")
        return 0
    if cmd == "check":
        errs = check(trees, recs)
        for e in errs:
            print(e)
        if errs:
            print(f"作業の木: {len(errs)} 件の問題")
            return 1
        print(f"作業の木: 問題なし（木 {len(trees)} 件、記録 {len(recs)} 件）")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
