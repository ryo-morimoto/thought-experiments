# ソフトウェア/リポジトリ向けライセンス準拠ツール・標準の保証範囲と限界

調査日: 2026-11-20。層の定義（依頼文より）: (1) 内部整合（リポジトリ⇔宣言）、(2) 事実整合（宣言⇔現実: 上流で本当にそのライセンスで公開されているか、ライセンサーに権利があるか）、(3) 法的評価。加えて「網羅性（未宣言コンテンツがないこと）」「忠実性（チェック規則が実際の義務を含意すること）」「証拠保全（当時の条項の版）」。
注: 調査は約16回のツール呼び出しで打ち切った。FOSSA・Snyk・FOSSology 本体のドキュメントは一次情報を取得できておらず、Gaps に記載した。

## Q1. 各ツール・標準は何を保証/検証し、どの層をカバーするか

### Takeaway
調べたツールと標準は、どれも主に層(1)、つまり宣言の存在・形式・リポジトリ内での一貫性を機械的に検査するものだった。層(2)（宣言が上流の実態と合っているか、ライセンサーが権利を持つか）を検証する仕組みは、どれにも見当たらなかった。層(3)の法的評価は、利用者が書くポリシー規則や人手のレビューに委ねられている。OpenChain（ISO/IEC 5230）は成果物ではなくプロセスの規格である。

### Cited Findings
**REUSE（FSFE）仕様 / `reuse lint`**
- 仕様 3.3（2024-11-14）。LICENSES/ 配下のファイル、VCS が無視するファイル、サブモジュール、REUSE.toml、シンボリックリンク、0バイトのファイルなどを除く全ファイルが Covered File になり、それぞれが「MUST have Licensing Information associated with it」とされる — [REUSE Spec 3.3](https://reuse.software/spec-3.3/)
- 画像のようにコメントを書けないファイルは、隣接する `.license` ファイル（例: `cat.jpg.license`）か REUSE.toml の `[[annotations]]` で情報を付ける。REUSE.toml はパスの glob と `precedence`（closest / aggregate / override）を持つ。DEP5 は非推奨で、REUSE.toml とは併用できない — [REUSE Spec 3.3](https://reuse.software/spec-3.3/)
- `SPDX-SnippetBegin` / `SPDX-SnippetEnd` でファイルの一部に別ライセンスを宣言できる。`REUSE-IgnoreStart/End` は「MUST NOT be used to ignore valid Licensing Information」とされている — [REUSE Spec 3.3](https://reuse.software/spec-3.3/)
- `reuse lint` の検査項目: SPDX 外で LicenseRef- でもない「Bad licenses」、非推奨ライセンス、拡張子のないライセンスファイル、参照されているのに LICENSES/ にない「Missing licenses」、どこからも参照されない「Unused licenses」、SPDX 式として不正なもの、著作権・ライセンス情報のないファイル — [reuse-lint man page](https://reuse.readthedocs.io/en/stable/man/reuse-lint.html)
- ドキュメントの範囲では、著作権者の正しさ、ライセンスが実際に合っているか、ライセンス本文が真正かといった検証は記述されていない。仕様も「表現方法」を定めるだけで、真実性には触れていない — [reuse-lint](https://reuse.readthedocs.io/en/stable/man/reuse-lint.html), [Spec 3.3](https://reuse.software/spec-3.3/)

**SPDX（仕様・ライセンスリスト・LicenseRef・式）**
- `LicenseRef-[idstring]` は SPDX License List にないライセンスを指す文書内一意の識別子。Extracted Text には「the actual text of the license reference」を入れる。例示から、短い参照文だけでも可とされている — [SPDX 2.3.1 §10](https://spdx.github.io/spdx-spec/v2.3.1/other-licensing-information-detected/)
- PackageLicenseDeclared は「パッケージ作者が述べたライセンス」。PackageLicenseConcluded は「SPDX 文書作成者が結論づけたライセンス」。両者が違う場合は License Comments に説明を書く（should）。NOASSERTION は、意図的に情報を出さない場合、判断を試みたが結論できなかった場合、判断を試みなかった場合に使う — [SPDX 2.3.1 §7](https://spdx.github.io/spdx-spec/v2.3.1/package-information/)
- PackageChecksum と PackageVerificationCode（各ファイルの SHA1 をソートして結合し、さらにハッシュしたもの）は「independently reproducible mechanism」で、内容の同一性を固定する。PackageDownloadLocation には取得元 URL や VCS の位置を書く — [SPDX 2.3.1 §7](https://spdx.github.io/spdx-spec/v2.3.1/package-information/)

**ScanCode Toolkit**
- ライセンス検出は近似マッチを許す。このため未知の検出（unknown）や複数の近似マッチが起き、結果が曖昧になる。scancode-analyzer は、不完全なカバレッジ、余分な語、誤検出タグ、unknown-match を問題種別として分類している — [scancode-results-analyzer](https://www.github.com/nexB/scancode-results-analyzer), [Issue types](https://scancode-analyzer.readthedocs.io/en/stable/how-analysis-is-performed/cases-incorrect-scans.html)
- 誤検出は「gpl/lgpl といった語だけを持つ一握りのルール」によるものがほとんど、とされている — [scancode-analyzer docs](https://scancode-analyzer.readthedocs.io/en/stable/how-analysis-is-performed/selecting-incorrect-unique.html)
- CHANGELOG によれば、6753 件の誤検出ルールが削除され、新しいフィルタに置き換えられた（ルールベースの精度が保守作業に依存していることの例）— [ScanCode CHANGELOG（検索結果経由）](https://redirect.github.com/aboutcode-org/scancode-toolkit/blob/HEAD/CHANGELOG.rst)

**ORT（OSS Review Toolkit）**
- Evaluator は Kotlin DSL の `evaluator.rules.kts` で書くポリシー規則。例として、未分類ライセンス（UNHANDLED_LICENSE）、宣言ライセンスが SPDX にマップできない場合の警告、COPYLEFT_IN_SOURCE などがある。ライセンスはそれぞれ concluded / declared / detected のどの由来かを持ち、`CONCLUDED_OR_DECLARED_AND_DETECTED` のようなビューで評価する — [ORT evaluator rules](https://oss-review-toolkit.org/ort/docs/configuration/evaluator-rules)
- サンプル規則は「only contains example」と明記され、法務チームへの相談を推奨している。ドキュメントには組み込みの互換性判定ロジックの記述がなかった — [ORT evaluator rules](https://oss-review-toolkit.org/ort/docs/configuration/evaluator-rules)

**licensee（GitHub）**
- ルートの LICENSE / COPYING 等と REUSE 形式の `LICENSES/` を読み、choosealicense.com の既知ライセンス本文と比べる。まず完全一致を試し、だめなら Sørensen–Dice 係数で類似度を出す — [licensee README](https://github.com/licensee/licensee)
- 意図的に見ないもの: 依存関係、（既定では）README、全ライセンス、全ファイル（「checking every single file for a copyright header」はしない）。コンプライアンスには複数のツールと人手のレビューが必要と明記している。単一ライセンスに決まらない場合は project license を返さない — [what-we-look-at.md](https://github.com/licensee/licensee/blob/main/docs/what-we-look-at.md)

**ClearlyDefined**
- ScanCode、FOSSology、Licensee などで自動収集（harvest）したデータを、コミュニティの「curation」で修正する。修正は通常の OSS と同じくレビューを経てマージされる — [OSI blog](https://opensource.org/blog/clearlydefined-at-soss-fusion-2024-a-collaborative-solution-to-open-source-license-compliance), [opensource.com](https://opensource.com/article/19/5/license-compliance-clearlydefined)
- Declared は「コンポーネントが全体ライセンスとして明示したもの」、Discovered は「ファイル内に見つかった他のライセンス」。NOASSERTION は「license-like data はあるが SPDX ライセンスを特定できない」状態。SPDX Matching Guidelines を満たさないものは OTHER とする。正規ソース同士が矛盾するときは作者に連絡し、7日間応答がなければ定められた優先順位に従う。キュレーターは作者の意図を推測しないこと — [Curation guidelines](https://docs.clearlydefined.io/docs/curation/curation-guidelines)
- ガイドラインには正確性や責任に関する免責の明示がなかった — [Curation guidelines](https://docs.clearlydefined.io/docs/curation/curation-guidelines)

**Black Duck**
- スニペットマッチング: ローカルで codeprint を生成して KB の Snippet Matching Service に送り、コード片の一致からコンポーネント・版・ライセンス名・ライセンス種別・一致位置を返す。codeprint の解析対象はファイル先頭の 1MB（新しい版の文書では 1〜4MB、既定 1MB）— [Black Duck docs: About snippet matching](https://testing.blackduck.synopsys.com/doc/ComponentDiscovery/Snippets.html), [2026.4.2 docs](https://verint.app.blackduck.com/2026_4_2/doc/static/en-us/help/ComponentDiscovery/Snippets.html), [Snippet API blog](https://www.blackduck.com/blog/analyze-ai-generated-code-black-duck-snippet-api.html)
- CodePrint 解析は、パッケージマネージャで宣言されていない依存も検出するとされている — [Black Duck SCA datasheet](https://origin-www.synopsys.com/content/dam/synopsys/sig-assets/datasheets/blackduck-sca-ds-ul.pdf)

**OpenChain ISO/IEC 5230 / 18974**
- 5230 は、ライセンスコンプライアンスのプロセスを置く場所、役割と責任、プロセスの持続性を定める。適合は自己認証、または公式パートナーによる独立評価・第三者認証で示す — [OpenChain license compliance](https://www.openchainproject.org/license-compliance)
- 18974 は 2023年12月に国際規格化された（旧 OpenChain Security Assurance Specification 1.1）。既知脆弱性（CVE 等）を確認するセキュリティ保証プログラムの要件で、5230 を下敷きにしている — [OpenChain security assurance](https://openchainproject.org/security-assurance), [ISO 18974](https://www.iso.org/standard/86450.html)

### Inferences
- 層の対応（推論）:
  - REUSE/`reuse lint` は層(1)と網羅性（全ファイルに宣言があること）を担う。網羅性は「宣言が付いているか」を見るだけで、REUSE.toml の glob で大量のファイルにまとめて宣言を付けると、中身が異質でも lint は通る。ユーザーの SOURCE.toml 方式と同じ構造的な弱点を持つ。
  - SPDX は表現形式。declared / concluded を分けていることと、チェックサムで内容を固定できることが、層(2)の主張とその証拠を記録する受け皿になる。ただし検証そのものは行わない。
  - ScanCode / FOSSology / Black Duck は本文マッチやスニペットマッチで「未宣言のライセンス文言・既知 OSS コード片」を見つける。網羅性に部分的に効くが、ライセンス文言を含まないデータ（CSV、画像）の出所は検出できない。
  - ORT は、検出結果・宣言・curation を突き合わせて規則を評価する基盤。忠実性は利用者が書く規則次第になる。
  - ClearlyDefined は層(2)に最も近い。ただし検証対象は上流パッケージの内容（その中に書かれた宣言）で、ライセンサーが権利を持っているかは見ない。
  - OpenChain は「プロセスがあること」の適合性で、個々の成果物の正しさは保証しない。
- 依頼にあった「上流で本当にそのライセンスか」をクロールして確かめる機能、ライセンス本文の当時の版を保存する機能を中核に持つツールは、確認できた範囲では存在しない。

### Gaps
- FOSSA、Snyk、FOSSology の公式ドキュメントは今回取得できていない。FOSSA は依存関係とファイル単位のスキャンを行い、Snyk のライセンス機能はパッケージマニフェストの依存関係に限られる、という一般的な理解はあるが未検証。
- ORT のパッケージ curation、ライセンス所見 curation、`concluded` 決定の詳細は別ページにあり、未取得。
- ScanCode が画像や CSV などデータファイルに対して何をするか（メタデータ/EXIF の読み取りなど）は未確認。
- REUSE 仕様には CSV への明示的な言及がない（コメントを書けないファイルとして `.license` を使う、というのは推論）。

## Q2. 検出精度・宣言の不一致に関する実証研究（数値）

### Takeaway
スキャナの精度は完璧からほど遠く、ScanCode の in-code 検出は F≒0.77 にとどまる。GitHub リポジトリの約半数で、トップレベルの宣言とコード内のライセンスが一致していない。データセットの領域では、ライセンス記載の欠落が70%超、誤りが50%超と報告されている。宣言を信頼するチェッカーは、こうした誤りをそのまま受け継ぐ。

### Cited Findings
- Wolter, Barcomb, Riehle, Harutyunyan「Open Source License Inconsistencies on GitHub」（ACM TOSEM, DOI 10.1145/3571852）。GitHub∩OpenHub から1,000リポジトリを抽出（2020年4月）。250リポジトリ・500ファイルを手作業で検証して正解データを作った — [PDF](https://dirkriehle.com/wp-content/uploads/2022/10/License_Inconsistencies_on_Github.pdf), [ACM](https://dl.acm.org/doi/10.1145/3571852)
  - 再現率/適合率/F値: 宣言ライセンス 0.8977/0.9753/0.9349、in-code Nomos（FOSSology のスキャナ）0.7688/0.8255/0.7961、in-code ScanCode 0.7875/0.7456/0.7660、両者の一致を要求するハイブリッド 0.7468/0.8613/0.8000。ScanCode は「より寛容に」ライセンスを付与するため誤検出が多く、版番号が書かれていない場合に特にそうなる — 同上
  - 宣言とコード内ライセンスの不一致は、最も保守的なハイブリッドでも「almost half」のリポジトリにある。宣言が寛容型なのにコピーレフトのコードを含むリポジトリが約10%。宣言箇所同士（API / LICENSE / README）の不一致は約5%で、不整合のあるリポジトリ1件あたり平均3.357件。結論として「existing tools cannot fully identify licences」— 同上
  - 事例: mimemagic（MIT と宣言）が GPL の shared-mime-info を取り込んでおり、マージツールが著作権表示を落としていた。Rails を経由して172パッケージに波及し、推定577,000リポジトリに影響した（2021年3月）— 同上
  - 先行研究の引用: Ninka は Debian 5.0.2 の0.8M ファイルで再現率82.3%、適合率96.6% — 同上
- LiDetector（Xu et al., ACM TOSEM, DOI 10.1145/3518994）。ライセンス条項の識別で適合率93.28%・再現率75.70%、権利・義務の推論で精度91.09%、非互換検出で偽陽性率10.06%・偽陰性率2.56%。1,846プロジェクトの72.91%に非互換があった — [arXiv 2204.10502](https://arxiv.org/abs/2204.10502v1), [GitHub](https://github.com/XuSihan/LiDetector)（依頼にあった ICSE 2023 の版は確認できなかった。TOSEM 掲載）
- Data Provenance Initiative（Longpre et al., Nature Machine Intelligence, DOI 10.1038/s42256-024-00878-8）。1,800超のテキストデータセットを監査し、集約プラットフォーム上のライセンス欠落が70%超（版により68%〜72%超と表記が揺れる）、誤りが50%超。再アノテーションの結果、Hugging Face のライセンスの66%が別の利用カテゴリに属し、作者の意図より寛容に表示されていることが多かった — [arXiv 2310.16787](https://arxiv.org/abs/2310.16787), [MIT Media Lab](https://www.media.mit.edu/publications/a-large-scale-audit-of-dataset-licensing-and-attribution-in-ai/)

### Inferences
- 層(2)について: 集約サイト（Hugging Face など）のライセンス表示を SOURCE.toml に転記した場合、その表示自体が5割超の確率で誤っている母集団から来ている可能性がある。一次の公開元（作者のページ）の条項を確かめる必要がある。
- 網羅性について: 最良のスキャナでも再現率は約0.79で、in-code ライセンスのおよそ2割を見逃す。スキャナを通過したことは「未宣言のものがない」ことの証明にならない。
- 忠実性について: 非互換検出の研究ツールにも10%前後の偽陽性があり、ライセンス条項を形式化すること自体が誤差を伴う。

### Gaps
- ScanCode と FOSSology をデータファイル（CSV や画像のライセンス）で評価した研究は見つからなかった。
- 最新版 ScanCode（v32 以降の license detection 刷新後）の精度を独立に評価した研究は見つからなかった。Wolter らのデータは2020年のもの。
- licensee、Black Duck、FOSSA、Snyk の精度を独立に評価した公開研究は見つからなかった。

## Q3. 義務の符号化（忠実性）と証拠保全

### Takeaway
互換性や義務の判断は、利用者が定義する分類と規則（ORT）か、研究段階のツール（LiDetector）に頼ることになる。標準化された「正しい」互換性エンジンは確認できなかった。証拠保全は、SPDX のチェックサムとライセンス本文の同梱、REUSE の LICENSES/ ディレクトリで部分的に実現できる。ただしどちらも「どの時点で、どの URL で、その条項が公開されていたか」というタイムスタンプ付きの証拠は持たない。

### Cited Findings
- ORT の例では、license-classifications ファイルでライセンスを permissive / copyleft / copyleft-limited / public-domain 等に分類し、規則はその分類に対して書く。1つのライセンスが複数カテゴリに入るとエラーになる — [ORT evaluator rules](https://oss-review-toolkit.org/ort/docs/configuration/evaluator-rules)
- REUSE は LICENSES/ にライセンス本文を置くことを求め、lint は「宣言があるのに本文がない」「本文があるのに使われていない」を検出する — [reuse-lint](https://reuse.readthedocs.io/en/stable/man/reuse-lint.html)
- SPDX の Extracted Text は SPDX リストにないライセンスの本文コピーを保持でき、PackageChecksum / VerificationCode は内容を再現可能な形で固定する。PackageDownloadLocation は取得元を記録する — [SPDX 2.3.1 §7](https://spdx.github.io/spdx-spec/v2.3.1/package-information/), [§10](https://spdx.github.io/spdx-spec/v2.3.1/other-licensing-information-detected/)
- ClearlyDefined のガイドラインは、著作権表示を「it is abundantly clear」なスキャナ誤りの場合を除いて改変しないこと、作者の意図を推測しないことを求めている。つまり人手のキュレーションでも、解釈せずに記録することに留めている — [Curation guidelines](https://docs.clearlydefined.io/docs/curation/curation-guidelines)

### Inferences
- ユーザーのチェッカーにある、許可リストと share-alike の系譜チェックは、ORT の分類と規則のモデルとほぼ同じ構造をしている（推論）。業界ツールでも、忠実性（規則が実際の義務を含意すること）はツールの外にある法務判断に委ねられている。「過度に厳しい規則で解釈的な義務を包み込む」という戦略は、ORT の COPYLEFT_IN_SOURCE をエラーにする例に近い。
- 証拠保全で業界標準が持たない要素（推論）: 取得日時、上流の条項ページのスナップショット（例: Web アーカイブ）、そのハッシュ。SPDX の Created タイムスタンプとチェックサムを使えば成果物の側は固定できるが、上流の条項ページの版は固定できない。

### Gaps
- OSADL ライセンス互換性マトリクスなど、公開されている互換性エンジンは今回調べていない。
- SPDX 3.0 で証拠や出所（provenance）の表現が変わったかは確認していない。
- データ向けのライセンス（CC 系、ODbL など）で、attribution / share-alike の義務を自動判定するツールの存在は未確認。
