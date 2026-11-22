------------------------------- MODULE HavocFix -------------------------------
(* fixes/FIXES.md: HavocFixCore for the fixed model (Mutant = "none") and   *)
(* for each "false:<id>" of the new steps (positive controls). Run from     *)
(* site-isolation/ with -DTLA-Library=/spec.                                 *)
EXTENDS Naturals, Sequences, FiniteSets, TLC
VARIABLE dummy
H(m) == INSTANCE HavocFixCore WITH Mutant <- m, dummy <- dummy

Ms == <<"none", "false:secure-ctx-top", "false:nav-corp-check", "false:nav-coep-adherence",
        "false:mc-ancestor", "false:mc-upgrade", "false:mc-block">>
Pts == H("none")!PointSeq

PrintConservative == PrintT(<<"hf-conservative", H("none")!Conservative>>)
PrintTable == \A i \in 1..Len(Ms) :
  PrintT(<<"hf", Ms[i], <<"base", H(Ms[i])!Props({})>>,
           [j \in 1..Len(Pts) |-> <<Pts[j], H(Ms[i])!Props({Pts[j]})>>]>>)

\* Behaviour level: the omission changes some fetch result, and havoc at
\* h-mc covers every result of the full model.
Differs(m) ==
  \E c \in H("none")!Contexts, coep \in H("none")!COEPs, r \in H("none")!Responses :
    H("none")!FR({}, H("none")!V0, c, coep, r) # H(m)!FR({}, H(m)!V0, c, coep, r)
Recovers(m, p) ==
  \A c \in H("none")!Contexts, coep \in H("none")!COEPs, r \in H("none")!Responses :
    H("none")!FR({}, H("none")!V0, c, coep, r) \in {H(m)!FR({p}, v, c, coep, r) : v \in H(m)!Vals({p})}
PrintControl == \A i \in 2..Len(Ms) :
  PrintT(<<"hf-control", Ms[i], <<"differs", Differs(Ms[i])>>,
           <<"recovers-h-mc", Recovers(Ms[i], "h-mc")>>,
           <<"recovers-h-secure", Recovers(Ms[i], "h-secure")>>>>)

Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
