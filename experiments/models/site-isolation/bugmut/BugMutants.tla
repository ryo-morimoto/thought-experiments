------------------------------ MODULE BugMutants ------------------------------
(* bugmut/RESULTS.md (tree node C9). Mutants taken from public, fixed browser *)
(* defects (bugs.tsv), as C-style ids that the unedited models already       *)
(* interpret: SpecIsolation's C(id, e) handles "neg:", "false:" and "true:"; *)
(* RedirectSeq reuses it; Gen2Model's G2 handles "neg:" and "false:" only.    *)
(* No operator of the models is changed here: this module only names sets.   *)
EXTENDS Naturals, Sequences, FiniteSets
VARIABLE dummy
SI == INSTANCE SpecIsolation WITH Mutant <- "none"

\* Earlier runs' mutants (the author's): 33 neg:, 16 named, 6 false: fixes,
\* 9 gen2 mutants, 10 redirect-local mutants.
G2Author == {"neg:g2-sb-opaque", "neg:g2-pp-self", "neg:g2-noopener", "neg:g2-coop-secure",
             "neg:g2-blank-coop", "false:g2-sb-opaque", "false:g2-pp-self",
             "false:g2-noopener", "false:g2-coop-secure"}
RedirectIds == {"hop-accumulate", "hop-switch", "hop-update", "hop-blank", "hop-coep",
                "blank-inherit", "final-swap", "hop-same-entry"}
RedirectAuthor == {"neg:" \o d : d \in RedirectIds} \cup {"first-hop-only", "final-hop-only"}
Author == SI!MechMutants \cup SI!Mutants \cup SI!FixMutants \cup G2Author \cup RedirectAuthor

\* Type M1 of bugs.tsv ("check omitted"): the most frequent model-step type in
\* the defects, while the author's mutants were almost all negations. Its two
\* C-style forms on every decision that no earlier run used:
\*   true:<id>   the check the decision makes is skipped (always passes)
\*   false:<id>  the step the decision guards is skipped
BugTrue  == {"true:" \o d : d \in SI!DecisionIds}
BugFalse == {"false:" \o d : d \in SI!DecisionIds \ SI!FixIds}
\* Redirect decisions whose condition is not the constant TRUE (for the others
\* false: equals neg: and true: equals the unmutated model). Type M6 ("stale
\* value across steps": the per-hop check skipped or forced).
BugRedirect == {"true:hop-blank", "false:hop-blank", "true:hop-switch", "false:hop-switch",
                "true:final-swap", "false:final-swap"}
New == BugTrue \cup BugFalse \cup BugRedirect

\* Instance level: model-step defects of bugs.tsv whose step is in the model.
\* Each maps onto a mutant that already exists (column new_mutant_id).
BugInstance == {"false:mc-ancestor", "neg:hop-update", "first-hop-only",
                "false:g2-sb-opaque", "false:g2-pp-self"}

All == New \cup Author
===============================================================================
