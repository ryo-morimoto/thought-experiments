------------------------------ MODULE PremisesPT ------------------------------
(* premises/round2/RESULTS.md. The narrower domain concepts, with the      *)
(* missing cases added: localhost (potentially trustworthy over http),     *)
(* a ported origin, and an opaque requester (sandboxed document).          *)
(* SpecIsolationPT is SpecIsolation with Secure = potentially trustworthy, *)
(* the CORP scheme test on the literal scheme, and two localhost origins.  *)
EXTENDS SpecIsolationPT, FiniteSets

\* Fetch internal check, explicit header (fetch.bs:4459): literal schemes.
CorpPermitsLit(o, r) ==
  \/ r.corp = "cross-origin"
  \/ r.corp = "same-site" /\ SameSite(o, r.origin) /\ (SchemeHttps(o) \/ ~SchemeHttps(r.origin))
\* Round 1's CorpPermits, which wrote the scheme test with Secure.
CorpPermitsR1(o, r) ==
  \/ r.corp = "cross-origin"
  \/ r.corp = "same-site" /\ SameSite(o, r.origin) /\ (Secure(o) \/ ~Secure(r.origin))

OAport == [scheme |-> "https", host |-> "a.test:8443", site |-> "a.test"]
Opaque == [scheme |-> "opaque", host |-> "opaque", site |-> "opaque"]
ExtO   == Origins \cup {OAport, OAwww2, OAwwwhttp, OBhttp}
ExtContexts  == [self : ExtO \cup {Opaque}, top : ExtO \cup {Opaque}]
ExtResponses == [origin : ExtO, corp : CORPs, creds : BOOLEAN]

\* (2) asymmetry, and CorpPermitsLit = the internal check for explicit headers.
Rsp2(o, c) == [origin |-> o, corp |-> c, creds |-> FALSE]
Asym == CorpPermitsLit(OA, Rsp2(OAhttp, "same-site")) /\ ~CorpPermitsLit(OAhttp, Rsp2(OA, "same-site"))
LitEqualsCheck ==
  \A o \in ExtO \cup {Opaque}, coep \in COEPs, r \in ExtResponses :
    r.corp # "none" =>
      ((CorpInternal(o, coep, r, FALSE) = "allowed")
       <=> ((r.corp = "same-origin" /\ SameOrigin(o, r.origin)) \/ CorpPermitsLit(o, r)))
R1DiffersOnLocalhost == CorpPermitsR1(OLocal, Rsp2(OLocalS, "same-site"))
                        /\ ~CorpPermitsLit(OLocal, Rsp2(OLocalS, "same-site"))

\* (1) the properties over the extended domains.
OptInCtxExt ==
  \A ctx \in ExtContexts, r \in ExtResponses :
    (SecureCtx(ctx) /\ FetchResultCtx(ctx, "require-corp", "no-cors", r) = "opaque") =>
      CorpPermitsLit(ctx.self, r)
OptInPCExt ==
  \A ctx \in ExtContexts, r \in ExtResponses :
    FetchResultPC(ctx, "require-corp", "no-cors", r) = "opaque" => CorpPermitsLit(ctx.self, r)
COITopExt ==
  \A o \in ExtO, coop \in COOPs, coep \in COEPs, s \in ExtResponses :
    LET ss == DocCreds(o, EffectiveCOEP(o, coep), "no-cors", s) IN
    (CrossOriginIsolated(coop, coep, o) /\ FetchResult(o, coep, "no-cors", s) = "opaque")
      => (~ss.creds \/ CorpPermitsLit(o, s))
COINestedExt ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, r \in Responses,
     ccoep \in COEPs, s \in Responses :
    LET pctx == TopCtx(o)
        cctx == ChildCtx(pctx, r)
        ss   == DocCreds(cctx.self, EffectiveCOEPCtx(cctx, ccoep), "no-cors", s)
    IN (CrossOriginIsolated(coop, coep, o) /\ NavChild(pctx, EffectiveCOEP(o, coep), r, ccoep) = "loaded")
       => /\ (SameOrigin(o, r.origin) \/ CorpPermitsLit(o, r))
          /\ (FetchResultCtx(cctx, ccoep, "no-cors", s) = "opaque" => (~ss.creds \/ CorpPermitsLit(cctx.self, s)))
\* Non-vacuity: how many cases satisfy each premise (localhost included).
NCtx == Cardinality({x \in ExtContexts \X ExtResponses :
          SecureCtx(x[1]) /\ FetchResultCtx(x[1], "require-corp", "no-cors", x[2]) = "opaque"})
NLocal == Cardinality({x \in ExtContexts \X ExtResponses :
          x[1].top \in {OLocal} /\ SecureCtx(x[1])
          /\ FetchResultCtx(x[1], "require-corp", "no-cors", x[2]) = "opaque"})
\* The old origin-scheme premise would miss localhost: secure context, not https.
LocalSecureNotHttps == SecureCtx(TopCtx(OLocal)) /\ ~SchemeHttps(OLocal)
\* Ported origin behaves as a same-site cross-origin host (isomorphism check).
PortLikeWww ==
  \A o \in {OA, OAhttp, OB}, coep \in COEPs, c \in CORPs, cr \in BOOLEAN, m \in {"cors", "no-cors"} :
    FetchResult(o, coep, m, [origin |-> OAport, corp |-> c, creds |-> cr])
    = FetchResult(o, coep, m, [origin |-> OAwww, corp |-> c, creds |-> cr])

PrintPT == PrintT(<<"pt",
  <<"asym", Asym>>, <<"lit-equals-check", LitEqualsCheck>>,
  <<"r1-corppermits-wrong-on-localhost", R1DiffersOnLocalhost>>,
  <<"optin-ctx-ext", OptInCtxExt>>, <<"optin-pc-ext", OptInPCExt>>,
  <<"coi-top-ext", COITopExt>>, <<"coi-nested-ext", COINestedExt>>,
  <<"orig-optin-ctx", OptInOnlySecureCtx>>, <<"orig-coi-nested", COIOnlyWithOptInNested>>,
  <<"n-premise-ctx", NCtx>>, <<"n-premise-localhost-top", NLocal>>,
  <<"localhost-secure-not-https", LocalSecureNotHttps>>,
  <<"port-like-www", PortLikeWww>>>>)
===============================================================================
