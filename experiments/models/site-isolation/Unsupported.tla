----------------------------- MODULE Unsupported ------------------------------
(* Stage B, operation 1 of experiments/2026-11-21-toe-optional-feature.md:   *)
(* a shipped browser that does not support some isolation features. Such a  *)
(* browser reads the header as if absent: HTML "obtain an embedder policy"   *)
(* and "obtain an opener policy" set a value only for values they know, so   *)
(* an unknown value leaves the default "unsafe-none". The spec operators are *)
(* those of SpecIsolation with no misreading (Mutant = "none").              *)
(* Question: which safety statements carry over from the supporting browser *)
(* to the non-supporting one, and does it depend on whether the feature     *)
(* adds capability or restriction (rival R5)?                               *)
EXTENDS Naturals, TLC

\* Features this browser supports: a subset of {"credentialless", "coop", "oac"}.
CONSTANT Supported

VARIABLE dummy
S == INSTANCE SpecIsolation WITH Mutant <- "none", dummy <- dummy

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
        ec == S!EffectiveCOEP(o, c)
        rr == S!DocCreds(o, ec, "no-cors", r)
    IN (/\ S!CrossOriginIsolated(SeenCOOP(coop), c, o)
        /\ ~S!SameOrigin(o, r.origin)
        /\ S!FetchResult(o, c, "no-cors", r) = "opaque")
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

Results == [isolationGuarded |-> IsolationGuarded,
            credentiallessStrips |-> CredentiallessStrips,
            coopSevers |-> COOPSevers,
            oacFresh |-> OACFresh, oacAny |-> OACAny]
PrintResults == PrintT(<<"supported", Supported, Results>>)

Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
