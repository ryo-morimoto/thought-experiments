----------------------------- MODULE OriginOracle -----------------------------
(* Part 3 of experiments/2026-11-20-browser-semantics-soundness.md: can a   *)
(* spec-derived oracle catch bugs where the browser computed a principal    *)
(* wrongly from clean inputs? Spec steps (HTML "determining the origin",    *)
(* creating a browsing context, window open steps, Window reuse; URL         *)
(* "origin of a URL"; "obtain a site") are the author's reading of the       *)
(* passages quoted in the record. Each bug's computation encodes the root   *)
(* cause stated in its fix CL message; the model does not run browsers.     *)
EXTENDS Naturals, TLC

\* Tuple origins and opaque origins. Opaque origins carry an identity.
A  == [kind |-> "tuple", host |-> "a.test", site |-> "a.test"]
B  == [kind |-> "tuple", host |-> "b.test", site |-> "b.test"]
V  == [kind |-> "tuple", host |-> "v.test", site |-> "v.test"]
Op == [kind |-> "opaque", id |-> 1]
Oq == [kind |-> "opaque", id |-> 2]
Ox == [kind |-> "opaque", id |-> 3]      \* a fresh opaque origin
Null == [kind |-> "null"]                \* no source origin / no URL origin

\* HTML: determining the origin (url kinds: "blank", "srcdoc", "data", "http").
DetermineOrigin(url, urlOrigin, sandboxed, sourceOrigin) ==
  IF sandboxed THEN Ox
  ELSE IF url = "srcdoc" THEN sourceOrigin
  ELSE IF url = "blank" /\ sourceOrigin # Null THEN sourceOrigin
  ELSE IF url = "data" THEN Ox
  ELSE urlOrigin

\* HTML: obtain a site. An opaque origin is its own site.
Site(o) == IF o.kind = "opaque" THEN o ELSE o.site
SpecSameSite(o1, o2) == Site(o1) = Site(o2)

\* HTML: Window reuse when an initial about:blank is replaced.
SpecReuseWindow(isInitialBlank, activeOrigin, newOrigin) ==
  isInitialBlank /\ activeOrigin = newOrigin

\* Each case records the spec inputs and what the buggy and fixed browsers
\* computed, at the level each oracle compares.
Cases == {
  \* CVE-2022-1637: top A embeds iframe B; B calls open("data:...") and the
  \* popup stays on its initial about:blank. Creator is the calling frame (B).
  [bug |-> "CVE-2022-1637", level |-> "origin",
   spec  |-> DetermineOrigin("blank", Null, FALSE, B),
   buggy |-> A,                     \* GetOriginalOpener(): opener's main frame
   fixed |-> B],
  \* CVE-2018-16074: data: documents of sites P and Q (opaque Op, Oq) each
  \* create blob:null/<guid>. Are the two blob documents same-site?
  [bug |-> "CVE-2018-16074", level |-> "site",
   spec  |-> SpecSameSite(Op, Oq),
   buggy |-> TRUE,                  \* both site keys were "blob:"
   fixed |-> FALSE],
  \* CVE-2019-13738: sandbox applied to X's document (opaque), replacing the
  \* non-sandboxed initial about:blank of origin X'. Reuse the Window?
  [bug |-> "CVE-2019-13738", level |-> "derived",
   spec  |-> SpecReuseWindow(TRUE, A, Ox),
   buggy |-> TRUE,                  \* only CSP sandbox flags were checked
   fixed |-> FALSE],
  \* CVE-2024-1671: attacker parent A; a history traversal reuses victim V's
  \* srcdoc entry. Recomputing the origin from the reused entry gives V
  \* (agrees with the browser); the derived invariant "a srcdoc document's
  \* origin is its parent's origin, or opaque" does not hold.
  [bug |-> "CVE-2024-1671", level |-> "origin",
   spec  |-> DetermineOrigin("srcdoc", Null, FALSE, V),
   buggy |-> V,
   fixed |-> V],
  [bug |-> "CVE-2024-1671", level |-> "derived",
   spec  |-> TRUE,                  \* invariant must hold: origin in {parent, opaque}
   buggy |-> V \in {A, Ox},
   fixed |-> A \in {A, Ox}],
  \* CVE-2018-16073: data: iframe restored after tab restore. Origins agree
  \* (opaque); the bug is process placement after the creator was lost.
  [bug |-> "CVE-2018-16073", level |-> "origin",
   spec  |-> DetermineOrigin("data", Null, FALSE, A),
   buggy |-> Ox,
   fixed |-> Ox],
  \* CVE-2018-6165: popup on its initial about:blank keeps the opener's origin
  \* after document.write; the bug is the URL shown in the omnibox.
  [bug |-> "CVE-2018-6165", level |-> "origin",
   spec  |-> DetermineOrigin("blank", Null, FALSE, A),
   buggy |-> A,
   fixed |-> A]
}

Levels == {"origin", "site", "derived"}
\* An oracle at level L compares every case whose level is at most L.
Rank(l) == CASE l = "origin" -> 1 [] l = "site" -> 2 [] l = "derived" -> 3
CaughtAt(L) == {c.bug : c \in {x \in Cases : Rank(x.level) <= Rank(L) /\ x.buggy # x.spec}}
FalseAlarmAt(L) == {c.bug : c \in {x \in Cases : Rank(x.level) <= Rank(L) /\ x.fixed # x.spec}}
AllBugs == {c.bug : c \in Cases}

Report == PrintT(<<"caught",
                   [l \in Levels |-> CaughtAt(l)],
                   "false-alarms", [l \in Levels |-> FalseAlarmAt(l)],
                   "never-caught", AllBugs \ CaughtAt("derived")>>)

\* Expected outcome, checked as invariants.
NoFalseAlarms == \A l \in Levels : FalseAlarmAt(l) = {}
CaughtExpected ==
  /\ CaughtAt("origin")  = {"CVE-2022-1637"}
  /\ CaughtAt("site")    = {"CVE-2022-1637", "CVE-2018-16074"}
  /\ CaughtAt("derived") = {"CVE-2022-1637", "CVE-2018-16074", "CVE-2019-13738", "CVE-2024-1671"}

VARIABLE dummy
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
