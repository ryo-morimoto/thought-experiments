---- MODULE ExtensionHooks ----
\* Extension points of HTML/Fetch as hooks around the modelled fetch
\* (experiments/2026-11-21-informal-extension.md). Another specification may
\* add behaviour at a hook. Two hook kinds:
\*   monotone   - the hook can only turn the result into a network error
\*                (block), combined conjunctively with the existing checks;
\*   substitute - the hook can supply its own response instead
\*                (a response-supplying hook).
\* The contract HookReads says what the hook's decision may depend on:
\*   "declared" - only the requester and what the target declared
\*                (Declared(mode, r) and r.origin);
\*   "any"      - also undeclared parts of the response (its body).
\* Properties quantify over every hook decision allowed by the contract, so
\* they hold for every extension that satisfies it.
EXTENDS SpecIsolation

CONSTANT HookReads

\* A pair of responses that the page must not tell apart (same origin, same
\* declarations): r2 differs from r1 only in the body, and only when the body
\* is not declared.
Twin(mode, r1, b) ==
  IF mode = "cors" /\ r1.acao THEN r1 ELSE [r1 EXCEPT !.body = b]

\* -- monotone hook ----------------------------------------------------------
ResultM(o, r, blk) ==
  IF blk THEN "error" ELSE FetchResult(o, "require-corp", "no-cors", r)
ObserveM(o, coep, mode, r, blk) ==
  IF blk THEN <<"error">> ELSE Observe(o, coep, mode, r)

\* Access control survives any block-only hook, whatever it reads.
ACMonotone ==
  \A o \in Origins, r \in Responses, blk \in BOOLEAN :
    (Secure(o) /\ ResultM(o, r, blk) = "opaque") =>
      \/ r.corp = "cross-origin"
      \/ r.corp = "same-site" /\ SameSite(o, r.origin)

\* Flow: the hook's decisions for the two twins must be equal if it reads
\* only declared inputs; otherwise they may differ.
FlowMonotone ==
  \A o \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"},
     r1 \in FlowResponses, b \in Bodies, k1, k2 \in BOOLEAN :
    LET r2 == Twin(mode, r1, b) IN
    (~SameOrigin(o, r1.origin) /\ (HookReads = "declared" => k1 = k2)) =>
      ObserveM(o, coep, mode, r1, k1) = ObserveM(o, coep, mode, r2, k2)

\* -- substituting hook -----------------------------------------------------
\* The hook answers with "none" (no substitution), with its own body "own",
\* or with a body it read from the target. Reading the target's body is
\* allowed only under "any", or under "declared" when the body is declared.
SubChoices(mode, r) ==
  {"none", "own"} \cup
    (IF HookReads = "any" \/ (mode = "cors" /\ r.acao) THEN {r.body} ELSE {})
ObserveS(o, coep, mode, r, s) ==
  IF s = "none" THEN Observe(o, coep, mode, r) ELSE <<"read", s>>

\* Access control: the target's body is read only through its CORS opt-in.
ACSubstitute ==
  \A o \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"}, r \in FlowResponses :
    \A s \in SubChoices(mode, r) :
      (~SameOrigin(o, r.origin) /\ ObserveS(o, coep, mode, r, s) = <<"read", r.body>>) => r.acao

\* Flow: under "declared" the hook makes the same choice for both twins
\* (a choice of the same kind: none, own, or the declared body).
Kind(s, r) == IF s \in {"none", "own"} THEN s ELSE "target"
FlowSubstitute ==
  \A o \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"},
     r1 \in FlowResponses, b \in Bodies :
    LET r2 == Twin(mode, r1, b) IN
    \A s1 \in SubChoices(mode, r1), s2 \in SubChoices(mode, r2) :
      (~SameOrigin(o, r1.origin)
       /\ (HookReads = "declared" => Kind(s1, r1) = Kind(s2, r2))) =>
        ObserveS(o, coep, mode, r1, s1) = ObserveS(o, coep, mode, r2, s2)

PrintHooks == PrintT(<<"hooks", HookReads,
                       <<"ac-monotone", ACMonotone>>,
                       <<"flow-monotone", FlowMonotone>>,
                       <<"ac-substitute", ACSubstitute>>,
                       <<"flow-substitute", FlowSubstitute>>>>)
====
