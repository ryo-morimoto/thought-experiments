#!/usr/bin/env python3
"""List every name in the given paths, mechanically, so an audit cannot skip a surface.

Usage:
    inventory.py <path>...                  # kind<TAB>name<TAB>file:line, one row per definition
    inventory.py <path>... --collisions     # names that appear with two or more kinds
    inventory.py <path>... --unused         # names whose word appears only once (never used)
    inventory.py <path>... --words W...     # every whole-word occurrence of W (leftovers after renames)

Surfaces: Python (via ast), JS/TS, CSS classes and custom properties, HTML ids and classes,
JSON/TOML/YAML keys, Markdown code spans, Rust, Clojure. CSS, HTML and JS embedded in other
files (for example an HTML template in a Python string) are scanned too. Non-Python
languages use regular expressions, so unusual syntax can be missed; check the counts.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ID = r"[A-Za-z_$][\w$]*"
SKIP = {".git", "node_modules", "__pycache__", ".venv", "target", "dist", "build"}


def scan_text(add, text: str, base: int, suffix: str) -> None:
    """Regex surfaces. `base` is the line number of the text's first line."""
    in_style = suffix == ".css"
    in_script = suffix in {".js", ".mjs", ".ts", ".tsx", ".jsx"}
    for i, line in enumerate(text.split("\n")):
        n = base + i
        if re.search(r"<style\b", line):
            in_style = True
        if re.search(r"<script\b(?![^>]*application/json)", line):
            in_script = True
        for m in re.finditer(r"(--[A-Za-z_][\w-]*)\s*:", line):
            add("css-var", m.group(1), n)
        if in_style:
            selector = re.sub(r"\{.*", "", line) if "{" in line else ""
            for m in re.finditer(r"\.([A-Za-z_][\w-]*)", selector):
                add("css-class", m.group(1), n)
        for m in re.finditer(r'\bid="([^"]+)"', line):
            add("html-id", m.group(1), n)
        for m in re.finditer(r'\bclass(?:Name)?\s*=\s*"([^"]+)"', line):
            for c in m.group(1).split():
                add("css-class", c, n)
        for m in re.finditer(r"classList\.\w+\(([^)]*)\)", line):
            for c in re.findall(r'"([\w-]+)"', m.group(1)):
                add("css-class", c, n)
        if in_script:
            for m in re.finditer(rf"\b(?:const|let|var)\s+(?:\[([^\]]*)\]|\{{([^}}]*)\}}|({ID}))", line):
                names = [m.group(3)] if m.group(3) else re.findall(ID, m.group(1) or m.group(2))
                for name in names:
                    add("js-binding", name, n)
            for m in re.finditer(rf"\b(?:function|class)\s+({ID})", line):
                add("js-function-or-class", m.group(1), n)
            for m in re.finditer(rf"\(([^()]*)\)\s*=>|\b({ID})\s*=>|\bfunction\s*{ID}?\s*\(([^)]*)\)", line):
                for name in re.findall(ID, m.group(1) or m.group(2) or m.group(3) or ""):
                    add("js-param", name, n)
            for m in re.finditer(rf"[{{,]\s*({ID})\s*:", line):
                add("js-key", m.group(1), n)
        if suffix == ".md":
            for m in re.finditer(r"`([^`]+)`", line):
                add("doc-term", m.group(1).strip(), n)
        if suffix == ".rs":
            for m in re.finditer(r"\b(?:fn|struct|enum|trait|const|static|let(?: mut)?|mod|type)\s+([A-Za-z_]\w*)", line):
                add("rust", m.group(1), n)
        if suffix in {".clj", ".cljs", ".cljc", ".edn"}:
            for m in re.finditer(r"\((?:def|defn|defn-|defmacro|defrecord|defprotocol|ns)\s+([^\s()]+)", line):
                add("clojure", m.group(1), n)
        if suffix in {".toml"}:
            m = re.match(r"\s*\[\[?([\w.-]+)\]\]?", line) or re.match(r"\s*([A-Za-z_][\w-]*)\s*=", line)
            if m:
                for part in m.group(1).split("."):
                    add("config-key", part, n)
        if suffix in {".yml", ".yaml"}:
            m = re.match(r"\s*-?\s*([A-Za-z_][\w-]*)\s*:", line)
            if m:
                add("config-key", m.group(1), n)
        if "</style>" in line:
            in_style = False
        if "</script>" in line and suffix not in {".js", ".mjs", ".ts", ".tsx", ".jsx"}:
            in_script = False


def scan_python(add, text: str) -> None:
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            add("py-class", node.name, node.lineno)
            for b in node.body:
                if isinstance(b, ast.AnnAssign) and isinstance(b.target, ast.Name):
                    add("py-field", b.target.id, b.lineno)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            if not isinstance(node, ast.Lambda):
                add("py-function", node.name, node.lineno)
            a = node.args
            for arg in a.posonlyargs + a.args + a.kwonlyargs + [x for x in (a.vararg, a.kwarg) if x]:
                add("py-param", arg.arg, node.lineno)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            add("py-constant" if node.id.isupper() else "py-local", node.id, node.lineno)
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
            add("py-attribute", node.attr, node.lineno)
        elif isinstance(node, ast.Dict):
            for k in node.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str) and re.fullmatch(r"\w+", k.value):
                    add("data-key", k.value, k.lineno)
        elif isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) \
                and isinstance(node.slice.value, str) and re.fullmatch(r"\w+", node.slice.value):
            add("data-key", node.slice.value, node.lineno)
        elif isinstance(node, ast.Call):
            attr = getattr(node.func, "attr", getattr(node.func, "id", ""))
            strs = [x.value for x in node.args if isinstance(x, ast.Constant) and isinstance(x.value, str)]
            if attr == "add_parser" and strs:
                add("cli-command", strs[0], node.lineno)
            elif attr == "add_argument" and strs:
                add("cli-flag", strs[0], node.lineno)
            elif attr == "get" and strs and re.fullmatch(r"\w+", strs[0]):
                add("data-key", strs[0], node.lineno)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and re.search(r"<(style|script|html)\b", node.value):
            scan_text(add, node.value, node.lineno, ".html")  # embedded page


def collect(paths: list[Path]) -> dict[tuple[str, str], list[str]]:
    rows: dict[tuple[str, str], list[str]] = defaultdict(list)
    files = [f for p in paths for f in ([p] if p.is_file() else sorted(p.rglob("*")))
             if f.is_file() and not SKIP & set(f.parts)]
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        add = lambda kind, name, line, f=f: rows[(kind, name)].append(f"{f}:{line}")  # noqa: E731
        add("file", f.name, 1)
        if f.suffix == ".py":
            try:
                scan_python(add, text)
            except SyntaxError as e:
                print(f"skip {f}: {e}", file=sys.stderr)
        elif f.suffix == ".json":
            try:
                def keys(x):
                    if isinstance(x, dict):
                        for k, v in x.items():
                            add("config-key", k, 1)
                            keys(v)
                    elif isinstance(x, list):
                        for v in x:
                            keys(v)
                keys(json.loads(text))
            except ValueError:
                pass
        else:
            scan_text(add, text, 1, f.suffix)
    return rows


def main(argv: list[str]) -> int:
    words = argv[argv.index("--words") + 1:] if "--words" in argv else []
    args = argv[: argv.index("--words")] if "--words" in argv else argv
    paths = [Path(a) for a in args if not a.startswith("--")]
    if not paths:
        print(__doc__, file=sys.stderr)
        return 2
    if words:
        pattern = re.compile(r"(?<![\w$-])(" + "|".join(map(re.escape, words)) + r")(?![\w$-])")
        for p in paths:
            for f in ([p] if p.is_file() else sorted(p.rglob("*"))):
                if f.is_file() and not SKIP & set(f.parts):
                    try:
                        for i, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
                            if pattern.search(line):
                                print(f"{f}:{i}:\t{line.strip()}")
                    except (UnicodeDecodeError, OSError):
                        pass
        return 0
    rows = collect(paths)
    if "--unused" in argv:
        text = "\n".join(f.read_text(encoding="utf-8", errors="replace") for p in paths
                         for f in ([p] if p.is_file() else sorted(p.rglob("*")))
                         if f.is_file() and not SKIP & set(f.parts))
        for kind, name in sorted(rows):
            word = name.lstrip(".#")
            # Mentions in docs, and functions a framework calls by name, are not definitions to use.
            if kind in {"file", "doc-term"} or re.match(r"(test|setUp|tearDown)", name):
                continue
            if len(re.findall(r"(?<![\w$-])" + re.escape(word) + r"(?![\w$-])", text)) <= 1:
                print(f"{kind}\t{name}\t{', '.join(rows[(kind, name)])}")
        return 0
    if "--collisions" in argv:
        kinds = defaultdict(set)
        for kind, name in rows:
            kinds[name.lstrip(".-#")].add(kind)
        for name in sorted(kinds):
            if len(kinds[name]) > 1:
                print(f"{name}\t{', '.join(sorted(kinds[name]))}")
        return 0
    for (kind, name), where in sorted(rows.items()):
        print(f"{kind}\t{name}\t{', '.join(sorted(set(where)))}")
    print(f"{len(rows)} names, {len({n for _, n in rows})} distinct", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
