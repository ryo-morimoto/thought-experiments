---- MODULE ORBExtension ----
\* Opaque Response Blocking (ORB) added to the no-cors path of SpecIsolation,
\* and the question: what must Declared contain for NoUndeclaredLeak to hold?
\* ORB is not in the Fetch Standard at commit d7fc0fd (no "opaque-response"
\* text there; HTML only links github.com/annevk/orb). The steps below follow
\* the "opaque-response-safelist check" in whatwg/fetch PR #1442 (preview
\* https://whatpr.org/fetch/1442.html, section #orb-algorithm). See ORB-NOTES.md.
\* In the PR the check runs in HTTP fetch BEFORE the CORP check; both give a
\* network error, so the order does not change what the page observes.
EXTENDS SpecIsolation, FiniteSets

\* --- Abstract response fields ------------------------------------------------
\* Extracted MIME type, by the class ORB distinguishes:
\*   "safe"   opaque-response-safelisted (JavaScript, text/css, image/svg+xml)
\*   "block"  opaque-response-blocklisted (HTML, JSON, XML)
\*   "never"  opaque-response-blocklisted-never-sniffed (pdf, zip, csv, ...)
\*   "plain"  essence text/plain
\*   "avimg"  essence starts with audio/, image/ or video/
\*   "other"  any other parsable type (e.g. application/octet-stream)
\*   "none"   extraction failure (no or bad Content-Type)
Mimes    == {"safe", "block", "never", "plain", "avimg", "other", "none"}
Statuses == {"200", "206", "404"}          \* 206 is an ok status; 404 is not
\* Requester side: the request's no-cors media request state.
MediaStates == {"N/A", "initial", "subsequent"}
\* A body is a secret plus two predicates of its bytes:
\*   head  - what the first 1024 bytes sniff as: audio/video, image, neither
\*   parse - "js" (parses as a Script and not as JSON), "json", "neither"
ORBBodies == [secret : Bodies, head : {"av", "img", "text"},
              parse : {"js", "json", "neither"}]
ORBResponsesAt(ro) ==
  [origin : {ro}, corp : CORPs, creds : BOOLEAN, acao : BOOLEAN, body : ORBBodies,
   mime : Mimes, nosniff : BOOLEAN, status : Statuses]

\* --- The opaque-response-safelist check (PR #1442) ---------------------------
\* Assumptions: a 206 always passes "validate a partial response"; reading the
\* first 1024 bytes never fails; the JavaScript parse is the body's "parse".
\* Stage 1 (steps on headers and status only): "allow", "block" or "body".
ORBHeaderStage(ms, r) ==
  IF r.mime = "safe" THEN "allow"
  ELSE IF r.mime = "never" THEN "block"
  ELSE IF r.status = "206" /\ r.mime = "block" THEN "block"
  ELSE IF r.nosniff /\ r.mime \in {"block", "plain"} THEN "block"
  ELSE IF ms = "subsequent" THEN "allow"
  ELSE "body"
\* Stage 2: sniffing interleaved with more header checks.
ORBBodyStage(ms, r) ==
  IF r.body.head = "av" THEN ms = "initial" /\ r.status \in {"200", "206"}
  ELSE IF ms # "N/A" THEN FALSE
  ELSE IF r.body.head = "img" THEN TRUE
  ELSE IF r.nosniff THEN FALSE
  ELSE IF r.status = "404" THEN FALSE
  ELSE IF r.mime = "none" THEN TRUE
  ELSE IF r.mime = "avimg" THEN FALSE
  ELSE r.body.parse = "js"
ORBAllows(ms, r) ==
  LET s == ORBHeaderStage(ms, r) IN
  IF s = "allow" THEN TRUE ELSE IF s = "block" THEN FALSE ELSE ORBBodyStage(ms, r)

\* --- Observation with ORB -----------------------------------------------------
ObserveORB(o, coep, mode, ms, r) ==
  IF SameOrigin(o, r.origin) THEN <<"read", r.body>>
  ELSE IF mode = "cors" THEN (IF r.acao THEN <<"read", r.body>> ELSE <<"error">>)
  ELSE IF ~ORBAllows(ms, r) THEN <<"error">>
  ELSE IF CorpCheck(o, EffectiveCOEP(o, coep),
                    DocCreds(o, EffectiveCOEP(o, coep), mode, Base(r)), FALSE) = "blocked"
       THEN <<"error">>
  ELSE <<"opaque">>

\* --- Declared variants ---------------------------------------------------------
NC(mode, x) == IF mode = "no-cors" THEN x ELSE "n/a"
Hdr(r) == <<r.mime, r.nosniff, r.status>>
D0(mode, ms, r)      == Declared(mode, r)                                 \* unchanged
DHdr(mode, ms, r)    == <<Declared(mode, r), Hdr(r)>>                     \* + headers/status
DVerdict(mode, ms, r) == <<Declared(mode, r), NC(mode, ORBAllows(ms, r))>> \* + verdict bit only
DHdrHead(mode, ms, r) == <<Declared(mode, r), Hdr(r), r.body.head>>       \* + sniff only
DHdrParse(mode, ms, r) == <<Declared(mode, r), Hdr(r), r.body.parse>>     \* + parse only
DHdrBoth(mode, ms, r) == <<Declared(mode, r), Hdr(r), r.body.head, r.body.parse>>
\* + the verdict only when ORB had to look at the body (the genuinely
\* body-dependent part); "n/a" when headers and status decided.
BodyBit(mode, ms, r) ==
  IF mode = "cors" \/ ORBHeaderStage(ms, r) # "body" THEN "n/a" ELSE ORBBodyStage(ms, r)
DHdrBodyBit(mode, ms, r) == <<Declared(mode, r), Hdr(r), BodyBit(mode, ms, r)>>

\* NoUndeclaredLeak restated: Observe is a function of D within each context.
\* (Same as the pairwise form, checked as: no declared value maps to two
\* observations.)
NI(D(_, _, _)) ==
  \A o, ro \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"}, ms \in MediaStates :
    ~SameOrigin(o, ro) =>
      LET S == {<<D(mode, ms, r), ObserveORB(o, coep, mode, ms, r)>> : r \in ORBResponsesAt(ro)}
      IN Cardinality({p[1] : p \in S}) = Cardinality(S)

\* A witness for D0: same declarations, different observation.
WitnessSet == {r \in ORBResponsesAt(OB) : r.corp = "none" /\ ~r.creds /\ ~r.acao}
ORBWitness ==
  CHOOSE p \in WitnessSet \X WitnessSet :
    /\ D0("no-cors", "N/A", p[1]) = D0("no-cors", "N/A", p[2])
    /\ ObserveORB(OA, "unsafe-none", "no-cors", "N/A", p[1])
       # ObserveORB(OA, "unsafe-none", "no-cors", "N/A", p[2])
    /\ Hdr(p[1]) = Hdr(p[2])        \* so that only the body differs
\* The same, where the bodies differ only in whether they parse as JavaScript.
ORBWitnessJS ==
  CHOOSE p \in WitnessSet \X WitnessSet :
    /\ Hdr(p[1]) = Hdr(p[2])
    /\ p[1].body.head = "text" /\ p[2].body.head = "text"
    /\ p[1].body.secret = p[2].body.secret
    /\ ObserveORB(OA, "unsafe-none", "no-cors", "N/A", p[1])
       # ObserveORB(OA, "unsafe-none", "no-cors", "N/A", p[2])

\* --- How much the body-dependent part reveals --------------------------------
\* For one response the page can vary only its own request (the media state).
\* The body-dependent information is the vector of verdicts over media states.
VerdictVec(r) == <<ORBAllows("N/A", r), ORBAllows("initial", r), ORBAllows("subsequent", r)>>
HeaderCombos == Mimes \X BOOLEAN \X Statuses
WithHdr(h, b) == [origin |-> OB, corp |-> "none", creds |-> FALSE, acao |-> FALSE,
                  body |-> b, mime |-> h[1], nosniff |-> h[2], status |-> h[3]]
VecsFor(h) == {VerdictVec(WithHdr(h, b)) : b \in ORBBodies}
MaxBodyClasses == LET n == {Cardinality(VecsFor(h)) : h \in HeaderCombos}
                  IN CHOOSE m \in n : \A k \in n : k <= m
AllVecs == UNION {VecsFor(h) : h \in HeaderCombos}
\* Do two bodies with the same secret but different predicates ever differ,
\* and two bodies with the same predicates but different secrets never?
SecretIrrelevant ==
  \A h \in HeaderCombos, b1, b2 \in ORBBodies :
    (b1.head = b2.head /\ b1.parse = b2.parse) =>
      VerdictVec(WithHdr(h, b1)) = VerdictVec(WithHdr(h, b2))

\* --- Access control still holds: ORB only adds blocks --------------------------
ORBOnlyBlocks ==
  \A o, ro \in Origins, coep \in COEPs, ms \in MediaStates : \A r \in ORBResponsesAt(ro) :
    ObserveORB(o, coep, "no-cors", ms, r) = <<"opaque">> =>
      Observe(o, coep, "no-cors", r) = <<"opaque">>
OptInOnlySecureORB ==
  \A o, ro \in Origins, ms \in MediaStates : \A r \in ORBResponsesAt(ro) :
    (Secure(o) /\ ~SameOrigin(o, ro)
     /\ ObserveORB(o, "require-corp", "no-cors", ms, r) = <<"opaque">>) =>
      \/ r.corp = "cross-origin"
      \/ r.corp = "same-site" /\ SameSite(o, r.origin)
BodyOnlyByOptInORB ==
  \A o, ro \in Origins, coep \in COEPs, mode \in {"cors", "no-cors"}, ms \in MediaStates :
    \A r \in ORBResponsesAt(ro) :
    (~SameOrigin(o, ro) /\ ObserveORB(o, coep, mode, ms, r)[1] = "read") => r.acao

PrintORB == PrintT(<<"orb",
  <<"ni-D0", NI(D0)>>,
  <<"ni-hdr", NI(DHdr)>>,
  <<"ni-verdict", NI(DVerdict)>>,
  <<"ni-hdr-head", NI(DHdrHead)>>,
  <<"ni-hdr-parse", NI(DHdrParse)>>,
  <<"ni-hdr-head-parse", NI(DHdrBoth)>>,
  <<"ni-hdr-bodybit", NI(DHdrBodyBit)>>,
  <<"witness-D0", ORBWitness,
    ObserveORB(OA, "unsafe-none", "no-cors", "N/A", ORBWitness[1]),
    ObserveORB(OA, "unsafe-none", "no-cors", "N/A", ORBWitness[2])>>,
  <<"witness-D0-js", ORBWitnessJS[1].body, ORBWitnessJS[2].body, Hdr(ORBWitnessJS[1]),
    ObserveORB(OA, "unsafe-none", "no-cors", "N/A", ORBWitnessJS[1]),
    ObserveORB(OA, "unsafe-none", "no-cors", "N/A", ORBWitnessJS[2])>>,
  <<"max-body-classes-per-header", MaxBodyClasses>>,
  <<"all-verdict-vectors", AllVecs>>,
  <<"secret-irrelevant", SecretIrrelevant>>,
  <<"orb-only-blocks", ORBOnlyBlocks>>,
  <<"optin-only-secure", OptInOnlySecureORB>>,
  <<"body-only-by-optin", BodyOnlyByOptInORB>>>>)
====
