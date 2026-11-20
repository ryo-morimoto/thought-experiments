# WPTBroad の行番号と WPT の試験

WPTBroad.tla の w001 以降と、元の表の行の対応。試験の本文（wpt.live、web-platform-tests の master）から subagent が読み取った引数と期待値、wpt.fyi の 2026-11-20 の stable の実行（Chrome 158、Firefox 160、Safari 27.2）の結果。試験そのものは載せず、事実の要約だけを載せる。

<!-- data-source: original（WPT の試験の期待値と実行結果を要約した事実の表） -->
| 名前 | 試験 | 演算子 | 引数 | 期待 | Chrome | Firefox | Safari |
| --- | --- | --- | --- | --- | --- | --- | --- |
| w001 | fetch/cross-origin-resource-policy/fetch.any.js (window: fetch.any.html) | FetchResult | Ahttp,unsafe-none,cors,Ahttp,same-origin,TRUE | basic | PASS | PASS | PASS |
| w002 | fetch/cross-origin-resource-policy/fetch.any.js (window: fetch.any.html) | FetchResult | Ahttp,unsafe-none,cors,Ahttp,same-site,TRUE | basic | PASS | PASS | PASS |
| w003 | fetch/cross-origin-resource-policy/fetch.any.js (window: fetch.any.html) | FetchResult | Ahttp,unsafe-none,no-cors,Bhttp,same-origin,FALSE | error | PASS | PASS | PASS |
| w004 | fetch/cross-origin-resource-policy/fetch.any.js (window: fetch.any.html) | FetchResult | Ahttp,unsafe-none,no-cors,Bhttp,same-site,FALSE | error | PASS | PASS | PASS |
| w005 | fetch/cross-origin-resource-policy/fetch.any.js (window: fetch.any.html) | FetchResult | Ahttp,unsafe-none,no-cors,A,same-site,FALSE | error | PASS | PASS | PASS |
| w006 | fetch/cross-origin-resource-policy/fetch.any.js (window: fetch.any.html) | FetchResult | Ahttp,unsafe-none,no-cors,A,same-origin,FALSE | error | PASS | PASS | PASS |
| w007 | fetch/cross-origin-resource-policy/fetch.any.js (window: fetch.any.html) | FetchResult | Ahttp,unsafe-none,no-cors,Awwwhttp,same-site,FALSE | opaque | PASS | PASS | PASS |
| w008 | fetch/cross-origin-resource-policy/fetch.any.js (window: fetch.any.html) | FetchResult | Ahttp,unsafe-none,no-cors,Awwwhttp,same-origin,FALSE | error | PASS | PASS | PASS |
| w009 | fetch/cross-origin-resource-policy/fetch.https.any.js (window: fetch.https.any.html) | FetchResult | A,unsafe-none,cors,A,same-origin,TRUE | basic | PASS | PASS | PASS |
| w010 | fetch/cross-origin-resource-policy/fetch.https.any.js (window: fetch.https.any.html) | FetchResult | A,unsafe-none,cors,A,same-site,TRUE | basic | PASS | PASS | PASS |
| w011 | fetch/cross-origin-resource-policy/fetch.https.any.js (window: fetch.https.any.html) | FetchResult | A,unsafe-none,no-cors,B,same-origin,FALSE | error | PASS | PASS | PASS |
| w012 | fetch/cross-origin-resource-policy/fetch.https.any.js (window: fetch.https.any.html) | FetchResult | A,unsafe-none,no-cors,B,same-site,FALSE | error | PASS | PASS | PASS |
| w013 | fetch/cross-origin-resource-policy/scheme-restriction.any.js (scheme-restriction.any.html) | FetchResult | Ahttp,unsafe-none,no-cors,Awww,same-site,FALSE | error | PASS | PASS | PASS |
| w014 | fetch/cross-origin-resource-policy/scheme-restriction.https.window.js | FetchResult | A,unsafe-none,no-cors,Awwwhttp,same-site,FALSE | opaque | FAIL | FAIL | FAIL |
| w015 | fetch/cross-origin-resource-policy/image-loads.html | FetchResult | Ahttp,unsafe-none,no-cors,Ahttp,same-origin,TRUE | basic | PASS | PASS | PASS |
| w016 | fetch/cross-origin-resource-policy/image-loads.html | FetchResult | Ahttp,unsafe-none,no-cors,Ahttp,same-site,TRUE | basic | PASS | PASS | PASS |
| w017 | fetch/cross-origin-resource-policy/image-loads.html | FetchResult | Ahttp,unsafe-none,no-cors,Bhttp,same-origin,TRUE | error | PASS | PASS | PASS |
| w018 | fetch/cross-origin-resource-policy/image-loads.html | FetchResult | Ahttp,unsafe-none,no-cors,Bhttp,same-site,TRUE | error | PASS | PASS | PASS |
| w019 | fetch/cross-origin-resource-policy/script-loads.html | FetchResult | Ahttp,unsafe-none,no-cors,Ahttp,same-origin,TRUE | basic | PASS | PASS | PASS |
| w020 | fetch/cross-origin-resource-policy/script-loads.html | FetchResult | Ahttp,unsafe-none,no-cors,Ahttp,same-site,TRUE | basic | PASS | PASS | PASS |
| w021 | fetch/cross-origin-resource-policy/script-loads.html | FetchResult | Ahttp,unsafe-none,no-cors,Bhttp,same-origin,TRUE | error | PASS | PASS | PASS |
| w022 | fetch/cross-origin-resource-policy/script-loads.html | FetchResult | Ahttp,unsafe-none,no-cors,Bhttp,same-site,TRUE | error | PASS | PASS | PASS |
| w023 | html/cross-origin-embedder-policy/require-corp.https.html | FetchResult | A,require-corp,no-cors,Awww,cross-origin,FALSE | opaque | PASS | PASS | PASS |
| w024 | html/cross-origin-embedder-policy/require-corp.https.html | FetchResult | A,require-corp,no-cors,Awww,none,FALSE | error | PASS | PASS | PASS |
| w025 | html/cross-origin-embedder-policy/require-corp.https.html | FetchResult | A,require-corp,no-cors,Awww,none,FALSE | error | PASS | PASS | PASS |
| w026 | html/cross-origin-embedder-policy/credentialless/no-cors-omit.https.window.js | FetchResult | A,credentialless,no-cors,Awww,none,FALSE | opaque | PASS | PASS | PASS |
| w027 | html/cross-origin-opener-policy/popup-same-origin-allow-popups-with-cross-origin.https.html | PopupSevered | same-origin-allow-popups,A,unsafe-none,B | FALSE | PASS | PASS | PASS |
| w028 | html/cross-origin-opener-policy/popup-same-origin-allow-popups-with-cross-origin.https.html | PopupSevered | same-origin-allow-popups,A,same-origin,B | TRUE | PASS | PASS | PASS |
| w029 | html/cross-origin-opener-policy/popup-same-origin-allow-popups-with-cross-origin.https.html | PopupSevered | same-origin-allow-popups,A,same-origin-allow-popups,B | TRUE | PASS | PASS | PASS |
| w030 | html/cross-origin-opener-policy/popup-same-origin-allow-popups-with-same-origin.https.html | PopupSevered | same-origin-allow-popups,A,unsafe-none,A | FALSE | PASS | PASS | PASS |
| w031 | html/cross-origin-opener-policy/popup-same-origin-allow-popups-with-same-origin.https.html | PopupSevered | same-origin-allow-popups,A,same-origin,A | TRUE | PASS | PASS | PASS |
| w032 | html/cross-origin-opener-policy/popup-same-origin-allow-popups-with-same-origin.https.html | PopupSevered | same-origin-allow-popups,A,same-origin-allow-popups,A | FALSE | PASS | PASS | PASS |
| w033 | html/cross-origin-opener-policy/popup-same-origin-allow-popups-with-same-site.https.html | PopupSevered | same-origin-allow-popups,A,unsafe-none,Awww | FALSE | PASS | PASS | PASS |
| w034 | html/cross-origin-opener-policy/popup-same-origin-allow-popups-with-same-site.https.html | PopupSevered | same-origin-allow-popups,A,same-origin,Awww | TRUE | PASS | PASS | PASS |
| w035 | html/cross-origin-opener-policy/popup-same-origin-allow-popups-with-same-site.https.html | PopupSevered | same-origin-allow-popups,A,same-origin-allow-popups,Awww | TRUE | PASS | PASS | PASS |
| w036 | html/cross-origin-opener-policy/popup-same-origin-with-cross-origin.https.html | PopupSevered | same-origin,A,unsafe-none,B | TRUE | PASS | PASS | PASS |
| w037 | html/cross-origin-opener-policy/popup-same-origin-with-cross-origin.https.html | PopupSevered | same-origin,A,same-origin,B | TRUE | PASS | PASS | PASS |
| w038 | html/cross-origin-opener-policy/popup-same-origin-with-cross-origin.https.html | PopupSevered | same-origin,A,same-origin-allow-popups,B | TRUE | PASS | PASS | PASS |
| w039 | html/cross-origin-opener-policy/popup-same-origin-with-same-origin.https.html | PopupSevered | same-origin,A,unsafe-none,A | TRUE | PASS | PASS | PASS |
| w040 | html/cross-origin-opener-policy/popup-same-origin-with-same-origin.https.html | PopupSevered | same-origin,A,same-origin,A | FALSE | PASS | PASS | PASS |
| w041 | html/cross-origin-opener-policy/popup-same-origin-with-same-origin.https.html | PopupSevered | same-origin,A,same-origin-allow-popups,A | TRUE | PASS | PASS | PASS |
| w042 | html/cross-origin-opener-policy/popup-same-origin-with-same-site.https.html | PopupSevered | same-origin,A,unsafe-none,Awww | TRUE | PASS | PASS | PASS |
| w043 | html/cross-origin-opener-policy/popup-same-origin-with-same-site.https.html | PopupSevered | same-origin,A,same-origin,Awww | TRUE | PASS | PASS | PASS |
| w044 | html/cross-origin-opener-policy/popup-same-origin-with-same-site.https.html | PopupSevered | same-origin,A,same-origin-allow-popups,Awww | TRUE | PASS | PASS | PASS |
| w045 | html/cross-origin-opener-policy/popup-unsafe-none-with-cross-origin.https.html | PopupSevered | unsafe-none,A,unsafe-none,B | FALSE | PASS | PASS | PASS |
| w046 | html/cross-origin-opener-policy/popup-unsafe-none-with-cross-origin.https.html | PopupSevered | unsafe-none,A,same-origin,B | TRUE | PASS | PASS | PASS |
| w047 | html/cross-origin-opener-policy/popup-unsafe-none-with-cross-origin.https.html | PopupSevered | unsafe-none,A,same-origin-allow-popups,B | TRUE | PASS | PASS | PASS |
| w048 | html/cross-origin-opener-policy/popup-unsafe-none-with-same-origin.https.html | PopupSevered | unsafe-none,A,unsafe-none,A | FALSE | PASS | PASS | PASS |
| w049 | html/cross-origin-opener-policy/popup-unsafe-none-with-same-origin.https.html | PopupSevered | unsafe-none,A,same-origin,A | TRUE | PASS | PASS | PASS |
| w050 | html/cross-origin-opener-policy/popup-unsafe-none-with-same-origin.https.html | PopupSevered | unsafe-none,A,same-origin-allow-popups,A | TRUE | PASS | PASS | PASS |
| w051 | html/cross-origin-opener-policy/popup-unsafe-none-with-same-site.https.html | PopupSevered | unsafe-none,A,unsafe-none,Awww | FALSE | PASS | PASS | PASS |
| w052 | html/cross-origin-opener-policy/popup-unsafe-none-with-same-site.https.html | PopupSevered | unsafe-none,A,same-origin,Awww | TRUE | PASS | PASS | PASS |
| w053 | html/cross-origin-opener-policy/popup-unsafe-none-with-same-site.https.html | PopupSevered | unsafe-none,A,same-origin-allow-popups,Awww | TRUE | PASS | PASS | PASS |
| w054 | html/cross-origin-opener-policy/popup-unspecified-with-cross-origin.https.html | PopupSevered | unsafe-none,A,unsafe-none,B | FALSE | PASS | PASS | PASS |
| w055 | html/cross-origin-opener-policy/popup-unspecified-with-cross-origin.https.html | PopupSevered | unsafe-none,A,same-origin,B | TRUE | PASS | PASS | PASS |
| w056 | html/cross-origin-opener-policy/popup-unspecified-with-cross-origin.https.html | PopupSevered | unsafe-none,A,same-origin-allow-popups,B | TRUE | PASS | PASS | PASS |
| w057 | html/cross-origin-opener-policy/popup-unspecified-with-same-origin.https.html | PopupSevered | unsafe-none,A,unsafe-none,A | FALSE | PASS | PASS | PASS |
| w058 | html/cross-origin-opener-policy/popup-unspecified-with-same-origin.https.html | PopupSevered | unsafe-none,A,same-origin,A | TRUE | PASS | PASS | PASS |
| w059 | html/cross-origin-opener-policy/popup-unspecified-with-same-origin.https.html | PopupSevered | unsafe-none,A,same-origin-allow-popups,A | TRUE | PASS | PASS | PASS |
| w060 | html/cross-origin-opener-policy/popup-unspecified-with-same-site.https.html | PopupSevered | unsafe-none,A,unsafe-none,Awww | FALSE | PASS | PASS | PASS |
| w061 | html/cross-origin-opener-policy/popup-unspecified-with-same-site.https.html | PopupSevered | unsafe-none,A,same-origin,Awww | TRUE | PASS | PASS | PASS |
| w062 | html/cross-origin-opener-policy/popup-unspecified-with-same-site.https.html | PopupSevered | unsafe-none,A,same-origin-allow-popups,Awww | TRUE | PASS | PASS | PASS |
| w063 | html/cross-origin-embedder-policy/credentialless/cross-origin-isolated.window.js | CrossOriginIsolated | same-origin,credentialless,A | TRUE | PASS | PASS | FAIL |
| w064 | html/cross-origin-embedder-policy/credentialless/cross-origin-isolated.window.js | CrossOriginIsolated | same-origin,credentialless,Ahttp | FALSE | PASS | PASS | PASS |
| w065 | html/cross-origin-embedder-policy/credentialless/cross-origin-isolated.window.js | CrossOriginIsolated | unsafe-none,credentialless,A | FALSE | PASS | PASS | PASS |
| w066 | html/cross-origin-embedder-policy/credentialless/cross-origin-isolated.window.js | CrossOriginIsolated | same-origin,unsafe-none,A | FALSE | PASS | PASS | PASS |
| w067 | html/cross-origin-embedder-policy/credentialless/cross-origin-isolated.window.js | CrossOriginIsolated | same-origin,credentialless,A | TRUE | PASS | PASS | FAIL |
| w068 | html/cross-origin-embedder-policy/credentialless/no-cors-omit.https.window.js | CrossOriginIsolated | same-origin,credentialless,A | TRUE | PASS | PASS | FAIL |
| w069 | html/cross-origin-opener-policy/coep-with-same-origin.https.html | CrossOriginIsolated | same-origin,require-corp,A | TRUE | PASS | PASS | PASS |
| w070 | html/cross-origin-opener-policy/coep-with-same-site.https.html | CrossOriginIsolated | same-origin,require-corp,A | TRUE | PASS | PASS | PASS |
| w071 | html/cross-origin-opener-policy/coep-with-cross-origin.https.html | CrossOriginIsolated | same-origin,require-corp,A | TRUE | PASS | PASS | PASS |
| w072 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-no-child-yes-subdomain.sub.https.html | OriginAgentCluster | A,none,absent,FALSE | FALSE | FAIL | PASS | FAIL |
| w073 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-yes-child-no-subdomain.sub.https.html | OriginAgentCluster | A,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w074 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-no-child-bad-subdomain.sub.https.html | OriginAgentCluster | Awww,none,absent,FALSE | FALSE | FAIL | PASS | FAIL |
| w075 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-no-child-yes-cross-site.sub.https.html | OriginAgentCluster | B,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w076 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-no-child-yes-port.sub.https.html | OriginAgentCluster | Awww,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w077 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-no-child-yes-same.sub.https.html | OriginAgentCluster | A,none,site,TRUE | FALSE | FAIL | PASS | FAIL |
| w078 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-no-child-yes-subdomain.sub.https.html | OriginAgentCluster | Awww,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w079 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-no-child-yeswithparams-subdomain.sub.https.html | OriginAgentCluster | Awww,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w080 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-yes-child-no-port.sub.https.html | OriginAgentCluster | Awww,none,absent,FALSE | FALSE | FAIL | PASS | FAIL |
| w081 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-yes-child-no-same.sub.https.html | OriginAgentCluster | A,none,origin,FALSE | TRUE | PASS | PASS | FAIL |
| w082 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-yes-child-no-subdomain.sub.https.html | OriginAgentCluster | Awww,none,absent,FALSE | FALSE | FAIL | PASS | FAIL |
| w083 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-yes-child-yes-port.sub.https.html | OriginAgentCluster | Awww,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w084 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-yes-child-yes-same.sub.https.html | OriginAgentCluster | A,none,origin,TRUE | TRUE | PASS | PASS | FAIL |
| w085 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-yes-child-yes-subdomain.sub.https.html | OriginAgentCluster | Awww,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w086 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-no-child1-no-subdomain-child2-yes-subdomain.sub.https.html | OriginAgentCluster | Awww,none,site,TRUE | FALSE | FAIL | PASS | FAIL |
| w087 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-no-child1-no-subdomain-child2-yes-subdomainport.sub.https.html | OriginAgentCluster | Awww2,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w088 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-no-child1-no-subdomain1-child2-yes-subdomain2.sub.https.html | OriginAgentCluster | Awww2,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w089 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-no-child1-yes-subdomain-child2-no-port.sub.https.html | OriginAgentCluster | Awww2,none,absent,FALSE | FALSE | FAIL | PASS | FAIL |
| w090 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-no-child1-yes-subdomain-child2-no-subdomain.sub.https.html | OriginAgentCluster | Awww,none,origin,FALSE | TRUE | PASS | PASS | FAIL |
| w091 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-yes-child1-no-subdomain-child2-no-subdomain.sub.https.html | OriginAgentCluster | Awww,none,site,FALSE | FALSE | FAIL | PASS | FAIL |
| w092 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-yes-child1-no-subdomain-child2-no-subdomain2.sub.https.html | OriginAgentCluster | Awww2,none,absent,FALSE | FALSE | FAIL | PASS | FAIL |
| w093 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-yes-child1-no-subdomain-child2-yes-subdomain.sub.https.html | OriginAgentCluster | Awww,none,site,TRUE | FALSE | FAIL | PASS | FAIL |
| w094 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-yes-child1-no-subdomain-child2-yes-subdomain2.sub.https.html | OriginAgentCluster | Awww2,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w095 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-yes-child1-yes-subdomain-child2-no-port.sub.https.html | OriginAgentCluster | Awww2,none,absent,FALSE | FALSE | FAIL | PASS | FAIL |
| w096 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-yes-child1-yes-subdomain-child2-no-subdomain.sub.https.html | OriginAgentCluster | Awww,none,origin,FALSE | TRUE | PASS | PASS | FAIL |
| w097 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-yes-child1-yes-subdomain-child2-yes-subdomain.sub.https.html | OriginAgentCluster | Awww,none,origin,TRUE | TRUE | PASS | PASS | FAIL |
| w098 | html/browsers/origin/origin-keyed-agent-clusters/getter-special-cases/cross-origin-isolated.sub.https.html | OriginAgentCluster | A,concrete,absent,FALSE | TRUE | PASS | PASS | FAIL |
| w099 | html/browsers/origin/origin-keyed-agent-clusters/getter-special-cases/cross-origin-isolated.sub.https.html | OriginAgentCluster | Awww,concrete,absent,FALSE | TRUE | PASS | PASS | FAIL |
| w100 | html/browsers/origin/origin-keyed-agent-clusters/popups/opener-yes-openee-no-subdomain.sub.https.html | OriginAgentCluster | Awww,none,absent,FALSE | FALSE | FAIL | PASS | FAIL |
| w101 | html/browsers/origin/origin-keyed-agent-clusters/popups/opener-no-openee-yes-subdomain.sub.https.html | OriginAgentCluster | Awww,none,absent,TRUE | TRUE | PASS | PASS | FAIL |
| w102 | html/browsers/origin/origin-keyed-agent-clusters/insecure-http.sub.html | OriginAgentCluster | Ahttp,none,absent,TRUE | FALSE | PASS | PASS | FAIL |
| w103 | html/browsers/origin/origin-keyed-agent-clusters/insecure-http.sub.html | OriginAgentCluster | Awwwhttp,none,absent,TRUE | FALSE | PASS | PASS | FAIL |
| w104 | html/browsers/origin/origin-keyed-agent-clusters/document-domain.sub.https.html | DocumentDomainNoOp | origin | TRUE | PASS | PASS | FAIL |
| w105 | html/browsers/origin/origin-keyed-agent-clusters/document-domain.sub.https.html | DocumentDomainNoOp | origin | TRUE | PASS | PASS | FAIL |
| w106 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-no-child1-no-subdomain-child2-yes-subdomain.sub.https.html | DocumentDomainNoOp | site | FALSE | FAIL | PASS | PASS |
| w107 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-yes-child1-no-subdomain-child2-no-subdomain2.sub.https.html | DocumentDomainNoOp | site | FALSE | FAIL | PASS | PASS |
| w108 | html/browsers/origin/origin-keyed-agent-clusters/1-iframe/parent-no-child-bad-subdomain.sub.https.html | DocumentDomainNoOp | site | FALSE | FAIL | PASS | PASS |
| w109 | html/browsers/origin/origin-keyed-agent-clusters/2-iframes/parent-no-child1-yes-subdomain-child2-no-port.sub.https.html | DocumentDomainNoOp | site | FALSE | FAIL | PASS | PASS |
