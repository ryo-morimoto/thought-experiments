---- MODULE DIPExtension ----
\* Document-Isolation-Policy (WICG editor's draft, fetched 2026-11-21) brought
\* into the closure of SpecIsolation (experiments/2026-11-21-informal-extension.md).
\* DIP is a monkey patch over HTML and Fetch. The parts modelled here:
\*  - obtain a document isolation policy: a non-secure context keeps "none";
\*  - the document's agent cluster cross-origin isolation key (from its DIP)
\*    overrides the browsing context group's key (from COOP + COEP);
\*  - Fetch: "Document-Isolation-Policy allows credentials" is false for a
\*    cross-origin no-cors request from an isolate-and-credentialless client;
\*  - Fetch: the CORP check also upgrades to same-origin due to DIP
\*    (isolate-and-require-corp always; isolate-and-credentialless when the
\*    response's request-includes-credentials is true).
\* Simplifications: the DIP upgrade is modelled as a second CORP check with
\* the DIP value read as a COEP value (forNavigation false), combined by
\* "blocked if either blocks"; reports are not modelled.
EXTENDS SpecIsolation

DIPs == {"none", "isolate-and-require-corp", "isolate-and-credentialless"}

EffectiveDIP(o, dip) == IF ~Secure(o) THEN "none" ELSE dip
DIPAsCOEP(d) ==
  CASE d = "none" -> "unsafe-none"
    [] d = "isolate-and-require-corp" -> "require-corp"
    [] d = "isolate-and-credentialless" -> "credentialless"

\* The document key overrides the group key.
COIModeD(coop, coep, o, dip) ==
  IF EffectiveDIP(o, dip) # "none" THEN COIChoice ELSE COIMode(coop, coep, o)
CrossOriginIsolatedD(coop, coep, o, dip) == COIModeD(coop, coep, o, dip) = "concrete"

\* Credentials actually sent, as seen in the response.
ReqD(o, coep, dip, mode, r) ==
  LET rr == DocCreds(o, EffectiveCOEP(o, coep), mode, r) IN
  IF mode = "no-cors" /\ EffectiveDIP(o, dip) = "isolate-and-credentialless"
     /\ ~SameOrigin(o, r.origin)
  THEN [rr EXCEPT !.creds = FALSE] ELSE rr

CorpBlockedD(o, coep, dip, rr) ==
  \/ CorpCheck(o, EffectiveCOEP(o, coep), rr, FALSE) = "blocked"
  \/ CorpInternal(o, DIPAsCOEP(EffectiveDIP(o, dip)), rr, FALSE) = "blocked"

FetchResultD(o, coep, dip, mode, r) ==
  IF SameOrigin(o, r.origin) THEN "basic"
  ELSE IF mode = "cors" THEN "cors"
  ELSE IF CorpBlockedD(o, coep, dip, ReqD(o, coep, dip, mode, r)) THEN "error"
  ELSE "opaque"

\* (1) DIP "none" leaves the model unchanged (conservative extension).
Conservative ==
  \A o \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"}, r \in Responses, coop \in COOPs :
    /\ FetchResultD(o, coep, "none", mode, r) = FetchResult(o, coep, mode, r)
    /\ CrossOriginIsolatedD(coop, coep, o, "none") = CrossOriginIsolated(coop, coep, o)

\* (2) The access-control property of the closed model, with any DIP.
OptInOnlySecureD ==
  \A o \in Origins, r \in Responses, dip \in DIPs :
    (Secure(o) /\ FetchResultD(o, "require-corp", dip, "no-cors", r) = "opaque") =>
      \/ r.corp = "cross-origin"
      \/ r.corp = "same-site" /\ SameSite(o, r.origin)

\* (3) What the closed model implies: crossOriginIsolated needs COOP
\* same-origin and a compatible COEP.
COIOnlyByCOOPCOEP ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, dip \in DIPs :
    CrossOriginIsolatedD(coop, coep, o, dip) =>
      coop = "same-origin" /\ coep \in {"require-corp", "credentialless"}

\* (4) The reason for the capability: in a cross-origin isolated document,
\* cross-origin no-cors bytes arrive only with a CORP opt-in or without
\* credentials.
COIOnlyWithOptIn ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, dip \in DIPs, r \in Responses :
    LET rr == ReqD(o, coep, dip, "no-cors", r) IN
    (CrossOriginIsolatedD(coop, coep, o, dip)
     /\ FetchResultD(o, coep, dip, "no-cors", r) = "opaque") =>
      \/ ~rr.creds
      \/ r.corp = "cross-origin"
      \/ r.corp = "same-site" /\ SameSite(o, r.origin)

\* (5) Flow property with DIP: what the page observes depends only on what
\* the target declared.
ObserveD(o, coep, dip, mode, r) ==
  IF SameOrigin(o, r.origin) THEN <<"read", r.body>>
  ELSE IF mode = "cors" THEN (IF r.acao THEN <<"read", r.body>> ELSE <<"error">>)
  ELSE IF CorpBlockedD(o, coep, dip, ReqD(o, coep, dip, mode, Base(r))) THEN <<"error">>
  ELSE <<"opaque">>
NoUndeclaredLeakD ==
  \A o \in Origins, coep \in COEPs, dip \in DIPs, mode \in {"cors", "no-cors"},
     r1, r2 \in FlowResponses :
    (/\ r1.origin = r2.origin
     /\ ~SameOrigin(o, r1.origin)
     /\ Declared(mode, r1) = Declared(mode, r2))
    => ObserveD(o, coep, dip, mode, r1) = ObserveD(o, coep, dip, mode, r2)

COIWitness ==
  CHOOSE x \in Origins \X COOPs \X COEPs \X DIPs :
    CrossOriginIsolatedD(x[2], x[3], x[1], x[4])
    /\ ~(x[2] = "same-origin" /\ x[3] \in {"require-corp", "credentialless"})

PrintDIP == PrintT(<<"dip",
                     <<"conservative", Conservative>>,
                     <<"optin-only-secure", OptInOnlySecureD>>,
                     <<"coi-only-by-coop-coep", COIOnlyByCOOPCOEP>>,
                     <<"coi-only-with-optin", COIOnlyWithOptIn>>,
                     <<"no-undeclared-leak", NoUndeclaredLeakD>>,
                     <<"coi-witness", COIWitness>>>>)
====
