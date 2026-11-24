------------------------------ MODULE RedirectEnum -----------------------------
(* redirect/RESULTS.md: pre-screen on the model, without browsers. For every  *)
(* scenario of the whole space (RedirectSpace.tla, from gen.py) the set of     *)
(* mutants whose allowed-value vector differs from the unmutated one, under   *)
(* COIChoice {concrete, logical} (Dl) and {concrete} (Dc). Scenarios with the *)
(* same pair form a class; gen.py select runs representatives of each class. *)
(* Also: which sequence properties (RedirectSeq P1..P4) each mutant breaks.   *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, RedirectSpace
VARIABLE dummy
R(m) == INSTANCE RedirectSeq WITH Mutant <- m
Ms == R("none")!AllMutants
N == Len(Space)
CL == {"concrete", "logical"}
CC == {"concrete"}
S(i) == R("none")!Decode(Space[i])
BaseL == [i \in 1..N |-> R("none")!Vec(S(i), CL)]
BaseC == [i \in 1..N |-> R("none")!Vec(S(i), CC)]
DL == [i \in 1..N |-> {m \in Ms : R(m)!Vec(S(i), CL) # BaseL[i]}]
DC == [i \in 1..N |-> {m \in Ms : R(m)!Vec(S(i), CC) # BaseC[i]}]
Classes == {<<DL[i], DC[i]>> : i \in 1..N}
Members(cl) == {i \in 1..N : <<DL[i], DC[i]>> = cl}
Union(F) == UNION {F[i] : i \in 1..N}
\* Shallowest number of hops at which a mutant is distinguishable (CL).
MinHops(m) == CHOOSE h \in 0..2 : /\ \E i \in 1..N : m \in DL[i] /\ S(i).nh = h
                                  /\ \A i \in 1..N : (m \in DL[i] /\ S(i).nh < h) => FALSE
PrintEnum ==
  /\ PrintT(<<"enum", "scenarios", N, "mutants", Cardinality(Ms)>>)
  /\ PrintT(<<"equivalent-on-space-L", Ms \ Union(DL)>>)
  /\ PrintT(<<"equivalent-on-space-C", Ms \ Union(DC)>>)
  /\ PrintT(<<"min-hops", {<<m, MinHops(m)>> : m \in Union(DL)}>>)
  /\ PrintT(<<"dist-count", {<<m, Cardinality({i \in 1..N : m \in DL[i]})>> : m \in Union(DL)}>>)
  /\ PrintT(<<"nclasses", Cardinality(Classes)>>)
  /\ \A cl \in Classes : PrintT(<<"class", cl[1], cl[2], Members(cl)>>)
\* Sequence properties over the whole space, per mutant: the ones that fail.
PropFails(m) == {p \in {"P1", "P1c", "P2", "P2c", "P3", "P4"} :
                   \E i \in 1..N : ~R(m)!Prop(p, R(m)!Decode(Space[i]))}
Witness(m, p) == CHOOSE i \in 1..N : ~R(m)!Prop(p, R(m)!Decode(Space[i]))
PrintProps ==
  /\ PrintT(<<"props-none", PropFails("none"),
              {<<p, Space[Witness("none", p)]>> : p \in PropFails("none")}>>)
  /\ PrintT(<<"props-mutants", {<<m, PropFails(m)>> : m \in R("none")!LocalMutants
               \cup {"neg:popup-opener-sap", "neg:popup-unsafe", "neg:coop-equal",
                     "neg:coop-same-origin", "popup-no-sap-exception", "neg:coi-mode"}}>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
