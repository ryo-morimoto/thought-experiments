------------------------------ MODULE HavocSpec -------------------------------
(* experiments/2026-11-23-havoc-unmodeled-steps.md: replace what an          *)
(* unmodeled closure step writes by any value of the model's type for that   *)
(* concept, at the place where the model reads it, and see which safety      *)
(* properties survive.                                                       *)
(* A havoc point is a slot in the model's data flow (writesets.tsv maps each *)
(* closure step to one). For points in HS the slot takes any value of its    *)
(* type, chosen per context (the record v is universally quantified inside   *)
(* the property); otherwise it takes the model's value. Every slot's range   *)
(* contains the model's value, so breaking is monotone in HS.                *)
(* Fetch and COI paths below mirror SpecIsolation's FetchResult and          *)
(* CrossOriginIsolated; with HS = {} and Omit = "none" they agree with them  *)
(* (checked by Conservative).                                                *)
EXTENDS SpecIsolation, FiniteSets

\* The two known omissions, as a parameter rather than through Mutant, so one
\* run can compare the model with and without the step.
Omits == {"none", "false:coep-insecure", "false:coep-cl-strips"}
Dec(m, id, e) == IF m = "false:" \o id THEN FALSE ELSE C(id, e)

\* Points backed by unmodeled closure steps (writesets.tsv, status unmodeled),
\* plus h-coicap, whose writer is not a closure step (the capability getter
\* and Permissions Policy).
Unmodeled == {"h-ecoep-inherit", "h-secure", "h-creds-mode", "h-coop",
              "h-respurl", "h-coimode", "h-sw"}
Boundary  == {"h-coicap"}
\* Points at modeled steps (positive-control points, guarded) and variants.
Modeled   == {"h-ecoep-insecure", "h-creds-cl", "h-tainting", "h-mode",
              "h-coicap-mono", "h-reqorigin", "h-reqorigin-any"}
\* Contract variants of unmodeled points: the value is limited to what the
\* step can write (-c: a default or the model's own value; -k: the property
\* is restated on the response actually delivered, so header and origin stay
\* coupled, which makes the delivered response just another quantified input:
\* the -k variants hold by construction; -adh: any group mode, but only with a
\* compatible COEP).
Contract  == {"h-secure-c", "h-coop-c", "h-coimode-c", "h-respurl-k", "h-sw-k", "h-coimode-adh"}
Points == Unmodeled \cup Boundary \cup Modeled \cup Contract
PointSeq == <<"h-ecoep-inherit", "h-secure", "h-creds-mode", "h-coop", "h-respurl",
              "h-coimode", "h-sw", "h-coicap", "h-ecoep-insecure", "h-creds-cl",
              "h-tainting", "h-mode", "h-coicap-mono", "h-reqorigin", "h-reqorigin-any",
              "h-secure-c", "h-coop-c", "h-coimode-c", "h-respurl-k", "h-sw-k", "h-coimode-adh">>
Coupled(HS) == HS \cap {"h-respurl-k", "h-sw-k"} # {}

Taints == {"basic", "cors", "opaque"}
In(p, HS) == p \in HS
\* The range of each slot (a singleton dummy when no point havocs it).
\* h-reqorigin is guarded by "navigation request", which never holds on the
\* fetch path the properties use, so it widens nothing.
Ranges(HS) ==
  [secure    |-> IF In("h-secure", HS) THEN BOOLEAN ELSE {TRUE},
   sw        |-> IF HS \cap {"h-sw", "h-sw-k"} # {} THEN Responses ELSE {Rsp(OA, "none")},
   respurl   |-> IF HS \cap {"h-respurl", "h-respurl-k"} # {} THEN Origins ELSE {OA},
   reqorigin |-> IF In("h-reqorigin-any", HS) THEN Origins ELSE {OA},
   mode      |-> IF In("h-mode", HS) THEN {"cors", "no-cors"} ELSE {"cors"},
   ecoep     |-> IF HS \cap {"h-ecoep-insecure", "h-ecoep-inherit"} # {} THEN COEPs ELSE {"unsafe-none"},
   creds     |-> IF HS \cap {"h-creds-cl", "h-creds-mode"} # {} THEN BOOLEAN ELSE {FALSE},
   taint     |-> IF In("h-tainting", HS) THEN Taints ELSE {"basic"},
   coop      |-> IF In("h-coop", HS) THEN COOPs \cup {"same-origin-plus-COEP"} ELSE {"unsafe-none"},
   coimode   |-> IF In("h-coimode", HS) THEN {"none", "logical", "concrete"} ELSE {"none"},
   cap       |-> IF HS \cap {"h-coicap", "h-coicap-mono"} # {} THEN BOOLEAN ELSE {FALSE},
   pickS     |-> IF In("h-secure-c", HS) THEN BOOLEAN ELSE {TRUE},
   pickC     |-> IF In("h-coop-c", HS) THEN BOOLEAN ELSE {TRUE},
   pickM     |-> IF In("h-coimode-c", HS) THEN BOOLEAN ELSE {TRUE},
   adh       |-> IF In("h-coimode-adh", HS) THEN {"none", "logical", "concrete"} ELSE {"none"}]
Vals(HS) ==
  LET R == Ranges(HS) IN
  [secure : R.secure, sw : R.sw, respurl : R.respurl, reqorigin : R.reqorigin,
   mode : R.mode, ecoep : R.ecoep, creds : R.creds, taint : R.taint,
   coop : R.coop, coimode : R.coimode, cap : R.cap,
   pickS : R.pickS, pickC : R.pickC, pickM : R.pickM, adh : R.adh]

\* Fetch path. Returns the result and the creds bit the CORP check saw.
\* The guarded points fire only where the step they stand for fires:
\*  h-ecoep-insecure: obtain an embedder policy, non-secure environment;
\*  h-creds-cl: COEP allows credentials, no-cors + credentialless + cross-origin;
\*  h-reqorigin: request origin set for navigation requests, never in this path.
Sec(HS, v, o) ==
  IF In("h-secure", HS) THEN v.secure
  ELSE IF In("h-secure-c", HS) THEN Secure(o) /\ v.pickS  \* nesting, data: lower it
  ELSE Secure(o)
FetchH(m, HS, v, o, coep, mode, r) ==
  LET sec   == Sec(HS, v, o)
      rsp   == IF HS \cap {"h-sw", "h-sw-k"} # {} THEN v.sw ELSE r
      rspO  == IF HS \cap {"h-respurl", "h-respurl-k"} # {} THEN v.respurl ELSE rsp.origin
      reqO  == IF In("h-reqorigin-any", HS) THEN v.reqorigin ELSE o
      mo    == IF In("h-mode", HS) THEN v.mode ELSE mode
      e0    == IF Dec(m, "coep-insecure", ~sec) THEN "unsafe-none" ELSE coep
      e1    == IF In("h-ecoep-insecure", HS) /\ ~sec THEN v.ecoep ELSE e0
      ecoep == IF In("h-ecoep-inherit", HS) THEN v.ecoep ELSE e1
      strip == mo = "no-cors" /\ ecoep = "credentialless" /\ ~SameOrigin(reqO, rspO)
      c0    == IF Dec(m, "coep-cl-strips", strip) THEN FALSE ELSE rsp.creds
      c1    == IF In("h-creds-cl", HS) /\ strip THEN v.creds ELSE c0
      cr    == IF In("h-creds-mode", HS) THEN v.creds ELSE c1
      rr    == [origin |-> rspO, corp |-> rsp.corp, creds |-> cr]
      t0    == IF C("fetch-same-origin", SameOrigin(reqO, rspO))
                  \/ (mo = "no-cors" /\ Mutant = "nocors-site-basic" /\ SameSite(reqO, rspO))
               THEN "basic" ELSE IF C("fetch-cors", mo = "cors") THEN "cors" ELSE "opaque"
      taint == IF In("h-tainting", HS) THEN v.taint ELSE t0
  IN [res   |-> IF taint = "basic" THEN "basic"
                ELSE IF taint = "cors" THEN "cors"
                ELSE IF C("fetch-blocked", CorpCheck(reqO, ecoep, rr, FALSE) = "blocked")
                     THEN "error" ELSE "opaque",
      creds |-> cr,
      seen  |-> [origin |-> rspO, corp |-> rsp.corp, creds |-> rsp.creds]]

\* COI path: the document's cross-origin isolated capability.
COIH(m, HS, v, coop, coep, o) ==
  LET sec  == Sec(HS, v, o)
      p0   == IF C("coi-insecure", ~sec) THEN "unsafe-none"
              ELSE IF C("coi-coop-so", coop = "same-origin") /\ C("coi-coep-compat", coep \in CompatibleCOEP)
                   THEN "same-origin-plus-COEP" ELSE coop
      pc   == IF In("h-coop", HS) THEN v.coop
              ELSE IF In("h-coop-c", HS) /\ ~v.pickC THEN "unsafe-none" ELSE p0
      g0   == IF C("coi-mode", pc = "same-origin-plus-COEP") THEN COIChoice ELSE "none"
      \* h-coimode-adh: a document kept in an existing group (step 2: nested)
      \* gets any group mode, but only if its COEP is compatible, as the
      \* unmodeled embedder-policy adherence check for child navigables requires.
      g    == IF In("h-coimode", HS) THEN v.coimode
              ELSE IF In("h-coimode-c", HS) /\ ~v.pickM THEN "none"
              ELSE IF In("h-coimode-adh", HS) /\ sec /\ coep \in CompatibleCOEP THEN v.adh
              ELSE g0
      cap0 == g = "concrete"
  IN IF In("h-coicap", HS) THEN v.cap
     ELSE IF In("h-coicap-mono", HS) THEN cap0 /\ v.cap   \* can only be turned off
     ELSE cap0

OptIn(o, r) == r.corp = "cross-origin" \/ (r.corp = "same-site" /\ SameSite(o, r.origin))

\* Properties. They read r (the model's input) and o; the slots read the
\* havocked values. COIOptInH reads the creds bit the CORP check saw (as
\* DIPExtension's COIOnlyWithOptIn reads ReqD), with dip = "none".
OptInSecH(m, HS) ==
  \A o \in Origins, r \in Responses, v \in Vals(HS) :
    LET f == FetchH(m, HS, v, o, "require-corp", "no-cors", r) IN
    (Secure(o) /\ f.res = "opaque") => OptIn(o, IF Coupled(HS) THEN f.seen ELSE r)
OptInH(m, HS) ==
  \A o \in Origins, r \in Responses, v \in Vals(HS) :
    LET f == FetchH(m, HS, v, o, "require-corp", "no-cors", r) IN
    f.res = "opaque" => OptIn(o, IF Coupled(HS) THEN f.seen ELSE r)
COIOptInH(m, HS) ==
  \A o \in Origins, coop \in COOPs, coep \in COEPs, r \in Responses, v \in Vals(HS) :
    LET f == FetchH(m, HS, v, o, coep, "no-cors", r) IN
    (COIH(m, HS, v, coop, coep, o) /\ f.res = "opaque")
      => (~f.creds \/ OptIn(o, IF Coupled(HS) THEN f.seen ELSE r))

Props(m, HS) == <<OptInSecH(m, HS), OptInH(m, HS), COIOptInH(m, HS)>>

\* Witnesses (only meaningful when the property fails).
Seen(HS, f, r) == IF Coupled(HS) THEN f.seen ELSE r
W1(m, HS) == CHOOSE x \in Origins \X Responses \X Vals(HS) :
  LET f == FetchH(m, HS, x[3], x[1], "require-corp", "no-cors", x[2]) IN
  Secure(x[1]) /\ f.res = "opaque" /\ ~OptIn(x[1], Seen(HS, f, x[2]))
W2(m, HS) == CHOOSE x \in Origins \X Responses \X Vals(HS) :
  LET f == FetchH(m, HS, x[3], x[1], "require-corp", "no-cors", x[2]) IN
  f.res = "opaque" /\ ~OptIn(x[1], Seen(HS, f, x[2]))
W3(m, HS) == CHOOSE x \in Origins \X COOPs \X COEPs \X Responses \X Vals(HS) :
  LET f == FetchH(m, HS, x[5], x[1], x[3], "no-cors", x[4]) IN
  COIH(m, HS, x[5], x[2], x[3], x[1]) /\ f.res = "opaque" /\ f.creds
  /\ ~OptIn(x[1], Seen(HS, f, x[4]))
\* Only the havocked fields of a witness valuation.
Show(HS, v) ==
  LET F == {f \in DOMAIN v : Cardinality(Ranges(HS)[f]) > 1} IN
  [f \in F |-> v[f]]
Wit(m, HS) ==
  <<IF OptInSecH(m, HS) THEN "-" ELSE <<W1(m, HS)[1], W1(m, HS)[2], Show(HS, W1(m, HS)[3])>>,
    IF OptInH(m, HS) THEN "-" ELSE <<W2(m, HS)[1], W2(m, HS)[2], Show(HS, W2(m, HS)[3])>>,
    IF COIOptInH(m, HS) THEN "-" ELSE <<W3(m, HS)[1], W3(m, HS)[2], W3(m, HS)[3], W3(m, HS)[4], Show(HS, W3(m, HS)[5])>>>>

\* Sanity: with nothing havocked and nothing omitted, the model is unchanged.
V0 == CHOOSE v \in Vals({}) : TRUE
Conservative ==
  /\ \A o \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"}, r \in Responses :
       FetchH("none", {}, V0, o, coep, mode, r).res = FetchResult(o, coep, mode, r)
  /\ \A o \in Origins, coop \in COOPs, coep \in COEPs :
       COIH("none", {}, V0, coop, coep, o) = CrossOriginIsolated(coop, coep, o)

\* Behaviour-level positive control: the omission changes some fetch result,
\* and havoc at the omitted step's point over-approximates the full model.
Differs(m) ==
  \E o \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"}, r \in Responses :
    FetchH("none", {}, V0, o, coep, mode, r).res # FetchH(m, {}, V0, o, coep, mode, r).res
Recovers(m, p) ==
  \A o \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"}, r \in Responses :
    FetchH("none", {}, V0, o, coep, mode, r).res
      \in {FetchH(m, {p}, v, o, coep, mode, r).res : v \in Vals({p})}

CONSTANT Omit, Sets   \* Sets: a sequence of havoc sets to check jointly
NoSets == <<>>
\* Joint checks (Sets.cfg): the real unmodeled set, with the boundary point,
\* and the union of the points that did not break OptInSecH (NB1) or
\* COIOptInH (NB2) one at a time in Singles-none. By monotonicity, if a union
\* holds, every subset of it holds.
NB1 == {"h-creds-mode", "h-coop", "h-coimode", "h-coicap", "h-ecoep-insecure",
        "h-creds-cl", "h-mode", "h-coicap-mono", "h-reqorigin"}
NB2 == {"h-secure", "h-creds-mode", "h-ecoep-insecure", "h-creds-cl", "h-mode",
        "h-coicap-mono", "h-reqorigin"}
\* UC: the unmodeled set with each point replaced by its contract variant
\* where one exists (h-ecoep-inherit and h-creds-mode have none).
UC == {"h-ecoep-inherit", "h-secure-c", "h-creds-mode", "h-coop-c", "h-respurl-k",
       "h-coimode-c", "h-sw-k", "h-coicap-mono"}
UCnoInherit == UC \ {"h-ecoep-inherit"}
JointSets == <<Unmodeled, Unmodeled \cup Boundary, NB1, NB2, UC, UCnoInherit>>
PrintBase == PrintT(<<"havoc-base", Omit, <<"conservative", Conservative>>, Props(Omit, {})>>)
PrintSingles == PrintT(<<"havoc-singles", Omit,
  [i \in 1..Len(PointSeq) |-> <<PointSeq[i], Props(Omit, {PointSeq[i]})>>]>>)
PrintWitness == PrintT(<<"havoc-witness", Omit,
  [i \in 1..Len(PointSeq) |-> <<PointSeq[i], Wit(Omit, {PointSeq[i]})>>]>>)
PrintControl == PrintT(<<"havoc-control", Omit,
  <<"differs", Differs(Omit)>>,
  <<"recovers-ecoep-insecure", Recovers(Omit, "h-ecoep-insecure")>>,
  <<"recovers-creds-cl", Recovers(Omit, "h-creds-cl")>>>>)
PrintSets == PrintT(<<"havoc-sets", Omit, [i \in 1..Len(Sets) |-> <<Sets[i], Props(Omit, Sets[i])>>]>>)
===============================================================================
