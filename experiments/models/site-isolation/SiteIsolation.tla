---------------------------- MODULE SiteIsolation ----------------------------
(* Toy interface model of browser-process enforcement under a compromised   *)
(* renderer. Parts of claim D' from                                         *)
(* experiments/2026-11-20-browser-semantics-soundness.md:                   *)
(*   G'  guards on renderer IPC (jail check on claimed origins)             *)
(*   I*  integrity of trusted state (history written only from commits)     *)
(*   L   process-allocation policy (where a restored subframe is placed)    *)
(*   J   interleavings: check-then-use of a data request (AtomicCheckUse)   *)
(* Teardown and message queues other than the data request are not modelled.*)
EXTENDS Naturals, FiniteSets

CONSTANTS
  ValidateReplaceState,  \* I*: browser checks replaceState URL against committed
  BuggyRestore,          \* L bug: restored subframe placed in its parent's process
  AttackerIPC,           \* FALSE = honest traces only (no compromised renderer)
  UnlockedHosting,       \* L bug: site A runs in an unlocked process; a later commit locks it
  AtomicCheckUse         \* FALSE = data request is checked, then served after a gap

Sites  == {"A", "V"}          \* A = attacker site, V = victim site
None   == "None"
Procs  == {"p1", "p2"}
Frames == {"top", "sub"}      \* "sub" is an iframe inside "top"

VARIABLES lock, committed, history, frameProc, access, ipcAccess, hosted, pending,
          violations  \* accesses not permitted by the lock at the time they happened
vars == <<lock, committed, history, frameProc, access, ipcAccess, hosted, pending,
          violations>>

\* An unlocked process may host any site (no isolated-site list in this model).
Permits(l, s) == l = None \/ l = s
Record(p, s, l) == IF Permits(l, s) THEN violations ELSE violations \cup {<<p, s>>}

\* Attacker code persists in any process that has ever run a site-A document.
Compromised(p) == AttackerIPC /\ "A" \in hosted[p]

Init ==
  /\ lock      = [p \in Procs  |-> None]
  /\ committed = [f \in Frames |-> None]
  /\ history   = [f \in Frames |-> None]
  /\ frameProc = [f \in Frames |-> None]
  /\ access    = {}
  /\ ipcAccess = {}
  /\ hosted    = [p \in Procs  |-> {}]
  /\ pending   = {}
  /\ violations = {}

\* Correct L: a process already locked to s, or a fresh unlocked one.
Placeable(s) == {p \in Procs : lock[p] = s \/ lock[p] = None}

Commit(f, s, p) ==
  /\ committed' = [committed EXCEPT ![f] = s]
  /\ history'   = [history   EXCEPT ![f] = s]
  /\ frameProc' = [frameProc EXCEPT ![f] = p]
  /\ LET nl == IF lock[p] = None /\ ~(UnlockedHosting /\ s = "A")
                 THEN [lock EXCEPT ![p] = s] ELSE lock
     IN /\ lock' = nl
        /\ violations' = Record(p, s, nl[p])
  /\ access'    = access \cup {<<p, s>>}
  /\ hosted'    = [hosted EXCEPT ![p] = @ \cup {s}]
  /\ UNCHANGED <<ipcAccess, pending>>

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
  /\ UNCHANGED <<lock, committed, frameProc, access, ipcAccess, hosted, pending,
                 violations>>

\* Browser reload: trusts history[f] as the frame's own URL, so it stays in
\* the same process (sound only if I* holds).
Reload(f) ==
  /\ committed[f] # None
  /\ Commit(f, history[f], frameProc[f])

\* G': compromised renderer requests data of a claimed origin; jail check.
RequestData(f, s) ==
  /\ AtomicCheckUse
  /\ frameProc[f] # None
  /\ Compromised(frameProc[f])
  /\ lock[frameProc[f]] = s                      \* guard; otherwise kill
  /\ access'    = access    \cup {<<frameProc[f], s>>}
  /\ ipcAccess' = ipcAccess \cup {<<frameProc[f], s>>}
  /\ violations' = Record(frameProc[f], s, lock[frameProc[f]])
  /\ UNCHANGED <<lock, committed, history, frameProc, hosted, pending>>

\* J: the same request split in two. The check passes for the frame's origin
\* now; the data is served later for the frame's origin at that time.
BeginRequest(f) ==
  /\ ~AtomicCheckUse
  /\ frameProc[f] # None
  /\ Compromised(frameProc[f])
  /\ lock[frameProc[f]] = committed[f]           \* guard at check time
  /\ pending' = pending \cup {<<frameProc[f], f>>}
  /\ UNCHANGED <<lock, committed, history, frameProc, access, ipcAccess, hosted,
                 violations>>

CompleteRequest(r) ==
  /\ r \in pending
  /\ access'    = access    \cup {<<r[1], committed[r[2]]>>}
  /\ ipcAccess' = ipcAccess \cup {<<r[1], committed[r[2]]>>}
  /\ pending'   = pending \ {r}
  /\ violations' = Record(r[1], committed[r[2]], lock[r[1]])
  /\ UNCHANGED <<lock, committed, history, frameProc, hosted>>

Next ==
  \E f \in Frames, s \in Sites :
     \/ Navigate(f, s)
     \/ Restore(s)
     \/ ReplaceState(f, s)
     \/ Reload(f)
     \/ RequestData(f, s)
     \/ BeginRequest(f)
  \/ \E r \in pending : CompleteRequest(r)

Spec == Init /\ [][Next]_vars

\* S: every data access by process p was permitted by p's lock at that time.
S == violations = {}
\* G' alone: every access granted over IPC is permitted by the current lock.
GuardSound == \A x \in ipcAccess : Permits(lock[x[1]], x[2])
\* S' (b): lock assignment conforms to L: a locked process only ever ran
\* documents of its lock site.
LockConforms == \A p \in Procs : lock[p] # None => hosted[p] \subseteq {lock[p]}
\* A counterexample to this is a state where S holds but S' (b) does not.
SImpliesConform == S => LockConforms
==============================================================================
