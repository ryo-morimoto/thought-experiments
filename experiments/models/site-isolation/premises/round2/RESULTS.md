# Round 2: assessing every non-exact correspondence

This round follows [../RESULTS.md](../RESULTS.md) and answers the Stage C attacks on
[experiments/2026-11-24-property-premises.md](../../../../2026-11-24-property-premises.md) (tree node A1).
Specs: HTML `html.src` 0e292f4 and Fetch `fetch.bs` d7fc0fd. A subagent wrote it on 2026-11-24.
No existing file was edited and nothing is committed.

## Files

- `assess.tsv`: the 24 narrower or broader rows of `../premises.tsv`, each with a class and an argument or TLC result.
- `SpecIsolationPT.tla`: a copy of `../../SpecIsolation.tla` with three changes. `Secure` means "potentially trustworthy"
  (localhost counts). The CORP scheme test uses the literal scheme (`SchemeHttps`). `Origins` gains http and https localhost.
- `PremisesPT.tla/.cfg`: the properties over extended domains: localhost, a ported origin, an opaque requester.
- `PremisesExt.tla/.cfg` and `PremisesExt-samesite-scheme.cfg`: the strict opt-in conclusion in DIP, Dominance, Hooks
  and ORB, plus the nested property at depth 2.

## (1) The 24 non-exact rows

Classes: 17 harmless (one of them only up to depth 2), 5 restrict the claim's scope, 2 must be fixed.

- **Must fix (2):** the broader "opt-in" conclusion (round 1 M1) in OptInOnlySecureCtx and OptInOnlyPC. A broader
  conclusion is a weaker claim. It cannot fail for reasons outside the spec, but here it misses a misreading. An http
  document under an https top is a secure context, so the scheme condition matters. Under `samesite-scheme` the strict
  forms are FALSE while the originals stay TRUE. The fix is `CorpPermits`.
- **The other M1 rows are harmless (6).** These properties have only top-level https requesters (OptInOnlySecure,
  COI-top, DIP, Dominance, Hooks, ORB), or an https top over its child (COI-nested), so the scheme condition always
  holds. PremisesExt shows the strict and original forms are both TRUE, unmutated and under `samesite-scheme`
  (output below). OptInOnly and OptInOnlySecureLifted are superseded.
- **Restricts scope (5):**
  - secure context, in three rows: documents only, no data: or about: top-level URLs, no workers.
    Localhost is now checked: the properties hold, and they are not vacuous (1162 premise cases, 166 with an
    http://localhost top).
  - `cors` in Signature: it cannot separate CORS-check readings.
  - `noopener-allow-popups` in P1 to P4.
- **Harmless (12):** each has an argument or a TLC result in `assess.tsv`. For example, a ported origin behaves like a
  same-site host (`PortLikeWww` TRUE). The COEP slot is quantified whatever wrote it (OptInOnlyPC TRUE). Retries range
  over a superset of the 401 retries. The broader COI premises still hold.

PremisesExt, unmutated and under `samesite-scheme`, all TRUE: `dip-optin-strict`, `dip-coi-strict`,
`acsub-strict`, `acnav-strict`, `acmono-strict`, `orb-optin-strict`, their originals, and `coi-nested-depth2`.
It takes minutes, because TLC also evaluates ORBExtension's zero-arity `PrintORB`.
PremisesPT (14 s), all TRUE: `optin-ctx-ext`, `optin-pc-ext`, `coi-top-ext`, `coi-nested-ext`, `port-like-www`,
`localhost-secure-not-https`.

## (2) CorpPermits is asymmetric

`CorpPermits(o, r)` contains `Secure(o) \/ ~Secure(r.origin)`. Fetch's same-site case (fetch.bs:4459) says
"origin's scheme is "https" or response's URL's scheme is not "https"".

- `Asym` is TRUE: https://a.test passes for an http://a.test response with CORP same-site. The reverse is blocked.
- `LitEqualsCheck` is TRUE: for every explicit CORP header, every COEP and every extended origin (opaque included),
  the literal form equals `CorpInternal`'s result.
- **Latent conflation (2b).** SpecIsolation's `corp-ss-scheme` and round 1's `CorpPermits` write the literal scheme
  test as `Secure`. That is correct only while `Secure` means scheme = https. Widen `Secure` to "potentially
  trustworthy" and both go wrong: `r1-corppermits-wrong-on-localhost` is TRUE, meaning http://localhost would pass
  for https://localhost. The fix, used in SpecIsolationPT, is a separate `SchemeHttps`.

## (3) Every use of SameSite / `.site`

| use | correct concept | verdict |
|---|---|---|
| CORP internal check (`corp-ss-site`) | schemelessly same site (fetch.bs:4459) | right |
| `HasOptIn` and its copies (DIP, Dominance, Hooks, ORB, havoc, Unsupported*) | CORP's condition | broader (M1), read as schemeless (M2) |
| `Key(o, "site")` (agent cluster keys, OAC, document.domain rows) | site = (scheme, registrable domain) (html.src:94802) | wrong: drops the scheme (M4). No TLC impact on the 81 O scenarios, because each pair shares a scheme |
| sandbox `Opaque` (`site` "opaque") | opaque origin is its own site | right: there is a single opaque origin. Two would collide |
| `OriginOracle.Site`, `SpecSameSite` | obtain a site | its tuple origins have no scheme field (one implicit scheme), so harmless |
| mutant `nocors-site-basic` | a misreading by design | n/a |

## (4) Permissions Policy

The real premise:
- no `allow` attribute on any iframe;
- no `Permissions-Policy` response header on any document;
- so "cross-origin-isolated" keeps its default allowlist 'self' (html.src:5570), and a child is allowed only if it is
  same origin with its parent.

Where the model assumes it:
- `CrossOriginIsolated`, read as the getter of a top-level document (the WPT coi-* cases, COIOnlyWithOptInTop, DIP);
- the RedirectSeq "coi" row;
- GenModel `PP`;
- Gen2 `g2-pp-self`.

`gen.py`, `gen2.py` and `redirect/gen.py` emit neither `allow=` nor `Permissions-Policy` (grep finds nothing), so the
generated scenarios satisfy the premise. The access-control properties do not depend on it, because Permissions
Policy only removes the capability.

## (5) The 15 definitions of the analysis

| definition | reason stated | a test that would expose a wrong one |
|---|---|---|
| WPTAgree expected values | yes | yes: browser inclusion found w014 outdated |
| NoHeaderLeak observation | yes | yes, by design: LeakWitness |
| Observe | yes (opaque filtered response) | partly: `opaque-length` kills NoUndeclaredLeak. Timing and size are untested (risk) |
| Declared | yes | yes: ORB witness-D0 showed it incomplete under ORB |
| Bodies, secret | yes | yes: two lengths, killed by `opaque-length` |
| Signature, Conservative | meta | Conservative exposed itself (FALSE after Mixed Content) |
| NoUndeclaredLeakD | yes | no DIP-specific test (low risk: same Declared) |
| hooks: block-only, HookReads/Twin, substitute, Kind | yes | only a positive control (Hooks-any versus Hooks-declared). No real extension is mapped to a hook kind (risk: a service worker changes the response type) |
| ORB Declared variants | yes | yes: the NI table |
| SrcCheck (P2, P2c) | yes | yes: the P2c counterexample matches upstream WPT popup-redirect-same-origin-allow-popups |

So 2 of the 15 rows carry a real risk of silent divergence: the Observe side channels and the hook kinds.

## A1 done condition

Every premise concept now maps to a spec definition or is a labelled analysis definition. Every non-exact
correspondence is assessed: 17 harmless, 5 scope, 2 must fix. The condition is met **with conditions**:

- the 2 must-fix rows need the `CorpPermits` restatement adopted in SpecIsolation, and `SchemeHttps` if `Secure` is
  ever widened;
- the scope limits must be stated with each claim: documents only, no data: or about: tops, depth 2 or less, and no
  `noopener-allow-popups`;
- the Observe and hook definitions have no exposing test.
