# PR・課題・バグの安定した分類基準

**結論**: 検証を通った主張の範囲で、外部で評価者間一致度（IRR）が測られ、安定性の裏づけが最も強いのは、IBM の Orthogonal Defect Classification（ODC）の欠陥タイプの属性である（少し改変した版で Cohen の κ が 0.66 と 0.82）。標準化された基準として確認できたのは IEEE 1044 だけで、改訂は 1993 年版から 2009 年版への 1 回、その 2009 年版も 2020-03-05 から保守されていない（Inactive-Reserved）。変更（PR・コミット）の意図の分類では Swanson 系の corrective/perfective/adaptive が研究で使われ続けているが、κ は 0.62〜0.66 程度で、adaptive の定義も研究ごとに違う。実務では Conventional Commits へ移りつつあるとされる一方、型の取り違えが最大の課題と報告されている。課題管理の bug/feature の種別ラベルは 33.8% が誤分類だった。人が付けた種別ラベルはそのまま信用できず、理解支援の分類軸には、IRR の実測がある ODC 型の直交する軸を選び、定義と判定例を明示する必要がある（推論）。

この報告は、deep-research のワークフロー（検索・取得・主張ごとに 3 票の敵対的な検証・統合）の結果を、筆者がまとめ直したものである。「票」は検証者 3 人のうち主張を支持した数と反証した数。

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

## 分類軸として使うときの含意（推論）

- **「標準だから安定」は成り立たない。** 唯一の標準（IEEE 1044）は保守されておらず、実務にも広まらなかった。安定性の根拠は、標準であることより、IRR を独立に測れたことに置くほうがよい。
- **人が付けた種別ラベルは入力として信用しない。** bug/feature の 3 分の 1 が誤りで、コミットの意図でも κ は 0.6 台にとどまる。仕組みが分類するなら、ラベルを読むのではなく、判定の根拠（どの事実からそう判定したか）を添えて付け直すほうがよい。
- **一つの多値の分類より、直交する複数の軸。** ODC が IRR を確保した設計の要は直交性（互いに排他で区別できること）と、判定例による較正だった。「何が壊れたか」「いつ・どこで入ったか」「どれだけ影響するか」を別の軸にすると、一つの軸の中での迷い（CCS の型の取り違えのようなもの）が減ると考えられる。
- **ラベル名だけを借りない。** corrective/adaptive は研究ごとに定義が違った。軸を採るときは、定義の出典と版を固定し、境界の事例（テストの追加、コードの削除、軽微な修正）の判定例を一緒に持つ。

## 確かめられなかったこと

- 問いに挙げた候補のうち、CWE・CVSS、Beizer の分類、ISO/IEC 25010、Semantic Versioning、Tan らの根本原因分類、課題の種別の分類研究、Bugzilla・Jira・Mozilla の重大度・優先度（S1〜S4）の定義は、検証を通った主張に入らなかった。これらについては何も言えない。（重大度については、別の調査 [課題とバグの理解支援 先行事例](../research_notes/課題とバグの理解支援%20先行事例/triage_and_incident_practice.md) が、Mozilla が 2020 年に Severity の記入を必須にした経緯を一次資料で確かめている。）
- ODC の属性の数（8 つの欠陥タイプ、6 次元）という主張は、検証で反証された（1-2、0-3）。具体的な属性値は、版（v5.2 など）と出典を確かめ直す必要がある。
- 根拠の多くはそれぞれ 1 本の一次資料で、複数の独立した資料で裏づけられたのは IEEE 1044 の状態と改訂履歴だけ。
- ODC の IRR は 1998 年、Wagner は 2008 年、Herzig は 2013 年のもので、対象は単一のプロジェクトか少数の Java OSS。今の GitHub の PR や課題の慣行に当てはまるかは確かめていない。
- IRR の数値は条件がそろっていない（Cohen の κ、Krippendorff の α、単純一致率が混在し、分類を作った本人同士や議論後の一致も含む）。外部の評価者が独立に当てはめたときの信頼性として比べられるのは、El Emam & Wieczorek と Trautsch らの数値だけ。
- 「標準化されていて、今も保守されている欠陥分類」は、この調査の範囲では見つからなかった。
