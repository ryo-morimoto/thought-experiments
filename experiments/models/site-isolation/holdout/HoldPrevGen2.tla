----------------------------- MODULE HoldPrevGen2 -----------------------------
(* holdout/RESULTS.md: K_prev on the committed gen2/ rows (see HoldPrev).    *)
(* OACParam per browser as registered: Chrome "7617", Firefox "spec".        *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, Gen2Space, Gen2Rows, HoldMutants
CONSTANTS COIChoices, CfgName
G2(m, p) == INSTANCE Gen2Model WITH Mutant <- m, OACParam <- p
OAC(b) == IF b = "chrome" THEN "7617" ELSE "spec"
N == Len(Rows)
A(m, r, b) == G2(m, OAC(b))!Allowed(Scen[Rows[r].s], Rows[r].k, COIChoices)
Inside(b) == {r \in 1..N : Rows[r][b] # {} /\ Rows[r][b] \subseteq A("none", r, b)}
Killed(b, Ms) == {m \in Ms : \E r \in Inside(b) : ~(Rows[r][b] \subseteq A(m, r, b))}
PrintPrev == \A b \in Browsers : PrintT(<<"prevkill", "gen2", CfgName, b, Killed(b, NMs)>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
