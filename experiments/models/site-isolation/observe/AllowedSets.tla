----------------------------- MODULE AllowedSets -----------------------------
(* Implementation inclusion (herd/litmus style): is every value a browser     *)
(* produced for a WPT scenario in the set of values SpecIsolation allows?    *)
(* Allowed(m, r) (AllowedRows.tla) ranges over the model's parameter          *)
(* COIChoice in {concrete, logical}; the model has no other nondeterminism.  *)
(* Source = "observed" uses Observed.tla; "expected" feeds the TSV expected  *)
(* column in as pseudo-observations, to check the pipeline.                 *)
EXTENDS AllowedRows, Observed

CONSTANT Source
B0 == IF Source = "expected" THEN {"expected"} ELSE Browsers
O(b) == IF Source = "expected" THEN Expected ELSE Obs(b)
ObsRows(b) == DOMAIN O(b)

Ms == S("none")!MechMutants \cup S("none")!Mutants

\* Rows whose observations are not all in the allowed set under m.
Out(m, b) == {r \in ObsRows(b) : ~(O(b)[r] \subseteq Allowed(m, r))}
\* m is killed by b when some observation inside the unmutated model's set
\* falls outside m's set. Observations outside the base model cannot kill.
KillRows(m, b) == {r \in ObsRows(b) :
                     O(b)[r] \subseteq Allowed("none", r) /\ ~(O(b)[r] \subseteq Allowed(m, r))}
\* Observations outside the base model that m lets in.
RescueRows(m, b) == Out("none", b) \ Out(m, b)
\* m allows the same sets as the base model on every row: no observation of
\* these 109 scenarios can kill it.
SameOnRows(m) == \A r \in Rows : Allowed(m, r) = Allowed("none", r)

Killed(b)    == {m \in Ms : KillRows(m, b) # {}}
Equivalent   == {m \in Ms : SameOnRows(m)}
Survived(b)  == (Ms \ Killed(b)) \ Equivalent

PrintAllowed == PrintT(<<"allowed-none",
  [i \in 1..Len(RowSeq) |-> <<RowSeq[i], Allowed("none", RowSeq[i])>>]>>)
PrintOut == \A b \in B0 : PrintT(<<"out-of-model", b, Out("none", b),
  {<<r, O(b)[r], Allowed("none", r)>> : r \in Out("none", b)}>>)
PrintKills == \A b \in B0 :
  /\ PrintT(<<"counts", b, "mutants", Cardinality(Ms), "killed", Cardinality(Killed(b)),
              "equivalent-on-rows", Cardinality(Equivalent),
              "survived-nonequivalent", Cardinality(Survived(b))>>)
  /\ PrintT(<<"killed", b, {<<m, KillRows(m, b)>> : m \in Killed(b)}>>)
  /\ PrintT(<<"survived-nonequivalent", b, Survived(b)>>)
  /\ PrintT(<<"rescuing", b, {<<m, RescueRows(m, b)>> : m \in {x \in Ms : RescueRows(x, b) # {}}}>>)
PrintEquivalent == PrintT(<<"equivalent-on-rows", Equivalent>>)

\* Constant-level module: a single state; the checks are invariants.
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
