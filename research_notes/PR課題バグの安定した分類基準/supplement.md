# PR・課題・バグの安定した分類基準 補遺（初回の調査で扱えなかった候補）

調査日: 2026-11-21。報告 [PR課題バグの安定した分類基準](../../reports/PR課題バグの安定した分類基準.md) で「検証を通った主張に入らなかった」候補を、一次資料で補った。WebFetch か PDF の本文抽出で読んだものは「本文確認」、論文の abstract や公式ページの要約だけのものは「要旨のみ」、検索エンジンの要約だけのものは「検索要約のみ」と書く。初回の報告と違い、主張ごとの 3 票の敵対的な検証は経ていない。引用は短く、直後に URL を書く。

「安定」は、標準化されている、長く使われて改訂が少ない、広く採用されている、評価者間一致度（IRR）が測られて高い、のいずれかを指す。

## 1. CWE（MITRE）

**定義と粒度（本文確認）**
- 弱点（weakness）を Pillar → Class → Base → Variant の 4 段の抽象度で並べ、別に Category（似た弱点のまとまりで、弱点そのものではない）と View（目的・読み手ごとの切り出し）を持つ — [CWE Root Cause Mapping Guidance](https://cwe.mitre.org/documents/cwe_usage/guidance.html)
- 脆弱性への対応づけ（mapping）には Base と Variant を使い、合うものがなければ Class を使う。Category には対応づけない：「never map a vulnerability to a CWE Category」— [同](https://cwe.mitre.org/documents/cwe_usage/guidance.html)
- 各 CWE に使ってよいかの印（Allowed / Allowed-with-Review / Discouraged / Prohibited）がある — [同](https://cwe.mitre.org/documents/cwe_usage/guidance.html)
- NVD 用の View-1003 は「~130 CWEs most commonly seen in the National Vulnerability Database」— [同](https://cwe.mitre.org/documents/cwe_usage/guidance.html)
- 現行は CWE List 5.0、弱点の総数は 956 — [CWE List](https://cwe.mitre.org/data/index.html)

**改訂（本文確認、日付の一部は未確認）**
- 初版のリストは 2006 年 — [CWE History](https://cwe.mitre.org/about/history.html)。同ページは 5.0 を 2026 年 10 月のリリースとしている
- 版の一覧は 1.0 から 5.0 まで 60 版（1.x が 16、2.x が 13、3.x が 6、4.x が 24、5.0）— [Releases Archive](https://cwe.mitre.org/data/archive.html)。各版の日付はこのページに無く、確かめていない。約 20 年で 60 版なので、平均で年 3 版ほど（推論）
- 分類体系そのものが頻繁に改訂される。「改訂が少ない」意味の安定ではない

**対応づけの一貫性（本文確認）**
- Şimşek ら（Boston University と Red Hat、COMPSAC 2025）：2024-12 時点の NVD の 28 万件超の CVE のうち 55% が、無効か不足した CWE（Prohibited、Discouraged、プレースホルダの CWE-Other と CWE-noinfo）に対応づけられていた。内訳は CWE 空欄 18.4%、CWE-Other 10.8%、CWE-noinfo 10%、Prohibited か Discouraged が 16.2%。Prohibited と Discouraged の印は 2019 年に MITRE が導入 — [Fixing Invalid CVE-CWE Mappings in Threat Databases](https://people.bu.edu/staro/COMPSAC-2025-final.pdf)
- 同論文：2008〜2024 年の各年で、報告された CVE の 15〜30% が有効な CWE を持たないまま — [同](https://people.bu.edu/staro/COMPSAC-2025-final.pdf)
- Nong ら（arXiv 2608.21977、2026-08、査読前）：オープンソースの CVE 15,556 件を、コードに根ざした判定と比べた。NVD の CWE がそれと完全一致したのは「only 49.70%」、分類体系の曖昧さから見て弁護できる別解が 31.37%、証拠と矛盾する誤りらしいものが 3.63%。誤りの割合は年とともに増えた — [arXiv 2608.21977](https://arxiv.org/abs/2608.21977)（要旨のみ）
- 複数の人が同じ CVE に独立に CWE を付けたときの IRR（κ など）は見つけられなかった

## 2. CVSS（FIRST）

**定義と粒度（本文確認）**
- v4.0 は 4 つの指標群（Base、Threat、Environmental、Supplemental）。点数を None（0.0）/ Low（0.1〜3.9）/ Medium（4.0〜6.9）/ High（7.0〜8.9）/ Critical（9.0〜10.0）の 5 段の重大度に写す — [CVSS v4.0 Specification](https://www.first.org/cvss/v4.0/specification-document)
- v3.1 の利用者ガイド：「CVSS is designed to measure the severity of a vulnerability and should not be used alone to assess risk」— [CVSS v3.1 User Guide](https://www.first.org/cvss/v3.1/user-guide)

**改訂**
- v2 は 2007 年 6 月（「The last round of voting ended June 1, 2007」）— [CVSS v2 History](https://www.first.org/cvss/v2/history)（本文確認）
- v3.0 は 2015 年 6 月、v3.1 は 2019 年 6 月 — [NVD の告知](https://nvd.nist.gov/General/News/CVSS-v3-1-Official-Support)、[SecurityWeek](https://www.securityweek.com/first-releases-cvss-version-3/)（検索要約のみ）
- v3.1 は v3.0 の明確化で、新しい指標はなく、リスクの言い回しの明確化、Attack Vector の書き直し、Roundup の再定義などの式の修正 — [v3.1 User Guide](https://www.first.org/cvss/v3.1/user-guide)（本文確認）
- v4.0 は 2023-11-01 に初版 — [v4.0 Specification](https://www.first.org/cvss/v4.0/specification-document)（本文確認）
- v3.0 は 2016 年 3 月に ITU-T X.1521 として国際標準になった — 検索要約のみ（[ITU-T X.1521](https://www.itu.int/dms_pubrec/itu-t/rec/x/T-REC-X.1521-201603-I!!TOC-HTM-E.htm) の目次の URL のみ確認）

**評価者の一致（本文確認）**
- Wunder ら（IEEE S&P 2024）：CVSS 利用者 196 人のオンライン調査。広く見られる脆弱性（2022 CWE Top 25 の 1 位 Out-of-bounds Write、2 位 XSS など）で、Attack Vector、User Interaction、Scope の評価がそろわなかった。9 か月後に同じ脆弱性を同じ人（59 人）に評価し直してもらうと、68% の人で重大度が変わった — [arXiv 2308.15259](https://arxiv.org/abs/2308.15259)
  - 68% は評価者内（同じ人の時間をおいた再評価）の不一致で、評価者間ではない
  - 同論文：利用者の 30% は CVSS の文書を読んだことがない。評価の正しさに効くのは、経験や文書の知識より、指標そのものの問題 — [同](https://arxiv.org/pdf/2308.15259)
- Allodi ら（WEIS 2018、EMSE 2020 に拡張）：学生と実務者に CVSS v3 で採点させ、セキュリティの能力（教育か経験）が正確さを上げると報告 — [arXiv 1808.06547](https://arxiv.org/abs/1808.06547)（検索要約のみ。EMSE 版 10.1007/s10664-019-09797-4 は取得できず）

**批判（本文確認）**
- curl は CVSS をやめ、独自の 4 段（low / medium / high / critical）で重大度を付ける：「we have given up trying to use CVSS to get a severity score and associated severity level」— [Daniel Stenberg, CVSS is dead to us (2025-01-23)](https://daniel.haxx.se/blog/2025/01/23/cvss-is-dead-to-us/)。理由は、入力の少なさからネットワーク製品で点数が高く出やすいこと、curl の使われ方を反映できないこと

## 3. 課題管理の重大度・優先度

**Mozilla（本文確認）**
- Severity：S1（Catastrophic、開発や試験を止める、25% 超の利用者に影響しうる、データ損失など）、S2（Serious）、S3（Normal、重要でない機能を止める、または回避策がある）、S4（Small/Trivial）、N/A（Task と Enhancement 用）— [BMO User Guide: Bug Fields](https://wiki.mozilla.org/BMO/UserGuide/BugFields)
- Priority：P1 は今のリリースで直す、P2 は次か次の次、P3 は Backlog、P4 は使わない（Web Platform Test のボット用）、P5 は直さないがパッチは受け入れる — [Priority Definitions](https://firefox-source-docs.mozilla.org/bug-mgmt/guides/priority.html)
- Firefox の severity の手引きは、定義を外部の wiki に任せ、各段の例（S1：URL バーから検索できない、データ損失を伴うクラッシュ等）を挙げる。新規バグは `--`（重大度ではない）で始まり、defect に N/A を付けない — [Severity guide](https://firefox-source-docs.mozilla.org/bug-mgmt/guides/severity.html)
- 2020 年の Severity 必須化と、severity を変えるときに理由をコメントに書く規則は、別の調査ノート [triage_and_incident_practice.md](../課題とバグの理解支援%20先行事例/triage_and_incident_practice.md) で確認済み

**Bugzilla の既定（本文確認）**
- Priority の既定値は P1〜P5。Severity は「blocker」（application unusable）から trivial（minor cosmetic issue）まで — [Bugzilla documentation](https://bugzilla.readthedocs.io/en/latest/using/understanding.html)。Tian らは Bugzilla の 6 段を blocker / critical / major / normal / minor / trivial と書く（下記）

**Jira の既定（検索要約のみ）**
- 既定の優先度は Highest / High / Medium / Low / Lowest。管理者が変更・追加でき、説明は任意 — [Atlassian: Manage priorities](https://support.atlassian.com/jira-cloud-administration/docs/configure-priorities-for-projects/)。各段の公式の定義は見つからなかった

**Chromium のセキュリティ重大度（本文確認）**
- Critical（S0）：攻撃者が任意の資源を読み書きできる。High（S1）：ある origin かプロセスの文脈でコードを実行できる。Medium（S2）：限られた情報を読み書きできる。Low（S3）：通常ならより高いが、緩和要因で下がったもの — [Severity Guidelines for Security Issues](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md)
- 緩和要因があれば 1 段下げる（大きければ 2 段）。Linux だけに影響する Critical も Critical のまま — [同](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md)
- 対応目標：Critical は 30 日以内、High は 60 日以内に全利用者へ。実際に悪用されているものは重大度にかかわらず P0。Critical→P0、High と Medium→P1、Low→P3 — [同](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md)
- 各段に実在のバグを例として挙げて較正する形をとる
- Chromium の一般のバグの Pri-0〜3 の定義は確かめていない

**重大度ラベルの信頼性（本文確認）**
- Tian, Ali, Lo, Hassan「On the unreliability of bug severity data」（EMSE 2016、オンライン 2015）：OpenOffice、Mozilla、Eclipse の重複バグ報告（同じ問題を指す報告の組）で、重大度が食い違ったのは 28.9%、36.6%、50.8%（abstract では「around 51 %」）。標本 437 組の手作業の確認で、95% は本当に同じ問題を指していた。食い違いが最も多いのは major。normal は分析から除いた — [EMSE 2015 PDF](https://sailresearch.github.io/sail-website/data/pdfs/EMSE2015_OnTheUnreliabilityOfBugSeverityData.pdf)
- 同論文：重大度の自動付与（Menzies & Marcus 2008、Lamkanfi ら 2010 など）は人の付けたラベルを正解として評価してきたが、その前提が崩れる。新しい評価法では自動付与が人のラベルと 77〜86% 一致 — [同](https://sailresearch.github.io/sail-website/data/pdfs/EMSE2015_OnTheUnreliabilityOfBugSeverityData.pdf)
- Herraiz ら（MSR 2008）：Eclipse の severity は 7 段で区別しにくい段がある。閉じるまでの時間のまとまりは段の数より少なく、報告フォームの単純化を提案 — 検索要約のみ（[dblp](https://dblp.org/rec/conf/msr/HerraizGGR08)）

## 4. ISO/IEC 25010（製品品質モデル）

**定義と改訂（本文確認、iTeh のプレビューで前書きを読んだ）**
- 2023 年 11 月の第 2 版が 2011 年版を取り消して置き換えた。品質利用（quality in use）モデルなどは ISO/IEC 25002 と 25019 に移った — [ISO/IEC 25010:2023 プレビュー](https://cdn.standards.iteh.ai/samples/78176/13ff8ea97048443f99318920757df124/ISO-IEC-25010-2023.pdf)
- 主な変更：Safety を特性に追加（operational constraint、risk identification、fail safe、hazard warning、safe integration）。Usability を interaction capability に、Portability を flexibility に置き換え。inclusivity、self-descriptiveness、resistance、scalability を副特性に追加。user interface aesthetics を user engagement に、maturity を faultlessness に置き換え。accessibility を inclusivity と user assistance に分割 — [同](https://cdn.standards.iteh.ai/samples/78176/13ff8ea97048443f99318920757df124/ISO-IEC-25010-2023.pdf)
- 2023 年版の特性は 9 つ（functional suitability、performance efficiency、compatibility、interaction capability、reliability、security、maintainability、flexibility、safety）。2011 年版は safety を除く 8 つ（名前は usability と portability）（推論：前書きの差分から）
- 前身は ISO/IEC 9126。9126 → 25010:2011 → 25010:2023 で、約 12 年ごとに特性の名前が変わっている

**分類に使ったときの一致（検索要約のみ）**
- Vetro, Zazworka, Seaman, Shull（EASE 2012）：ISO/IEC 9126 で産業の Web アプリの欠陥 78 件を分類。主特性（6）のほうが副特性（22）より信頼性が高く、不完全な報告でも「reasonably reliable」と結論 — [IEEE Xplore 6272514](https://ieeexplore.ieee.org/document/6272514)。κ などの数値は本文を読めず未確認
- 25010 自体で課題を分類し、IRR を報告した研究は見つからなかった。技術的負債の研究（arXiv 2212.05537）が 25010:2011 の品質特性で課題に印を付け、κ が 0.8 を超えるまで二人で付け直したと書く（検索要約のみ）。手順のための閾値で、分類体系の信頼性の測定ではない

## 5. Semantic Versioning

**定義（本文確認）**
- MAJOR は互換でない API の変更、MINOR は後方互換な機能の追加、PATCH は後方互換なバグ修正。0.y.z は初期開発で「Anything MAY change at any time」。仕様は CC BY 3.0、作者は Tom Preston-Werner — [semver.org 2.0.0](https://semver.org/)

**改訂と運営**
- 2.0.0 は 2013 年 6 月（Phil Haack の告知）— [SemVer 2.0 Released](https://haacked.com/archive/2013/06/18/semver-2-0-released.aspx/)（検索要約のみ）。以後 13 年、2.0.0 のまま
- 2019 年、Haack が単独の保守者を降り、SemVer を使うパッケージマネージャの代表からなるチームと RFC の手続きに移った：「It's too much responsibility for one person to make these decisions unilaterally」— [SemVer's New Maintainers](https://haacked.com/archive/2019/02/11/semver-collective/)（本文確認）

**守られているか（本文確認、一部要旨のみ）**
- Raemaekers, van Deursen, Visser（JSS 2017）：Maven の 7 年分・22,000 超のライブラリで「around one third of all releases introduce at least one breaking change」— [TU Delft repository](https://repository.tudelft.nl/record/uuid:7c30551c-a00a-49c6-809a-48cc28a1b386)（要旨のみ）
- Ochoa ら（EMSE 2022、外部の差分追試）：119,879 のライブラリ更新と 293,817 の利用者で、更新の 83.4% が SemVer に従い、遵守は時とともに上がった。破壊的変更の影響を受けた利用者は 7.9% — [arXiv 2110.07889](https://arxiv.org/abs/2110.07889)（要旨のみ）。非 major のリリースの 20.1% が破壊的という数値は検索要約のみ
- npm の Decan & Mens（TSE 2019）、Pinckney ら（2023）は本文を読めず未確認
- SemVer の分類（破壊的か否か）は、API の差分という機械で判定できる事実に寄せられるので、人の判断の一致を問う必要が小さい（推論）。ただし「公開 API」と「互換」の範囲を仕様は形式的に定めていない

## 6. Beizer の分類、Tan らの根本原因分類、課題の種別の分類研究

**Beizer（検索要約のみ）**
- 『Software Testing Techniques』第 2 版（1990）の付録「Bug Taxonomy and Statistics」。4 桁の番号で階層を表す（例：3xxx が構造のバグ、9xxx がその他、16xx が要求の変更）。Otto Vinter による改訂版もある — [Kaner, Bug Taxonomies](https://www.kaner.com/pdfs/BugTaxonomies.pdf) など。原典（書籍）は読めていない
- Wagner（2008、報告の表）は、有名な欠陥分類はどれも広く使われなかったとする。Beizer もその一つ（推論）

**Tan ら「Bug characteristics in open source software」（EMSE 2014、本文確認）**
- Linux カーネル、Mozilla、Apache の 2,060 件を、根本原因（memory / concurrency / semantic）、影響、コンポーネントの 3 次元で手作業で分類 — [PDF](https://www.cs.purdue.edu/homes/lintan/publications/bugchar-emse14.pdf)
- semantic は「inconsistencies with the requirements or the programmers' intention that are not memory bugs or concurrency bugs」と、他の 2 つの残りとして定義 — [同](https://www.cs.purdue.edu/homes/lintan/publications/bugchar-emse14.pdf)
- semantic の割合：Mozilla 87.0%、Apache 82.5%、Linux 70.1% — [同](https://www.cs.purdue.edu/homes/lintan/publications/bugchar-emse14.pdf)
- 一致の扱い：各報告を 2 人が独立に見て、食い違えば議論して合意。IRR の数値は報告していない — [同](https://www.cs.purdue.edu/homes/lintan/publications/bugchar-emse14.pdf)
- 最上位の 3 分類は、7〜9 割が一つの残余クラスに入るので、理解を助ける軸としては解像度が低い（推論）

**課題の種別（bug / enhancement / question）の分類研究（本文確認、一部要旨のみ）**
- Kallis ら Ticket Tagger（ICSME 2019 デモ）：GitHub の既定ラベル bug / enhancement / question を、書き手の意図の 3 分類として使う。理由は「included by default in every issue tracker on GitHub repositories」。約 3 万件で F 値 83.1%（bug）、82.3%（enhancement）、82.5%（question）— [PDF](https://digitalcollection.zhaw.ch/bitstream/11475/19309/2/2019_Kallis-etal_Ticket-Tagger-Tool-Demo_ICSME.pdf)
- NLBSE のツール競技（2022：約 80 万件、2023：約 140 万件、2024：3 千件・5 リポジトリ）が同じ 3 分類で続いている — [NLBSE'24 issue-report-classification](https://github.com/nlbse2024/issue-report-classification)（検索要約のみ）。CatIss は micro F1 87.2% — [arXiv 2203.17196](https://arxiv.org/abs/2203.17196)（要旨のみ）
- これらの正解は、プロジェクトが付けたラベルそのもの。Ticket Tagger の論文にも CatIss の要旨にも、正解ラベルの手作業の確認や IRR は書かれていない。Herzig ら（2013）の 33.8% 誤分類を考えると、F 値は「プロジェクトのラベル付けの癖をどれだけ再現したか」を測っている（推論）
