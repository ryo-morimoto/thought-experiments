------------------------------ MODULE Gen2Model -------------------------------
(* gen2/RESULTS.md: what ../SpecIsolation.tla (unedited) allows for one     *)
(* scenario of gen2.py's four families (P popup, O Origin-Agent-Cluster,    *)
(* S sandboxed iframe, C top-level CORP and images). SpecIsolation's        *)
(* operators are used as they are. Steps SpecIsolation lacks are added here *)
(* and wrapped as G2(id, e), with the same "neg:"/"false:" mutants as C:    *)
(*   g2-sb-opaque    sandboxed origin flag gives an opaque origin           *)
(*   g2-pp-self      cross-origin-isolated feature, default allowlist self  *)
(*   g2-noopener     noopener creates a new top-level traversable           *)
(*   g2-coop-secure  obtain an opener policy: non-secure -> unsafe-none    *)
(*   g2-blank-coop   the popup's initial about:blank takes the opener COOP *)
(* OACParam is not a misreading: "spec" is the HTML text (requestsOAC only  *)
(* for ?1); "7617" is whatwg/html#7617 (unmerged): an absent header also    *)
(* requests origin keying in a secure context, ?0 keeps site keying.        *)
EXTENDS Naturals, Sequences
CONSTANTS Mutant, OACParam
VARIABLE dummy
SI == INSTANCE SpecIsolation

G2(id, e) ==
  CASE Mutant = "neg:" \o id   -> ~e
    [] Mutant = "false:" \o id -> FALSE
    [] OTHER                   -> e
G2Ids == {"g2-sb-opaque", "g2-pp-self", "g2-noopener", "g2-coop-secure", "g2-blank-coop"}
\* "neg:g2-blank-coop" equals "false:g2-blank-coop" (its condition is TRUE).
G2Mutants == {"neg:" \o d : d \in G2Ids} \cup {"false:" \o d : d \in G2Ids \ {"g2-blank-coop"}}

Opaque == [scheme |-> "opaque", host |-> "opaque", site |-> "opaque"]
B2S(b) == IF b THEN "TRUE" ELSE "FALSE"
Any == {"TRUE", "FALSE", "loaded", "blocked", "basic", "cors", "opaque", "error", "load",
        "tuple"}
Img(x) == IF x \in {"basic", "opaque"} THEN "load" ELSE "error"

\* --- P: popup severing ------------------------------------------------------
\* sc.oo opener origin (top-level), sc.oc its COOP, sc.po / sc.pc the popup's.
PSev(sc) ==
  LET blank == IF G2("g2-blank-coop", TRUE) THEN sc.oc ELSE "unsafe-none"
      pc    == IF G2("g2-coop-secure", ~SI!Secure(sc.po)) THEN "unsafe-none" ELSE sc.pc
  IN IF G2("g2-noopener", sc.mode = "noopener") THEN TRUE
     ELSE SI!PopupSevered(blank, sc.oo, pc, sc.po)

\* --- O: agent cluster keys ---------------------------------------------------
HB(h) == h = "?1" \/ (OACParam = "7617" /\ h = "absent")
OK(sc) ==
  LET cm == IF sc.coi THEN SI!COIMode("same-origin", "require-corp", sc.o0) ELSE "none"
      c1 == [self |-> sc.o1, top |-> sc.o0]
      k0 == SI!KeyKindCtx(SI!TopCtx(sc.o0), cm, "absent", HB(sc.h[1]))
      k1 == SI!KeyKindCtx(c1, cm, "absent", HB(sc.h[2]))
      k2 == SI!KeyKindCtx(c1, cm, k1, HB(sc.h[3]))
  IN <<k0, k1, k2>>
\* document.domain set on both, then synchronous access top -> child 1.
ODD(sc) == LET k == OK(sc) IN
  ~SI!DocumentDomainNoOp(k[1]) /\ ~SI!DocumentDomainNoOp(k[2])
  /\ SI!Key(sc.o0, k[1]) = SI!Key(sc.o1, k[2])

\* --- S: sandboxed iframe -----------------------------------------------------
SOrig(sc) == IF G2("g2-sb-opaque", sc.sb = "scripts") THEN Opaque ELSE sc.co
SCtx(sc) == [self |-> SOrig(sc), top |-> sc.to]
SNav(sc) == SI!NavChild(SI!TopCtx(sc.to), SI!EffectiveCOEP(sc.to, sc.te),
                        [origin |-> sc.co, corp |-> sc.corp, creds |-> TRUE], sc.ce)
SCOIConcrete(sc) ==
  SI!CrossOriginIsolated(sc.tc, sc.te, sc.to) /\ G2("g2-pp-self", SI!SameOrigin(SOrig(sc), sc.to))
\* fetch() defaults to credentials "same-origin"; <img> sends credentials.
SFetch(sc, tgt, corp, dest, served) ==
  SI!FetchResultDest(SCtx(sc), sc.ce, "no-cors", dest,
    [origin |-> tgt, corp |-> corp,
     creds |-> IF dest = "image" THEN TRUE ELSE SI!SameOrigin(SOrig(sc), tgt)], served)

\* --- C: top-level fetch() and <img> ---------------------------------------
CRes(sc) ==
  LET r == [sc.r EXCEPT !.creds = IF sc.dest = "img" THEN TRUE ELSE SI!SameOrigin(sc.to, sc.r.origin)]
  IN IF sc.dest = "fetch" THEN SI!FetchResultCtx(SI!TopCtx(sc.to), sc.te, "no-cors", r)
     ELSE Img(SI!ImageResult(sc.to, sc.te, r, sc.served))

\* --- rows ----------------------------------------------------------------------
Kinds(sc) ==
  CASE sc.fam = "P" -> <<"sev">>
    [] sc.fam = "O" -> <<"g0", "g1", "g2", "dd">>
    [] sc.fam = "S" -> <<"load", "coi", "sec", "orig", "fself", "fx", "fhttp", "ihttp">>
    [] OTHER        -> <<"r">>
SRow(sc, k, cc) ==
  CASE k = "coi"   -> (IF "concrete" \in cc THEN {B2S(SCOIConcrete(sc))} ELSE {})
                                  \cup (IF "logical" \in cc THEN {"FALSE"} ELSE {})
                [] k = "sec"   -> {B2S(SI!SecureCtx(SCtx(sc)))}
                [] k = "orig"  -> {IF SOrig(sc) = Opaque THEN "opaque" ELSE "tuple"}
                [] k = "fself" -> {SFetch(sc, sc.co, "none", "fetch", TRUE)}
                [] k = "fx"    -> {SFetch(sc, sc.xo, "none", "fetch", TRUE)}
                [] k = "fhttp" -> {SFetch(sc, sc.xh, "none", "fetch", TRUE)}
                [] k = "ihttp" -> {Img(SFetch(sc, sc.xh, "cross-origin", "image", TRUE))}
\* Allowed values of row kind k over COIChoice in cc. A sandbox row of a
\* child the model does not load is unconstrained (its load row decides).
Allowed(sc, k, cc) ==
  CASE sc.fam = "P" -> {B2S(PSev(sc))}
    [] sc.fam = "O" ->
         IF k = "dd" THEN {B2S(ODD(sc))}
         ELSE {B2S(SI!OriginAgentCluster(OK(sc)[CASE k = "g0" -> 1 [] k = "g1" -> 2 [] OTHER -> 3]))}
    [] sc.fam = "S" ->
         IF k = "load" THEN {IF SNav(sc) = "loaded" THEN "loaded" ELSE "blocked"}
         ELSE IF SNav(sc) # "loaded" THEN Any
         ELSE SRow(sc, k, cc)
    [] OTHER -> {CRes(sc)}
Vec(sc, cc) == [j \in 1..Len(Kinds(sc)) |-> Allowed(sc, Kinds(sc)[j], cc)]
===============================================================================
