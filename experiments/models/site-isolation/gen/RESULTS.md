# Axis-generated nested-frame scenarios: inclusion and mutant kills

diy/litmus-style follow-up to [../observe/RESULTS.md](../observe/RESULTS.md) for the record
[experiments/2026-11-24-axis-generated-scenarios.md](../../../2026-11-24-axis-generated-scenarios.md).
The scenarios are generated from structural axes, not taken from WPT. The model is `../SpecIsolation.tla`
at 3b9239d, unedited. A subagent ran this on 2026-11-24. Nothing is committed.

## Generator (`gen.py`)

- Top (level 0): scheme {https, http} × COEP {unsafe-none, require-corp, credentialless} × COOP
  {unsafe-none, same-origin}. That gives 12 configurations, one test file each (`tests/top-*.sub.html` + `.headers`).
- Each child level: scheme × host relation to its parent {same host, same site/other host, other
  site} × COEP (3) × response CORP {none, same-origin, cross-origin}. That gives 54 configurations. Frames are
  served by `tests/resources/frame.py`, which sets the headers from the query.
- The relation axis is on hosts. "Same host" with another scheme is a different origin.
- Depth 0..2: the full space has 12 + 648 + 34 992 = **35 652** scenarios.
- Run: depth 0 and 1 exhaustively (12 + 648). For depth 2, for each top and child configuration, 2
  grandchild configurations drawn with seed 20261124, giving 1 296. Total **1 956 scenarios**.
- Every combination is kept, including the ones Mixed Content must block. Coverage per axis value is
  even by construction: each child value covers 1/3 or 1/2 of the depth-1 scenarios. For depth-2
  values, each count is between 412 and 663 (`driver/analyze.py`).
- Observations (`tests/resources/gobs.js`, passing subtests `OBS <sid>.<level>.<kind> :: v`): `coi`
  and `sec` (crossOriginIsolated, isSecureContext) per level; `load` (`loaded` iff the child's
  postMessage to top arrives within 12 s, batches of 27); `fetch`/`fetchc` from the deepest document,
  no-cors to the other site's https bare host without CORP (`fetchc`: `credentials: "include"`).
- `onload` is recorded but not mapped: Chrome fired it for 204 frames that never ran (error pages).

## Allowed sets (`GenModel.tla`, `GenAllowed.tla`, `GenEnum.tla`)

- `GenModel` composes SpecIsolation operators per level: `TopCtx`, `EffectiveCOEP(Ctx)`, `ChildCtx`,
  `NavChild` (level i from level i−1's context and policy-container COEP), `SecureCtx`,
  `CrossOriginIsolated`, `FetchResultCtx`. `ChildCtx` keeps `top`, so depth 2 needs no new operator.
- One step is not in SpecIsolation ("no permissions policy"): `PP`. The `cross-origin-isolated`
  feature has default allowlist `self`, so a child's getter is TRUE only if every link up to the top
  is same-origin. `WithPP = FALSE` drops it.
- The COI choice is {concrete, logical} (union per row) or {concrete}. Rows of a level the model does
  not load are unconstrained; their `load` row carries the difference.
- Mutants (55): 33 `neg:` MechMutants, 16 named Mutants and 6 `false:` FixMutants. As before, m is
  killed iff some observation is inside `Allowed(none)` and outside `Allowed(m)`.
- `GenEnum` evaluates the whole 35 652-scenario space, without browsers, to find mutants that no
  observation on these axes can kill.

## Run cost

- podman `python:3.12-bookworm`, WPT clone 31362d122, `--timeout-multiplier=4`, 2 repeats, Chrome and
  Firefox in parallel containers. The clone is mounted as an overlay (`:O`), so the host copy is
  untouched.
- Firefox 160.0.1 in both repeats. Chrome 158.0.8127.36 (r1) and 158.0.8127.88 (r2): `--install-browser` picked up a
  stable update.
- One repeat of the 12 files takes about 10.5 min per browser (r2: 625 s Chrome, 617 s Firefox).
  The http tops take 28 s per file and the https tops 63–76 s.
- Repeat 1 lost about 5.7 h on one file (`top-https-cl-un`) in both containers at once (host
  apparently suspended); Firefox's run of it was CRASH and was replaced by one rerun (97 s).
- TLC: 18 s per `GenAllowed` cfg, 181 s for `GenEnum`.
- All 8 280 mapped rows per browser are consistent across both repeats. No frame message arrived after its
  batch was recorded (`LATE :: none`).

## Inclusion (8 280 rows per browser)

| cfg | Chrome inside | Firefox inside |
|---|---|---|
| {concrete, logical}, with PP (`GenAllowed.cfg`) | 8 280 | 8 254 (26 out) |
| {concrete}, with PP | 8 280 | 8 254 (26 out) |
| {concrete, logical}, SpecIsolation as is (no PP) | 8 280 | 8 280 |
| {concrete}, no PP | 8 254 (26 out) | 8 280 |

The browsers agree on every `load`, `sec` and `fetch` row. They are inside the model on all of
them, including all Mixed Content blocks and every `sec` = FALSE for an https child under an http top.

| rows | browser | observed | allowed | classification | evidence |
|---|---|---|---|---|---|
| 26 `coi` rows: https child with CORP cross-origin, cross-origin to its parent, in a COI group (tops `https/rc/so`, `https/cl/so`; 24 at level 1, 2 at level 2) | Firefox | TRUE | {FALSE} with PP | browser deviation, known on wpt.fyi | `html/cross-origin-embedder-policy/cross-origin-isolated-permission-iframe.https.window.html`: Firefox 160.0.1 3/8 on wpt.fyi stable (run 5108994293891072, rev e00a7b14e8), Chrome 158 8/8. locally (`driver/originals.sh`) Firefox also passes 3/8 and fails the cross-origin "(undefined)" subtest; Chrome passes 8/8 |
| same 26 | Chrome | FALSE | {TRUE} without PP, concrete only | model gap: SpecIsolation has no permissions policy | the same test expects FALSE |

These rows report crossOriginIsolated = TRUE where the PP reading says FALSE, so the deviation
goes towards weaker isolation. It is already a public failure, so it is described here and nothing
was held. Nothing else is outside the model.

## Mutant kills (55 mutants)

| | killed, {concrete, logical} | killed, {concrete} | equivalent on the rows |
|---|---|---|---|
| generated, Chrome | 29 | 31 | 24 |
| generated, Firefox | 29 (same set) | 31 | 24 |
| 109 WPT rows (../observe, fixed model) | 41 | 43 | 12 (incl. all six `false:`) |
| union of both | 51 | 53 | — |

- **The three nested-frame fixes are now killed**, in both browsers, already at depth 1. Rows of Chrome's
  kill sets, at depth 1 / depth 2:

  | mutant | depth 1 | depth 2 |
  |---|---|---|
  | `false:secure-ctx-top` | 270 | 805 |
  | `false:nav-coep-adherence` | 20 | 60 |
  | `false:nav-corp-check` | 32 | 86 |
  | `false:mc-block` | 78 | 353 |

  `false:secure-ctx-top` is killed by `sec` and also by `fetch` (with it, an https child under an
  http top applies its require-corp COEP; both browsers return `opaque`). The `neg:` forms of the
  three ids are killed too. On the 109 rows all six were equivalent.
- Also new beyond the 109 rows: `cl-ignore-creds`, `crossorigin-as-site` and `neg:coep-cl-strips`.
  These were the three old equivalents. Credentialless children and `fetchc` reach them.
- Survivors under the union are `coi-ignore-secure` and `coi-coop-only`, as in ../observe. They
  only add TRUE, and the logical branch allows FALSE. With {concrete} both are killed.
- **Equivalent on the whole generated space (`GenEnum`)** — the same 24 as on the sampled rows, so
  the sample loses no discrimination relative to the full space. Every mutant distinguishable on the
  35 652 scenarios is killed:
  - OAC, COOP and popup mutants: there is no such observation on these axes.
  - `samesite-scheme`, `samesite-as-origin`, `neg:corp-ss-*`: no CORP same-site value.
  - `nocors-site-basic`: the target is always cross-site.
  - `neg:mc-upgrade`, `false:mc-upgrade`: no `<img>`.
  - `false:mc-ancestor`. With navigated documents only, a non-secure document under a secure ancestor
    is itself blocked by Mixed Content, so the ancestor clause never decides. It needs srcdoc,
    about:blank or other unmodelled creators.
- Shallowest distinguishing depth: 0 for most mutants. It is 1 for `cl-ignore-creds`,
  `crossorigin-as-site`, `neg:mc-ancestor`, `false:mc-block`, and both forms of `secure-ctx-top`,
  `nav-corp-check` and `nav-coep-adherence`. No mutant needs depth 2.

## Hypotheses of the record

- **R1 (visible): supported.** All three fix mutants and `false:mc-block` are killed; Chrome is
  100 % and Firefox 99.7 % inside.
- **R2 (many out-of-model values): not supported.** One pattern of 26 rows, about permissions
  policy, which the model lacks; which browser is "out" depends on whether PP is added.
- **R3 (cost limits): not at this bound.** About 21 min of browser time per browser for 2 repeats,
  one generator and three small resources. Depth 2 exhaustive is 27× the sampled count (hours per
  repeat, estimated, not measured), and `GenEnum` shows it adds no mutant discrimination.
- **R4 (observations don't reflect the fixes): not supported** for G1/G2. It is supported for
  `mc-ancestor` and `mc-upgrade`, which these observations cannot reach.

## Limits

- The axes were chosen by the author. Not covered: redirects, history, popups, sandbox, srcdoc /
  about:blank, `allow=` attributes, CORP same-site, same-site fetch targets and images.
- The `PP` step is the author's reading, added outside SpecIsolation. Its only effect is on `coi` rows.
- Load is inferred from a postMessage within 12 s. A slow frame would be counted as blocked, but none
  arrived late.
- `fetch` and `fetchc` never differed, so request credentials were not observable.
- One host configuration, one machine. Chrome's version changed between repeats, but its values did not.

## Files

- Generator and generated files: `gen.py`, `scenarios.tsv`, `tests/`.
- `driver/`: `run.sh`, `incontainer.sh`, `originals.sh` (the WPT test above), `extract.py` (raw logs
  → `observed.tsv`), `mkallowed.py` (→ `GenRows.tla`), `check.sh` (TLC), `analyze.py`.
- TLA+ modules and cfgs: `GenModel.tla`, `GenAllowed.tla` + 4 cfgs, `GenEnum.tla` + cfg.
- Raw logs (job scratch `tmp/gen/final/`, not committed), sha256: chrome r1 `b12f913e…d8148`, r2
  `c20c8113…16836`; firefox r1 (spliced) `bb9dbe3e…0afe`, r2 `b6619d41…92468`.
