---------------------------- MODULE SpecIsolation -----------------------------
(* Part 2-a of experiments/2026-11-20-browser-semantics-soundness.md:        *)
(* spec-level isolation with a spec-conformant attacker. Operators follow    *)
(* the WHATWG HTML and Fetch steps quoted in that record. Spec text gives    *)
(* no formal semantics; each operator is the author's reading of it.         *)
(* Simplifications: one response per check, no redirects, no report-only    *)
(* headers, no permissions policy, the implementation-defined choice between *)
(* "logical" and "concrete" cross-origin isolation is fixed to "concrete",   *)
(* and COOP/COEP are ignored on non-secure contexts.                         *)
EXTENDS Naturals, TLC

\* Deliberate misreadings, to see which ones WPT agreement would catch:
\*   "none"            the reading above
\*   "coep-default"    require-corp does not default a missing CORP to same-origin
\*   "samesite-scheme" CORP same-site ignores the https -> http scheme condition
CONSTANT Mutant

\* Origins are records; site is the registrable domain.
OA     == [scheme |-> "https", host |-> "a.test",      site |-> "a.test"]
OAwww  == [scheme |-> "https", host |-> "www1.a.test", site |-> "a.test"]
OB     == [scheme |-> "https", host |-> "b.test",      site |-> "b.test"]
OAhttp == [scheme |-> "http",  host |-> "a.test",      site |-> "a.test"]
Origins == {OA, OAwww, OB, OAhttp}

SameOrigin(x, y) == x = y
SameSite(x, y)   == x.site = y.site          \* schemelessly same site
Secure(o)        == o.scheme = "https"

COOPs == {"unsafe-none", "same-origin", "same-origin-allow-popups"}
COEPs == {"unsafe-none", "require-corp", "credentialless"}
CORPs == {"none", "same-origin", "same-site", "cross-origin"}

\* --- HTML: COOP parsing and cross-origin isolation -------------------------
ParsedCOOP(coop, coep, o) ==
  IF ~Secure(o) THEN "unsafe-none"
  ELSE IF coop = "same-origin" /\ coep \in {"require-corp", "credentialless"}
       THEN "same-origin-plus-COEP" ELSE coop

COIMode(coop, coep, o) ==
  IF ParsedCOOP(coop, coep, o) = "same-origin-plus-COEP" THEN "concrete" ELSE "none"

CrossOriginIsolated(coop, coep, o) == COIMode(coop, coep, o) = "concrete"

\* --- HTML: obtain a similar-origin window agent (agent cluster key) --------
\* hist is the group's historical key for this origin: "absent", "site", "origin".
RequestsOAC(header, o) == header /\ Secure(o)
KeyKind(o, coiMode, hist, oacHeader) ==
  IF coiMode # "none" THEN "origin"
  ELSE IF hist # "absent" THEN hist
  ELSE IF RequestsOAC(oacHeader, o) THEN "origin" ELSE "site"
Key(o, kind) == IF kind = "origin" THEN o.host ELSE o.site
OriginAgentCluster(kind) == kind = "origin"
\* document.domain setter is a no-op when the cluster is origin-keyed.
DocumentDomainNoOp(kind) == kind = "origin"

\* --- HTML: match opener policy values (popup BCG switch) -------------------
MatchCOOP(dCOOP, dOrigin, rCOOP, rOrigin) ==
  IF dCOOP = "unsafe-none" /\ rCOOP = "unsafe-none" THEN TRUE
  ELSE IF dCOOP = "unsafe-none" \/ rCOOP = "unsafe-none" THEN FALSE
  ELSE IF dCOOP = rCOOP /\ SameOrigin(dOrigin, rOrigin) THEN TRUE
  ELSE FALSE
\* A popup's initial about:blank carries the opener's COOP and origin.
PopupSevered(openerCOOP, openerOrigin, popupCOOP, popupOrigin) ==
  ~MatchCOOP(openerCOOP, openerOrigin, popupCOOP, popupOrigin)

\* --- Fetch: cross-origin resource policy check ----------------------------
CorpInternal(o, coep, r, forNav) ==
  IF forNav /\ coep = "unsafe-none" THEN "allowed"
  ELSE
    LET p0 == r.corp
        p  == IF p0 # "none" THEN p0
              ELSE CASE coep = "unsafe-none"    -> "none"
                     [] coep = "credentialless" ->
                          IF r.creds \/ forNav THEN "same-origin" ELSE "none"
                     [] coep = "require-corp"   ->
                          IF Mutant = "coep-default" THEN "none" ELSE "same-origin"
    IN CASE p \in {"none", "cross-origin"} -> "allowed"
         [] p = "same-origin" -> IF SameOrigin(o, r.origin) THEN "allowed" ELSE "blocked"
         [] p = "same-site"   ->
              IF SameSite(o, r.origin)
                 /\ (Mutant = "samesite-scheme" \/ Secure(o) \/ ~Secure(r.origin))
              THEN "allowed" ELSE "blocked"

CorpCheck(o, coep, r, forNav) ==
  IF CorpInternal(o, "unsafe-none", r, forNav) = "blocked" THEN "blocked"
  ELSE CorpInternal(o, coep, r, forNav)

\* Result of fetch(url, {mode}) seen by script in a document of origin o.
FetchResult(o, coep, mode, r) ==
  IF mode = "cors" THEN "cors"                       \* CORS outcome not modelled
  ELSE IF SameOrigin(o, r.origin) THEN "basic"
  ELSE IF CorpCheck(o, coep, r, FALSE) = "blocked" THEN "error" ELSE "opaque"

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

\* Noninterference: what a page observes about a cross-origin no-cors fetch
\* does not depend on the target's response headers.
NoHeaderLeak ==
  \A o \in Origins, coep \in COEPs, r1, r2 \in Responses :
    (r1.origin = r2.origin /\ r1.creds = r2.creds /\ ~SameOrigin(o, r1.origin)) =>
      FetchResult(o, coep, "no-cors", r1) = FetchResult(o, coep, "no-cors", r2)

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
