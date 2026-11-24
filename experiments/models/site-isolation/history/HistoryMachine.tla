---------------------------- MODULE HistoryMachine -----------------------------
(* history/RESULTS.md: HistorySeq's runs (unmutated) as a state machine. The  *)
(* state is (scenario, UA bfcache choices h, history state st, next op i);    *)
(* one step per navigation (NavA) or traversal (TravA). Space: HistorySpace   *)
(* (gen.py). Checked with HistoryMachine.cfg; HistoryMachine-Q1.cfg is       *)
(* expected to fail (bfcache restore rejoins the opener).                    *)
EXTENDS HistorySeq, HistorySpace
VARIABLES x, h, st, i, nd, k
vars == <<x, h, st, i, nd, k, dummy>>
SC == Decode(Space[x])
Init == /\ x \in 1..Len(Space) /\ dummy = 0
        /\ h \in Hs(Decode(Space[x]))
        /\ st = NavStep(Decode(Space[x]), Init0(Decode(Space[x])), 1, TRUE)
        /\ i = 1 /\ nd = 2 /\ k = 1
NavA == /\ i <= Len(SC.ops) /\ SC.ops[i] = 0
        /\ st' = NavStep(SC, st, nd, FALSE) /\ i' = i + 1 /\ nd' = nd + 1
        /\ UNCHANGED <<x, h, k, dummy>>
TravA == /\ i <= Len(SC.ops) /\ SC.ops[i] # 0
         /\ st' = TravStep(SC, st, SC.ops[i], h[k]) /\ i' = i + 1 /\ k' = k + 1
         /\ UNCHANGED <<x, h, nd, dummy>>
Done == i > Len(SC.ops) /\ UNCHANGED vars
Next == NavA \/ TravA \/ Done
Spec == Init /\ [][Next]_vars /\ WF_vars(NavA \/ TravA)
\* State invariants (on runs whose UA choices are allowed so far).
Q2Inv == st.ok => ((Pop(SC) /\ OpenerOf(st)) => OpenerCompat(SC, Active(st)))
Q3Inv == st.ok => (Active(st).mode = "concrete" => Active(st).coop = "same-origin-plus-COEP")
\* The machine agrees with the functional Run/Final.
FinalAgrees == i > Len(SC.ops) => st = Final(SC, h)
\* A kept document comes back unchanged; a re-fetched one is COOP-checked.
RestoreKeeps == [][(i' # i /\ st'.how = "restore") => Active(st') = st.es[st'.cur].doc]_vars
RefetchChecks == [][(i' # i /\ st'.how = "refetch") =>
                    ((Active(st').bc > Len(st.bcs)) <=> CheckSwitch(FALSE, Src(Active(st)), SC.docs[st'.es[st'.cur].j]))]_vars
\* Q1: severed stays severed. Holds without bfcache hits; fails with them.
NoRejoinRefetch == [][(st'.ok /\ NoHit(h) /\ Pop(SC) /\ ~OpenerOf(st)) => ~OpenerOf(st')]_vars
NoRejoin == [][(st'.ok /\ Pop(SC) /\ ~OpenerOf(st)) => ~OpenerOf(st')]_vars
Decides == <>(i > Len(SC.ops))
===============================================================================
