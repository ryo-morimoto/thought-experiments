------------------------------ MODULE MutKill ---------------------------------
(* adequacy/RESULTS.md: for every mutant of ../SpecIsolation.tla, which of  *)
(* its properties fail, and its Signature class, on the domain the .cfg     *)
(* gives (Origins <- [SpecIsolation] D18 overrides SpecIsolation's Origins; *)
(* SigDom is the Signature's domain, AllOrigins by default).                *)
EXTENDS Naturals, Sequences, FiniteSets, TLC, Domains
VARIABLE dummy
K(m) == INSTANCE SpecIsolation WITH Mutant <- m
B == INSTANCE SpecIsolation WITH Mutant <- "none"
Ms == B!Mutants \cup B!FlowMutants
      \cup {p \o d : p \in {"neg:", "false:", "true:"}, d \in B!DecisionIds}
\* Properties, as SpecIsolation states them (over its Origins).
PropNames == <<"OptInOnlySecure", "OptInOnlySecureCtx", "OptInOnlyPC",
               "COIOnlyWithOptInTop", "COIOnlyWithOptInNested", "NoUndeclaredLeak",
               "BodyOnlyByOptIn">>
\* Without the nested property (it is checked by NestedSym on large domains).
PropNamesNoNested == <<"OptInOnlySecure", "OptInOnlySecureCtx", "OptInOnlyPC",
               "COIOnlyWithOptInTop", "NoUndeclaredLeak", "BodyOnlyByOptIn">>
\* COIOnlyWithOptInNested with the top-level origin o restricted to Reps.
\* The body is SpecIsolation's, unchanged. Every operator it uses sees
\* origins only through =, .site and .scheme (and HttpsTwin, which is not
\* reached from fetch()), so on a domain that is a product of sites x hosts
\* x schemes every o is mapped onto a member of Reps by a permutation of
\* sites and of hosts within a site that preserves the property.
RepsAll == B!Origins
Reps == {Og("https", "a.test", "a.test"), Og("http", "a.test", "a.test")}
NestedSym(m) ==
  \A o \in Reps, coop \in B!COOPs, coep \in B!COEPs, r \in B!Responses,
     ccoep \in B!COEPs, s \in B!Responses :
    LET pctx == K(m)!TopCtx(o)
        cctx == K(m)!ChildCtx(pctx, r)
        cec  == K(m)!EffectiveCOEPCtx(cctx, ccoep)
        ss   == K(m)!DocCreds(cctx.self, cec, "no-cors", s)
    IN (K(m)!CrossOriginIsolated(coop, coep, o)
        /\ K(m)!NavChild(pctx, K(m)!EffectiveCOEP(o, coep), r, ccoep) = "loaded")
       => /\ (K(m)!SameOrigin(o, r.origin) \/ K(m)!HasOptIn(o, r))
          /\ (K(m)!FetchResultCtx(cctx, ccoep, "no-cors", s) = "opaque"
                => (~ss.creds \/ K(m)!HasOptIn(cctx.self, s)))
NestedKills == {m \in Ms : ~NestedSym(m)}
PrintNested == /\ PrintT(<<"nested-sym", Cardinality(B!Origins), "none", NestedSym("none")>>)
               /\ PrintT(<<"nested-kills", NestedKills>>)
Prop(m, p) ==
  CASE p = "OptInOnlySecure" -> K(m)!OptInOnlySecure
    [] p = "OptInOnlySecureCtx" -> K(m)!OptInOnlySecureCtx
    [] p = "OptInOnlyPC" -> K(m)!OptInOnlyPC
    [] p = "COIOnlyWithOptInTop" -> K(m)!COIOnlyWithOptInTop
    [] p = "COIOnlyWithOptInNested" -> K(m)!COIOnlyWithOptInNested
    [] p = "NoUndeclaredLeak" -> K(m)!NoUndeclaredLeak
    [] OTHER -> K(m)!BodyOnlyByOptIn
Fails(m) == {PropNames[i] : i \in {j \in 1..Len(PropNames) : ~Prop(m, PropNames[j])}}
\* Signature (SpecIsolation's four operators) over SigDom.
SigDom == B!AllOrigins
SigResp == [origin : SigDom, corp : B!CORPs, creds : BOOLEAN]
Sig(m) ==
  <<[x \in B!COOPs \X B!COEPs \X SigDom |-> K(m)!CrossOriginIsolated(x[1], x[2], x[3])],
    [x \in SigDom \X {"none", "concrete"} \X {"absent", "site", "origin"} \X BOOLEAN
        |-> K(m)!KeyKind(x[1], x[2], x[3], x[4])],
    [x \in B!COOPs \X SigDom \X B!COOPs \X SigDom |-> K(m)!PopupSevered(x[1], x[2], x[3], x[4])],
    [x \in SigDom \X B!COEPs \X {"cors", "no-cors"} \X SigResp
        |-> K(m)!FetchResult(x[1], x[2], x[3], x[4])]>>
SigTab == [m \in Ms \cup {"none"} |-> Sig(m)]
EquivNone == {m \in Ms : SigTab[m] = SigTab["none"]}
\* Classes of mutants with equal signatures (size > 1 only).
Classes == {{m2 \in Ms : SigTab[m2] = SigTab[m]} : m \in Ms}
Print1 ==
  /\ PrintT(<<"domain", Cardinality(B!Origins), "sigdom", Cardinality(SigDom), "mutants", Cardinality(Ms)>>)
  /\ PrintT(<<"fails-none", Fails("none")>>)
  /\ PrintT(<<"kills", {<<m, Fails(m)>> : m \in {m \in Ms : Fails(m) # Fails("none")}}>>)
  /\ PrintT(<<"equiv-none", EquivNone>>)
  /\ PrintT(<<"nclasses", Cardinality(Classes)>>)
  /\ PrintT(<<"classes>1", {c \in Classes : Cardinality(c) > 1}>>)
Init == dummy = 0
Next == UNCHANGED dummy
Spec == Init /\ [][Next]_dummy
===============================================================================
