------------------------------- MODULE Params ---------------------------------
(* Node C7 of plan/browser-semantics-soundness/TREE.md, record              *)
(* experiments/2026-11-24-divergence-config-catalog.md. Deployment values   *)
(* for the version- and configuration-dependent choices in catalog/*.tsv.   *)
(* No existing module is changed. Each operator says which existing         *)
(* constant it feeds:                                                       *)
(*   OACParam(d)   -> gen2/Gen2Model.tla CONSTANT OACParam                  *)
(*   COIChoices(d) -> the COIChoice set of observe/, gen/, gen2/, redirect/ *)
(*                    (SpecIsolation Mutant "param:coi-logical" = logical)  *)
(*   Supported(d)  -> Unsupported.tla CONSTANT Supported                    *)
(*   MCUpgradeImg(d) -> fixes/ step mc-upgrade (FALSE = Mutant false:...)   *)
(* PARAMETERS are values a browser picked where a merged or shipped         *)
(* proposal exists. PREMISES are choices the spec leaves to the UA; they    *)
(* are listed so a proof can name the value it assumes, and the spec-level *)
(* model keeps the nondeterministic envelope.                               *)
(* "unknown" means not observed and not checked in a primary source.        *)
EXTENDS FiniteSets, TLC

Deployments == {"chrome158-desktop", "chrome158-android-2gb",
                "chrome158-android-lowmem", "android-webview", "chrome-ios",
                "firefox160-desktop", "safari27.2-macos"}

Features == {"credentialless", "coop", "oac", "dip", "nap"}
Unknown  == "unknown"

\* ---------------------------------------------------------------- PARAMETERS

\* P-OAC. "spec": requestsOAC only for ?1 (HTML now). "7617": absent header
\* in a secure context is origin-keyed (whatwg/html#7617, open, shipped by
\* Chromium). Chrome 158 and Firefox 160 observed in gen2/ (13 O rows).
\* Enterprise policy OriginAgentClusterDefaultEnabled = Disabled gives "spec".
OACParam(d) ==
  CASE d \in {"chrome158-desktop", "chrome158-android-2gb",
              "chrome158-android-lowmem"} -> "7617"
    [] d = "firefox160-desktop"           -> "spec"
    [] OTHER                              -> Unknown
OACParamWithPolicy(d, policyEnabled) ==
  IF d \in {"chrome158-desktop", "chrome158-android-2gb",
            "chrome158-android-lowmem"} /\ ~policyEnabled
  THEN "spec" ELSE OACParam(d)

\* P-SUP. Features read from headers. A feature outside the set is read as
\* the header being absent (Unsupported.tla). Values from observations,
\* primary sources or recall, per configs.tsv.
Supported(d) ==
  CASE d = "chrome158-desktop"  -> Features
    [] d = "firefox160-desktop" -> {"credentialless", "coop", "oac"}
    [] d = "android-webview"    -> {"credentialless", "oac", "dip", "nap"}
    [] OTHER                    -> Features  \* all unsettled, see below
\* Features whose membership is not settled for d (recalled or unobserved).
SupportedUnsettled(d) ==
  CASE d = "chrome158-desktop"  -> {"nap"}
    [] d = "firefox160-desktop" -> {"nap"}
    [] d = "android-webview"    -> {"credentialless", "oac", "dip", "nap"}
    [] OTHER                    -> Features
\* Chrome with --disable-features=CrossOriginOpenerPolicy (coop-detect/).
SupportedWithFlags(d, coopDisabled) ==
  IF coopDisabled THEN Supported(d) \ {"coop"} ELSE Supported(d)

\* P-MC. Mixed Content 4.1 upgrade of http images (port kept).
MCUpgradeImg(d) ==
  CASE d \in {"chrome158-desktop", "firefox160-desktop"} -> "yes"
    [] OTHER                                             -> Unknown

\* P-SERVED. Not a browser value: whether a TLS server answers at the
\* upgraded URL (fixes/ ImageResult). wptserve's default ports give FALSE.
ServedAtUpgradedURL(host) == IF host = "wptserve-default" THEN "no" ELSE Unknown

\* ------------------------------------------------------------------ PREMISES

\* Q-COI. HTML: "The choice of which is implementation-defined." Spec-level
\* proofs use {"concrete", "logical"}; observed deployments pick concrete.
COIChoices(d) ==
  CASE d \in {"chrome158-desktop", "firefox160-desktop"} -> {"concrete"}
    [] d = "safari27.2-macos"                            -> {"concrete"}
    [] OTHER                                             -> {"concrete", "logical"}
SpecCOIChoices == {"concrete", "logical"}

\* Q-PROC. Process placement. "full": every site in its own locked process;
\* "partial": only sites that met a trigger (password, OAuth, COOP);
\* "none": no out-of-process iframes. SiteIsolation's L (LateLock-*.cfg).
ProcessIsolation(d) ==
  CASE d = "chrome158-desktop"        -> "full"
    [] d = "chrome158-android-2gb"    -> "partial"
    [] d \in {"chrome158-android-lowmem", "android-webview",
              "chrome-ios"}           -> "none"
    [] OTHER                          -> Unknown
\* SitePerProcessAndroid = Enabled forces full isolation on Android.
ProcessIsolationWithPolicy(d, sppAndroid) ==
  IF d = "chrome158-android-2gb" /\ sppAndroid THEN "full" ELSE ProcessIsolation(d)
\* OAC is a hint for process placement, never a guarantee (Chromium doc).
OACPlacesProcess(d) == FALSE

\* Q-SAB. Enterprise policy SharedArrayBufferUnrestrictedAccessAllowed
\* (Chrome and ChromeOS 91-). TRUE breaks the capability/restriction link:
\* SAB without crossOriginIsolated. Default not set = FALSE.
SABWithoutCOI(d, policyEnabled) ==
  d = "chrome158-desktop" /\ policyEnabled

\* Q-SWAP. Optional BCG swap, case (c) ("group size 1"). Chrome 158: a
\* function of observable state (bcg-observe/, 36 runs). Others unsettled.
ChromeSwaps(groupSize, bfcacheEligible) == groupSize = 1 /\ bfcacheEligible
OptionalSwap(d, groupSize, bfcacheEligible) ==
  IF d = "chrome158-desktop" THEN {ChromeSwaps(groupSize, bfcacheEligible)}
  ELSE IF groupSize = 1 THEN {TRUE, FALSE} ELSE {FALSE}

\* ------------------------------------------------------------------ checks
ASSUME \A d \in Deployments :
         /\ OACParam(d) \in {"spec", "7617", Unknown}
         /\ COIChoices(d) \subseteq SpecCOIChoices /\ COIChoices(d) # {}
         /\ Supported(d) \subseteq Features
         /\ SupportedUnsettled(d) \subseteq Features
         /\ ProcessIsolation(d) \in {"full", "partial", "none", Unknown}
         /\ MCUpgradeImg(d) \in {"yes", "no", Unknown}
\* A deployment's choice is inside the spec envelope.
ASSUME \A d \in Deployments, g \in {1, 2}, b \in BOOLEAN :
         OptionalSwap(d, g, b) \subseteq (IF g = 1 THEN BOOLEAN ELSE {FALSE})

PrintTable ==
  PrintT([d \in Deployments |->
           [oac |-> OACParam(d), coi |-> COIChoices(d), sup |-> Supported(d),
            unsettled |-> SupportedUnsettled(d), proc |-> ProcessIsolation(d),
            mcimg |-> MCUpgradeImg(d)]])

VARIABLE x
Init == x = 0 /\ PrintTable
Next == UNCHANGED x
Spec == Init /\ [][Next]_x
================================================================================
