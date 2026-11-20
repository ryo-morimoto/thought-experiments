---------------------------- MODULE NestedHistory ----------------------------
(* Toy model of CVE-2024-1671 (Chromium issue 41487933): an about:srcdoc     *)
(* session history entry of a victim document is reused in a child frame of *)
(* the document that replaced it, so the srcdoc document commits with the   *)
(* victim's origin under an attacker parent.                                *)
(*                                                                          *)
(* Encoded from HTML:                                                       *)
(*  - "get session history entries": for a non-top navigable, return the   *)
(*    entries of the nested history (in some document state's nested        *)
(*    histories, reached from the traversable's entries) whose id equals    *)
(*    the navigable's id.                                                   *)
(*  - "determine the origin": about:srcdoc -> sourceOrigin; about:blank     *)
(*    with sourceOrigin -> sourceOrigin; otherwise the URL's origin.        *)
(*  - location.replace of the parent creates a new document state whose     *)
(*    nested histories are fresh; its new child navigable has a new id.     *)
(*                                                                          *)
(* Simplifications: the parent is the top-level traversable and is only     *)
(* ever replaced (its session history has exactly one entry); one child     *)
(* slot; no sandboxing; no forward traversal; the child's own document      *)
(* state has no nested histories; "back" moves the child one step in the   *)
(* list returned by the selection function.                                 *)
(*                                                                          *)
(* Mode = "spec": entries are selected from the CURRENT parent document     *)
(*   state's nested history for the child's id.                             *)
(* Mode = "bug": the browser keeps a per-frame-slot pointer to the nested   *)
(*   history the child last used (owner) and its step index; neither is     *)
(*   reset by the parent's replacement (mimicking the stale                 *)
(*   was_on_initial_empty_document during a speculative RFH commit), so     *)
(*   selection reuses the child's previous nested history.                  *)
EXTENDS Naturals, Sequences

CONSTANTS Mode, MaxEntries, MaxDS

Origins == {"V", "A"}          \* V = victim, A = attacker
URLs    == {"blank", "srcdoc", "x"}
Navs    == 1..MaxDS            \* one child navigable id per parent document

VARIABLES
  dstate,    \* Seq of parent document states: [origin, nested : Navs -> Seq(entry id)]
  entries,   \* Seq of child entries: [url, src (sourceOrigin), uorigin (URL's origin), origin (doc state origin)]
  topDS,     \* document state of the top's (single) session history entry
  childNav,  \* id of the child navigable of the top's active document
  childIdx,  \* child's current index into its selected entry list
  childDoc,  \* child's active document: [url, origin, entry]
  owner      \* bug mode only: [ds, nav] whose nested history the browser thinks is the child's
vars == <<dstate, entries, topDS, childNav, childIdx, childDoc, owner>>

ParentOrigin == dstate[topDS].origin

\* HTML "determine the origin" (sandboxing omitted).
DetermineOrigin(url, src, uorigin) ==
  IF url = "srcdoc" THEN src
  ELSE IF url = "blank" /\ src # "none" THEN src
  ELSE uorigin

\* HTML "get session history entries" for a non-top navigable. The top's
\* session history is <<entry with document state topDS>>; child documents
\* have no nested histories, so the walk stops at depth one.
SpecEntries(nav) ==
  IF dstate[topDS].nested[nav] # <<>> THEN dstate[topDS].nested[nav] ELSE <<>>

SelectedEntries ==
  IF Mode = "spec" THEN SpecEntries(childNav)
  ELSE dstate[owner.ds].nested[owner.nav]

Range(s) == {s[i] : i \in DOMAIN s}

NewEntry(url, src, uorigin) ==
  [url |-> url, src |-> src, uorigin |-> uorigin,
   origin |-> DetermineOrigin(url, src, uorigin)]

Init ==
  /\ dstate = << [origin |-> "V",
                  nested |-> [n \in Navs |-> IF n = 1 THEN <<1>> ELSE <<>>]] >>
  /\ entries = << NewEntry("blank", "V", "none") >>
  /\ topDS = 1
  /\ childNav = 1
  /\ childIdx = 1
  /\ childDoc = [url |-> "blank", origin |-> "V", entry |-> 1]
  /\ owner = [ds |-> 1, nav |-> 1]

\* Child navigates (push) to about:srcdoc or to a URL "x" of origin o.
\* srcdoc's sourceOrigin is the parent's active document's origin.
NavigateChild(url, o) ==
  /\ Len(entries) < MaxEntries
  /\ url \in {"srcdoc", "x"}
  /\ url = "srcdoc" => o = ParentOrigin
  /\ LET e    == NewEntry(url, IF url = "srcdoc" THEN ParentOrigin ELSE "none",
                          IF url = "x" THEN o ELSE "none")
         eid  == Len(entries) + 1
         loc  == IF Mode = "spec" THEN [ds |-> topDS, nav |-> childNav] ELSE owner
         hist == dstate[loc.ds].nested[loc.nav]
         kept == SubSeq(hist, 1, IF childIdx <= Len(hist) THEN childIdx ELSE Len(hist))
     IN /\ entries' = Append(entries, e)
        /\ dstate' = [dstate EXCEPT ![loc.ds].nested[loc.nav] = Append(kept, eid)]
        /\ childIdx' = Len(kept) + 1
        /\ childDoc' = [url |-> url, origin |-> e.origin, entry |-> eid]
        /\ UNCHANGED <<topDS, childNav, owner>>

\* location.replace of the parent to a document of origin o: new document
\* state with fresh nested histories; its iframe is a new child navigable
\* whose initial about:blank entry inherits o.
ReplaceParent(o) ==
  /\ Len(dstate) < MaxDS
  /\ Len(entries) < MaxEntries
  /\ LET nav == childNav + 1
         eid == Len(entries) + 1
     IN /\ dstate' = Append(dstate, [origin |-> o,
                         nested |-> [n \in Navs |-> IF n = nav THEN <<eid>> ELSE <<>>]])
        /\ entries' = Append(entries, NewEntry("blank", o, "none"))
        /\ topDS' = Len(dstate) + 1
        /\ childNav' = nav
        /\ childDoc' = [url |-> "blank", origin |-> o, entry |-> eid]
        /\ IF Mode = "spec"
             THEN childIdx' = 1
             ELSE UNCHANGED childIdx      \* stale step and owner survive the replace
        /\ UNCHANGED owner

\* history.back() for the child: go to the previous entry in the selected
\* list; the document is recreated with its document state's origin.
Back ==
  LET L == SelectedEntries IN
  /\ childIdx > 1
  /\ childIdx <= Len(L)
  /\ LET eid == L[childIdx - 1]
         e   == entries[eid]
     IN /\ childIdx' = childIdx - 1
        /\ childDoc' = [url |-> e.url, origin |-> e.origin, entry |-> eid]
  /\ UNCHANGED <<dstate, entries, topDS, childNav, owner>>

Next ==
  \/ \E url \in {"srcdoc", "x"}, o \in Origins : NavigateChild(url, o)
  \/ \E o \in Origins : ReplaceParent(o)
  \/ Back

Spec == Init /\ [][Next]_vars

\* ---- Properties ----

\* Target property: a srcdoc child has its parent's active document's origin.
SrcdocOriginOK ==
  childDoc.url = "srcdoc" => childDoc.origin = ParentOrigin

\* Oracle 1: recompute the origin with "determine the origin" from the entry
\* the child is showing (sourceOrigin = that entry's document state's origin).
DetermineOriginOK ==
  LET e == entries[childDoc.entry] IN
  childDoc.origin = DetermineOrigin(e.url, e.src, e.uorigin)

\* Oracle 2: the child's active entry is among the entries that
\* "get session history entries" returns for the child navigable.
SelectionOK ==
  childDoc.entry \in Range(SpecEntries(childNav))

\* Coverage: every srcdoc-origin violation is also a selection violation.
SelectionCoversOrigin == SelectionOK => SrcdocOriginOK
=============================================================================
