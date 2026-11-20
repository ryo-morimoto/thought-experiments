#!/usr/bin/env python3
"""思考実験の地図。2 つの軸（なるべく標準や論文の分類）で問いの空間を区切り、
どのセルが埋まっていて、次にどこを考えるべきかを出す。依存は標準ライブラリだけ（Python 3.11+）。

地図は <root>/maps/<name>/map.toml に書き（雛形: templates/map.toml）、map.html はそこから生成する。
<root> は既定で作業ディレクトリ。根拠（evidence）のパスも <root> からの相対で書く。

使い方:
    thought_map.py candidates maps/<name>        # 次に考える候補を番号付きで出す
    thought_map.py candidates maps/<name> --json
    thought_map.py render [maps/<name> ...]      # map.html を再生成（省略時は <root>/maps/ のすべて）
    thought_map.py check [maps/<name> ...]       # 形式の検査と、map.html が最新かの検査
    共通: --root <dir>

map.html は外部を読み込まない。データは <script type="application/json"> に入れ、
表示はすべて textContent で組み立てる（セルの文章に HTML が混じっても実行されない）。
"""

from __future__ import annotations

import argparse
import html
import json
import os
import sys
import tomllib
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path.cwd()  # main() が --root で上書きする
TOP = 6  # 順位を出す候補の数（map.html と candidates の既定）
# map.html の「コピー」で渡すコマンド（このリポジトリの skill）。
SKILL_COMMAND = "/thought-map"

# 状態 → (記号, 意味)。「埋まった」とみなすのは SETTLED だけ。
LEGEND_BY_STATUS = {
    "unexplored": ("·", "未探索（セルの記述がない）"),
    "open": ("?", "問いだけがある"),
    "hypothesis": ("△", "仮説はあるが裏付けがない"),
    "supported": ("◎", "根拠のある結論"),
    "refuted": ("✕", "仮説が否定された（否定されたこと自体が結論）"),
    "contested": ("!", "根拠が衝突している"),
    "out_of_scope": ("—", "この地図では扱わない（理由を claim に書く）"),
}
SETTLED = {"supported", "refuted"}
MODES = {"constructive", "destructive", "exploratory"}
BASES = {"standard", "paper", "own"}


@dataclass
class Candidate:
    """次に考える候補。target はセルなら "row/col"、軸なら "axis:rows" など。"""
    score: int
    kind: str
    target: str
    name: str
    why: str
    mode: str
    premises: list[str] = field(default_factory=list)  # 推論の前提にするセルの target


def rel(p: Path) -> str:
    """<root> からの相対パス（POSIX 形式）。"""
    return Path(os.path.relpath(p, ROOT)).as_posix()


# ---------- 読み込みと検査 ----------

def load(path: Path) -> dict:
    p = path / "map.toml" if path.is_dir() else path
    m = tomllib.loads(p.read_text(encoding="utf-8"))
    m["_path"] = p.resolve()
    m["_cells"] = {(c.get("row"), c.get("col")): c for c in m.get("cells", [])}
    return m


def validate(m: dict) -> list[str]:
    where = rel(m["_path"])
    errs = []
    for k in ("title", "question", "rows", "cols"):
        if k not in m:
            errs.append(f"{where}: {k} がない")
    if errs:
        return errs
    ids_by_axis = {}
    for ax in ("rows", "cols"):
        a = m[ax]
        for k in ("name", "basis", "ref", "values"):
            if k not in a:
                errs.append(f"{where}: [{ax}] に {k} がない")
        if a.get("basis") not in BASES:
            errs.append(f"{where}: [{ax}].basis は {sorted(BASES)} のどれか")
        vids = [v.get("id") for v in a.get("values", [])]
        if not vids or len(vids) != len(set(vids)) or None in vids or "" in vids:
            errs.append(f"{where}: [{ax}] の値がないか、id が欠けている・重複している")
        ids_by_axis[ax] = set(vids)
    if errs:
        return errs
    seen = set()
    for c in m.get("cells", []):
        target = (c.get("row"), c.get("col"))
        label = f"{where}: セル {target[0]}/{target[1]}"
        if target in seen:
            errs.append(f"{label} が重複している")
        seen.add(target)
        if target[0] not in ids_by_axis["rows"] or target[1] not in ids_by_axis["cols"]:
            errs.append(f"{label} の row/col が軸の値にない")
        st = c.get("status")
        if st not in LEGEND_BY_STATUS or st == "unexplored":
            errs.append(f"{label}: status は {sorted(set(LEGEND_BY_STATUS) - {'unexplored'})} のどれか")
        if st != "open" and not c.get("claim"):
            errs.append(f"{label}: open 以外は claim（結論・仮説・扱わない理由）を書く")
        if c.get("mode") and c["mode"] not in MODES:
            errs.append(f"{label}: mode は {sorted(MODES)} のどれか")
        for e in c.get("evidence", []):
            if "://" not in e and not (ROOT / e.split("#")[0]).exists():
                errs.append(f"{label}: 根拠 {e} が見つからない（--root {ROOT} からの相対で探した）")
    return errs


# ---------- 次に考える候補 ----------

def status(m: dict, r: str, c: str) -> str:
    return m["_cells"].get((r, c), {}).get("status", "unexplored")


def name(m: dict, ax: str, vid: str) -> str:
    return next(v["name"] for v in m[ax]["values"] if v["id"] == vid)


def candidates(m: dict) -> list[Candidate]:
    row_ids = [v["id"] for v in m["rows"]["values"]]
    col_ids = [v["id"] for v in m["cols"]["values"]]
    cands = []

    # 軸そのもの: 自作の分類だと、分類が見落としている値に気づけない
    for ax in ("rows", "cols"):
        a = m[ax]
        if a["basis"] == "own":
            cands.append(Candidate(75, "axis", f"axis:{ax}", f"軸「{a['name']}」の根拠を探す",
                                   "自作の分類なので、既存の標準・論文の分類と突き合わせると欠けている値が見つかる可能性がある",
                                   "exploratory"))
        elif not a.get("ref_read"):
            cands.append(Candidate(50, "axis", f"axis:{ax}", f"軸「{a['name']}」の出典を確認する",
                                   f"出典（{a['ref']}）の本文で値の定義をまだ確かめていない", "exploratory"))

    for r in row_ids:
        for c in col_ids:
            cell = m["_cells"].get((r, c), {})
            st = status(m, r, c)
            cell_name = f"{name(m, 'rows', r)} × {name(m, 'cols', c)}"
            target = f"{r}/{c}"
            if st == "contested":
                cands.append(Candidate(100, "cell", target, cell_name,
                                       f"根拠が衝突している（{cell['claim']}）。どの前提が違うのかを特定する", "destructive"))
            elif st == "hypothesis":
                cands.append(Candidate(80, "cell", target, cell_name,
                                       f"仮説「{cell['claim']}」に反例がないか。反例がなければ根拠を足して確定させる",
                                       "destructive"))
            elif st == "open":
                q = cell.get("next_question") or cell.get("claim") or "問いが置かれている"
                cands.append(Candidate(70, "cell", target, cell_name, f"問い「{q}」に答える", "constructive"))
            elif st in SETTLED and not cell.get("evidence"):
                cands.append(Candidate(65, "cell", target, cell_name,
                                       "結論に根拠が書かれていない。根拠を足すか、仮説に戻す", "destructive"))
            elif st == "unexplored":
                # 空のセル: 同じ行・列の結論から、どう推論すればよいかを出す
                in_row = [(cc, m["_cells"][(r, cc)]) for cc in col_ids if status(m, r, cc) in SETTLED]
                in_col = [(rr, m["_cells"][(rr, c)]) for rr in row_ids if status(m, rr, c) in SETTLED]
                score = 40 + 10 * min(len(in_row), 2) + 10 * min(len(in_col), 2)
                if in_row and in_col:
                    (cc, row_cell), (rr, col_cell) = in_row[0], in_col[0]
                    why = (f"同じ行の「{name(m, 'cols', cc)}」では「{row_cell['claim']}」、"
                           f"同じ列の「{name(m, 'rows', rr)}」では「{col_cell['claim']}」。"
                           "両方を前提にすると、このセルで何が言えるかを組み立てる")
                    cands.append(Candidate(score, "cell", target, cell_name, why, "constructive",
                                           [f"{r}/{cc}", f"{rr}/{c}"]))
                elif in_row or in_col:
                    ax, (vid, near) = ("cols", in_row[0]) if in_row else ("rows", in_col[0])
                    why = (f"隣の「{name(m, ax, vid)}」の結論「{near['claim']}」がここにも移るか。"
                           "移らないなら、何が違うせいかを条件を変えて探す")
                    mode = "destructive" if near["status"] == "supported" else "constructive"
                    cands.append(Candidate(score, "cell", target, cell_name, why, mode,
                                           [f"{r}/{vid}" if in_row else f"{vid}/{c}"]))
                else:
                    untouched = (all(status(m, r, cc) == "unexplored" for cc in col_ids)
                                 and all(status(m, rr, c) == "unexplored" for rr in row_ids))
                    why = (("行も列もまったく手がついていない" if untouched else "近くに結論がない")
                           + "。まず問いを立てて、何が起きうるかを広く出す")
                    cands.append(Candidate(score, "cell", target, cell_name, why, "exploratory"))

    cands.sort(key=lambda cand: -cand.score)  # 安定ソート: 同点は軸 → 行 → 列の順
    return cands


# ---------- map.html ----------

def render(m: dict) -> str:
    map_dir = m["_path"].parent
    keep = lambda d, ks: {k: d[k] for k in ks if k in d}  # noqa: E731
    axis = lambda a: {**keep(a, ("name", "basis", "ref", "ref_title", "ref_read", "note")),  # noqa: E731
                      "values": [keep(v, ("id", "name", "note")) for v in a["values"]]}
    up = Path(os.path.relpath(ROOT, map_dir)).as_posix()
    data = json.dumps({
        "title": m["title"], "question": m["question"], "map_dir": rel(map_dir),
        "up": "" if up == "." else up + "/",  # map.html から <root> への相対パス
        "skill_command": SKILL_COMMAND,
        "rows": axis(m["rows"]), "cols": axis(m["cols"]),
        "cells": [keep(c, ("row", "col", "status", "claim", "evidence", "mode", "next_question"))
                  for c in m.get("cells", [])],
        "legend_by_status": {k: list(v) for k, v in LEGEND_BY_STATUS.items()},
        "settled": sorted(SETTLED),
        "candidates": [asdict(cand) for cand in candidates(m)],
        "top": TOP,
    }, ensure_ascii=False, indent=1)
    return (TEMPLATE.replace("__TITLE__", html.escape(m["title"]))
            .replace("__DATA__", data.replace("</", "<\\/")))


# ---------- CLI ----------

def main(argv: list[str] | None = None) -> int:
    global ROOT
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path.cwd(), help="maps/ と根拠のパスの基点（既定: 作業ディレクトリ）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    cands_cli = sub.add_parser("candidates", help="次に考える候補")
    cands_cli.add_argument("map", type=Path)
    cands_cli.add_argument("--top", type=int, default=TOP)
    cands_cli.add_argument("--json", action="store_true")
    for cmd, h in (("render", "map.html を生成"), ("check", "形式と map.html の鮮度を検査")):
        sub.add_parser(cmd, help=h).add_argument("maps", type=Path, nargs="*")
    args = ap.parse_args(argv)
    ROOT = args.root.resolve()

    if args.cmd == "candidates":
        m = load(args.map.resolve())
        if errs := validate(m):
            print("\n".join(errs), file=sys.stderr)
            return 1
        cands = candidates(m)[: args.top]
        if args.json:
            print(json.dumps([asdict(cand) for cand in cands], ensure_ascii=False, indent=2))
        else:
            for i, cand in enumerate(cands, 1):
                print(f"{i}. [{cand.score}] {cand.name}  ({cand.target}, {cand.mode})\n   {cand.why}")
        return 0

    paths = ([path.resolve() for path in args.maps]
             or sorted(toml.parent for toml in (ROOT / "maps").glob("*/map.toml")))
    if not paths:
        print(f"地図がない（{ROOT / 'maps'}/*/map.toml）", file=sys.stderr)
        return 1
    errs = []
    for path in paths:
        m = load(path)
        if map_errs := validate(m):
            errs += map_errs
            continue
        page_file = m["_path"].parent / "map.html"
        page = render(m)
        if args.cmd == "render":
            page_file.write_text(page, encoding="utf-8")
            print(f"書き出し: {rel(page_file)}")
        elif not page_file.exists() or page_file.read_text(encoding="utf-8") != page:
            errs.append(f"{rel(page_file)} が map.toml と一致しない。render を実行する")
    if errs:
        print("\n".join(errs), file=sys.stderr)
        return 1
    if args.cmd == "check":
        print(f"地図 {len(paths)} 件: 問題なし")
    return 0


TEMPLATE = r"""<!doctype html>
<!-- thought_map.py render で map.toml から生成。直接編集しない -->
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root {
  --bg: #f7f6f2; --paper: #ffffff; --ink: #1d1d1b; --sub: #6b6a64; --line: #dcd9d0; --out_of_scope: #dcd9d0;
  --supported: #2f7d6d; --supported-bg: #dcefe9; --refuted: #7a5c58; --refuted-bg: #ece3e1;
  --hypothesis: #b07a12; --hypothesis-bg: #f8ecd2; --open: #b07a12; --contested: #c0392b; --contested-bg: #f7dcd8;
  --unexplored: #b9b5aa; --focus: #3b5bdb; --focus-bg: #e5eafd; --premise: #7048e8;
  --mono: ui-monospace, SFMono-Regular, Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #161614; --paper: #1f1f1c; --ink: #ecebe6; --sub: #a3a198; --line: #3a3934; --out_of_scope: #3a3934;
    --supported: #6cc3ad; --supported-bg: #1f3a33; --refuted: #c9a8a2; --refuted-bg: #3a2d2b;
    --hypothesis: #e2b453; --hypothesis-bg: #3d3220; --open: #e2b453; --contested: #ff8a7a; --contested-bg: #4a2522;
    --unexplored: #5d5b54; --focus: #8ea2ff; --focus-bg: #262d4d; --premise: #b197fc;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
  font: 15px/1.6 system-ui, -apple-system, "Hiragino Sans", "Noto Sans JP", sans-serif; }
a { color: var(--focus); }
header { padding: 28px 32px 8px; max-width: 1400px; margin: 0 auto; }
.eyebrow { font-size: 12px; letter-spacing: .08em; color: var(--sub); }
h1 { font-size: 24px; margin: 4px 0 6px; }
.question { font-size: 17px; margin: 0 0 16px; }
.question::before { content: "問い "; color: var(--sub); font-size: 13px; }
.progress { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
.bar { display: flex; height: 10px; width: min(420px, 100%); border-radius: 5px; overflow: hidden; background: var(--line); }
.bar span { display: block; height: 100%; }
.progress .count { font-size: 14px; }
.progress .count b { font-size: 20px; }
.legend { display: flex; gap: 12px; flex-wrap: wrap; font-size: 12px; color: var(--sub); }
.legend i { display: inline-block; width: 14px; height: 14px; vertical-align: -2px; margin-right: 4px; border-radius: 3px; }

main { display: grid; grid-template-columns: minmax(0, 1fr) 380px; gap: 24px; padding: 16px 32px 40px; max-width: 1400px; margin: 0 auto; }
@media (max-width: 1000px) { main { grid-template-columns: 1fr; } }
section.panel { background: var(--paper); border: 1px solid var(--line); border-radius: 10px; padding: 18px; }
h2 { font-size: 14px; margin: 0 0 12px; color: var(--sub); font-weight: 600; letter-spacing: .04em; }

/* 軸 */
.axis-card { display: flex; gap: 10px; align-items: baseline; flex-wrap: wrap; margin-bottom: 8px; font-size: 13px; }
.axis-card .side { color: var(--sub); width: 2em; }
.axis-card .name { font-weight: 600; }
.chip { font-size: 11px; padding: 1px 8px; border-radius: 999px; border: 1px solid currentColor; white-space: nowrap; }
.chip.standard, .chip.paper { color: var(--supported); }
.chip.own { color: var(--hypothesis); border-style: dashed; }
.chip.unread { color: var(--sub); border-style: dotted; }
.axis-card.flag { cursor: pointer; }
.axis-card.selected { outline: 2px solid var(--focus); outline-offset: 3px; border-radius: 4px; }

/* 地図 */
.grid { display: grid; gap: 6px; margin-top: 14px; }
.colhead, .rowhead { font-size: 13px; font-weight: 600; padding: 6px 8px; display: flex; flex-direction: column; justify-content: center; }
.colhead { text-align: center; align-items: center; border-bottom: 2px solid var(--line); }
.rowhead { border-right: 2px solid var(--line); }
.rowhead.head-own { border-right-style: dashed; border-right-color: var(--hypothesis); }
.colhead.head-own { border-bottom-style: dashed; border-bottom-color: var(--hypothesis); }
.tally { font-size: 11px; color: var(--sub); font-weight: 400; }
.corner { font-size: 11px; color: var(--sub); display: flex; align-items: flex-end; padding: 6px; }

.cell { position: relative; min-height: 96px; border-radius: 8px; padding: 9px 10px 8px; cursor: pointer;
  border: 1.5px solid transparent; transition: opacity .15s, transform .15s; font-size: 12.5px; overflow: hidden; }
.cell:hover { transform: translateY(-1px); }
.cell .glyph { font-size: 18px; font-weight: 700; line-height: 1; }
.cell .text { margin-top: 6px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.cell.supported { background: var(--supported-bg); border-color: var(--supported); color: var(--ink); }
.cell.supported .glyph { color: var(--supported); }
.cell.refuted { background: var(--refuted-bg); border-color: var(--refuted); }
.cell.refuted .glyph { color: var(--refuted); }
.cell.hypothesis { border-color: var(--hypothesis);
  background: repeating-linear-gradient(135deg, var(--hypothesis-bg) 0 8px, var(--paper) 8px 14px); }
.cell.hypothesis .glyph { color: var(--hypothesis); }
.cell.contested { border-color: var(--contested);
  background: repeating-linear-gradient(45deg, var(--contested-bg) 0 6px, var(--paper) 6px 12px); }
.cell.contested .glyph { color: var(--contested); }
.cell.open { border: 2px dashed var(--open); background: var(--paper); }
.cell.open .glyph { color: var(--open); }
.cell.unexplored { border: 1.5px dashed var(--unexplored); background: transparent; color: var(--sub); }
.cell.unexplored .glyph { color: var(--unexplored); }
.cell.out_of_scope { background: var(--out_of_scope); color: var(--sub); }

.rank { position: absolute; top: 7px; right: 8px; width: 22px; height: 22px; border-radius: 50%;
  background: var(--focus); color: #fff; font-size: 12px; font-weight: 700; display: grid; place-items: center; }
.grid.focusing .cell { opacity: .35; }
.grid.focusing .cell.chosen, .grid.focusing .cell.premise { opacity: 1; }
.cell.chosen { box-shadow: 0 0 0 3px var(--focus); }
.cell.premise { box-shadow: 0 0 0 3px var(--premise); }
.cell.premise::after { content: "前提"; position: absolute; top: 8px; left: 32px; font-size: 10px;
  color: #fff; background: var(--premise); padding: 0 6px; border-radius: 4px; }

/* 次に考える候補 */
.cands { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }
.cand { border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; cursor: pointer; display: grid;
  grid-template-columns: 26px 1fr; gap: 2px 8px; }
.cand:hover { border-color: var(--focus); }
.cand.selected { border-color: var(--focus); background: var(--focus-bg); }
.cand .n { grid-row: span 2; width: 22px; height: 22px; border-radius: 50%; background: var(--focus); color: #fff;
  font-size: 12px; font-weight: 700; display: grid; place-items: center; }
.cand.k-axis .n { background: var(--hypothesis); }
.cand .t { font-weight: 600; font-size: 13.5px; }
.cand .meta { font-size: 12px; color: var(--sub); }
.mode { font-size: 11px; padding: 1px 7px; border-radius: 4px; background: var(--line); color: var(--ink); margin-right: 6px; }

.detail { margin-top: 16px; border-top: 1px solid var(--line); padding-top: 14px; font-size: 13.5px; }
.detail h3 { font-size: 15px; margin: 0 0 6px; }
.detail .why { background: var(--focus-bg); border-left: 3px solid var(--focus); padding: 8px 10px; border-radius: 4px; margin: 8px 0; }
.detail .claim { margin: 8px 0; }
.detail ul { padding-left: 18px; margin: 6px 0; }
.cmd { display: flex; gap: 6px; margin-top: 10px; }
.cmd code { flex: 1; font: 12px var(--mono); background: var(--bg); border: 1px solid var(--line); border-radius: 6px; padding: 7px 9px; overflow-x: auto; white-space: nowrap; }
.cmd button { font: inherit; font-size: 12px; border: 1px solid var(--focus); background: var(--focus); color: #fff; border-radius: 6px; padding: 0 12px; cursor: pointer; }
.hint { font-size: 12px; color: var(--sub); margin-top: 10px; }
.muted { color: var(--sub); }
</style>
</head>
<body>
<script type="application/json" id="data">
__DATA__
</script>
<header>
  <div class="eyebrow">思考実験の地図 · <span id="map-dir"></span></div>
  <h1 id="title"></h1>
  <p class="question" id="question"></p>
  <div class="progress">
    <div class="bar" id="bar"></div>
    <div class="count" id="count"></div>
    <div class="legend" id="legend"></div>
  </div>
</header>
<main>
  <section class="panel">
    <h2>どこまで分かっているか</h2>
    <div id="axes"></div>
    <div class="grid" id="grid"></div>
  </section>
  <section class="panel">
    <h2>次に考える候補 — 選ぶと、推論の前提になるセルが光る</h2>
    <ol class="cands" id="cands"></ol>
    <div class="detail" id="detail"></div>
  </section>
</main>
<script>
const D = JSON.parse(document.getElementById("data").textContent);
const $ = (id) => document.getElementById(id);
const el = (tag, cls, text) => { const node = document.createElement(tag); if (cls) node.className = cls; if (text != null) node.textContent = text; return node; };
const labelByMode = { constructive: "組み立てる", destructive: "崩す（反例探し）", exploratory: "広げる" };
const SETTLED = new Set(D.settled);
const cellOf = (r, c) => D.cells.find((cell) => cell.row === r && cell.col === c) || { row: r, col: c, status: "unexplored" };
const nameOf = (ax, id) => D[ax].values.find((v) => v.id === id).name;
const link = (p) => { const anchor = el("a", null, p); anchor.href = p.includes("://") ? p : D.up + p; return anchor; };

$("map-dir").textContent = D.map_dir;
$("title").textContent = D.title;
$("question").textContent = D.question;

// 進み具合
const gridCells = D.rows.values.flatMap((r) => D.cols.values.map((c) => cellOf(r.id, c.id)));
const countByStatus = {};
gridCells.forEach((cell) => countByStatus[cell.status] = (countByStatus[cell.status] || 0) + 1);
["supported", "refuted", "contested", "hypothesis", "open", "out_of_scope", "unexplored"].forEach((s) => {
  if (!countByStatus[s]) return;
  const seg = el("span"); seg.style.width = (100 * countByStatus[s] / gridCells.length) + "%";
  seg.style.background = `var(--${s})`; seg.title = `${D.legend_by_status[s][1]}: ${countByStatus[s]}`; $("bar").append(seg);
});
const settledCount = gridCells.filter((cell) => SETTLED.has(cell.status)).length;
$("count").append(el("b", null, `${settledCount}`), ` / ${gridCells.length} セルに結論 · 未探索 ${countByStatus.unexplored || 0}`);
Object.entries(D.legend_by_status).forEach(([s, [glyph, meaning]]) => {
  const item = el("span"); const sw = el("i"); sw.style.background = `var(--${s})`;
  if (s === "unexplored" || s === "open") { sw.style.background = "transparent"; sw.style.border = `1.5px dashed var(--${s})`; }
  item.append(sw, `${glyph} ${meaning.split("（")[0]}`); $("legend").append(item);
});

// 軸
const cardByAxis = {};
[["rows", "行"], ["cols", "列"]].forEach(([ax, label]) => {
  const a = D[ax];
  const card = el("div", "axis-card");
  card.append(el("span", "side", label), el("span", "name", a.name));
  card.append(el("span", "chip " + a.basis, { standard: "標準", paper: "論文", own: "自作の分類" }[a.basis]));
  if (!a.ref_read) card.append(el("span", "chip unread", "出典は未確認"));
  const cite = el("span", "muted"); cite.append("出典: ", link(a.ref)); if (a.ref_title) cite.lastChild.textContent = a.ref_title;
  card.append(cite);
  $("axes").append(card); cardByAxis[ax] = card;
});

// 地図
const grid = $("grid");
grid.style.gridTemplateColumns = `minmax(110px, 160px) repeat(${D.cols.values.length}, minmax(120px, 1fr))`;
grid.append(el("div", "corner", `${D.rows.name} ＼ ${D.cols.name}`));
D.cols.values.forEach((c) => {
  const h = el("div", "colhead" + (D.cols.basis === "own" ? " head-own" : ""), c.name);
  const n = D.rows.values.filter((r) => SETTLED.has(cellOf(r.id, c.id).status)).length;
  h.append(el("span", "tally", `${n}/${D.rows.values.length}`)); if (c.note) h.title = c.note;
  grid.append(h);
});
const rankByTarget = {};
D.candidates.forEach((cand, i) => { if (cand.kind === "cell" && rankByTarget[cand.target] == null && i < D.top) rankByTarget[cand.target] = i + 1; });
const nodeByTarget = {};
D.rows.values.forEach((r) => {
  const h = el("div", "rowhead" + (D.rows.basis === "own" ? " head-own" : ""), r.name);
  const n = D.cols.values.filter((c) => SETTLED.has(cellOf(r.id, c.id).status)).length;
  h.append(el("span", "tally", `${n}/${D.cols.values.length}`)); if (r.note) h.title = r.note;
  grid.append(h);
  D.cols.values.forEach((c) => {
    const cell = cellOf(r.id, c.id); const target = `${r.id}/${c.id}`;
    const node = el("div", "cell " + cell.status);
    node.append(el("div", "glyph", D.legend_by_status[cell.status][0]));
    node.append(el("div", "text", cell.claim || cell.next_question || (cell.status === "unexplored" ? "まだ誰も考えていない" : "")));
    if (rankByTarget[target]) node.append(el("div", "rank", rankByTarget[target]));
    node.onclick = () => select(D.candidates.findIndex((cand) => cand.target === target), target);
    grid.append(node); nodeByTarget[target] = node;
  });
});

// 次に考える候補
D.candidates.slice(0, D.top).forEach((cand, i) => {
  const li = el("li", "cand k-" + cand.kind);
  li.append(el("span", "n", i + 1), el("span", "t", cand.name));
  const meta = el("span", "meta"); meta.append(el("span", "mode", labelByMode[cand.mode]), cand.kind === "axis" ? "軸を見直す" : cand.target);
  li.append(meta); li.onclick = () => select(i); $("cands").append(li);
});

function select(i, target) {
  const cand = i >= 0 ? D.candidates[i] : null;
  target = target || (cand && cand.target);
  document.querySelectorAll(".cand").forEach((node, j) => node.classList.toggle("selected", j === i));
  Object.values(nodeByTarget).forEach((node) => node.classList.remove("chosen", "premise"));
  Object.values(cardByAxis).forEach((node) => node.classList.remove("selected"));
  grid.classList.remove("focusing");
  if (cand && cand.kind === "axis") cardByAxis[target.split(":")[1]].classList.add("selected");
  else if (target) {
    grid.classList.add("focusing"); nodeByTarget[target].classList.add("chosen");
    (cand ? cand.premises : []).forEach((premise) => nodeByTarget[premise] && nodeByTarget[premise].classList.add("premise"));
  }
  const d = $("detail"); d.replaceChildren();
  if (target && !target.startsWith("axis:")) {
    const [r, c] = target.split("/"); const cell = cellOf(r, c);
    d.append(el("h3", null, `${D.legend_by_status[cell.status][0]} ${nameOf("rows", r)} × ${nameOf("cols", c)}`));
    d.append(el("div", "muted", D.legend_by_status[cell.status][1]));
    if (cell.claim) d.append(el("p", "claim", cell.claim));
    if (cell.next_question) d.append(el("p", null, "次の問い: " + cell.next_question));
    if (cell.evidence && cell.evidence.length) {
      const ul = el("ul"); cell.evidence.forEach((p) => { const li = el("li", null, "根拠: "); li.append(link(p)); ul.append(li); }); d.append(ul);
    }
  } else if (cand) d.append(el("h3", null, cand.name));
  if (cand) {
    const box = el("div", "why"); box.append(el("span", "mode", labelByMode[cand.mode]), cand.why); d.append(box);
    const cmd = el("div", "cmd"); const code = el("code", null, `${D.skill_command} ${D.map_dir} ${cand.target}`);
    const btn = el("button", null, "コピー");
    btn.onclick = () => navigator.clipboard.writeText(code.textContent).then(() => { btn.textContent = "コピーした"; setTimeout(() => btn.textContent = "コピー", 1200); });
    cmd.append(code, btn); d.append(cmd);
    d.append(el("div", "hint", "Claude Code に貼ると、この候補から思考実験を始める。"));
  } else if (target) d.append(el("div", "hint", "このセルは今の候補に入っていない。考えたいなら Claude Code で " + D.skill_command + " " + D.map_dir + " " + target));
}
document.addEventListener("keydown", (e) => {
  const n = parseInt(e.key, 10); if (n >= 1 && n <= Math.min(9, D.top)) select(n - 1);
  if (e.key === "Escape") select(-1);
});
// map.html#3 で 3 番目の候補を選んだ状態で開く
const fromHash = parseInt(location.hash.slice(1), 10);
select(fromHash >= 1 && fromHash <= D.top ? fromHash - 1 : 0);
window.addEventListener("hashchange", () => { const n = parseInt(location.hash.slice(1), 10); if (n >= 1) select(n - 1); });
</script>
</body>
</html>
"""


if __name__ == "__main__":
    sys.exit(main())
