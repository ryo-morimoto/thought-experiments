----------------------------- MODULE RedirectSat ------------------------------
(* adequacy/RESULTS.md: does the redirect chain of ../redirect/RedirectSeq.tla *)
(* saturate in its length? For a mutant m the key after n hops is            *)
(*   <<unmutated enforcement result, m's enforcement result, first hop>>,    *)
(* and the next layer is the image of the current one under one hop, so     *)
(* Keys(n) = Keys(n+1) means every later layer is the same set. Every       *)
(* observation (RedirectSeq!Vec) is computed by RedirectSeq itself on a      *)
(* witness chain that reaches the key. RedirectSeq is unedited; MkHop and   *)
(* MkFin are its Hop and Fin with more origins (Rels, overridable in .cfg). *)
EXTENDS Integers, Sequences, FiniteSets, TLC
VARIABLE dummy
R(m) == INSTANCE RedirectSeq WITH Mutant <- m
N0 == INSTANCE RedirectSeq WITH Mutant <- "none"
SI == INSTANCE SpecIsolation WITH Mutant <- "none"
OC == [scheme |-> "https", host |-> "c.test", site |-> "c.test"]
\* Relation of a response's origin to the opener's (A = SI!OA).
\* O, S, X are RedirectSeq's three (Org); the rest are new.
Org7(rel) == CASE rel = "O" -> SI!OA [] rel = "S" -> SI!OAwww [] rel = "X" -> SI!OB
              [] rel = "S2" -> SI!OAwww2 [] rel = "X2" -> OC
              [] rel = "Oh" -> SI!OAhttp [] rel = "Xh" -> SI!OBhttp
Rels3 == {"O", "S", "X"}
Rels7 == {"O", "S", "X", "S2", "X2", "Oh", "Xh"}
Rels == Rels3
HopK == Rels \X (1..4)
FinK == Rels \X (1..3) \X (1..2)
MkHop(p) == [o |-> Org7(p[1]), coop |-> N0!HCOOP(N0!OPq[p[2]]), coep |-> N0!HCOEP(N0!OPq[p[2]]),
             redirect |-> TRUE]
MkFin(f) == [o |-> Org7(f[1]), coop |-> N0!FCq[f[2]], coep |-> N0!FEq[f[3]], redirect |-> FALSE]
Sc(op, st, ps, f) == [op |-> N0!OPq[op], st |-> N0!STq[st], nh |-> Len(ps),
                      rs |-> [j \in 1..Len(ps) |-> MkHop(ps[j])] \o <<MkFin(f)>>]
Sc0(op, st) == Sc(op, st, <<>>, <<"O", 1, 1>>)
CL == {"concrete", "logical"}
MaxN == 5
BFN == 2

Key0(m, op, st) == <<N0!Src1(Sc0(op, st)), R(m)!Src1(Sc0(op, st)), <<>>>>
Step(m, op, st, k, p) ==
  LET b == N0!Blank1(Sc0(op, st)) IN
  <<N0!Enforce(b, k[1], MkHop(p)), R(m)!Enforce(b, k[2], MkHop(p)),
    IF k[3] = <<>> /\ m = "first-hop-only" THEN p ELSE k[3]>>
\* Keys after n hops, each with one witness chain.
WitL(m, op, st) ==
  LET F[n \in 0..MaxN] ==
        IF n = 0 THEN [k \in {Key0(m, op, st)} |-> <<>>]
        ELSE LET P == F[n - 1]
                 Cand == {<<Step(m, op, st, k, p), Append(P[k], p)>> : k \in DOMAIN P, p \in HopK}
             IN [k \in {c[1] : c \in Cand} |-> (CHOOSE c \in Cand : c[1] = k)[2]]
  IN F
Ops == (1..4) \X (1..2)
Ms == N0!AllMutants
\* The mutants this run looks at (cfg: RunMs <- ...); "none" always.
RunMs == Ms
NoMs == {}
\* Every layer, evaluated once (a constant definition).
LT == [m \in RunMs \cup {"none"} |-> [x \in Ops |->
         LET F == WitL(m, x[1], x[2]) IN [n \in 0..MaxN |-> F[n]]]]
Wit(m, op, st, n) == LT[m][<<op, st>>][n]
\* Per layer n: keys (over all openers), observations of m and of none.
Layer(m, n) ==
  UNION {LET W == Wit(m, x[1], x[2], n) IN {<<x, k, W[k]>> : k \in DOMAIN W} : x \in Ops}
Keys(m, n) == {<<e[1], e[2]>> : e \in Layer(m, n)}
ObsPair(m, n) == {<<e[1], f, N0!Vec(Sc(e[1][1], e[1][2], e[3], f), CL),
                    R(m)!Vec(Sc(e[1][1], e[1][2], e[3], f), CL)>> : e \in Layer(m, n), f \in FinK}
Dist(m, n) == \E o \in ObsPair(m, n) : o[3] # o[4]
ObsNone(n) == {<<o[1], o[2], o[3]>> : o \in ObsPair("none", n)}

\* Brute force over all chains of length n, unmutated (cross-check).
BF(n) == {<<x, f, N0!Vec(Sc(x[1], x[2], ps, f), CL)>> :
            x \in Ops, ps \in [1..n -> HopK], f \in FinK}

PrintBase ==
  /\ PrintT(<<"rels", Rels, "base-keys", [n \in 0..MaxN |-> Cardinality(Keys("none", n))],
              "base-obs", [n \in 0..MaxN |-> Cardinality(ObsNone(n))],
              "obs-eq-prev", [n \in 1..MaxN |-> ObsNone(n) = ObsNone(n - 1)],
              "keys-eq-prev", [n \in 1..MaxN |-> Keys("none", n) = Keys("none", n - 1)]>>)
PrintBF == PrintT(<<"bf-agrees", [n \in 0..BFN |-> BF(n) = ObsNone(n)]>>)
\* RedirectSeq's sequence properties P1..P4, unmutated, over all chains of
\* length 0..BFN on Rels: the ones that fail.
PropFailsBF == {p \in {"P1", "P1c", "P2", "P2c", "P3", "P4"} :
  \E x \in Ops, n \in 0..BFN : \E ps \in [1..n -> HopK], f \in FinK :
    ~N0!Prop(p, Sc(x[1], x[2], ps, f))}
PrintPropsBF == PrintT(<<"props-bf", Rels, PropFailsBF>>)
\* First n at which Keys(m, n) = Keys(m, n - 1), and the n at which m is
\* first distinguishable (0..MaxN, or -1).
SatAt(m) == IF \E n \in 1..MaxN : Keys(m, n) = Keys(m, n - 1)
            THEN CHOOSE n \in 1..MaxN : Keys(m, n) = Keys(m, n - 1)
                                       /\ \A j \in 1..(n - 1) : Keys(m, j) # Keys(m, j - 1)
            ELSE -1
FirstDist(m) == IF \E n \in 0..MaxN : Dist(m, n)
                THEN CHOOSE n \in 0..MaxN : Dist(m, n) /\ \A j \in 0..(n - 1) : ~Dist(m, j)
                ELSE -1
PrintMut == PrintT(<<"mutants", Cardinality(Ms),
  "rows", {<<m, SatAt(m), FirstDist(m)>> : m \in RunMs}>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
