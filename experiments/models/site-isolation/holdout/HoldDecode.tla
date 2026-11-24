------------------------------ MODULE HoldDecode ------------------------------
(* holdout/RESULTS.md: scenario records for the frozen models, from the     *)
(* compact codes of HoldSpace.tla (written by gen_holdout.py space).        *)
(* NSc(x) is a ../gen/GenModel.tla scenario (depth 2); RSc(x) is a          *)
(* ../redirect/RedirectSeq.tla scenario. RSc is RedirectSeq!Decode with the  *)
(* relation-to-A origin (Org) replaced by an explicit origin; the codes and *)
(* the header mapping (OPq, HCOOP, HCOEP, STq, FCq, FEq) are RedirectSeq's.  *)
(* Neither model is edited. Origins are records as in SpecIsolation.        *)
EXTENDS Naturals, Sequences, HoldSpace

\* x = <<rep, top cfg, l1 cfg, l2 cfg, target kind>>
NSc(x) ==
  LET R == NestRep[x[1]] T == TopCfg[x[2]] C1 == ChildCfg[x[3]] C2 == ChildCfg[x[4]]
  IN [d |-> 2, coop |-> T.coop, o |-> R.o, e |-> <<T.e, C1.e, C2.e>>,
      corp |-> <<"none", C1.corp, C2.corp>>, tgt |-> R.tg[x[5]]]

OPq  == <<"unsafe-none", "same-origin-allow-popups", "same-origin", "so+rc">>
STq  == <<"blank", "doc">>
FCq  == <<"unsafe-none", "same-origin-allow-popups", "same-origin">>
FEq  == <<"unsafe-none", "require-corp">>
HCOOP(h) == IF h = "so+rc" THEN "same-origin" ELSE h
HCOEP(h) == IF h = "so+rc" THEN "require-corp" ELSE "unsafe-none"
\* x = <<op, st, rep, <<hop codes>>, final COOP, final COEP>>
RSc(x) ==
  LET R == RedirRep[x[3]] hs == x[4]
  IN [op |-> OPq[x[1]], st |-> STq[x[2]], nh |-> Len(hs),
      rs |-> [j \in 1..Len(hs) |-> [o |-> R.hops[j], coop |-> HCOOP(OPq[hs[j]]),
                                    coep |-> HCOEP(OPq[hs[j]]), redirect |-> TRUE]]
             \o <<[o |-> R.fin, coop |-> FCq[x[5]], coep |-> FEq[x[6]], redirect |-> FALSE]>>]
===============================================================================
