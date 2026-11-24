----------------------------- MODULE HoldPrevRedir ----------------------------
(* holdout/RESULTS.md: K_prev on the committed redirect/ rows (see HoldPrev). *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, RedirectSpace, RedirectRows, HoldMutants
CONSTANTS COIChoices, CfgName
N == Len(Rows)
A(m, r) == R(m)!Allowed(R(m)!Decode(Space[Rows[r].x]), Rows[r].k, COIChoices)
Base == [r \in 1..N |-> A("none", r)]
Inside(b) == {r \in 1..N : Rows[r][b] # {} /\ Rows[r][b] \subseteq Base[r]}
Killed(b, Ms) == {m \in Ms : \E r \in Inside(b) : ~(Rows[r][b] \subseteq A(m, r))}
PrintPrev == \A b \in Browsers : PrintT(<<"prevkill", "redirect", CfgName, b, Killed(b, RMs)>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
