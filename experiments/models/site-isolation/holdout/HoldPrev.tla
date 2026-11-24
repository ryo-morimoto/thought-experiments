------------------------------- MODULE HoldPrev -------------------------------
(* holdout/RESULTS.md: the previous union K_prev of the registration. Kill   *)
(* sets of the registered mutant sets (HoldMutants) on the committed rows of *)
(* gen/ (GenRows from gen/driver/mkallowed.py, GenModel, WithPP as given),   *)
(* with the kill rule of gen/GenAllowed.tla. HoldPrevGen2 and HoldPrevRedir  *)
(* do the same for gen2/ and redirect/.                                     *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, GenRows, HoldMutants
CONSTANTS COIChoices, WithPP, CfgName
N == Len(Rows)
A(m, r) == G(m)!Allowed(Scen[Rows[r].s], Rows[r].i, Rows[r].k, COIChoices, WithPP)
Base == [r \in 1..N |-> A("none", r)]
Inside(b) == {r \in 1..N : Rows[r][b] # {} /\ Rows[r][b] \subseteq Base[r]}
Killed(b, Ms) == {m \in Ms : \E r \in Inside(b) : ~(Rows[r][b] \subseteq A(m, r))}
PrintPrev == \A b \in Browsers : PrintT(<<"prevkill", "gen", CfgName, b, Killed(b, NMs)>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
