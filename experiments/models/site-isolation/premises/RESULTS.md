# Premise and conclusion concepts of every property, mapped to spec definitions

For [experiments/2026-11-24-property-premises.md](../../../2026-11-24-property-premises.md) (tree node A1).
Specs: HTML `html.src` 0e292f4, Fetch `fetch.bs` d7fc0fd (job scratch `tmp/extract/data/`, not committed).
Line numbers below are in those files. A subagent wrote this on 2026-11-24. The readings of the spec are its own.
Nothing is committed. No existing file was edited.

## Files

- `premises.tsv`: one row per (property, concept). Columns: property, module, concept, how the model
  represents it, spec anchor, match, note. Rows with property `*` hold for every property that uses the concept.
- `PremisesFix.tla`, `PremisesFix.cfg`, `PremisesFix-samesite-scheme.cfg`: the restated properties (M1 to M4).

## What "match" means

The model's representation compared with the spec concept:

- **exact**: the same cases on the model's domain, and no spec case outside it bears on the property.
- **narrower**: the same on the model's domain, but the spec concept has cases the domain cannot express.
  The property says nothing about them (this is R3).
- **broader**: the representation admits cases that the spec concept excludes.
- **none**: no definition in HTML or Fetch at the pinned commits. This covers definitions of the analysis
  (Declared, Observe, hooks), external specs (DIP, ORB PR, Mixed Content), and one wrong concept that was already fixed.
- `narrower / broader` marks rows that only repeat the OptInOnlySecure pair (secure context narrower, opt-in broader).

## Counts

36 properties, plus the `*` rows. 83 concept rows: 31 exact, 12 narrower, 12 broader, 4 narrower / broader, 24 none.
Of the 24 none rows, 15 are definitions of the analysis, 7 belong to external or unmerged specs, and 2 are the
known wrong premises of OptInOnly and OptInOnlySecureLifted.

## Mismatches and fixes

| id | property | model | spec | fix | TLC |
|---|---|---|---|---|---|
| M1 | OptInOnly*, COIOnlyWithOptIn*, ACSub, OptInOnlySecureD/ORB, ACMonotone | `HasOptIn`: CORP same-site and `SameSite` | internal check (fetch.bs:4459) also needs "origin's scheme is "https" or response's URL's scheme is not "https"" | `CorpPermits` adds that condition | Ctx, PC, COI-top and COI-nested strict forms are TRUE. With `Mutant = "samesite-scheme"` the strict Ctx and PC forms are FALSE, while the originals stay TRUE |
| M2 | same | operator `SameSite` = `.site` equal | it is "schemelessly same site" (html.src:94870); HTML "same site" (html.src:94821) needs equal schemes | read the conclusion as schemelessly same site, or use `CorpPermits` | `OptInOnlyPCHTML` is FALSE. Witness: https://a.test gets opaque from http://a.test with CORP same-site. With Mixed Content (`OptInOnlySecureCtxHTML`) it is TRUE |
| M3 | COIOnlyWithOptInNested | premise: the top document's group mode is concrete | the child's capability also needs "allowed to use" cross-origin-isolated (html.src:99265), default allowlist 'self' (html.src:5570) | premise: group concrete, and the child same origin with its parent | TRUE (`COIOnlyWithOptInNestedStrict`). The original holds under the broader premise, so the property still applies |
| M4 | Gen2Model O rows, WPT oac-separate | `Key`: host or registrable domain, no scheme | key is "a site or tuple origin" (html.src:118245); a site is (scheme, host) (html.src:94802) | `KeyHTML` tags the kind and keeps the scheme | 48 collisions over AllOrigins (e.g. https and http a.test; origin key a.test = site key a.test). ODD is unchanged on all 81 O scenarios, and oac-separate is unchanged |
| M5 | Signature, DIP Conservative | `FetchResult` gives "cors" for every cors fetch | a CORS filtered response needs the CORS check (fetch.bs:7274) | none needed: no premise uses it | not run |
| (known) | OptInOnly, OptInOnlySecureLifted | header COEP; `Secure(ctx.self)` | non-secure context keeps the default (html.src:96928); secure context decided by "top-level creation URL" (html.src:119348) | OptInOnlySecure, OptInOnlySecureCtx, OptInOnlyPC (FIXES.md) | as before: FALSE / FALSE / TRUE TRUE TRUE |

The M1 to M4 checks ran unmutated as invariants: no error. `PrintPremises` output, unmutated:
`optin-ctx-strict TRUE, optin-pc-strict TRUE, optin-ctx-html-samesite TRUE, optin-pc-html-samesite FALSE,
coi-top-strict TRUE, coi-nested-cap-strict TRUE, coi-nested-group-strict TRUE, key-collisions 48,
o-scenarios 81 odd-agrees TRUE, oac-separate-html TRUE`. The originals (Ctx, PC, COI-top, COI-nested) are TRUE.
Under `samesite-scheme`, the first four are all FALSE, and the originals stay TRUE.

## Narrower concepts (domain restrictions, R3)

- secure context (html.src:119312): no data:, localhost, file:, about:blank or about:srcdoc top-level URLs,
  no workers or worklets. "data" is excluded explicitly at html.src:119348.
- origin (html.src:94612): no port, no document.domain, and no opaque origin except in gen2.
- embedder policy: from the header only. No policy-container inheritance, and no report-only value (html.src:96928).
- opener policy values: no `noopener-allow-popups` (html.src:95659, step 1).
- one nesting level (two in gen); no redirects outside RedirectSeq; no CORS-check failure.
- 401 retry (fetch.bs:6525) needs includeCredentials and a prompt. DominanceRetry does not separate it from other retries.

## Definitions of the analysis (none), with justification

- `Observe` and its values: an opaque filtered response has status 0, an empty header list and a null body (fetch.bs:2716).
  Timing and size channels are excluded by choice.
- `Declared`: CORP (fetch.bs:4399) and ACAO (fetch.bs:7274) are the target's opt-ins. `creds` is
  includeCredentials (fetch.bs:6152). It is fixed by the request's credentials mode and response tainting, not by cookies,
  so the requester already knows it.
- `NoHeaderLeak` observation, `Bodies`, `Twin`, the hook kinds and `HookReads`: abstractions for quantifying over
  other specs that add network errors or supply responses. HTML and Fetch have no hook concept.
- `SrcCheck` (P2, P2c): a hypothetical comparison against the navigation source. The spec compares with
  "currentCOOPEnforcementResult's origin" (html.src:95784), which is the previous response.
- `Placement "before"`, `Conservative`, `Signature`, `WPTAgree`: meta properties of the model, or test oracles.
- External specs: DIP (WICG ED), ORB (whatwg/fetch PR #1442), Mixed Content (W3C ED), Permissions Policy allowlists,
  and OACParam "7617" (whatwg/html#7617, unmerged).

## R1 to R3

- R1 (everything corresponds): rejected. M1 and M3 are broader, M4 is narrower, and 24 rows have no HTML or Fetch definition.
- R2 (model-only concepts in premises): partly supported. Declared is in the premise of NoUndeclaredLeak(D), ORB NI and the
  hook flow properties. HookReads and blk are in the hook premises. These are labelled as definitions of the analysis,
  with the reasons above. Every other premise concept has a spec anchor.
- R3 (the spec concept is wider): supported for secure context, origin, embedder policy, opener policy values and request mode.
  The properties hold only on the model's domain.

## A1 done condition

Each property's premise concepts now correspond to a spec definition, or are labelled as a definition of the
analysis or an external spec. So the condition holds with labels. What remains:

- The fixes are proposed only, as new operators. `HasOptIn`, `SameSite` and `Key` in SpecIsolation are unchanged.
  Adopting them is a decision for the record.
- R3 domain gaps: data: and localhost top-level URLs, workers, ports, inherited COEP, and noopener-allow-popups.
- DIP and ORB map to drafts that are not pinned to commits here. Their premises have no HTML or Fetch anchor.
- One person judged the matches, so misreadings of the spec can remain.

## How to run

TLC's library path resolves only one directory, so copy the modules into the container:
`podman run --rm -v <site-isolation>:/spec:Z,ro -w /spec --entrypoint sh localhost/veda-tlc:1.8.0 -c 'mkdir /tmp/w && cp /spec/SpecIsolation.tla /spec/gen2/Gen2Model.tla /spec/gen2/Gen2Space.tla /spec/premises/PremisesFix.tla /spec/premises/PremisesFix.cfg /tmp/w && cd /tmp/w && java -cp /opt/tla2tools.jar tlc2.TLC -metadir /tmp/st-x -config PremisesFix.cfg PremisesFix.tla'`
(about 6 s). For the mutant run, use `PremisesFix-samesite-scheme.cfg` instead.
