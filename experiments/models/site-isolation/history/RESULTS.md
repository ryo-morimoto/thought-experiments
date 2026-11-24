# Session history and bfcache as state transitions: inclusion and traversal-mutant kills

Second fragment after [../redirect/RESULTS.md](../redirect/RESULTS.md), for the record
[experiments/2026-11-24-history-bfcache-sequence.md](../../../2026-11-24-history-bfcache-sequence.md)
(tree nodes D1, E1, history axis of C2). `../SpecIsolation.tla` is reused unedited. A subagent ran
this on 2026-11-24. Nothing is committed.

## What the spec keeps and re-evaluates (HTML 0e292f4)

- `#create-navigation-params-by-fetching`: the COOP enforcement result starts from
  "navigable's active document's" URL, origin and opener policy. A traversal re-fetch goes through
  the same algorithm (`#attempt-to-populate-the-history-entry's-document`), so it is
  **re-evaluated against the document being left**, not against the entry's earlier state.
- `#apply-the-history-step`: re-fetch only "If targetEntry's document is null, or ... reload pending".
  Otherwise the kept document is used and no COOP step runs.
- `#activate-history-entry` → `#make-active`: "Set document's browsing context's WindowProxy's
  [[Window]]" to it. The navigable's active browsing context is "its active document's browsing context".
  So a restored document comes back **in its own old browsing context and group**, with that context's
  opener, and the old `WindowProxy` points at it again.
- `#obtain-browsing-context-navigation`, swap note: the old context is kept "such as ones in the
  back/forward cache". The document's crossOriginIsolated and agent cluster are its own, so they are kept.
- `#dom-window-closed`: true "if this's navigable is null". That holds while the opener's context
  is not active.
- `#unload-a-document`: intendToKeepInBfcache "must be false if oldDocument is not salvageable".
  The rest is UA choice. Active WebSocket objects make the document unsalvageable (`#make-document-unsalvageable`,
  reason "websocket"). Unload handlers and `Cache-Control: no-store` are UA-specific, so they are not axes.
- Consequence: the spec does **not** guarantee "severed stays severed". If a UA keeps a document that
  shares the opener's group, going back to it rejoins the opener. The upstream test
  `coop-navigated-history-popup` asserts severing after `history.go(-1)`, which holds only without bfcache.

## Model

- `HistorySeq.tla` folds the operations over a state: entries `[j, doc]`, the current index, and the
  browsing contexts `[opener, mode]`. `bcs[1]` is the context `window.open` made. The steps are `NavStep`
  (COOP check, forward pruning) and `TravStep(d, hit)`; `hit` is the UA's bfcache choice, feasible only if salvageable.
- Local decision ids, gated with `SI!C`: nav-switch, nav-blank, blank-inherit, nav-prune, trav-enforce,
  trav-noblank, trav-active-bc, restore-reuse-bc, restore-keep-coi, ws-unsalvageable (`false:`).
  Named mutants: `reevaluate-coop-on-restore`, `restore-opener` and `new-agent-cluster-on-restore`.
  That gives 13 local mutants; with SI's 55 there are **68**.
- Observations: `closed`, `opener`, `coi`, `hlen`, and `hit1`/`hit2` (the k-th traversal target was
  restored: `pageshow.persisted` with loadCount 1). Allowed values are **conditioned on the hits the
  same browser showed** (`Allowed(sc, k, cc, H)`). This removes the bfcache nondeterminism without hiding it.
- Sequence properties: Q1 is "once severed, never rejoined". Q2: sharing the opener's group implies
  COOP compatible with the opener. Q3: isolated implies own COOP+COEP. Q4: a restored document is
  unchanged. Q5: a re-fetch swaps iff it mismatches the active document.
- `HistoryMachine.tla` is the same runs as a state machine, over 37 120 initial (scenario, h) pairs
  and 147 200 states (43 s). Q2Inv, Q3Inv, FinalAgrees, RestoreKeeps, RefetchChecks, NoRejoinRefetch
  and Decides hold. **NoRejoin (Q1) fails** (`HistoryMachine-Q1.cfg`). The counterexample: an
  unsafe-none opener; the popup goes to A (unsafe-none), then to A with same-origin-allow-popups (swap),
  then back with h = TRUE, and the opener is rejoined.
- Whole space, unmutated (`HistoryEnum`): Q2–Q5 hold. Q1 fails on 993 of 17 280 scenarios, always
  with some hit TRUE. With no hits, Q1 holds. No mutant restores Q1 (even
  `reevaluate-coop-on-restore` fails it on longer sequences). Q2 is broken by neg:nav-switch,
  neg:coop-equal, neg:coop-same-origin, neg:popup-unsafe, neg:popup-opener-sap, neg:blank-inherit and
  neg:trav-enforce. Q4 is broken by all three restore mutants, neg:restore-reuse-bc and neg:restore-keep-coi.

## Scenarios and cost

- Axes (`gen.py`): start popup (opener COOP {un, sap, so, so+rc}) or noopener; sequence NB, NBF, NNB,
  NNB2 (`go(-2)`), NBN; per document {same-origin, cross-site} × COOP {un, sap, so, so+rc}, and
  {no, open} WebSocket on traversal targets. That gives **17 280** scenarios. Documents are the WPT back-forward-cache `executor.html` with
  header pipes, driven by `RemoteContext` and `prepareNavigation()`. `tests/resources/hobs.js` has 93
  lines and `hws.sub.js` 4.
- Pre-screen: `driver/enum.sh`, 3 parallel ranges, 1 191–1 317 s each, **354 classes**; one per class
  gives 354 scenarios (2.0 %), 1 805 rows per browser. 41 SI mutants equivalent on the space; all 13 local ones distinguishable.
- Run: podman `python:3.12-bookworm`, WPT clone 31362d122 (overlay), `--processes=2`,
  `--timeout-multiplier=10`, 2 repeats, 47 files of ≤ 8 scenarios. Chrome 158.0.8127.88: 618 s and
  557 s. Firefox 160.0.1: 2 314 s and 2 262 s.
- No `.error`/`.odd` rows. All rows repeat-consistent except 12 Firefox NNB2 `hit1` rows (mixed).

## Inclusion (1 805 rows per browser; {concrete, logical} and {concrete} identical)

| browser | inside | out |
|---|---|---|
| Chrome | 1 691 | 114 (`hit` rows only) |
| Firefox | 1 805 | 0 |

- Neither browser restored a document sharing the opener's group (every hit TRUE ends with opener
  FALSE), so the spec's rejoin branch (Q1 counterexample) was never exercised. Chrome: 288 hits.

## Mutant kills (68; 43 equivalent on the rows)

- Each browser kills **23 of 25** row-distinguishable mutants. Local kills (Chrome/Firefox rows):
  restore-opener 164/164, neg:nav-switch 184/224, neg:nav-prune 103/103, neg:trav-enforce 62/62,
  neg:trav-active-bc 34/34, neg:blank-inherit 50/48, neg:nav-blank 22/22, neg:restore-keep-coi 13/17,
  neg:restore-reuse-bc 4/4. All 14 SI COOP, popup and COI mutants distinguishable here are killed.
- Survivors (non-equivalent): `false:ws-unsalvageable` (its allowed set is a superset, so no inside
  row can kill it) and `neg:trav-noblank` (4 scenarios of the space; its class representative did not
  get the needed re-fetch).
- Equivalent on the rows but not on the space: `reevaluate-coop-on-restore` and
  `new-agent-cluster-on-restore`. They differ only when a document that shares the opener's group is
  restored, which neither browser does.
- Upstream expectations (`mkrows.py` `WptRows`): `coop-navigated-history-popup` (opener FALSE, closed
  TRUE) is inside and kills restore-opener; the WebSocket test (no bfcache) is inside; the **tentative**
  `back-forward-cache-closes-open-websocket-connection` wants bfcache and is **outside the model**
  (Chrome's behaviour). Locally (`driver/originals.txt`) Chrome fails the non-tentative WebSocket test
  and passes the tentative one; Firefox passes the former, PRECONDITION_FAILED on the latter; both pass
  `coop-navigated-history-popup`.

## Out-of-model rows (non-held)

| rows | browser | observed | allowed | classification | evidence |
|---|---|---|---|---|---|
| 114 `hit1`/`hit2` rows of scenarios whose traversal target held an open WebSocket | Chrome | TRUE | FALSE | browser deviation from "websocket" unsalvageable; not an isolation weakening (opener FALSE in every row) | `false:ws-unsalvageable` contains all 114 and loses 0 inside rows; upstream non-tentative WS test fails locally in Chrome, tentative one passes |

- No weaker-isolation value was observed; nothing is held (`held/` is empty).

## Hypotheses of the record

- **R1 (works): partly supported.** 100 % inclusion in Firefox, and 100 % in Chrome outside the
  WebSocket rows. 23/25 kills, including restore-opener and the re-fetch-path ids. Cost is comparable
  to the redirect fragment (below).
- **R2 (modelling cost limits): not supported.** The model has 191 lines, against 137 for redirect.
  The hard part was the nondeterministic UA choice. Conditioning on observed hits solved it.
- **R3 (not visible): supported for the restore branch.** bfcache hits are observable
  (`persisted` + loadCount). But both browsers refuse bfcache for documents that share a group with an
  opener, so the spec's rejoin branch and two named restore mutants are unobservable here.
- **R4 (many differences): partly supported.** There is one Chrome-vs-spec difference (WebSocket),
  matching an upstream tentative test. Firefox has nondeterministic hits on `go(-2)`. There are no COOP
  or opener differences.

## Cost and effect against the redirect fragment (E1)

| | redirect | history |
|---|---|---|
| model lines / local mutants | 137 / 10 | 191 / 13 |
| space / classes / run | 22 608 / 290 / 565 | 17 280 / 354 / 354 |
| pre-screen | 9.5 min | 3 × 21 min parallel |
| browser time, 2 repeats | Chrome 18 min, Firefox 36 min (1 process) | Chrome 20 min, Firefox 76 min (2 processes) |
| test components | hop.py + robs.js (85 lines) | hobs.js + hws.sub.js (97 lines), WPT bfcache executor reused |
| kills / distinguishable | Chrome 24/24, Firefox 23/24 | 23/25 each |
| model gaps found | P2c fails (known SAP case) | Q1 fails in the spec; spec-vs-upstream-test tension; selection key misses UA choice |

- Method change: key the pre-screen by UA choice too (`neg:trav-noblank` shows why).

## Limits

- Page-initiated `history.go` only; no reload, iframes, report-only COOP or Origin-Agent-Cluster keys;
  same-origin and cross-site hosts; ≤ 3 operations and documents; WebSocket is the only bfcache blocker;
  one machine, one version per browser, 500 ms settle.

## Files

- Model: `HistorySeq.tla`, `HistoryMachine.tla` (+ `.cfg`, `-Q1.cfg`), `HistoryEnum.tla` (cfgs from
  `driver/enum.sh`), `HistoryAllowed.tla` (+ `.cfg`, `-concrete.cfg`). Generator: `gen.py` (`space` →
  `HistorySpace.tla`, not kept; `select` → `scenarios.tsv`, `tests/`). Data: `observed.tsv`. `driver/`:
  `run.sh`, `incontainer.sh`, `enum.sh`, `check.sh`, `extract.py`, `mkrows.py`, `originals.txt`.
- Raw logs (job scratch `tmp/history/run/`), sha256: chrome r1 `9b048293…1d8e28aa`, r2 `66cebbcb…8bc396a3`;
  firefox r1 `53352187…bb32cff1`, r2 `c039900f…28dbd57d`. TLC outputs: `tmp/history/w/`.
