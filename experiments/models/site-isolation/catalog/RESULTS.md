# Divergences and version/configuration choices: parameter, defect or premise

Catalogue for the record
[experiments/2026-11-24-divergence-config-catalog.md](../../../2026-11-24-divergence-config-catalog.md)
(tree nodes C4, C7). A subagent wrote it on 2026-11-24. No existing file was edited. Nothing is committed.

## Decision rule (from the record)

- **PARAMETER**: a merged spec change, or a proposal that has shipped. Its value is a deployment assumption.
- **BROWSER DEFECT**: a public failing test exists and the behaviour is contrary to the spec.
- **MODEL PREMISE**: the choice varies by version or configuration, and the spec delegates it to the implementation.
- **UNDECIDED (R2)**: the rule gives no class, or gives two.

## Sources and how they were checked

- wpt.fyi stable runs (API `runs?label=stable&max-count=1`, fetched 2026-11-24): Chrome 158.0.8127.36
  run 6313827378135040, Firefox 160.0.1 run 5108994293891072, Safari 27.2 run 6234878279155712, all at
  rev e00a7b14e8 (2026-11-23). The responses are not committed. sha256: runs `997ff08c…b1fe`,
  COI permission iframe `16a59dde…bc0`, SAP redirect `eed14913…4c1`, scheme-restriction `37a5dfc5…a0b8`,
  OAC `10f8211f…f10b`, window.name `24c3ad68…4787`.
- Fetched 2026-11-24: whatwg/html#7617 (GitHub), HTML multipage `browsers.html` and
  `document-sequences.html`, and the Chromium docs `process_model_and_site_isolation.md` and
  `services/network/public/cpp/features.cc`. Also fetched were the policy YAMLs
  `SharedArrayBufferUnrestrictedAccessAllowed`, `OriginAgentClusterDefaultEnabled` and
  `SitePerProcessAndroid`.
- Found by web search on 2026-11-24 (search summary, page not opened): the Mozilla security blog post of
  2024-06-05 (Firefox 127 upgrades mixed images), and the Chrome blog and blink-dev threads saying DIP
  shipped in Chrome 137 on desktop.
- "Recalled" in the TSVs means taken from earlier records in this repo or from memory, not rechecked today.

Quotes (short, for the decisions):

> The choice of which is implementation-defined.

HTML, obtain a browsing context to use for a navigation response (cross-origin isolation mode),
https://html.spec.whatwg.org/multipage/browsers.html, fetched 2026-11-24.

> This is not a security guarantee and may not always be honored.

Chromium, docs/process_model_and_site_isolation.md (on Origin-Agent-Cluster),
https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md, fetched 2026-11-24.

> Currently this feature is enabled for all platforms except WebView.

Chromium, services/network/public/cpp/features.cc (kCrossOriginOpenerPolicy),
https://chromium.googlesource.com/chromium/src/+/main/services/network/public/cpp/features.cc, fetched 2026-11-24.

## Observed divergences (`divergences.tsv`)

| id | item | decision | evidence |
|---|---|---|---|
| D1 | Chrome: absent OAC header means origin-keyed (25 rows) | PARAMETER, provisional; **rule conflict** | #7617 open ("do not merge yet", change request 2026-09-30) and shipped. Chrome also fails the public OAC tests (e.g. parent-no-child-yes-same 1/3 vs Firefox 3/3) |
| D2 | Chrome: document.domain is a no-op (w106–w109) | follows D1 | same cause |
| D3 | Firefox: cross-origin child reports crossOriginIsolated TRUE (29 rows) | BROWSER DEFECT | cross-origin-isolated-permission-iframe: Chrome 8/8, Firefox 3/8, Safari 3/8; Permissions Policy default allowlist `self`. Model side: SpecIsolation has no Permissions Policy (premise; GenModel's PP step) |
| D4 | Firefox: SAP exemption carried across redirect hops (24 rows) | BROWSER DEFECT | popup-redirect-same-origin-allow-popups: Chrome 2/2, Firefox 0/2, Safari 2/2; #coop-enforce compares each response with the previous one |
| D5 | Firefox: sandboxed same-host child blocked by CORP (3 rows) | **UNDECIDED** | no public test (none in clone 31362d122; wpt.fyi query gave 0 results). The spec checks CORP against the container document, so it reads as contrary to the spec. The behaviour is stricter |
| D6 | w014: http image errors in all browsers | PARAMETER (`served`, the target server) and a test defect | scheme-restriction.https.window 0/1 in all 3 engines. Browsers follow MIX 4.1 (upgrade, port kept) |
| D7 | Chrome: window.name kept after a cross-site noopener navigation | **UNDECIDED**, outside the model | the only near test (popup with opener) fails 0/1 in all 3 engines. The rule needs a failing test for this case |
| D8 | Firefox: no bfcache restore under the harness | MODEL PREMISE (harness limit) | bfcache eligibility is UA-defined; recalled |
| D9 | Safari: credentialless missing or partial | PARAMETER (`Supported`) | merged spec. wpt.fyi now shows Safari 3/5, so the value has moved since 2026-11-20 |
| D10 | Chrome patch changed between repeats | no divergence | the values were identical |

## Version and configuration choices (`configs.tsv`)

| id | choice | decision |
|---|---|---|
| K1, K2 | OAC default; policy OriginAgentClusterDefaultEnabled | PARAMETER `OACParam`, `OACParamWithPolicy` |
| K3 | COI mode logical/concrete | PREMISE: the spec says implementation-defined. The spec-level envelope is {concrete, logical}; observed deployments are concrete |
| K4 | policy SharedArrayBufferUnrestrictedAccessAllowed | **UNDECIDED** by the rule: it varies by config, but HTML does not delegate SAB gating. It is held as a premise (policy off), `SABWithoutCOI` |
| K5, K6 | process isolation full/partial/none; SitePerProcessAndroid, IsolateOrigins | PREMISE: the process model is outside the spec. `ProcessIsolation` |
| K7 | OAC as process placement | PREMISE: a hint only. `OACPlacesProcess = FALSE` |
| K8 | COOP absent (WebView comment; Chrome `--disable-features`) | PARAMETER `Supported`, `SupportedWithFlags`. WebView itself was not run |
| K9–K11 | DIP, noopener-allow-popups, credentialless support | PARAMETER `Supported`. Unsettled members are in `SupportedUnsettled` |
| K12 | Mixed Content image upgrade | PARAMETER `MCUpgradeImg` (Firefox 127+, checked; Chrome recalled) |
| K13, K14 | optional BCG swap (c), (a), (b) | PREMISE: per-event policy inside a nondeterministic envelope. `OptionalSwap`, `ChromeSwaps` |
| K15 | scripting disabled by policy | PREMISE: the isolation steps do not branch on it |
| K16 | TLS served at the upgraded URL | PARAMETER: a fact about the target server, `ServedAtUpgradedURL` |

## Params.tla

New module, standalone (`EXTENDS FiniteSets, TLC`). It gives values per deployment, and each value
feeds an existing constant. `OACParam` feeds Gen2Model's `OACParam`. `COIChoices` feeds the COIChoice
sets. `Supported` feeds Unsupported.tla's `Supported`. `MCUpgradeImg` feeds the `mc-upgrade` step.
Premises are listed too, so a proof can name the value it assumes. TLC (veda-tlc 1.8.0, run in a
scratch copy) checks the ASSUMEs: every value is in its domain, and each deployment's swap choice is
inside the spec envelope. Result: "Model checking completed. No error has been found." (2 states).
`Params.cfg` is `SPECIFICATION Spec`.

## Verdict

- **R1 (all decided by the rule): not supported.** Four items are not decided:
  - **D1/K1 (Chrome OAC):** both the parameter clause and the defect clause apply. For a parameter:
    the behaviour is intentional and shipped, a policy controls it, and a PR is open. For a defect:
    it is contrary to the current HTML text, the public tests fail, and the PR is blocked by a change
    request. The catalogue keeps it as a provisional parameter.
  - **D5 (Firefox sandbox CORP):** no public test exists. The spec reading points to a defect, but the
    rule needs a test.
  - **D7 (Chrome window.name):** the only public test is for a neighbouring case, and it fails in all
    engines.
  - **K4 (SAB policy):** the item varies by configuration, but the spec does not delegate the choice.
- **R2: supported**, by those four items: 3 of the 10 divergences (D1, D5, D7) and 1 of the
  16 choices (K4). The rule needs two additions. One is a
  precedence order for D1. The other is a class for test defects (D6) and for harness limits (D8).
- **C4 (each divergence decided):** not fully met. 6 of 10 are decided by the rule. D1 and D2 (which follows D1) have a provisional decision. D5 and D7 are
  explicitly undecided, with the evidence on both sides.
- **C7 (version/config choices written as parameters or premises):** met. All 16 are in
  `configs.tsv` and in Params.tla. K4 is written as a premise, but its class is undecided.

## Limits

- One reader of the spec. Safari values come mostly from wpt.fyi totals, not local runs. WebView,
  Android and iOS were not run. Firefox's support for nap and DIP, and Chrome's mixed-image version,
  are recalled.
- wpt.fyi counts are subtest pass totals; a pass total does not show which subtest failed.
