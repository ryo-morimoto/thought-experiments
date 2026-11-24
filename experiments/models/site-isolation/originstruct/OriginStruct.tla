----------------------------- MODULE OriginStruct ------------------------------
(* originstruct/RESULTS.md, for experiments/2026-11-24-origin-structure.md   *)
(* (tree node B7). Gives SpecIsolation richer origins and checks whether the *)
(* property verdicts change. SpecIsolation is reused unedited: the .cfg      *)
(* files replace its origin operators (SameSite, Secure, SecureCtx, TopCtx,  *)
(* ChildCtx, Key, CorpInternal, FetchResultDest, Origins, Contexts,          *)
(* Responses) with the definitions below.                                    *)
(* Specs: HTML 0e292f4, URL 4f461b8, Fetch d7fc0fd (job scratch), Secure     *)
(* Contexts ED 2023-11-10 and Mixed Content ED 2023-02-23 (fetched           *)
(* 2026-11-24). Line numbers are in html.src / url.bs / fetch.bs.           *)
EXTENDS SpecIsolation, FiniteSets

\* --- Origins (html.src:94612): opaque, or tuple (scheme, host, port, domain).
\* domain (document.domain) is not modelled. All origins are records with the
\* same fields so that TLC can compare any two.
TO(s, h, p) == [op |-> FALSE, id |-> "-", scheme |-> s, host |-> h, port |-> p]
Opq(i)      == [op |-> TRUE, id |-> i, scheme |-> "-", host |-> "-", port |-> "-"]

\* Hosts by class: registrable domain non-null / null, potentially
\* trustworthy (Secure Contexts 3.1 steps 4-5) or not.
Normal   == <<"a.test", "x.a.test", "y.a.test", "b.test", "c.test">>
LocalReg == <<"a.localhost", "x.a.localhost", "y.a.localhost", "b.localhost", "c.localhost">>
NullPT   == <<"127.0.0.2", "127.0.0.1", "localhost">>
NullNPT  == <<"198.51.100.1", "test", "192.0.2.1">>   \* "test" is itself a public suffix
Hosts == {Normal[i] : i \in 1..5} \cup {LocalReg[i] : i \in 1..5}
         \cup {NullPT[i] : i \in 1..3} \cup {NullNPT[i] : i \in 1..3}
IPHosts == {"127.0.0.2", "127.0.0.1", "198.51.100.1", "192.0.2.1"}
PTHosts == {"127.0.0.2", "127.0.0.1", "localhost"} \cup {LocalReg[i] : i \in 1..5}
Ports == <<"", "8443", "8444">>   \* "" is the null (default) port
PortsUpTo(n) == {Ports[i] : i \in 1..n}
Schemes == {"https", "http"}
\* st[i]: number of ports of Normal[i] and LocalReg[i]; sn[i]: of NullPT[i], NullNPT[i].
StairDom(st, sn) ==
  UNION {{TO(s, Normal[i], p) : p \in PortsUpTo(st[i])} \cup {TO(s, LocalReg[i], p) : p \in PortsUpTo(st[i])}
           : i \in 1..5, s \in Schemes}
  \cup UNION {{TO(s, NullPT[i], p) : p \in PortsUpTo(sn[i])} \cup {TO(s, NullNPT[i], p) : p \in PortsUpTo(sn[i])}
           : i \in 1..3, s \in Schemes}
\* types2.py: DomRich realizes every relational type of k <= 3 origins (6501),
\* DomSmall every type of k <= 2 (194). Both are closed under HttpsTwin.
DomRich  == StairDom(<<1, 2, 3, 1, 2>>, <<1, 2, 3>>) \cup {Opq("n1"), Opq("n2"), Opq("n3")}
DomSmall == StairDom(<<1, 2, 0, 1, 0>>, <<0, 1, 2>>) \cup {Opq("n1"), Opq("n2")}
TupleOrigins  == {o \in Origins : ~o.op}
OpaquePool == {Opq("n1"), Opq("n2"), Opq("n3"), Opq("n4")}

\* --- The public suffix list as a parameter: host -> registrable domain or "null".
\* URL "registrable domain" (url.bs:838): null if the public suffix is null or
\* equals the host; IP addresses are not domains. "localhost" is its own public
\* suffix by the PSL default rule "*".
RegA == [h \in Hosts |->
          CASE h \in {"a.test", "x.a.test", "y.a.test"} -> "a.test"
            [] h \in {"b.test", "c.test", "b.localhost", "c.localhost"} -> h
            [] h \in {"a.localhost", "x.a.localhost", "y.a.localhost"} -> "a.localhost"
            [] OTHER -> "null"]
\* PSL B: "a.test" is a public suffix too (a shared-hosting suffix).
RegB == [RegA EXCEPT !["a.test"] = "null", !["x.a.test"] = "x.a.test", !["y.a.test"] = "y.a.test"]
Reg == RegA   \* replaced by RegB in the PSL-B .cfg
PSLAdmissible(reg) ==
  \A h \in Hosts : /\ (reg[h] # "null" => reg[h] \in Hosts /\ reg[reg[h]] = reg[h])
                   /\ (h \in IPHosts \/ h = "localhost" => reg[h] = "null")

\* --- Operators (HTML 7.1.1 Sites, html.src:94800-94915) -----------------------
SSSiteP(reg, a, b) ==   \* "schemelessly same site" (html.src:94870)
  IF a.op \/ b.op THEN a = b
  ELSE \/ a.host = b.host /\ reg[a.host] = "null"
       \/ reg[a.host] # "null" /\ reg[a.host] = reg[b.host]
SchemelesslySameSite(a, b) == SSSiteP(Reg, a, b)
ObtainSite(o) ==        \* "obtain a site" (html.src:94809)
  IF o.op THEN <<"opaque", o.id>>
  ELSE <<"site", o.scheme, IF Reg[o.host] = "null" THEN o.host ELSE Reg[o.host]>>
SameSiteHTML(a, b) == ObtainSite(a) = ObtainSite(b)   \* "same site" (html.src:94898)
\* Secure Contexts 3.1 "Is origin potentially trustworthy?" (no file:, no
\* configured or UA-authenticated schemes; UA follows let-localhost-be-localhost).
PTOrigin(o) == ~o.op /\ (o.scheme = "https" \/ o.host \in PTHosts)
SchemeHttps(o) == ~o.op /\ o.scheme = "https"
\* URLs as far as the model needs them: a network URL (by its origin), about:blank, data:.
NoOrigin == Opq("-")
NetUrl(o) == [kind |-> "net", o |-> o]
BlankUrl  == [kind |-> "blank", o |-> NoOrigin]
DataUrl   == [kind |-> "data", o |-> NoOrigin]
PTUrl(u) == IF u.kind \in {"blank", "data"} THEN TRUE ELSE PTOrigin(u.o)   \* Secure Contexts 3.2
\* HTML secure context (html.src:119312): top-level creation URL; data: is excluded.
SecureCtxR(ctx) ==
  IF Mutant = "false:secure-ctx-top" THEN Secure(ctx.self)
  ELSE ctx.topUrl.kind # "data" /\ PTUrl(ctx.topUrl)
\* A context now carries the top-level creation URL. An opaque top-level origin
\* (sandboxed, or about:blank without a creator) has its URL chosen from
\* OpaqueTopUrls; only PTUrl of it is read, so these four representatives
\* realize every case. TopCtx of an opaque origin uses about:blank.
OpaqueTopUrls == {NetUrl(TO("https", "a.test", "")), NetUrl(TO("http", "a.test", "")), BlankUrl, DataUrl}
TopUrls(t) == IF t.op THEN OpaqueTopUrls ELSE {NetUrl(t)}
TopCtxR(o) == [self |-> o, top |-> o, topUrl |-> IF o.op THEN BlankUrl ELSE NetUrl(o)]
ChildCtxR(pctx, r) == [self |-> r.origin, top |-> pctx.top, topUrl |-> pctx.topUrl]
ContextsR == UNION {{[self |-> s, top |-> t, topUrl |-> u] : u \in TopUrls(t)} : s \in Origins, t \in Origins}
ResponsesR == [origin : TupleOrigins, corp : CORPs, creds : BOOLEAN]

\* Agent cluster key (html.src:118254): obtain a site, or the origin itself.
\* An opaque origin is its own site, so both kinds give the same key.
KeyR(o, kind) == IF kind = "origin" /\ ~o.op THEN <<"tuple", o.scheme, o.host, o.port>>
                 ELSE ObtainSite(o)
\* The earlier readings, for comparison (tuple origins only).
KeyOld(o, kind) == IF kind = "origin" THEN o.host            \* SpecIsolation's Key
                   ELSE IF Reg[o.host] = "null" THEN o.host ELSE Reg[o.host]
KeyPrem(o, kind) == IF kind = "origin" THEN <<"origin", o.scheme, o.host>>   \* premises/ KeyHTML
                    ELSE <<"site", o.scheme, IF Reg[o.host] = "null" THEN o.host ELSE Reg[o.host]>>

\* Fetch "cross-origin resource policy internal check" (fetch.bs:4459). Same as
\* SpecIsolation's CorpInternal, but the same-site step's second condition is
\* on the scheme, which is no longer the same thing as Secure (= PTOrigin).
\* Mutant "corp-scheme-as-pt" uses trustworthiness instead.
CorpInternalR(o, coep, r, forNav) ==
  IF C("corp-nav", forNav /\ coep = "unsafe-none") THEN "allowed"
  ELSE
    LET p == IF C("corp-has-header", r.corp # "none") THEN r.corp
             ELSE CASE coep = "unsafe-none"    -> "none"
                    [] coep = "credentialless" ->
                         IF C("corp-cl-creds", r.creds \/ forNav) THEN "same-origin" ELSE "none"
                    [] coep = "require-corp"   -> "same-origin"
    IN IF C("corp-allow-kinds", p \in {"none", "cross-origin"}) THEN "allowed"
       ELSE IF p = "same-origin"
            THEN IF C("corp-so-check", SameOrigin(o, r.origin)) THEN "allowed" ELSE "blocked"
       ELSE IF C("corp-ss-site", SchemelesslySameSite(o, r.origin))
               /\ C("corp-ss-scheme", IF Mutant = "corp-scheme-as-pt"
                                      THEN Secure(o) \/ ~Secure(r.origin)
                                      ELSE SchemeHttps(o) \/ ~SchemeHttps(r.origin))
            THEN "allowed" ELSE "blocked"
\* Mixed Content 4.1: no upgrade when the URL's host is an IP address.
FetchResultDestR(ctx, coep, mode, dest, r, served) ==
  LET up == C("mc-upgrade", IsMixed(ctx, r) /\ dest = "image" /\ r.origin.host \notin IPHosts)
      rr == IF up THEN [r EXCEPT !.origin = HttpsTwin(r.origin)] ELSE r
  IN IF up /\ ~served THEN "error"
     ELSE IF C("mc-block", IsMixed(ctx, rr)) THEN "error"
     ELSE FetchResultPC(ctx, EffectiveCOEPCtx(ctx, coep), mode, rr)

\* --- Opaque origins: creation and inheritance --------------------------------
\* HTML "determine the origin" (html.src:107640) with the document state's
\* origin for about:blank and about:srcdoc set to the initiator's
\* (html.src:109569), and URL's blob: origin = the blob URL entry's
\* environment's origin (url.bs:3351). A new opaque origin is one not in used.
\* Mutant "opaque-constant": gen2's reading, one opaque value for all.
Fresh(used) == IF Mutant = "opaque-constant" THEN Opq("n1") ELSE CHOOSE x \in OpaquePool : x \notin used
Kinds == {"net", "blank", "srcdoc", "blob", "data"}
DocOrigin(kind, u, sandboxed, initiator, creator, used) ==
  IF sandboxed THEN Fresh(used)                       \* sandboxed origin browsing context flag
  ELSE CASE kind \in {"blank", "srcdoc"} -> initiator
         [] kind = "blob" -> creator
         [] kind = "data" -> Fresh(used)
         [] kind = "net"  -> u

\* --- Properties -------------------------------------------------------------
CorpPermitsP(reg, o, r) ==
  \/ r.corp = "cross-origin"
  \/ r.corp = "same-site" /\ SSSiteP(reg, o, r.origin) /\ (SchemeHttps(o) \/ ~SchemeHttps(r.origin))
CorpPermitsR(o, r) == CorpPermitsP(Reg, o, r)
\* TLC evaluates every constant-level definition without arguments at startup.
\* "dummy = 0 /\" makes the expensive ones state-level, so that only the
\* invariant being checked is evaluated. (The .cfg files also replace
\* SpecIsolation's expensive definitions by Off.)
Off == TRUE
OptInSecure == dummy = 0 /\ \A o \in Origins, r \in Responses :
  (Secure(o) /\ FetchResult(o, "require-corp", "no-cors", r) = "opaque") => CorpPermitsR(o, r)
OptInCtx == dummy = 0 /\ \A ctx \in Contexts, r \in Responses :
  (SecureCtx(ctx) /\ FetchResultCtx(ctx, "require-corp", "no-cors", r) = "opaque") => CorpPermitsR(ctx.self, r)
OptInPC == dummy = 0 /\ \A ctx \in Contexts, r \in Responses :
  FetchResultPC(ctx, "require-corp", "no-cors", r) = "opaque" => CorpPermitsR(ctx.self, r)
CtxWitness == CHOOSE x \in Contexts \X Responses : dummy = 0 /\
  SecureCtx(x[1]) /\ FetchResultCtx(x[1], "require-corp", "no-cors", x[2]) = "opaque" /\ ~CorpPermitsR(x[1].self, x[2])
COITop == dummy = 0 /\ \A o \in Origins, coop \in COOPs, coep \in COEPs, s \in Responses :
  LET ss == DocCreds(o, EffectiveCOEP(o, coep), "no-cors", s) IN
  (CrossOriginIsolated(coop, coep, o) /\ FetchResult(o, coep, "no-cors", s) = "opaque")
    => (~ss.creds \/ CorpPermitsR(o, s))
\* premises/ M3 premise (child same origin with its parent). Without a Mutant,
\* COI needs COOP same-origin and a COEP in CompatCOI, and the premise needs
\* r.origin = o, so the quantifiers are restricted to those values.
NestedBody(o, coep, r, ccoep, s) ==
  LET pctx == TopCtx(o) cctx == ChildCtx(pctx, r)
      ss == DocCreds(cctx.self, EffectiveCOEPCtx(cctx, ccoep), "no-cors", s)
  IN (CrossOriginIsolated("same-origin", coep, o) /\ NavChild(pctx, EffectiveCOEP(o, coep), r, ccoep) = "loaded")
     => /\ (SameOrigin(o, r.origin) \/ CorpPermitsR(o, r))
        /\ (FetchResultCtx(cctx, ccoep, "no-cors", s) = "opaque" => (~ss.creds \/ CorpPermitsR(cctx.self, s)))
NestedCap == dummy = 0 /\ \A o \in Origins, coep \in CompatCOI : \A r \in {x \in Responses : x.origin = o} :
                \A ccoep \in COEPs, s \in Responses : NestedBody(o, coep, r, ccoep, s)
\* The original (group-mode) premise, over every child response. Heavy.
NestedGroup == dummy = 0 /\ \A o \in {x \in TupleOrigins : PTOrigin(x)}, coep \in CompatCOI, r \in Responses,
                  ccoep \in COEPs, s \in Responses : NestedBody(o, coep, r, ccoep, s)

\* Agent cluster keys under isolation: distinct origins, distinct clusters.
KeyCOI(K(_, _), D) == \A o1, o2 \in D :
  o1 # o2 => K(o1, KeyKind(o1, "concrete", "absent", FALSE)) # K(o2, KeyKind(o2, "concrete", "absent", FALSE))
KeyCOIWitness(K(_, _), D) == CHOOSE x \in D \X D :
  x[1] # x[2] /\ K(x[1], KeyKind(x[1], "concrete", "absent", FALSE)) = K(x[2], KeyKind(x[2], "concrete", "absent", FALSE))
\* Site keys are exactly HTML "same site" (ports and subdomains share, schemes do not).
KeySite == \A o1, o2 \in Origins : (KeyR(o1, "site") = KeyR(o2, "site")) <=> SameSiteHTML(o1, o2)

\* PSL variance: the client computes sites with Reg; the response's author
\* meant CORP same-site under PSL B (RegB). Run with Reg = RegA and RegB.
CrossPSL == dummy = 0 /\ \A o \in Origins, r \in Responses :
  (Secure(o) /\ FetchResult(o, "require-corp", "no-cors", r) = "opaque") => CorpPermitsP(RegB, o, r)
CrossPSLWitness == CHOOSE x \in Origins \X Responses : dummy = 0 /\
  Secure(x[1]) /\ FetchResult(x[1], "require-corp", "no-cors", x[2]) = "opaque" /\ ~CorpPermitsP(RegB, x[1], x[2])

\* (One cross-spec property is withheld from this repository until checked.)

\* Opaque origins. A sandboxed (or data:) document's origin is new: equal to,
\* same site with, and in an agent cluster with no existing origin.
\* (u, the network URL's origin, is read only for kind "net" unsandboxed, so it is fixed.)
FreshIsolated == \A kind \in Kinds, sb \in BOOLEAN, i, c \in Origins :
  (sb \/ kind = "data") =>
    LET d == DocOrigin(kind, TO("https", "a.test", ""), sb, i, c, Origins) IN
    \A x \in Origins, k1, k2 \in {"origin", "site"} :
      d # x /\ ~SchemelesslySameSite(d, x) /\ KeyR(d, k1) # KeyR(x, k2)
FreshWitness == CHOOSE x \in Kinds \X Origins \X Origins :
  LET d == DocOrigin(x[1], TO("https", "a.test", ""), TRUE, x[2], x[2], Origins) IN d = x[3]
\* Content written by an opaque-origin document (about:blank or srcdoc it
\* initiated, a blob: it created, data:) never gets a tuple origin.
OpaqueStaysOpaque == \A kind \in Kinds, sb \in BOOLEAN, i, c \in Origins :
  ((kind \in {"blank", "srcdoc", "data"} /\ i.op) \/ (kind = "blob" /\ c.op))
    => DocOrigin(kind, TO("https", "a.test", ""), sb, i, c, Origins).op
\* about:blank / srcdoc child of a cross-origin isolated top-level document:
\* no navigation response and no COEP header; it inherits the initiator's
\* policy container (Mutant "no-pc-inherit": header only, so unsafe-none).
InhBody(o, coep, kind, sb, s) ==
  LET c    == DocOrigin(kind, o, sb, o, o, Origins)
      cctx == [self |-> c, top |-> o, topUrl |-> NetUrl(o)]
      cec  == IF Mutant = "no-pc-inherit" THEN "unsafe-none" ELSE EffectiveCOEP(o, coep)
      ss   == DocCreds(c, EffectiveCOEPCtx(cctx, cec), "no-cors", s)
  IN (CrossOriginIsolated("same-origin", coep, o) /\ FetchResultCtx(cctx, cec, "no-cors", s) = "opaque")
     => (~ss.creds \/ CorpPermitsR(c, s))
InheritedCOI == dummy = 0 /\ \A o \in TupleOrigins, coep \in CompatCOI, kind \in {"blank", "srcdoc"},
                   sb \in BOOLEAN, s \in Responses : InhBody(o, coep, kind, sb, s)
InheritedWitness == CHOOSE x \in TupleOrigins \X CompatCOI \X {"blank", "srcdoc"} \X BOOLEAN \X Responses :
  dummy = 0 /\ ~InhBody(x[1], x[2], x[3], x[4], x[5])

\* --- Witness values (single scenarios) --------------------------------------
A0 == TO("https", "a.test", "")  A8 == TO("https", "a.test", "8443")
R(o, c) == [origin |-> o, corp |-> c, creds |-> FALSE]
Values == <<
  <<"port: same origin", SameOrigin(A0, A8), "same site", SameSiteHTML(A0, A8)>>,
  <<"port: rc fetch CORP none", FetchResult(A0, "require-corp", "no-cors", R(A8, "none")),
    "CORP same-site", FetchResult(A0, "require-corp", "no-cors", R(A8, "same-site"))>>,
  <<"port: popup COOP so/so severed", PopupSevered("same-origin", A0, "same-origin", A8)>>,
  <<"port: site keys equal", KeyR(A0, "site") = KeyR(A8, "site"),
    "old origin keys equal", KeyOld(A0, "origin") = KeyOld(A8, "origin"),
    "premises KeyHTML origin keys equal", KeyPrem(A0, "origin") = KeyPrem(A8, "origin")>>,
  <<"psl: x.a.test ~ y.a.test", SchemelesslySameSite(TO("https", "x.a.test", ""), TO("https", "y.a.test", ""))>>,
  <<"localhost: COI http://localhost", CrossOriginIsolated("same-origin", "require-corp", TO("http", "localhost", "")),
    "COI http://127.0.0.1", CrossOriginIsolated("same-origin", "require-corp", TO("http", "127.0.0.1", "")),
    "COI http://a.test", CrossOriginIsolated("same-origin", "require-corp", TO("http", "a.test", ""))>>,
  <<"localhost: https://a.test fetch http://127.0.0.1", FetchResult(A0, "unsafe-none", "no-cors", R(TO("http", "127.0.0.1", ""), "none")),
    "http://192.0.2.1", FetchResult(A0, "unsafe-none", "no-cors", R(TO("http", "192.0.2.1", ""), "none")),
    "img http://192.0.2.1 (no upgrade)", ImageResult(A0, "unsafe-none", R(TO("http", "192.0.2.1", ""), "none"), TRUE),
    "img http://b.test (upgraded)", ImageResult(A0, "unsafe-none", R(TO("http", "b.test", ""), "none"), TRUE)>>,
  <<"localhost: http://localhost rc CORP same-site from https://localhost",
    FetchResult(TO("http", "localhost", ""), "require-corp", "no-cors", R(TO("https", "localhost", ""), "same-site"))>>
>>

PrintOS == PrintT(<<"originstruct", Mutant, "PSL", IF Reg = RegA THEN "A" ELSE "B",
  "|Origins|", Cardinality(Origins), "admissible", PSLAdmissible(Reg),
  <<"OptInSecure", OptInSecure>>,
  <<"OptInCtx", OptInCtx, IF OptInCtx THEN "-" ELSE CtxWitness>>,
  <<"OptInPC", OptInPC>>,
  <<"COITop", COITop>>,
  <<"NestedCap", NestedCap>>,
  <<"KeyCOI KeyR", KeyCOI(KeyR, Origins)>>,
  <<"KeyCOI old Key", KeyCOI(KeyOld, TupleOrigins), KeyCOIWitness(KeyOld, TupleOrigins)>>,
  <<"KeyCOI premises KeyHTML", KeyCOI(KeyPrem, TupleOrigins), KeyCOIWitness(KeyPrem, TupleOrigins)>>,
  <<"KeySite", KeySite>>,
  <<"CrossPSL (intended B)", CrossPSL, IF CrossPSL THEN "-" ELSE CrossPSLWitness>>,
  <<"FreshIsolated", FreshIsolated, IF FreshIsolated THEN "-" ELSE FreshWitness>>,
  <<"OpaqueStaysOpaque", OpaqueStaysOpaque>>,
  <<"InheritedCOI", InheritedCOI, IF InheritedCOI THEN "-" ELSE InheritedWitness>>,
  Values>>)
\* One property at a time: the .cfg replaces Target (CONSTANT Target <- OptInCtx).
Target == TRUE
PrintTarget == PrintT(<<"target", Mutant, IF Reg = RegA THEN "A" ELSE "B", Cardinality(Origins), Target>>)
\* The heavy and the flow properties, for the smaller domain.
\* SpecIsolation's flow properties over the new operators, guarded (see Off).
NoHeaderLeakR == dummy = 0 /\ \A o \in Origins, coep \in COEPs, r1, r2 \in Responses :
    (r1.origin = r2.origin /\ r1.creds = r2.creds /\ ~SameOrigin(o, r1.origin)) =>
      FetchResult(o, coep, "no-cors", r1) = FetchResult(o, coep, "no-cors", r2)
FlowResponsesR == [origin : TupleOrigins, corp : CORPs, creds : BOOLEAN, acao : BOOLEAN, body : Bodies]
BodyOnlyByOptInR == dummy = 0 /\ \A o \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"}, r \in FlowResponsesR :
    (~SameOrigin(o, r.origin) /\ Observe(o, coep, mode, r)[1] = "read") => r.acao
PrintHeavy == PrintT(<<"heavy", Mutant, Cardinality(Origins),
  <<"NestedGroup", NestedGroup>>, <<"NoHeaderLeak", NoHeaderLeakR>>,
  <<"BodyOnlyByOptIn", BodyOnlyByOptInR>>>>)
================================================================================
