----------------------------- MODULE PremisesFix ------------------------------
(* premises/RESULTS.md, for experiments/2026-11-24-property-premises.md     *)
(* (tree node A1). Restates the properties whose premise or conclusion     *)
(* concepts are narrower or broader than the spec definitions (HTML        *)
(* 0e292f4, Fetch d7fc0fd), and checks the restatements. SpecIsolation and *)
(* gen2 are reused unedited.                                                *)
EXTENDS SpecIsolation, Gen2Space, FiniteSets
G2 == INSTANCE Gen2Model WITH Mutant <- "none", OACParam <- "spec"

\* --- M1/M2: the "opt-in" in the conclusions ------------------------------
\* Fetch "cross-origin resource policy internal check", explicit header:
\* cross-origin allows; same-site allows only if schemelessly same site AND
\* (origin's scheme is https OR the response URL's scheme is not https).
CorpPermits(o, r) ==
  \/ r.corp = "cross-origin"
  \/ r.corp = "same-site" /\ SameSite(o, r.origin) /\ (Secure(o) \/ ~Secure(r.origin))
\* HTML "same site" (concept-site-same-site on obtained sites): scheme equal.
HTMLSameSite(x, y) == x.site = y.site /\ x.scheme = y.scheme
HasOptInHTML(o, r) ==
  \/ r.corp = "cross-origin"
  \/ r.corp = "same-site" /\ HTMLSameSite(o, r.origin)

OptInOnlySecureCtxStrict ==
  \A ctx \in Contexts, r \in Responses :
    (SecureCtx(ctx) /\ FetchResultCtx(ctx, "require-corp", "no-cors", r) = "opaque") =>
      CorpPermits(ctx.self, r)
OptInOnlyPCStrict ==
  \A ctx \in Contexts, r \in Responses :
    FetchResultPC(ctx, "require-corp", "no-cors", r) = "opaque" => CorpPermits(ctx.self, r)
OptInOnlySecureCtxHTML ==
  \A ctx \in Contexts, r \in Responses :
    (SecureCtx(ctx) /\ FetchResultCtx(ctx, "require-corp", "no-cors", r) = "opaque") =>
      HasOptInHTML(ctx.self, r)
OptInOnlyPCHTML ==
  \A ctx \in Contexts, r \in Responses :
    FetchResultPC(ctx, "require-corp", "no-cors", r) = "opaque" => HasOptInHTML(ctx.self, r)
PCHTMLWitness ==
  CHOOSE x \in Contexts \X Responses :
    FetchResultPC(x[1], "require-corp", "no-cors", x[2]) = "opaque" /\ ~HasOptInHTML(x[1].self, x[2])
COIOnlyWithOptInTopStrict ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, s \in Responses :
    LET ss == DocCreds(o, EffectiveCOEP(o, coep), "no-cors", s) IN
    (CrossOriginIsolated(coop, coep, o) /\ FetchResult(o, coep, "no-cors", s) = "opaque")
      => (~ss.creds \/ CorpPermits(o, s))

\* --- M3: COIOnlyWithOptInNested's premise as the child's capability -----
\* HTML: capability = agent cluster mode "concrete" AND allowed to use
\* "cross-origin-isolated" (default allowlist 'self'; no allow attribute:
\* the child must be same origin with its parent).
COIOnlyWithOptInNestedStrict ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, r \in Responses,
     ccoep \in COEPs, s \in Responses :
    LET pctx == TopCtx(o)
        cctx == ChildCtx(pctx, r)
        cec  == EffectiveCOEPCtx(cctx, ccoep)
        ss   == DocCreds(cctx.self, cec, "no-cors", s)
        cap  == CrossOriginIsolated(coop, coep, o) /\ SameOrigin(r.origin, o)
    IN (cap /\ NavChild(pctx, EffectiveCOEP(o, coep), r, ccoep) = "loaded")
       => /\ (SameOrigin(o, r.origin) \/ CorpPermits(o, r))
          /\ (FetchResultCtx(cctx, ccoep, "no-cors", s) = "opaque" => (~ss.creds \/ CorpPermits(cctx.self, s)))
\* The original premise (group mode) with the strict conclusion.
COIOnlyWithOptInNestedGroupStrict ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, r \in Responses,
     ccoep \in COEPs, s \in Responses :
    LET pctx == TopCtx(o)
        cctx == ChildCtx(pctx, r)
        cec  == EffectiveCOEPCtx(cctx, ccoep)
        ss   == DocCreds(cctx.self, cec, "no-cors", s)
    IN (CrossOriginIsolated(coop, coep, o) /\ NavChild(pctx, EffectiveCOEP(o, coep), r, ccoep) = "loaded")
       => /\ (SameOrigin(o, r.origin) \/ CorpPermits(o, r))
          /\ (FetchResultCtx(cctx, ccoep, "no-cors", s) = "opaque" => (~ss.creds \/ CorpPermits(cctx.self, s)))

\* --- M4: agent cluster key ------------------------------------------------
\* HTML: a key is a site (scheme, registrable domain) or a tuple origin.
\* SpecIsolation's Key drops the scheme and lets an origin key equal a site key.
KeyHTML(o, kind) == IF kind = "origin" THEN <<"origin", o.scheme, o.host>>
                    ELSE <<"site", o.scheme, o.site>>
Kinds2 == {"origin", "site"}
\* Collisions of Key that KeyHTML separates, over all origins of SpecIsolation.
KeyCollisions ==
  {<<x, k1, y, k2>> \in AllOrigins \X Kinds2 \X AllOrigins \X Kinds2 :
     Key(x, k1) = Key(y, k2) /\ KeyHTML(x, k1) # KeyHTML(y, k2)}
\* gen2 O family: document.domain access with KeyHTML.
ODDHTML(sc) == LET k == G2!OK(sc) IN
  ~DocumentDomainNoOp(k[1]) /\ ~DocumentDomainNoOp(k[2])
  /\ KeyHTML(sc.o0, k[1]) = KeyHTML(sc.o1, k[2])
OScen == {i \in 1..Len(Scen) : Scen[i].fam = "O"}
ODDAgrees == \A i \in OScen : G2!ODD(Scen[i]) = ODDHTML(Scen[i])
\* WPT case oac-separate with KeyHTML.
OACSeparateHTML ==
  KeyHTML(OA, KeyKind(OA, "none", "absent", FALSE)) # KeyHTML(OAwww, KeyKind(OAwww, "none", "absent", TRUE))

PrintPremises == PrintT(<<"premises", Mutant,
  <<"optin-ctx-strict", OptInOnlySecureCtxStrict>>,
  <<"optin-pc-strict", OptInOnlyPCStrict>>,
  <<"optin-ctx-html-samesite", OptInOnlySecureCtxHTML>>,
  <<"optin-pc-html-samesite", OptInOnlyPCHTML,
    IF OptInOnlyPCHTML THEN "-" ELSE PCHTMLWitness>>,
  <<"coi-top-strict", COIOnlyWithOptInTopStrict>>,
  <<"coi-nested-cap-strict", COIOnlyWithOptInNestedStrict>>,
  <<"coi-nested-group-strict", COIOnlyWithOptInNestedGroupStrict>>,
  <<"key-collisions", Cardinality(KeyCollisions)>>,
  <<"o-scenarios", Cardinality(OScen), "odd-agrees", ODDAgrees>>,
  <<"oac-separate-html", OACSeparateHTML>>,
  \* the original statements, for comparison under a Mutant
  <<"orig-optin-ctx", OptInOnlySecureCtx>>, <<"orig-optin-pc", OptInOnlyPC>>,
  <<"orig-coi-top", COIOnlyWithOptInTop>>, <<"orig-coi-nested", COIOnlyWithOptInNested>>>>)
===============================================================================
