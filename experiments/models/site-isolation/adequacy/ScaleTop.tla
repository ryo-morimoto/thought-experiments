------------------------------ MODULE ScaleTop --------------------------------
(* adequacy/RESULTS.md: SpecIsolation's own properties, unchanged, with the  *)
(* definition Origins overridden by a larger domain in the .cfg             *)
(* (CONSTANT Origins <- D18). Contexts, Responses and FlowResponses are     *)
(* defined from Origins, so they follow.                                     *)
EXTENDS SpecIsolation, Domains, FiniteSets
PrintProps == PrintT(<<"props", Mutant, Cardinality(Origins),
  <<"OptInOnlySecure", OptInOnlySecure>>,
  <<"OptInOnlySecureLifted", OptInOnlySecureLifted>>,
  <<"OptInOnlySecureCtx", OptInOnlySecureCtx>>,
  <<"OptInOnlyPC", OptInOnlyPC>>,
  <<"COIOnlyWithOptInTop", COIOnlyWithOptInTop>>,
  <<"NoUndeclaredLeak", NoUndeclaredLeak>>,
  <<"BodyOnlyByOptIn", BodyOnlyByOptIn>>,
  <<"NoHeaderLeak", NoHeaderLeak>>,
  <<"OptInOnly", OptInOnly>>>>)
PrintNested == PrintT(<<"nested", Mutant, Cardinality(Origins), COIOnlyWithOptInNested>>)
===============================================================================
