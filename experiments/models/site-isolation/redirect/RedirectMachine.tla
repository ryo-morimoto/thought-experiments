---------------------------- MODULE RedirectMachine ----------------------------
(* redirect/RESULTS.md: RedirectSeq's chain (unmutated) as a state machine.   *)
(* The state is the opener policy enforcement result; one step per response  *)
(* (HopStep), then the switch decision (Final). The space is RedirectSpace.tla *)
(* (written by gen.py). Checked with RedirectMachine.cfg.                     *)
EXTENDS RedirectSeq, RedirectSpace
VARIABLES x, res, k, swapped
vars == <<x, res, k, swapped, dummy>>
SC == Decode(x)
Init == /\ x \in {Space[i] : i \in 1..Len(Space)} /\ dummy = 0
        /\ res = Src1(Decode(x)) /\ k = 0 /\ swapped = "pending"
HopStep == /\ k < Len(SC.rs)
           /\ res' = Enforce(Blank1(SC), res, SC.rs[k + 1])
           /\ k' = k + 1 /\ UNCHANGED <<x, swapped, dummy>>
Final == /\ k = Len(SC.rs) /\ swapped = "pending"
         /\ swapped' = B2S(C("final-swap", res.needs)) /\ UNCHANGED <<x, res, k, dummy>>
Done == swapped # "pending" /\ UNCHANGED vars
Next == HopStep \/ Final \/ Done
Spec == Init /\ [][Next]_vars /\ WF_vars(HopStep \/ Final)
\* The flag after k responses is exactly "some step among the first k mismatched".
FlagIsAnyStep == res.needs = (\E j \in 1..k : StepCheck(SC, j))
\* The flag never goes back to FALSE.
Sticky == [][res.needs => res'.needs]_vars
\* Every chain reaches the decision.
Decides == <>(swapped # "pending")
\* The state machine agrees with the functional Swap1.
FinalAgrees == swapped # "pending" => swapped = B2S(Swap1(SC))
PropsHold == swapped # "pending" => (P1(SC) /\ P1c(SC) /\ P2(SC) /\ P3(SC) /\ P4(SC))
\* Expected to fail: severing is not decided by responses vs the source alone.
P2cHolds == swapped # "pending" => P2c(SC)
===============================================================================
