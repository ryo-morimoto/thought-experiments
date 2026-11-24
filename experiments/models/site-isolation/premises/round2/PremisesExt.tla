----------------------------- MODULE PremisesExt ------------------------------
(* premises/round2/RESULTS.md. The broader "opt-in" conclusion (round 1 M1)*)
(* in the modules round 1 did not re-check (DIP, Dominance, ORB, Hooks),   *)
(* restated with the Fetch condition; and the nested property at depth 2.  *)
(* All modules are reused unedited.                                         *)
EXTENDS SpecIsolation, FiniteSets
D  == INSTANCE DIPExtension WITH Mutant <- Mutant
DA == INSTANCE DominanceRetry WITH Mutant <- Mutant, Placement <- "after"
H  == INSTANCE ExtensionHooks WITH Mutant <- Mutant, HookReads <- "any"
O  == INSTANCE ORBExtension WITH Mutant <- Mutant

CorpPermits(o, r) ==
  \/ r.corp = "cross-origin"
  \/ r.corp = "same-site" /\ SameSite(o, r.origin) /\ (Secure(o) \/ ~Secure(r.origin))

OptInOnlySecureDStrict ==
  \A o \in Origins, r \in Responses, dip \in D!DIPs :
    (Secure(o) /\ D!FetchResultD(o, "require-corp", dip, "no-cors", r) = "opaque") => CorpPermits(o, r)
COIOnlyWithOptInDStrict ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, dip \in D!DIPs, r \in Responses :
    LET rr == D!ReqD(o, coep, dip, "no-cors", r) IN
    (D!CrossOriginIsolatedD(coop, coep, o, dip) /\ D!FetchResultD(o, coep, dip, "no-cors", r) = "opaque")
      => (~rr.creds \/ CorpPermits(o, r))
ACSubStrict ==
  \A o \in Origins, first, second \in Responses, retried, blk \in BOOLEAN :
    LET delivered == IF retried THEN second ELSE first IN
    (Secure(o) /\ first.origin = second.origin /\ DA!SubArrives(o, first, second, retried, blk))
      => CorpPermits(o, delivered)
ACNavStrict ==
  \A o \in Origins, r \in Responses, cc \in COEPs, blk \in BOOLEAN :
    (Secure(o) /\ DA!NavArrives(o, r, cc, blk)) => CorpPermits(o, r)
ACMonotoneStrict ==
  \A o \in Origins, r \in Responses, blk \in BOOLEAN :
    (Secure(o) /\ H!ResultM(o, r, blk) = "opaque") => CorpPermits(o, r)
OptInOnlySecureORBStrict ==
  \A o, ro \in Origins, ms \in O!MediaStates : \A r \in O!ORBResponsesAt(ro) :
    (Secure(o) /\ ~SameOrigin(o, ro)
     /\ O!ObserveORB(o, "require-corp", "no-cors", ms, r) = <<"opaque">>) => CorpPermits(o, r)

\* Depth 2: top (COI) -> child -> grandchild; the grandchild's no-cors bytes.
COINested2 ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, r1 \in Responses, c1 \in COEPs :
    LET p0 == TopCtx(o)  e0 == EffectiveCOEP(o, coep)
        x1 == ChildCtx(p0, r1)  e1 == EffectiveCOEPCtx(x1, c1) IN
    (CrossOriginIsolated(coop, coep, o) /\ NavChild(p0, e0, r1, c1) = "loaded") =>
    \A r2 \in Responses, c2 \in COEPs, s \in Responses :
      LET x2 == ChildCtx(x1, r2)  e2 == EffectiveCOEPCtx(x2, c2)
          ss == DocCreds(x2.self, e2, "no-cors", s) IN
      NavChild(x1, e1, r2, c2) = "loaded" =>
        /\ (SameOrigin(x1.self, r2.origin) \/ CorpPermits(x1.self, r2))
        /\ (FetchResultCtx(x2, c2, "no-cors", s) = "opaque" => (~ss.creds \/ CorpPermits(x2.self, s)))

PrintExt == PrintT(<<"ext", Mutant,
  <<"dip-optin-strict", OptInOnlySecureDStrict>>, <<"dip-coi-strict", COIOnlyWithOptInDStrict>>,
  <<"orig-dip-optin", D!OptInOnlySecureD>>, <<"orig-dip-coi", D!COIOnlyWithOptIn>>,
  <<"acsub-strict", ACSubStrict>>, <<"acnav-strict", ACNavStrict>>,
  <<"orig-acsub", DA!ACSub>>, <<"orig-acnav", DA!ACNav>>,
  <<"acmono-strict", ACMonotoneStrict>>, <<"orig-acmono", H!ACMonotone>>,
  <<"orb-optin-strict", OptInOnlySecureORBStrict>>, <<"orig-orb-optin", O!OptInOnlySecureORB>>,
  <<"coi-nested-depth2", COINested2>>>>)
===============================================================================
