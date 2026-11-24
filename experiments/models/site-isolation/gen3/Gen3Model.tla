------------------------------ MODULE Gen3Model -------------------------------
(* gen3/RESULTS.md (tree node C11): what ../SpecIsolation.tla (unedited)      *)
(* plus the steps below allows for one scenario of gen3.py's eight families: *)
(*   X sandbox flags and popups      Y sandbox flags and top navigation      *)
(*   R values carried across redirects (Origin header, Referer)              *)
(*   K CSP violation blockedURI after redirects                              *)
(*   D document.domain and same origin-domain                                *)
(*   N Window reuse when the initial about:blank is replaced                 *)
(*   W worker policy containers (dedicated, shared, blob:)                   *)
(*   F cross-origin cors-mode fetch() under COEP                             *)
(* Each added step is wrapped as G3(id, e), with the same "neg:", "false:"  *)
(* and "true:" mutants as SpecIsolation's C(id, e). Spec anchors are in      *)
(* RESULTS.md. Parameters (not misreadings):                                 *)
(*   OShare  {"ref","copy"}: whether the initial about:blank shares its      *)
(*           creator's origin object, so a later document.domain on the     *)
(*           creator reaches it (HTML sets "creatorOrigin"; it is silent).   *)
(*   RefMay  "may": the UA MAY strip the referrer further (Referrer Policy   *)
(*           "determine request's referrer", step "MAY alter"); "exact": no. *)
EXTENDS Naturals, Sequences, FiniteSets
CONSTANTS Mutant, OShare, RefMay
VARIABLE dummy
SI == INSTANCE SpecIsolation

G3(id, e) ==
  CASE Mutant = "neg:" \o id   -> ~e
    [] Mutant = "false:" \o id -> FALSE
    [] Mutant = "true:" \o id  -> TRUE
    [] OTHER                   -> e
\* Decisions whose condition is not a constant.
G3Ids == {"g3-kw-popups", "g3-kw-top", "g3-kw-topua", "g3-kw-so", "g3-kw-escape",
          "g3-sb-aux", "g3-sb-prop", "g3-sb-origin", "g3-sb-dd", "g3-sb-top", "g3-sb-act",
          "g3-ref-redirect", "g3-taint-sticky", "g3-taint-req", "g3-taint", "g3-org-cors",
          "g3-org-post", "g3-org-rp",
          "g3-od-domain", "g3-od-null", "g3-reuse",
          "g3-w-check", "g3-w-shared",
          "g3-cors", "g3-cors-star", "g3-cors-acac"}
\* Constant-TRUE gates: only "neg:" (= "false:") is a mutant; it omits the step.
G3Const == {"g3-ref-sticky", "g3-csp-hop", "g3-csp-url", "g3-w-blob", "g3-w-own"}
G3Named == {"od-as-origin"}   \* document.domain access compares origins, not origin-domains
G3Mutants == {p \o d : p \in {"neg:", "false:", "true:"}, d \in G3Ids}
             \cup {"neg:" \o d : d \in G3Const} \cup G3Named

Opaque == [scheme |-> "opaque", host |-> "opaque", site |-> "opaque"]
B2S(b) == IF b THEN "TRUE" ELSE "FALSE"
Any == {"TRUE", "FALSE", "opaque", "tuple", "ok", "threw", "skip", "nav", "denied",
        "absent", "null", "self", "full", "origin", "none", "basic", "cors", "error",
        "load", "orig", "cur"}
Min(S) == CHOOSE x \in S : \A y \in S : x <= y

\* --- Sandboxing flags (HTML "parse a sandboxing directive") ----------------
\* sc.sbon: the iframe has a sandbox attribute; sc.sb: its tokens.
Kw(sc, id, t) == G3(id, t \in sc.sb)
Flags(sc) ==
  IF ~sc.sbon THEN {} ELSE
  {"nav", "dd"}
  \cup (IF Kw(sc, "g3-kw-popups", "allow-popups") THEN {} ELSE {"aux"})
  \cup (IF Kw(sc, "g3-kw-top", "allow-top-navigation") THEN {} ELSE {"topnoact"})
  \cup (IF Kw(sc, "g3-kw-top", "allow-top-navigation")
           \/ Kw(sc, "g3-kw-topua", "allow-top-navigation-by-user-activation") THEN {} ELSE {"topact"})
  \cup (IF Kw(sc, "g3-kw-so", "allow-same-origin") THEN {} ELSE {"origin"})
  \cup (IF Kw(sc, "g3-kw-escape", "allow-popups-to-escape-sandbox") THEN {} ELSE {"prop"})
IsOpaque(fl) == G3("g3-sb-origin", "origin" \in fl)
\* document.domain setter: the flag check, then "effective domain is null".
DDThrows(fl) == G3("g3-sb-dd", "dd" \in fl) \/ IsOpaque(fl)

\* --- X: window.open from a sandboxed frame ----------------------------------
Opened(sc) == ~G3("g3-sb-aux", "aux" \in Flags(sc))
PFlags(sc) == IF G3("g3-sb-prop", "prop" \in Flags(sc)) THEN Flags(sc) ELSE {}

\* --- Y: the frame sets top.location (no transient activation) -------------
TopNav(sc) ==
  LET fl == Flags(sc) IN
  IF G3("g3-sb-act", FALSE) THEN "topact" \notin fl
  ELSE ~G3("g3-sb-top", "topnoact" \in fl)

\* --- R: fetch() through redirects ------------------------------------------
\* sc.urls: origins of the URL list; sc.rp: the referrerPolicy init ("" = the
\* policy container's default, strict-origin-when-cross-origin); sc.hrp: the
\* Referrer-Policy header of the first redirect response ("" = none).
RPol(sc, j) ==
  IF j > 1 /\ G3("g3-ref-redirect", sc.hrp # "") THEN sc.hrp
  ELSE IF sc.rp = "" THEN "strict-origin-when-cross-origin" ELSE sc.rp
\* Referrer Policy "determine request's referrer"; src: what request's referrer
\* holds ("full" document URL or its "origin"); its origin is sc.to.
Det(pol, src, cur, to) ==
  CASE pol = "no-referrer" -> "none"
    [] pol = "unsafe-url"  -> src
    [] pol = "same-origin" -> IF SI!SameOrigin(to, cur) THEN src ELSE "none"
    [] OTHER -> IF SI!SameOrigin(to, cur) THEN src
                ELSE IF SI!Secure(to) /\ ~SI!Secure(cur) THEN "none" ELSE "origin"
\* Main fetch sets request's referrer to the result on every hop, so a later
\* hop starts from the earlier (already stripped) value: "g3-ref-sticky".
RECURSIVE RefAt(_, _)
RefAt(sc, j) ==
  LET src == IF j = 1 \/ ~G3("g3-ref-sticky", TRUE) THEN "full" ELSE RefAt(sc, j - 1)
  IN IF src = "none" THEN "none" ELSE Det(RPol(sc, j), src, sc.urls[j], sc.to)
\* Main fetch: basic only while current URL is same origin and tainting basic.
RECURSIVE Taint(_, _)
Taint(sc, j) ==
  LET prev == IF j = 1 THEN "basic" ELSE Taint(sc, j - 1) IN
  IF G3("g3-taint-sticky", prev # "basic") THEN prev
  ELSE IF SI!SameOrigin(sc.urls[j], sc.to) THEN "basic"
  ELSE IF sc.mode = "no-cors" THEN "opaque" ELSE "cors"
\* Fetch "redirect-taint" of the URL list urls[1..n].
RTaint(sc, n) ==
  LET u == sc.urls
      cs == \E i \in 2..n : ~SI!SameSite(u[i], u[i - 1]) /\ G3("g3-taint-req", ~SI!SameSite(sc.to, u[i - 1]))
      ss == \E i \in 2..n : u[i] # u[i - 1] /\ G3("g3-taint-req", sc.to # u[i - 1])
  IN IF cs THEN "cross-site" ELSE IF ss THEN "same-site" ELSE "same-origin"
Ser(sc, n) == IF G3("g3-taint", RTaint(sc, n) # "same-origin") THEN "null" ELSE "self"
NullByRP(pol, cur, to) ==
  CASE pol = "no-referrer" -> TRUE
    [] pol = "same-origin" -> ~SI!SameOrigin(to, cur)
    [] pol = "unsafe-url"  -> FALSE
    [] OTHER -> SI!Secure(to) /\ ~SI!Secure(cur)
\* Fetch "append a request Origin header", at the last hop.
OrgHdr(sc) ==
  LET n == Len(sc.urls) IN
  IF G3("g3-org-cors", Taint(sc, n) = "cors") THEN Ser(sc, n)
  ELSE IF G3("g3-org-post", sc.meth # "GET") THEN
    IF sc.mode # "cors" /\ G3("g3-org-rp", NullByRP(RPol(sc, n), sc.urls[n], sc.to))
    THEN "null" ELSE Ser(sc, n)
  ELSE "absent"
Rank(v) == CASE v = "full" -> 2 [] v = "origin" -> 1 [] OTHER -> 0
RefAllowed(v) == IF RefMay = "exact" THEN {v}
                 ELSE {w \in {"full", "origin", "none"} : Rank(w) <= Rank(v)}

\* --- K: <img> through redirects under CSP img-src --------------------------
\* The pre-request check runs on every hop (main fetch, recursive); the
\* violation's resource is request's url (the first URL).
KBlock(sc) ==
  LET B == {j \in 1..Len(sc.urls) : sc.urls[j] \notin sc.allow
                                     /\ (j = 1 \/ G3("g3-csp-hop", TRUE))}
  IN IF B = {} THEN 0 ELSE Min(B)
KBU(sc) == LET j == KBlock(sc) IN
  IF j = 0 THEN "none" ELSE IF j = 1 \/ G3("g3-csp-url", TRUE) THEN "orig" ELSE "cur"

\* --- D, N: document.domain and origin-domain --------------------------------
\* Every document sends Origin-Agent-Cluster: ?0 (header false).
NoOp(o, top) == SI!DocumentDomainNoOp(SI!KeyKindCtx([self |-> o, top |-> top], "none", "absent", FALSE))
\* HTML "same origin-domain"; "" is a null domain.
SameOD(o1, d1, o2, d2) ==
  IF Mutant = "od-as-origin" THEN SI!SameOrigin(o1, o2)
  ELSE IF G3("g3-od-domain", d1 # "" /\ d1 = d2 /\ o1.scheme = o2.scheme) THEN TRUE
  ELSE G3("g3-od-null", d1 = "" /\ d2 = "") /\ SI!SameOrigin(o1, o2) /\ o1 # Opaque
\* D: the top sets document.domain to its site if sc.set \in {p, both}; the
\* child (sandboxed with allow-scripts allow-same-origin if sc.sbon) to its site
\* if sc.set \in {c, both}.
PDom(sc) == IF sc.set \in {"p", "both"} /\ ~NoOp(sc.to, sc.to) THEN sc.to.site ELSE ""
CThrows(sc) == DDThrows(Flags(sc))
COrig(sc) == IF IsOpaque(Flags(sc)) THEN Opaque ELSE sc.ch
CDom(sc) == IF sc.set \in {"c", "both"} /\ ~CThrows(sc) /\ ~NoOp(sc.ch, sc.to) THEN sc.ch.site ELSE ""
DAccess(sc) == SameOD(sc.to, PDom(sc), COrig(sc), CDom(sc))
\* N: the creator sets document.domain before creating the about:blank, after
\* it, or not; then the about:blank navigates to sc.tgt.
BlankDom(sc, s) ==
  IF NoOp(sc.to, sc.to) THEN ""
  ELSE CASE sc.dd = "before" -> sc.to.site
         [] sc.dd = "after"  -> (IF s = "ref" THEN sc.to.site ELSE "")
         [] OTHER            -> ""
Reuse(sc, s) == G3("g3-reuse", SameOD(sc.to, BlankDom(sc, s), sc.tgt, ""))

\* --- W: workers ----------------------------------------------------------------
\* sc.tc/sc.te: the owner's COOP/COEP; sc.kind: ded, shared, blob (dedicated
\* from a blob: URL); sc.wc: the worker script response's COEP.
OwnerCOEP(sc) == SI!EffectiveCOEP(sc.to, sc.te)
WPol(sc) ==
  IF sc.kind = "blob" THEN (IF G3("g3-w-blob", TRUE) THEN OwnerCOEP(sc) ELSE "unsafe-none")
  ELSE sc.wc
\* HTML "check a global object's embedder policy" (dedicated workers only).
WLoad(sc) == sc.kind = "shared"
             \/ ~G3("g3-w-check", OwnerCOEP(sc) \in SI!CompatCOI /\ WPol(sc) \notin SI!CompatCOI)
\* Concrete choice: a dedicated worker is in its owner's agent cluster; a
\* shared worker's new cluster gets a mode iff its own COEP is compatible.
WCOI(sc) == IF sc.kind = "shared" THEN G3("g3-w-shared", WPol(sc) \in SI!CompatCOI)
            ELSE SI!CrossOriginIsolated(sc.tc, sc.te, sc.to)
WFetch(sc) ==
  SI!FetchResultPC(SI!TopCtx(sc.to), IF G3("g3-w-own", TRUE) THEN WPol(sc) ELSE OwnerCOEP(sc),
                   "no-cors", [origin |-> sc.xo, corp |-> "none", creds |-> FALSE])

\* --- F: cross-origin cors-mode fetch ------------------------------------------
\* Fetch "CORS check"; acao "origin" echoes the request Origin, "origin-acac"
\* also sends Access-Control-Allow-Credentials: true.
CORSOk(sc) ==
  sc.acao # "none"
  /\ (G3("g3-cors-star", sc.acao = "*" /\ sc.cred # "include")
      \/ (sc.acao \in {"origin", "origin-acac"}
          /\ (sc.cred # "include" \/ G3("g3-cors-acac", sc.acao = "origin-acac"))))
FRes(sc) ==
  LET r == SI!FetchResultCtx(SI!TopCtx(sc.to), sc.te, "cors",
             [origin |-> sc.tg, corp |-> sc.corp, creds |-> sc.cred = "include"])
  IN IF r = "cors" THEN (IF G3("g3-cors", CORSOk(sc)) THEN "cors" ELSE "error") ELSE r

\* --- rows ----------------------------------------------------------------------
Kinds(sc) ==
  CASE sc.fam = "X" -> <<"pop", "porig", "pdd", "fdd">>
    [] sc.fam = "Y" -> <<"tnav">>
    [] sc.fam = "R" -> <<"org", "ref", "res">>
    [] sc.fam = "K" -> <<"img", "bu">>
    [] sc.fam = "D" -> <<"pc", "cp", "cset">>
    [] sc.fam = "N" -> <<"reuse">>
    [] sc.fam = "W" -> <<"load", "coi", "fx">>
    [] OTHER        -> <<"r">>
OkThrew(b) == IF b THEN "threw" ELSE "ok"
XRow(sc, k) ==
  CASE k = "pop"   -> {B2S(Opened(sc))}
    [] k = "fdd"   -> {OkThrew(DDThrows(Flags(sc)))}
    [] ~Opened(sc) -> Any
    [] k = "porig" -> {IF IsOpaque(PFlags(sc)) THEN "opaque" ELSE "tuple"}
    [] OTHER       -> {OkThrew(DDThrows(PFlags(sc)))}
COIRow(b, cc) == (IF "concrete" \in cc THEN {B2S(b)} ELSE {}) \cup (IF "logical" \in cc THEN {"FALSE"} ELSE {})
Allowed(sc, k, cc) ==
  CASE sc.fam = "X" -> XRow(sc, k)
    [] sc.fam = "Y" -> {IF ~sc.sbon \/ TopNav(sc) THEN "nav" ELSE "threw"}
    [] sc.fam = "R" -> (CASE k = "org" -> {OrgHdr(sc)}
                          [] k = "ref" -> RefAllowed(RefAt(sc, Len(sc.urls)))
                          [] OTHER     -> {Taint(sc, Len(sc.urls))})
    [] sc.fam = "K" -> (IF k = "img" THEN {IF KBlock(sc) = 0 THEN "load" ELSE "error"} ELSE {KBU(sc)})
    [] sc.fam = "D" -> (IF k = "cset"
                        THEN {IF sc.set \in {"c", "both"} THEN OkThrew(CThrows(sc)) ELSE "skip"}
                        ELSE {IF DAccess(sc) THEN "ok" ELSE "denied"})
    [] sc.fam = "N" -> {B2S(Reuse(sc, s)) : s \in OShare}
    [] sc.fam = "W" -> (CASE k = "load" -> {IF WLoad(sc) THEN "load" ELSE "error"}
                          [] ~WLoad(sc) -> Any
                          [] k = "coi"  -> COIRow(WCOI(sc), cc)
                          [] OTHER      -> {WFetch(sc)})
    [] OTHER -> {FRes(sc)}
Vec(sc, cc) == [j \in 1..Len(Kinds(sc)) |-> Allowed(sc, Kinds(sc)[j], cc)]
===============================================================================
