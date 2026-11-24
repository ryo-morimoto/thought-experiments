# Bug-derived axes: sandbox flags, redirect-carried values, document.domain, workers, cors (C11)

Record: [experiments/2026-11-24-bug-derived-axes.md](../../../2026-11-24-bug-derived-axes.md).
Axes come from the missing steps in [../bugmut/RESULTS.md](../bugmut/RESULTS.md) section 3.
`../SpecIsolation.tla` is unedited. The new steps are in `Gen3Model.tla`. The pipeline is gen2's
(space, then pre-screen, then cover + sample, then WPT in podman, then kill rule). A subagent ran
this on 2026-11-24. Nothing is committed.

## Specs

HTML `html.src` 0e292f4 and Fetch `fetch.bs` d7fc0fd (job scratch `tmp/extract/data/`). Referrer
Policy `index.src.html` at w3c/webappsec-referrer-policy cc435b05 (sha256 a277e78e…5eb1). CSP3
`index.bs` at w3c/webappsec-csp e3461f7c (sha256 2c6ca12c…6ef). Both were fetched 2026-11-24 07:29Z
into `tmp/gen3/spec/`.

## Steps added (`G3(id, e)`; mutants `neg:`, `false:`, `true:`; constant gates `neg:` only)

| family | ids | spec phrase (anchor) |
|---|---|---|
| sandbox parse | `g3-kw-popups/top/topua/so/escape` | "unless tokens contains the allow-popups keyword" ([#parse-a-sandboxing-directive](https://html.spec.whatwg.org/#parse-a-sandboxing-directive)) |
| X popups | `g3-sb-aux`, `g3-sb-prop`, `g3-sb-origin`, `g3-sb-dd` | "prevents content from creating new auxiliary browsing contexts"; "any auxiliary browsing context it creates inherits" ([#sandboxing](https://html.spec.whatwg.org/#sandboxing)); document.domain setter: flag check, then "effectiveDomain is null" ([#dom-document-domain](https://html.spec.whatwg.org/#dom-document-domain)) |
| Y top nav | `g3-sb-top`, `g3-sb-act` | "has transient activation is false, and … without user activation … flag is set" ([#allowed-to-navigate](https://html.spec.whatwg.org/#allowed-to-navigate)) |
| R Origin | `g3-taint`, `g3-taint-req`, `g3-taint-sticky`, `g3-org-cors`, `g3-org-post`, `g3-org-rp` | "redirect-taint is not same-origin, then return null" ([#serializing-a-request-origin](https://fetch.spec.whatwg.org/#serializing-a-request-origin)); taint loop ([#concept-request-tainted-origin](https://fetch.spec.whatwg.org/#concept-request-tainted-origin)); referrer-policy switch ([#append-a-request-origin-header](https://fetch.spec.whatwg.org/#append-a-request-origin-header)) |
| R Referer | `g3-ref-redirect`, `g3-ref-sticky` | "set request's referrer policy to policy" ([#set-requests-referrer-policy-on-redirect](https://w3c.github.io/webappsec-referrer-policy/#set-requests-referrer-policy-on-redirect)); main fetch sets request's referrer on every hop, and the next hop starts from it ([#determine-requests-referrer](https://w3c.github.io/webappsec-referrer-policy/#determine-requests-referrer)) |
| K CSP | `g3-csp-hop`, `g3-csp-url` | "We use request's url, and not its current url" ([#create-violation-for-request](https://w3c.github.io/webappsec-csp/#create-violation-for-request)) |
| D, N | `g3-od-domain`, `g3-od-null`, named `od-as-origin`, `g3-reuse` | "domains are identical and non-null" ([#same-origin-domain](https://html.spec.whatwg.org/#same-origin-domain)); "same origin-domain with navigationParams's origin, then set window" ([#initialise-the-document-object](https://html.spec.whatwg.org/#initialise-the-document-object)) |
| W workers | `g3-w-check`, `g3-w-shared`, `g3-w-blob`, `g3-w-own` | "not a DedicatedWorkerGlobalScope object, then return true" ([#check-a-global-object's-embedder-policy](https://html.spec.whatwg.org/#check-a-global-object's-embedder-policy)); "compatible with cross-origin isolation and is shared is true" ([#run-a-worker](https://html.spec.whatwg.org/#run-a-worker)); blob: inherits its creator's policy container |
| F cors | `g3-cors`, `g3-cors-star`, `g3-cors-acac`, plus SpecIsolation's `fetch-cors` | CORS check ([#concept-cors-check](https://fetch.spec.whatwg.org/#concept-cors-check)); the CORP check runs only for opaque tainting ([#concept-http-fetch](https://fetch.spec.whatwg.org/#concept-http-fetch)) |

There are 84 G3 mutants. Two parameters are not misreadings. `OShare` {ref, copy}: HTML does not
say whether the initial about:blank shares its creator's origin object, so a later document.domain
may or may not reach it. `RefMay` {may, exact}: "The user agent MAY alter referrerURL". The four
cfgs are `{both,concrete}-{may,exact}`, with both = COIChoice {concrete, logical}.

## Space, pre-screen, selection, cost

- `gen3.py space`: **2 230 scenarios**: X 28, Y 14, R 1 776, K 117, D 24, N 27, W 28, F 216 (axes in the docstring).
- `Gen3Enum` (TLC, -Xmx2g, 1 worker) took 10–12 s per cfg. It ran 199 mutants: 55 author mutants,
  60 bugmut bug-type mutants (`true:`/`false:` on SpecIsolation decisions) and 84 G3 mutants.
  122 are distinguishable on the space. The 4 equivalent G3 mutants are all `g3-kw-topua` and
  `false:g3-sb-act`: no scenario has user activation.
- `gen3.py select`: 45 cover scenarios, then X/Y/K/D/N/W in whole, R 25 % and F 40 % per stratum
  (seed 20261124). That gives **783 scenarios** (R 454, F 91) and 1 974 rows per browser, in 13 files.
- Run: podman `python:3.12-bookworm`, WPT 31362d122, Chrome 158.0.8127.88, then Firefox 160.0.1,
  one after the other, 2 repeats. `wpt run`: Chrome 133 / 130 s, Firefox 146 / 136 s. Wall time
  including the install: 296 and 321 s. All 52 file runs were OK. Every row was the same in both repeats.
  `Gen3Allowed` took 7–9 s per cfg.

## Inclusion (rows inside / 1 974)

| cfg | Chrome | Firefox |
|---|---|---|
| both-may | 1 947 (27 out) | 1 964 (10 out) |
| concrete-may | 1 939 (35) | 1 956 (18) |
| both-exact | 1 947 (27) | 1 922 (52) |
| concrete-exact | 1 939 (35) | 1 914 (60) |

## Out-of-model values (nothing held)

| rows | browser | observed | model | class |
|---|---|---|---|---|
| R.org ×14: no-cors POST, last policy no-referrer or same-origin | Chrome | Origin sent | `null` | **weaker, public**. wpt.fyi `fetch/origin/assorted.window.html`, Chrome 158.0.8127.36 (run 6313827378135040) fails 3 subtests "…fetch no-cors mode with Referrer-Policy no-referrer / same-origin". In R1337 and R1349 the no-referrer comes only from the redirect's header. That is the same mechanism, and WPT does not test it |
| R.org ×12: no-cors POST, same-origin URL then a cross-origin one | Chrome | `null` | the origin (taint needs the request origin ≠ lastURL) | stricter |
| N0001: iframe without src, src set after insertion, same origin | both | not reused | reused | stricter, public: wpt.fyi `window-reuse-in-nested-browsing-contexts.tentative.html`, both fail "navigate iframe with no initial src" |
| W.coi ×8: shared worker with COEP rc/cl | both | FALSE | TRUE under concrete | stricter. FALSE is inside under logical (implementation-defined) |
| X.pop ×8: sandbox without allow-popups | Firefox | `window.open` throws InvalidAccessError | returns null | stricter (no popup either way) |
| Y0002: unsandboxed cross-site frame sets top.location | Firefox | SecurityError | navigates (spec); Chrome navigates | stricter (framebusting block outside the spec) |
| R.ref ×42 (exact cfgs only): cross-origin, unsafe-url from init or redirect | Firefox | origin only | full URL | stricter. Inside under `may`. This is the CVE-2021-23971 fix direction |

No sandboxed document escaped. No worker reported crossOriginIsolated without COEP. document.domain
never allowed access that the model forbids. CSP blockedURI was always the original URL. No Window was
reused across origins.

## Kills (either browser)

| cfg | G3 killed / 80 non-equiv. | all mutants killed / 199 |
|---|---|---|
| both-may | 76 | 116 |
| concrete-may | 78 | 120 |
| both-exact | 77 | 117 |
| concrete-exact | **79** | 121 |

- G3 survivors: `false:g3-w-shared`, because browsers never report TRUE in a shared worker.
  `neg:g3-ref-sticky` survives only under `may`: the MAY clause allows the stripped value. Under
  `exact` it is killed by 114 R rows in each browser, so Chrome and Firefox both keep the stripped
  referrer across hops. Under both-COIChoice, `neg/true:g3-w-shared` also survive. In Firefox only,
  `false:g3-sb-aux` and `true:g3-kw-popups` survive, because its pop rows are out of model.
- **bugmut mutants**: `false:fetch-cors` was the row gap, and it is now killed by 68 F rows in
  both browsers (cfg-independent). Of the old COI survivors, `true:coi-mode` is killed under concrete
  cfgs by 7 dedicated-worker `coi` rows. It still survives under both. `false:coi-insecure` stays
  equivalent. The 4 bugmut equivalents stay equivalent here too. The gen3 rows alone kill 22/60
  bug-type mutants (concrete). Except for `false:fetch-cors`, every one of these was already killed
  by an earlier set.
- bugs.tsv `step` bugs now on a killed mutant (11 of 15):
  - CVE-2024-3840 and CVE-2020-6526: `false:g3-sb-top`, `false:g3-kw-top`.
  - CVE-2019-25154: `false:g3-sb-prop`.
  - CVE-2022-29911: `g3-kw-*`, except `topua`, which needs activation.
  - CVE-2026-8950: `neg:g3-taint` (265/277 rows).
  - CVE-2021-23971: `neg:/false:g3-ref-redirect`.
  - CVE-2021-23968 and CVE-2021-23969: `neg:g3-csp-url`.
  - CVE-2019-11711: `neg:/true:g3-reuse`.
  - CVE-2019-11762: `od-as-origin`.
  - CVE-2026-12302 is partial: its policy container is modelled for COEP, not CSP.
  - Not covered: custom protocols, history (2), ORB.

## Hypotheses of the record

- **R1 (bug-type mutants killed, values mostly inside): supported.** 79/80 non-equivalent G3
  mutants are killed, and 97–99 % of rows are inside. The one bugmut row gap is closed.
- **R2 (outside values): supported in part.** There are 7 patterns. Only one is weaker than the model:
  Chrome's Origin under no-referrer, which already fails publicly. The other 6 are stricter.
- **R3 (axes not visible in values): supported for 3 places.** First, allow-top-navigation-by-user-activation
  needs activation (4 mutants are equivalent on the space). Second, a shared worker's COI is an
  implementation-defined choice that browsers resolve to FALSE. Third, Referer stickiness is hidden
  by the MAY clause.

**C11 done condition** (missing steps added as axes, inclusion and kills checked in browsers): **met**
for the five listed axes. It is not met for custom protocols, history, ORB or worker CSP.

## Limits

The axes are my reading of the specs. No user activation, no Safari, one machine, https only, and one
redirect status (307). Shared workers and popups are one level deep. Window reuse is seen only
through an expando. R and F are sampled at 25 % and 40 %.

## Files

- Model: `Gen3Model.tla`, `Gen3Enum.tla`, `Gen3Allowed.tla` + 8 cfgs.
- Generator: `gen3.py`, which writes `space.tsv`, `Gen3Space.tla`, `selected.tsv` and the cfgs.
- Observations: `observed.tsv`.
- `tests/`: 13 files, and `resources/g3.js` with the `*.py` pages.
- `driver/`: `run.sh`, `incontainer.sh`, `tlc.sh`, `mkrows.py`, `analyze.py`. Extraction uses `../gen2/driver/extract.py`.
- Raw logs: `tmp/gen3/final/` (sha256 chrome r1 8f3a4330…1e1e, r2 a03238cc…2e7f;
  firefox r1 8a583163…9d39, r2 017fad61…3b23b).
