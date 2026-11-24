------------------------------- MODULE GenModel -------------------------------
(* gen/RESULTS.md: what ../SpecIsolation.tla (fixed model, 3b9239d) allows   *)
(* for one generated scenario. A scenario sc is a record:                    *)
(*   d    depth 0..2; levels are 1 (top) .. d+1                             *)
(*   o    <<o1, o2, o3>> origins (unused levels repeat o1)                   *)
(*   e    <<e1, e2, e3>> COEP headers; corp <<"none", c2, c3>> CORP headers  *)
(*   coop top COOP; tgt origin of the no-cors fetch target (no CORP)         *)
(* Only SpecIsolation operators are used, except PP: the permissions-policy  *)
(* step of the crossOriginIsolated getter, which SpecIsolation does not      *)
(* model ("no permissions policy"). With WithPP = FALSE a nested document's  *)
(* getter is the group's mode alone.                                         *)
EXTENDS Naturals, Sequences
CONSTANT Mutant
VARIABLE dummy
SI == INSTANCE SpecIsolation

B2S(b) == IF b THEN "TRUE" ELSE "FALSE"
\* A navigation request carries credentials (forNavigation makes it moot).
R(sc, i) == [origin |-> sc.o[i], corp |-> sc.corp[i], creds |-> TRUE]
Ctx1(sc) == SI!TopCtx(sc.o[1])
PEC1(sc) == SI!EffectiveCOEP(sc.o[1], sc.e[1])
Ctx2(sc) == SI!ChildCtx(Ctx1(sc), R(sc, 2))
PEC2(sc) == SI!EffectiveCOEPCtx(Ctx2(sc), sc.e[2])
Ctx3(sc) == SI!ChildCtx(Ctx2(sc), R(sc, 3))
Ctx(sc, i) == CASE i = 1 -> Ctx1(sc) [] i = 2 -> Ctx2(sc) [] OTHER -> Ctx3(sc)
\* Navigation of level i (2 or 3) from its parent.
Nav(sc, i) == IF i = 2 THEN SI!NavChild(Ctx1(sc), PEC1(sc), R(sc, 2), sc.e[2])
              ELSE SI!NavChild(Ctx2(sc), PEC2(sc), R(sc, 3), sc.e[3])
Loaded(sc, i) == \A j \in 2..i : Nav(sc, j) = "loaded"

\* Permissions Policy (not in SpecIsolation): "cross-origin-isolated" has
\* default allowlist 'self'; without an allow attribute a child document is
\* allowed only if its parent is and it is same origin with its parent.
PP(sc, i) == \A j \in 2..i : SI!SameOrigin(sc.o[j], sc.o[j - 1])
\* The browsing context group's mode is the top-level document's.
COIConcrete(sc, i, withPP) ==
  SI!CrossOriginIsolated(sc.coop, sc.e[1], sc.o[1]) /\ (withPP => PP(sc, i))
Sec(sc, i) == SI!SecureCtx(Ctx(sc, i))
Fetch(sc, creds) ==
  SI!FetchResultCtx(Ctx(sc, sc.d + 1), sc.e[sc.d + 1], "no-cors",
                    [origin |-> sc.tgt, corp |-> "none", creds |-> creds])

Any == {"TRUE", "FALSE", "loaded", "blocked", "basic", "cors", "opaque", "error"}
\* Allowed values of row kind k at level i, over COIChoice in cc. A row of a
\* level the model does not load is unconstrained (its load row decides).
\* Under COIChoice "logical" the getter is FALSE whatever the mutant does.
Allowed(sc, i, k, cc, withPP) ==
  IF k = "load" THEN (IF Loaded(sc, i - 1) THEN {IF Nav(sc, i) = "loaded" THEN "loaded" ELSE "blocked"}
                      ELSE Any)
  ELSE IF ~Loaded(sc, i) THEN Any
  ELSE CASE k = "coi"    -> (IF "concrete" \in cc THEN {B2S(COIConcrete(sc, i, withPP))} ELSE {})
                            \cup (IF "logical" \in cc THEN {"FALSE"} ELSE {})
         [] k = "sec"    -> {B2S(Sec(sc, i))}
         [] k = "fetch"  -> {Fetch(sc, FALSE)}
         [] k = "fetchc" -> {Fetch(sc, TRUE)}

\* Every row of a scenario, in a fixed order (for equivalence over the space).
Kinds(sc, i) == <<"load", "coi", "sec">> \o (IF i = sc.d + 1 THEN <<"fetch", "fetchc">> ELSE <<>>)
Vec(sc, cc, withPP) ==
  [i \in 1..(sc.d + 1) |-> [j \in 1..Len(Kinds(sc, i)) |->
     IF i = 1 /\ Kinds(sc, i)[j] = "load" THEN {"loaded"}
     ELSE Allowed(sc, i, Kinds(sc, i)[j], cc, withPP)]]
===============================================================================
