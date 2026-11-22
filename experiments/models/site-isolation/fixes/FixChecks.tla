------------------------------ MODULE FixChecks -------------------------------
(* fixes/FIXES.md: the properties and WPTBroad agreement of SpecIsolation    *)
(* for Mutant = "none" and for each "false:<id>" / "neg:<id>" of the steps   *)
(* added there (FixIds). Run from site-isolation/ with -DTLA-Library=/spec.  *)
EXTENDS Naturals, Sequences, FiniteSets, TLC
VARIABLE dummy
W(m) == INSTANCE WPTBroad WITH Mutant <- m, dummy <- dummy


\* w014 as the <img> it is (destination image); served: whether a TLS
\* server answers at the upgraded URL. In WPT it does not (wptserve's
\* port 8000 is plain HTTP), so served = FALSE is the WPT setting.
W014(m, served) ==
  LET v == W(m)!ImageResult(W("none")!OA, "unsafe-none",
                            [origin |-> W("none")!OAwwwhttp, corp |-> "same-site", creds |-> FALSE], served)
  IN IF v = "error" THEN "error" ELSE "opaque"
BroadFix(m, served) ==
  (W(m)!BroadMismatches \ {"w014"}) \cup (IF W014(m, served) # "opaque" THEN {"w014"} ELSE {})

Ms == <<"none">> \o
      <<"false:secure-ctx-top", "false:nav-corp-check", "false:nav-coep-adherence",
        "false:mc-ancestor", "false:mc-upgrade", "false:mc-block",
        "neg:secure-ctx-top", "neg:nav-corp-check", "neg:nav-coep-adherence",
        "neg:mc-ancestor", "neg:mc-upgrade", "neg:mc-block">>

Row(m) ==
  <<m,
    <<"broad-fetch-w014", W(m)!BroadMismatches>>,
    <<"broad-img-w014-wpt", BroadFix(m, FALSE)>>,
    <<"broad-img-w014-tls", BroadFix(m, TRUE)>>,
    <<"optin-only-secure", W(m)!OptInOnlySecure>>,
    <<"lifted", W(m)!OptInOnlySecureLifted>>,
    <<"secure-ctx", W(m)!OptInOnlySecureCtx>>,
    <<"pc", W(m)!OptInOnlyPC>>,
    <<"coi-top", W(m)!COIOnlyWithOptInTop>>,
    <<"coi-nested", W(m)!COIOnlyWithOptInNested>>>>
PrintRows == \A i \in 1..Len(Ms) : PrintT(<<"fixrow", Row(Ms[i])>>)
PrintWitnesses == PrintT(<<"fixwit",
  <<"lifted", W("none")!LiftedWitness>>,
  <<"nested-without-adherence", W("false:nav-coep-adherence")!NestedWitness>>>>)

\* Behaviour level for the <img> path: the omission changes some result.
DiffersImg(m) ==
  \E o \in W("none")!Origins, coep \in W("none")!COEPs, r \in W("none")!Responses,
     served \in BOOLEAN :
    W("none")!ImageResult(o, coep, r, served) # W(m)!ImageResult(o, coep, r, served)
PrintImg == PrintT(<<"fiximg", [i \in 2..7 |-> <<Ms[i], DiffersImg(Ms[i])>>]>>)

Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
