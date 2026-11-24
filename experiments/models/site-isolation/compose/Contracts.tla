------------------------------ MODULE Contracts ------------------------------
(* compose/RESULTS.md, for experiments/2026-11-24-cross-fragment-assume-      *)
(* guarantee.md (tree node D2). Assume-guarantee contracts between the        *)
(* fragments of ../SpecIsolation.tla, ../DIPExtension.tla and                 *)
(* ../redirect/RedirectSeq.tla (all used unedited), and the stepwise          *)
(* (temporal-induction) check of the circular rule.                           *)
(*                                                                            *)
(* A state is one browsing context group: its COI mode g (fixed when the     *)
(* group is created), its documents, its agent clusters and its historical   *)
(* agent cluster key map. A step commits one document (top-level, child, or  *)
(* popup through 0..1 redirects). Each fragment's guarantee is a predicate on *)
(* a committed document (Gdoc) or on a cluster / map entry. The stepwise      *)
(* check: from ANY pre-state element satisfying all guarantees (not only     *)
(* reachable ones), the step's new document satisfies every guarantee. With  *)
(* Init satisfying them, induction over steps gives []G; then G => Prop.      *)
(* A step reads one earlier document (parent or opener), g, one map entry    *)
(* and the cluster with the new document's key, so one pre-document          *)
(* suffices (existing elements are never changed: append-only frame).        *)
(*                                                                            *)
(* Choices not in the modules reused (marked in RESULTS.md):                 *)
(*  - KeyHasDIP: whether the agent cluster key carries the document's DIP.   *)
(*    No reused fragment states it (DIPExtension has no agent clusters).    *)
(*  - A DIP-isolated document's own COI mode (COIModeD) is the mode passed to *)
(*    KeyKindCtx and given to the cluster it creates.                         *)
(*  - DIP only on top-level documents (DIPExtension is top-level only).      *)
(*  - cap (crossOriginIsolated capability) = cluster mode concrete /\ PP,     *)
(*    PP = Gen2's g2-pp-self (default allowlist 'self', no allow attribute). *)
EXTENDS DIPExtension, FiniteSets
CONSTANT KeyHasDIP
RS == INSTANCE RedirectSeq

Modes  == {"none", "concrete"}
PCOOPs == COOPs \cup {"same-origin-plus-COEP"}
Kinds  == {"site", "origin"}
SOC    == "same-origin-plus-COEP"

DocSpace == [self : Origins, top : Origins, pcoep : COEPs, dip : DIPs, coopP : PCOOPs,
             kind : Kinds, cmode : Modes, ppok : BOOLEAN, cap : BOOLEAN, isTop : BOOLEAN]
Ctx(d) == [self |-> d.self, top |-> d.top]

\* --- Guarantees, one per fragment --------------------------------------------
\* F_PC  (obtain an embedder policy; secure context from the top-level URL)
G_PC(g, d)  == ~SecureCtx(Ctx(d)) => d.pcoep = "unsafe-none"
\* F_DIP (obtain a document isolation policy)
G_DIP(g, d) == d.dip # "none" => d.isTop /\ Secure(d.self)
\* F_BCG (COOP parsing, group COI mode, popup matching via RedirectSeq)
G_BCG(g, d) == d.isTop => (d.top = d.self /\ ((d.coopP = SOC) <=> (g = "concrete")))
\* F_MEM (who can be in a concrete group: COOP match for popups, COEP
\*        adherence for nested navigation)
G_MEM(g, d) == g = "concrete" => d.pcoep \in CompatCOI
\* F_AC  (obtain a similar-origin window agent: key, cluster, cluster mode)
G_AC(g, d)  == /\ d.cmode = (IF d.dip # "none" THEN "concrete" ELSE g)
               /\ (d.cmode # "none" => d.kind = "origin")
\* F_PP  (crossOriginIsolated getter: cluster mode and permissions policy)
G_CAP(g, d) == d.cap = (d.cmode = "concrete" /\ d.ppok) /\ (d.isTop => d.ppok)

GNames == <<"pc", "dip", "bcg", "mem", "ac", "cap">>
GBy(n, g, d) == CASE n = "pc" -> G_PC(g, d) [] n = "dip" -> G_DIP(g, d)
                  [] n = "bcg" -> G_BCG(g, d) [] n = "mem" -> G_MEM(g, d)
                  [] n = "ac" -> G_AC(g, d) [] OTHER -> G_CAP(g, d)
Gdoc(g, d) == \A j \in 1..6 : GBy(GNames[j], g, d)
\* The assumption about an earlier document, with one guarantee dropped
\* (drop = "none" keeps all): shows which assumptions are load-bearing.
Pre(drop, g, d) == \A j \in 1..6 : GNames[j] = drop \/ GBy(GNames[j], g, d)
PreDocs(drop, g) == {d \in DocSpace : Pre(drop, g, d)}

\* Clusters (as seen by a new document: the one with its key, if any) and
\* map entries. F_AC's guarantees about them:
ClSpace == [ex : BOOLEAN, dip : DIPs, mode : Modes]
G_CL(g, cl) == cl.ex => cl.mode = (IF cl.dip # "none" THEN "concrete" ELSE g)
\* A cluster the new document (DIP nd) can join: same key.
Joinable(drop, g, nd) == {cl \in ClSpace : (drop = "cl" \/ G_CL(g, cl))
                                           /\ (cl.ex => (KeyHasDIP => cl.dip = nd))
                                           /\ (~cl.ex => cl.dip = "none" /\ cl.mode = "none")}
G_HIST(g, h) == g = "concrete" => h \in {"absent", "origin"}
Hists(drop, g) == {h \in {"absent", "site", "origin"} : drop = "hist" \/ G_HIST(g, h)}

\* --- Steps (composition of the reused operators) -----------------------------
\* Returns [ok, g, d, hist (new map entry), joined].
Mk(o, top, pc, dip, coopP, kind, cl, own, ppok, isTop, g, h) ==
  LET cm == IF cl.ex THEN cl.mode ELSE own IN
  [ok |-> TRUE, g |-> g, joined |-> cl.ex,
   hist |-> IF h = "absent" THEN kind ELSE h,
   d |-> [self |-> o, top |-> top, pcoep |-> pc, dip |-> dip, coopP |-> coopP, kind |-> kind,
          cmode |-> cm, ppok |-> ppok, cap |-> (cm = "concrete" /\ ppok), isTop |-> isTop]]
NoCl == [ex |-> FALSE, dip |-> "none", mode |-> "none"]

\* Navigation commit of a top-level document: creates the group.
TopStep(o, coop, coep, dip, oac) ==
  LET ctx  == TopCtx(o)
      g    == COIMode(coop, coep, o)
      own  == COIModeD(coop, coep, o, dip)
      kind == KeyKindCtx(ctx, own, "absent", oac)
  IN Mk(o, o, EffectiveCOEPCtx(ctx, coep), EffectiveDIP(o, dip), ParsedCOOP(coop, coep, o),
        kind, NoCl, own, TRUE, TRUE, g, "absent")

\* Nested navigation of a child of p to response r with COEP header ccoep.
ChildStep(g, p, r, ccoep, oac, h, cl) ==
  LET pctx == Ctx(p)
      ctx  == ChildCtx(pctx, r)
      kind == KeyKindCtx(ctx, g, h, oac)
      res  == Mk(r.origin, pctx.top, EffectiveCOEPCtx(ctx, ccoep), "none", "unsafe-none", kind,
                 cl, g, p.ppok /\ SameOrigin(r.origin, p.self), FALSE, g, h)
  IN IF NavChild(pctx, p.pcoep, r, ccoep) = "loaded" THEN res ELSE [res EXCEPT !.ok = FALSE]

\* Popup from top-level document p through the responses rs (RedirectSeq).
PopupStep(g, p, rs, oac, h, cl) ==
  LET f    == rs[Len(rs)]
      ctx  == TopCtx(f.o)
      kind == KeyKindCtx(ctx, g, h, oac)
      res  == Mk(f.o, f.o, EffectiveCOEP(f.o, f.coep), "none", RS!Parsed(f), kind, cl, g, TRUE,
                 TRUE, g, h)
  IN IF p.isTop /\ ~RS!Swap(TRUE, RS!Res0(p.self, p.coopP), rs) THEN res
     ELSE [res EXCEPT !.ok = FALSE]

ChildResp == {r \in Responses : r.creds}       \* navigation requests send credentials
PopOrigins == {OA, OAwww, OB}                  \* RedirectSeq: https origins only
HopSet(red) == [o : PopOrigins, coop : COOPs, coep : COEPs, redirect : {red}]
Chains == {<<f>> : f \in HopSet(FALSE)} \cup {<<x, f>> : x \in HopSet(TRUE), f \in HopSet(FALSE)}

\* What every step must establish about what it adds.
PostOK(res, cl) ==
  res.ok => /\ Gdoc(res.g, res.d)
            /\ G_HIST(res.g, res.hist) /\ res.hist = res.d.kind
            /\ (~cl.ex => G_CL(res.g, [ex |-> TRUE, dip |-> res.d.dip, mode |-> res.d.cmode]))

\* --- Stepwise checks (one per step kind) --------------------------------------
StepTop(u) ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, dip \in DIPs, oac \in BOOLEAN :
    PostOK(TopStep(o, coop, coep, dip, oac), NoCl)
StepChild(drop) ==
  \A g \in Modes : \A p \in PreDocs(drop, g), r \in ChildResp, ccoep \in COEPs,
                      oac \in BOOLEAN, h \in Hists(drop, g), cl \in Joinable(drop, g, "none") :
    PostOK(ChildStep(g, p, r, ccoep, oac, h, cl), cl)
StepPopup(drop) ==
  \A g \in Modes : \A p \in {d \in PreDocs(drop, g) : d.isTop}, rs \in Chains, oac \in BOOLEAN,
                      h \in Hists(drop, g), cl \in Joinable(drop, g, "none") :
    PostOK(PopupStep(g, p, rs, oac, h, cl), cl)

\* --- The fetch fragment and the global property ------------------------------
FetchD(d, s) ==
  IF d.dip # "none" THEN FetchResultD(d.self, d.pcoep, d.dip, "no-cors", s)
  ELSE FetchResultCtx(Ctx(d), d.pcoep, "no-cors", s)
SentD(d, s) ==
  IF d.dip # "none" THEN ReqD(d.self, d.pcoep, d.dip, "no-cors", s)
  ELSE DocCreds(d.self, EffectiveCOEPCtx(Ctx(d), d.pcoep), "no-cors", s)
\* Global property: in a crossOriginIsolated document, cross-origin no-cors
\* bytes arrive only without credentials or with a CORP opt-in; and the
\* document's agent cluster is origin-keyed.
Prop(d, s) == /\ (d.cap /\ FetchD(d, s) = "opaque") => (~SentD(d, s).creds \/ HasOptIn(d.self, s))
              /\ d.cap => d.kind = "origin"
\* F_FETCH's guarantee, which assumes only the document's own policy fields.
G_FETCH(d, s) == (G_PC("-", d) /\ (d.pcoep \in CompatCOI \/ d.dip # "none") /\ FetchD(d, s) = "opaque")
                   => (~SentD(d, s).creds \/ HasOptIn(d.self, s))
FetchOK(u) == \A d \in DocSpace, s \in Responses : G_FETCH(d, s)
\* With F_DIP's guarantee assumed as well (the first run showed it is needed).
FetchOKDIP(u) == \A d \in DocSpace, s \in Responses : G_DIP("-", d) => G_FETCH(d, s)
FetchWitness == CHOOSE x \in DocSpace \X Responses : ~G_FETCH(x[1], x[2])
PrintFetch == dummy = 0 /\ PrintT(<<"fetch", FetchOK(0), FetchOKDIP(0), FetchWitness,
                                   FetchD(FetchWitness[1], FetchWitness[2]),
                                   SentD(FetchWitness[1], FetchWitness[2])>>)
\* The premise F_FETCH needs, derived from F_MEM, F_AC, F_PP.
CapPrem(drop) == \A g \in Modes : \A d \in PreDocs(drop, g) :
                   d.cap => (d.pcoep \in CompatCOI \/ d.dip # "none")
GlobalFromG(drop) == \A g \in Modes : \A d \in PreDocs(drop, g), s \in Responses : Prop(d, s)

\* One counterexample to a child step, for the report.
ChildBad(drop, g, x) == ~PostOK(ChildStep(g, x[1], x[2], x[3], x[4], x[5], x[6]), x[6])
ChildIn(drop, g) == PreDocs(drop, g) \X ChildResp \X COEPs \X BOOLEAN \X Hists(drop, g)
                    \X Joinable(drop, g, "none")
ChildWitness(drop) ==
  LET g == CHOOSE g \in Modes : \E x \in ChildIn(drop, g) : ChildBad(drop, g, x)
  IN <<g>> \o CHOOSE x \in ChildIn(drop, g) : ChildBad(drop, g, x)
FailingG(res) == {GNames[j] : j \in {i \in 1..6 : ~GBy(GNames[i], res.g, res.d)}}

Drops == <<"none", "pc", "dip", "bcg", "mem", "ac", "cap", "cl", "hist">>
\* State-level (dummy) so that TLC does not evaluate them eagerly at startup.
PrintSteps == dummy = 0 /\ PrintT(<<"steps", Mutant, KeyHasDIP, <<"top", StepTop(0)>>, <<"fetch", FetchOK(0), "with-dip", FetchOKDIP(0)>>,
  [j \in 1..Len(Drops) |-> <<Drops[j], "child", StepChild(Drops[j]), "popup", StepPopup(Drops[j]),
                              "capprem", CapPrem(Drops[j]), "global", GlobalFromG(Drops[j])>>]>>)
PrintNone == dummy = 0 /\ PrintT(<<"steps-none", Mutant, KeyHasDIP, <<"top", StepTop(0)>>, <<"fetch", FetchOK(0), "with-dip", FetchOKDIP(0)>>,
  <<"child", StepChild("none")>>, <<"popup", StepPopup("none")>>,
  <<"capprem", CapPrem("none")>>, <<"global", GlobalFromG("none")>>>>)
PrintChildWitness(drop) == dummy = 0 /\
  LET x == ChildWitness(drop) res == ChildStep(x[1], x[2], x[3], x[4], x[5], x[6], x[7]) IN
  PrintT(<<"child-witness", drop, x, res.d, FailingG(res)>>)
PrintChildWitnessNone == StepChild("none") \/ PrintChildWitness("none")
===============================================================================
