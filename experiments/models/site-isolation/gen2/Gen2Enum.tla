------------------------------- MODULE Gen2Enum -------------------------------
(* gen2/RESULTS.md: the whole gen2 space (Gen2Space.tla, from gen2.py       *)
(* space), without browsers. For each mutant, the scenarios whose vector of *)
(* allowed sets (Gen2Model!Vec) differs from the unmutated model's. A       *)
(* mutant with none is equivalent on the whole space. gen2.py select reads  *)
(* the "dist" lines.                                                         *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, Gen2Space
CONSTANTS COIChoices, OACParam, CfgName
VARIABLE dummy
G(m) == INSTANCE Gen2Model WITH Mutant <- m
Ms == G("none")!SI!MechMutants \cup G("none")!SI!Mutants \cup G("none")!SI!FixMutants
      \cup G("none")!G2Mutants
N == Len(Scen)
Base == [s \in 1..N |-> G("none")!Vec(Scen[s], COIChoices)]
Dist(m) == {s \in 1..N : G(m)!Vec(Scen[s], COIChoices) # Base[s]}
PrintEnum ==
  /\ PrintT(<<"enum", CfgName, "scenarios", N, "mutants", Cardinality(Ms)>>)
  /\ \A m \in Ms : PrintT(<<"dist", CfgName, m, Dist(m)>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
