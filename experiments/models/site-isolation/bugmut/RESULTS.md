# Mutants from public fixed browser defects (tree node C9)

Record: [experiments/2026-11-24-bug-history-mutants.md](../../../2026-11-24-bug-history-mutants.md).
Model: `../SpecIsolation.tla`, unedited. A subagent wrote this on 2026-11-24. Nothing is committed.

## 1. Fixed before collecting (written 2026-11-24, before any bug was read)

Before this section was written, only four NVD results for the keyword `Cross-Origin-Opener-Policy`
had been printed. All four were web applications that omit the header, so none is a browser defect.

**Sources.** (A) The 44 rows of `../../../prereg/data/candidates-table.md`, an earlier held-out
collection (Chromium/Firefox, fixed 2024-01..2026-11). (B) The NVD CVE API 2.0 `keywordSearch`, run
once per keyword. Only public, fixed, disclosed entries are used. Undisclosed defects are not sought.

**Keywords (B):** `Cross-Origin-Opener-Policy`, `Cross-Origin-Embedder-Policy`,
`Cross-Origin-Resource-Policy`, `crossOriginIsolated`, `SharedArrayBuffer`, `site isolation`,
`origin-keyed`, `document.domain`, `opener`, `sandbox` + `iframe`, `redirect` + `origin`,
`navigation` + `origin`.

**Filter (B):** the description names Google Chrome, Mozilla Firefox (or Thunderbird/Firefox ESR)
or Safari/WebKit. Published 2018-01-01..2026-11-24. The description or the linked public bug title
names a cross-origin, cross-site or isolation boundary. Pure memory-safety bugs (use after free,
heap overflow, type confusion) are excluded unless the text names an isolation decision.

**Filter (A):** the row's component or wrong value names site isolation, sandbox, opener/popup,
redirect, COOP/COEP/CORP or an origin. Rows already judged out of scope in the prereg (#26, #28)
stay in. Their type is coded by the same taxonomy, not by the prereg verdict.

**Size and order.** At most 60 bugs: up to 25 from A in table order, then B round-robin over the
keywords in the order above. Within a keyword, CVEs are taken in ascending sha256(CVE id).
Duplicates (the same CVE in A and B, or under two keywords) count once.

**Per bug:** id, source URL (NVD page or public bug page), engine, fixed version, defect type, and
whether it maps to a model mutant. bugs.tsv holds only my own short summaries and URLs. No text
from bug reports is copied.

**Defect taxonomy (one primary type per bug).** Model-step types (M) can become a mutant if the
model has the step. Non-model types (N) are missing axes.

| code | type | example of the wrong step |
|---|---|---|
| M1 | check omitted | a spec check skipped (CORP, COEP adherence, sandbox flag, COOP switch) |
| M2 | wrong comparison | same-site where same-origin is due, scheme ignored, opaque treated as tuple |
| M3 | wrong input | the right check on the wrong entity (initiator vs self, top vs self, pre-redirect value) |
| M4 | lost inheritance | policy not inherited by about:blank, srcdoc, blob:, data:, popup, worker |
| M5 | wrong default or parse | header value parsed or defaulted wrongly |
| M6 | stale value across steps | computed once and not updated on redirect, history traversal or reuse |
| N1 | renderer trust | the browser process accepts a value a compromised renderer supplies |
| N2 | process model | wrong process / SiteInstance / BrowsingInstance, process reuse |
| N3 | cache, storage, bfcache, prerender | state kept across a boundary in a cache or partition |
| N4 | race or lifetime | ordering, timing, detached or inactive documents |
| N5 | UI or user gesture | address bar, Ctrl+click, drag, dialogs |
| N6 | side channel | timing, length, error-event oracles |
| N7 | non-web-platform surface | extensions, MHTML, fenced frames, WebView, PDF, iOS shell, devtools |

**Mapping rule.** `existing`: the defect is an author mutant already (a named Mutant, `neg:` of a
DecisionId, a FixMutant, a G2 or Redirect mutant). `new`: a C-style id over an existing decision
that no earlier run used (`true:<id>`, `false:<id>`, or `neg:` on a G2/redirect id not yet run).
`step`: the model's vocabulary covers it, but it needs a decision the model lacks. `no`: N type.

**Kill rule (unchanged).** Mutant m is killed by browser b if some observation is inside the
unmutated model's allowed set and outside m's. Observation sets: observe/ (109 WPT rows), gen/
(8 280 rows), gen2/ (709/688 rows), redirect/. COIChoices = {concrete, logical} (conservative) is
the headline figure.

## 2. Collection (after section 1)

- NVD queried 2026-11-24 ~06:35Z, one request per keyword (`resultsPerPage=2000`). The raw JSON stays outside the repository, because it contains description text. Rerun: `select_nvd.py <dir>`, then `assemble.py <candidates-table.md> filtered.json out.tsv`.
- Kept after the filter: site isolation 186, sandbox iframe 29, navigation origin 21, redirect origin 12, document.domain 2. COOP/COEP/CORP/crossOriginIsolated/SharedArrayBuffer/origin-keyed/ opener: 0. All hits were web applications or had no browser match.
- A: 23 of 44 rows matched; all 23 were taken. B: 37 (round-robin), giving 60 in total. Two are `out`: smartbanner.js is a library, and the Epiphany race has no fixed release. **58 counted.**
- Types were coded by one coder (this subagent) from the NVD text, the public bug titles (issues.chromium.org / bugzilla REST, fetched only for public bugs) and the prereg table. Eight Chromium bugs are still restricted. Their type is coded from the NVD component name only.

## 3. Counts (bugs.tsv)

| type | n | | type | n |
|---|---|---|---|---|
| M1 check omitted | 5 | | N1 renderer trust | 8 |
| M2 wrong comparison | 1 | | N5 UI / gesture | 7 |
| M3 wrong input | 5 | | N7 non-web surface | 7 |
| M4 lost inheritance | 3 | | N2 process model | 3 |
| M5 wrong parse/default | 1 | | N3 cache/bfcache | 3 |
| M6 stale across steps | 8 | | N6 side channel | 3 |
| M? model step, unknown which | 2 | | N4 race/lifetime | 2 |

- Model-step types (M): 25/58. Non-model types (N): 33/58.
- Mapping: `existing` 7, `step` 15, `unknown` 3, `no` 33. **No bug maps onto a model decision that the author's mutants missed.** The 7 `existing` bugs land on 5 author mutants: `false:mc-ancestor` (CVE-2025-6556, CVE-2026-8962), `false:g2-sb-opaque` (CVE-2016-9078, CVE-2017-5466), `false:g2-pp-self` (CVE-2026-0877), `neg:hop-update` (bmo 2059205) and
  `first-hop-only` (CVE-2022-34474). Most of these are analogies. The bug's trigger (data:, blob:, EventSource, external protocol) is not on the model's axes. Only the step's error is.
- Steps the model lacks (15 bugs, 14 decisions): sandbox flags other than the opaque origin (5: allow-popups/top-navigation/custom protocols, flag parsing, propagation to popups), values carried across redirects other than COOP (4: Origin taint, referrer policy, CSP report URL ×2), history entries (2), document.domain with origin-domain and Window reuse (2), worker policy container (1), ORB (1).

## 4. Bug-derived mutants (`BugMutants.tla`) and kills

Instance-level mapping gives no new mutant, so the new mutants are taken at the **type** level. The
most frequent model-step types are M6 and M1, and both are omissions ("check skipped", "update
skipped"). The author's mutants are almost all negations (`neg:`), a form that only one bug
(CVE-2026-8950, an inverted condition) has. `New` = `true:<id>` (33) and `false:<id>` (27 non-fix
ids) on every SpecIsolation decision, plus 6 redirect forms: 66 mutants. `run.sh` checks
them together with the 74 author mutants on all four sets (kill rule of section 1; Chrome 158,
Firefox 160 observations as recorded).

| cfg COIChoices | bug-derived killed | equivalent on all rows | survived, non-equiv. | author killed |
|---|---|---|---|---|
| {concrete, logical} | **59/66** | 5 | 2 | 73/74 |
| {concrete} | **61/66** | 5 | 0 | 74/74 |

- Over non-equivalent mutants the rate is 59/61 (97 %) vs 73/74 (99 %), or 61/61 vs 74/74.
- Survivors under {concrete, logical}: `false:coi-insecure` (the same function as the author's `coi-ignore-secure`) and `true:coi-mode`. Both only add `TRUE`, which the logical branch already allows. This is the known survivor pattern.
- Equivalent: `false:coop-one-unsafe`, `false:corp-first-pass`, `true:coep-cl-strips` and `true:secure-ctx-top` look semantically equivalent (by reading the operators). For example, `true:secure-ctx-top` changes nothing for a top-level context. **`false:fetch-cors` is a row gap**: cross-origin `fetch()` in cors mode then goes through CORP instead of the CORS outcome, and no
  observation set has a cross-origin cors row.
- 6–8 of the new mutants are killed only by redirect/. The others are killed by observe/, gen/ or gen2/ (`summarize.py` prints the sets).
- The 5 mutants hit by instance mapping are killed in both browsers. The exception is `neg:hop-update`, which only Chrome kills (24 rows), as redirect/RESULTS.md found.

## 5. Missing axes, ranked by bug count

1. N1 renderer trust (8). Needs a compromised-renderer attacker and IPC values as inputs (part 1 of the record has one; the observation sets have none).
2. N5 UI / user gesture (7) and N7 non-web surfaces (7: MHTML, fenced frames, iOS/Android shells, extensions/IWA, media, devtools, network layer).
3. Model steps missing on existing axes (15): sandbox flags (5), non-COOP redirect-carried values (4), history (2), document.domain origin-domain/Window reuse (2), workers (1), ORB (1).
4. N2 process model (3), N3 cache/bfcache/persistent cache (3), N6 side channels (3), N4 race/lifetime (2).

## 6. Hypotheses of the record

- **R1 (killed): supported for what is expressible.** Every bug-derived mutant expressible in the model is killed, except the known COI-choice survivors and one row gap. The rate equals the author's mutants'. All 7 `existing` bugs land on killed author mutants.
- **R2 (out of the axes): supported.** 33/58 are non-model types. Another 15 need steps that the model lacks, and 3 cannot be placed. So 51/58 (88 %) are outside what the observations test.
- **R3 (not expressible in the model's words): partly supported.** 33/58 (57 %) are implementation-structure errors (N), and they are the majority. The M types themselves are expressible, but only 7/25 land on a step the model has.

## 7. C9 done condition

"Axes/mutants from bug histories, inclusion checked with them": **met in form, thin in
substance.** The axes (section 5) and mutants (section 4) come from 58 public, fixed bugs, and the
kill/inclusion check ran on all four observation sets. But no new instance-level mutant arose: the
type-level mutants are a re-weighting of C-style operators, and the actionable output is the
missing-axis ranking.

## Limits

- One coder. The taxonomy was fixed in advance, but restricted bugs are coded from component names. The A set comes from an earlier origin-computation-focused collection (2024–2026). NVD keyword search is literal: COOP/COEP/CORP defects are filed as "site isolation" or "Navigation" and were not hit by their own names.
- The `existing` mappings are analogies (same step error, different trigger).
- Equivalence was judged on the observed rows. Semantic equivalence was read by hand, not checked.

## Files

`bugs.tsv`, `BugMutants.tla`, `BugKill{Observe,Gen,Gen2,Redirect}.tla` (cfgs are written by
`run.sh`), `run.sh <outdir> [sets]` (TLC in podman, scratch copies, reports INCOMPLETE if TLC was
killed), `summarize.py bugs.tsv <outdir> ../SpecIsolation.tla`, `select_nvd.py`, `assemble.py`.
