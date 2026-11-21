# Optional browsing context group (BCG) swap: do browsers differ, and is the choice deterministic?

Run 2026-11-21 inside podman (`docker.io/library/python:3.12-bookworm`), WPT clone commit
31362d1, `./wpt run --headless --timeout-multiplier=4`. Browsers: stable Chrome 158.0.8127.36,
stable Firefox 160.0.1 (from the raw logs' `run_info`).

## Spec: what a swap is, and what web content can see

HTML "obtain a browsing context to use for a navigation response" has three optional
`swapGroup` cases:

- (a) source/destination not same site **and** "either of sourceOrigin or destinationOrigin
  have a scheme that is not an HTTP(S) scheme and the user agent considers it necessary ...
  (for implementation-defined reasons), optionally set swapGroup to true" (issue #10842);
- (b) "If navigationParams's user involvement is "browser UI", optionally set swapGroup to
  true" (issue #6356);
- (c) "If browsingContext's group's browsing context set's size is 1, optionally set swapGroup
  to true." Note: "Some implementations swap browsing context groups here for performance
  reasons." Case (c) has **no** same-site condition, so a same-origin navigation may swap too.

A swap only replaces the *browsing context* ("Let newBrowsingContext be the first return value
of creating a new top-level browsing context and document"); the traversable navigable stays.
Consequences:

- **window.name is not a swap observable.** The name lives in the history entry's document
  state and is cleared by a separate rule (`#resetBCName`): when the navigable is top-level,
  the document's BC "is not an auxiliary browsing context whose opener browsing context is
  non-null", and the new document is not same origin with the active document, "set
  historyEntry's document state's navigable target name to the empty string". That rule does
  not look at swapGroup.
- **sessionStorage and history.length** belong to the traversable (session storage shed,
  session history), so a swap does not change them.
- **BroadcastChannel / SharedWorker** are keyed by storage key, not by BCG: unchanged.
- **Opener/openee and named lookup** do change: the new BC starts with no opener and in a new
  group. With size 1 nothing else holds the old BC's WindowProxy, so the only visible effect is
  the one the spec note names: "the destination page could open a window, then if the user
  navigates back, the previous page could expect to be able to script the opened window. Doing
  a swap here would break that use case." Our probe tests exactly that.
- COOP report-only: when swapGroup is false a "virtual browsing context group ID" may change
  (reporting only).

## Existing WPT coverage (wpt.fyi stable runs at a3830cd8f7, 2026-11-20)

| test | Chrome 158 | Firefox 160 | Safari 27.2 |
|---|---|---|---|
| auxiliary-browsing-contexts/no-proactive-swap-when-other-contexts-in-group.html | 1/1 | 1/1 | 1/1 |
| auxiliary-browsing-contexts/named-lookup-scoped-to-browsing-context-group.html | 1/1 | 1/1 | 1/1 |
| auxiliary-browsing-contexts/named-lookup-noopener.html | 2/2 | 2/2 | 1/2 |
| history-traversal/window-name-after-cross-origin-main-frame-navigation.sub.html (popup with opener) | 0/1 | 0/1 | 0/1 |
| cross-origin-opener-policy/navigate-to-aboutblank.https.html | 5/5 | 4/5 | 5/5 |

The only test about the optional swap checks the **prohibition** (no swap when the group has
more than one context). No WPT test observes whether case (a), (b) or (c) is taken; that is
consistent with them being optional. Case (b) cannot be driven from testharness (WebDriver /
testdriver have no "browser UI" navigation). Case (a) needs an origin whose scheme is not
HTTP(S) and that web content can navigate to top-level cross-site; `data:` gives an opaque
origin (no scheme) and top-level `data:` is blocked; `blob:` documents take the creator's
HTTP(S) origin; `file:`, `about:settings`, `chrome://` are not reachable from WPT pages. So
case (a) is not testable from web content; only (c) was tested.

## Probe (case c)

`tests/resources/bcg-probe.js`: test page opens W on origin A (with `noopener` → W's group has
size 1, or without → size 2), sets `window.name='wname'`, `sessionStorage.k='v'`, and a JS
global marker. W navigates top-level to B. B opens popup P (origin A, named `probe_<token>`).
B does `history.back()` to A. A calls `window.open('', name)`: finding P means A and B share
a BCG (no swap); not finding it means a swap was observed. P also reads `opener.location.href`.
The JS marker surviving tells whether A came back from bfcache. Note: if A is *not* restored
from bfcache, A is re-created inside B's BC, so the probe cannot see a swap that happened at
A→B. "noswap" with bfcache=false therefore means "no observable swap", not "no swap".

## Results

Verdict = probe outcome; "bfcache" = A restored from bfcache; name = window.name at A / at B / after back.

| case | condition | Chrome 158 | Firefox 160 | deterministic across runs? |
|---|---|---|---|---|
| c1 | noopener, A→B cross-site | SWAP 6/6 (bfcache yes; name 'wname'/'wname'/'wname') | no observable swap 2/2 (bfcache no; name 'wname'/''/'wname'); 3rd run TIMEOUT (harness) | Chrome yes (6/6); Firefox 2/2 |
| c2 | noopener, A→B same-site cross-origin | SWAP 6/6 (bfcache yes) | no observable swap 2/2 (bfcache no; name cleared at B) | Chrome yes; Firefox 2/2 |
| c3 | noopener, same-origin A→A' | SWAP 6/6 (bfcache yes) | not obtained (runner window broke, see below) | Chrome yes |
| c4 | with opener (group size 2), cross-site | no swap 6/6 (bfcache no) | not obtained | Chrome yes |
| c5 | noopener, cross-site, A `Cache-Control: no-store` | no observable swap 6/6 (bfcache no) | not obtained | Chrome yes |
| c6 | noopener, same-site, A no-store | no observable swap 6/6 (bfcache no) | not obtained | Chrome yes |

Chrome: 1 run (r0) + 5 repeats in one session (r2), all 36 results identical per case.
Chrome after a swap: P's `opener` is non-null, `closed === false`, but cross-origin
(SecurityError): it still points to B's BC, which now sits in bfcache.
sessionStorage `k` = 'v' and history.length 1→2→2 in every run in both browsers (as the spec
predicts: these belong to the traversable).

Firefox problems: in a shared session the first file timed out once (r0) and after two files
every later file errored with `window.__wptrunner_process_next_event is not a function`
(r1); per-file runs (fresh browser each, `incontainer-perfile.sh`) work but take ~5 min each
and were stopped at the time cap after c1, c2. Firefox never restored A from bfcache here;
a likely cause is the RemoteContextHelper executor's in-flight fetch (wpt.fyi: Firefox fails
`back-forward-cache/eligibility/inflight-fetch-*.html`, Chrome passes). So the probe is blind
to a Firefox swap at A→B: Firefox shows "no observable swap", not "no swap".

Side finding (not a BCG effect): Chrome keeps window.name ('wname') after a cross-site
top-level navigation of a noopener window (c1/c2), and after a swap; the spec's
`#resetBCName` says it must be cleared. Firefox clears it at B and restores 'wname' on back
(it is per-entry document state), which matches the spec.

## Reading

- Browsers differ in what is observable: in Chrome the spec note's breakage (the earlier page
  cannot reach a window the later page opened) happens for every noopener window navigation
  where A goes into bfcache, even same-origin; in Firefox it did not happen in the runs we got.
- Chrome's choice is not a fixed parameter and not random: it was the same in all 6 runs of
  each case, and it followed observable state: group size 1 (no opener) **and** A eligible for
  bfcache (`no-store` or having an opener turned it off). Site relation did not matter.
  It fits a function of (group size, bfcache eligibility of the source document). The
  eligibility inputs are partly browser-internal (Chrome's bfcache rules), so for a spec model
  it is best modelled as a per-browser function of state rather than a free boolean.
- Firefox: not determined, because its bfcache never kept A in this harness.

## Files

- `tests/resources/bcg-probe.js`, `tests/c*.https.html` — probe and 6 variants
  (copied to `/wpt/bcg-observe/` inside the container).
- `driver/gen.py` — writes the variant files; `driver/incontainer.sh <repeat> <tag> [products]`
  (shared session, `--repeat`); `driver/incontainer-perfile.sh <repeat> <tag> <product>`
  (one `wpt run` per file); `driver/summ.py <raw.log>...` — per-run verdict + observations.
- Host command used: `podman run --rm -v $WPT:/wpt:Z -v $BCG:/bcg:Z -v $BCG/driver:/driver:Z
  -v $BCG/logs:/logs:Z docker.io/library/python:3.12-bookworm bash /driver/incontainer.sh 5 r2 chrome`.
- wpt.fyi API responses used for the coverage table were not committed (external data). Re-fetch from https://wpt.fyi/api/runs?label=stable&max-count=1 and https://wpt.fyi/api/search (stable runs as of 2026-11-20).

