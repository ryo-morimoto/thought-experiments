---------------------------- MODULE BugKillRedirect ---------------------------
(* bugmut/RESULTS.md: kills of BugMutants!All on the redirect/ rows, with    *)
(* the rule of ../redirect/RedirectAllowed.tla. RedirectSpace.tla:          *)
(* ../redirect/gen.py space; RedirectRows.tla: ../redirect/driver/mkrows.py. *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, RedirectSpace, RedirectRows
CONSTANTS COIChoices, CfgName
VARIABLE dummy
R(m) == INSTANCE RedirectSeq WITH Mutant <- m
BM == INSTANCE BugMutants
Ms == BM!All
N == Len(Rows)
A(m, r) == R(m)!Allowed(R(m)!Decode(Space[Rows[r].x]), Rows[r].k, COIChoices)
Base == [r \in 1..N |-> A("none", r)]
ObsIdx(b) == {r \in 1..N : Rows[r][b] # {}}
Inside(b) == {r \in ObsIdx(b) : Rows[r][b] \subseteq Base[r]}
PrintK == \A m \in Ms :
  LET MT == [r \in 1..N |-> A(m, r)] IN
  \A b \in Browsers :
    PrintT(<<"k", "redirect", CfgName, b, m,
             Cardinality({r \in Inside(b) : ~(Rows[r][b] \subseteq MT[r])}), MT = Base>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
