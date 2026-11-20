----------------------------- MODULE FetchStorage -----------------------------
(* Which definition of "permitted" makes a spec-conforming browser pass and  *)
(* a buggy one fail? From experiments/2026-11-20-browser-semantics-soundness.md *)
(* The compromised renderer runs site A, locked to A, in a frame whose        *)
(* top-level site is topSite. Fetch/ORB/CORP are heavily simplified:          *)
(*   a response reaches the renderer if it is same-site, CORS-allowed, or a   *)
(*   no-cors image without a CORP same-origin header (ORB blocks no-cors HTML).*)
EXTENDS Naturals

CONSTANTS
  OrbBug,           \* network service lets no-cors HTML through
  ValidateTopSite   \* browser checks the top-level site in a claimed StorageKey

Sites == {"A", "V"}
Kinds == {"image", "html"}
Modes == {"no-cors", "cors"}
Corps == {"none", "same-origin"}

VARIABLES topSite, delivered, storage
vars == <<topSite, delivered, storage>>

SpecDelivers(r) ==
  \/ r.site = "A"
  \/ r.mode = "cors" /\ r.acao
  \/ r.mode = "no-cors" /\ r.kind = "image" /\ r.corp = "none"

BrowserDelivers(r) ==
  \/ SpecDelivers(r)
  \/ OrbBug /\ r.mode = "no-cors" /\ r.kind = "html" /\ r.corp = "none"

Responses == [site : Sites, kind : Kinds, mode : Modes, corp : Corps, acao : BOOLEAN]

Init ==
  /\ topSite \in Sites          \* A embedded under A (first party) or under V
  /\ delivered = {}
  /\ storage = {}

\* One delivery per behavior: the properties below are per element, so this
\* loses no violation and keeps the state space small.
Fetch(r) ==
  /\ delivered = {}
  /\ BrowserDelivers(r)
  /\ delivered' = delivered \cup {r}
  /\ UNCHANGED <<topSite, storage>>

\* Renderer claims a StorageKey <<origin, top-level site>>.
OpenStorage(o, t) ==
  /\ o = "A"                                  \* jail check on the origin
  /\ ValidateTopSite => t = topSite           \* partition check
  /\ storage' = storage \cup {<<o, t>>}
  /\ UNCHANGED <<topSite, delivered>>

Next ==
  \/ \E r \in Responses : Fetch(r)
  \/ \E o, t \in Sites : OpenStorage(o, t)

Spec == Init /\ [][Next]_vars

\* Candidate definitions of "permitted".
FetchOriginOnly   == \A r \in delivered : r.site = "A"
FetchPermits      == \A r \in delivered : SpecDelivers(r)
StorageOriginOnly == \A k \in storage : k[1] = "A"
StorageKeyPermits == \A k \in storage : k = <<"A", topSite>>
===============================================================================
