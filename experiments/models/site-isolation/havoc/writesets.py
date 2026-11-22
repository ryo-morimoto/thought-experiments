#!/usr/bin/env python3
"""Write-set measurement for the havoc experiment
(experiments/2026-11-23-havoc-unmodeled-steps.md).

Reads closure_steps.tsv (not committed; spec text) and writes writesets.tsv
with one row per step that writes something, using the author's own labels
only (algorithm name, step number, a short target label, concept, status).

    python3 -I writesets.py <closure_steps.tsv> <out writesets.tsv>

Rules: a step "writes" if its form is assign, or if it is a branch/loop/call
whose text contains an embedded write clause (set/let/append/...), or if it is
a return in an algorithm whose result is a model-read concept. The concept is
decided from the target phrase and the algorithm name by the patterns below,
then corrected by the hand-review table REVIEW.
"""
import csv
import re
import sys
from collections import Counter

# Concepts the model reads (SpecIsolation.tla), and the concepts it does not.
READ = {"coep", "coop", "corp", "creds", "secure", "origin", "akey", "coimode",
        "coicap", "tainting", "mode", "bcgswitch", "response"}
NOT_READ = {"report", "timing", "sandbox", "other"}

# Algorithms whose return value is a model-read concept.
RETURNS = {
    "obtain an embedder policy": "coep",
    "obtain an opener policy": "coop",
    "Cross-Origin-Embedder-Policy allows credentials": "creds",
    "cross-origin resource policy check": "corp",
    "cross-origin resource policy internal check": "corp",
    "secure context": "secure",
    "determine the origin": "origin",
    "obtain a site": "origin",
    "same site": "origin",
    "same origin": "origin",
    "schemelessly same site": "origin",
    "obtain a similar-origin window agent": "akey",
    "clone a policy container": "coep",
    "create a policy container from a fetch response": "coep",
    "determine navigation params policy container": "coep",
    "match opener policy values": "bcgswitch",
    "check if popup COOP values require a browsing context group switch": "bcgswitch",
    "check if COOP values require a browsing context group switch": "bcgswitch",
    "enforce a response's opener policy": "bcgswitch",
    "obtain a browsing context to use for a navigation response": "coimode",
    "redirect-taint": "creds",
}

# Ordered target patterns (lowercase target phrase -> concept).
TARGET = [
    (r"report|endpoint|violation", "report"),
    (r"time|timing|coarsen", "timing"),
    (r"sandbox", "sandbox"),
    (r"cross-origin isolation mode", "coimode"),
    (r"cross-origin ?isolated ?capability|crossoriginisolatedcapability", "coicap"),
    (r"agent cluster|origin-keyed|historical agent|^key$|^site$|^agent$", "akey"),
    (r"embedder policy|policy ?container|embedderpolicy|^coep$|parentpolicy", "coep"),
    (r"opener policy|^coop$|navigationcoop|responsecoop|coopenforcementresult|"
     r"browsing context group switch|^swapgroup$", "coop"),
    (r"credentials|includecredentials|redirect taint|^taint$", "creds"),
    (r"response tainting", "tainting"),
    (r"creation url", "secure"),
    (r"(request|httprequest)'s mode$", "mode"),
    (r"url list|current url", "origin"),
    (r"top-level origin|toplevelorigin|ancestor origin|serializ", "other"),
    (r"origin", "origin"),
    (r"^(response|internalresponse|response and internalresponse|fetchresponse|"
     r"forwardresponse|storedresponse)$", "response"),
    (r"header list", "corp"),
]

WRITE_VERBS = r"(append|add|remove|extend|prepend|enqueue|push|clear|empty|replace|update|" \
              r"increment|decrement|initialize|store|unset)"


def target_of(text):
    """Return (kind, target phrase) or None."""
    t = text.strip()
    m = re.match(r"(?i)(?:if .*?,\s*then |otherwise,?\s*(?:if .*?,\s*then )?|.*?\bthen )?"
                 r"(?:optionally )?set (.+?) to\b", t)
    if m and not re.match(r"(?i)set up\b", t):
        tgt = m.group(1)
        kind = "field" if "'s " in tgt or "[" in tgt else "local"
        return kind, tgt.split("'s ")[-1] if kind == "field" else tgt, tgt
    m = re.match(r"(?i)let (\S+(?: and \S+)?) be\b", t)
    if m:
        return "local", m.group(1), m.group(1)
    m = re.match(r"(?i)(?:.*?\bthen )?" + WRITE_VERBS + r"\b.*?\b(?:to|from|into|in) (.+?)[.,]", t)
    if m:
        return "collection", m.group(2).split("'s ")[-1], m.group(2)
    if re.match(r"(?i)" + WRITE_VERBS + r"\b", t):
        return "collection", "?", "?"
    return None


def concept_of(phrase, full, text):
    p = phrase.lower().strip("|")
    f = full.lower()
    for pat, c in TARGET:
        if re.search(pat, p) or re.search(pat, f):
            return c
    # local bindings: look at the right-hand side
    rhs = text.lower()
    for alg, c in RETURNS.items():
        if "result of " in rhs and alg.lower().split()[0] in rhs and alg.lower() in rhs:
            return c
    return "other"


# Hand review: (algorithm, step) -> (concept, status, model_ref, point)
# status: modeled | unmodeled | outscope (write applies only outside the
# property's context, e.g. navigation requests or new requests) | notread.
REVIEW = {
    ("obtain an embedder policy", "1"): ("coep", "modeled", "EffectiveCOEP default", "h-ecoep-insecure"),
    ("obtain an embedder policy", "2"): ("coep", "modeled", "coep-insecure", "h-ecoep-insecure"),
    ("obtain an embedder policy", "4.1"): ("coep", "modeled", "coep argument", ""),
    ("obtain an embedder policy", "7"): ("coep", "modeled", "EffectiveCOEP", ""),
    ("obtain an embedder policy", "3"): ("coep", "modeled", "coep argument", ""),
    ("obtain an embedder policy", "5"): ("report", "notread", "", ""),
    ("obtain an embedder policy", "6.1"): ("report", "notread", "", ""),
    ("clone a policy container", "1"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("clone a policy container", "3"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("clone a policy container", "6"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("create a policy container from a fetch response", "1"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("create a policy container from a fetch response", "2"): ("coep", "modeled", "EffectiveCOEP", ""),
    ("create a policy container from a fetch response", "4"): ("coep", "modeled", "EffectiveCOEP", ""),
    ("create a policy container from a fetch response", "7"): ("coep", "modeled", "EffectiveCOEP", ""),
    ("determine navigation params policy container", "1.2"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("determine navigation params policy container", "2.2"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("determine navigation params policy container", "3"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("determine navigation params policy container", "4"): ("coep", "modeled", "EffectiveCOEP", ""),
    ("determine navigation params policy container", "5"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("process early hint headers", "1"): ("coep", "notread", "early hints preload", ""),
    ("navigate", "24.8.1"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("navigate", "24.8.2"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("evaluate a javascript: URL", "11"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("create navigation params from a srcdoc resource", "6"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("create navigation params by fetching", "16"): ("coep", "modeled", "EffectiveCOEP", ""),
    ("create navigation params by fetching", "21.9"): ("coep", "modeled", "EffectiveCOEP", ""),
    ("create navigation params by fetching", "25"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("populate request from client", "3.1"):("coep", "modeled", "identity (client COEP)", ""),
    ("populate request from client", "3.2"): ("coep", "outscope", "no client", ""),
    ("populate request from client", "2.2"): ("origin", "modeled", "identity (requester o)", ""),
    ("create a new browsing context and document", "19.2"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("attempt to populate the history entry's document", "5.7.3.3.2"): ("coep", "unmodeled", "", "h-ecoep-inherit"),
    ("cross-origin resource policy check", "1"): ("corp", "modeled", "forNav", ""),
    ("cross-origin resource policy check", "2"): ("coep", "modeled", "CorpCheck coep", ""),
    ("cross-origin resource policy check", "3"): ("corp", "modeled", "corp-first-pass", ""),
    ("cross-origin resource policy check", "5"): ("corp", "modeled", "fetch-blocked", ""),
    ("cross-origin resource policy check", "7"):("corp", "modeled", "CorpCheck", ""),
    ("cross-origin resource policy internal check", "1"): ("corp", "modeled", "corp-nav", ""),
    ("cross-origin resource policy internal check", "2"): ("corp", "modeled", "r.corp", ""),
    ("cross-origin resource policy internal check", "3"): ("corp", "modeled", "r.corp (CORPs)", ""),
    ("cross-origin resource policy internal check", "4"): ("corp", "modeled", "corp-cl-creds", ""),
    ("cross-origin resource policy internal check", "5"): ("corp", "modeled", "corp-allow-kinds", ""),
    ("Cross-Origin-Embedder-Policy allows credentials", "2"): ("creds", "modeled", "coep-cl-strips", "h-creds-cl"),
    ("Cross-Origin-Embedder-Policy allows credentials", "3"): ("creds", "outscope", "no client", ""),
    ("Cross-Origin-Embedder-Policy allows credentials", "4"): ("creds", "modeled", "coep-cl-strips", "h-creds-cl"),
    ("Cross-Origin-Embedder-Policy allows credentials", "5"): ("creds", "unmodeled", "redirect taint", "h-creds-mode"),
    ("Cross-Origin-Embedder-Policy allows credentials", "6"): ("creds", "modeled", "coep-cl-strips", "h-creds-cl"),
    ("HTTP-network-or-cache fetch", "8.3"): ("creds", "unmodeled", "credentials mode", "h-creds-mode"),
    ("HTTP-network-or-cache fetch", "8.4"): ("creds", "modeled", "coep-cl-strips", "h-creds-cl"),
    ("HTTP-network-or-cache fetch", "14"): ("creds", "modeled", "r.creds", ""),
    ("HTTP-network-or-cache fetch", "12"): ("origin", "unmodeled", "redirects", "h-respurl"),
    ("HTTP-redirect fetch", "18"): ("origin", "unmodeled", "redirects", "h-respurl"),
    ("main fetch", "16"): ("origin", "unmodeled", "redirects", "h-respurl"),
    ("main fetch", "17"): ("creds", "unmodeled", "redirect taint", "h-creds-mode"),
    ("redirect-taint", "2"): ("creds", "unmodeled", "redirect taint", "h-creds-mode"),
    ("redirect-taint", "3"): ("creds", "unmodeled", "redirect taint", "h-creds-mode"),
    ("redirect-taint", "4.4"): ("creds", "unmodeled", "redirect taint", "h-creds-mode"),
    ("redirect-taint", "5"): ("creds", "unmodeled", "redirect taint", "h-creds-mode"),
    ("main fetch", "12.4"): ("tainting", "modeled", "fetch-same-origin", "h-tainting"),
    ("main fetch", "12.7"): ("tainting", "modeled", "fetch-cors/opaque", "h-tainting"),
    ("main fetch", "12.9"): ("tainting", "modeled", "fetch-cors", "h-tainting"),
    ("main fetch", "12.13"): ("tainting", "modeled", "fetch-cors", "h-tainting"),
    ("main fetch", "14.2"): ("tainting", "modeled", "FetchResult kinds", "h-tainting"),
    ("main fetch", "12"): ("response", "modeled", "FetchResult", ""),
    ("main fetch", "3"): ("response", "outscope", "local-URLs-only", ""),
    ("HTTP fetch", "3.4"): ("response", "unmodeled", "service worker (boundary)", "h-sw"),
    ("HTTP fetch", "4.3"): ("response", "modeled", "r", ""),
    ("fetch", "3"): ("coicap", "notread", "timing only", ""),
    ("fetch", "5.2"): ("coicap", "notread", "timing only", ""),
    ("set up a window environment settings object", "6"): ("secure", "unmodeled", "top-level creation URL", "h-secure"),
    ("create navigation params by fetching", "21.2.3.2"): ("secure", "unmodeled", "top-level creation URL", "h-secure"),
    ("create and initialize a Document object", "8.9.2"): ("secure", "unmodeled", "top-level creation URL", "h-secure"),
    ("create a new browsing context and document", "11.1"): ("secure", "unmodeled", "top-level creation URL", "h-secure"),
    ("create a new browsing context and document", "11.2"): ("secure", "unmodeled", "top-level creation URL", "h-secure"),
    ("secure context", "1.2.1"): ("secure", "unmodeled", "worker owner", "h-secure"),
    ("secure context", "1.2.2"): ("secure", "unmodeled", "worker owner", "h-secure"),
    ("secure context", "1.3"): ("secure", "unmodeled", "worklet", "h-secure"),
    ("secure context", "2"): ("secure", "unmodeled", "data: URL", "h-secure"),
    ("secure context", "3"): ("secure", "modeled", "Secure(o)", ""),
    ("secure context", "4"): ("secure", "modeled", "Secure(o)", ""),
    ("create navigation params by fetching", "5.1"): ("origin", "outscope", "navigation request", "h-reqorigin"),
    ("create navigation params by fetching", "10.1"): ("origin", "outscope", "navigation request", "h-reqorigin"),
    ("obtain an opener policy", "1"): ("coop", "modeled", "ParsedCOOP default", ""),
    ("obtain an opener policy", "2"): ("coop", "modeled", "coi-insecure", ""),
    ("obtain an opener policy", "4.1.1"): ("coep", "modeled", "coi-coep-compat", ""),
    ("obtain an opener policy", "4.1.2"): ("coop", "modeled", "coi-coop-so/coi-coep-compat", ""),
    ("obtain an opener policy", "4.1.3"): ("coop", "modeled", "ParsedCOOP", ""),
    ("obtain an opener policy", "4.2"): ("coop", "modeled", "ParsedCOOP", ""),
    ("obtain an opener policy", "4.3"): ("coop", "unmodeled", "noopener-allow-popups", "h-coop"),
    ("obtain an opener policy", "7"): ("coop", "modeled", "ParsedCOOP", ""),
    ("navigate", "24.8.5"): ("coop", "unmodeled", "new default COOP", "h-coop"),
    ("create navigation params from a srcdoc resource", "4"): ("coop", "unmodeled", "srcdoc default", "h-coop"),
    ("create navigation params by fetching", "17"): ("coop", "unmodeled", "default before response", "h-coop"),
    ("create navigation params by fetching", "21.12.1"): ("coop", "modeled", "ParsedCOOP", ""),
    ("evaluate a javascript: URL", "13"): ("coop", "unmodeled", "javascript: URL", "h-coop"),
    ("create a document to display a user agent page or PDF viewer inline", "2"): ("coop", "unmodeled", "UA page", "h-coop"),
    ("create a new browsing context and document", "19.3"): ("coop", "modeled", "popup carries opener COOP", ""),
    ("obtain a browsing context to use for a navigation response", "12"): ("coimode", "modeled", "coi-mode / COIChoice", "h-coimode"),
    ("obtain a browsing context to use for a navigation response", "2"): ("coimode", "unmodeled", "non-top-level keeps group", "h-coimode"),
    ("obtain a browsing context to use for a navigation response", "9.2"): ("coimode", "unmodeled", "no swap keeps group", "h-coimode"),
    ("obtain a browsing context to use for a navigation response", "10"): ("coimode", "unmodeled", "new group", "h-coimode"),
    ("obtain a similar-origin window agent", "6.2"): ("coimode", "modeled", "identity (group mode)", ""),
}


# Second pass of the hand review, by algorithm and concept, for rows the
# per-step table does not list. status "input": the value is upstream of both
# the property and the model's read site, so the model's universal
# quantification over its inputs already covers any value ("composite" when
# the target is a whole response record). "nocone": read by the model but by
# neither safety property.
NAV = {"navigate", "create navigation params by fetching", "create navigation params from a srcdoc resource",
       "attempt to populate the history entry's document", "create a new browsing context and document",
       "create a document to display a user agent page or PDF viewer inline", "evaluate a javascript: URL",
       "get session history entries for the navigation API", "apply the history step",
       "obtain a browsing context to use for a navigation response"}


def second_pass(x, c, label):
    alg, step, t = x["algorithm"], x["step"], x["text"].lower()
    if c == "corp":  # header list writes
        if "response's header list" in t:
            return "corp", "input", "r.corp quantified", ""
        return "other", "notread", "request header", ""
    if c == "response":
        return "response", "composite", "r quantified", ""
    if c == "origin":
        if alg == "main fetch" and step == "10":
            return "origin", "unmodeled", "scheme upgrade", "h-respurl"
        if alg in NAV or alg in ("determine the origin",):
            return "origin", "input", "document origin o quantified", ""
        if alg in ("same origin", "same site", "obtain a site", "schemelessly same site"):
            return "origin", "modeled", "SameOrigin/SameSite", ""
        return "other", "notread", "origin not read by model", ""
    if c == "akey":
        if alg == "obtain a similar-origin window agent":
            return "akey", "nocone", "KeyKind", "h-keykind"
        return "other", "notread", "other key", ""
    if c in ("coop", "bcgswitch"):
        if "opener policy" in alg.lower() or "coop" in alg.lower() or alg in NAV:
            return "bcgswitch", "nocone", "MatchCOOP/PopupSevered", "h-popup"
    if c == "coep" and alg == "obtain an opener policy":
        return "report", "notread", "report-only", ""
    if c == "coep" and alg.startswith("check a navigation response"):
        # a check, not a write; COIOptIn relies on it (HavocSpec h-coimode-adh)
        return "coep", "unmodeled-guard", "child adherence check", "h-coimode-adh"
    if c == "creds":
        if alg == "redirect-taint":
            return "creds", "unmodeled", "redirect taint", "h-creds-mode"
        if alg == "CORS check":
            return "other", "notread", "CORS credentials", ""
        return None
    if c == "coimode":
        return "coimode", "modeled", "COIMode", ""
    return None


def auto_selects(x):
    """Would the automatic rules select this row as a write?"""
    form = x["form"]
    if form == "return":
        return x["algorithm"] in RETURNS
    if form == "branch" and x["algorithm"] in RETURNS and re.search(r"(?i)\breturn\b", x["text"]):
        return True
    return form == "assign" or target_of(x["text"]) is not None


CONTROL_STEPS = [("obtain an embedder policy", "2"), ("HTTP-network-or-cache fetch", "8.4")]


def main(src, dst, blind=False):
    """blind: ignore the per-step table REVIEW (rules only), to see which
    steps the automatic rules select without hand seeding."""
    review = {} if blind else REVIEW
    rows = list(csv.DictReader(open(src, encoding="utf-8"), delimiter="\t"))
    out = []
    rows_by_key = {(x["algorithm"], x["step"]): x for x in rows}
    for x in rows:
        form = x["form"]
        key = (x["algorithm"], x["step"])
        tg = target_of(x["text"]) if form not in ("return",) else None
        if form == "return":
            c = RETURNS.get(x["algorithm"])
            if not c and key not in review:
                continue
            kind, label = "return", "result"
        elif tg is None and form == "branch" and x["algorithm"] in RETURNS \
                and re.search(r"(?i)\breturn\b", x["text"]):
            # a guarded early return writes the algorithm's result
            kind, label, c = "embedded-return", "result", RETURNS[x["algorithm"]]
        elif tg is None:
            if key not in review and form != "assign":
                continue
            kind, label, c = ("embedded", "?", "other") if form != "assign" else ("unparsed", "?", "other")
        else:
            if form != "assign" and form not in ("branch", "loop", "call", "None", "external-call"):
                continue
            kind, label, full = tg
            if form != "assign":
                kind = "embedded-" + kind
            c = concept_of(label, full, x["text"])
        label = " ".join(re.sub(r"[|\[\]]", "", label).split()[:6])
        if key in review:
            c, status, ref, point = review[key]
        elif c in READ and second_pass(x, c, label) is not None:
            c, status, ref, point = second_pass(x, c, label)
        else:
            status = "notread" if c in NOT_READ else ("gap" if c == "other" else "auto-unreviewed")
            if kind in ("local", "collection", "unparsed") and c == "other":
                status = "gap"
            if c == "other" and kind == "field":
                status = "notread"
            ref, point = "", ""
        out.append([x["spec"], x["algorithm"], x["step"], form, kind, label, c, status, ref, point])
    with open(dst, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["spec", "algorithm", "step", "form", "write_kind", "target_label",
                    "concept", "status", "model_ref", "havoc_point"])
        w.writerows(out)
    # summary
    print("rows", len(out), "of", len(rows))
    print("forms", Counter(r[3] for r in out))
    print("kind", Counter(r[4].split("-")[-1] for r in out))
    print("assign-form writes", sum(1 for r in out if r[3] == "assign"))
    print("concept x status", sorted(Counter((r[6], r[7]) for r in out).items()))
    rd = [r for r in out if r[6] in READ]
    print("writes to model-read concepts", len(rd), Counter(r[7] for r in rd))
    print("  of which assign-form", sum(1 for r in rd if r[3] == "assign"))
    print("gaps (target undetermined)", sum(1 for r in out if r[7] == "gap"),
          Counter(r[4] for r in out if r[7] == "gap"))
    print("unmodeled by point", Counter(r[9] for r in out if r[7] == "unmodeled"))
    nonw = Counter(x["form"] for x in rows if x["form"] in ("call", "external-call") or x["class"] in ("remainder", "boundary"))
    print("non-write steps that may write via callee/prose", nonw)
    print("guarded early returns counted as writes", sum(1 for r in out if r[4] == "embedded-return"))
    sel = {(r[1], r[2]): r for r in out}
    for k in CONTROL_STEPS:
        r = sel.get(k)
        print("control step", k, "->", (r[4], r[6], r[7]) if r else "NOT SELECTED")
    if not blind:
        print("rows selected only through REVIEW:",
              sorted(k for k in REVIEW if k in sel and not auto_selects(rows_by_key[k])))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], blind=len(sys.argv) > 3 and sys.argv[3] == "--blind")
