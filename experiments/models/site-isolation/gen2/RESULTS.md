# Popup, sandbox, Origin-Agent-Cluster and CORP same-site axes: inclusion and mutant kills

Follow-up to [../gen/RESULTS.md](../gen/RESULTS.md) for the record
[experiments/2026-11-24-popup-sandbox-axes.md](../../../2026-11-24-popup-sandbox-axes.md).
The model is `../SpecIsolation.tla`, unedited. The steps it lacks are in `Gen2Model.tla`. A subagent
ran this on 2026-11-24. Nothing is committed.

## Generator (`gen2.py`)

The full space has four families, **873 scenarios** (`space.tsv`):

| family | axes | scenarios | rows per scenario |
|---|---|---|---|
| P popup | opener COOP × popup COOP (un, sap, so) × popup origin (same-origin, same-site, cross-site https, cross-site http) × {direct, `about:blank` then navigate, noopener} | 108 | `sev` |
| O OAC | top {https, https + COI, http} × `Origin-Agent-Cluster` of top, child 1 (www1, same site) and child 2 (same origin as child 1) ∈ {absent, ?0, ?1}; each scenario runs in its own noopener popup | 81 | 3 getters, `dd` (sync access after `document.domain`) |
| S sandbox | top COEP (un, rc, cl) × top COOP (un, so) × `sandbox` {none, allow-scripts, allow-scripts allow-same-origin} × child host relation × child COEP (un, rc) × child CORP (none, so, xo) | 324 | load, coi, sec, `self.origin` opaque, no-cors fetch to own URL origin, to the other https site, to http, `<img>` at http URL on the https port |
| C CORP / images | top {https, http} × COEP (3) × target relation × target scheme {https, http, http on the https port} × CORP (none, so, ss, xo) × {`fetch()`, `<img>`} | 360 | one result |

The http-on-the-https-port target (`http://host:8443/…`) makes the Mixed Content upgrade observable:
after the upgrade, a TLS server answers (`served = TRUE` in `ImageResult`).

## Model steps added in `Gen2Model.tla`

These are wrapped as `G2(id, e)`, with the same `neg:` and `false:` mutants as `C(id, e)`. 9 mutants:

- `g2-sb-opaque`: "the sandboxed origin browsing context flag … return a new opaque origin"
  ([#sandboxOrigin](https://html.spec.whatwg.org/#sandboxOrigin)).
- `g2-pp-self`: "cross-origin-isolated … default allowlist of 'self'"
  ([#cross-origin-isolated-feature](https://html.spec.whatwg.org/#cross-origin-isolated-feature)).
  An opaque origin never matches `self`.
- `g2-noopener`: "If noopener is true … creating a new top-level traversable"
  ([#noopener](https://html.spec.whatwg.org/#noopener)).
- `g2-coop-secure`: "If reservedEnvironment is a non-secure context, then return policy"
  ([#obtain-coop](https://html.spec.whatwg.org/#obtain-coop)).
  `PopupSevered` takes raw header values, so an http popup's COOP needs this step.
- `g2-blank-coop`: the initial `about:blank` takes the opener's top-level COOP
  ([#creating-a-new-browsing-context](https://html.spec.whatwg.org/#creating-a-new-browsing-context)).
  It applies to direct opens as well, so the model predicts direct = `about:blank` then navigate.

An opaque origin is a record with scheme `opaque`. `Secure` is FALSE for it, so `ProhibitsMixed` falls
back to the ancestor clause (`mc-ancestor`). Navigation CORP runs against the container document:
"cross-origin resource policy check with navigable's container document's origin"
([#create-navigation-params-by-fetching](https://html.spec.whatwg.org/#create-navigation-params-by-fetching)).

**OAC parameter** `OACParam` (not a mutant): `spec` means requestsOAC is true only for `?1`
([#create-new-agent-and-window](https://html.spec.whatwg.org/#create-new-agent-and-window)).
`7617` is unmerged [whatwg/html#7617](https://github.com/whatwg/html/pull/7617): in a secure context, an
absent header also means origin-keyed, and `?0` keeps site keying. The cfgs are
`Gen2Allowed-{spec,7617}-{both,concrete}.cfg`, where `both` = COIChoice {concrete, logical}.

## Pre-screen (`Gen2Enum.tla`, no browsers)

- 64 mutants: 55 old (33 `neg:`, 16 named, 6 `false:` fixes) plus 9 `g2`. On the full space, 63 are
  distinguishable under all four cfgs. The equivalent one is `coi-ignore-secure`: no http top
  carries COOP + COEP here, and gen/ kills it.
- `gen2.py select` picks 32 scenarios that cover each distinguishable mutant at least twice (greedy).
  It adds a 30 % random sample per family × top-configuration stratum (seed 20261124), giving
  **285 scenarios** (P 43, O 27, S 104, C 111) in 16 test files.
- TLC: 5 s per `Gen2Enum` cfg, 2–3 s per `Gen2Allowed` cfg.

## Run cost

- podman `python:3.12-bookworm`, WPT clone 31362d122, `--timeout-multiplier=4`, Chrome 158.0.8127.88 and
  Firefox 160.0.1, 2 repeats, in parallel containers.
- `wpt run` per repeat: Chrome 137 s / 127 s, Firefox 203 s / 193 s. Wall time including the browser
  install: 300 s and 429 s. All 64 file runs were OK. Every row was consistent across repeats. No
  frame was late, and no sandbox frame was alive without reporting (`noreport`: 0).
- One earlier smoke run (1 repeat) gave the same values.

## Inclusion

| cfg | Chrome (709 rows) | Firefox (688 rows) |
|---|---|---|
| OAC `spec`, {concrete, logical} or {concrete} | 696 inside, 13 out (O) | 682 inside, 6 out (S) |
| OAC `7617`, either COIChoice set | **709 inside** | 669 inside, 19 out (13 O + 6 S) |

Chrome is inside the model exactly when the #7617 default is assumed. Firefox is closest to the `spec`
value. The browsers agree on every P and C row and on every Mixed Content row.

| rows | browser | observed | allowed | classification |
|---|---|---|---|---|
| O001–O003 (all headers absent), O007 g0 (top absent): 13 | Chrome | origin-keyed, `dd` FALSE | site-keyed under `spec` | browser follows #7617. This is a known wpt.fyi deviation (Chrome fails the OAC tests, ../observe/RESULTS.md). Direction: stricter. |
| same 13 | Firefox | site-keyed | origin-keyed under `7617` | parameter value, not a deviation |
| S174, S288 (cross-origin child, CORP xo), S210 (same-site child with allow-scripts allow-same-origin) in a COI top: `coi` | Firefox | TRUE | {FALSE} | known wpt.fyi deviation: `cross-origin-isolated-permission-iframe.https.window.html`, Firefox 3/8 (../gen/RESULTS.md). The child keeps a cross-origin tuple origin. |
| S130, S184, S185: top COEP rc, `sandbox=allow-scripts`, same-host child, COEP rc, CORP none / same-origin: `load` | Firefox | blocked | {loaded} | browser deviation, stricter. Firefox seems to check CORP against the opaque origin, not the container document. No WPT test for this was found in the clone. |

Nothing was held: no out-of-model value is weaker than the model except the 3 Firefox `coi` rows,
and those are the publicly failing permissions-policy test. No sandboxed opaque-origin frame reported
crossOriginIsolated TRUE. Every popup severed where the model severs. Every no-CORP cross-origin
load under COEP was blocked.

## Mutant kills

| | {concrete, logical} | {concrete} |
|---|---|---|
| gen2 alone, old 55 (Chrome = Firefox, both OAC values) | 53 | 54 |
| gen2 alone, 9 `g2` | 9 | 9 |
| gen/ (29–31) ∪ 109 WPT rows (41–43) | 51 | 53 |
| gen2 ∪ gen/ ∪ WPT | **53** | **55 (all)** |

- **All 24 previously equivalent mutants are killed**, in both browsers and under both OAC values.
  Kill rows (Chrome, `spec`, family): COOP / popup, 9 mutants, P 2–21 rows; OAC, 7 mutants,
  O 3–87; `samesite-scheme`, `samesite-as-origin`, `neg:corp-ss-*`, C 5–13; `nocors-site-basic`, C 29;
  `neg:mc-upgrade`, C 36 + S 66; `false:mc-upgrade`, C 6 + S 49; `false:mc-ancestor`, S 7 (fetch to
  http from a sandboxed opaque frame: only the ancestor clause makes it mixed).
- 22 of the 24 were already killed by the 109 WPT rows. Only `false:mc-ancestor` and
  `false:mc-upgrade` are new beyond the gen/ ∪ WPT union. With them the union reaches 53/55 and 55/55.
- Survivors under {concrete, logical}: `coi-ignore-secure` and `coi-coop-only`, as before. They only add
  TRUE, and the logical branch allows FALSE. `coi-ignore-secure` is equivalent on the gen2 space
  (the axis it needs is an http top with COOP + COEP, which only gen/ has).
- Under `7617`, the OAC kill-row counts change (e.g. `neg:oac-secure` from 24 to 53 rows in Chrome),
  but the kill sets do not.

## Hypotheses of the record

- **R1 (distinguishable): supported.** 24/24 are killed. 2 of them were not reachable by any earlier row.
- **R2 (many out-of-model values): not supported.** There are 3 patterns. One is the OAC default
  (a parameter). One is the known permissions-policy failure. One is a stricter Firefox sandbox
  navigation check (3 rows).
- **R3 (cost limits): not supported at this bound.** The popups ran 43 scenarios at about 1–2 s each.
  The whole run took 5–7 min per browser for 2 repeats.
- **R4 (still indistinguishable): not supported.** Only `coi-ignore-secure` is equivalent, and only
  on this space. Its axis (http top, COOP + COEP) is outside gen2 and inside gen/.

## Limits

- The axes are the author's choice. Popup lineage depth is 1, and the opener is always top-level
  (a popup from a cross-origin iframe is not modelled). There are no redirects, history, bfcache,
  service workers, sandboxed popups or `allow=` attributes.
- `Gen2Model` steps are the author's reading. `ODD` treats document.domain as effective iff both
  documents are site-keyed with equal keys.
- `sev` is `popup.closed` plus `window.opener` after 500 ms, as in WPT's popup-test.js. With noopener
  only the opener is seen.
- Ports are not modelled, so http-on-the-https-port targets are run only from https tops.
- The random sample is 30 %. Inclusion is measured on 285/873 scenarios, not on the full space.
- One machine, one host configuration, no Safari.

## Files

- `gen2.py` (space / select / tests), `space.tsv`, `selected.tsv`, `Gen2Space.tla`, `tests/` (16 files and
  `resources/`: `gobs2.js`, `sframe.py`, `oac-top.py`, `oac-child.py`, `res.py`, `img.py`).
- `Gen2Model.tla`, `Gen2Enum.tla` + 4 cfgs, `Gen2Allowed.tla` + 4 cfgs, `observed.tsv`.
- `driver/`: `run.sh`, `incontainer.sh`, `extract.py`, `mkrows.py` (→ `Gen2Rows.tla`), `tlc.sh`, `analyze.py`.
- Raw logs are in job scratch `tmp/gen2/final/` (not committed). sha256: chrome r1 `ef4208b0…39cd`,
  r2 `b5b9eb45…ce00`; firefox r1 `e3b466c7…f6b36a`, r2 `fddb9634…1a52`.
