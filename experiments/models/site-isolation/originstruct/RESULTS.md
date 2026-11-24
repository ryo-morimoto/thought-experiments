# Origin structure the model omitted: ports, registrable domains, localhost, opaque origins

For [experiments/2026-11-24-origin-structure.md](../../../2026-11-24-origin-structure.md) (tree node B7).
A subagent wrote this on 2026-11-24. The readings of the spec are its own. Nothing is committed, and no existing file was edited.

Specs: HTML `html.src` 0e292f4, URL `url.bs` 4f461b8, Fetch `fetch.bs` d7fc0fd (job scratch `tmp/extract/data/`, not committed).
Secure Contexts ED 2023-11-10 (https://w3c.github.io/webappsec-secure-contexts/) and Mixed Content ED 2023-02-23
(https://w3c.github.io/webappsec-mixed-content/), both fetched 2026-11-24.

## Files

- `OriginStruct.tla`: extends `../SpecIsolation.tla` unedited. The .cfg files replace SpecIsolation's origin operators
  (`SameSite`, `Secure`, `SecureCtx`, `TopCtx`, `ChildCtx`, `Key`, `CorpInternal`, `FetchResultDest`, `Origins`,
  `Contexts`, `Responses`) with the definitions below, and replace its expensive constant definitions by `Off`.
- `OS-rich-{A,B}.cfg`: the k ≤ 3 domain (63 origins), PSL A / B. `OS-small-*.cfg`: k ≤ 2 (30). `OS-mut-*.cfg`: one earlier or naive reading each.
- `types2.py`: relational types of the richer domain (`--minimize k` finds a domain realizing all types).
- `tlc.sh <cfg> [property]`: run TLC (podman, `-Xmx2g`) from `site-isolation/`. With a property name, it checks
  only that property. `python3 -I originstruct/types2.py` takes 10 s.

## Model design

- **Origin** (html.src:94612): a record `[op, id, scheme, host, port]`. Tuple origins have `op = FALSE`.
  Opaque origins have `op = TRUE` and are equal only to themselves (by `id`). `domain` (document.domain) is not modelled.
- **PSL as a parameter**: `Reg` maps a host to its registrable domain or `"null"` (url.bs:838). `RegA`: only `test` and
  `localhost` are public suffixes. `RegB`: `a.test` is a suffix too, as a shared-hosting suffix would be.
  `PSLAdmissible` checks that reg(reg(h)) = reg(h), and that IP hosts and `localhost` have none. Both are admissible.
- **Hosts by class** (registrable / trustworthy): `*.test` (yes / no), `*.localhost` (yes / yes), `localhost`, `127.0.0.1`,
  `127.0.0.2` (no / yes), `test`, `192.0.2.1`, `198.51.100.1` (no / no). Ports: `""` (null), `8443`, `8444`.
- **Operators**: `SchemelesslySameSite` (html.src:94870, now the operator behind CORP same-site), `ObtainSite` and
  `SameSiteHTML` (html.src:94809, 94898), `PTOrigin` (Secure Contexts 3.1 with localhost, loopback and https),
  `SchemeHttps` (the CORP same-site scheme condition, fetch.bs:4459, which is not trustworthiness).
- **Secure context** (html.src:119312): a context is `[self, top, topUrl]`. `topUrl` is the top-level creation URL: a
  network URL, `about:blank` or `data:`. Opaque tops take one of four representative URLs (only `PTUrl` reads it).
- **Agent cluster key** (html.src:118254): `KeyR` is the tuple origin, or `ObtainSite`. An opaque origin is its own site.
- **Mixed Content**: `ProhibitsMixed` keeps SpecIsolation's origin check (MC 4.3), now with `PTOrigin`. No upgrade for
  IP hosts (MC 4.1).
- **Opaque creation and inheritance** (`DocOrigin`): "determine the origin" (html.src:107640). Sandboxed documents get a
  fresh origin, outside every origin that exists. `about:blank` and `about:srcdoc` get the initiator's origin
  (html.src:109569). `blob:` gets the origin of the blob URL entry's environment (url.bs:3351). `data:` gets a fresh origin.
  An about:blank or srcdoc child inherits the initiator's policy container (embedder policy).

## Verdicts (TLC, Mutant none)

Same on DomRich under PSL A (3 min 28 s) and PSL B (2 min 56 s), and on DomSmall:

| property | verdict | before (SpecIsolation / premises/) |
|---|---|---|
| OptInSecure, OptInCtx, OptInPC (conclusion `CorpPermitsR`) | TRUE | TRUE (strict forms in premises/) |
| COITop, NestedCap (M3 premise) | TRUE | TRUE |
| NestedGroup (original premise) | TRUE (DomSmall 2.5 min; DomRich PSL A 20 min) | TRUE |
| BodyOnlyByOptIn; NoHeaderLeak (DomSmall) | TRUE; FALSE | TRUE; FALSE (the CORP error oracle, as before) |
| KeyCOI with `KeyR` (distinct origins, distinct keys under COI) | TRUE | new |
| KeyCOI with SpecIsolation's `Key` | FALSE: https://a.test vs http://a.test | collision known (premises M4) |
| KeyCOI with premises' `KeyHTML` | FALSE: https://x.a.test vs https://x.a.test:8443 | **new**: A1's fix drops the port |
| KeySite (site keys equal iff HTML same site) | TRUE | new |
| FreshIsolated, OpaqueStaysOpaque, InheritedCOI | TRUE | new (gen2 had one opaque constant) |
| CrossPSL (client PSL A, author meant PSL B) | FALSE under A, TRUE under B | new |

Witnesses and single values:

- **Ports**: https://a.test and https://a.test:8443 are cross-origin and same site. With require-corp, a response with
  no CORP header is `error`, and CORP same-site is `opaque`. A popup with same-origin COOP on both sides is severed. The
  site keys are equal, so without isolation the two share an agent cluster. Under COI they get different keys with `KeyR`,
  and the same key with `KeyHTML`. No property in the table breaks on ports.
- **PSL variance**: x.a.test and y.a.test are same site under A and cross-site under B. `CrossPSL` witness under A:
  https://a.test gets `opaque` from https://x.a.test with CORP same-site, which PSL B does not permit (a.test has
  no registrable domain under B). A client with the older list grants more than the author meant. In the other
  direction the client only blocks more, so TRUE.
- **localhost**: `CrossOriginIsolated` is TRUE for http://localhost and http://127.0.0.1, and FALSE for http://a.test.
  https://a.test fetching http://127.0.0.1 is not mixed content (`opaque`). http://192.0.2.1 is `error`, and an `<img>`
  from it is not upgraded (IP host), so `error`. http://localhost fetching https://localhost with CORP same-site
  is `error`: the CORP condition is on the scheme. Mutant `corp-scheme-as-pt` (trustworthiness in place of the scheme,
  which is what replacing `Secure` everywhere would do) makes OptInCtx FALSE. Witness: http://a.localhost in a
  https://a.test top gets https://a.localhost with CORP same-site.
- **Opaque**: Mutant `opaque-constant` (gen2's single value) makes FreshIsolated FALSE: a sandboxed document gets
  origin n1, which already exists. Mutant `no-pc-inherit` (header-only COEP for about:blank) makes InheritedCOI FALSE:
  an about:blank child of a COI https://a.test loads a credentialed no-cors https://b.test response that has no CORP.
  Mutant `false:secure-ctx-top` (secure context from the document's own origin) makes InheritedCOI FALSE as well: a
  sandboxed about:blank child is non-secure, so its inherited require-corp is dropped. So the earlier fix (G1) is also
  needed for opaque documents.
- **One cross-spec reading withheld**: one further property, comparing two specs' texts, came out FALSE. Its statement
  and witness are kept outside the repository until it is checked (user's decision on withholding spec-text gaps).

## Relational types and the adequate domain

The operators see an origin only through these relations. Per origin: opaque or not, scheme, registrable domain null
or not, trustworthy host or not. Per pair: equal, same host, same port, same non-null registrable domain.
`SchemelesslySameSite`, `ObtainSite`, `KeyR`, `SameOrigin`, `PTOrigin` and `SchemeHttps` are all functions of these.
`HttpsTwin` keeps host and port, so the domain must be closed under it.

| domain | k=1 | k=2 | k=3 |
|---|---|---|---|
| possible types | 9 | 194 | 6501 |
| adequacy/ D18 (no ports, no opaque, no localhost), PSL A | 2 | 12 | 96 |
| DomSmall (30), PSL A / B | 9 / 9 | 194 / 186 | 5076 / 4628 |
| DomRich (63), PSL A / B | 9 / 9 | 194 / 186 | 6501 / 5837 |

- The types do not depend on the PSL. A PSL only decides which concrete host falls in which class. So a domain that
  realizes every type under one admissible PSL covers every PSL, with no need to list PSLs. The PSL B run is only a check.
- DomRich is `types2.py --minimize 3` (reverse deletion from 147, twin-closed), renamed: per host class, hosts with 1, 2, 3 ports; 3 opaque.
- Number of origins each property quantifies: OptInCtx 3 (self, top, response; topUrl is read only through PTUrl),
  NestedGroup 3, NestedCap 2 (child = parent), COITop 2, KeyCOI 2, FreshIsolated 3 plus the fresh one (outside the
  domain by construction), InheritedCOI 2. Under the data-independence argument of adequacy/, DomRich suffices for
  all of them. That argument is not a proof. `Fresh` uses CHOOSE only to pick a value outside the domain, which no
  relation can tell apart.
- D18 realized all 96 types of the old relations. It realizes 96 of the 6501 richer types, so the earlier adequacy claim
  does not carry over to this structure.

## Still out, and why

- `domain` / document.domain (same origin-domain): needs effective domains and a mutable origin. No property uses it.
- file: origins, configured trustworthy origins, UA-authenticated schemes (Secure Contexts 3.1 steps 6 to 8): implementation-defined.
- The PSL algorithm (wildcard and exception rules), IDNA, trailing dots, IPv6: only through the `Reg` function.
- Sandbox details: flag inheritance into nested documents and popups, `allow-same-origin`,
  `allow-popups-to-escape-sandbox`. The COOP network error for sandboxed responses (html.src:111944) is approximated:
  an opaque top is never cross-origin isolated.
- Popups' initial about:blank, whose top-level creation URL comes from the creator; workers; history restore of origins;
  blob URL revocation and partitioning; more than one ancestor for Mixed Content.
- NoUndeclaredLeak not re-checked (about 1.4 × 10^8 cases on DomSmall); BodyOnlyByOptIn, on the same operators, was.

The model's claims are about this abstraction. An origin is (scheme, host, port) or an opaque value. Sites are computed
from a PSL that satisfies `PSLAdmissible`. Trustworthiness covers https, loopback and localhost names. Opaque origins
are created and inherited as above. Within that, the restated properties hold for every PSL. Claims that depend on
document.domain, file:, sandbox flags beyond the origin, or a client whose PSL differs from the author's are out of
scope. For the last of these, CrossPSL shows the gap.

## R1 to R3

- R1 (no verdict changes): holds for the properties as restated with spec operators (`CorpPermitsR`, `KeyR`, secure
  context from the top-level URL, inherited policy container). Their verdicts are the same on the richer domain.
- R2 (some verdict changes): holds for operators that build in an earlier reading. The agent-cluster key fails with
  ports (A1's `KeyHTML` too). Treating the CORP condition as trustworthiness fails at localhost. A single opaque value
  fails freshness. A header-only COEP, or a secure context from the document's own origin, fails for inherited and
  sandboxed documents. One cross-spec reading is withheld (see above).
- R3 (some structure only as a parameter): holds for the PSL. It enters as `Reg`. A client whose PSL differs from the
  one the author assumed falls outside any single model (CrossPSL is FALSE).
