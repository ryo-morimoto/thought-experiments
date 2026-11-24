# Frozen-model holdout on the relational-type gaps: inclusion, out-of-model rows and kills

Pre-registered in [experiments/prereg/2026-11-24-frozen-holdout.md](../../../prereg/2026-11-24-frozen-holdout.md)
(commit bf5e9f9, tag `prereg-frozen-holdout-2026-11-24`; model commit 94deed8) for the record
[experiments/2026-11-24-frozen-holdout.md](../../../2026-11-24-frozen-holdout.md) (tree nodes C10, C2).
The frozen models `../SpecIsolation.tla`, `../gen/GenModel.tla` and `../redirect/RedirectSeq.tla` are
used unedited. A subagent ran this on 2026-11-24. Nothing here is committed except the registration.

## What ran

- Scenarios were generated only after the registration commit, with seed 20261125 (`gen_holdout.py space`;
  selection seed 20261126).
- Sites a, b, c, d (`web-platform.test`, `not-web-platform.test`, and two alternate hosts added inside the
  container: `web-platform-c.test`, `web-platform-d.test`). Hosts: bare, www, www1, www2. Schemes: https, http.
- **N (nested frames, GenModel):** one representative per coarse type of (top, l1, l2) (66 types). Axes:
  top COEP × COOP, per-level COEP × CORP, fetch target {fresh cross-site https, same-site https, same-host http}.
  Pre-screen space 19 008, which gave 389 classes. **1 190 scenarios** were run.
- **R (popup redirect chains, RedirectSeq):** one representative per type of (A, final) (5), (A, hop, final)
  (33) and (A, hop1, hop2, final) (269). Hops include http and distinct cross-site origins. Pre-screen space
  19 488, which gave 420 classes. **880 scenarios** were run.
- Pre-screen (`HoldEnum.tla`, 4 TLC chunks, 2 in parallel): 606 + 472 s, then 375 + 539 s, about 19 min of wall time.
- Browsers: Chrome 158.0.8127.88 and Firefox 160.0.1, 2 repeats, podman, WPT 31362d122 (overlay).
  - N: 1 082 s (Chrome) and 1 076 s (Firefox) of wall time, about 520 s per repeat.
  - R: 1 601 s (Chrome, about 780 s per repeat) and 3 304 s (Firefox, about 1 630 s per repeat).
  - All 56 file runs were OK. Every row was consistent across repeats. `LATE` was none, and there
    were 0 R `error` rows.
- Rows: N 6 759 per browser, including 12 top rows (one per file). R 3 520 per browser.

## Relational-type coverage (rule 5; `driver/types.py`)

| family | types possible | types in run | types with rows in both browsers |
|---|---|---|---|
| N (top, l1, l2) | 66 | 66 | 66 |
| R (A, final) | 5 | 5 | 5 |
| R (A, hop, final) | 33 | 33 | 33 |
| R (A, hop1, hop2, final) | 269 | 269 | 269 |

Compared with adequacy/RESULTS.md (gen 52/66, redirect 9/66), the gap on these axes is closed. The run includes
three mutually cross-site origins, two distinct http origins, http hops, and distinct cross-site hops.

## Inclusion (rule 1)

| cfg | Chrome inside | Firefox inside |
|---|---|---|
| **N-both** (primary: WithPP TRUE, {concrete, logical}) | 6 759 / 6 759 | 6 595 / 6 759 (164 out) |
| N-concrete | 6 759 | 6 595 (164 out) |
| N-noPP-both | 6 759 | 6 759 |
| N-noPP-concrete | 6 595 (164 out) | 6 759 |
| **R-both** (primary) | 3 520 / 3 520 | 3 470 / 3 520 (50 out) |
| R-concrete | 3 520 | 3 470 (50 out) |

## Out-of-model rows (rule 2)

| rows | browser | observed / allowed | class | evidence |
|---|---|---|---|---|
| 164 N `coi` rows. The top is COI (rc or cl, COOP so). The level, or a link up to the top, is cross-origin (same-site or cross-site, any of the 3 sites). 98 rows are at level 1, 66 at level 2. | Firefox | TRUE / {FALSE} | **K1**, weaker | Same mechanism as gen/RESULTS.md: Firefox does not apply the `cross-origin-isolated` default allowlist `self`. That is the public failure of `cross-origin-isolated-permission-iframe.https.window.html` (Firefox 3/8). With WithPP FALSE, Firefox is fully inside and Chrome has the mirror 164 rows (FALSE where the no-PP model says TRUE). `driver/outrows.py` groups them. |
| 50 R rows (`closed` FALSE, `opener` TRUE) of 25 scenarios. All have a SAP opener and a blank start; 7 have 1 hop and 18 have 2. Hops include http and cross-site c/d origins. | Firefox | not severed / severed | **K2**, weaker | `HoldRescue.tla`: all 50 rows are inside `neg:hop-update`'s sets (each response is compared with the source), and that mutant loses 0 inside Firefox rows. This is the public failure of `popup-redirect-same-origin-allow-popups.https.html` (Firefox 0/2), the same pattern as redirect/RESULTS.md, now also through http and third-site hops. |

- No P-only, M, T or U pattern. Nothing was held: both weaker-isolation patterns are the registered public
  K patterns. The note is `tmp/holdout/w2/held/NOTE.txt`.
- Chrome is inside on every row of both families under the primary cfgs.

## Mutant kills (rule 3; `driver/score.py`, `driver/famkill.py`)

K_prev is computed on the committed rows of gen/, gen2/ and redirect/ with the registered sets (`driver/prev.sh`).
Out of 141 distinct names, it is 128 / 126 under {concrete, logical} and 131 / 129 under {concrete} (Chrome / Firefox).

| cfg | killed N (of 115) C / F | killed R (of 141) C / F | killed now, not in K_prev |
|---|---|---|---|
| both (primary) | 59 / 59 | 54 / 52 | **`coi-ignore-secure`, `false:coi-insecure`** (both browsers, by R) |
| concrete | 65 / 65 | 55 / 53 | none |

- Per family against the previous family on the same model:
  - N vs gen/ newly kills `nocors-site-basic`, `false:fetch-same-origin`, `neg:mc-upgrade` and `true:mc-upgrade`,
    with the same-site and http fetch targets. All four were already in K_prev through gen2/.
  - R vs redirect/ newly kills `coi-ignore-secure` and `false:coi-insecure`, with http final documents. That is the
    effect adequacy/RESULTS.md predicted for http finals. No kill was lost.
- Under {concrete}, those two R kills were already in K_prev through gen/, so the identity-level change exists
  only under the primary COI set.
- Still unkilled by everything: `false:coop-one-unsafe`, `false:corp-first-pass`, `false:fetch-cors`,
  `true:coep-cl-strips`, `true:secure-ctx-top` and the `true:hop-*`/`true:blank-inherit` group. Firefox also leaves
  `neg:hop-update` and `false:hop-update` unkilled (it behaves like `neg:hop-update`). Under {concrete, logical},
  `true:coi-mode` is unkilled too. Equivalent on the rows: 50 (N), 86 (R).

## Hypotheses (rule 4)

- **R1 (preserved): supported.** All out-of-model rows are K1 or K2, both registered public patterns. Chrome is
  100 % inside, and Firefox is 97.6 % (N) and 98.6 % (R) inside.
- **R2 (new gaps): not supported.** There is no M or U pattern, even with 3 sites, http hops and a fresh-site target.
- **R3 (kills change): supported, narrowly.** Under the primary COI set, R kills 2 mutants outside K_prev
  (`coi-ignore-secure`, `false:coi-insecure`). They need an http final document, a type the all-https redirect
  space lacked. Under {concrete} nothing new is killed.

## Deviations from the registration

- None in rules, models, parameters, seeds or selection.
- Added after the registration, for scoring only:
  - `HoldRescue.tla`, which checks rule 2's K2 condition. The registered tools had no printer for it.
  - `driver/outrows.py`, `driver/famkill.py` and `driver/types.py`, which are summaries.
- Before registration, a slip (recorded in the prereg): the dry run's kill counts were seen.

## Limits

- The axes and mutants come from the model's vocabulary (C9).
- Types are coarse. Same-host relations are not stratified.
- The pre-screen is a sampled subspace of the full product, so equivalence is measured on that subspace.
- OAC is not exercised by these families.
- Sites c and d use the stock certificate with errors ignored, as for a and b.
- One machine, no Safari.

## Files

- Generator: `gen_holdout.py`. Selected scenarios: `scenarios.tsv`. Tests: `tests/` (28 files plus
  `resources/`: `hobs.js`, `hrobs.js`, and `frame.py`, `res.py` and `hop.py` copied from gen/ and redirect/).
- TLA+: `HoldDecode`, `HoldMutants`, `HoldEnum`, `HoldAllowed` (+ 6 cfgs), `HoldPrev*` (+ 6 cfgs), `HoldRescue`.
- Data: `observed.tsv` (N via gen/driver/extract.py, R via redirect/driver/extract.py).
- Drivers in `driver/`: `run.sh`, `incontainer.sh`, `tlc.sh`, `prev.sh`, `mkrows.py`, `score.py`, `famkill.py`,
  `outrows.py`, `types.py`.
- Raw logs are in job scratch `tmp/holdout/w2/final/`. sha256: N chrome r1 `60248d4a…36e5`, r2 `271571c6…bd9d`;
  firefox r1 `16be89a6…58be5`, r2 `9de1873c…c3c6`. R chrome r1 `84f5f0fb…c758`, r2 `9a337c0e…3f3f`; firefox r1
  `8afbd344…b344`, r2 `eb48a665…84b5`.
