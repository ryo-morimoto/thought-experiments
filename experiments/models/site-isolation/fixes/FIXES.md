# Fixes for three gaps in SpecIsolation, and whether three methods see them

Gaps from [havoc/RESULTS.md](../havoc/RESULTS.md) and [observe/RESULTS.md](../observe/RESULTS.md). Written by a subagent on 2026-11-23. The readings of the spec are the author's. Nothing is committed yet.

## Changes to `../SpecIsolation.tla`

Every new step is `C(id, e)` with an id in `FixIds` (also in `DecisionIds`). `Mutant = "false:<id>"` omits that one step. One string turns off only one step, so the "before" figures below come from the HEAD copy (9a7bab9) run in scratch. Old operator signatures are unchanged: `FetchResult(o,…) = FetchResultCtx(TopCtx(o),…)`, `EffectiveCOEP`, `KeyKind`, `RequestsOAC` likewise.

| gap | id | operator | spec (HTML 0e292f4, Fetch d7fc0fd, Mixed Content ED) |
|---|---|---|---|
| G1 | `secure-ctx-top` | `SecureCtx(ctx)`, `ctx = [self, top]`; used by `EffectiveCOEPCtx` and `RequestsOACCtx` | HTML #secure-context: decided by "environment's top-level creation URL"; #obtain-an-embedder-policy step 2 |
| G2 | `nav-corp-check` | `NavChildPC`: CORP check with forNavigation against the container document | HTML #create-navigation-params-by-fetching ("navigable is a child navigable") |
| G2 | `nav-coep-adherence` | `NavChildPC`: parent compatible, child not → error | HTML #check-a-navigation-response's-adherence-to-its-embedder-policy |
| G3 | `mc-ancestor` | `ProhibitsMixed`: own origin or ancestor's is trustworthy | MIX #categorize-settings-object (4.3) |
| G3 | `mc-upgrade` | `FetchResultDest`, dest `image`: scheme set to https, port kept | MIX #upgrade-algorithm (4.1) |
| G3 | `mc-block` | blockable mixed request (fetch, iframe) → error | MIX #should-block-fetch (4.4) |

- `coi-insecure` (top-level COOP) and `corp-ss-scheme` (Fetch's origin-scheme test) keep `Secure(o)`.
- `ImageResult(o, coep, r, served)`: `served` says whether a TLS server answers at the upgraded URL. It is a fact about the target, not a browser choice.
- New properties, next to the old ones:
  - `OptInOnlySecureLifted`: the old premise (https origin), quantified over contexts.
  - `OptInOnlySecureCtx`: premise "secure context".
  - `OptInOnlyPC`: premise on the policy container's COEP.
  - `COIOnlyWithOptInTop`.
  - `COIOnlyWithOptInNested`: the navigation response is same-origin or opted in, and the child's no-cors bytes arrive without credentials or with opt-in.
- `OptInOnlySecure` is unchanged *by construction*: it quantifies over top-level documents only. Its TRUE is no evidence about G1.

## G3: why w014 errors

- WPT `fetch/cross-origin-resource-policy/scheme-restriction.https.window.js` (clone 31362d122) loads an `<img>` from `HTTP_REMOTE_ORIGIN`, i.e. `http://www1.web-platform.test:8000`.
- MIX 4.1 upgrades an image with initiator "" and "set request's URL's scheme to https". The note says the port is not modified, so `https://www1…:8000` goes to wptserve's plain-HTTP port.
- Chrome's log says "This request was automatically upgraded to HTTPS". Both browsers' runs log a wptserve `code 400, message Bad request version` with TLS ClientHello bytes, at the time of this test file. This is inference from the timing: the port is not in the line.
  - Chrome: job scratch `tmp/observe/logs/obs/chrome-fetch-https.https-r1-raw.log`, sha256 `21d53c0ecf335b3fa021f93b873ec27f8d0c71543d5b88ba0dedfe6fb69fce4c`.
  - Firefox: `tmp/observe/logs/obs/firefox-fetch-https.https-r1-raw.log`, sha256 `8cc3b02bea44e35418f75066c0803d35f7358ece96ee3f66f115c5a475e24bfe`.
- So the test can't pass under current Mixed Content plus wptserve's ports. The model now says `error` for it (`served = FALSE`), and with `served = TRUE` it says load.
- `served = FALSE` is an input I set from wptserve's config (`ports: http [8000]`), not something the browsers showed.
- Source: https://w3c.github.io/webappsec-mixed-content/, fetched 2026-11-22T17:52:25Z (Last-Modified 2023-02-23), sha256 `6222f7990fa9825ce24c5afd68de19b08ab52ef29232d506a0cc08dfba7c1bd5`. It is kept in job scratch `tmp/fixes/mc/` and not committed.

## (a) WPTBroad (`FixChecks.cfg`)

| model | mismatches (w014 via FetchResult) | w014 as `<img>`, WPT (served F) | `<img>`, TLS served |
|---|---|---|---|
| before (HEAD) | {} | n/a | n/a |
| fixed | {w014} | {w014} | {} |
| false:secure-ctx-top / nav-corp-check / nav-coep-adherence / mc-ancestor | {w014} | {w014} | {} |
| false:mc-upgrade | {w014} | {w014} | {w014} |
| false:mc-block | {} | {w014} | {} |

- The stable rows (`StableNames`, all-browser PASS) all still match.
- The expected-value method sees G3 only, and as a *new mismatch*: the TSV expectation is the outdated one.
- G1 and G2 are invisible to it: no row is nested.

## (b) Inclusion (`check.sh`; observed.tsv unchanged; w014 patched to `ImageResult`)

| COIChoices | browser | inside before → after | old 43 killed before → after |
|---|---|---|---|
| {concrete} | Chrome | 92 → 93 | 40 → 40 |
| {concrete} | Firefox | 108 → 109 | 40 → 40 |
| {concrete, logical} | both | same as above | 38 → 38 |
| expected column | TSV | 109 → 108 (w014 out) | 38 → 38 |

- New ids: `neg:mc-ancestor`, `neg:mc-upgrade` and `neg:mc-block` are killed (on w001/w002/w007/…).
- `neg:` of `secure-ctx-top`, `nav-corp-check` and `nav-coep-adherence`, and all six `false:` forms, are equivalent on the 109 rows.
- `false:mc-block` would be killed on w014 only if w014 is mapped as `fetch()`. As `<img>`, both `false:mc-upgrade` and `false:mc-block` still give error.
- Inclusion sees G3 (w014 enters both browsers' sets). It cannot see G1 or G2.
- No `false:<new id>` is killed, so no observation pins any single Mixed Content step. w014 lands inside only through the row patch plus `served = FALSE`.

## (c) Havoc (`HavocFix.cfg`, `HavocFixCore.tla`)

The properties are, in order: top-level OptInSec, Lifted, SecureCtx, PC, COI-top, COI-nested.

`Conservative` is TRUE: with HS = {}, the paths equal `FetchResultCtx`, `CrossOriginIsolated` and `NavChild`.

| point | fixed | false:secure-ctx-top | false:nav-coep-adherence / nav-corp-check |
|---|---|---|---|
| base | T F T T T T | T T T T T T | T F T T T **F** |
| h-secure-c (lower only) | F F F T T T | F F F T T T | F F F T T F |
| h-ecoep-inherit (type-wide) | F F F T F F | same | same |
| h-ecoep-inherit-p (child may inherit parent's) | T F T T T T | T T T T T T | T F T T T F |
| h-coimode (type-wide) | T F T T F F | T T T T F F | T F T T F F |
| h-coimode-adh (any mode if creator's COEP compatible) | T F T T T **T** | T T T T T T | T F T T T **F** |
| h-mc | T F T T T T | T T T T T T | T F T T T F |

- **h-secure-c still breaks OptInSec, by design.** It lowers the bit below what the model computes. Its remaining writers (data: top-level URL, worker owner) are unmodelled. It breaks the same way with or without the fix, so havoc does not discriminate G1.
  - The lower-only contract now also lowers contexts nested under https, where no spec writer exists. The remaining break stands only for the data: and worker writers.
  - G1 shows up in the base instead: Lifted is F with the fix and T with `false:secure-ctx-top`.
  - Behaviour control: `Differs` T, `Recovers(h-secure)` T.
  - COI-nested holds under h-secure-c, because adherence reads the lowered child COEP.
- **h-coimode, restricted (-adh on the group's creator), now holds for nested documents.** With `false:nav-coep-adherence`, COI-nested is F, also at base. This is the positive control for G2. `false:nav-corp-check` breaks clause (1).
- **Premise mismatch.** With the premise on the slot (PC), the property holds *by construction*.
  - The restricted inheritance (a child gets its parent's policy container) holds for every property.
  - Type-wide h-ecoep-inherit still breaks COI-top. A top-level inherited COEP (about:blank popup) would need COOP and group inheritance modelled too, which is not straightforward, so I did not model it.
- **Mixed Content cannot be flagged by these safety properties.** It only removes results: h-mc never breaks.
  - Behaviour level: `Differs` is T for mc-block and mc-ancestor, `Recovers(h-mc)` is T.
  - `Differs` is F for mc-upgrade, nav-corp-check and nav-coep-adherence, because their effects are not on the fetch() path.
  - On the `<img>` path (`DiffersImg` in FixChecks), only `false:mc-upgrade` differs. This is mc-upgrade's only control in any method.

## Side effects

- `havoc/HavocSpec.tla` `Conservative` is now FALSE, because its mirror lacks Mixed Content. It is TRUE with `Mutant = "false:mc-block"` (`HavocSpec-nomc.cfg`), and its singles table is unchanged.
- `DIPExtension` `Conservative` is TRUE → FALSE for the same reason. Its other values are unchanged.
- `Observe` (the flow part) has no Mixed Content.
- `MechMutants` grows from 27 to 33. Rerunning `observe/driver/check.sh` unmodified would count 49 mutants and map w014 through `fetch()`, so observe/RESULTS.md describes the HEAD model.
- I ran every SpecIsolation-dependent cfg at the top level and in `havoc/`, on HEAD and on the fixed tree, and diffed the `Print*` output after dropping the new `PrintFixes` and `PrintSignature` lines. These are the only changes:
  - `Spec-WPTBroad` now reports {w014}.
  - Both `Conservative`s above.
  - `UnsupportedSplit-{all,split}`: the `isoW` count goes from 70 to 44, with the booleans unchanged.
  - Dominance, ORB, Hooks, Unsupported and the other `Spec-*` cfgs are unchanged.
- `PrintFixes` and `PrintSignature` are zero-arity, so TLC prints them in every module that extends SpecIsolation.

## Remaining gaps

data: top-level URL and workers (secure context); nesting deeper than one level; inherited COOP/COEP for top-level about:blank; `imageset`, audio, video and CORS-mode mixed images; MIX 4.5 response check; DIP and the flow part without Mixed Content.

## Files and how to run (from `site-isolation/`)

- `FixChecks.{tla,cfg}` (a); `check.sh` + `patch_w014.py` + `AllowedSetsFix*.{tla,cfg}` (b): `bash fixes/check.sh <out dir>`.
- `HavocFix{,Core}.tla`, `HavocFix.cfg` (c).
- Run TLC with `-DTLA-Library=/spec -config fixes/<cfg> fixes/<module>.tla`. `HavocSpec-nomc.cfg` runs `havoc/HavocSpec.tla`.
