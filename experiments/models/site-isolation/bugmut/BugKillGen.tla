------------------------------ MODULE BugKillGen ------------------------------
(* bugmut/RESULTS.md: kills of BugMutants!All on the gen/ rows, with the     *)
(* rule of ../gen/GenAllowed.tla. GenRows.tla: ../gen/driver/mkallowed.py.  *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, GenRows
CONSTANTS COIChoices, WithPP, CfgName
VARIABLE dummy
G(m) == INSTANCE GenModel WITH Mutant <- m
BM == INSTANCE BugMutants
Ms == BM!All
N == Len(Rows)
A(m, r) == G(m)!Allowed(Scen[Rows[r].s], Rows[r].i, Rows[r].k, COIChoices, WithPP)
Base == [r \in 1..N |-> A("none", r)]
ObsIdx(b) == {r \in 1..N : Rows[r][b] # {}}
Inside(b) == {r \in ObsIdx(b) : Rows[r][b] \subseteq Base[r]}
PrintK == \A m \in Ms :
  LET MT == [r \in 1..N |-> A(m, r)] IN
  \A b \in Browsers :
    PrintT(<<"k", "gen", CfgName, b, m,
             Cardinality({r \in Inside(b) : ~(Rows[r][b] \subseteq MT[r])}), MT = Base>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
