------------------------------ MODULE HoldMutants -----------------------------
(* holdout/RESULTS.md: the registered mutant sets.                          *)
(*   NOld = GenModel's 55 (gen/GenAllowed.tla Ms)                            *)
(*   ROld = RedirectSeq!AllMutants, 65 (redirect/RedirectAllowed.tla Ms)     *)
(*   X    = the extension: "false:" of the 27 SpecIsolation decisions that   *)
(*          are not FixIds, and "true:" of all 33 (SI!C supports both);      *)
(*   RX   = X plus "false:" and "true:" of RedirectSeq's 8 RedirectIds.      *)
(* NMs = NOld \cup X (115), RMs = ROld \cup RX (141).                         *)
EXTENDS Naturals, Sequences, FiniteSets
VARIABLE dummy
G(m) == INSTANCE GenModel WITH Mutant <- m
R(m) == INSTANCE RedirectSeq WITH Mutant <- m
SI0 == INSTANCE SpecIsolation WITH Mutant <- "none"
NOld == G("none")!SI!MechMutants \cup G("none")!SI!Mutants \cup G("none")!SI!FixMutants
ROld == R("none")!AllMutants
X == {"false:" \o d : d \in SI0!DecisionIds \ SI0!FixIds} \cup {"true:" \o d : d \in SI0!DecisionIds}
RX == X \cup {"false:" \o d : d \in R("none")!RedirectIds} \cup {"true:" \o d : d \in R("none")!RedirectIds}
NMs == NOld \cup X
RMs == ROld \cup RX
===============================================================================
