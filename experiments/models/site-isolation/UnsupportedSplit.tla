----------------------------- MODULE UnsupportedSplit ------------------------------
(* Stage C attack (formal-methods reviewer) of                              *)
(* experiments/2026-11-21-toe-optional-feature.md: Unsupported.tla plus     *)
(* constants Mut (SpecIsolation's Mutant), Split (the fetch path reads      *)
(* credentialless as unsafe-none while the isolation check knows it), and  *)
(* the number of tuples that satisfy the antecedent of IsolationGuarded.   *)
(* Stage B, operation 1 of experiments/2026-11-21-toe-optional-feature.md:   *)
(* a shipped browser that does not support some isolation features. Such a  *)
(* browser reads the header as if absent: HTML "obtain an embedder policy"   *)
(* and "obtain an opener policy" set a value only for values they know, so   *)
(* an unknown value leaves the default "unsafe-none". The spec operators are *)
(* those of SpecIsolation with no misreading (Mutant = "none").              *)
(* Question: which safety statements carry over from the supporting browser *)
(* to the non-supporting one, and does it depend on whether the feature     *)
(* adds capability or restriction (rival R5)?                               *)
EXTENDS Naturals, TLC, FiniteSets

\* Features this browser supports: a subset of
\* {"credentialless", "coop", "oac", "dip", "nap"}.
CONSTANTS Supported, Mut, Split

VARIABLE dummy
S == INSTANCE SpecIsolation WITH Mutant <- Mut, dummy <- dummy

\* What the browser makes of the headers a page sent.
SeenCOEP(coep) ==
  IF coep = "credentialless" /\ "credentialless" \notin Supported THEN "unsafe-none" ELSE coep
SeenCOOP(coop) == IF "coop" \notin Supported THEN "unsafe-none" ELSE coop
SeenOAC(h)     == h /\ "oac" \in Supported

Hists == {"absent", "site", "origin"}

\* P1, a guarantee tied to a capability. If the page gets cross-origin
\* isolation (SharedArrayBuffer etc.), every cross-origin no-cors body it
\* embeds either opted in with CORP or was fetched without credentials.
IsolationGuarded ==
  \A o \in S!Origins, coop \in S!COOPs, coep \in S!COEPs, r \in S!Responses :
    LET c  == SeenCOEP(coep)
        cf == IF Split /\ coep = "credentialless" THEN "unsafe-none" ELSE c
        ec == S!EffectiveCOEP(o, cf)
        rr == S!DocCreds(o, ec, "no-cors", r)
    IN (/\ S!CrossOriginIsolated(SeenCOOP(coop), c, o)
        /\ ~S!SameOrigin(o, r.origin)
        /\ S!FetchResult(o, cf, "no-cors", r) = "opaque")
       => \/ r.corp = "cross-origin"
          \/ r.corp = "same-site" /\ S!SameSite(o, r.origin)
          \/ ~rr.creds

\* P2, a promise read off the header alone: a secure page that sent
\* COEP credentialless sends its cross-origin no-cors requests without
\* credentials.
CredentiallessStrips ==
  \A o \in S!Origins, r \in S!Responses :
    (S!Secure(o) /\ ~S!SameOrigin(o, r.origin) /\ r.creds) =>
      ~S!DocCreds(o, S!EffectiveCOEP(o, SeenCOEP("credentialless")), "no-cors", r).creds

\* P3, a restriction with no capability attached: a secure opener that sent
\* COOP same-origin is severed from any cross-origin popup.
COOPSevers ==
  \A o \in S!Origins, p \in S!Origins, pc \in S!COOPs :
    (S!Secure(o) /\ ~S!SameOrigin(o, p)) =>
      S!PopupSevered(SeenCOOP("same-origin"), o, SeenCOOP(pc), p)

\* P4, Origin-Agent-Cluster as a request. Fresh: the group has no
\* historical key for the origin. Any: every historical state.
OACFresh ==
  \A o \in S!Origins :
    S!Secure(o) => S!DocumentDomainNoOp(S!KeyKind(o, "none", "absent", SeenOAC(TRUE)))
OACAny ==
  \A o \in S!Origins, h \in Hists :
    S!Secure(o) => S!DocumentDomainNoOp(S!KeyKind(o, "none", h, SeenOAC(TRUE)))

\* --- Stage B, second round: Document-Isolation-Policy and noopener-allow-popups.
\* DIP (WICG Draft Community Group Report, 23 April 2025): a secure document
\* with isolate-and-require-corp or isolate-and-credentialless is assigned to
\* a cross-origin isolated agent cluster, and its no-cors fetches are checked.
\* Approximation (author's reading): the fetch check is that of the COEP value
\* of the same name. An unsupported or unknown value leaves the policy "none".
DIPs == {"none", "isolate-and-require-corp", "isolate-and-credentialless"}
SeenDIP(d) == IF "dip" \notin Supported THEN "none" ELSE d
DIPIsolated(d, o) == S!Secure(o) /\ d # "none"
DIPAsCOEP(d) == CASE d = "isolate-and-require-corp"   -> "require-corp"
                  [] d = "isolate-and-credentialless" -> "credentialless"
                  [] OTHER                            -> "unsafe-none"

\* P5, DIP's guarantee tied to the capability, as P1.
DIPGuarded ==
  \A o \in S!Origins, d \in DIPs, r \in S!Responses :
    LET dd == SeenDIP(d)
        c  == DIPAsCOEP(IF S!Secure(o) THEN dd ELSE "none")
        rr == S!DocCreds(o, c, "no-cors", r)
    IN (/\ DIPIsolated(dd, o)
        /\ ~S!SameOrigin(o, r.origin)
        /\ S!FetchResult(o, c, "no-cors", r) = "opaque")
       => \/ r.corp = "cross-origin"
          \/ r.corp = "same-site" /\ S!SameSite(o, r.origin)
          \/ ~rr.creds

\* HTML "check if popup COOP values require a browsing context group switch",
\* with the noopener-allow-popups steps that SpecIsolation leaves out.
COOPsNAP == S!COOPs \cup {"noopener-allow-popups"}
SeenCOOPNAP(coop) ==
  IF coop = "noopener-allow-popups" /\ "nap" \notin Supported THEN "unsafe-none"
  ELSE SeenCOOP(coop)
SeveredNAP(openerCOOP, openerOrigin, popupCOOP, popupOrigin) ==
  IF popupCOOP = "noopener-allow-popups" THEN TRUE
  ELSE IF openerCOOP \in {"same-origin-allow-popups", "noopener-allow-popups"}
          /\ popupCOOP = "unsafe-none" THEN FALSE
  ELSE IF openerCOOP = "noopener-allow-popups" THEN TRUE
  ELSE S!PopupSevered(openerCOOP, openerOrigin, popupCOOP, popupOrigin)

\* P6, a restriction with no capability attached: a secure document that sent
\* noopener-allow-popups is severed from whatever opened it, even same-origin.
NAPSevers ==
  \A o \in S!Origins, p \in S!Origins, oc \in COOPsNAP :
    S!Secure(p) =>
      SeveredNAP(SeenCOOPNAP(oc), o, SeenCOOPNAP("noopener-allow-popups"), p)

Results == [dipGuarded |-> DIPGuarded, napSevers |-> NAPSevers,
            isolationGuarded |-> IsolationGuarded,
            credentiallessStrips |-> CredentiallessStrips,
            coopSevers |-> COOPSevers,
            oacFresh |-> OACFresh, oacAny |-> OACAny]
IsoWitnesses == Cardinality({x \in S!Origins \X S!COOPs \X S!COEPs \X S!Responses :
   /\ S!CrossOriginIsolated(SeenCOOP(x[2]), SeenCOEP(x[3]), x[1])
   /\ ~S!SameOrigin(x[1], x[4].origin)
   /\ S!FetchResult(x[1], SeenCOEP(x[3]), "no-cors", x[4]) = "opaque"})
DIPWitnesses == Cardinality({x \in S!Origins \X DIPs : DIPIsolated(SeenDIP(x[2]), x[1])})
PrintResults == PrintT(<<Supported, Mut, Split, "isoW", IsoWitnesses, "dipW", DIPWitnesses, Results>>)

Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
