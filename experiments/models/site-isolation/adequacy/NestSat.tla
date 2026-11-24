------------------------------- MODULE NestSat --------------------------------
(* adequacy/RESULTS.md: does ../gen/GenModel.tla's nesting saturate in its   *)
(* depth? GenModel fixes 3 levels; LevelStep is its per-level step          *)
(* (ChildCtx, NavChild, EffectiveCOEPCtx, PP) written once for any depth,   *)
(* with SpecIsolation's operators. The key of a level is                     *)
(*   <<ctx, policy-container COEP, COEP header, loaded, PP so far>>         *)
(* of the unmutated model and of mutant m, and its rows (load, coi, sec,    *)
(* fetch to every target) are functions of it. Keys(n+1) is the image of     *)
(* Keys(n), so Keys(n) = Keys(n+1) means every deeper level adds nothing.   *)
(* AgreeGen checks Rows against GenModel!Allowed for depth <= 2.             *)
EXTENDS Integers, Sequences, FiniteSets, TLC, Domains
VARIABLE dummy
S(m) == INSTANCE SpecIsolation WITH Mutant <- m
G(m) == INSTANCE GenModel WITH Mutant <- m
N0 == INSTANCE SpecIsolation WITH Mutant <- "none"
D == N0!AllOrigins
Tops == {N0!OA, N0!OAhttp} \X {"unsafe-none", "same-origin"} \X N0!COEPs
Child == D \X {"none", "same-origin", "cross-origin"} \X N0!COEPs
CC == {"concrete", "logical"}
WithPP == TRUE
B2S(b) == IF b THEN "TRUE" ELSE "FALSE"
AnyV == {"TRUE", "FALSE", "loaded", "blocked", "basic", "cors", "opaque", "error"}

K1(m, t) == LET o == t[1] IN
  [ctx |-> S(m)!TopCtx(o), pec |-> S(m)!EffectiveCOEP(o, t[3]), e |-> t[3],
   loaded |-> TRUE, nav |-> "loaded", pp |-> TRUE]
Rsp(c) == [origin |-> c[1], corp |-> c[2], creds |-> TRUE]
LevelStep(m, k, c) ==
  LET nav == S(m)!NavChild(k.ctx, k.pec, Rsp(c), c[3])
      cx  == S(m)!ChildCtx(k.ctx, Rsp(c))
  IN [ctx |-> cx, pec |-> S(m)!EffectiveCOEPCtx(cx, c[3]), e |-> c[3],
      loaded |-> k.loaded /\ nav = "loaded", nav |-> IF k.loaded THEN nav ELSE "unreached",
      pp |-> k.pp /\ N0!SameOrigin(c[1], k.ctx.self)]
\* GenModel!Allowed's rows for a level with key k (fetch to every target).
Rows(m, t, k) ==
  <<IF k.nav = "unreached" THEN AnyV ELSE {IF k.nav = "loaded" THEN "loaded" ELSE "blocked"},
    IF ~k.loaded THEN AnyV
    ELSE {B2S(S(m)!CrossOriginIsolated(t[2], t[3], t[1]) /\ (WithPP => k.pp))} \cup {"FALSE"},
    IF ~k.loaded THEN AnyV ELSE {B2S(S(m)!SecureCtx(k.ctx))},
    [x \in D \X BOOLEAN |->
       IF ~k.loaded THEN AnyV
       ELSE {S(m)!FetchResultCtx(k.ctx, k.e, "no-cors",
                                 [origin |-> x[1], corp |-> "none", creds |-> x[2]])}]>>
MaxD == 4
\* Layers of pairs <<unmutated key, m's key>> for top t.
LayersL(m, t) ==
  LET F[n \in 0..MaxD] ==
        IF n = 0 THEN {<<K1("none", t), K1(m, t)>>}
        ELSE {<<LevelStep("none", p[1], c), LevelStep(m, p[2], c)>> : p \in F[n - 1], c \in Child}
  IN F
KeysAt(m, n) == UNION {{<<t, p>> : p \in LayersL(m, t)[n]} : t \in Tops}
\* All layers of m at once (one evaluation of each layer).
AllLayers(m) == [t \in Tops |-> LET F == LayersL(m, t) IN [n \in 0..MaxD |-> F[n]]]
RowsAt(n) == {<<x[1], Rows("none", x[1], x[2][1])>> : x \in KeysAt("none", n)}
Dist(m, n) == \E x \in KeysAt(m, n) : Rows("none", x[1], x[2][1]) # Rows(m, x[1], x[2][2])

PrintBase ==
  PrintT(<<"nest-base", "keys", [n \in 0..MaxD |-> Cardinality(KeysAt("none", n))],
           "keys-eq-prev", [n \in 1..MaxD |-> KeysAt("none", n) = KeysAt("none", n - 1)],
           "rows", [n \in 0..MaxD |-> Cardinality(RowsAt(n))],
           "rows-eq-prev", [n \in 1..MaxD |-> RowsAt(n) = RowsAt(n - 1)]>>)

\* Cross-check with GenModel (fetch target fixed to GenModel's: no CORP).
GenSc(t, cs) == [d |-> Len(cs), coop |-> t[2],
  o |-> <<t[1]>> \o [i \in 1..Len(cs) |-> cs[i][1]] \o [i \in 1..(2 - Len(cs)) |-> t[1]],
  e |-> <<t[3]>> \o [i \in 1..Len(cs) |-> cs[i][3]] \o [i \in 1..(2 - Len(cs)) |-> t[3]],
  corp |-> <<"none">> \o [i \in 1..Len(cs) |-> cs[i][2]] \o [i \in 1..(2 - Len(cs)) |-> "none"],
  tgt |-> N0!OB]
KeyOf(m, t, cs) == LET F[i \in 0..Len(cs)] == IF i = 0 THEN K1(m, t) ELSE LevelStep(m, F[i - 1], cs[i])
                   IN F[Len(cs)]
AgreeGen(m, d) ==
  \A t \in Tops, cs \in [1..d -> Child] :
    LET sc == GenSc(t, cs) k == KeyOf(m, t, cs) r == Rows(m, t, k) i == d + 1 IN
    /\ (i > 1 => G(m)!Allowed(sc, i, "load", CC, WithPP) = r[1])
    /\ G(m)!Allowed(sc, i, "coi", CC, WithPP) = r[2]
    /\ G(m)!Allowed(sc, i, "sec", CC, WithPP) = r[3]
    /\ G(m)!Allowed(sc, i, "fetch", CC, WithPP) = r[4][<<N0!OB, FALSE>>]
    /\ G(m)!Allowed(sc, i, "fetchc", CC, WithPP) = r[4][<<N0!OB, TRUE>>]
PrintAgree == PrintT(<<"agree-gen", [d \in 0..1 |-> AgreeGen("none", d)]>>)

Ms == N0!MechMutants \cup N0!Mutants \cup N0!FixMutants
SatAt(m) == IF \E n \in 1..MaxD : KeysAt(m, n) = KeysAt(m, n - 1)
            THEN CHOOSE n \in 1..MaxD : KeysAt(m, n) = KeysAt(m, n - 1)
                   /\ \A j \in 1..(n - 1) : KeysAt(m, j) # KeysAt(m, j - 1)
            ELSE -1
FirstDist(m) == IF \E n \in 0..MaxD : Dist(m, n)
                THEN CHOOSE n \in 0..MaxD : Dist(m, n) /\ \A j \in 0..(n - 1) : ~Dist(m, j)
                ELSE -1
PrintMut == PrintT(<<"nest-mutants", Cardinality(Ms),
                     "rows", {<<m, SatAt(m), FirstDist(m)>> : m \in Ms}>>)
\* Rows at depth 3 seen at no depth 0..2, and one key giving each.
NewAt3 == RowsAt(3) \ (RowsAt(0) \cup RowsAt(1) \cup RowsAt(2))
PrintNew == PrintT(<<"new-at-3", Cardinality(NewAt3),
  {CHOOSE x \in KeysAt("none", 3) : <<x[1], Rows("none", x[1], x[2][1])>> = r : r \in NewAt3}>>)
Skip == TRUE
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
