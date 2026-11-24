----------------------------- MODULE HistoryAllowed ----------------------------
(* history/RESULTS.md: inclusion and mutant kills for the run scenarios, as    *)
(* redirect/RedirectAllowed.tla. HistoryRows.tla is written by                *)
(* driver/mkrows.py. Allowed values of a row are conditioned on the bfcache   *)
(* hits the same browser showed for that scenario (HistorySeq Allowed with H). *)
(* A mutant m is killed by browser b when some row's observation is inside   *)
(* the unmutated model's set and outside m's. WptRows: upstream WPT tests     *)
(* with their expected values (hits unknown: all feasible vectors).          *)
EXTENDS Integers, Sequences, FiniteSets, TLC, HistorySpace, HistoryRows
CONSTANTS COIChoices
VARIABLE dummy
R(m) == INSTANCE HistorySeq WITH Mutant <- m
Ms == R("none")!AllMutants
N == Len(Rows)
H(r, b) == Rows[r]["h" \o b]
A(m, r, b) == R(m)!Allowed(R(m)!Decode(Space[Rows[r].x]), Rows[r].k, COIChoices, H(r, b))
Base == [b \in Browsers |-> [r \in 1..N |-> A("none", r, b)]]
MT   == [m \in Ms |-> [b \in Browsers |-> [r \in 1..N |-> A(m, r, b)]]]
ObsIdx(b) == {r \in 1..N : Rows[r][b] # {}}
Out(b)    == {r \in ObsIdx(b) : ~(Rows[r][b] \subseteq Base[b][r])}
Inside(b) == ObsIdx(b) \ Out(b)
KillRows(m, b) == {r \in Inside(b) : ~(Rows[r][b] \subseteq MT[m][b][r])}
Killed(b)  == {m \in Ms : KillRows(m, b) # {}}
Equivalent == {m \in Ms : MT[m] = Base}
NW == Len(WptRows)
AllH(sc) == R("none")!Hs(sc)
WA(m, w) == LET sc == R(m)!Decode(WptRows[w].sc) IN R(m)!Allowed(sc, WptRows[w].k, COIChoices, AllH(sc))
WptOut == {WptRows[w].id : w \in {v \in 1..NW : WptRows[v].want \notin WA("none", v)}}
WptKilled == {<<WptRows[w].id, m>> : w \in 1..NW, m \in {y \in Ms : WptRows[w].want \in WA("none", w)
                                                          /\ WptRows[w].want \notin WA(y, w)}}
Focus == R("none")!LocalMutants
PrintAllowed ==
  /\ PrintT(<<"cfg", COIChoices, "rows", N, "mutants", Cardinality(Ms)>>)
  /\ PrintT(<<"equivalent-on-rows", Equivalent>>)
  /\ \A b \in Browsers :
       /\ PrintT(<<"counts", b, "observed", Cardinality(ObsIdx(b)), "inside", Cardinality(Inside(b)),
                   "out", Cardinality(Out(b)), "killed", Cardinality(Killed(b)),
                   "survived-nonequivalent", (Ms \ Killed(b)) \ Equivalent>>)
       /\ PrintT(<<"killed", b, {<<m, Cardinality(KillRows(m, b))>> : m \in Killed(b)}>>)
       /\ PrintT(<<"out-of-model", b, {<<Rows[r].id, Rows[r][b], Base[b][r], H(r, b)>> : r \in Out(b)}>>)
       /\ PrintT(<<"rescuing-all", b, {<<m, Cardinality(KillRows(m, b))>> :
                    m \in {y \in Ms : Out(b) # {} /\ \A r \in Out(b) : Rows[r][b] \subseteq MT[y][b][r]}}>>)
  /\ PrintT(<<"wpt-out", WptOut>>)
  /\ PrintT(<<"wpt-killed", WptKilled>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
