"""Convert WPT expectation TSV into a TLA+ module of test cases.

Usage: python3 -I tsv2tla.py cases.tsv WPTBroad.tla
"""
import csv
import sys

ORIGINS = {
    "A": "OA", "Awww": "OAwww", "Awww2": "OAwww2", "B": "OB",
    "Ahttp": "OAhttp", "Awwwhttp": "OAwwwhttp", "Bhttp": "OBhttp",
}


def lit(tok):
    if tok in ORIGINS:
        return ORIGINS[tok]
    if tok in ("TRUE", "FALSE"):
        return tok
    return '"%s"' % tok


def call(op, args):
    a = [lit(x) for x in args]
    if op == "FetchResult":
        o, coep, mode, ro, corp, creds = a
        return 'FetchResult(%s, %s, %s, [origin |-> %s, corp |-> %s, creds |-> %s])' % (
            o, coep, mode, ro, corp, creds)
    if op == "OriginAgentCluster":
        o, coi, hist, hdr = a
        return "OriginAgentCluster(KeyKind(%s, %s, %s, %s))" % (o, coi, hist, hdr)
    if op == "DocumentDomainNoOp":
        return "DocumentDomainNoOp(%s)" % a[0]
    if op == "CrossOriginIsolated":
        return "CrossOriginIsolated(%s)" % ", ".join(a)
    if op == "PopupSevered":
        return "PopupSevered(%s)" % ", ".join(a)
    raise SystemExit("unknown operator " + op)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    rows = list(csv.DictReader(open(src, encoding="utf-8"), delimiter="\t"))
    lines = [
        "------------------------------ MODULE WPTBroad ------------------------------",
        "(* Generated from WPT expectations collected for                          *)",
        "(* experiments/2026-11-20-browser-semantics-soundness.md. Names w001...   *)",
        "(* follow the row order of the source table; see WPTBroadIndex.md.        *)",
        "EXTENDS SpecIsolation",
        "",
        "BroadCases == {",
    ]
    entries = []
    for i, r in enumerate(rows, 1):
        args = [x.strip() for x in r["args"].split(",")]
        got = call(r["operator"], args)
        want = lit(r["expected"].strip())
        entries.append('  [name |-> "w%03d", got |-> %s, want |-> %s]' % (i, got, want))
    lines.append(",\n".join(entries))
    lines += [
        "}",
        "BroadMismatches == {t.name : t \\in {u \\in BroadCases : u.got # u.want}}",
        'PrintBroad == PrintT(<<"broad", Mutant, BroadMismatches>>)',
        "BroadAgree == BroadMismatches = {}",
        "\\* Cases that Chrome, Firefox and Safari all pass on wpt.fyi.",
        "StableNames == {%s}" % ", ".join(
            '"w%03d"' % i for i, r in enumerate(rows, 1)
            if (r.get("chrome"), r.get("firefox"), r.get("safari")) == ("PASS",) * 3),
        'PrintStable == PrintT(<<"stable", Mutant, BroadMismatches \\cap StableNames>>)',
        "===============================================================================",
        "",
    ]
    open(dst, "w", encoding="utf-8").write("\n".join(lines))
    idx = ["# WPTBroad の行番号と WPT の試験", "",
           "WPTBroad.tla の w001 以降と、元の表の行の対応。試験の本文（wpt.live、"
           "web-platform-tests の master）から subagent が読み取った引数と期待値、"
           "wpt.fyi の 2026-11-20 の stable の実行（Chrome 158、Firefox 160、Safari 27.2）"
           "の結果。試験そのものは載せず、事実の要約だけを載せる。", "",
           "<!-- data-source: original（WPT の試験の期待値と実行結果を要約した事実の表） -->",
           "| 名前 | 試験 | 演算子 | 引数 | 期待 | Chrome | Firefox | Safari |",
           "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for i, r in enumerate(rows, 1):
        idx.append("| w%03d | %s | %s | %s | %s | %s | %s | %s |" % (
            i, r["wpt_path"], r["operator"], r["args"], r["expected"],
            r.get("chrome", ""), r.get("firefox", ""), r.get("safari", "")))
    open(dst.replace("WPTBroad.tla", "WPTBroadIndex.md"), "w", encoding="utf-8").write(
        "\n".join(idx) + "\n")
    print(len(rows), "cases")


main()
