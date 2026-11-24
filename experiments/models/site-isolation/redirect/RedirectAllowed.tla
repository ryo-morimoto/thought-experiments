----------------------------- MODULE RedirectAllowed ---------------------------
(* redirect/RESULTS.md: inclusion and mutant kills for the run scenarios, as   *)
(* gen/GenAllowed.tla. RedirectRows.tla is written by driver/mkrows.py. A     *)
(* mutant m is killed by browser b when some row's observation is inside the  *)
(* unmutated model's set and outside m's. WptRows: upstream WPT redirect      *)
(* tests (not among the 109 rows) with their expected values.               *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, RedirectSpace, RedirectRows
CONSTANTS COIChoices
VARIABLE dummy
R(m) == INSTANCE RedirectSeq WITH Mutant <- m
Ms == R("none")!AllMutants
N == Len(Rows)
A(m, r) == R(m)!Allowed(R(m)!Decode(Space[Rows[r].x]), Rows[r].k, COIChoices)
Base == [r \in 1..N |-> A("none", r)]
MT   == [m \in Ms |-> [r \in 1..N |-> A(m, r)]]
ObsIdx(b) == {r \in 1..N : Rows[r][b] # {}}
Out(b)    == {r \in ObsIdx(b) : ~(Rows[r][b] \subseteq Base[r])}
Inside(b) == ObsIdx(b) \ Out(b)
KillRows(m, b) == {r \in Inside(b) : ~(Rows[r][b] \subseteq MT[m][r])}
Killed(b)  == {m \in Ms : KillRows(m, b) # {}}
Equivalent == {m \in Ms : MT[m] = Base}
\* Upstream WPT: the expected value is inside the unmutated set (checked) and
\* kills m if outside m's set.
NW == Len(WptRows)
WA(m, w) == R(m)!Allowed(R(m)!Decode(WptRows[w].sc), WptRows[w].k, COIChoices)
WptOut == {WptRows[w].id : w \in {v \in 1..NW : WptRows[v].want \notin WA("none", v)}}
WptKilled == {m \in Ms : \E w \in 1..NW : WptRows[w].want \in WA("none", w) /\ WptRows[w].want \notin WA(m, w)}
Focus == R("none")!LocalMutants
PrintAllowed ==
  /\ PrintT(<<"cfg", COIChoices, "rows", N, "mutants", Cardinality(Ms)>>)
  /\ PrintT(<<"equivalent-on-rows", Equivalent>>)
  /\ \A b \in Browsers :
       /\ PrintT(<<"counts", b, "observed", Cardinality(ObsIdx(b)), "inside", Cardinality(Inside(b)),
                   "out", Cardinality(Out(b)), "killed", Cardinality(Killed(b)),
                   "survived-nonequivalent", (Ms \ Killed(b)) \ Equivalent>>)
       /\ PrintT(<<"killed", b, {<<m, Cardinality(KillRows(m, b))>> : m \in Killed(b)}>>)
       /\ PrintT(<<"focus-kill-rows", b, {<<m, {Rows[r].id : r \in KillRows(m, b)}>> : m \in Focus}>>)
       /\ PrintT(<<"out-of-model", b, {<<Rows[r].id, Rows[r][b], Base[r]>> : r \in Out(b)}>>)
       \* mutants whose sets contain every out-of-model row of b (and how many inside rows they lose)
       /\ PrintT(<<"rescuing-all", b, {<<m, Cardinality(KillRows(m, b))>> :
                    m \in {y \in Ms : Out(b) # {} /\ \A r \in Out(b) : Rows[r][b] \subseteq MT[y][r]}}>>)
  /\ PrintT(<<"wpt-out", WptOut>>)
  /\ PrintT(<<"wpt-killed", WptKilled>>)
  /\ PrintT(<<"wpt-killed-local", WptKilled \cap Focus>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
