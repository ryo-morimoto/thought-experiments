------------------------------ MODULE HoldAllowed -----------------------------
(* holdout/RESULTS.md: inclusion and mutant kills of the observed rows, as   *)
(* gen/GenAllowed.tla and redirect/RedirectAllowed.tla. HoldRows.tla is      *)
(* written by driver/mkrows.py. A row is inside when its observed set (union *)
(* over repeats) is a subset of the unmutated model's allowed set. A mutant  *)
(* m is killed by browser b when some inside row's observed set is not a     *)
(* subset of m's allowed set.                                                *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, HoldDecode, HoldMutants, HoldRows
CONSTANTS Fam, COIChoices, WithPP, CfgName
Ms == IF Fam = "N" THEN NMs ELSE RMs
Rows == IF Fam = "N" THEN NRows ELSE RRows
N == Len(Rows)
A(m, r) == IF Fam = "N"
           THEN G(m)!Allowed(NSc(NestSpace[Rows[r].x]), Rows[r].i, Rows[r].k, COIChoices, WithPP)
           ELSE R(m)!Allowed(RSc(RedirSpace[Rows[r].x]), Rows[r].k, COIChoices)
Base == [r \in 1..N |-> A("none", r)]
MT   == [m \in Ms |-> [r \in 1..N |-> A(m, r)]]
ObsIdx(b) == {r \in 1..N : Rows[r][b] # {}}
Out(b)    == {r \in ObsIdx(b) : ~(Rows[r][b] \subseteq Base[r])}
Inside(b) == ObsIdx(b) \ Out(b)
KillRows(m, b) == {r \in Inside(b) : ~(Rows[r][b] \subseteq MT[m][r])}
Equivalent == {m \in Ms : MT[m] = Base}
PrintAllowed ==
  /\ PrintT(<<"cfg", CfgName, Fam, "rows", N, "mutants", Cardinality(Ms)>>)
  /\ PrintT(<<"equivalent", CfgName, Equivalent>>)
  /\ \A b \in Browsers :
       /\ PrintT(<<"counts", CfgName, b, Cardinality(ObsIdx(b)), Cardinality(Inside(b)), Cardinality(Out(b))>>)
       /\ \A r \in Out(b) : PrintT(<<"out", CfgName, b, Rows[r].id, Rows[r][b], Base[r]>>)
       /\ \A m \in Ms : PrintT(<<"kill", CfgName, b, m, Cardinality(KillRows(m, b))>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
