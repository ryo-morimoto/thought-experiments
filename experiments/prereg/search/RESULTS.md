# Spec-oracle + automatic trigger search for two held-out bugs

Run 2026-11-21 inside podman (`docker.io/library/python:3.12-bookworm`), WPT clone commit
31362d1, `./wpt run --headless --timeout-multiplier=4`. This extends the single-scenario
repros in `../repro/` by pairing each spec-derived oracle with a seeded random/state-space
search over operation sequences, so detection no longer depends on one hand-written path.

Browser builds actually launched (from the raw logs): Chrome for Testing **134.0.6998.165**
(CVE-2025-3071 pre-fix), stable Chrome **158.0.8127.36**, Firefox **150.0** (CVE-2026-8950
pre-fix; bug fixed in Fx 151), stable Firefox **160.0.1**.

## Target A — CVE-2025-3071 (Chromium, fixed Chrome 135)

**Generator** (`search-a-origin-after-nav.sub.https.html` + `nav-helper.sub.html`). A popup is
opened on same-origin A; a seeded PRNG (mulberry32, base seed printed) builds sequences of
length 3–8 from: navigate to {A-helper, B-helper(cross-site), about:blank} with optional
`#fragment`; `location.replace`; `history.pushState`/`replaceState`; `location.hash`;
`history.back`/`forward`/`go(n)`. Navigations are driven by the opener (`popup.location=`,
allowed cross-origin); history/hash/state ops are tried opener-direct and, on SecurityError,
routed to the popup's helper by `postMessage`. Up to 400 sequences per file within a
150 s budget.

**Oracle** (HTML "determine the origin" + same-origin access rule). After each step, from the
opener: if `popup.location.href` is readable (no SecurityError) then the URL must be same-origin
A or an `about:` URL — a readable cross-origin http(s) URL is the leak. Secondary: when the
helper reports its own `self.origin` with `location.href`, they must agree for http(s) URLs.
On a violation, delta-debug (remove steps while the violation persists).

## Target B — CVE-2026-8950 (Firefox, fixed Fx 151)

**Generator** (`search-b-redirect-origin.sub.https.html` + `redirect.py`, `echo-origin.py`,
`echo-origin-page.py`). Seeded PRNG builds redirect chains of 1–4 hops over origins
{A, A-subdomain (same-site), B (cross-site)}, statuses {301,302,303,307,308}, method {GET,POST},
final echo target on any of the three origins, observed in mode {cors-fetch, form-POST
navigation, iframe-GET navigation}. The echo handler returns the received `Origin` header.
Up to 600 chains within a 120 s budget.

**Oracle** — a JS reference implementation of Fetch's "compute the redirect-taint",
"serializing a request origin", "append a request Origin header", and the HTTP-redirect method
rewrite (301/302 on POST→GET; 303 on non-GET/HEAD→GET), extracted verbatim from `fetch.bs`.
On a mismatch, shrink by dropping hops. Unit-tested offline (`oracle_test.mjs`, 9/9) before use.

**Oracle bug found and fixed (via current-browser validation):** v1 assumed `responseTainting`
is "cors" for every cors-mode fetch, so it expected a serialized Origin on fully same-origin
cors chains where browsers (correctly) send none. This produced 4 false mismatches on **both**
current Chrome and current Firefox — i.e. the validation step caught the oracle, not the engine.
Fix: tainting becomes "cors" only once a non-same-origin URL is fetched in cors mode. After the
fix, current Firefox 160 is clean (0/600).

## Results

| Target | Browser / build | Sequences-or-chains run | Violations | Shrunk counterexample | Matches the bug? |
|---|---|---|---|---|---|
| A (CVE-2025-3071) | Chrome 134 (pre-fix) | 50 seqs | 0 | — | **No (not detected)** |
| A | Chrome 158 (current) | 100 seqs | 0 | — | n/a (fixed) |
| A | Firefox 160 (current) | 22 seqs | 0 | — | n/a |
| B (CVE-2026-8950) | Firefox 150 (pre-fix) | 600 chains | 0 | — | **No (not detected)** |
| B | Firefox 160 (current) | 600 chains | 0 | — | n/a (fixed) |
| B | Chrome 158 (current) | 443 chains | 4 | `POST form [A:308] => Asub` exp=origin act=null | No — see below |

**Target A:** no origin confusion on any build, including pre-fix Chrome 134. The search broadened
coverage to many about:blank/back/replace/pushState orderings but still did not hit the
document-sequence-number-reuse trigger. Consistent with `../repro/` (a miss on the pre-fix build).

**Target B:** pre-fix Firefox 150 tainted the `Origin` header correctly to `null` on every
cross-site POST chain the generator produced (cors and form-POST, all 307/308 and rewrite cases),
so CVE-2026-8950 was **not** reproduced — matching the earlier single-scenario miss. The bug's
inverted same-origin check evidently sits on a path these black-box chains do not reach.

**Chrome 158's 4 residual mismatches are a genuine engine difference, not the CVE** (and the
opposite direction): on a form-POST navigation whose redirect lands on a *same-site but
cross-origin* target (e.g. A→A `308`→A-subdomain), the spec's redirect-taint stays "same-origin"
(the request origin is same-origin with the URL being redirected *from*), so the oracle expects
the real origin; current Chrome sends `Origin: null`. This is Chrome being more conservative than
the spec on navigation requests, surfaced by the oracle; it is not CVE-2026-8950 (Firefox sending
the *real* origin when the spec wants null) and appears on the fixed build. Left as an open,
benign discrepancy; current Firefox 160 agrees with the oracle here.

## What could not be done / caveats

- Neither held-out bug was detected even with the search, on hundreds of sequences/chains per
  pre-fix build. The combination did not beat the single scenario for these two bugs; it did add
  a validated oracle and, as a side effect, surfaced one real Chrome/spec navigation-Origin
  discrepancy and one oracle bug.
- Target A per-build sequence counts are modest (22–100) because each sequence opens a real popup
  with settle delays; the budget favored faithful timing over raw volume.
- The Chrome-vs-spec form-POST Origin difference was not traced to a root cause within the budget.

## Files

- Generators / pages: `search-a-origin-after-nav.sub.https.html`, `nav-helper.sub.html`,
  `search-b-redirect-origin.sub.https.html`
- Server handlers: `redirect.py`, `echo-origin.py`, `echo-origin-page.py`
- Oracle unit test (offline): `oracle_test.mjs`
- Runner: `driver/incontainer.sh`, `driver/runsearch.sh`
- Raw wptreport JSON + console logs were produced under the job tmp dir (not copied here).
