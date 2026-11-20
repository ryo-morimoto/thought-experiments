# PR・課題・バグの安定した分類基準

**結論**: 検証を通った主張の範囲で、外部で評価者間一致度（IRR）が測られ、安定性の裏づけが最も強いのは、IBM の Orthogonal Defect Classification（ODC）の欠陥タイプの属性である（少し改変した版で Cohen の κ が 0.66 と 0.82）。欠陥そのものの分類の標準として確認できたのは IEEE 1044 だけで（補遺で、品質特性の標準 ISO/IEC 25010 と、ITU-T X.1521 になった CVSS を加えた）、改訂は 1993 年版から 2009 年版への 1 回、その 2009 年版も 2020-03-05 から保守されていない（Inactive-Reserved）。変更（PR・コミット）の意図の分類では Swanson 系の corrective/perfective/adaptive が研究で使われ続けているが、κ は 0.62〜0.66 程度で、adaptive の定義も研究ごとに違う。実務では Conventional Commits へ移りつつあるとされる一方、型の取り違えが最大の課題と報告されている。課題管理の bug/feature の種別ラベルは 33.8% が誤分類だった。補遺で調べた候補もこの見立てを変えなかった。広く採用され標準にもなった CVSS では、同じ人が 9 か月後に評価し直すと 68% の人で重大度が変わり、NVD の CVE の 55% は無効か不足した CWE に対応づけられ、重複バグ報告の重大度は最大 51% で食い違った。改訂が少なく遵守も測られているのは Semantic Versioning（2.0.0 のまま 13 年、Maven の更新の 83.4% が遵守）だが、これは人の判断より API の差分という事実で決まる分類である。人が付けた種別ラベルはそのまま信用できず、理解支援の分類軸には、IRR の実測がある ODC 型の直交する軸か、機械で確かめられる事実に寄せた軸を選び、定義と判定例を明示する必要がある（推論）。

この報告は、deep-research のワークフロー（検索・取得・主張ごとに 3 票の敵対的な検証・統合）の結果を、筆者がまとめ直したものである。「票」は検証者 3 人のうち主張を支持した数と反証した数。「補遺」の節は、初回に扱えなかった候補を一次資料で補ったもので、3 票の検証は経ていない（詳細と出典: [補遺の調査ノート](../research_notes/PR課題バグの安定した分類基準/supplement.md)）。

## 基準ごとの検証済みの事実

<!-- data-source: original（検証を通った主張を筆者が整理した表） -->
| 基準 | 確かめられたこと | IRR の実測 | 出典 | 検証 |
|---|---|---|---|---|
| ODC（Chillarege ら 1992） | 欠陥を「開発プロセスのどこに注意が要るか」を指すクラスに分ける。直交性（互いに排他で区別できること）を要件にし、それで分類の人的誤りが減ると主張。原論文は IRR を測らず、較正は今後とした | 原論文には無い | [Chillarege](https://chillarege.com/docs/Papers/concept) | 3-0 |
| ODC 欠陥タイプの改変版（PSP にも採用） | コードインスペクションの実データ 2 組（計 605 件）で測定、著者は「概ね再現可能」と結論 | κ 0.66 と 0.82（両者が見つけた 140 件で計算）。一部カテゴリ間の混同が多い | [El Emam & Wieczorek 1998](https://www.ehealthinformation.ca/web/default/files/wp-files/isern-98-09.pdf) | 2-1 / 3-0 |
| IEEE 1044（ソフトウェア異常の分類） | 異常を一様に分類する標準。1993 年版を 2009 年版（発行 2010-01-07）が置き換え、2009 年版は 2020-03-05 に Inactive-Reserved。撤回ではなく入手は可能 | 確認できず | [IEEE SA 1044-2009](https://standards.ieee.org/ieee/1044/4607)、[1044-1993](https://standards.ieee.org/standard/1044-1993.html) | 3-0 |
| 欠陥分類の実務での普及（Wagner 2008） | 有名な欠陥分類はどれも広く使われるに至らず、実務で見るのは影響度・重大度の分類くらい | — | [Wagner, DEFECTS'08](https://wwwbroy.in.tum.de/publ/papers/defects08.pdf) | 3-0 |
| バグの根本原因 9 分類（Catolino ら 2019） | Mozilla・Apache・Eclipse の 1,280 件から作った研究上の分類 | Krippendorff の α 0.65→0.76→0.96。分類を作った本人 2 人の、議論を挟んだ一致 | [arXiv 1907.11031](https://arxiv.org/pdf/1907.11031) | 3-0 |
| 課題の種別ラベル（Herzig ら 2013） | 5 つの OSS の 7,000 件超を手で調べると 33.8% が誤分類 | — | [ICSE 2013](https://www.microsoft.com/en-us/research/publication/its-not-a-bug-its-a-feature-how-misclassification-impacts-bug-prediction/) | 3-0 |
| Swanson 系のコミット意図 | 54 OSS の 2,533 コミット。コード削除やテスト追加を開発者は corrective、研究者は perfective とみなすなど、見方が分かれた | κ 0.66（研究者 2 人）。Mauczka らのデータの付け直しで 0.62（研究者同士）、0.63（研究者と開発者） | [Trautsch ら](https://arxiv.org/pdf/2109.03544) | 3-0 |
| 同じラベル名の定義の揺れ（Levin & Yehudai 2017） | Adaptive を「新機能の導入」と定義（Swanson の原義は環境の変化への適応） | 単純一致率 79%→議論後 94.5%（κ ではない） | [arXiv 1711.05340](https://arxiv.org/pdf/1711.05340) | 3-0 |
| Conventional Commits（Zeng ら 2025） | 研究は Swanson の 3 クラスに集中し、実務は CCS（10 の型）へ移りつつあるという位置づけ。GitHub の課題と Stack Overflow の質問では、型の取り違えが最多の課題 | 測られていない | [ICSE 2025](https://conf.researchr.org/details/icse-2025/icse-2025-research-track/28/A-First-Look-at-Conventional-Commits-Classification) | 3-0 / 2-1 |

## 補遺：初回に扱えなかった候補

一次資料の本文を読んで確かめた。「要旨のみ」「検索要約のみ」は本文を読めていないもの。3 票の検証は経ていない。出典の詳細は [補遺の調査ノート](../research_notes/PR課題バグの安定した分類基準/supplement.md)。

<!-- data-source: original（一次資料を筆者が整理した表） -->
| 基準 | 粒度と改訂 | 採用 | 一致・誤りの実測 | 出典 |
|---|---|---|---|---|
| CWE（MITRE） | Pillar / Class / Base / Variant の 4 段の抽象度に、Category と View。対応づけは Base か Variant、Category は不可。2006 年の初版から 5.0 まで 60 版（年 3 版ほど、推論） | NVD が CVE ごとに付ける（View-1003、約 130 の CWE） | 2024-12 の NVD で CVE の 55% が無効か不足した CWE（空欄 18.4%、CWE-Other 10.8%、CWE-noinfo 10%、Prohibited/Discouraged 16.2%）。コードに根ざした判定との完全一致は 49.70%、明らかな誤りは 3.63%（査読前、要旨のみ）。評価者間の κ は見つからず | [Guidance](https://cwe.mitre.org/documents/cwe_usage/guidance.html)、[Şimşek ら 2025](https://people.bu.edu/staro/COMPSAC-2025-final.pdf)、[Nong ら 2026](https://arxiv.org/abs/2608.21977) |
| CVSS（FIRST） | 0〜10 の点と 5 段の重大度。v2 は 2007-06、v3.0 は 2015-06、v3.1 は 2019-06（v3.x の日付は検索要約のみ）、v4.0 は 2023-11-01。v3.0 は ITU-T X.1521（検索要約のみ） | NVD をはじめ業界標準として広く使われる | 利用者 196 人で Attack Vector、User Interaction、Scope がそろわず。同じ 59 人が 9 か月後に評価し直すと 68% の人で重大度が変わった（評価者内）。30% は文書を読んだことがない | [v4.0](https://www.first.org/cvss/v4.0/specification-document)、[v2 History](https://www.first.org/cvss/v2/history)、[Wunder ら S&P 2024](https://arxiv.org/abs/2308.15259) |
| CVSS への批判 | curl は CVSS をやめ、独自の 4 段にした（2025-01-23） | — | — | [Stenberg](https://daniel.haxx.se/blog/2025/01/23/cvss-is-dead-to-us/) |
| Mozilla の Severity と Priority | S1〜S4 と N/A（Task・Enhancement 用）、P1〜P5（P4 はボット用）。手引きは各段を例で示す。2020 年に Severity を必須化 | Firefox の Bugzilla | 測られていない | [BMO Bug Fields](https://wiki.mozilla.org/BMO/UserGuide/BugFields)、[Severity guide](https://firefox-source-docs.mozilla.org/bug-mgmt/guides/severity.html) |
| Bugzilla・Jira の既定 | Bugzilla は Priority P1〜P5、Severity は blocker〜trivial（6 段）。Jira は Highest〜Lowest の 5 段で、各段の公式の定義は見つからず、管理者が変えられる（Jira は検索要約のみ） | 既定値として広く入っている | 重複バグ報告で重大度が食い違ったのは OpenOffice 28.9%、Mozilla 36.6%、Eclipse 50.8%。標本の 95% は本当に同じ問題だった | [Bugzilla docs](https://bugzilla.readthedocs.io/en/latest/using/understanding.html)、[Tian ら EMSE 2016](https://sailresearch.github.io/sail-website/data/pdfs/EMSE2015_OnTheUnreliabilityOfBugSeverityData.pdf) |
| Chromium のセキュリティ重大度 | Critical / High / Medium / Low を「攻撃者に何ができるか」で定義し、実在のバグを例に挙げる。緩和要因で 1〜2 段下げる。Critical は 30 日、High は 60 日で修正を配る。Critical→P0、High・Medium→P1、Low→P3 | Chromium | 測られていない | [Severity Guidelines](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md) |
| ISO/IEC 25010 | 2011 年版の 8 特性を 2023-11 の第 2 版が置き換え、Safety を追加、Usability→interaction capability、Portability→flexibility など。前身の 9126 から約 12 年ごとに名前が変わる | 標準 | 25010 での IRR は見つからず。前身の 9126 で欠陥 78 件を分類し、主特性は副特性より信頼性が高かった（検索要約のみ、数値未確認） | [25010:2023 前書き](https://cdn.standards.iteh.ai/samples/78176/13ff8ea97048443f99318920757df124/ISO-IEC-25010-2023.pdf)、[Vetro ら 2012](https://ieeexplore.ieee.org/document/6272514) |
| Semantic Versioning | MAJOR / MINOR / PATCH。2.0.0（2013-06、検索要約のみ）のまま。2019 年に単独保守から、パッケージマネージャの代表のチームと RFC へ | 主要なパッケージマネージャ | Maven で約 3 分の 1 のリリースに破壊的変更（Raemaekers ら 2017）。追試では更新の 83.4% が遵守し、遵守は年とともに上昇（Ochoa ら 2022）。どちらも要旨のみ | [semver.org](https://semver.org/)、[Haack 2019](https://haacked.com/archive/2019/02/11/semver-collective/)、[Raemaekers ら](https://repository.tudelft.nl/record/uuid:7c30551c-a00a-49c6-809a-48cc28a1b386)、[Ochoa ら](https://arxiv.org/abs/2110.07889) |
| Beizer の分類 | 4 桁の番号の階層（1990、書籍の付録）。原典は読めず（検索要約のみ） | 広まらなかった（Wagner 2008 から推論） | 見つからず | [Kaner](https://www.kaner.com/pdfs/BugTaxonomies.pdf) |
| Tan らの根本原因分類 | 根本原因（memory / concurrency / semantic）・影響・コンポーネントの 3 次元。semantic は他の 2 つの残り | 研究で再利用 | 2 人が独立に見て議論で合意、IRR の数値は無し。semantic が Mozilla 87.0%、Apache 82.5%、Linux 70.1% | [Tan ら EMSE 2014](https://www.cs.purdue.edu/homes/lintan/publications/bugchar-emse14.pdf) |
| 課題の種別（bug / enhancement / question） | GitHub の既定ラベルをそのまま 3 分類に。Ticket Tagger（2019）、NLBSE の競技（2022〜2024） | 研究の共通課題 | 正解はプロジェクトのラベルで、手作業の確認や IRR は書かれていない。F 値は 82〜87% | [Ticket Tagger](https://digitalcollection.zhaw.ch/bitstream/11475/19309/2/2019_Kallis-etal_Ticket-Tagger-Tool-Demo_ICSME.pdf)、[CatIss](https://arxiv.org/abs/2203.17196) |

## 分類軸として使うときの含意（推論）

- **「標準だから安定」は成り立たない。** 唯一の標準（IEEE 1044）は保守されておらず、実務にも広まらなかった。安定性の根拠は、標準であることより、IRR を独立に測れたことに置くほうがよい。
- **人が付けた種別ラベルは入力として信用しない。** bug/feature の 3 分の 1 が誤りで、コミットの意図でも κ は 0.6 台にとどまる。仕組みが分類するなら、ラベルを読むのではなく、判定の根拠（どの事実からそう判定したか）を添えて付け直すほうがよい。
- **一つの多値の分類より、直交する複数の軸。** ODC が IRR を確保した設計の要は直交性（互いに排他で区別できること）と、判定例による較正だった。「何が壊れたか」「いつ・どこで入ったか」「どれだけ影響するか」を別の軸にすると、一つの軸の中での迷い（CCS の型の取り違えのようなもの）が減ると考えられる。
- **採用が広いことも安定の根拠にならない。** CVSS は業界標準で ITU-T の勧告にもなったが、同じ人の再評価で 68% の人の重大度が変わった。CWE は NVD の CVE の過半で無効か不足した対応づけだった。重大度のラベルも、同じ問題を指す報告の間で最大 51% 食い違った。広く使われる段階評価ほど、付けた値を事実として読まず、根拠（どの指標をどう判断したか）を一緒に見せるほうがよい。
- **事実で決まる軸は安定しやすい。** SemVer の major/minor/patch は、改訂が 13 年なく、遵守も測られ、追試で 8 割超の遵守だった。人の判断より API の差分で決まるからだと考えられる。Chromium の重大度も「攻撃者に何ができるか」という確かめられる事実で段を定義し、実在のバグを例にしている。軸を選ぶときは、判定を事実の確認に落とせるかを見る。
- **残余クラスが大きい軸は解像度が低い。** Tan らの根本原因では semantic（他の 2 つ以外）が 7〜9 割を占めた。理解支援で使うなら、その中をさらに分ける別の軸が要る。
- **ラベル名だけを借りない。** corrective/adaptive は研究ごとに定義が違った。軸を採るときは、定義の出典と版を固定し、境界の事例（テストの追加、コードの削除、軽微な修正）の判定例を一緒に持つ。

## 確かめられなかったこと

- 補遺の候補は一次資料で補ったが、3 票の敵対的な検証は経ていない。次は本文を読めず、要旨か検索要約だけで書いた：CVSS v3.0・v3.1 の公開日と ITU-T X.1521、Allodi らの CVSS 採点の正確さの研究、Jira の既定の優先度、SemVer 2.0.0 の公開日、Raemaekers らと Ochoa らの数値（要旨のみ）、Vetro らの ISO/IEC 9126 での一致の数値、Beizer の分類の原典、Herraiz らの Eclipse の重大度の研究、NLBSE の競技のデータの作り方、Nong らの NVD の CWE の監査（査読前）。
- CWE の対応づけと ISO/IEC 25010 の分類で、複数の評価者が独立に付けたときの IRR（κ など）は見つからなかった。CVSS の 68% は同じ人の時間をおいた再評価の不一致で、評価者間の一致ではない。
- CWE の各版の公開日、Chromium の一般のバグの優先度（Pri-0〜3）の定義、npm の SemVer 遵守の研究（Decan & Mens 2019 など）は確かめていない。
- ODC の属性の数（8 つの欠陥タイプ、6 次元）という主張は、検証で反証された（1-2、0-3）。具体的な属性値は、版（v5.2 など）と出典を確かめ直す必要がある。
- 根拠の多くはそれぞれ 1 本の一次資料で、複数の独立した資料で裏づけられたのは IEEE 1044 の状態と改訂履歴だけ。
- ODC の IRR は 1998 年、Wagner は 2008 年、Herzig は 2013 年のもので、対象は単一のプロジェクトか少数の Java OSS。今の GitHub の PR や課題の慣行に当てはまるかは確かめていない。
- IRR の数値は条件がそろっていない（Cohen の κ、Krippendorff の α、単純一致率が混在し、分類を作った本人同士や議論後の一致も含む）。外部の評価者が独立に当てはめたときの信頼性として比べられるのは、El Emam & Wieczorek と Trautsch らの数値だけ。
- 「標準化されていて、今も保守されている欠陥分類」は、この調査の範囲では見つからなかった。今も保守されている弱点の分類として CWE（MITRE が年に数版を出す）はあるが、標準化団体の規格ではなく、NVD での対応づけの過半が無効か不足していた。
