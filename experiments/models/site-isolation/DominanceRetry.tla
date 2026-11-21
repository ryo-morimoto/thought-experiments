---- MODULE DominanceRetry ----
\* Dominance condition (experiments/2026-11-21-dominance-declassification.md):
\* every path that delivers cross-origin bytes passes the base CORP check,
\* whatever a block-only extension hook does.
\* Paths modelled:
\*  - a no-cors subresource fetch whose HTTP-network-or-cache fetch may retry
\*    internally (e.g. after a 401, the retry carries credentials and may get a
\*    response with different headers);
\*  - after a block, the page retries by navigating an iframe to the URL
\*    (a navigation request: CORP check with forNavigation, and the child's
\*    COEP must not be unsafe-none under a require-corp parent).
\* Fetch "HTTP fetch" runs the CORP check on the response returned by
\* HTTP-network-or-cache fetch, i.e. after any internal retry (Placement
\* "after"). Placement "before" is a hypothetical spec that checks only the
\* first response.
EXTENDS SpecIsolation

CONSTANT Placement

OptIn(o, r) ==
  \/ r.corp = "cross-origin"
  \/ r.corp = "same-site" /\ SameSite(o, r.origin)

\* Subresource path. first: the first response; second: the response to the
\* internal retry (used when retried is TRUE). blk: a block-only hook.
SubArrives(o, first, second, retried, blk) ==
  LET delivered == IF retried THEN second ELSE first
      checked   == IF Placement = "after" THEN delivered ELSE first
  IN /\ ~blk
     /\ ~SameOrigin(o, delivered.origin)
     /\ CorpCheck(o, "require-corp", checked, FALSE) = "allowed"

ACSub ==
  \A o \in Origins, first, second \in Responses, retried, blk \in BOOLEAN :
    LET delivered == IF retried THEN second ELSE first IN
    (Secure(o) /\ first.origin = second.origin
     /\ SubArrives(o, first, second, retried, blk)) => OptIn(o, delivered)

\* Navigation path, taken after a block (or directly). cc: the child's COEP.
NavArrives(o, r, cc, blk) ==
  /\ ~blk
  /\ ~SameOrigin(o, r.origin)
  /\ CorpCheck(o, "require-corp", r, TRUE) = "allowed"
  /\ cc # "unsafe-none"

ACNav ==
  \A o \in Origins, r \in Responses, cc \in COEPs, blk \in BOOLEAN :
    (Secure(o) /\ NavArrives(o, r, cc, blk)) => (OptIn(o, r) /\ cc # "unsafe-none")

SubWitness ==
  CHOOSE x \in Origins \X Responses \X Responses :
    /\ Secure(x[1]) /\ x[2].origin = x[3].origin
    /\ SubArrives(x[1], x[2], x[3], TRUE, FALSE)
    /\ ~OptIn(x[1], x[3])

PrintDom == PrintT(<<"dominance", Placement,
                     <<"ac-sub", ACSub>>, <<"ac-nav", ACNav>>,
                     <<"witness", IF ACSub THEN "none" ELSE SubWitness>>>>)
====
