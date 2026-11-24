--------------------------- MODULE SpecIsolationPT ----------------------------
(* Part 2-a of experiments/2026-11-20-browser-semantics-soundness.md:        *)
(* spec-level isolation with a spec-conformant attacker. Operators follow    *)
(* the WHATWG HTML and Fetch steps quoted in that record. Spec text gives    *)
(* no formal semantics; each operator is the author's reading of it.         *)
(* Simplifications: one response per check, no redirects, no report-only    *)
(* headers, no permissions policy, the implementation-defined choice between *)
(* "logical" and "concrete" cross-origin isolation is fixed to "concrete",   *)
(* and COOP/COEP are ignored on non-secure contexts.                         *)
(* fixes/FIXES.md adds document contexts (secure context from the top-level *)
(* creation URL), one level of nested navigation, and Mixed Content, each   *)
(* gated by a decision id in FixIds (experiments/2026-11-23-havoc-unmodeled- *)
(* steps.md found the gaps). Old operator signatures are kept.              *)
EXTENDS Naturals, Sequences, TLC

\* Deliberate misreadings, to see which ones WPT agreement would catch.
\* "none" is the reading above; each other value changes one step.
CONSTANT Mutant
Mutants == {
  "coep-default",        \* require-corp does not default a missing CORP to same-origin
  "samesite-scheme",     \* CORP same-site ignores the https -> http scheme condition
  "cl-ignore-creds",     \* credentialless never defaults a missing CORP
  "cl-always",           \* credentialless defaults like require-corp
  "coi-ignore-secure",   \* COOP/COEP honoured on non-secure contexts
  "coi-coop-only",       \* COOP same-origin alone gives cross-origin isolation
  "coi-no-credentialless", \* only require-corp is compatible with isolation
  "oac-ignore-hist",     \* agent-cluster key ignores the historical map
  "oac-ignore-coi",      \* isolation does not force origin keying
  "oac-ignore-secure",   \* Origin-Agent-Cluster honoured on non-secure contexts
  "coop-ignore-origin",  \* matching COOP values ignores the same-origin condition
  "coop-unsafe-mismatch", \* unsafe-none on both sides does not match
  "samesite-as-origin",  \* CORP same-site requires same origin
  "crossorigin-as-site", \* CORP cross-origin treated as same-site
  "nocors-site-basic",   \* same-site no-cors responses are readable (basic)
  "popup-no-sap-exception" \* the author's first reading: no allow-popups step
}
\* Misreadings that only touch the information-flow observation (part 4):
FlowMutants == {"opaque-length"}  \* opaque responses expose the body length

\* Origins are records; site is the registrable domain.
OA     == [scheme |-> "https", host |-> "a.test",      site |-> "a.test"]
OAwww  == [scheme |-> "https", host |-> "www1.a.test", site |-> "a.test"]
OB     == [scheme |-> "https", host |-> "b.test",      site |-> "b.test"]
OAhttp == [scheme |-> "http",  host |-> "a.test",      site |-> "a.test"]
OAwww2 == [scheme |-> "https", host |-> "www2.a.test", site |-> "a.test"]
OAwwwhttp == [scheme |-> "http", host |-> "www1.a.test", site |-> "a.test"]
OBhttp == [scheme |-> "http",  host |-> "b.test",      site |-> "b.test"]
OLocal  == [scheme |-> "http",  host |-> "localhost", site |-> "localhost"]
OLocalS == [scheme |-> "https", host |-> "localhost", site |-> "localhost"]
Origins == {OA, OAwww, OB, OAhttp, OLocal, OLocalS}
AllOrigins == Origins \cup {OAwww2, OAwwwhttp, OBhttp}

SameOrigin(x, y) == x = y
SameSite(x, y)   == x.site = y.site          \* schemelessly same site
\* premises/round2: Secure is now "potentially trustworthy" (localhost too);
\* the CORP scheme test uses the literal scheme, as Fetch says.
Secure(o)        == o.scheme = "https" \/ o.host = "localhost"
SchemeHttps(o)   == o.scheme = "https"

COOPs == {"unsafe-none", "same-origin", "same-origin-allow-popups"}
COEPs == {"unsafe-none", "require-corp", "credentialless"}
CORPs == {"none", "same-origin", "same-site", "cross-origin"}

\* Mechanical mutants: every decision in the spec operators is wrapped as
\* C(id, e). Only the named decision changes:
\*   "neg:<id>"   negate it
\*   "false:<id>" always false: the step guarded by it is omitted
\*   "true:<id>"  always true: the check it makes is omitted
C(id, e) ==
  CASE Mutant = "neg:" \o id   -> ~e
    [] Mutant = "false:" \o id -> FALSE
    [] Mutant = "true:" \o id  -> TRUE
    [] OTHER                   -> e
DecisionIds == {"coi-insecure", "coi-coop-so", "coi-coep-compat", "coi-mode",
                "oac-coi", "oac-hist", "oac-header", "oac-secure",
                "coop-both-unsafe", "coop-one-unsafe", "coop-equal", "coop-same-origin",
                "popup-opener-sap", "popup-unsafe",
                "corp-nav", "corp-has-header", "corp-cl-creds", "corp-allow-kinds",
                "corp-so-check", "corp-ss-site", "corp-ss-scheme", "corp-first-pass",
                "fetch-same-origin", "fetch-cors", "fetch-blocked",
                "coep-insecure", "coep-cl-strips",
                \* added in fixes/FIXES.md (experiments/2026-11-23-havoc-unmodeled-steps.md)
                "secure-ctx-top", "nav-corp-check", "nav-coep-adherence",
                "mc-ancestor", "mc-upgrade", "mc-block"}
\* The steps added in fixes/FIXES.md; "false:<id>" omits one of them.
FixIds == {"secure-ctx-top", "nav-corp-check", "nav-coep-adherence",
           "mc-ancestor", "mc-upgrade", "mc-block"}
FixMutants == {"false:" \o d : d \in FixIds}
MechMutants == {"neg:" \o d : d \in DecisionIds}

\* A document's context (fixes/FIXES.md, G1). self: the document's origin;
\* top: the origin of its environment's top-level creation URL, i.e. of the
\* top-level document. A top-level document has top = self. One nesting
\* level; data: top-level URLs and workers are not modelled.
TopCtx(o) == [self |-> o, top |-> o]
Contexts  == [self : Origins, top : Origins]
\* HTML "secure context": decided by the top-level creation URL alone.
\* "false:secure-ctx-top" gives back the earlier per-origin reading.
SecureCtx(ctx) ==
  IF C("secure-ctx-top", ctx.top # ctx.self) THEN Secure(ctx.top) ELSE Secure(ctx.self)
\* "Compatible with cross-origin isolation" as the spec defines it (not
\* subject to the named Mutants, which change CompatibleCOEP).
CompatCOI == {"require-corp", "credentialless"}
\* Cross-origin resource policy "opt-in" of a response r to a requester o.
HasOptIn(o, r) == r.corp = "cross-origin" \/ (r.corp = "same-site" /\ SameSite(o, r.origin))

\* --- HTML: COOP parsing and cross-origin isolation -------------------------
CompatibleCOEP ==
  IF Mutant = "coi-no-credentialless" THEN {"require-corp"}
  ELSE IF Mutant = "coi-coop-only" THEN COEPs
  ELSE {"require-corp", "credentialless"}
ParsedCOOP(coop, coep, o) ==
  IF C("coi-insecure", ~Secure(o)) /\ Mutant # "coi-ignore-secure" THEN "unsafe-none"
  ELSE IF C("coi-coop-so", coop = "same-origin") /\ C("coi-coep-compat", coep \in CompatibleCOEP)
       THEN "same-origin-plus-COEP" ELSE coop

\* HTML "obtain a browsing context to use for a navigation response": the new
\* group's cross-origin isolation mode is "logical" or "concrete"
\* (implementation-defined). The model fixes "concrete"; the run with
\* Mutant = "param:coi-logical" uses "logical" instead. It is a parameter, not
\* a misreading, so it is not in Mutants (experiments/2026-11-21-informal-enumerated-choice.md).
COIChoice == IF Mutant = "param:coi-logical" THEN "logical" ELSE "concrete"
COIMode(coop, coep, o) ==
  IF C("coi-mode", ParsedCOOP(coop, coep, o) = "same-origin-plus-COEP")
  THEN COIChoice ELSE "none"

CrossOriginIsolated(coop, coep, o) == COIMode(coop, coep, o) = "concrete"

\* --- HTML: obtain a similar-origin window agent (agent cluster key) --------
\* hist is the group's historical key for this origin: "absent", "site", "origin".
\* The reserved environment's secure-ness is that of the context (G1);
\* KeyKind(o, ...) is the top-level case.
RequestsOACCtx(header, ctx) ==
  C("oac-header", header) /\ (C("oac-secure", SecureCtx(ctx)) \/ Mutant = "oac-ignore-secure")
RequestsOAC(header, o) == RequestsOACCtx(header, TopCtx(o))
KeyKindCtx(ctx, coiMode, hist, oacHeader) ==
  IF C("oac-coi", coiMode # "none") /\ Mutant # "oac-ignore-coi" THEN "origin"
  ELSE IF C("oac-hist", hist # "absent") /\ Mutant # "oac-ignore-hist" THEN hist
  ELSE IF RequestsOACCtx(oacHeader, ctx) THEN "origin" ELSE "site"
KeyKind(o, coiMode, hist, oacHeader) == KeyKindCtx(TopCtx(o), coiMode, hist, oacHeader)
Key(o, kind) == IF kind = "origin" THEN o.host ELSE o.site
OriginAgentCluster(kind) == kind = "origin"
\* document.domain setter is a no-op when the cluster is origin-keyed.
DocumentDomainNoOp(kind) == kind = "origin"

\* --- HTML: match opener policy values (popup BCG switch) -------------------
MatchCOOP(dCOOP, dOrigin, rCOOP, rOrigin) ==
  IF C("coop-both-unsafe", dCOOP = "unsafe-none" /\ rCOOP = "unsafe-none")
  THEN Mutant # "coop-unsafe-mismatch"
  ELSE IF C("coop-one-unsafe", dCOOP = "unsafe-none" \/ rCOOP = "unsafe-none") THEN FALSE
  ELSE IF C("coop-equal", dCOOP = rCOOP)
          /\ (C("coop-same-origin", SameOrigin(dOrigin, rOrigin)) \/ Mutant = "coop-ignore-origin")
       THEN TRUE
  ELSE FALSE
\* A popup's initial about:blank carries the opener's COOP and origin.
\* HTML "check if popup COOP values require a browsing context group switch".
\* The first version of this model omitted the same-origin-allow-popups step;
\* 3 of the 109 broad WPT cases caught it (kept as a mutant below).
PopupSevered(openerCOOP, openerOrigin, popupCOOP, popupOrigin) ==
  IF C("popup-opener-sap", openerCOOP = "same-origin-allow-popups")
     /\ C("popup-unsafe", popupCOOP = "unsafe-none")
     /\ Mutant # "popup-no-sap-exception"
  THEN FALSE
  ELSE ~MatchCOOP(openerCOOP, openerOrigin, popupCOOP, popupOrigin)

\* --- Fetch: cross-origin resource policy check ----------------------------
CorpInternal(o, coep, r, forNav) ==
  IF C("corp-nav", forNav /\ coep = "unsafe-none") THEN "allowed"
  ELSE
    LET p0 == IF r.corp = "cross-origin" /\ Mutant = "crossorigin-as-site"
              THEN "same-site" ELSE r.corp
        p  == IF C("corp-has-header", p0 # "none") THEN p0
              ELSE CASE coep = "unsafe-none"    -> "none"
                     [] coep = "credentialless" ->
                          IF Mutant = "cl-ignore-creds" THEN "none"
                          ELSE IF Mutant = "cl-always" THEN "same-origin"
                          ELSE IF C("corp-cl-creds", r.creds \/ forNav)
                               THEN "same-origin" ELSE "none"
                     [] coep = "require-corp"   ->
                          IF Mutant = "coep-default" THEN "none" ELSE "same-origin"
    IN IF C("corp-allow-kinds", p \in {"none", "cross-origin"}) THEN "allowed"
       ELSE IF p = "same-origin"
            THEN IF C("corp-so-check", SameOrigin(o, r.origin)) THEN "allowed" ELSE "blocked"
       ELSE \* p = "same-site"
              IF C("corp-ss-site", IF Mutant = "samesite-as-origin" THEN SameOrigin(o, r.origin)
                                   ELSE SameSite(o, r.origin))
                 /\ (Mutant = "samesite-scheme"
                     \/ C("corp-ss-scheme", SchemeHttps(o) \/ ~SchemeHttps(r.origin)))
              THEN "allowed" ELSE "blocked"

CorpCheck(o, coep, r, forNav) ==
  IF C("corp-first-pass", CorpInternal(o, "unsafe-none", r, forNav) = "blocked")
  THEN "blocked"
  ELSE CorpInternal(o, coep, r, forNav)

\* Steps added after the step-coverage measurement
\* (experiments/2026-11-21-fsp-correspondence.md). Negating either with
\* "false:<id>" gives back the earlier model that omitted it.
\* HTML "obtain an embedder policy" step 2: a non-secure context keeps the
\* default policy (unsafe-none).
\* Since fixes/FIXES.md (G1), "non-secure context" is SecureCtx of the
\* document's context; EffectiveCOEP(o, coep) is the top-level case.
EffectiveCOEPCtx(ctx, coep) ==
  IF C("coep-insecure", ~SecureCtx(ctx)) THEN "unsafe-none" ELSE coep
EffectiveCOEP(o, coep) == EffectiveCOEPCtx(TopCtx(o), coep)
\* Fetch "Cross-Origin-Embedder-Policy allows credentials": a document whose
\* policy is credentialless sends its own cross-origin no-cors requests
\* without credentials, so the response's request-includes-credentials is false.
DocCreds(o, ecoep, mode, r) ==
  IF C("coep-cl-strips", mode = "no-cors" /\ ecoep = "credentialless"
                         /\ ~SameOrigin(o, r.origin))
  THEN [r EXCEPT !.creds = FALSE] ELSE r

\* Result of a fetch by a document in context ctx whose policy container's
\* embedder policy is ecoep (whether parsed from its own header or
\* inherited). The part below Mixed Content.
FetchResultPC(ctx, ecoep, mode, r) ==
  LET o  == ctx.self
      rr == DocCreds(o, ecoep, mode, r)
  IN
  IF C("fetch-same-origin", SameOrigin(o, r.origin))
     \/ (mode = "no-cors" /\ Mutant = "nocors-site-basic" /\ SameSite(o, r.origin))
  THEN "basic"
  ELSE IF C("fetch-cors", mode = "cors") THEN "cors"  \* CORS outcome not modelled
  ELSE IF C("fetch-blocked", CorpCheck(o, ecoep, rr, FALSE) = "blocked")
       THEN "error" ELSE "opaque"

\* --- Mixed Content (fixes/FIXES.md, G3) -----------------------------------
\* Mixed Content 4.3: the client prohibits mixed security contexts if its
\* origin, or an ancestor document's origin, is potentially trustworthy.
ProhibitsMixed(ctx) == Secure(ctx.self) \/ C("mc-ancestor", Secure(ctx.top))
IsMixed(ctx, r) == ProhibitsMixed(ctx) /\ ~Secure(r.origin)
\* 4.1 rewrites only the scheme; the explicit port is kept.
HttpsTwin(o) == [o EXCEPT !.scheme = "https"]
\* dest: "fetch" (fetch(), blockable) or "image" (<img>, upgradeable).
\* served: whether a TLS server answers at the upgraded URL (same host and
\* port). It is an input about the target, not a choice of the browser.
\* The upgraded request reaches the https twin with the same headers.
FetchResultDest(ctx, coep, mode, dest, r, served) ==
  LET up == C("mc-upgrade", IsMixed(ctx, r) /\ dest = "image")
      rr == IF up THEN [r EXCEPT !.origin = HttpsTwin(r.origin)] ELSE r
  IN IF up /\ ~served THEN "error"   \* network error: no TLS at that port
     ELSE IF C("mc-block", IsMixed(ctx, rr)) THEN "error"   \* 4.4: blocked
     ELSE FetchResultPC(ctx, EffectiveCOEPCtx(ctx, coep), mode, rr)

\* fetch() from a document in context ctx.
FetchResultCtx(ctx, coep, mode, r) == FetchResultDest(ctx, coep, mode, "fetch", r, TRUE)
\* <img> from a top-level document (element rows: basic/opaque mean "load").
ImageResult(o, coep, r, served) ==
  FetchResultDest(TopCtx(o), coep, "no-cors", "image", r, served)
\* Result of fetch(url, {mode}) seen by script in a top-level document of
\* origin o. Before fixes/FIXES.md this was FetchResultPC(TopCtx(o),
\* EffectiveCOEP(o, coep), mode, r), without Mixed Content.
FetchResult(o, coep, mode, r) == FetchResultCtx(TopCtx(o), coep, mode, r)

\* --- HTML: nested navigation (fixes/FIXES.md, G2) --------------------------
\* A child navigable whose container document has context pctx and policy
\* container embedder policy pecoep navigates to response r. cecoep is the
\* policy container embedder policy the child document would get.
ChildCtx(pctx, r) == [self |-> r.origin, top |-> pctx.top]
NavChildPC(pctx, pecoep, r, cecoep) ==
  \* Mixed Content 4.4: an iframe request is blockable.
  IF C("mc-block", IsMixed(pctx, r)) THEN "error"
  \* create navigation params by fetching: CORP check with forNavigation
  \* against the container document.
  ELSE IF C("nav-corp-check", CorpCheck(pctx.self, pecoep, r, TRUE) = "blocked") THEN "error"
  \* check a navigation response's adherence to its embedder policy.
  ELSE IF C("nav-coep-adherence", pecoep \in CompatCOI /\ cecoep \notin CompatCOI) THEN "error"
  ELSE "loaded"
\* ccoep: the COEP header of r.
NavChild(pctx, pecoep, r, ccoep) ==
  NavChildPC(pctx, pecoep, r, EffectiveCOEPCtx(ChildCtx(pctx, r), ccoep))

Responses == [origin : Origins, corp : CORPs, creds : BOOLEAN]

\* --- WPT expectations (scenarios and expected results from the record) ----
Rsp(o, c) == [origin |-> o, corp |-> c, creds |-> FALSE]

WPTCases == {
  \* credentialless/cross-origin-isolated.window.js
  [name |-> "coi-cl-https", got |-> CrossOriginIsolated("same-origin", "credentialless", OA),     want |-> TRUE],
  [name |-> "coi-cl-http",  got |-> CrossOriginIsolated("same-origin", "credentialless", OAhttp), want |-> FALSE],
  [name |-> "coi-coep-only", got |-> CrossOriginIsolated("unsafe-none", "credentialless", OA),    want |-> FALSE],
  [name |-> "coi-coep-ro",  got |-> CrossOriginIsolated("same-origin", "unsafe-none", OA),       want |-> FALSE],
  \* origin-keyed-agent-clusters/getter-special-cases/cross-origin-isolated
  [name |-> "oac-coi-child", got |-> OriginAgentCluster(KeyKind(OAwww, "concrete", "absent", FALSE)), want |-> TRUE],
  \* cross-origin-embedder-policy/require-corp.https.html
  [name |-> "rc-nocors-nocorp", got |-> FetchResult(OA, "require-corp", "no-cors", Rsp(OB, "none")),         want |-> "error"],
  [name |-> "rc-nocors-corpxo", got |-> FetchResult(OA, "require-corp", "no-cors", Rsp(OB, "cross-origin")), want |-> "opaque"],
  \* fetch/cross-origin-resource-policy/fetch.any.js (no COEP)
  [name |-> "corp-so-xsite",   got |-> FetchResult(OA, "unsafe-none", "no-cors", Rsp(OB, "same-origin")), want |-> "error"],
  [name |-> "corp-ss-xsite",   got |-> FetchResult(OA, "unsafe-none", "no-cors", Rsp(OB, "same-site")),   want |-> "error"],
  [name |-> "corp-ss-samesite", got |-> FetchResult(OA, "unsafe-none", "no-cors", Rsp(OAwww, "same-site")), want |-> "opaque"],
  \* cross-origin-opener-policy/popup-same-origin-with-{cross,same}-origin
  [name |-> "popup-xo-so",  got |-> PopupSevered("same-origin", OA, "same-origin", OB),  want |-> TRUE],
  [name |-> "popup-xo-un",  got |-> PopupSevered("same-origin", OA, "unsafe-none", OB),  want |-> TRUE],
  [name |-> "popup-so-so",  got |-> PopupSevered("same-origin", OA, "same-origin", OA),  want |-> FALSE],
  [name |-> "popup-so-sap", got |-> PopupSevered("same-origin", OA, "same-origin-allow-popups", OA), want |-> TRUE],
  \* origin-keyed-agent-clusters/document-domain and 1-iframe/parent-no-child-yes-subdomain
  [name |-> "oac-docdomain", got |-> DocumentDomainNoOp(KeyKind(OA, "none", "absent", TRUE)), want |-> TRUE],
  [name |-> "oac-parent",    got |-> OriginAgentCluster(KeyKind(OA, "none", "absent", FALSE)), want |-> FALSE],
  [name |-> "oac-child",     got |-> OriginAgentCluster(KeyKind(OAwww, "none", "absent", TRUE)), want |-> TRUE],
  [name |-> "oac-separate",  got |-> Key(OA, KeyKind(OA, "none", "absent", FALSE))
                                     # Key(OAwww, KeyKind(OAwww, "none", "absent", TRUE)), want |-> TRUE]
}
WPTAgree == \A t \in WPTCases : t.got = t.want
Mismatches == {t.name : t \in {u \in WPTCases : u.got # u.want}}

\* --- Global properties ------------------------------------------------------
\* Access control: in a context with COEP require-corp, cross-origin bytes
\* arrive only if the response opted in with CORP.
OptInOnly ==
  \A o \in Origins, r \in Responses :
    FetchResult(o, "require-corp", "no-cors", r) = "opaque" =>
      \/ r.corp = "cross-origin"
      \/ r.corp = "same-site" /\ SameSite(o, r.origin)

\* OptInOnly is false once a non-secure context keeps COEP unsafe-none
\* (experiments/2026-11-21-fsp-correspondence.md). The property restated with
\* the condition the spec puts on COEP: only secure contexts get the guarantee.
OptInOnlySecure ==
  \A o \in Origins, r \in Responses :
    (Secure(o) /\ FetchResult(o, "require-corp", "no-cors", r) = "opaque") =>
      \/ r.corp = "cross-origin"
      \/ r.corp = "same-site" /\ SameSite(o, r.origin)
\* One requester and response for which OptInOnly fails.
OptInWitness ==
  CHOOSE x \in Origins \X Responses :
    /\ FetchResult(x[1], "require-corp", "no-cors", x[2]) = "opaque"
    /\ ~(x[2].corp = "cross-origin" \/ (x[2].corp = "same-site" /\ SameSite(x[1], x[2].origin)))
PrintOptIn == PrintT(<<"optin-witness", OptInWitness>>)

\* --- Properties added in fixes/FIXES.md -------------------------------------
\* OptInOnlySecure quantifies over top-level documents only, so the fixes
\* leave it unchanged by construction. Lifted to nested contexts with its
\* old premise (https origin), and restated over secure contexts (G1).
OptInOnlySecureLifted ==
  \A ctx \in Contexts, r \in Responses :
    (Secure(ctx.self) /\ FetchResultCtx(ctx, "require-corp", "no-cors", r) = "opaque") =>
      HasOptIn(ctx.self, r)
OptInOnlySecureCtx ==
  \A ctx \in Contexts, r \in Responses :
    (SecureCtx(ctx) /\ FetchResultCtx(ctx, "require-corp", "no-cors", r) = "opaque") =>
      HasOptIn(ctx.self, r)
\* Premise on the policy container's embedder policy, whatever wrote it
\* (header or inheritance), instead of the header.
OptInOnlyPC ==
  \A ctx \in Contexts, r \in Responses :
    FetchResultPC(ctx, "require-corp", "no-cors", r) = "opaque" => HasOptIn(ctx.self, r)
\* G2: DIPExtension's COIOnlyWithOptIn (no DIP) for a top-level document
\* and for a child it embeds. If the top-level document is cross-origin
\* isolated and the child loads, (1) the navigation response itself is
\* same-origin or opted in, and (2) the child's cross-origin no-cors bytes
\* arrive only without credentials or with an opt-in.
COIOnlyWithOptInNested ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, r \in Responses,
     ccoep \in COEPs, s \in Responses :
    LET pctx == TopCtx(o)
        cctx == ChildCtx(pctx, r)
        cec  == EffectiveCOEPCtx(cctx, ccoep)
        ss   == DocCreds(cctx.self, cec, "no-cors", s)
    IN (CrossOriginIsolated(coop, coep, o) /\ NavChild(pctx, EffectiveCOEP(o, coep), r, ccoep) = "loaded")
       => /\ (SameOrigin(o, r.origin) \/ HasOptIn(o, r))
          /\ (FetchResultCtx(cctx, ccoep, "no-cors", s) = "opaque" => (~ss.creds \/ HasOptIn(cctx.self, s)))
\* Same, without the child (DIPExtension's COIOnlyWithOptIn, dip = "none").
COIOnlyWithOptInTop ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, s \in Responses :
    LET ss == DocCreds(o, EffectiveCOEP(o, coep), "no-cors", s) IN
    (CrossOriginIsolated(coop, coep, o) /\ FetchResult(o, coep, "no-cors", s) = "opaque")
      => (~ss.creds \/ HasOptIn(o, s))
NestedWitness ==
  CHOOSE x \in Origins \X COOPs \X COEPs \X Responses \X COEPs \X Responses :
    LET pctx == TopCtx(x[1]) cctx == ChildCtx(pctx, x[4])
        ss == DocCreds(cctx.self, EffectiveCOEPCtx(cctx, x[5]), "no-cors", x[6]) IN
    /\ CrossOriginIsolated(x[2], x[3], x[1])
    /\ NavChild(pctx, EffectiveCOEP(x[1], x[3]), x[4], x[5]) = "loaded"
    /\ ~(/\ (SameOrigin(x[1], x[4].origin) \/ HasOptIn(x[1], x[4]))
         /\ (FetchResultCtx(cctx, x[5], "no-cors", x[6]) = "opaque" => (~ss.creds \/ HasOptIn(cctx.self, x[6]))))
LiftedWitness ==
  CHOOSE x \in Contexts \X Responses :
    Secure(x[1].self) /\ FetchResultCtx(x[1], "require-corp", "no-cors", x[2]) = "opaque"
    /\ ~HasOptIn(x[1].self, x[2])
PrintFixes == PrintT(<<"fixes", Mutant,
  <<"optin-only-secure", OptInOnlySecure>>,
  <<"optin-only-secure-lifted", OptInOnlySecureLifted,
    IF OptInOnlySecureLifted THEN "-" ELSE LiftedWitness>>,
  <<"optin-only-secure-ctx", OptInOnlySecureCtx>>,
  <<"optin-only-pc", OptInOnlyPC>>,
  <<"coi-optin-top", COIOnlyWithOptInTop>>,
  <<"coi-optin-nested", COIOnlyWithOptInNested,
    IF COIOnlyWithOptInNested THEN "-" ELSE NestedWitness>>>>)

\* Noninterference: what a page observes about a cross-origin no-cors fetch
\* does not depend on the target's response headers.
NoHeaderLeak ==
  \A o \in Origins, coep \in COEPs, r1, r2 \in Responses :
    (r1.origin = r2.origin /\ r1.creds = r2.creds /\ ~SameOrigin(o, r1.origin)) =>
      FetchResult(o, coep, "no-cors", r1) = FetchResult(o, coep, "no-cors", r2)

\* --- Part 4: isolation as information flow with declared channels ----------
\* A response now has a secret body and a CORS opt-in. What a page sees:
\* same-origin or CORS-allowed bodies are readable; a CORP-blocked no-cors
\* fetch is an error; any other cross-origin no-cors fetch is opaque.
Bodies == {"x", "yy"}                 \* two secrets of different length
FlowResponses ==
  [origin : Origins, corp : CORPs, creds : BOOLEAN, acao : BOOLEAN, body : Bodies]
Base(r) == [origin |-> r.origin, corp |-> r.corp, creds |-> r.creds]

Observe(o, coep, mode, r) ==
  IF SameOrigin(o, r.origin) THEN <<"read", r.body>>
  ELSE IF mode = "cors" THEN (IF r.acao THEN <<"read", r.body>> ELSE <<"error">>)
  ELSE IF CorpCheck(o, EffectiveCOEP(o, coep),
                    DocCreds(o, EffectiveCOEP(o, coep), mode, Base(r)), FALSE) = "blocked"
       THEN <<"error">>
  ELSE IF Mutant = "opaque-length" THEN <<"opaque", Len(r.body)>>
  ELSE <<"opaque">>

\* Declared channels: what the target chose to reveal. Its headers (CORP,
\* ACAO), whether the request carried credentials, and the body only when it
\* opted in to CORS. The error-or-opaque oracle is declared through CORP.
Declared(mode, r) ==
  <<r.corp, r.creds, r.acao, IF mode = "cors" /\ r.acao THEN r.body ELSE "hidden">>

NoUndeclaredLeak ==
  \A o \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"},
     r1, r2 \in FlowResponses :
    (/\ r1.origin = r2.origin
     /\ ~SameOrigin(o, r1.origin)
     /\ Declared(mode, r1) = Declared(mode, r2))
    => Observe(o, coep, mode, r1) = Observe(o, coep, mode, r2)

\* The access-control property follows from the flow property's declarations:
\* a cross-origin body is readable only through the CORS declaration.
BodyOnlyByOptIn ==
  \A o \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"}, r \in FlowResponses :
    (~SameOrigin(o, r.origin) /\ Observe(o, coep, mode, r)[1] = "read") => r.acao

\* Every operator's output over its whole input domain. Two Mutant values
\* with the same Signature are equivalent: no test of these operators can
\* tell them apart.
AllResponses == [origin : AllOrigins, corp : CORPs, creds : BOOLEAN]
Signature ==
  <<[x \in COOPs \X COEPs \X AllOrigins |-> CrossOriginIsolated(x[1], x[2], x[3])],
    [x \in AllOrigins \X {"none", "concrete"} \X {"absent", "site", "origin"} \X BOOLEAN
        |-> KeyKind(x[1], x[2], x[3], x[4])],
    [x \in COOPs \X AllOrigins \X COOPs \X AllOrigins |-> PopupSevered(x[1], x[2], x[3], x[4])],
    [x \in AllOrigins \X COEPs \X {"cors", "no-cors"} \X AllResponses
        |-> FetchResult(x[1], x[2], x[3], x[4])]>>
\* The same outputs as nested sequences over fixed input orders. TLC prints
\* functions over record domains in no stable order, so equivalence is judged
\* on this form.
OSeq    == <<OA, OAwww, OAwww2, OB, OAhttp, OAwwwhttp, OBhttp>>
COOPSeq == <<"unsafe-none", "same-origin", "same-origin-allow-popups">>
COEPSeq == <<"unsafe-none", "require-corp", "credentialless">>
CORPSeq == <<"none", "same-origin", "same-site", "cross-origin">>
BoolSeq == <<FALSE, TRUE>>
Seq7 == 1..7
SignatureSeq ==
  <<[a \in 1..3 |-> [b \in 1..3 |-> [c \in Seq7 |->
       IF CrossOriginIsolated(COOPSeq[a], COEPSeq[b], OSeq[c]) THEN 1 ELSE 0]]],
    [a \in Seq7 |-> [b \in 1..2 |-> [c \in 1..3 |-> [d \in 1..2 |->
       KeyKind(OSeq[a], <<"none", "concrete">>[b], <<"absent", "site", "origin">>[c],
               BoolSeq[d])]]]],
    [a \in 1..3 |-> [b \in Seq7 |-> [c \in 1..3 |-> [d \in Seq7 |->
       IF PopupSevered(COOPSeq[a], OSeq[b], COOPSeq[c], OSeq[d]) THEN 1 ELSE 0]]]],
    [a \in Seq7 |-> [b \in 1..3 |-> [c \in 1..2 |-> [d \in Seq7 |-> [e \in 1..4 |->
       [f \in 1..2 |->
         FetchResult(OSeq[a], COEPSeq[b], <<"cors", "no-cors">>[c],
                     [origin |-> OSeq[d], corp |-> CORPSeq[e], creds |-> BoolSeq[f]])]]]]]]>>
PrintSignature == PrintT(<<"signature", SignatureSeq>>)

\* One pair of responses that the page can tell apart.
LeakWitness ==
  CHOOSE w \in [o : Origins, coep : COEPs, r1 : Responses, r2 : Responses] :
    /\ w.r1.origin = w.r2.origin /\ w.r1.creds = w.r2.creds
    /\ ~SameOrigin(w.o, w.r1.origin)
    /\ FetchResult(w.o, w.coep, "no-cors", w.r1) # FetchResult(w.o, w.coep, "no-cors", w.r2)
PrintLeak == PrintT(<<"leak", LeakWitness,
                      FetchResult(LeakWitness.o, LeakWitness.coep, "no-cors", LeakWitness.r1),
                      FetchResult(LeakWitness.o, LeakWitness.coep, "no-cors", LeakWitness.r2)>>)
PrintMismatches == PrintT(<<"mismatches", Mutant, Mismatches>>)

\* Constant-level module: a single state; the checks are invariants.
VARIABLE dummy
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
