"""思考実験の地図の HTML（thought_map.py から使う）。外部の読み込みはしない。

データは <script type="application/json"> に入れ、表示はすべて textContent で組み立てる
（セルの文章に HTML が混じっても実行されない）。
"""

from __future__ import annotations

import html
import json


def page(data: dict) -> str:
    payload = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return (TEMPLATE.replace("__TITLE__", html.escape(data["title"]))
            .replace("__DATA__", payload))


TEMPLATE = r"""<!doctype html>
<!-- tools/thought_map.py render で map.toml から生成。直接編集しない -->
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root {
  --bg: #f7f6f2; --paper: #ffffff; --ink: #1d1d1b; --sub: #6b6a64; --line: #dcd9d0;
  --known: #2f7d6d; --known-bg: #dcefe9; --refuted: #7a5c58; --refuted-bg: #ece3e1;
  --hypo: #b07a12; --hypo-bg: #f8ecd2; --open: #b07a12; --conflict: #c0392b; --conflict-bg: #f7dcd8;
  --void: #b9b5aa; --focus: #3b5bdb; --focus-bg: #e5eafd; --premise: #7048e8;
  --mono: ui-monospace, SFMono-Regular, Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #161614; --paper: #1f1f1c; --ink: #ecebe6; --sub: #a3a198; --line: #3a3934;
    --known: #6cc3ad; --known-bg: #1f3a33; --refuted: #c9a8a2; --refuted-bg: #3a2d2b;
    --hypo: #e2b453; --hypo-bg: #3d3220; --open: #e2b453; --conflict: #ff8a7a; --conflict-bg: #4a2522;
    --void: #5d5b54; --focus: #8ea2ff; --focus-bg: #262d4d; --premise: #b197fc;
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
.axis-card .dir { color: var(--sub); width: 2em; }
.axis-card .name { font-weight: 600; }
.chip { font-size: 11px; padding: 1px 8px; border-radius: 999px; border: 1px solid currentColor; white-space: nowrap; }
.chip.standard, .chip.paper { color: var(--known); }
.chip.own { color: var(--hypo); border-style: dashed; }
.chip.unchecked { color: var(--sub); border-style: dotted; }
.axis-card.flag { cursor: pointer; }
.axis-card.selected { outline: 2px solid var(--focus); outline-offset: 3px; border-radius: 4px; }

/* 地図 */
.grid { display: grid; gap: 6px; margin-top: 14px; }
.colhead, .rowhead { font-size: 13px; font-weight: 600; padding: 6px 8px; display: flex; flex-direction: column; justify-content: center; }
.colhead { text-align: center; align-items: center; border-bottom: 2px solid var(--line); }
.rowhead { border-right: 2px solid var(--line); }
.rowhead.head-own { border-right-style: dashed; border-right-color: var(--hypo); }
.colhead.head-own { border-bottom-style: dashed; border-bottom-color: var(--hypo); }
.tally { font-size: 11px; color: var(--sub); font-weight: 400; }
.corner { font-size: 11px; color: var(--sub); display: flex; align-items: flex-end; padding: 6px; }

.cell { position: relative; min-height: 96px; border-radius: 8px; padding: 9px 10px 8px; cursor: pointer;
  border: 1.5px solid transparent; transition: opacity .15s, transform .15s; font-size: 12.5px; overflow: hidden; }
.cell:hover { transform: translateY(-1px); }
.cell .glyph { font-size: 18px; font-weight: 700; line-height: 1; }
.cell .text { margin-top: 6px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.cell.supported { background: var(--known-bg); border-color: var(--known); color: var(--ink); }
.cell.supported .glyph { color: var(--known); }
.cell.refuted { background: var(--refuted-bg); border-color: var(--refuted); }
.cell.refuted .glyph { color: var(--refuted); }
.cell.hypothesis { border-color: var(--hypo);
  background: repeating-linear-gradient(135deg, var(--hypo-bg) 0 8px, var(--paper) 8px 14px); }
.cell.hypothesis .glyph { color: var(--hypo); }
.cell.contested { border-color: var(--conflict);
  background: repeating-linear-gradient(45deg, var(--conflict-bg) 0 6px, var(--paper) 6px 12px); }
.cell.contested .glyph { color: var(--conflict); }
.cell.open { border: 2px dashed var(--open); background: var(--paper); }
.cell.open .glyph { color: var(--open); }
.cell.unexplored { border: 1.5px dashed var(--void); background: transparent; color: var(--sub); }
.cell.unexplored .glyph { color: var(--void); }
.cell.out_of_scope { background: var(--line); color: var(--sub); }

.rank { position: absolute; top: 7px; right: 8px; width: 22px; height: 22px; border-radius: 50%;
  background: var(--focus); color: #fff; font-size: 12px; font-weight: 700; display: grid; place-items: center; }
.grid.focusing .cell { opacity: .35; }
.grid.focusing .cell.target, .grid.focusing .cell.premise { opacity: 1; }
.cell.target { box-shadow: 0 0 0 3px var(--focus); }
.cell.premise { box-shadow: 0 0 0 3px var(--premise); }
.cell.premise::after { content: "前提"; position: absolute; top: 8px; left: 32px; font-size: 10px;
  color: #fff; background: var(--premise); padding: 0 6px; border-radius: 4px; }

/* 次の一手 */
.cands { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }
.cand { border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; cursor: pointer; display: grid;
  grid-template-columns: 26px 1fr; gap: 2px 8px; }
.cand:hover { border-color: var(--focus); }
.cand.selected { border-color: var(--focus); background: var(--focus-bg); }
.cand .n { grid-row: span 2; width: 22px; height: 22px; border-radius: 50%; background: var(--focus); color: #fff;
  font-size: 12px; font-weight: 700; display: grid; place-items: center; }
.cand.k-axis .n { background: var(--hypo); }
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
  <div class="eyebrow">思考実験の地図 · <span id="mapdir"></span></div>
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
    <h2>次の一手 — 選ぶと、推論の前提になるセルが光る</h2>
    <ol class="cands" id="cands"></ol>
    <div class="detail" id="detail"></div>
  </section>
</main>
<script>
const D = JSON.parse(document.getElementById("data").textContent);
const $ = (id) => document.getElementById(id);
const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
const MODE = { constructive: "組み立てる", destructive: "崩す（反例探し）", exploratory: "広げる" };
const COLOR = { supported: "--known", refuted: "--refuted", hypothesis: "--hypo", contested: "--conflict", open: "--open", unexplored: "--void", out_of_scope: "--line" };
const SETTLED = new Set(D.settled);
const cellOf = (r, c) => D.cells.find((x) => x.row === r && x.col === c) || { row: r, col: c, status: "unexplored" };
const nameOf = (ax, id) => D[ax].values.find((v) => v.id === id).name;
const link = (p) => { const a = el("a", null, p); a.href = p.includes("://") ? p : D.up + p; return a; };

$("mapdir").textContent = D.dir;
$("title").textContent = D.title;
$("question").textContent = D.question;

// 進み具合
const all = D.rows.values.flatMap((r) => D.cols.values.map((c) => cellOf(r.id, c.id)));
const counts = {};
all.forEach((x) => counts[x.status] = (counts[x.status] || 0) + 1);
["supported", "refuted", "contested", "hypothesis", "open", "out_of_scope", "unexplored"].forEach((s) => {
  if (!counts[s]) return;
  const seg = el("span"); seg.style.width = (100 * counts[s] / all.length) + "%";
  seg.style.background = `var(${COLOR[s]})`; seg.title = `${D.status[s][1]}: ${counts[s]}`; $("bar").append(seg);
});
const settled = all.filter((x) => SETTLED.has(x.status)).length;
$("count").append(el("b", null, `${settled}`), ` / ${all.length} セルに結論 · 未探索 ${counts.unexplored || 0}`);
Object.entries(D.status).forEach(([s, [g, d]]) => {
  const item = el("span"); const sw = el("i"); sw.className = ""; sw.style.background = `var(${COLOR[s]})`;
  if (s === "unexplored" || s === "open") { sw.style.background = "transparent"; sw.style.border = `1.5px dashed var(${COLOR[s]})`; }
  item.append(sw, `${g} ${d.split("（")[0]}`); $("legend").append(item);
});

// 軸
const axisCards = {};
[["rows", "行"], ["cols", "列"]].forEach(([ax, dir]) => {
  const a = D[ax];
  const card = el("div", "axis-card");
  card.append(el("span", "dir", dir), el("span", "name", a.name));
  card.append(el("span", "chip " + a.basis, { standard: "標準", paper: "論文", own: "自作の分類" }[a.basis]));
  if (!a.checked) card.append(el("span", "chip unchecked", "出典は未確認"));
  const ref = el("span", "muted"); ref.append("出典: ", link(a.ref)); if (a.ref_title) ref.lastChild.textContent = a.ref_title;
  card.append(ref);
  $("axes").append(card); axisCards[ax] = card;
});

// 地図
const grid = $("grid");
grid.style.gridTemplateColumns = `minmax(110px, 160px) repeat(${D.cols.values.length}, minmax(120px, 1fr))`;
const corner = el("div", "corner", `${D.rows.name} ＼ ${D.cols.name}`); grid.append(corner);
const heads = { rows: [], cols: [] };
D.cols.values.forEach((c) => {
  const h = el("div", "colhead" + (D.cols.basis === "own" ? " head-own" : ""), c.name);
  const n = D.rows.values.filter((r) => SETTLED.has(cellOf(r.id, c.id).status)).length;
  h.append(el("span", "tally", `${n}/${D.rows.values.length}`)); if (c.note) h.title = c.note;
  grid.append(h); heads.cols.push(h);
});
const rankOf = {};
D.frontier.forEach((o, i) => { if (o.kind === "cell" && rankOf[o.target] == null && i < D.top) rankOf[o.target] = i + 1; });
const cellEls = {};
D.rows.values.forEach((r) => {
  const h = el("div", "rowhead" + (D.rows.basis === "own" ? " head-own" : ""), r.name);
  const n = D.cols.values.filter((c) => SETTLED.has(cellOf(r.id, c.id).status)).length;
  h.append(el("span", "tally", `${n}/${D.cols.values.length}`)); if (r.note) h.title = r.note;
  grid.append(h); heads.rows.push(h);
  D.cols.values.forEach((c) => {
    const x = cellOf(r.id, c.id); const key = `${r.id}/${c.id}`;
    const e = el("div", "cell " + x.status);
    e.append(el("div", "glyph", D.status[x.status][0]));
    e.append(el("div", "text", x.claim || x.next || (x.status === "unexplored" ? "まだ誰も考えていない" : "")));
    if (rankOf[key]) e.append(el("div", "rank", rankOf[key]));
    e.onclick = () => select(D.frontier.findIndex((o) => o.target === key), key);
    grid.append(e); cellEls[key] = e;
  });
});

// 次の一手
D.frontier.slice(0, D.top).forEach((o, i) => {
  const li = el("li", "cand k-" + o.kind);
  li.append(el("span", "n", i + 1), el("span", "t", o.title));
  const meta = el("span", "meta"); meta.append(el("span", "mode", MODE[o.mode]), o.kind === "axis" ? "軸を見直す" : o.target);
  li.append(meta); li.onclick = () => select(i); $("cands").append(li);
});

function select(i, key) {
  const o = i >= 0 ? D.frontier[i] : null;
  key = key || (o && o.target);
  document.querySelectorAll(".cand").forEach((x, j) => x.classList.toggle("selected", j === i));
  Object.values(cellEls).forEach((x) => x.classList.remove("target", "premise"));
  Object.values(axisCards).forEach((x) => x.classList.remove("selected"));
  grid.classList.remove("focusing");
  if (o && o.kind === "axis") axisCards[o.target.split(":")[1]].classList.add("selected");
  else if (key) {
    grid.classList.add("focusing"); cellEls[key].classList.add("target");
    (o ? o.sources : []).forEach((s) => cellEls[s] && cellEls[s].classList.add("premise"));
  }
  const d = $("detail"); d.replaceChildren();
  if (key && !key.startsWith("axis:")) {
    const [r, c] = key.split("/"); const x = cellOf(r, c);
    d.append(el("h3", null, `${D.status[x.status][0]} ${nameOf("rows", r)} × ${nameOf("cols", c)}`));
    d.append(el("div", "muted", D.status[x.status][1]));
    if (x.claim) d.append(el("p", "claim", x.claim));
    if (x.next) d.append(el("p", null, "次の問い: " + x.next));
    if (x.evidence && x.evidence.length) {
      const ul = el("ul"); x.evidence.forEach((p) => { const li = el("li", null, "根拠: "); li.append(link(p)); ul.append(li); }); d.append(ul);
    }
  } else if (o) d.append(el("h3", null, o.title));
  if (o) {
    const why = el("div", "why"); why.append(el("span", "mode", MODE[o.mode]), o.why); d.append(why);
    const cmd = el("div", "cmd"); const code = el("code", null, `/thought-map ${D.dir} ${o.target}`);
    const btn = el("button", null, "コピー");
    btn.onclick = () => navigator.clipboard.writeText(code.textContent).then(() => { btn.textContent = "コピーした"; setTimeout(() => btn.textContent = "コピー", 1200); });
    cmd.append(code, btn); d.append(cmd);
    d.append(el("div", "hint", "Claude Code に貼ると、この候補から思考実験を始める。"));
  } else if (key) d.append(el("div", "hint", "このセルは今の候補に入っていない。考えたいなら Claude Code で /thought-map " + D.dir + " " + key));
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
