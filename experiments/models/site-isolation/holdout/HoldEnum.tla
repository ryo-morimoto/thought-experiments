------------------------------- MODULE HoldEnum -------------------------------
(* holdout/RESULTS.md: pre-screen of both families on the frozen models,     *)
(* without browsers (as redirect/RedirectEnum.tla). For each scenario index  *)
(* i in Lo..Hi of family Fam, the set of mutants whose vector of allowed     *)
(* sets differs from the unmutated one under COIChoice {concrete, logical}   *)
(* (DL) and {concrete} (DC). Scenarios with the same pair form a class;      *)
(* gen_holdout.py select merges the chunks and picks scenarios per class.    *)
(* Family N uses GenModel with WithPP = TRUE.                                *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, HoldDecode, HoldMutants
CONSTANTS Fam, Lo, Hi
CL == {"concrete", "logical"}
CC == {"concrete"}
Rng == Lo..Hi
VN(m, i, cc) == G(m)!Vec(NSc(NestSpace[i]), cc, TRUE)
VR(m, i, cc) == R(m)!Vec(RSc(RedirSpace[i]), cc)
V(m, i, cc) == IF Fam = "N" THEN VN(m, i, cc) ELSE VR(m, i, cc)
Ms == IF Fam = "N" THEN NMs ELSE RMs
BaseL == [i \in Rng |-> V("none", i, CL)]
BaseC == [i \in Rng |-> V("none", i, CC)]
DL == [i \in Rng |-> {m \in Ms : V(m, i, CL) # BaseL[i]}]
DC == [i \in Rng |-> {m \in Ms : V(m, i, CC) # BaseC[i]}]
Classes == {<<DL[i], DC[i]>> : i \in Rng}
Members(cl) == {i \in Rng : <<DL[i], DC[i]>> = cl}
PrintEnum ==
  /\ PrintT(<<"enum", Fam, Lo, Hi, "mutants", Cardinality(Ms), "nclasses", Cardinality(Classes)>>)
  /\ \A cl \in Classes : PrintT(<<"class", Fam, Lo, cl[1], cl[2], Members(cl)>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
