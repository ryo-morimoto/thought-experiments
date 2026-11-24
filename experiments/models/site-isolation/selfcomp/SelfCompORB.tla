---------------------------- MODULE SelfCompORB ------------------------------
(* experiments/2026-11-24-selfcomp-orb-leak.md (tree node B5).              *)
(* How much of a secret does the ORB verdict (whatwg/fetch PR #1442, as     *)
(* modelled in ../ORBExtension.tla) reveal when the attacker controls part  *)
(* of the response body and repeats queries adaptively?                     *)
(*                                                                          *)
(* Body = A0 s1 A1 s2 ... sN AN. Secret bit si is one byte: 1 -> a quote    *)
(* (q), 0 -> a letter (a). Ai are attacker-reflected snippets; which Ai the *)
(* attacker sets is the constant-free parameter ctl:                        *)
(*   "none" all Ai empty (the server's own body)                           *)
(*   "ends" A0 and AN (reflected prefix/suffix)                            *)
(*   "all"  every Ai (attacker fields interleaved with secret fields)      *)
(* Snippets are one byte from {q, /, n} (n = newline), or empty; A0 may    *)
(* also be g, a magic byte that sniffs as an image.                         *)
(* "parses as JS and not JSON" is computed by a lexer-level abstraction:    *)
(* strings "..", line comments // .. newline, a raw newline inside a string *)
(* is a syntax error, code bytes always compose. JSON = one string literal  *)
(* with optional surrounding whitespace. The first-1024-byte sniff class is *)
(* "img" iff the body starts with g (the whole toy body fits in 1024 bytes; *)
(* secret bytes never form a signature).                                    *)
(* ORBAllows from ../ORBExtension.tla is reused unchanged.                 *)
(*****************************************************************************)
EXTENDS ORBExtension

CONSTANTS N,       \* secret length in bits
          Mech     \* "pr" = PR #1442 ORB; "sniffonly" = ORB without step 15

Secrets == [1..N -> {0, 1}]
Byte(b) == IF b = 1 THEN "q" ELSE "a"
E == <<>>
Snips  == {E, <<"q">>, <<"/">>, <<"n">>}
Snips0 == Snips \cup {<<"g">>}

\* --- queries ------------------------------------------------------------
Ctls == {"none", "ends", "all"}
Allowed(ctl, i) ==
  CASE ctl = "none" -> {E}
    [] ctl = "ends" -> IF i = 0 THEN Snips0 ELSE IF i = N THEN Snips ELSE {E}
    [] ctl = "all"  -> IF i = 0 THEN Snips0 ELSE Snips
Fills(ctl) == {f \in [0..N -> Snips0] : \A i \in 0..N : f[i] \in Allowed(ctl, i)}
Queries(ctl) == [a : Fills(ctl), ms : MediaStates]
Empty == [i \in 0..N |-> E]

RECURSIVE BodyFrom(_, _, _)
BodyFrom(a, s, i) == IF i > N THEN E ELSE <<Byte(s[i])>> \o a[i] \o BodyFrom(a, s, i + 1)
Body(a, s) == a[0] \o BodyFrom(a, s, 1)

\* --- lexer-level JS / JSON ----------------------------------------------
Step(st, c) ==
  CASE st = "err"  -> "err"
    [] st = "code" -> (IF c = "q" THEN "str" ELSE IF c = "/" THEN "cmt" ELSE "code")
    [] st = "str"  -> (IF c = "q" THEN "code" ELSE IF c = "n" THEN "err" ELSE "str")
    [] st = "cmt"  -> (IF c = "n" THEN "code" ELSE "cmt")
RECURSIVE LexFrom(_, _, _)
LexFrom(b, i, st) == IF i > Len(b) THEN st ELSE LexFrom(b, i + 1, Step(st, b[i]))
IsJS(b) == LexFrom(b, 1, "code") \in {"code", "cmt"}
IsJSON(b) ==
  LET idx == {i \in 1..Len(b) : b[i] # "n"} IN
  IF idx = {} THEN FALSE ELSE
  LET lo == CHOOSE i \in idx : \A j \in idx : i <= j
      hi == CHOOSE i \in idx : \A j \in idx : i >= j
  IN /\ lo < hi /\ b[lo] = "q" /\ b[hi] = "q"
     /\ \A j \in (lo + 1)..(hi - 1) : b[j] \notin {"q", "n"}
Parse(b) == IF IsJSON(b) THEN "json" ELSE IF IsJS(b) THEN "js" ELSE "neither"
Sniff(b)  == IF Len(b) > 0 /\ b[1] = "g" THEN "img" ELSE "text"

\* --- observation: the ORB verdict on a cross-origin no-cors fetch -------
\* Response: no CORP, requester without require-corp, so the CORP check
\* passes and the page sees exactly the verdict (error vs opaque).
\* Leaky header combination (ORB-NOTES JS witness): mime "block" (e.g.
\* text/html, application/json), no nosniff, 200.
Hdr0 == <<"block", FALSE, "200">>
Rec(h, b) == [mime |-> h[1], nosniff |-> h[2], status |-> h[3],
              body |-> [secret |-> "x", head |-> Sniff(b),
                        parse |-> IF Mech = "sniffonly" THEN "neither" ELSE Parse(b)]]
ObsH(h, q, s) == IF ORBAllows(q.ms, Rec(h, Body(q.a, s))) THEN "opaque" ELSE "error"
Obs(q, s) == ObsH(Hdr0, q, s)

\* --- counting: max number of secret classes after k adaptive queries -----
\* A predicate is the set of secrets on which a query answers "opaque".
PredsH(h, ctl) == {{s \in Secrets : ObsH(h, q, s) = "opaque"} : q \in Queries(ctl)}
Preds(ctl) == PredsH(Hdr0, ctl)
BitPreds == {{s \in Secrets : s[i] = 1} : i \in 1..N}   \* ideal bit oracle
AnyPreds == SUBSET Secrets                               \* any binary oracle
SetMax(S) == CHOOSE m \in S : \A x \in S : x <= m
\* Best(P, k, T): an adaptive strategy is a decision tree of depth k whose
\* inner nodes are predicates in P; its classes are its non-empty leaves.
\* Best is the maximum over all such trees (equivalently, over strategies
\* that choose each query as a function of the observations so far).
RECURSIVE Best(_, _, _)
Best(P, k, T) ==
  IF T = {} THEN 0 ELSE IF k = 0 THEN 1 ELSE
  LET sp == {T \cap p : p \in P} \ {{}, T}
      bound == IF Cardinality(T) < 2^k THEN Cardinality(T) ELSE 2^k
  IN IF sp = {} THEN 1
     ELSE IF \E x \in sp : Best(P, k - 1, x) + Best(P, k - 1, T \ x) = bound THEN bound
     ELSE SetMax({Best(P, k - 1, x) + Best(P, k - 1, T \ x) : x \in sp})
\* Unbounded k: secrets that no query separates.
Kernel(P) == Cardinality({{p \in P : s \in p} : s \in Secrets})
KernelParts(P) == {{t \in Secrets : \A p \in P : (s \in p) = (t \in p)} : s \in Secrets}

\* --- declassification policies (escape hatches, delimited release) -------
\* A policy is a function of the secret alone. It holds for ctl iff two
\* secrets with the same escape-hatch value give the same observation on
\* every query; by induction on k this is the same as: equal observation
\* sequences under every adaptive strategy and every k.
FixedVerdict(s) == [ms \in MediaStates |-> Obs([a |-> Empty, ms |-> ms], s)]
Hatch(pol, ctl, s) ==
  CASE pol = "nothing"     -> 0
    [] pol = "fixedverdict" -> FixedVerdict(s)            \* verdict of the server's own body
    [] pol = "sniff"       -> Sniff(Body(Empty, s))        \* 1024-byte sniff class only
    [] pol = "sniffparse"  -> <<Sniff(Body(Empty, s)), Parse(Body(Empty, s))>>
    [] pol = "kernel"      -> {p \in Preds(ctl) : s \in p} \* minimal policy that holds
    [] pol = "secret"      -> s
Policies == {"nothing", "fixedverdict", "sniff", "sniffparse", "kernel", "secret"}
DR(pol, ctl) ==
  \A s1, s2 \in Secrets :
    Hatch(pol, ctl, s1) = Hatch(pol, ctl, s2) =>
      \A q \in Queries(ctl) : Obs(q, s1) = Obs(q, s2)
\* The ORB-NOTES "declare the verdict bit" form: the declared value is the
\* observation itself. It is a fixed function of the secret only if it does
\* not depend on the attacker's bytes.
VerdictIsSecretFn(ctl) ==
  \A s \in Secrets, q1, q2 \in Queries(ctl) :
    q1.ms = q2.ms => Obs(q1, s) = Obs(q2, s)
HatchClasses(pol, ctl) == Cardinality({Hatch(pol, ctl, s) : s \in Secrets})

\* Header combinations (server's choice) under which some query separates secrets.
LeakyHdrs == {h \in HeaderCombos : Kernel(PredsH(h, "all")) > 1}

PrintCounts == PrintT(<<"selfcomp", "N", N, "Mech", Mech,
  [c \in Ctls |-> <<"preds", Cardinality(Preds(c)),
                    "k", [k \in 1..N |-> Best(Preds(c), k, Secrets)],
                    "kernel", Kernel(Preds(c)),
                    "verdict-is-secret-fn", VerdictIsSecretFn(c),
                    "DR", [p \in Policies |-> DR(p, c)],
                    "hatch-classes", [p \in Policies |-> HatchClasses(p, c)]>>],
  <<"bit-oracle", [k \in 1..N |-> Best(BitPreds, k, Secrets)]>>,
  <<"any-oracle", IF N <= 3 THEN [k \in 1..N |-> Best(AnyPreds, k, Secrets)] ELSE "skipped">>,
  <<"leaky-headers", IF N = 2 THEN LeakyHdrs ELSE "skipped">>,
  <<"ends-merged", {c \in KernelParts(Preds("ends")) : Cardinality(c) > 1}>>>>)

=============================================================================
