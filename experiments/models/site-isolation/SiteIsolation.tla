---------------------------- MODULE SiteIsolation ----------------------------
(* Toy interface model of browser-process enforcement under a compromised   *)
(* renderer. Parts of claim D' from                                         *)
(* experiments/2026-11-20-browser-semantics-soundness.md:                   *)
(*   G'  guards on renderer IPC (jail check on claimed origins)             *)
(*   I*  integrity of trusted state (history written only from commits)     *)
(*   L   process-allocation policy (where a restored subframe is placed)    *)
(* J (interleavings, teardown) is not modelled: every action is atomic.     *)
EXTENDS Naturals, FiniteSets

CONSTANTS
  ValidateReplaceState,  \* I*: browser checks replaceState URL against committed
  BuggyRestore,          \* L bug: restored subframe placed in its parent's process
  AttackerIPC            \* FALSE = honest traces only (no compromised renderer)

Sites  == {"A", "V"}          \* A = attacker site, V = victim site
None   == "None"
Procs  == {"p1", "p2"}
Frames == {"top", "sub"}      \* "sub" is an iframe inside "top"

VARIABLES lock, committed, history, frameProc, access, ipcAccess
vars == <<lock, committed, history, frameProc, access, ipcAccess>>

Compromised(p) == AttackerIPC /\ lock[p] = "A"

Init ==
  /\ lock      = [p \in Procs  |-> None]
  /\ committed = [f \in Frames |-> None]
  /\ history   = [f \in Frames |-> None]
  /\ frameProc = [f \in Frames |-> None]
  /\ access    = {}
  /\ ipcAccess = {}

\* Correct L: a process already locked to s, or a fresh unlocked one.
Placeable(s) == {p \in Procs : lock[p] = s \/ lock[p] = None}

Commit(f, s, p) ==
  /\ committed' = [committed EXCEPT ![f] = s]
  /\ history'   = [history   EXCEPT ![f] = s]
  /\ frameProc' = [frameProc EXCEPT ![f] = p]
  /\ lock'      = IF lock[p] = None THEN [lock EXCEPT ![p] = s] ELSE lock
  /\ access'    = access \cup {<<p, s>>}
  /\ UNCHANGED ipcAccess

\* Browser-initiated navigation; the site comes from the network (trusted).
Navigate(f, s) ==
  /\ f = "sub" => committed["top"] # None
  /\ \E p \in Placeable(s) : Commit(f, s, p)

\* Back/forward-cache restore of the subframe (L decides the process).
Restore(s) ==
  /\ committed["top"] # None
  /\ IF BuggyRestore
       THEN Commit("sub", s, frameProc["top"])
       ELSE \E p \in Placeable(s) : Commit("sub", s, p)

\* Compromised renderer claims a new same-document URL for frame f.
ReplaceState(f, s) ==
  /\ frameProc[f] # None
  /\ Compromised(frameProc[f])
  /\ ValidateReplaceState => s = committed[f]   \* otherwise: kill, no effect
  /\ history' = [history EXCEPT ![f] = s]
  /\ UNCHANGED <<lock, committed, frameProc, access, ipcAccess>>

\* Browser reload: trusts history[f] as the frame's own URL, so it stays in
\* the same process (sound only if I* holds).
Reload(f) ==
  /\ committed[f] # None
  /\ Commit(f, history[f], frameProc[f])

\* G': compromised renderer requests data of a claimed origin; jail check.
RequestData(f, s) ==
  /\ frameProc[f] # None
  /\ Compromised(frameProc[f])
  /\ lock[frameProc[f]] = s                      \* guard; otherwise kill
  /\ access'    = access    \cup {<<frameProc[f], s>>}
  /\ ipcAccess' = ipcAccess \cup {<<frameProc[f], s>>}
  /\ UNCHANGED <<lock, committed, history, frameProc>>

Next ==
  \E f \in Frames, s \in Sites :
     \/ Navigate(f, s)
     \/ Restore(s)
     \/ ReplaceState(f, s)
     \/ Reload(f)
     \/ RequestData(f, s)

Spec == Init /\ [][Next]_vars

\* S: every data access by process p is permitted by p's lock.
S == \A x \in access : lock[x[1]] = x[2]
\* G' alone: every access granted over IPC passed the jail check.
GuardSound == \A x \in ipcAccess : lock[x[1]] = x[2]
==============================================================================
