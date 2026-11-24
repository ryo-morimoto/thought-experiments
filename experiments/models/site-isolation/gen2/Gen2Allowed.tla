------------------------------ MODULE Gen2Allowed -----------------------------
(* gen2/RESULTS.md: inclusion and mutant kills for the gen2 rows, as         *)
(* gen/GenAllowed.tla does. Gen2Rows.tla is written by driver/mkrows.py. A   *)
(* mutant m is killed by browser b when some row's observation is inside the *)
(* unmutated model's set and outside m's. driver/analyze.py reads the lines. *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, Gen2Space, Gen2Rows
CONSTANTS COIChoices, OACParam, CfgName
VARIABLE dummy
G(m) == INSTANCE Gen2Model WITH Mutant <- m
Ms == G("none")!SI!MechMutants \cup G("none")!SI!Mutants \cup G("none")!SI!FixMutants
      \cup G("none")!G2Mutants
N == Len(Rows)
A(m, r) == G(m)!Allowed(Scen[Rows[r].s], Rows[r].k, COIChoices)
Base == [r \in 1..N |-> A("none", r)]
MT   == [m \in Ms |-> [r \in 1..N |-> A(m, r)]]
ObsIdx(b) == {r \in 1..N : Rows[r][b] # {}}
Out(b)    == {r \in ObsIdx(b) : ~(Rows[r][b] \subseteq Base[r])}
Inside(b) == ObsIdx(b) \ Out(b)
KillRows(m, b) == {r \in Inside(b) : ~(Rows[r][b] \subseteq MT[m][r])}
Equivalent == {m \in Ms : MT[m] = Base}
Ids(S) == {Rows[r].id : r \in S}
PrintGen ==
  /\ PrintT(<<"cfg", CfgName, "rows", N, "mutants", Cardinality(Ms)>>)
  /\ PrintT(<<"equivalent", CfgName, Equivalent>>)
  /\ \A b \in Browsers :
       /\ PrintT(<<"counts", CfgName, b, Cardinality(ObsIdx(b)), Cardinality(Inside(b)), Cardinality(Out(b))>>)
       /\ \A r \in Out(b) : PrintT(<<"out", CfgName, b, Rows[r].id, Rows[r][b], Base[r]>>)
       /\ \A m \in Ms : PrintT(<<"kill", CfgName, b, m, Ids(KillRows(m, b))>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
