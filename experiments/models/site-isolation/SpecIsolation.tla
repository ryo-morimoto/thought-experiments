---------------------------- MODULE SpecIsolation -----------------------------
(* Part 2-a of experiments/2026-11-20-browser-semantics-soundness.md:        *)
(* spec-level isolation with a spec-conformant attacker. Operators follow    *)
(* the WHATWG HTML and Fetch steps quoted in that record. Spec text gives    *)
(* no formal semantics; each operator is the author's reading of it.         *)
(* Simplifications: one response per check, no redirects, no report-only    *)
(* headers, no permissions policy, the implementation-defined choice between *)
(* "logical" and "concrete" cross-origin isolation is fixed to "concrete",   *)
(* and COOP/COEP are ignored on non-secure contexts.                         *)
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
Origins == {OA, OAwww, OB, OAhttp}
AllOrigins == Origins \cup {OAwww2, OAwwwhttp, OBhttp}

SameOrigin(x, y) == x = y
SameSite(x, y)   == x.site = y.site          \* schemelessly same site
Secure(o)        == o.scheme = "https"

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
                "coep-insecure", "coep-cl-strips"}
MechMutants == {"neg:" \o d : d \in DecisionIds}

\* --- HTML: COOP parsing and cross-origin isolation -------------------------
CompatibleCOEP ==
  IF Mutant = "coi-no-credentialless" THEN {"require-corp"}
  ELSE IF Mutant = "coi-coop-only" THEN COEPs
  ELSE {"require-corp", "credentialless"}
ParsedCOOP(coop, coep, o) ==
  IF C("coi-insecure", ~Secure(o)) /\ Mutant # "coi-ignore-secure" THEN "unsafe-none"
  ELSE IF C("coi-coop-so", coop = "same-origin") /\ C("coi-coep-compat", coep \in CompatibleCOEP)
       THEN "same-origin-plus-COEP" ELSE coop

COIMode(coop, coep, o) ==
  IF C("coi-mode", ParsedCOOP(coop, coep, o) = "same-origin-plus-COEP")
  THEN "concrete" ELSE "none"

CrossOriginIsolated(coop, coep, o) == COIMode(coop, coep, o) = "concrete"

\* --- HTML: obtain a similar-origin window agent (agent cluster key) --------
\* hist is the group's historical key for this origin: "absent", "site", "origin".
RequestsOAC(header, o) ==
  C("oac-header", header) /\ (C("oac-secure", Secure(o)) \/ Mutant = "oac-ignore-secure")
KeyKind(o, coiMode, hist, oacHeader) ==
  IF C("oac-coi", coiMode # "none") /\ Mutant # "oac-ignore-coi" THEN "origin"
  ELSE IF C("oac-hist", hist # "absent") /\ Mutant # "oac-ignore-hist" THEN hist
  ELSE IF RequestsOAC(oacHeader, o) THEN "origin" ELSE "site"
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
                     \/ C("corp-ss-scheme", Secure(o) \/ ~Secure(r.origin)))
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
EffectiveCOEP(o, coep) ==
  IF C("coep-insecure", ~Secure(o)) THEN "unsafe-none" ELSE coep
\* Fetch "Cross-Origin-Embedder-Policy allows credentials": a document whose
\* policy is credentialless sends its own cross-origin no-cors requests
\* without credentials, so the response's request-includes-credentials is false.
DocCreds(o, ecoep, mode, r) ==
  IF C("coep-cl-strips", mode = "no-cors" /\ ecoep = "credentialless"
                         /\ ~SameOrigin(o, r.origin))
  THEN [r EXCEPT !.creds = FALSE] ELSE r

\* Result of fetch(url, {mode}) seen by script in a document of origin o.
FetchResult(o, coep, mode, r) ==
  LET ecoep == EffectiveCOEP(o, coep)
      rr    == DocCreds(o, ecoep, mode, r)
  IN
  IF C("fetch-same-origin", SameOrigin(o, r.origin))
     \/ (mode = "no-cors" /\ Mutant = "nocors-site-basic" /\ SameSite(o, r.origin))
  THEN "basic"
  ELSE IF C("fetch-cors", mode = "cors") THEN "cors"  \* CORS outcome not modelled
  ELSE IF C("fetch-blocked", CorpCheck(o, ecoep, rr, FALSE) = "blocked")
       THEN "error" ELSE "opaque"

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
