------------------------------- MODULE GenEnum --------------------------------
(* gen/RESULTS.md: the whole generated space (35652 scenarios, as gen.py     *)
(* builds them), without browsers. A mutant is "distinguishable" if some     *)
(* scenario's vector of allowed sets (GenModel!Vec) differs from the         *)
(* unmutated model's; one that is not is equivalent on the whole space, and  *)
(* no observation of these axes can kill it.                                 *)
EXTENDS Naturals, Sequences, FiniteSets, TLC
CONSTANTS COIChoices, WithPP
VARIABLE dummy
G(m) == INSTANCE GenModel WITH Mutant <- m
Ms == G("none")!SI!MechMutants \cup G("none")!SI!Mutants \cup G("none")!SI!FixMutants

Sch   == <<"https", "http">>
COEPq == <<"unsafe-none", "require-corp", "credentialless">>
COOPq == <<"unsafe-none", "same-origin">>
RELq  == <<"same-host", "same-site", "cross-site">>
CORPq == <<"none", "same-origin", "cross-origin">>
\* Index orders follow itertools.product in gen.py.
TopOf(t) == LET x == t - 1 IN [s |-> Sch[x \div 6 + 1], e |-> COEPq[((x \div 2) % 3) + 1], coop |-> COOPq[(x % 2) + 1]]
ChildOf(c) == LET x == c - 1 IN
  [s |-> Sch[x \div 27 + 1], rel |-> RELq[((x \div 9) % 3) + 1], e |-> COEPq[((x \div 3) % 3) + 1],
   corp |-> CORPq[(x % 3) + 1]]
Other(site) == IF site = "a" THEN "b" ELSE "a"
RelHost(p, rel) == CASE rel = "same-host" -> p
                     [] rel = "same-site" -> [site |-> p.site, sub |-> IF p.sub = "" THEN "1" ELSE ""]
                     [] OTHER -> [site |-> Other(p.site), sub |-> ""]
Org(s, h) == [scheme |-> s, host |-> h.site \o h.sub, site |-> h.site]
H0 == [site |-> "a", sub |-> ""]
\* cs: <<>>, <<c>> or <<c, g>> child configuration indices.
ScenOf(t, cs) ==
  LET T  == TopOf(t)
      d  == Len(cs)
      C1 == IF d >= 1 THEN ChildOf(cs[1]) ELSE ChildOf(1)
      C2 == IF d >= 2 THEN ChildOf(cs[2]) ELSE ChildOf(1)
      h1 == RelHost(H0, C1.rel)
      h2 == RelHost(h1, C2.rel)
      o0 == Org(T.s, H0)
      deep == CASE d = 0 -> H0 [] d = 1 -> h1 [] OTHER -> h2
  IN [d |-> d, coop |-> T.coop,
      o |-> <<o0, IF d >= 1 THEN Org(C1.s, h1) ELSE o0, IF d >= 2 THEN Org(C2.s, h2) ELSE o0>>,
      e |-> <<T.e, IF d >= 1 THEN C1.e ELSE T.e, IF d >= 2 THEN C2.e ELSE T.e>>,
      corp |-> <<"none", IF d >= 1 THEN C1.corp ELSE "none", IF d >= 2 THEN C2.corp ELSE "none">>,
      tgt |-> Org("https", [site |-> Other(deep.site), sub |-> ""])]
Idx == {<<t>> : t \in 1..12} \cup {<<t, c>> : t \in 1..12, c \in 1..54}
       \cup {<<t, c, g>> : t \in 1..12, c \in 1..54, g \in 1..54}
SC(x) == ScenOf(x[1], SubSeq(x, 2, Len(x)))
Base == [x \in Idx |-> G("none")!Vec(SC(x), COIChoices, WithPP)]
Witness(m) == CHOOSE x \in Idx : G(m)!Vec(SC(x), COIChoices, WithPP) # Base[x]
Dist == {m \in Ms : \E x \in Idx : G(m)!Vec(SC(x), COIChoices, WithPP) # Base[x]}
\* depth of the shallowest distinguishing scenario of each distinguishable mutant
MinDepth(m) == CHOOSE k \in 0..2 :
  /\ \E x \in Idx : Len(x) = k + 1 /\ G(m)!Vec(SC(x), COIChoices, WithPP) # Base[x]
  /\ \A j \in 0..(k - 1) : \A x \in Idx : Len(x) = j + 1 => G(m)!Vec(SC(x), COIChoices, WithPP) = Base[x]
PrintEnum ==
  /\ PrintT(<<"enum", COIChoices, WithPP, "scenarios", Cardinality(Idx), "mutants", Cardinality(Ms)>>)
  /\ PrintT(<<"equivalent-on-space", Ms \ Dist>>)
  /\ PrintT(<<"min-depth", {<<m, MinDepth(m)>> : m \in Dist}>>)

Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
