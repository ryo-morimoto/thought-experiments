------------------------------ MODULE HistoryEnum ------------------------------
(* history/RESULTS.md: pre-screen on the model, without browsers. For every    *)
(* scenario of the whole space (HistorySpace.tla, from gen.py) the set of      *)
(* mutants whose observation function (per UA bfcache choice vector:          *)
(* feasibility, opener, closed, isolation mode, history length) differs from  *)
(* the unmutated one. COIChoice {concrete} and {concrete, logical} give the    *)
(* same sets here (only the mode none/concrete is compared), so the class key *)
(* prints the set twice, in gen.py's format. Also: the sequence properties    *)
(* Q1..Q5 (HistorySeq) on the whole space, unmutated and per local mutant.   *)
EXTENDS Integers, Sequences, FiniteSets, TLC, HistorySpace
CONSTANTS Lo, Hi
VARIABLE dummy
R(m) == INSTANCE HistorySeq WITH Mutant <- m
Ms == R("none")!AllMutants
N == Len(Space)
Idx == Lo..(IF Hi > N THEN N ELSE Hi)
S(i) == R("none")!Decode(Space[i])
Raw(m, i) == LET sc == S(i) IN
  [h \in R(m)!Hs(sc) |-> IF R(m)!Feasible(sc, h)
     THEN LET f == R(m)!Final(sc, h) IN
          <<f.bcs[R(m)!Active(f).bc].opener, R(m)!Active(f).bc # 1, R(m)!Active(f).mode, Len(f.es)>>
     ELSE <<>>]
Base == [i \in Idx |-> Raw("none", i)]
D == [i \in Idx |-> {m \in Ms : Raw(m, i) # Base[i]}]
Classes == {D[i] : i \in Idx}
Members(cl) == {i \in Idx : D[i] = cl}
Union(F) == UNION {F[i] : i \in Idx}
DistSeqs(m) == {S(i).sq : i \in {j \in Idx : m \in D[j]}}
PrintEnum ==
  /\ PrintT(<<"enum", "scenarios", Cardinality(Idx), "mutants", Cardinality(Ms)>>)
  /\ PrintT(<<"equivalent-on-space", Ms \ Union(D)>>)
  /\ PrintT(<<"dist-count", {<<m, Cardinality({i \in Idx : m \in D[i]})>> : m \in Union(D)}>>)
  /\ PrintT(<<"dist-seqs", {<<m, DistSeqs(m)>> : m \in Union(D)}>>)
  /\ PrintT(<<"nclasses", Cardinality(Classes)>>)
  /\ \A cl \in Classes : PrintT(<<"class", cl, cl, Members(cl)>>)
\* Sequence properties per mutant: the ones failing on some feasible run, with a witness.
Bad(m, p, nohit, i, h) == (nohit => R(m)!NoHit(h)) /\ ~R(m)!Prop(p, S(i), R(m)!Run(S(i), h))
Fails(m, p, nohit) == {i \in Idx : \E h \in R(m)!Fs(S(i)) : Bad(m, p, nohit, i, h)}
PropFails(m, nohit) == {p \in {"Q1", "Q2", "Q3", "Q4", "Q5"} : Fails(m, p, nohit) # {}}
Wit(m, p, nohit) == LET F == Fails(m, p, nohit) IN
  LET i == CHOOSE j \in F : \A k \in F : j <= k IN
  <<Space[i], CHOOSE h \in R(m)!Fs(S(i)) : Bad(m, p, nohit, i, h)>>
PrintProps ==
  /\ PrintT(<<"props-none", PropFails("none", FALSE),
              {<<p, Wit("none", p, FALSE), Cardinality(Fails("none", p, FALSE))>> : p \in PropFails("none", FALSE)}>>)
  /\ PrintT(<<"props-none-nohit", PropFails("none", TRUE)>>)
  /\ PrintT(<<"props-mutants", {<<m, PropFails(m, FALSE), PropFails(m, TRUE)>> : m \in R("none")!LocalMutants
               \cup {"neg:popup-opener-sap", "neg:popup-unsafe", "neg:coop-equal",
                     "neg:coop-same-origin", "popup-no-sap-exception", "neg:coi-mode"}}>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
