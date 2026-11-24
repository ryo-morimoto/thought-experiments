------------------------------ MODULE Compose -------------------------------
(* compose/RESULTS.md: the monolithic cross-check of Contracts.tla. The same *)
(* steps run as one state machine over a browsing context group (up to      *)
(* MaxDocs documents), with real agent clusters (keyed by kind, origin or    *)
(* scheme+site, and the DIP when KeyHasDIP) and a real historical key map.  *)
(* Every reachable state is checked against the global property directly    *)
(* (PropInv) and against the contracts (GInv), with no induction.             *)
(* Our key is a tuple, not SpecIsolation's Key (which confuses an apex host  *)
(* with its site name; adequacy/RESULTS.md section 1).                       *)
EXTENDS Contracts
CONSTANT MaxDocs
VARIABLES gm, docs, clusters, hist
cvars == <<gm, docs, clusters, hist, dummy>>

KeyVal(o, kind, dip) ==
  <<kind, IF kind = "origin" THEN o ELSE [scheme |-> o.scheme, site |-> o.site],
    IF KeyHasDIP THEN dip ELSE "-">>
ClAt(k) ==
  IF \E c \in clusters : c.k = k
  THEN LET c == CHOOSE c \in clusters : c.k = k IN [ex |-> TRUE, dip |-> c.dip, mode |-> c.mode]
  ELSE NoCl
NewCl(d) == [k |-> KeyVal(d.self, d.kind, d.dip), dip |-> d.dip, mode |-> d.cmode]

CInit ==
  /\ dummy = 0
  /\ \E o \in Origins, coop \in COOPs, coep \in COEPs, dip \in DIPs, oac \in BOOLEAN :
       LET t == TopStep(o, coop, coep, dip, oac) IN
       /\ gm = t.g /\ docs = <<t.d>> /\ clusters = {NewCl(t.d)}
       /\ hist = [x \in Origins |-> IF x = o THEN t.hist ELSE "absent"]

Add(res, cl) ==
  /\ res.ok
  /\ docs' = Append(docs, res.d)
  /\ clusters' = IF cl.ex THEN clusters ELSE clusters \cup {NewCl(res.d)}
  /\ hist' = [hist EXCEPT ![res.d.self] = res.hist]
  /\ UNCHANGED <<gm, dummy>>

\* The key kind does not depend on the cluster, so it is computed first
\* (with NoCl), then the cluster with that key is looked up.
Child ==
  /\ Len(docs) < MaxDocs
  /\ \E i \in 1..Len(docs), r \in ChildResp, cc \in COEPs, oac \in BOOLEAN :
       LET h  == hist[r.origin]
           k0 == ChildStep(gm, docs[i], r, cc, oac, h, NoCl)
           cl == ClAt(KeyVal(r.origin, k0.d.kind, "none"))
       IN Add(ChildStep(gm, docs[i], r, cc, oac, h, cl), cl)
Popup ==
  /\ Len(docs) < MaxDocs
  /\ \E i \in 1..Len(docs), rs \in Chains, oac \in BOOLEAN :
       LET f  == rs[Len(rs)]
           h  == hist[f.o]
           k0 == PopupStep(gm, docs[i], rs, oac, h, NoCl)
           cl == ClAt(KeyVal(f.o, k0.d.kind, "none"))
       IN Add(PopupStep(gm, docs[i], rs, oac, h, cl), cl)
CNext == Child \/ Popup

PropInv == \A i \in 1..Len(docs), s \in Responses : Prop(docs[i], s)
GInv == /\ \A i \in 1..Len(docs) : Gdoc(gm, docs[i])
        /\ \A c \in clusters : G_CL(gm, [ex |-> TRUE, dip |-> c.dip, mode |-> c.mode])
        /\ \A o \in Origins : G_HIST(gm, hist[o])
\* F_AC's self-loop through time: an origin keeps one key kind in a group.
KeyConsistent == \A i, j \in 1..Len(docs) : docs[i].self = docs[j].self => docs[i].kind = docs[j].kind
===============================================================================
