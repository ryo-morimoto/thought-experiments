# データセットのメタデータ/ドキュメント標準とライセンスツールの限界（公開性・明確なライセンス・再利用許諾・ライセンス遵守の保証手段として）

調査日: 2026-11-20。各標準について一次資料（仕様書・論文）を優先した。今回のセッションで直接確認できなかった項目は「未検証」と明記した。
層の定義（依頼文による）: (1) 内部整合性、(2) 事実整合性（宣言が現実と一致しているか、権利者性）、(3) 法的評価。条件付き証明の追加要件: 網羅性（未宣言のデータがないこと）、忠実性（チェック規則が実際のライセンス義務を含意すること）、証拠保全（当時の条項の版を残すこと）。

## Q1: 各標準・ツールは何を記録し、何を保証・検証するか。どの層・要件をカバーするか

### Takeaway
調査した標準（Datasheets、Data Cards、Croissant/RAI、HF dataset card、DCAT、schema.org、Data Package、DataCite、D&TA）はいずれも、ライセンスを「記述する語彙や設問」を提供するだけである。層(2)（事実整合性・権利者性）と層(3)（法的評価）を検証する仕組みはどれも持たない。多少なりとも事実検証に踏み込んでいるのは Data Provenance Initiative（DPI）の人手による再アノテーションだけだが、DPI 自身が「自己申告ライセンスのベストエフォート分類であり、法的助言ではない」と明言している。

### Cited Findings

**Data Provenance Initiative（DPI）/ DPCollection**
- 1800以上のテキストデータセットを監査・追跡した。ホスティングサイトについては「70%+ のライセンス欠落」「50%+ の誤分類率」を報告している。著者は Longpre, Mahari, … Luis Villa, Sara Hooker ら17名（arXiv:2310.16787, 2023-10）— [arXiv abs](https://arxiv.org/abs/2310.16787)
- ライセンスアノテーションは5段階の人手手順で行う。(1) GitHub/arXiv/HF/Papers with Code/コレクション本体から自己申告ライセンスを集める。(2) コードではなくデータに対して付与された明示的ライセンスを探す。HF のラベルは「データセット作成者本人がアップロードしたもの」に限って採用する。(3) ライセンス種別（MIT, Apache 2, CC BY-SA, Custom, Request Form, Unspecified）を決める。(4) Permitted Use（商用/非商用・学術）、Attribution、Share-Alike の3軸に分類する。ライセンスが複数あるときは軸ごとに最も厳しいものを採る。(5) 追加の来歴情報（ソース、作成者、競合関係など）を集める — [DPI 論文 PDF §2.2](https://arxiv.org/pdf/2310.16787)
- 論文は、ベストエフォートの検証であり法的助言ではないと述べる。さらに「元データを他所から得たデータセットでは、作成者が実際に著作権上の利益を持つかが重要な前提だが、ケースバイケースの分析が必要」とし、「大半の開発者は自分だけがデータセットを所有していると仮定して動いているようだ」と指摘している。これは層(2)の権利者性を DPI も解決していないことを示す — [DPI 論文 PDF §2.2](https://arxiv.org/pdf/2310.16787)
- 論文末尾の注記: "Collected License Information is NOT Legal Advice… we collect self-reported licenses, and categorize them according to our best efforts" — [DPI 論文 PDF](https://arxiv.org/pdf/2310.16787)
- 出力は「Data Provenance Card」で、Symbolic Attribution（データの参考文献一覧に相当する構造化来歴ストア）として自動生成される。生成物は GitHub の Data-Provenance-Collection リポジトリにある — [DPI 論文 PDF §2.3](https://arxiv.org/pdf/2310.16787)

**Datasheets for Datasets（Gebru ら）**
- 著者は Gebru, Morgenstern, Vecchione, Wortman Vaughan, Wallach, Daumé III, Crawford。CACM 2021年12月掲載（arXiv:1803.09010）。自動化ではなく、標準化された文書化プロセスとして提案された — [arXiv abs](https://arxiv.org/abs/1803.09010)
- ライセンス関連の設問は次のとおり。「著作権その他のIPライセンスや利用規約（ToU）の下で配布するか。するならライセンス/ToUを説明し、リンクを示すか条項を再掲せよ」「第三者がインスタンスに関連するデータにIP上の制約を課しているか」「輸出規制など規制上の制約があるか」 — [Datasheets PDF](https://arxiv.org/pdf/1803.09010)
- 外部資源への依存についても設問がある。「外部資源（Web、ツイート、他データセット）にリンク・依存しているか。それらが存続し不変である保証はあるか。作成時点の外部資源を含む公式アーカイブ版はあるか。外部資源にライセンスなどの制約はあるか」。証拠保全と網羅性に相当する問いを自由記述で求めているが、検証はしない — [Datasheets PDF](https://arxiv.org/pdf/1803.09010)

**Data Cards（Google）**
- Pushkarna, Zaldivar, Kjartansson（Google Research）による arXiv:2204.01075（2022-04、FAccT 2022 投稿）。上流ソース、収集・アノテーション方法、意図された用途などを構造化して要約する「ユーザー中心のプロダクト」としての文書であり、20以上の Data Card を展開した教訓を報告している — [arXiv abs](https://arxiv.org/abs/2204.01075)

**Croissant（MLCommons）1.0**
- 仕様 1.0 は 2024-03-01 公開。`sc:license` は Required で、型は CreativeWork または URL、複数指定可。「既知ライセンスの URL を推奨」としており、SPDX 一覧は例示にとどまり必須ではない — [Croissant spec](https://docs.mlcommons.org/croissant/docs/croissant-spec.html)
- `datePublished` は Required、`version` は Recommended（SemVer を推奨）。FileObject には `sha256` があり、バージョン付きデータセットでは全 FileObject へのチェックサム記録を「強く推奨」している。ライブデータセットでは、変化するファイルのチェックサムを省略する — [Croissant spec](https://docs.mlcommons.org/croissant/docs/croissant-spec.html)
- 派生関係について、仕様本文には `prov:wasDerivedFrom` や `isBasedOn` のプロパティ表がない（`sameAs` は「同一データセットの別リソース」の意味）— [Croissant spec](https://docs.mlcommons.org/croissant/docs/croissant-spec.html)
- 仕様例にも不整合がある。PASS 例の `sha256` 値が32桁（MD5相当の長さ）になっている — [Croissant spec](https://docs.mlcommons.org/croissant/docs/croissant-spec.html)

**Croissant RAI 拡張 1.0**
- 2024-03-06 公開。`rai:dataCollection`、`rai:dataCollectionType`、`rai:dataCollectionRawData`、`rai:dataCollectionTimeframe`、`rai:dataPreprocessingProtocol`、`rai:dataManipulationProtocol`、`rai:dataReleaseMaintenancePlan` などを持つ。ライセンス・著作権・同意の専用プロパティはなく、ライセンスはコアの `sc:license` に委ねている。来歴・系譜も「コア語彙がカバーすることを期待」としている。どのプロパティが必須かは明示されていない（必須なのは `dct:conformsTo` の宣言だけ）。例と表でプロパティ名が食い違っている — [Croissant RAI spec](https://docs.mlcommons.org/croissant/docs/croissant-rai-spec.html)

**Hugging Face dataset card**
- README.md 冒頭の YAML に `license: "any valid license identifier"` を書く。HF のライセンス表のキーワードを使った場合だけ、ページにライセンスが表示される — [HF Hub docs: Dataset Cards](https://huggingface.co/docs/hub/datasets-cards)
- 仕様テンプレートの関連フィールドは `license`（例: apache-2.0 または HF ライセンス表の値）、`license_name`（カスタムライセンスの ID）、`license_link`（リポジトリ内の LICENSE ファイルまたは URL）、`license_details`（レガシーの自由記述）、`source_datasets`（例: wikipedia, laion/laion-2b）。`source_datasets` は自由記述の識別子であり、ライセンスの伝播を検査する仕組みは記述されていない — [hub-docs datasetcard.md](https://raw.githubusercontent.com/huggingface/hub-docs/main/datasetcard.md)

**DCAT 3（W3C）**
- 2024-08-22 に W3C 勧告。`dcterms:license` は「リソースが利用可能とされる法的文書」、`dcterms:rights` は license/accessRights で扱わない権利の記述（例: 著作権表示）、`dcterms:accessRights` はアクセス可能者やセキュリティ状態、`odrl:hasPolicy` は ODRL 準拠ポリシーである。ライセンス・権利情報は MAY で任意 — [W3C DCAT 3](https://www.w3.org/TR/vocab-dcat-3/)
- 系譜は `dcat:qualifiedRelation`（`prov:qualifiedInfluence` のサブプロパティ）で表す。関係種別として `prov:wasDerivedFrom` / `prov:wasRevisionOf` などを使える。Dataset には `prov:wasGeneratedBy` もある — [W3C DCAT 3](https://www.w3.org/TR/vocab-dcat-3/)

**schema.org**
- `license` は「このコンテンツに適用されるライセンス文書。通常は URL で示す」と定義される。期待型は CreativeWork または URL、ドメインは CreativeWork（Dataset を含む）— [schema.org/license](https://schema.org/license)

**Frictionless Data Package v2**
- `licenses` は配列でなければならない（MUST）。各要素は `name` と `path` の少なくとも一方を含む必要があり（MUST）、`title` は任意（MAY）。`name` は「Open Definition license ID を含む文字列」と説明されるが、RFC 2119 の MUST はない。仕様自体に "This property is not legally binding." と明記されている — [Data Package v2](https://datapackage.org/standard/data-package/)
- `sources` は配列でなければならない（MUST）。各 Source は最低1プロパティを持つ（MUST）。`title` を推奨（RECOMMENDED）し、`path`、`email`、`version` は任意（MAY）— [Data Package v2](https://datapackage.org/standard/data-package/)

**DataCite Metadata Schema 4.6**
- Rights は Optional で 0〜n 回。サブプロパティは `rightsURI`、`rightsIdentifier`、`rightsIdentifierScheme`（例: SPDX）、`schemeURI`（例: https://spdx.org/licenses/）— [DataCite 4.6 Rights](https://datacite-metadata-schema.readthedocs.io/en/4.6/properties/rights/)

**Data & Trust Alliance Data Provenance Standards**
- v1.0.0 は 2024-07-09 発表（プロジェクト開始は 2023-11-30）。22のメタデータフィールドを Source / Provenance / Use の3群に分ける。ライセンス関連は「License to use」、同意関連は「Consent documentation location」で、著作権の専用フィールドはない。系譜関連として Source metadata for dataset、Dataset issuer、Data origin geography、Method、Date of previously issued version がある — [D&TA Data Provenance Standards](https://www.dtaalliance.org/work/data-provenance-standards)
- 検証・認証の仕組みは記述されていない。遵守状況の監視は採用組織側に委ねられている（「第三者のコンプライアンスを含め遵守を監視する指標を定義・実装せよ」）。また、標準は「特定のデータ保護法への準拠を保証しない」と明記している — [D&TA Data Provenance Standards](https://www.dtaalliance.org/work/data-provenance-standards)
- ドラフト段階では8カテゴリ（source, legal rights, privacy, generation date, data type, method, intended use, restrictions, lineage）があり、v1.0 で3つに整理された。メタデータ生成ツールは JSON/XML/YAML/CSV を出力する — [Help Net Security インタビュー 2024-07](https://www.helpnetsecurity.com/2024/07/22/saira-jesani-data-trust-alliance-data-provenance-standards/); [IAPP](https://iapp.org/news/a/leading-corporations-proposed-data-provenance-standards-aims-to-enhance-quality-of-ai-training-data)（二次資料）

### Inferences
層・要件ごとのカバレッジ（上記の一次資料に基づく推論）:

<!-- data-source: original（調査担当による整理） -->
| 対象 | 層1 内部整合性 | 層2 事実整合性/権利者性 | 層3 法的評価 | 網羅性 | 忠実性 | 証拠保全 |
|---|---|---|---|---|---|---|
| DPI / DPCollection | 部分的（構造化カードを生成） | **部分的**（人手で一次情報まで遡って再アノテーション。ただし権利者性は未解決と自認） | なし（法的助言ではないと明記） | なし（対象は収集済みコレクションのみ） | 粗い（3軸カテゴリに縮約。最も厳しいものを採る集約は保守的近似） | なし（条項の版の保存は論文中に記述なし） |
| Datasheets | なし（自由記述） | なし | なし | 設問として問う（外部資源依存） | なし | 設問として問う（アーカイブ版の有無） |
| Data Cards | なし | なし | なし | なし | なし | なし |
| Croissant(+RAI) | スキーマ上の必須性のみ（license 必須） | なし | なし | 部分的（FileObject 列挙と sha256） | なし | 部分的（sha256・version・datePublished。ライセンス条項自体の保存はない） |
| HF card | 表示用の識別子 | なし | なし | なし | なし | git 履歴のみ（推論） |
| DCAT 3 | 語彙のみ（license は MAY） | なし | ODRL で機械可読ポリシーを表現できるが評価はしない | なし | ODRL を使えば忠実性を表現する余地あり（推論） | なし |
| schema.org | 語彙のみ | なし | なし | なし | なし | なし |
| Data Package | JSON Schema で構造を検証 | なし | なし（"not legally binding"） | 部分的（resources 列挙） | なし | なし |
| DataCite | 語彙のみ（Rights は Optional） | なし | なし | なし | なし | DOI による版固定（推論。未検証） |
| D&TA | 語彙のみ | なし（検証機構なし） | なし（法準拠を保証しないと明記） | なし | なし | 「前版の日付」フィールドのみ |

- 原理的な限界: どの標準も宣言を記述する言語であり、宣言と現実の対応（層2）と法解釈（層3）は標準の外にある。ODRL のような機械可読ポリシーを使っても、ポリシーが元のライセンス文と一致していること（忠実性）は別途の人手判断になる（推論）。
- 実装上の限界: Croissant の SPDX 非強制、Data Package の `name` が SHOULD ですらない点、DataCite と DCAT でライセンスが任意である点は、仕様を改訂すれば埋められる類の欠落である（推論）。
- ユーザーの SOURCE.toml 方式（SPDX 必須、allowlist、share-alike の系譜チェック、NOTICE 生成）は、層1と忠実性の一部について、調査したどの標準よりも厳格である。層2と証拠保全の欠落は既存標準を採用しても補えない（推論）。

### Gaps
- Data Provenance Explorer の現在の機能（フィルタ、カード生成、収録数、モダリティ）は、dataprovenance.org のページ本文を取得できず未検証。後続研究（Consent in Crisis、マルチモーダル監査など）の数値も今回は確認していない。
- DCAT-AP（EU プロファイル）固有の制約（license の必須度、管理語彙）は未取得で未検証。DCAT 3 の Distribution レベルの license 定義本文（§6.8.5）も未読。
- DataCite の `relatedIdentifier` における relationType `IsDerivedFrom` / `IsSourceOf` の存在は、今回取得したページでは確認できなかった（存在すると記憶しているが未検証）。
- Data Cards の具体的なライセンス関連フィールドは、論文本文やテンプレートを未読のため未検証。

## Q2: ライセンスメタデータは何かに照らして検証されるのか、それとも純粋な自己申告か。検証ツールは何をチェックするか

### Takeaway
仕様レベルでは、すべて自己申告である。仕様が構造上の必須性を課している例は Croissant の `sc:license` 必須と Data Package の `licenses` 構造（MUST）くらいで、値が実在の正しいライセンスかどうかまで検証する仕組みは仕様に書かれていない。ライセンスの実質を検証した唯一の例は DPI による人手の再監査である。

### Cited Findings
- HF: 表にあるキーワードを使えばライセンスがページに表示される、と書かれているだけである。表にない値を拒否するかどうかはドキュメントに記載がない — [HF Hub docs](https://huggingface.co/docs/hub/datasets-cards)
- DPI は、HF のライセンスラベルを「データセット作成者本人がアップロードしたもの」に限って採用した。プラットフォームのラベルを無条件には信頼していない — [DPI 論文 PDF §2.2](https://arxiv.org/pdf/2310.16787)
- Data Package の `licenses` は構造に MUST がある一方、"not legally binding" とされる — [Data Package v2](https://datapackage.org/standard/data-package/)
- D&TA には検証・認証機構がなく、遵守監視は採用組織に委ねられている — [D&TA](https://www.dtaalliance.org/work/data-provenance-standards)
- Jewitt ら（2026-02, arXiv:2602.08816）は、メタデータではなくライセンスファイルと notice を真実の源とみなすべきだと結論している — [arXiv abs](https://arxiv.org/abs/2602.08816)

### Inferences
- 構造バリデータ（JSON Schema、SHACL など）が検証できるのは層1の形式面までで、ライセンス ID が SPDX 語彙に属するかの照合が上限である（推論）。

### Gaps
- `mlcroissant validate` が何を検査するか（license 値の形式チェックの有無）は、仕様ページに記載がなく未検証。
- Frictionless の validator（frictionless-py、datapackage-validator.datist.io）が license の `name` を Open Definition/SPDX 一覧と照合するかは未検証。
- HF Hub が YAML の `license` 値をスキーマ検証してプッシュを拒否するかどうかは、公式ドキュメントで確認できなかった。

## Q3: 系譜（derived-from 関係）とライセンス伝播はサポートされるか

### Takeaway
派生関係を記述できるのは DCAT 3（`dcat:qualifiedRelation` と PROV-O の `prov:wasDerivedFrom`）、HF（`source_datasets` の自由識別子）、Data Package（`sources`）、D&TA（Source/Provenance 群）である。ただし、派生元のライセンス義務を派生物へ伝播させて整合性を検査する機構は、どの標準にもない。伝播を扱った実例は DPI の「複数ライセンスのうち最も厳しいものを採る」集約だけで、これも人手による分類ルールである。

### Cited Findings
- DCAT 3: `dcat:qualifiedRelation` は `prov:qualifiedInfluence` のサブプロパティで、関係種別に `prov:wasDerivedFrom` / `prov:wasRevisionOf` を使える — [W3C DCAT 3](https://www.w3.org/TR/vocab-dcat-3/)
- Croissant コア仕様には派生関係のプロパティ表がなく、RAI 拡張は系譜をコア語彙に委ねている — [Croissant spec](https://docs.mlcommons.org/croissant/docs/croissant-spec.html); [Croissant RAI spec](https://docs.mlcommons.org/croissant/docs/croissant-rai-spec.html)
- HF の `source_datasets` は "wikipedia" や "laion/laion-2b" のような識別子の列挙である — [hub-docs datasetcard.md](https://raw.githubusercontent.com/huggingface/hub-docs/main/datasetcard.md)
- DPI: ライセンスの85%が帰属表示を、30%が share-alike 条項を要求していた。実務者は、衝突する複数の share-alike ライセンスを解決する明確な方法がないまま再パッケージ化している。share-alike ライセンスが、より制限的またはより緩い条件で上書きされることも頻繁にある — [DPI 論文 PDF](https://arxiv.org/pdf/2310.16787)
- 下流への伝播の実測（Jewitt ら 2026）: 124,278 の dataset→model→application チェーン（データセット 3,338、モデル 6,664、アプリ 28,516。HF と GitHub）を監査した。上流が完全なライセンス証拠を備えていても、準拠した dataset notice を保持していたモデルは 27.59%、準拠した model notice を保持していたアプリは 5.75%、上流 notice を何か1つでも保持していたアプリは 6.38% だった — [arXiv:2602.08816](https://arxiv.org/abs/2602.08816)

### Inferences
- ユーザーの share-alike 系譜チェックは、既存標準のどれも自動化していない部分を実装している（推論）。ただし DPI が示すように、share-alike 同士の衝突（例: CC BY-SA と GPL）は互換性表という外部知識を必要とする。チェック規則の忠実性は、その表の正しさに依存する（推論）。

### Gaps
- Croissant の後続版（1.1 など）で派生や来歴のプロパティが追加されたかは未確認。
- DataCite の relationType による派生記述は未検証（Q1 Gaps を参照）。

## Q4: メタデータ品質の実証研究（欠落率・誤ラベル率）

### Takeaway
プラットフォーム上のライセンスメタデータは、欠落が約7割、誤り（特に実際より緩い表示）が16〜29%に上る（DPI, 2023）。2026年の研究では、許容的ライセンスを表示するデータセットの96.5%が、そのライセンスが要求するライセンス本文を同梱していなかった。ライセンスラベルが付いていることは、遵守の証拠にならない。

### Cited Findings
- DPI（Table 2）: 「Unspecified」の割合は GitHub 72%、Hugging Face 69%、Papers with Code 70%。DPI 自身のプロトコルでは 30% に下がった — [DPI 論文 PDF](https://arxiv.org/pdf/2310.16787)
- DPI の判定とアグリゲータのライセンスが一致したのは GitHub 43%、HF 35%、PwC 54%。実際より緩すぎるライセンスを示していたのは 29%、27%、16% だった。原因は、コントリビュータが GitHub のコードライセンスをデータのライセンスと取り違えることだと推定されている — [DPI 論文 PDF](https://arxiv.org/pdf/2310.16787)
- DPI の要旨: 再アノテーションした HF ライセンスの 66% が異なる用途カテゴリに属し、元の表示は多くの場合より許容的だった。DPI はプラットフォームに応じて 46〜65% のライセンスを再割り当てした — [DPI 論文 PDF](https://arxiv.org/pdf/2310.16787)
  - 注: 66%（カテゴリ不一致の全体）と 27%（緩すぎる方向の誤り）は別の指標である。混同しないこと。
- Yang ら（ICLR 2024, arXiv:2401.13822）: 2023-03-16 時点の HF データセットリポジトリ 24,065 件のうち、空でない dataset card を持つのは 7,433 件（30.9%）だった。ダウンロード上位100件では 86.0% が5つのテンプレート節をすべて記入していたのに対し、ダウンロード0件では 7.9% だった。ライセンスを含む「Additional Information」節の記入率は 0.58（Table S4）。ライセンス単独の統計は報告されていない — [arXiv html](https://arxiv.org/html/2401.13822v1); [ICLR 2024](https://iclr.cc/virtual/2024/poster/17463)
- Jewitt ら（2026-02）: データセットの 96.5%、モデルの 95.8% が必要なライセンス本文を欠いていた。ライセンス本文と著作権表示の両要件を満たしたのはデータセットの 2.3%、モデルの 3.2% だった — [arXiv:2602.08816](https://arxiv.org/abs/2602.08816)

### Inferences
- 自己申告のライセンスタグは、約3割弱の確率で実際より緩い方向に誤る（DPI）。したがって、ラベルを信頼して allowlist で判定する方式は、層2で系統的に偽陽性（許可すべきでないものを許可する）を生みうる（推論）。
- 「ライセンス本文や著作権表示を同梱・保存せよ」という Jewitt らの結論は、証拠保全要件（当時の条項の版を保存する）とも整合する（推論）。

### Gaps
- HF の `license` タグ単独の欠落率や誤り率について、2024年以降の大規模で最新の統計は今回見つからなかった。
- DPI の後続研究（Consent in Crisis 2024 など）の数値は未検証。
