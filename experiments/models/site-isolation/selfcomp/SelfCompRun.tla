------------------------------ MODULE SelfCompRun -----------------------------
(* Self-composition of SelfCompORB as a state machine (2-safety check).    *)
EXTENDS SelfCompORB
CONSTANTS K,       \* number of queries
          Ctl,     \* attacker control: "none", "ends", "all"
          Policy   \* escape hatch (see Hatch in SelfCompORB)
\* Two runs, same attacker, secrets s1 # s2 with equal escape-hatch value.
\* While the observation histories are equal, a deterministic strategy
\* must pick the same next query in both runs, so one shared q per round
\* is exactly "some adaptive strategy". SCNI: histories stay equal for K
\* rounds (a 2-safety property; a violation is a distinguishing strategy).
\* h1, h2: observation sequences; lastq: the query of the last round.
VARIABLES s1, s2, h1, h2, lastq
scvars == <<dummy, s1, s2, h1, h2, lastq>>
SCInit == /\ dummy = 0
          /\ s1 \in Secrets /\ s2 \in Secrets /\ s1 # s2
          /\ Hatch(Policy, Ctl, s1) = Hatch(Policy, Ctl, s2)
          /\ h1 = E /\ h2 = E /\ lastq = "none"
SCNext == /\ Len(h1) < K /\ h1 = h2
          /\ \E q \in Queries(Ctl) :
               /\ h1' = Append(h1, Obs(q, s1))
               /\ h2' = Append(h2, Obs(q, s2))
               /\ lastq' = <<[i \in 0..N |-> q.a[i]], q.ms>>
          /\ UNCHANGED <<dummy, s1, s2>>
SCSpec == SCInit /\ [][SCNext]_scvars
SCNI == h1 = h2
===============================================================================
