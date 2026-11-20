"""自作物のテキストファイルに埋め込まれたデータを検出する（check_data_policy.py から使う）。

ファイルの形をしていないデータ（Markdown の表、コード中の数値リスト、貼り付けた CSV）は、
ファイル単位の宣言をすり抜ける。ここでは「データらしい塊」を見つけ、出所の印を要求する。

  自作のデータ:  塊の直前（3 行以内）に `data-source: original` と書く
  外部のデータ:  SPDX スニペットで囲み、中に `data-source: <SOURCE.toml の id>` と書く

REUSE-IgnoreStart（以下は例。REUSE とこの検査の両方に読み飛ばさせる）
      <!-- SPDX-SnippetBegin -->
      <!-- SPDX-SnippetCopyrightText: 江戸川区 -->
      <!-- SPDX-License-Identifier: CC-BY-4.0 -->
      <!-- data-source: edogawa-carpark -->
      出典：江戸川区「公営駐車場一覧」…（SOURCE.toml の attribution をそのまま書く）
      | 名称 | 台数 |
      ...
      <!-- SPDX-SnippetEnd -->
REUSE-IgnoreEnd

検出は経験則なので、小さな表や文中の数値は対象外（事実としての数値は著作物でないことが多い）。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# REUSE はソース中のタグ文字列そのものを宣言として読むので、連結して組み立てる
_SPDX = "SPDX-"
TAG_BEGIN, TAG_END = _SPDX + "SnippetBegin", _SPDX + "SnippetEnd"
TAG_LICENSE = _SPDX + "License-Identifier"
IGNORE_START, IGNORE_END = "REUSE-" + "IgnoreStart", "REUSE-" + "IgnoreEnd"
MARKER = re.compile(r"data-source:\s*([A-Za-z0-9_.-]+)")
NUMBER = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.])")


@dataclass
class Snippet:
    start: int
    end: int
    text: str
    licenses: list[str] = field(default_factory=list)
    source: str | None = None


def ignored_lines(lines: list[str]) -> set[int]:
    """REUSE の無視区間（IgnoreStart〜IgnoreEnd）の行。REUSE と同じく読み飛ばす。"""
    out, on = set(), False
    for i, line in enumerate(lines):
        if IGNORE_START in line:
            on = True
        if on:
            out.add(i)
        if IGNORE_END in line:
            on = False
    return out


def find_snippets(lines: list[str]) -> list[Snippet]:
    out, cur = [], None
    skip = ignored_lines(lines)
    for i, line in enumerate(lines):
        if i in skip:
            continue
        if TAG_BEGIN in line:
            cur = Snippet(start=i, end=len(lines) - 1, text="")
        elif TAG_END in line and cur:
            cur.end = i
            cur.text = "\n".join(lines[cur.start:i + 1])
            cur.licenses = re.findall(TAG_LICENSE + r":\s*([^\s>*-][^\s>*]*)", cur.text)
            m = MARKER.search(cur.text)
            cur.source = m.group(1) if m else None
            out.append(cur)
            cur = None
    return out


def _runs(flags: list[bool]) -> list[tuple[int, int]]:
    runs, start = [], None
    for i, f in enumerate(flags + [False]):
        if f and start is None:
            start = i
        elif not f and start is not None:
            runs.append((start, i - 1))
            start = None
    return runs


def _numeric(line: str) -> bool:
    s = line.strip()
    body = re.sub(r"\s", "", s)
    if not body:
        return False
    digits = sum(c.isdigit() for c in body)
    return len(NUMBER.findall(s)) >= 3 and digits / len(body) >= 0.5


def _delimited(line: str) -> tuple[str, int] | None:
    for d in ("\t", ","):
        n = line.count(d)
        if n >= 2:
            return (d, n)
    return None


def find_blocks(lines: list[str], min_rows: int, min_numbers: int) -> list[tuple[int, int, str]]:
    """データらしい塊の (開始行, 終了行, 種類)。行番号は 0 始まり。"""
    blocks = []
    table = [ln.lstrip().startswith("|") for ln in lines]
    for s, e in _runs(table):
        rows = [ln for ln in lines[s:e + 1] if not re.fullmatch(r"\s*\|[\s:|-]*\|?\s*", ln)]
        if len(rows) >= min_rows:
            blocks.append((s, e, "Markdown の表"))
    for s, e in _runs([_numeric(ln) for ln in lines]):
        if e - s + 1 >= min_rows:
            blocks.append((s, e, "数値の並び"))
    shape = [_delimited(ln) for ln in lines]
    i = 0
    while i < len(lines):
        j = i
        while j + 1 < len(lines) and shape[i] and shape[j + 1] == shape[i]:
            j += 1
        if shape[i] and j - i + 1 >= min_rows and not table[i]:
            blocks.append((i, j, "区切り文字の揃った行（CSV/TSV）"))
        i = j + 1
    for i, ln in enumerate(lines):
        if len(NUMBER.findall(ln)) >= min_numbers:
            blocks.append((i, i, f"1 行に {len(NUMBER.findall(ln))} 個の数値"))
    return blocks


def scan(path: str, data: bytes, sources: dict, licenses: dict, cfg: dict) -> list[str]:
    """1 ファイルを検査し、エラーメッセージのリストを返す。"""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return [f"{path}: UTF-8 のテキストでない。自作物の拡張子でバイナリを置かない（データなら SOURCE.toml の管轄に移す）"]
    lines = text.splitlines()
    snippets = find_snippets(lines)
    errs = []

    for sn in snippets:
        errs += _check_snippet(path, sn, sources, licenses)

    skip = ignored_lines(lines)
    for s, e, kind in find_blocks(lines, cfg.get("min_rows", 10), cfg.get("min_numbers", 50)):
        if s in skip:
            continue
        where = f"{path}:{s + 1}-{e + 1}"
        inside = next((sn for sn in snippets if sn.start < s and e < sn.end), None)
        if inside:
            if not inside.source:
                errs.append(f"{where}: {kind}がスニペット内にあるが data-source がない")
            continue
        before = "\n".join(lines[max(0, s - 3):s])
        m = MARKER.search(before)
        if m and m.group(1) == "original":
            continue
        if m:
            errs.append(f"{where}: 外部データ {m.group(1)!r} は SPDX スニペットで囲む")
        else:
            errs.append(f"{where}: {kind}が見つかった。自作なら直前に `data-source: original`、"
                        "外部データなら SPDX スニペットで囲んで data-source を書く")
    return errs


def externals(sid: str, sources: dict, seen=None) -> list[dict]:
    """sid の元をたどって外部データの宣言をすべて返す。"""
    seen = seen or set()
    if sid in seen or sid not in sources:
        return []
    seen.add(sid)
    src = sources[sid][1]
    if src.get("origin") == "external":
        return [src]
    out = []
    for p in src.get("derived_from", []):
        out += externals(p, sources, seen)
    return out


def _check_snippet(path: str, sn: Snippet, sources: dict, licenses: dict) -> list[str]:
    where = f"{path}:{sn.start + 1}"
    if not sn.source:
        return []
    if sn.source == "original":
        return [f"{where}: 自作のデータはスニペットで囲まず `data-source: original` だけを書く"]
    if sn.source not in sources:
        return [f"{where}: data-source {sn.source!r} に対応する SOURCE.toml がない"]
    errs = []
    src = sources[sn.source][1]
    lic = src.get("license")
    if sn.licenses != [lic]:
        errs.append(f"{where}: スニペットのライセンス {sn.licenses} が {sn.source} の {lic!r} と一致しない")
    for up in externals(sn.source, sources):
        uplic = up.get("license")
        info = licenses.get(uplic, {})
        # 本文より厳しい規則: 継承（SA）のデータは自作物（CC0）のファイルに埋め込まない
        if info.get("share_alike"):
            errs.append(f"{where}: {up['id']} は継承ライセンス {uplic} なので埋め込めない。"
                        "派生データとして SOURCE.toml の管轄に置く")
        # 本文より厳しい規則: クレジットはスニペットの中（データのすぐそば）に書く
        if info.get("attribution") and up.get("attribution") and up["attribution"] not in sn.text:
            errs.append(f"{where}: スニペットの中に {up['id']} のクレジット表記（attribution）をそのまま書く")
    return errs
