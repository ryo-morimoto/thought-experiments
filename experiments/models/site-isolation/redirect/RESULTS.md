# Redirect chains as state transitions: inclusion and intermediate-hop mutant kills

Follow-up to [../gen/RESULTS.md](../gen/RESULTS.md) for the record
[experiments/2026-11-24-redirect-sequence-model.md](../../../2026-11-24-redirect-sequence-model.md)
(tree node D1, redirect axis of C2). `../SpecIsolation.tla` is reused unedited. A subagent ran this on
2026-11-24. Nothing is committed.

## What the spec updates per hop (HTML 0e292f4)

- `#create-navigation-params-by-fetching`, loop over responses: "If navigable is a top-level
  traversable" → "Set coopEnforcementResult to the result of enforcing the response's opener policy".
  It runs for every response, redirects included. Child navigables skip it.
- `#obtain-coop` is called per response with that response and the reserved client. For
  same-origin it consults "a cross-origin embedder policy from response". So a redirect's own
  COEP decides whether that hop's value is `same-origin-plus-COEP`.
- `#coop-enforce`: the new result starts with needs-switch = "currentCOOPEnforcementResult's needs a
  browsing context group switch". So the flag **accumulates** and is never reset. It takes "url
  responseURL, origin responseOrigin, opener policy responseCOOP". The check compares the response
  with "currentCOOPEnforcementResult's origin" and its opener policy, i.e. **the previous
  response**, not the navigation source. isInitialAboutBlank is the active document's flag, so it is
  constant over the chain.
- `#check-browsing-context-group-switch-coop-value`: if isInitialAboutBlank, use
  `#check-browsing-context-group-switch-coop-value-popup`. That check exempts unsafe-none when the
  current value is same-origin-allow-popups.
- `#coop-enforcement-bcg-switch-report-only`: it is updated the same way, through "check if enforcing
  report-only COOP would require a browsing context group switch". It only sets a new virtual group
  id, and report-only headers are not on the axes, so it is not modelled.
- `#obtain-browsing-context-navigation`: "Let swapGroup be coopEnforcementResult's needs a browsing
  context group switch" (the final result). The optional swaps (non-HTTP(S) schemes, "browser UI",
  group size 1) do not apply to a popup. The new group's isolation mode comes from
  "navigationParams's cross-origin opener policy", which is the final response's. So only the final
  response's COEP makes the document isolated.
- Initial about:blank (`#creating-a-new-browsing-context` step "If creator's origin is same origin
  with creator's relevant settings object's top-level origin"): it takes the opener's top-level
  document's COOP.

## Model

- `RedirectSeq.tla`: `Enforce(blank, cur, r)` is one hop. `Chain` folds it over the responses.
  `Swap` is the final decision. `Severed`, `FinalMode` and `HLen` give the observations. It reuses
  `SI!ParsedCOOP`, `MatchCOOP`, `PopupSevered` and `COIMode`.
- Local decision ids, each gated with `SI!C`: hop-accumulate, hop-switch, hop-update, hop-blank,
  hop-coep, blank-inherit, final-swap and hop-same-entry. `neg:hop-accumulate` means no
  accumulation. `neg:hop-update` compares every response with the source.
- Two named mutants: `first-hop-only` and `final-hop-only`. Each checks one response against the
  source. With SI's 55 that gives **65 mutants**.
- `RedirectMachine.tla` is the same chain as a state machine. The state is (scenario, result, k,
  swapped), with one `HopStep` per response, then `Final`. Over all 22 608 scenarios there are 111 024
  states (13 s). The invariants `FlagIsAnyStep`, `FinalAgrees` and `PropsHold` and the properties
  `Sticky` and `Decides` hold.
- Sequence properties, whole space, unmutated. Hold: P1 (any step mismatching its predecessor
  severs), P1c (severing implies such a step), P2 (any response mismatching the source severs),
  P3 (an isolated final document is itself same-origin-plus-COEP), P4 (not severed ⇒ opener's
  mode). **P2c fails** (responses vs the source alone decide): TLC's counterexample is sap opener
  at A → unsafe-none hop at A → sap final at A, the chain of upstream
  `popup-redirect-same-origin-allow-popups`. P1 is broken by first-hop-only, final-hop-only,
  hop-accumulate, hop-switch, hop-update and final-swap (`RedirectEnum`).

## Scenarios and cost

- Axes (`gen.py`): opener COOP {un, sap, so, so+COEP rc}; start {blank: `window.open(chain)`;
  doc: the popup loads A with the opener's headers, then sets `location`}; 0..2 hops of
  {same-origin, same-site, cross-site} × {un, sap, so, so+rc}; final relation × COOP
  {un, sap, so} × COEP {un, rc}.
- That gives **22 608** scenarios. Hops are `tests/resources/hop.py` (302 with COOP/COEP); the
  final document is the WPT dispatcher executor with header pipes.
- Pre-screen (`RedirectEnum`, TLC 9 min 25 s): the scenarios fall into 290 classes, keyed by the
  pair of distinguished-mutant sets under {concrete, logical} and {concrete}. Up to 2
  representatives were taken per class, and 12 per class that no mutant distinguishes (seed
  20261124). That gives **565 scenarios** (2.5 %) and 2 260 rows.
- 41 SI mutants are equivalent on the whole space (fetch, CORP, OAC, Mixed Content, nested).
  No mutant distinguishable on the space is lost by the selection.
- Run: podman `python:3.12-bookworm`, WPT clone 31362d122 (overlay), `--timeout-multiplier=4`,
  2 repeats, 12 files of ≤ 60 scenarios. Browsers: Chrome 158.0.8127.88 (536 s and 535 s) and
  Firefox 160.0.1 (1 072 s and 1 068 s).
- All rows are consistent across repeats. There are no `.error` rows.
- Observations (`tests/resources/robs.js`): `closed` (the opener's `popup.closed` after 500 ms),
  `opener` (the popup's `window.opener != null`), `coi` and `hlen` (`history.length`).

## Inclusion (2 260 rows per browser)

| cfg | Chrome inside | Firefox inside |
|---|---|---|
| {concrete, logical} (`RedirectAllowed.cfg`) | 2 260 | 2 236 (24 out) |
| {concrete} | 2 260 | 2 236 (24 out) |

## Mutant kills (65 mutants; 41 equivalent on the rows and on the whole space)

The kill rule: an observation inside the unmutated set and outside the mutant's. Rows killed,
{concrete, logical}:

| mutant | min hops | Chrome | Firefox | upstream WPT exp. | 109 WPT rows |
|---|---|---|---|---|---|
| first-hop-only | 1 | 385 | 361 | killed | equivalent |
| final-hop-only | 1 | 408 | 384 | killed | equivalent |
| neg:hop-accumulate | 1 | 409 | 401 | killed | equivalent |
| neg:hop-update (compare with source) | 1 | 24 | **0 (survives)** | killed | equivalent |
| neg:hop-coep | 1 | 20 | 20 | killed | equivalent |
| neg:hop-switch / hop-blank / blank-inherit | 0 | 250 / 64 / 64 | 250 / 64 / 64 | killed / — / killed | equivalent |
| neg:final-swap / hop-same-entry | 0 / 1 | 717 / 492 | 693 / 492 | killed / — | equivalent |

- Chrome kills all 24 distinguishable mutants and Firefox kills 23. The 14 SI COOP, popup and COI
  mutants are killed by both.
- The 109 rows evaluate SI operators only, and no local id changes an SI operator. So all 10 local
  mutants are equivalent on them by construction.
- "upstream WPT exp." is the expected values of `coep-redirect`, `popup-redirect-same-origin-allow-popups`
  and `popup-redirect-cache`. These are 11 scenarios on these axes, none of them in the 109 rows
  (`mkrows.py` `WptRows`). All 11 expectations are inside the model, and they kill 8 of the 10 local
  mutants, including both intermediate-hop mutants.

## Out-of-model rows (non-held)

| rows | browser | observed | allowed | classification | evidence |
|---|---|---|---|---|---|
| 24 rows (`closed`, `opener`) of 12 scenarios. Each has a same-origin-allow-popups opener and starts blank. An unsafe-none response is exempted by the SAP popup step, then a later response is not unsafe-none. | Firefox | closed FALSE, opener TRUE | severed | browser deviation, known on wpt.fyi | `popup-redirect-same-origin-allow-popups.https.html`: Firefox 160.0.1 0/2 on wpt.fyi stable (run 5108994293891072, rev e00a7b14e8), Chrome 158 2/2. Locally (`driver/originals.txt`) Firefox fails 0/2 and Chrome passes 2/2. |

- Weaker isolation, but its defining chain is the public failing test, so it is described here;
  10 of the 12 scenarios generalise that chain to 2 hops. On all 12, Firefox equals
  `neg:hop-update` (each response compared with the source), which contains every Firefox row and
  loses none inside. Nothing else is out; Firefox passes `coep-redirect` and `popup-redirect-cache`.

## Hypotheses of the record

- **R1 (supported): supported for Chrome** (100 % inside, every distinguishable mutant killed,
  both hop-only ones included); **partly for Firefox** (both killed, compare-with-source rescued).
- **R2 (differs): supported for Firefox**, in one pattern, the known SAP-exemption-across-hops failure.
- **R3 (not visible): not supported.** Intermediate hops show in `closed`/`opener` and, through hop
  COEP, in `coi`. The shallowest distinguishing depth is 1 hop.
- **R4 (cost limits): not supported at this bound.** The space is 22 608 scenarios; pre-screening
  takes 9.5 min of TLC and runs 565 of them. Browser time is about 18 min (Chrome) and 36 min
  (Firefox) for 2 repeats.

## Limits

- Redirects only: no history traversal, bfcache, report-only COOP, noopener-allow-popups or sandbox.
- Top-level navigations without an opener (group-size-1 optional swap) are not observable with these
  signals and are not run; `doc` covers the non-initial branch. 500 ms settle as in `popup_test()`.
- `hop-same-entry` is a weak mutant (extra history entries). Axes are the author's; https only,
  one host configuration, one machine.

## Files

- Model: `RedirectSeq.tla`; `RedirectMachine.tla` + `.cfg` and `-P2c.cfg`; `RedirectEnum.tla` + `.cfg`;
  `RedirectAllowed.tla` + `.cfg` and `-concrete.cfg`.
- Generator: `gen.py` (`space` → `RedirectSpace.tla`, not kept; `select` → `scenarios.tsv`, `tests/`).
- Data: `observed.tsv`. `driver/`: `run.sh`, `incontainer.sh`, `originals.txt`, `extract.py`, `mkrows.py` (→
  `RedirectRows.tla`) and `check.sh`.
- Raw logs (job scratch `tmp/redirect/final/`), sha256: chrome r1 `92f5cb68…0f731`, r2 `cc62c84e…1abc`;
  firefox r1 `aba72243…594b`, r2 `61fb149b…2ec5`.
