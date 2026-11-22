---------------------------- MODULE HavocFixCore -----------------------------
(* fixes/FIXES.md: the havoc points of havoc/HavocSpec.tla that found G1, G2 *)
(* and the premise mismatch, re-run against the fixed SpecIsolation, which  *)
(* has document contexts, nested navigation and Mixed Content. Same method:  *)
(* a point in HS replaces the value at a slot by any value of its range,     *)
(* chosen per context (v is quantified inside the property). Each slot has  *)
(* a parent field (P) and a child field (C), so parent and child are havocked *)
(* independently. Mutant comes from the instantiating module (HavocFix.tla). *)
EXTENDS SpecIsolation, FiniteSets

PointSeq == <<"h-secure", "h-secure-c", "h-ecoep-inherit", "h-ecoep-inherit-p",
              "h-coimode", "h-coimode-adh", "h-mc">>
In(p, HS) == p \in HS
Modes == {"none", "logical", "concrete"}
Vals(HS) ==
  [secP  : IF In("h-secure", HS) THEN BOOLEAN ELSE {TRUE},
   secC  : IF In("h-secure", HS) THEN BOOLEAN ELSE {TRUE},
   pickP : IF In("h-secure-c", HS) THEN BOOLEAN ELSE {TRUE},
   pickC : IF In("h-secure-c", HS) THEN BOOLEAN ELSE {TRUE},
   ecP   : IF In("h-ecoep-inherit", HS) THEN COEPs ELSE {"unsafe-none"},
   ecC   : IF In("h-ecoep-inherit", HS) THEN COEPs ELSE {"unsafe-none"},
   inhC  : IF In("h-ecoep-inherit-p", HS) THEN BOOLEAN ELSE {FALSE},
   mode  : IF In("h-coimode", HS) THEN Modes ELSE {"none"},
   adh   : IF In("h-coimode-adh", HS) THEN Modes ELSE {"none"},
   mcP   : IF In("h-mc", HS) THEN BOOLEAN ELSE {FALSE},
   mcC   : IF In("h-mc", HS) THEN BOOLEAN ELSE {FALSE}]
V0 == CHOOSE v \in Vals({}) : TRUE

\* The secure-context bit read by obtain an embedder policy.
\*  h-secure: any value; h-secure-c: can only be lowered (data: top-level
\*  URL, worker owner: the writers still unmodelled).
Sec(HS, v, ctx, w) ==
  IF In("h-secure", HS) THEN (IF w = "P" THEN v.secP ELSE v.secC)
  ELSE IF In("h-secure-c", HS) THEN SecureCtx(ctx) /\ (IF w = "P" THEN v.pickP ELSE v.pickC)
  ELSE SecureCtx(ctx)
\* Policy container embedder policy. inh: the parent's (a child created
\* from srcdoc, about:blank or blob: inherits its creator's policy
\* container), or "-" for a top-level document.
\*  h-ecoep-inherit: any value; h-ecoep-inherit-p: the child's may be the parent's.
EC(HS, v, ctx, coep, w, inh) ==
  LET e0 == IF C("coep-insecure", ~Sec(HS, v, ctx, w)) THEN "unsafe-none" ELSE coep IN
  IF In("h-ecoep-inherit", HS) THEN (IF w = "P" THEN v.ecP ELSE v.ecC)
  ELSE IF In("h-ecoep-inherit-p", HS) /\ inh # "-" /\ v.inhC THEN inh
  ELSE e0
\* fetch() (destination "fetch") with the Mixed Content decision as a slot.
MC(HS, v, ctx, r, w) ==
  IF In("h-mc", HS) THEN (IF w = "P" THEN v.mcP ELSE v.mcC) ELSE C("mc-block", IsMixed(ctx, r))
FetchH(HS, v, ctx, e, r, w) ==
  IF MC(HS, v, ctx, r, w) THEN "error" ELSE FetchResultPC(ctx, e, "no-cors", r)
\* Group cross-origin isolation mode, set by the top-level document.
\*  h-coimode: any mode; h-coimode-adh: any mode, but only if the
\*  top-level document's COEP is compatible (the -adh contract of HavocSpec,
\*  now placed on the group's creator, not on the document itself).
\* As in HavocSpec's COIH, COOP parsing reads the same secure bit as the
\* embedder policy (parent field), so the two stay coupled.
Group(HS, v, coop, coep, o) ==
  LET sec == Sec(HS, v, TopCtx(o), "P")
      p0  == IF C("coi-insecure", ~sec) THEN "unsafe-none"
             ELSE IF C("coi-coop-so", coop = "same-origin") /\ C("coi-coep-compat", coep \in CompatibleCOEP)
                  THEN "same-origin-plus-COEP" ELSE coop
      g0  == IF C("coi-mode", p0 = "same-origin-plus-COEP") THEN COIChoice ELSE "none"
  IN IF In("h-coimode", HS) THEN v.mode
     ELSE IF In("h-coimode-adh", HS) /\ sec /\ coep \in CompatCOI THEN v.adh
     ELSE g0

\* Properties (all over no-cors fetches by a document; r, s: responses).
\* Top-level OptInOnlySecure (premise: https origin), as HavocSpec's OptInSecH.
POptTop(HS) ==
  \A o \in Origins, r \in Responses, v \in Vals(HS) :
    LET c == TopCtx(o) e == EC(HS, v, c, "require-corp", "P", "-") IN
    (Secure(o) /\ FetchH(HS, v, c, e, r, "P") = "opaque") => HasOptIn(o, r)
\* Over contexts: old premise (https origin) and new premise (secure context).
POptLifted(HS) ==
  \A c \in Contexts, r \in Responses, v \in Vals(HS) :
    LET e == EC(HS, v, c, "require-corp", "P", "-") IN
    (Secure(c.self) /\ FetchH(HS, v, c, e, r, "P") = "opaque") => HasOptIn(c.self, r)
POptCtx(HS) ==
  \A c \in Contexts, r \in Responses, v \in Vals(HS) :
    LET e == EC(HS, v, c, "require-corp", "P", "-") IN
    (SecureCtx(c) /\ FetchH(HS, v, c, e, r, "P") = "opaque") => HasOptIn(c.self, r)
\* Premise on the policy-container value (the slot itself): holds by construction.
POptPC(HS) ==
  \A c \in Contexts, coep \in COEPs, r \in Responses, v \in Vals(HS) :
    LET e == EC(HS, v, c, coep, "P", "-") IN
    (e = "require-corp" /\ FetchH(HS, v, c, e, r, "P") = "opaque") => HasOptIn(c.self, r)
\* COI reason property, top-level document (HavocSpec's COIOptInH).
PCoiTop(HS) ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, s \in Responses, v \in Vals(HS) :
    LET c == TopCtx(o) e == EC(HS, v, c, coep, "P", "-")
        ss == DocCreds(o, e, "no-cors", s) IN
    (Group(HS, v, coop, coep, o) = "concrete" /\ FetchH(HS, v, c, e, s, "P") = "opaque")
      => (~ss.creds \/ HasOptIn(o, s))
\* COI reason property for a child of the top-level document: the
\* navigation response and the child's own no-cors fetches.
PCoiNested(HS) ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, r \in Responses, ccoep \in COEPs,
     s \in Responses, v \in Vals(HS) :
    LET pc == TopCtx(o) pe == EC(HS, v, pc, coep, "P", "-")
        cc == ChildCtx(pc, r) ce == EC(HS, v, cc, ccoep, "C", pe)
        ss == DocCreds(cc.self, ce, "no-cors", s) IN
    (Group(HS, v, coop, coep, o) = "concrete" /\ NavChildPC(pc, pe, r, ce) = "loaded")
      => /\ (SameOrigin(o, r.origin) \/ HasOptIn(o, r))
         /\ (FetchH(HS, v, cc, ce, s, "C") = "opaque" => (~ss.creds \/ HasOptIn(cc.self, s)))

Props(HS) == <<POptTop(HS), POptLifted(HS), POptCtx(HS), POptPC(HS), PCoiTop(HS), PCoiNested(HS)>>

\* With nothing havocked, the paths equal SpecIsolation's operators.
Conservative ==
  /\ \A c \in Contexts, coep \in COEPs, r \in Responses :
       FetchH({}, V0, c, EC({}, V0, c, coep, "P", "-"), r, "P") = FetchResultCtx(c, coep, "no-cors", r)
  /\ \A o \in Origins, coop \in COOPs, coep \in COEPs :
       (Group({}, V0, coop, coep, o) = "concrete") = CrossOriginIsolated(coop, coep, o)
  /\ \A o \in Origins, coep \in COEPs, r \in Responses, ccoep \in COEPs :
       LET pe == EffectiveCOEP(o, coep) IN
       NavChildPC(TopCtx(o), pe, r, EC({}, V0, ChildCtx(TopCtx(o), r), ccoep, "C", pe))
         = NavChild(TopCtx(o), pe, r, ccoep)
\* Fetch result for the behaviour-level control (Differs / Recovers).
FR(HS, v, c, coep, r) == FetchH(HS, v, c, EC(HS, v, c, coep, "P", "-"), r, "P")
===============================================================================
