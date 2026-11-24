------------------------------ MODULE BugKillGen2 -----------------------------
(* bugmut/RESULTS.md: kills of BugMutants!All on the gen2/ rows, with the    *)
(* rule of ../gen2/Gen2Allowed.tla. Gen2Rows.tla: ../gen2/driver/mkrows.py. *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, Gen2Space, Gen2Rows
CONSTANTS COIChoices, OACParam, CfgName
VARIABLE dummy
G(m) == INSTANCE Gen2Model WITH Mutant <- m
BM == INSTANCE BugMutants
Ms == BM!All
N == Len(Rows)
A(m, r) == G(m)!Allowed(Scen[Rows[r].s], Rows[r].k, COIChoices)
Base == [r \in 1..N |-> A("none", r)]
ObsIdx(b) == {r \in 1..N : Rows[r][b] # {}}
Inside(b) == {r \in ObsIdx(b) : Rows[r][b] \subseteq Base[r]}
PrintK == \A m \in Ms :
  LET MT == [r \in 1..N |-> A(m, r)] IN
  \A b \in Browsers :
    PrintT(<<"k", "gen2", CfgName, b, m,
             Cardinality({r \in Inside(b) : ~(Rows[r][b] \subseteq MT[r])}), MT = Base>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
