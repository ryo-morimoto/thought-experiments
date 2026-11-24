------------------------------ MODULE HistorySeq ------------------------------
(* history/RESULTS.md, for experiments/2026-11-24-history-bfcache-sequence.md *)
(* A top-level traversable (a popup with an opener, or a noopener window) that *)
(* navigates and traverses its session history, as a sequence of states       *)
(* (html.src 0e292f4). Reading of the spec:                                   *)
(*  - navigate: "create navigation params by fetching" starts the opener      *)
(*    policy enforcement result from the navigable's ACTIVE document, then    *)
(*    "obtain a browsing context to use for a navigation response" swaps to a *)
(*    new browsing context (new group, no opener) iff the result's flag is    *)
(*    set. Forward entries are removed.                                       *)
(*  - traverse (apply the history step): if the target entry's document is    *)
(*    null, "attempt to populate the history entry's document" fetches again  *)
(*    (same COOP enforcement, source = the active document). Otherwise the    *)
(*    document is reused: "activate history entry" / "make active" set the   *)
(*    document's OWN browsing context's WindowProxy [[Window]] to it; no COOP *)
(*    step runs. The swap note keeps the old browsing context alive "such as *)
(*    ones in the back/forward cache".                                        *)
(*  - bfcache is optional ("intendToKeepInBfcache"), but must be false for an *)
(*    unsalvageable document; an active WebSocket makes it unsalvageable.     *)
(* The UA choice per traversal is a vector h of booleans (TRUE = the target   *)
(* entry's document was kept). Observations are taken from the final state.  *)
(* ../SpecIsolation.tla (unedited) gives ParsedCOOP, MatchCOOP, PopupSevered,  *)
(* COIMode and C.                                                             *)
EXTENDS Integers, Sequences, FiniteSets, TLC
CONSTANT Mutant
VARIABLE dummy
SI == INSTANCE SpecIsolation
C(id, e) == SI!C(id, e)

\* Decisions of the steps; "neg:<id>" negates one (TRUE gates: omits the step).
HistIds == {
  "nav-switch",        \* a navigation response's COOP check sets the swap
  "nav-blank",         \* the first navigation uses the popup check (initial about:blank)
  "blank-inherit",     \* the popup's initial about:blank takes the opener's COOP
  "nav-prune",         \* a navigation removes the forward entries
  "trav-enforce",      \* a re-fetched traversal target gets the COOP check
  "trav-noblank",      \* ... with the non-popup check (the active doc is not initial about:blank)
  "trav-active-bc",    \* ... and, without a swap, the active browsing context
  "restore-reuse-bc",  \* a kept document comes back in its own browsing context
  "restore-keep-coi",  \* ... with its own cross-origin isolation mode
  "ws-unsalvageable"}  \* an open WebSocket makes the document unsalvageable
\* Named misreadings of the traversal step.
NamedMutants == {
  "reevaluate-coop-on-restore",   \* a kept document is COOP-checked against the active doc; a mismatch severs it
  "restore-opener",               \* a re-fetched target is checked against the opener, and rejoins it on a match
  "new-agent-cluster-on-restore"} \* a kept document always comes back in a new group, without opener
\* ws-unsalvageable is a condition, not a TRUE gate: "false:" omits the step.
LocalMutants == {"neg:" \o d : d \in HistIds \ {"ws-unsalvageable"}} \cup {"false:ws-unsalvageable"}
                \cup NamedMutants
AllMutants == SI!MechMutants \cup SI!Mutants \cup SI!FixMutants \cup LocalMutants

\* --- Scenario encoding (gen.py writes the same codes) ----------------------
STq  == <<"popup", "noopener">>
OPq  == <<"unsafe-none", "same-origin-allow-popups", "same-origin", "so+rc">>
RELq == <<"same-origin", "cross-site">>
SEQq == <<"NB", "NBF", "NNB", "NNB2", "NBN">>
\* 0 = navigate to the next document; d # 0 = history.go(d).
SeqOps == <<<<0, -1>>, <<0, -1, 1>>, <<0, 0, -1>>, <<0, 0, -2>>, <<0, -1, 0>>>>
\* x = <<st, op, sq, docs>>; docs[j] = <<rel, coop, ws>> (ws: 1 none, 2 open WebSocket).
Org(r) == IF r = "same-origin" THEN SI!OA ELSE SI!OB
HCOOP(h) == IF h = "so+rc" THEN "same-origin" ELSE h
HCOEP(h) == IF h = "so+rc" THEN "require-corp" ELSE "unsafe-none"
Doc(d) == [o |-> Org(RELq[d[1]]), coop |-> HCOOP(OPq[d[2]]), coep |-> HCOEP(OPq[d[2]]), ws |-> d[3] = 2]
Decode(x) == [st |-> STq[x[1]], op |-> OPq[x[2]], sq |-> SEQq[x[3]], ops |-> SeqOps[x[3]],
              docs |-> [j \in 1..Len(x[4]) |-> Doc(x[4][j])]]
NT(sc) == Cardinality({i \in 1..Len(sc.ops) : sc.ops[i] # 0})

\* --- One response ---------------------------------------------------------
Parsed(r) == SI!ParsedCOOP(r.coop, r.coep, r.o)
Mode(r)   == SI!COIMode(r.coop, r.coep, r.o)
\* cur = [o, coop] (coop parsed): "check if COOP values require a BCG switch".
CheckSwitch(blank, cur, r) ==
  IF blank THEN SI!PopupSevered(cur.coop, cur.o, Parsed(r), r.o)
  ELSE ~SI!MatchCOOP(cur.coop, cur.o, Parsed(r), r.o)

\* --- States ---------------------------------------------------------------
\* st = [es, cur, bcs, ok, how]: es = entries [j, doc], doc = [bc, o, coop, mode];
\* bcs = browsing contexts [opener, mode]; bcs[1] is the one window.open made.
\* ok: the UA choices so far are allowed; how: the last step's kind.
OpR(sc) == [o |-> SI!OA, coop |-> HCOOP(sc.op), coep |-> HCOEP(sc.op)]
Opaque == [scheme |-> "opaque", host |-> "opaque", site |-> "opaque"]
BlankSrc(sc) ==
  IF sc.st = "popup"
  THEN [o |-> SI!OA, coop |-> IF C("blank-inherit", TRUE) THEN Parsed(OpR(sc)) ELSE "unsafe-none"]
  ELSE [o |-> Opaque, coop |-> "unsafe-none"]
BC1(sc) == IF sc.st = "popup" THEN [opener |-> TRUE, mode |-> Mode(OpR(sc))]
           ELSE [opener |-> FALSE, mode |-> "none"]
Active(st) == st.es[st.cur].doc
Src(d) == [o |-> d.o, coop |-> d.coop]
\* A document for response r: in a new browsing context if swap, else in bc.
Place(st, swap, bc, r) ==
  IF swap THEN [bcs |-> Append(st.bcs, [opener |-> FALSE, mode |-> Mode(r)]),
                doc |-> [bc |-> Len(st.bcs) + 1, o |-> r.o, coop |-> Parsed(r), mode |-> Mode(r)]]
  ELSE [bcs |-> st.bcs, doc |-> [bc |-> bc, o |-> r.o, coop |-> Parsed(r), mode |-> st.bcs[bc].mode]]

\* navigate to document j (first: from the initial about:blank, which it replaces).
NavStep(sc, st, j, first) ==
  LET r == sc.docs[j]
      src == IF first THEN BlankSrc(sc) ELSE Src(Active(st))
      abc == IF first THEN 1 ELSE Active(st).bc
      p == Place(st, C("nav-switch", CheckSwitch(C("nav-blank", first), src, r)), abc, r)
      kept == IF first THEN <<>> ELSE IF C("nav-prune", TRUE) THEN SubSeq(st.es, 1, st.cur) ELSE st.es
      es == Append(kept, [j |-> j, doc |-> p.doc])
  IN [es |-> es, cur |-> Len(es), bcs |-> p.bcs, ok |-> st.ok, how |-> IF first THEN "open" ELSE "nav"]

\* history.go(d); hit = the target entry's document was kept (bfcache).
TravStep(sc, st, d, hit) ==
  LET t == st.cur + d
      e == st.es[t]
      r == sc.docs[e.j]
      act == Active(st)
      unsalv == C("ws-unsalvageable", r.ws)
      fresh(swap) == Place(st, swap, act.bc, r)
      p == IF hit THEN
             CASE Mutant = "reevaluate-coop-on-restore" ->
                    IF CheckSwitch(FALSE, Src(act), r) THEN fresh(TRUE) ELSE [bcs |-> st.bcs, doc |-> e.doc]
               [] Mutant = "new-agent-cluster-on-restore" -> fresh(TRUE)
               [] OTHER ->
                    [bcs |-> st.bcs,
                     doc |-> [e.doc EXCEPT !.bc = IF C("restore-reuse-bc", TRUE) THEN e.doc.bc ELSE act.bc,
                                           !.mode = IF C("restore-keep-coi", TRUE) THEN e.doc.mode
                                                    ELSE st.bcs[act.bc].mode]]
           ELSE IF Mutant = "restore-opener" /\ sc.st = "popup" THEN
             IF CheckSwitch(FALSE, Src([o |-> SI!OA, coop |-> Parsed(OpR(sc))]), r)
             THEN fresh(TRUE) ELSE Place(st, FALSE, 1, r)
           ELSE
             LET swap == C("trav-enforce", CheckSwitch(~C("trav-noblank", TRUE), Src(act), r))
             IN Place(st, swap, IF C("trav-active-bc", TRUE) THEN act.bc ELSE e.doc.bc, r)
  IN [es |-> [st.es EXCEPT ![t].doc = p.doc], cur |-> t, bcs |-> p.bcs,
      ok |-> st.ok /\ (hit => ~unsalv), how |-> IF hit THEN "restore" ELSE "refetch"]

RECURSIVE Go(_, _, _, _, _, _)
Go(sc, h, sts, i, nd, k) ==
  IF i > Len(sc.ops) THEN sts
  ELSE LET st == sts[Len(sts)] IN
       IF sc.ops[i] = 0 THEN Go(sc, h, Append(sts, NavStep(sc, st, nd, FALSE)), i + 1, nd + 1, k)
       ELSE Go(sc, h, Append(sts, TravStep(sc, st, sc.ops[i], h[k])), i + 1, nd, k + 1)
Init0(sc) == [es |-> <<>>, cur |-> 0, bcs |-> <<BC1(sc)>>, ok |-> TRUE, how |-> "init"]
\* The states after window.open and after each operation.
Run(sc, h) == Go(sc, h, <<NavStep(sc, Init0(sc), 1, TRUE)>>, 1, 2, 1)
Final(sc, h) == LET s == Run(sc, h) IN s[Len(s)]
Hs(sc) == [1..NT(sc) -> BOOLEAN]
Feasible(sc, h) == Final(sc, h).ok
Fs(sc) == {h \in Hs(sc) : Feasible(sc, h)}

\* --- Observations ---------------------------------------------------------
B2S(b) == IF b THEN "TRUE" ELSE "FALSE"
OpenerOf(st) == st.bcs[Active(st).bc].opener
\* closed: the opener's WindowProxy (bcs[1]) has no active document in the navigable.
Obs1(st, k, cc) ==
  CASE k = "closed" -> {B2S(Active(st).bc # 1)}
    [] k = "opener" -> {B2S(OpenerOf(st))}
    [] k = "coi"    -> (IF "concrete" \in cc THEN {B2S(Active(st).mode = "concrete")} ELSE {})
                       \cup (IF "logical" \in cc THEN {"FALSE"} ELSE {})
    [] k = "hlen"   -> {ToString(Len(st.es))}
Kinds == <<"closed", "opener", "coi", "hlen">>
\* H: the hit vectors the browser showed; values allowed under them.
Use(sc, H) == IF H \cap Fs(sc) # {} THEN H \cap Fs(sc) ELSE Fs(sc)
Allowed(sc, k, cc, H) ==
  CASE k = "hit1" -> {B2S(h[1]) : h \in Fs(sc)}
    [] k = "hit2" -> {B2S(h[2]) : h \in Fs(sc)}
    [] OTHER -> UNION {Obs1(Final(sc, h), k, cc) : h \in Use(sc, H)}
\* Pre-screen vector: for every UA choice vector, feasibility and the observations.
Vec(sc, cc) == [h \in Hs(sc) |-> IF Feasible(sc, h)
                   THEN <<[j \in 1..4 |-> Obs1(Final(sc, h), Kinds[j], cc)]>> ELSE <<>>]

\* --- Sequence properties (over the states of one run) --------------------
Pop(sc) == sc.st = "popup"
OpenerCompat(sc, d) ==
  LET oc == Parsed(OpR(sc)) IN
  \/ d.coop = "unsafe-none" /\ oc \in {"unsafe-none", "same-origin-allow-popups"}
  \/ SI!MatchCOOP(oc, SI!OA, d.coop, d.o)
\* Q1: once the active document is severed from the opener, traversal never rejoins it.
Q1(sc, s) == Pop(sc) => \A i, j \in 1..Len(s) : (i < j /\ ~OpenerOf(s[i])) => ~OpenerOf(s[j])
\* Q2: a document shares the opener's group only if its COOP allows it.
Q2(sc, s) == \A i \in 1..Len(s) : (Pop(sc) /\ OpenerOf(s[i])) => OpenerCompat(sc, Active(s[i]))
\* Q3: an isolated document has COOP same-origin with COEP itself.
Q3(sc, s) == \A i \in 1..Len(s) : Active(s[i]).mode = "concrete" => Active(s[i]).coop = "same-origin-plus-COEP"
\* Q4: a kept document comes back unchanged (browsing context and isolation).
Q4(sc, s) == \A i \in 2..Len(s) : s[i].how = "restore" =>
               Active(s[i]) = s[i - 1].es[s[i].cur].doc
\* Q5: a re-fetched target gets a new browsing context iff it mismatches the active doc.
Q5(sc, s) == \A i \in 2..Len(s) : s[i].how = "refetch" =>
               ((Active(s[i]).bc > Len(s[i - 1].bcs)) <=>
                CheckSwitch(FALSE, Src(Active(s[i - 1])), sc.docs[s[i].es[s[i].cur].j]))
Props == <<"Q1", "Q2", "Q3", "Q4", "Q5">>
Prop(p, sc, s) == CASE p = "Q1" -> Q1(sc, s) [] p = "Q2" -> Q2(sc, s) [] p = "Q3" -> Q3(sc, s)
                    [] p = "Q4" -> Q4(sc, s) [] OTHER -> Q5(sc, s)
\* Q1 restricted to runs without bfcache (every h[k] FALSE).
NoHit(h) == \A k \in DOMAIN h : ~h[k]
===============================================================================
