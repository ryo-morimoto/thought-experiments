# 機械可読ライセンス／権利表現言語（REL）とポリシー評価器の限界

調査日: 2026-11-20。調査はツール呼び出し約15回に限った。ここでいう「確認済み」は、一次資料を取得して内容を確かめたもの。それ以外は「未検証」と明記した。

---

## Q1. 各ターゲットは何を表現でき、評価器は何を判定するか（形式意味論の状況と採用状況）

### Takeaway
ODRL 2.2 は W3C 勧告である。一方、その「評価のふるまい」（形式意味論）は 2026 年時点でも CG のドラフトにとどまり、未記述の節が残っている。学術的な評価器（SolidLab ODRL-Evaluator、Southampton の query ベース意味論）は存在する。ただし、いずれも「閉世界」「既定は禁止」など、仕様にない解釈上の選択を自分で補っている。ccREL と SPDX 式が表すのは、権利の「種類のラベル」や「ライセンスの組み合わせ方」までである。義務の中身の充足は表現しない。

### Cited Findings
**ODRL 2.2 / 形式意味論**
- ODRL Information Model 2.2 は W3C 勧告（2018 年 2 月）。DALICC 論文も「W3C recommendation from February 2018」と記している — [W3C ODRL IM](https://www.w3.org/TR/odrl-model/); [Panasiuk et al. ESWC 2018](https://penni.wu.ac.at/papers/ESWC%202018%20Modeling%20and%20Reasoning%20over%20Data%20Licenses.pdf)
- W3C ODRL CG の「formal semantics」文書は「ODRL Evaluator の期待されるふるまい」を定める。入力は policy、state of the world、evaluation request、behaviour パラメータの 4 つ（open/closed、既定は closed）。出力は Evaluation Report である — [ODRL Formal Semantics (draft)](https://w3c.github.io/odrl/formal-semantics/)
- 同文書は未完成である。PolicyReport の `result` が「pending to be written」で、ポリシー全体の判定結果が定義されていない。conflict（perm / prohibit / invalid）も概略だけで、remedy と consequence の意味論もない。「ODL VERSION TO BE DELETED」というブロックが残っている。状態や報告の語彙は「only illustrative」とされ、解釈は IM / Vocabulary に従属する。日付や正式な status 表記は確認できなかった — [ODRL Formal Semantics (draft)](https://w3c.github.io/odrl/formal-semantics/)
- 同文書は「policy monitoring（compliance checking / usage control）」シナリオを扱っている — [同上](https://w3c.github.io/odrl/formal-semantics)
- Salas, Pareti ほか（Southampton）"Evaluation and Comparison Semantics for ODRL"（arXiv 2509.05139、2025-09）。state of the world をイベント集合とし、違反をそのうえのクエリとして定義する一階の意味論である。ODRL Lite は prohibited-by-default かつ closed-world。ポリシー比較は query containment で定義し、実装は ODRL2SHACL（UPCAST プロジェクト）。決定可能性や計算量の結果は示されておらず、将来課題とされている — [arXiv 2509.05139](https://arxiv.org/html/2509.05139v1)
- 同論文は ODRL の仕様側の曖昧さを明言している。「as of August 2025, the formal semantics of ODRL is still in a draft state」で「in natural language」とあり、義務などの推論の扱いも「unclear」、推論規則については「no obvious interpretation of them can be extracted from the ODRL specification」と書く。比較手法の正しさの証明は ODRL Lite に限られる。Bonatti らとは義務の充足や consequence の扱いで解釈が異なる — [arXiv 2509.05139](https://arxiv.org/html/2509.05139v1)
- Slabbinck ほか（ESWC 2025）は Compliance Report Model、評価器向けテストケース、ODRL Evaluator（SolidLab、OSS）を提示した。リポジトリには「validation, cardinality, SOTW, policy decomposition」が未実装と書かれている（検索スニペット経由。リポジトリ本体は未取得）— [Verborgh 頁](https://ruben.verborgh.org/publications/slabbink_eswc_2025/); [ecosyste.ms 経由のリポジトリ情報](https://awesome.ecosyste.ms/projects/github.com%2Fsolidlabresearch%2Fodrl-evaluator)
- 実装の一覧は W3C ODRL Landscape にある（中身は未精査）— [ODRL Landscape](https://w3c.github.io/odrl/landscape/)
- 古い形式化として、ODRL を多ソート一階述語論理に翻訳した Pucella & Weissman がある — [A Formal Foundation for ODRL](https://arxiv.org/pdf/cs/0601085)

**ODRL によるライセンスのプロファイルとデータセット**
- 2005 年の ODRL Creative Commons Profile（ODRL 1.x 時代、W3C アーカイブ）は、CC License URI への参照を「informative」、ODRL 表現を「normative」と位置づけている（検索結果の要約による。本文は未精読）— [ODRL CC Profile](https://www.w3.org/2012/09/odrl/archive/odrl.net/Profiles/CC/SPEC-20050706.html)
- RDFLicense（Rodríguez-Doncel, Villata, Gómez-Pérez、2014）は 100 超のライセンスを主に ODRL 2.0 の RDF で表したもので、Open Data Commons、CC、ソフトウェアライセンスを含む。著者は「RDF licenses do not replace legal texts」としている — [core.ac.uk 論文](https://core.ac.uk/download/148675196.pdf); [W3C list 2014](https://lists.w3.org/Archives/Public/public-odrl-contrib/2014Sep/0000.html)
- 2017 年に Rodríguez-Doncel 自身が「RDF 版は複数の研究者による未検証の作業」と述べている — [W3C public-lod 2017](https://lists.w3.org/Archives/Public/public-lod/2017Jan/0047.html)
- licensius リポジトリには RDFLicense、ODRL evaluator、Java ライブラリがある — [GitHub oeg-upm/licensius](https://github.com/oeg-upm/licensius)

**ccREL**
- ccREL は W3C Member Submission（2008-05-01）で、「indicates no endorsement」とされる。ライセンス側の語彙は `cc:permits`（Reproduction / Distribution / DerivativeWorks）、`cc:prohibits`（CommercialUse）、`cc:requires`（Notice / Attribution / ShareAlike / SourceCode）、`cc:jurisdiction`、`cc:legalCode`。作品側は `cc:attributionName`、`cc:attributionURL` など — [W3C ccREL](https://www.w3.org/submissions/ccREL/)
- 「Attribution が required」という 1 ビットはあるが、帰属表示の方法（どの媒体で、どこに、何を書くか）を表す語彙は確認できなかった — 同上（推論を含む。後述）

**SPDX**
- SPDX ライセンス式は OR（選択）、AND（「simultaneously comply」）、WITH（例外）、`+`、`LicenseRef-`（リスト外の利用者定義ライセンス）を定義する。附属書の本文には、法的解釈、義務の内容、準拠判定についての記述がない — [SPDX 3.0.1 Annex: License Expressions](https://spdx.github.io/spdx-spec/v3.0.1/annexes/spdx-license-expressions/)

### Inferences
- ODRL で「準拠を形式的に証明する」には、少なくとも 3 つを自分で決めて固定する必要がある。評価意味論（open/closed、既定は許可か禁止か）、ポリシー全体の結果の定義、アクション階層の推論規則である。これらは標準で決まっていない。選び方によって結論が変わりうるので、「標準 ODRL に照らして証明済み」とは言えない。言えるのは「特定の意味論の下で」までである。
- SPDX 式と ccREL はどちらも「どの規範が適用されるか」の宣言層である。ユーザーのチェッカーの (1) 内部整合性、(3) の一部（許可リストへの照合や SA の系統）には使える。しかし義務の充足（帰属表示がなされたか）は表現の外にある。

### Gaps
- ODRL formal semantics ドラフトの正式な日付と status は、取得した頁から確認できなかった。
- SPDX License List に義務メタデータ（obligations）があるかどうかは未確認。調べた範囲では見当たらなかった。
- RDFLicense に ODbL が収録されているかは未確認。データセットの現在の稼働状況（rdflicense.appspot.com）も未確認。

---

## Q2. DALICC / OSADL / ODRL 評価器は実際に何を判定し、何ができないと明言しているか。CC BY 4.0 / ODbL の義務を形式化して忠実度を評価した研究はあるか

### Takeaway
DALICC が判定するのは、ODRL+ASP による「ライセンス間のルール衝突（互換性）」である。「この利用がこの義務を満たしたか」は判定しない。互換性の判定も、専門家が作った行為依存グラフに依存する。OSADL は義務を独自の制御言語（YOU MUST / YOU MUST NOT）で書いたチェックリストと互換性マトリクスを公開しているが、「法的助言ではない」「work in progress」と明言している。CC BY 4.0 や ODbL の義務の形式化について、法文に対する忠実度を体系的に評価した研究は見つからなかった。

### Cited Findings
**DALICC**
- ESWC 2018 の DALICC 論文は 14 ライセンス（CC BY 系 6 種、Apache、BSD-2/3、GPL-2/3、AGPL、LGPL、MIT）を ODRL で表現した。ODRL と ccREL だけでは概念が足りず、DALICC 語彙（`dalicc:modificationNotice`、`dalicc:worldwide`、`dalicc:perpetual` など）で補っている。ODbL は対象に含まれていない — [Panasiuk et al. ESWC 2018](https://penni.wu.ac.at/papers/ESWC%202018%20Modeling%20and%20Reasoning%20over%20Data%20Licenses.pdf)
- 互換性は clingo（ASP）で判定する。出力は `conflict(rule1, rule2)`（「l1 does not comply with l2」）で、行為間の includedIn / implies / sameAs / contradiction を「expert knowledge」として依存グラフに符号化している。拡張版は「all non conflicting sets of permissions, prohibitions, and duties」を返す — 同上
- 同論文の例では、Apache 2.0 の duty を `cc:Notice, cc:Attribution, dalicc:modificationNotice` という行為ラベルで表している。「どう帰属表示するか」の条件は持たない — 同上
- IRIS 2019 論文によると、当時の版の互換性チェックは「選択した許可・義務・禁止の束」に対して行うもので、2 つ以上のライセンス同士の直接比較ではなかった（検索結果の要約による）— [IRIS 2019 DALICC](https://penni.wu.ac.at/papers/IRIS%202019%20DALICC%20A%20License%20Management%20Framework%20for%20Digital%20Assets.pdf)
- dalicc.net は現在 api.dalicc.net/docs にリダイレクトされる（API の中身と免責表示は取得できず）— [dalicc.net](https://www.dalicc.net/)

**OSADL**
- OSADL Open Source License Obligations Checklists は、義務を「YOU MUST / YOU MUST NOT」と USE CASE / IF / ATTRIBUTE / NOT などで書き、引数には制御語彙を使う。プレーンテキスト版と JSON 版の両方を一次データとし、別に互換性マトリクスがある。「Non-copyleft licenses are implicitly assumed to be compatible between each other」— [OSADL Checklists](https://www.osadl.org/OSADL-Open-Source-License-Checklists.oss-compliance-lists.0.html)
- OSADL は免責を明記している。個別の法的助言ではないこと（ドイツでは法的助言は有資格者に限られる）、生データの利用者が国内法に沿って提供する責任を負うこと、「This project is a work in progress」であること、ローカル保存は「strongly discouraged」であること — 同上

**先行するライセンス推論研究**
- Governatori, Rotolo, Villata, Gandon "One License to Compose Them All"（ISWC 2013）は、deontic logic の意味論でライセンスを合成し、構成要素に準拠する合成ライセンスを生成する — [Springer](https://rd.springer.com/chapter/10.1007/978-3-642-41335-3_10); [arXiv 1212.0079（関連版と推定、未精読）](https://arxiv.org/pdf/1212.0079)
- ライセンスの互換性判定には deontic 演算子と規範衝突（例外を含む）の扱いが必要で、defeasible deontic logic がそれに適するという主張がある（EURECOM 掲載 PDF。著者は未確認）— [EURECOM PDF](https://eurecom.fr/publication/4376/download/mm-publi-4376.pdf)
- Gordon の Carneades による OSS ライセンス互換性（ICAIL 2011）は参照文献として挙がっていたが、本文は未取得 — 同上

**解釈を要する義務（参照用の一次法文）**
- CC BY 4.0 §3(a)(2):「You may satisfy the conditions in Section 3(a)(1) in any reasonable manner based on the medium, means, and context in which You Share the Licensed Material」— [CC BY 4.0 legalcode](https://creativecommons.org/licenses/by/4.0/legalcode.en)（本調査では再取得しておらず、文言は既知の条文として記載）
- ODbL 1.0 §4.3: Produced Work を公開するときは「a notice associated with the Produced Work reasonably calculated to make any Person ... aware」が必要 — [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/)（同じく本調査では再取得していない）

### Inferences
- 既存ツールの判定対象は「互換性（ルール集合同士の衝突の有無）」である。思考実験の (3) のうち「利用行為が義務を満たしたか」には届かない。DALICC の duty は `cc:Attribution` という原子ラベルなので、「reasonable manner」や「associated with」の充足は、モデルに入る前に人間が真と宣言する事実になる。つまり思考実験の (2) 事実整合性の側に押し出されている。
- 互換性の結論は、行為依存グラフ（expert knowledge）と OSADL の「非コピーレフト同士は互換と仮定」という明示的な仮定に依存している。忠実度は外部の専門家判断で担保されているだけで、形式的に検証されたものではない。
- 「過剰に厳しいルールで解釈義務を包む」戦略（例: 帰属表示は必ず NOTICE と各ディレクトリに全文で書く）は、上記ツールのどれも直接は支援しない。ただし OSADL の「YOU MUST」形式なら、自前の強化規則として書く足場にはなる。

### Gaps
- CC BY 4.0 や ODbL の形式化を法文と突き合わせて忠実度を評価した研究（専門家アノテーションとの一致率など）は見つからなかった。存在しない、とまでは断定できない。
- DALICC の現行 API の機能と免責文言は、リダイレクトのため取得できなかった。
- OSADL 互換性マトリクスの個別エントリ（ODbL や CC BY を含むか）は未確認。主対象は OSS ライセンスとみられるが、未検証。

---

## Q3. オプトアウト系プロトコル（TDMRep、robots.txt、IETF aipref）は法的・技術的に何を保証するか

### Takeaway
3 つとも「意思表示の伝達形式」であり、技術的な強制力はない。TDMRep は EU DSM 指令 4 条の「機械可読な権利留保」に応える手段として設計されたが、W3C 標準ではない（CG Final Report）。robots.txt（RFC 9309）は「access authorization ではない」と明記している。aipref vocab は 2026-09 の -08 でもコンセンサスに至っておらず、従うかどうかは受け手次第で、法的効果は仕様の範囲外としている。

### Cited Findings
- TDMRep は W3C TDMRep CG の Final Community Group Report（2024-05-10）で、「not a W3C Standard nor is it on the W3C Standards Track」とされる。`tdm-reservation`（1 = 留保、0 = 非留保）と `tdm-policy`（URL）を、tdmrep.json、HTTP ヘッダ、HTML meta、EPUB、PDF で配信する — [TDMRep CG-FINAL 2024-05-10](https://www.w3.org/community/reports/tdmrep/CG-FINAL-tdmrep-20240510/)
- TDMRep は DSM 指令 4 条への「technical answer」を自称し、4 条のオプトアウトは `tdm-reservation=1` で表すとする。EU 外では例外が適用されず、留保がないことを黙示の許諾とみなしてはならないとする。強制メカニズムの記述はない。research / non-research の目的制約は experimental — 同上
- robots.txt を定める RFC 9309（2022-09）:「These rules are not a form of access authorization.」— [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)
- IETF aipref: draft-ietf-aipref-vocab-08（2026-09-14、失効 2027-03-18）は「DO NOT REFLECT CONSENSUS of the Working Group」としている。カテゴリは `train-ai`、`ai-use`、`search` の 3 つ。受け手は「has a choice whether to follow those preferences」とされ、遵守の有無は「outside the scope」、「Preferences are not a security mechanism」と明記する。法律上の権利制限・例外には「without prejudice to applicable laws」とするだけで、相互作用は分析していない。契約が許諾していれば、選好表明があっても契約が優先すると書く — [draft-ietf-aipref-vocab-08](https://www.ietf.org/ietf-ftp/internet-drafts/draft-ietf-aipref-vocab-08.html)
- WG charter のマイルストーン（2026-08 に IESG へ送付）は過ぎている。検索結果からは IESG 送付も RFC 化も確認できなかった。添付方式の draft-ietf-aipref-attach も同じマイルストーンを持つ — [aipref WG](https://datatracker.ietf.org/wg/aipref/about/); [datatracker vocab](https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/)

### Inferences
- ユーザーのリポジトリ（他人のデータを「使う」側）にとって、これらのシグナルは「利用してはならない」という否定条件を事実として取り込む入力になる。準拠証明の根拠にはならない。仮に「留保なし」を確認しても、それは許諾ではない（TDMRep 自身が EU 外では黙示許諾とみなさないと述べている）。
- 技術的に保証されるのは「シグナルが、ある時刻に、ある形式で存在した」ことまでである。証拠保全（取得時刻つきのスナップショット）が必要になるという思考実験の指摘と整合する。

### Gaps
- 2026-11 時点で aipref vocab が IESG に送られたか、最新版が -08 より新しいかは未確認。
- ai.txt（Spawning などの民間提案）は調べていない。未検証。
- 各国の裁判例で TDMRep や robots.txt が「適切な方法による留保」と認められたかどうかは調査範囲外で、未検証。

---

## Q4（横断）. 解釈的基準や open texture は形式化できるか。法情報学の知見

### Takeaway
法情報学では、open texture（Hart と Waismann の概念）は「法の欠陥ではなく性質」とされることが多い。「唯一の正しい形式化は存在しないかもしれない」「意図的な曖昧さは符号化すべきでない」という立場が 2024〜2026 年の文献にも見られる。defeasible deontic logic は規範の衝突や例外は扱えるが、「reasonable」のような評価概念の充足判定そのものは与えない。

### Cited Findings
- Guitton ら（Maastricht、2024）は法文中の open-textured な語を測定する手法を提案し、アノテーター間の一致は substantial だったと報告した。規制が符号化に向くかどうかの判断に使えるとしている — [The challenge of open-texture in law](https://cris.maastrichtuniversity.nl/en/publications/the-challenge-of-open-texture-in-law)
- Baldini & De Benedetto（AI & Society 2024）は、open texture を、合理的な範囲に収まる限り法的言語の欠陥ではなく特徴だと論じる — [Springer s00146-024-01925-z](https://link.springer.com/10.1007/s00146-024-01925-z)
- arXiv 2606.23913 は、open texture のために唯一正しい形式化が存在しないかもしれない点を形式検証の課題として扱う（著者は、解釈主義が形式化を無益に見せるのは誤解だと反論している）— [arXiv 2606.23913](https://arxiv.org/pdf/2606.23913)
- arXiv 2608.13958 は、法の多くはコードに変換できない可能性があり、その一因は意図的な曖昧さだとする。形式化は実行可能であるべき部分に限るべきだと提案する — [arXiv 2608.13958](https://arxiv.org/pdf/2608.13958)
- Governatori & Rotolo の "Deontic Ambiguities in Legal Reasoning"（2023）は、defeasible deontic logic での曖昧性の遮断と伝播を扱う — [cris.unibo.it](https://cris.unibo.it/handle/11585/845524)
- 2026 年の Springer 論文（Law and Philosophy 系、s10982-026-09564-9）は、Hart、Dworkin、リアリズムに依拠して法を open system とし、計算的翻訳では司法の能力が失われると論じる。著者名と題名は未確認 — [Springer](https://link.springer.com/article/10.1007/s10982-026-09564-9)

### Inferences
- 中心問い「条件付きで形式的に証明できるほど忠実に義務を形式化できるか」への答えは次のとおり。義務の構造（何が許可・禁止・要求されるか、SA の伝播、ライセンス式の組み合わせ）は ODRL、ASP、deontic logic で十分に形式化できる。一方、「reasonable manner」「associated with」「reasonably calculated」の充足は、いずれの REL でも原子命題（宣言された事実）としてしか入らない。したがって証明は、形式部分の妥当性と、解釈部分を人間（またはより厳しい代替規則）が真と認定したことの連言になる。後者の忠実度は形式的には検証できず、法解釈の判断に委ねられる。
- 「過剰に厳しい規則で包む」戦略が健全なのは、厳しい規則の充足が元の解釈義務の充足を含意する場合だけである。その含意自体が解釈判断であり、検証済みの事例は見つからなかった。

### Gaps
- LegalRuleML（OASIS）の仕様状況とライセンスへの適用例は、今回の呼び出し回数の中で一次資料を取得できなかった。未検証。
- CC や ODC の法文に対して、形式化の妥当性を法律家が評価した実証研究は見つからなかった。
