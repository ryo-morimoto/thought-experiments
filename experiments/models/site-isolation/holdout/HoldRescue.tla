------------------------------ MODULE HoldRescue ------------------------------
(* holdout/RESULTS.md: classification check K2 of the registration (added   *)
(* after it, for scoring only). For each out-of-model row of browser b, is   *)
(* the observed set inside the allowed set of mutant RescueM?                *)
EXTENDS HoldAllowed
CONSTANTS RescueM
PrintRescue == \A b \in Browsers :
  PrintT(<<"rescue", CfgName, b, RescueM, Cardinality(Out(b)),
           Cardinality({r \in Out(b) : Rows[r][b] \subseteq A(RescueM, r)}),
           Cardinality({r \in Inside(b) : ~(Rows[r][b] \subseteq A(RescueM, r))})>>)
===============================================================================
