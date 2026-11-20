# 取り置きのバグの候補（表のみ）

subagent が 2026-11-20T22:39Z〜22:48Z（UTC）に集めた候補の表。各バグの報告の本文や引用は載せず、ID・ブラウザ・修正の時期・部品・報告された誤った値・きっかけ・根本原因の文が公開されているか・境界かだけを載せる。出典はバグの ID から、issues.chromium.org、bugzilla.mozilla.org、Chrome Releases、MFSA で引ける。

<!-- data-source: original（公開のバグの事実を subagent がまとめた表） -->

| # | ID(s) | Browser | Fixed (CL/flag date; release) | Component | Wrong value (as reported) | Trigger | Root-cause text | B |
|---|---|---|---|---|---|---|---|---|
| 1 | CVE-2025-3071 / crbug 40051596 | Chromium | CL 6185347 2025-02-14; Chrome 135 (2025-04-01) | Navigation | origin (same-document nav after about:blank + back keeps new origin); history entry (document sequence number reuse) | web | Y | |
| 2 | CVE-2024-9966 / crbug 364773822 | Chromium | CL 5860536 2024-09-16; Chrome 130 (2024-10-15) | Navigation | inheritance (policy container restored from history entry of an error page) | web | Y | |
| 3 | CVE-2025-6556 / crbug 40062462 | Chromium | CL 6388538 2025-05-08; Chrome 138 (2025-06-24) | Loader / Mixed Content | origin (opaque origin's precursor not used for auto-upgrade in about:blank popup / data: frame) | web | Y | B |
| 4 | CVE-2026-5903 / crbug 483771899 | Chromium | CL 7572487 2026-02-20; Chrome 147 (2026-04-07) | IFrameSandbox | other (navigation policy from untrusted Ctrl+click creates auxiliary context despite sandbox) | web | Y | B |
| 5 | CVE-2026-9903 / crbug 498783665 | Chromium | CL 7837898 2026-05-14; 2026-05-27 release | Site Isolation | origin (MHTML subframe renderer-provided origin accepted) | renderer | Y | |
| 6 | CVE-2026-11174 / crbug 502348223 | Chromium | CL 7794327 2026-05-02; 2026-06-02 release | Site Isolation | origin/site (error-page opaque origin keeps victim precursor; sandboxed srcdoc child placed in victim SiteInstance) | renderer | Y | |
| 7 | CVE-2026-11220 / crbug 487300831 | Chromium | CL 7794327 (merged; 7603574 abandoned); 2026-06-02 release | Navigation | origin (opaque initiator origin with arbitrary precursor accepted in error docs/MHTML) | renderer | Y | B |
| 8 | CVE-2026-11217 / crbug 487564032 | Chromium | CL 7607320 2026-04-09; 2026-06-02 release | Fenced Frames | origin (initiator_origin for `_unfencedTop` should be opaque) | web (fenced-frame content) | Y | |
| 9 | CVE-2026-84355 / crbug 511774376 | Chromium | CL 8285142 2026-08-26 (reland of 8041464); 2026-09-01 release | Navigation (Navigation API) | origin / history entry (origin derived from URL instead of entry's committed origin) | web | Y | |
| 10 | CVE-2026-87516 / crbug 513608513 | Chromium | CL 8162252 2026-07-31; 2026-09-08 release | Navigation | history entry selection (same-URL replacement of error pages without origin comparison) | web | Y | |
| 11 | CVE-2026-13024 / crbug 517148260 | Chromium | CL 7893390 2026-06-04; 2026-06-23 release | Site Isolation / BFCache | history entry / origin (commit accepted from BFCached subframe) | renderer | Y | B |
| 12 | CVE-2026-87442 / crbug 497443419 | Chromium | CL 8217707 2026-08-14; 2026-09-08 release | Prerender | creator (prefetch attributed to primary main frame instead of initiating RFH) | renderer | Y | B |
| 13 | CVE-2026-79237 / crbug 499068536 | Chromium | CL 7964570 2026-07-15; 2026-08-25 release | Navigation | inheritance (initiator policies looked up in wrong StoragePartition) | web (WebView/IWA context) | Y | B |
| 14 | CVE-2026-11025 / crbug 497595264 | Chromium | CL 7719744 2026-04-07; 2026-06-02 release | Navigation | inheritance (initiator policies lost in deferred popup navigation) | web (Android WebView) | Y | B |
| 15 | CVE-2026-87432 / crbug 511820041 | Chromium | CL 8162305 2026-08-04; 2026-09-08 release | Navigation / History | history entry (forged client_side_redirect_url origin) | renderer | Y | B |
| 16 | CVE-2026-79066 / crbug 511736672 | Chromium | CL 8139503 2026-07-24; 2026-08-25 release | Navigation | other: committed URL of error page stored in entry not validated | renderer | Y | B |
| 17 | CVE-2026-87541 / crbug 517156678 | Chromium | CL 8178743 2026-08-11; 2026-09-08 release | Navigation | other: final redirect URL sent to cross-origin process for error page | renderer | Y | B |
| 18 | CVE-2026-5918 / crbug 490139441 | Chromium | CL 7642049 2026-03-09; 2026-04-07 release | Navigation | other: redirect chain not sanitized for error-page commit | web | Y | B |
| 19 | CVE-2026-19152 / crbug 531165110 | Chromium | CL 8089319 2026-07-17; 2026-08-06 release | Navigation | history entry (post_data kept across SiteInstance change on failed history nav) | renderer | Y | B |
| 20 | CVE-2026-5876 / crbug 41485206 | Chromium | CL 7560041 2026-02-24; 2026-04-07 release | Navigation | other: load-event count leaks cross-origin iframe URL | web | P | B |
| 21 | CVE-2026-130937 / crbug 568973728 | Chromium (iOS) | CL 8563803 2026-10-15; 2026-11-17 release | Navigation (iOS) | history entry (back/forward carve-out does not check destination item URL) | web | Y | B |
| 22 | CVE-2026-3930 / crbug 476898368 | Chromium (iOS) | CL 7511016 2026-01-23; 2026-03-10 release | Navigation (iOS) | other: reload + server redirect reaches chrome:// | web | Y | B |
| 23 | CVE-2026-11219 / crbug 480074849 | Chromium | CL 7805947 2026-05-04; 2026-06-02 release | Navigation | other: navigation IPCs accepted from inactive (previous) document | web | Y | B |
| 24 | CVE-2025-0441 / crbug 368628042 | Chromium | CL 5902121 2024-10-15; Chrome 132 (2025-01-14) | Fenced Frames | other: localhost check ignores scheme (file://localhost loads) | web | Y | B |
| 25 | CVE-2024-3840 / crbug 41493458 | Chromium (Android) | CL 5269464 (listed in issue); Chrome 124 (2024-04-16) | Site Isolation / PopupBlocker | other: top navigation from cross-origin iframe with CSP sandbox allow-top-navigation | web | P | B |
| 26 | CVE-2025-4083 / bmo 1958350 | Firefox | Fx 138, ESR 128/115 (resolved 2025-04-18) | DOM: Content Processes | site/creator (javascript: doc from cross-origin iframe created in top-level's process) | web (user Ctrl-click) | Y | |
| 27 | CVE-2025-13018 / bmo 1984940 | Firefox | resolved 2025-09-27 | DOM: Security | creator/initiator (window.open noreferrer → Sec-Fetch-Site: none) | web | Y | B |
| 28 | CVE-2025-6427 / bmo 1966927 | Firefox | resolved 2025-05-27 | DOM: Security | inheritance (CSP null for loads from detached window; no client info) | web | Y | |
| 29 | CVE-2026-0877 / bmo 1999257 | Firefox | Fx 147, ESR 140/115 (resolved 2025-12-22) | DOM: Security | inheritance (Permissions Policy missing after cross-origin iframe navigates to blob:) | web | P | |
| 30 | CVE-2026-8962 / bmo 2004804 | Firefox | Fx 151, ESR 140 (resolved 2026-04-18) | DOM: Security | origin/inheritance (mixed-content context for data:/blob: popup content) | web | P | B |
| 31 | CVE-2026-12302 / bmo 2034489 | Firefox | Fx 152, ESR 140/115 (resolved 2026-05-20) | DOM: Security | Window reuse / inheritance (constructor saved before same-origin nav; CSP of initial about:blank) | web | Y | |
| 32 | CVE-2026-16349 / bmo 2034682 | Firefox | Fx 153, ESR 140/115/153 (resolved 2026-07-15) | DOM: Navigation | inheritance (PrincipalToInherit from content unvalidated; about:blank) | renderer | Y | |
| 33 | bmo 2035756 (depends on 2034682) | Firefox | Fx 153 (resolved 2026-07-08) | DOM: Navigation | inheritance (PrincipalToInherit; about:srcdoc) | renderer | Y | |
| 34 | CVE-2026-12295 / bmo 2040160 | Firefox | Fx 152 (resolved 2026-06-03) | DOM: Navigation | inheritance (forged srcdoc load state; same root cause as 2034682 in part) | renderer | Y | |
| 35 | bmo 2054677 | Firefox | Fx 154, ESR 140/115/153 (resolved 2026-07-23) | DOM: Navigation | history entry (srcdocData not compared in ValidateHistoryLoad) | renderer | Y | |
| 36 | CVE-2026-15719 / bmo 2043820 | Firefox | Fx 152 (resolved 2026-06-29) | DOM: Navigation | creator (triggering principal forged on PBrowserBridge LoadURL) | renderer | Y | B |
| 37 | CVE-2026-84136 / bmo 2048699 | Firefox | Fx 155, ESR 153 (resolved 2026-08-11) | DOM: Navigation | history entry (traversal driven for non-owned BrowsingContext) | renderer | Y | B |
| 38 | CVE-2024-5687 / bmo 1889066 | Firefox (Android) | Fx 127 (resolved 2024-05-07) | Browser Engine | creator/inheritance (parent tab's triggeringPrincipal used for typed URL) | user action | Y | |
| 39 | CVE-2024-6611 / bmo 1844827 | Firefox | Fx 128 (resolved 2024-06-12) | Networking: Cookies | site (same-site computation for cookies on cross-site iframe navigations) | web | P | B |
| 40 | CVE-2024-6601 / bmo 1890748 | Firefox | Fx 128, ESR 115 (resolved 2024-06-20) | DOM: Security | inheritance (feature policy initialized before window context is current → default policy) | web (race) | Y | |
| 41 | CVE-2026-74939 / bmo 2054416 | Firefox | Fx 154, ESR 140/115/153 (resolved 2026-07-21) | DOM: Navigation | site/process (about:blank NullPrincipal with chosen precursor + RemoteTypeOverride=file) | renderer | Y | |
| 42 | bmo 2059205 | Firefox | Fx 155, ESR 153 (resolved 2026-08-22) | DOM: Networking | origin (EventSource MessageEvent.origin computed once, pre-redirect) | web | Y | B |
| 43 | CVE-2026-8950 / bmo 1965430 | Firefox | Fx 151, ESR 140 (resolved 2026-04-15) | Networking: HTTP | origin (Origin header not tainted to null after cross-origin redirect; inverted condition) | web | Y | B |
| 44 | bmo 2018164 | Firefox | Fx 154, ESR 153 (resolved 2026-07-22) | DOM: Core & HTML | creator (ClientOpenWindow triggering principal from child unverified) | renderer | Y | B |

