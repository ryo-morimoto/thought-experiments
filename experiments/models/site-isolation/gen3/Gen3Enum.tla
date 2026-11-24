------------------------------- MODULE Gen3Enum -------------------------------
(* gen3/RESULTS.md: the whole gen3 space (Gen3Space.tla, from gen3.py space), *)
(* without browsers. For each mutant, the scenarios whose vector of allowed  *)
(* sets (Gen3Model!Vec) differs from the unmutated model's. gen3.py select   *)
(* reads the "dist" lines. Mutants: the author's (SpecIsolation's neg:,      *)
(* named and fix mutants), bugmut/'s bug-type mutants (true:/false: on every *)
(* SpecIsolation decision, as bugmut/BugMutants.tla names them) and G3's.    *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, Gen3Space
CONSTANTS COIChoices, OShare, RefMay, CfgName
VARIABLE dummy
G(m) == INSTANCE Gen3Model WITH Mutant <- m
Author == G("none")!SI!MechMutants \cup G("none")!SI!Mutants \cup G("none")!SI!FixMutants
BugNew == {"true:" \o d : d \in G("none")!SI!DecisionIds} \cup {"false:" \o d : d \in G("none")!SI!DecisionIds \ G("none")!SI!FixIds}
Ms == Author \cup BugNew \cup G("none")!G3Mutants
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
