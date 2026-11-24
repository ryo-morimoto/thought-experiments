------------------------------ MODULE RedirectSeq -----------------------------
(* redirect/RESULTS.md, for experiments/2026-11-24-redirect-sequence-model.md. *)
(* A popup navigation through 0..2 redirect hops, as a sequence of updates of *)
(* HTML's "opener policy enforcement result" (html.src 0e292f4):             *)
(*  - create navigation params by fetching: for each response, redirects     *)
(*    included, "Set coopEnforcementResult to the result of enforcing the    *)
(*    response's opener policy" (top-level traversable only).               *)
(*  - enforce a response's opener policy: the new result starts with the     *)
(*    current result's "needs a browsing context group switch", takes the    *)
(*    response's url, origin and opener policy, and sets the flag if "check  *)
(*    if COOP values require a browsing context group switch" is true,       *)
(*    comparing with the CURRENT result's origin and opener policy (the      *)
(*    previous response), with isInitialAboutBlank of the active document.   *)
(*  - obtain a browsing context to use for a navigation response: swapGroup  *)
(*    is the final result's flag; the new group's isolation mode comes from  *)
(*    navigationParams's opener policy (the final response's).               *)
(* Report-only COOP is not on the axes, so "would need ... due to          *)
(* report-only" stays FALSE and is not represented.                           *)
(* Operators of ../SpecIsolation.tla (fixed model, unedited) are reused:     *)
(* ParsedCOOP, MatchCOOP, PopupSevered, COIMode, and its C(id, e) wrapper.   *)
EXTENDS Naturals, Sequences, FiniteSets, TLC
CONSTANT Mutant
VARIABLE dummy
SI == INSTANCE SpecIsolation
C(id, e) == SI!C(id, e)

\* Decisions of the sequence steps; "neg:<id>" negates one (constant TRUE
\* gates mean: negating omits the step).
RedirectIds == {
  "hop-accumulate",   \* new result keeps the current result's switch flag
  "hop-switch",       \* the per-response check sets the flag
  "hop-update",       \* new result takes the response's origin and COOP
  "hop-blank",        \* isInitialAboutBlank selects the popup check
  "hop-coep",         \* a redirect response's COOP is parsed with its own COEP
  "blank-inherit",    \* initial about:blank takes the opener's COOP
  "final-swap",       \* swapGroup is the final result's flag
  "hop-same-entry"}   \* a redirect replaces the URL of the same history entry
\* neg:hop-accumulate = "no accumulation"; neg:hop-update = "compare with source".
\* Named: look at one response only, against the navigation source.
HopMutants == {"first-hop-only", "final-hop-only"}
LocalMutants == {"neg:" \o d : d \in RedirectIds} \cup HopMutants
AllMutants == SI!MechMutants \cup SI!Mutants \cup SI!FixMutants \cup LocalMutants

\* --- Scenario encoding (gen.py writes the same codes) ---------------------
OPq  == <<"unsafe-none", "same-origin-allow-popups", "same-origin", "so+rc">>
STq  == <<"blank", "doc">>
RELq == <<"same-origin", "same-site", "cross-site">>
FCq  == <<"unsafe-none", "same-origin-allow-popups", "same-origin">>
FEq  == <<"unsafe-none", "require-corp">>
\* x = <<op, st, hops, fin>>; hops = <<<<rel, hc>>, ...>> (hc indexes OPq);
\* fin = <<rel, fc, fe>>.
Org(rel) == CASE rel = "same-origin" -> SI!OA [] rel = "same-site" -> SI!OAwww [] OTHER -> SI!OB
HCOOP(h) == IF h = "so+rc" THEN "same-origin" ELSE h
HCOEP(h) == IF h = "so+rc" THEN "require-corp" ELSE "unsafe-none"
Hop(p) == [o |-> Org(RELq[p[1]]), coop |-> HCOOP(OPq[p[2]]), coep |-> HCOEP(OPq[p[2]]), redirect |-> TRUE]
Fin(f) == [o |-> Org(RELq[f[1]]), coop |-> FCq[f[2]], coep |-> FEq[f[3]], redirect |-> FALSE]
Decode(x) == [op |-> OPq[x[1]], st |-> STq[x[2]], nh |-> Len(x[3]),
              rs |-> [j \in 1..Len(x[3]) |-> Hop(x[3][j])] \o <<Fin(x[4])>>]

\* --- One response ---------------------------------------------------------
\* HTML "obtain an opener policy" (with "obtain a cross-origin embedder policy"
\* from the same response). All origins here are https.
Parsed(r) == SI!ParsedCOOP(r.coop,
               IF r.redirect /\ ~C("hop-coep", TRUE) THEN "unsafe-none" ELSE r.coep, r.o)
\* HTML "check if COOP values require a browsing context group switch".
CheckSwitch(blank, cur, r) ==
  IF C("hop-blank", blank) THEN SI!PopupSevered(cur.coop, cur.origin, Parsed(r), r.o)
  ELSE ~SI!MatchCOOP(cur.coop, cur.origin, Parsed(r), r.o)
\* HTML "enforce a response's opener policy".
Enforce(blank, cur, r) ==
  [needs  |-> (C("hop-accumulate", TRUE) /\ cur.needs) \/ C("hop-switch", CheckSwitch(blank, cur, r)),
   origin |-> IF C("hop-update", TRUE) THEN r.o ELSE cur.origin,
   coop   |-> IF C("hop-update", TRUE) THEN Parsed(r) ELSE cur.coop]
RECURSIVE Chain(_, _, _)
Chain(blank, cur, rs) == IF rs = <<>> THEN cur ELSE Chain(blank, Enforce(blank, cur, Head(rs)), Tail(rs))
NavNeeds(blank, src, rs) ==
  CASE Mutant = "first-hop-only" -> CheckSwitch(blank, src, rs[1])
    [] Mutant = "final-hop-only" -> CheckSwitch(blank, src, rs[Len(rs)])
    [] OTHER -> Chain(blank, src, rs).needs
\* HTML "obtain a browsing context to use for a navigation response" (popup:
\* group size > 1, http(s) only, no browser UI: none of the optional swaps).
Swap(blank, src, rs) == C("final-swap", NavNeeds(blank, src, rs))

\* --- A scenario ------------------------------------------------------------
\* The opener is the top-level test page at OA with COOP (and COEP) sc.op.
\* st = "blank": window.open(chain). st = "doc": window.open of a page at OA
\* with the opener's headers, which then sets location to the chain.
Res0(o, coop) == [needs |-> FALSE, origin |-> o, coop |-> coop]
OpResp(sc) == [o |-> SI!OA, coop |-> HCOOP(sc.op), coep |-> HCOEP(sc.op), redirect |-> FALSE]
OpenerMode(sc) == SI!COIMode(HCOOP(sc.op), HCOEP(sc.op), SI!OA)
\* create a new browsing context and document: the initial about:blank's COOP.
BlankSrc(sc) == Res0(SI!OA, IF C("blank-inherit", TRUE) THEN Parsed(OpResp(sc)) ELSE "unsafe-none")
Swap0(sc) == sc.st = "doc" /\ Swap(TRUE, BlankSrc(sc), <<OpResp(sc)>>)
Mode0(sc) == IF Swap0(sc) THEN SI!COIMode(HCOOP(sc.op), HCOEP(sc.op), SI!OA) ELSE OpenerMode(sc)
Blank1(sc) == sc.st = "blank"
Src1(sc) == IF Blank1(sc) THEN BlankSrc(sc) ELSE Res0(SI!OA, Parsed(OpResp(sc)))
Swap1(sc) == Swap(Blank1(sc), Src1(sc), sc.rs)
FinalR(sc) == sc.rs[Len(sc.rs)]
Severed(sc) == Swap0(sc) \/ Swap1(sc)
FinalMode(sc) == IF Swap1(sc) THEN SI!COIMode(FinalR(sc).coop, FinalR(sc).coep, FinalR(sc).o) ELSE Mode0(sc)
HLen(sc) == (IF sc.st = "doc" THEN 2 ELSE 1) + (IF C("hop-same-entry", TRUE) THEN 0 ELSE sc.nh)

B2S(b) == IF b THEN "TRUE" ELSE "FALSE"
\* Allowed values per observation kind, over COIChoice in cc.
Allowed(sc, k, cc) ==
  CASE k = "closed" -> {B2S(Severed(sc))}
    [] k = "opener" -> {B2S(~Severed(sc))}
    [] k = "coi"    -> (IF "concrete" \in cc THEN {B2S(FinalMode(sc) = "concrete")} ELSE {})
                       \cup (IF "logical" \in cc THEN {"FALSE"} ELSE {})
    [] k = "hlen"   -> {ToString(HLen(sc))}
Kinds == <<"closed", "opener", "coi", "hlen">>
Vec(sc, cc) == [j \in 1..4 |-> Allowed(sc, Kinds[j], cc)]

\* --- Sequence properties (stated on responses, not on the accumulated flag) --
\* Pred(sc, j): what response j is compared with if each step looks at its
\* predecessor; SrcCheck: response j against the navigation source.
Pred(sc, j) == IF j = 1 THEN Src1(sc) ELSE Res0(sc.rs[j - 1].o, Parsed(sc.rs[j - 1]))
StepCheck(sc, j) == CheckSwitch(Blank1(sc), Pred(sc, j), sc.rs[j])
SrcCheck(sc, j)  == CheckSwitch(Blank1(sc), Src1(sc), sc.rs[j])
Js(sc) == 1..Len(sc.rs)
\* P1: a COOP mismatch at any step severs the final document from its opener.
P1(sc) == (\E j \in Js(sc) : StepCheck(sc, j)) => Severed(sc)
\* P1c: severing has a cause in some step (with no doc-start swap).
P1c(sc) == (Swap1(sc)) => (\E j \in Js(sc) : StepCheck(sc, j))
\* P2: any response mismatching the source severs.
P2(sc) == (\E j \in Js(sc) : SrcCheck(sc, j)) => Severed(sc)
\* P2c: converse of P2 (only responses vs the source decide). Expected FALSE.
P2c(sc) == Swap1(sc) => (\E j \in Js(sc) : SrcCheck(sc, j))
\* P3: an isolated final document has COOP same-origin + compatible COEP itself.
P3(sc) == FinalMode(sc) = "concrete" => Parsed(FinalR(sc)) = "same-origin-plus-COEP"
\* P4: if not severed, the final document is in the opener's group, with its mode.
P4(sc) == ~Severed(sc) => FinalMode(sc) = OpenerMode(sc)
Props == <<"P1", "P1c", "P2", "P2c", "P3", "P4">>
Prop(p, sc) == CASE p = "P1" -> P1(sc) [] p = "P1c" -> P1c(sc) [] p = "P2" -> P2(sc)
                 [] p = "P2c" -> P2c(sc) [] p = "P3" -> P3(sc) [] OTHER -> P4(sc)

===============================================================================
