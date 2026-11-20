# 確からしさのラベルと、主張・根拠・来歴の表現の標準（te への採用候補）

前提：te の現行設計は、結論の前提に `definitional` / `argued` / `empirical-checked` / `empirical-unverified` / `value` のラベルを付け、`sources.toml`（URL、sha256、ページ、引用文、一次/二次）と `outputs/` に結び、出来事に `by`（`claude` / `user` / `reviewer:<lens>`）を記録する。不変条件 `checked-needs-primary` は、確認済みの前提に sha256 付きの一次資料を求める（設計文書 `plugins/thought-experiments/docs/te-design.md` §3.2・§3.3、ローカルで読んだ）。

調査日: 2026-11-21。「未確認」は一次資料で確かめられなかった項目。

一次資料による確認（2026-11-21）: GRADE、IPCC、NUSAP、Micropublications、ORKG の項目を、発行元の公式文書か著者の出版物で照合し、URL・sha256・ページを書いた（確認作業のファイルはコミットしていない）。ミラーや Wikipedia の出典は差し替えた。

## GRADE と GRADE-CERQual（根拠の確実性の段階と、下げる・上げる観点）

### Takeaway
GRADE は「推定値が真の効果に近いとどれだけ確信できるか」を4段階で表し、研究デザインで出発点を決めて5つの観点で下げ、3つの観点で上げる。te に必要なのは段階名そのものより「出発点＋下げた理由を観点ごとに記録する」型で、`empirical-checked` を細かくしたいときにだけ使える。

### Cited Findings
- 4段階：high（真の効果は推定値の近くにあると非常に確信できる。"We are very confident that the true effect lies close to that of the estimate of the effect."）、moderate、low、very low。Handbook ではこれを "quality of evidence" と呼ぶ（GRADE Book 以降は certainty） — [GRADE Handbook Table 5.1](https://gdt.gradepro.org/app/handbook/handbook.html)（GRADE Working Group 編の公式 Handbook。取得時の HTML の sha256 `2fb19241ae0c365ef62e7bac16978d48cb6ad75e1b4465fb915912aaa919a606`。以下この節の Handbook は同じ）
- 出発点：重大な限界のない無作為化試験は high から、特段の強みも限界もない観察研究は low から始める。症例集積・症例報告は通常 very low に下げる — [GRADE Handbook §5.1](https://gdt.gradepro.org/app/handbook/handbook.html)
- 下げる観点（各1〜2段階）：risk of bias、inconsistency、indirectness、imprecision、publication bias — [GRADE Handbook Table 5.2](https://gdt.gradepro.org/app/handbook/handbook.html)
- 上げる観点：効果の大きさ（1〜2段階）、用量反応（1段階）、残余交絡の向き（1段階） — [GRADE Handbook Table 5.3](https://gdt.gradepro.org/app/handbook/handbook.html)
- 普及：「20か国以上の120を超える組織が GRADE を支持または使用」。ロゴに WHO、Cochrane を含む — [GRADE Working Group](https://www.gradeworkinggroup.org/)
- 利用条件：Handbook の転載・翻訳は編者の許可が必要（"Permission to reproduce or translate the GRADE handbook ... should be sought from the editors."）。Handbook にオープンライセンスの表示はない。Handbook は GRADE Book（book.gradepro.org、2024年から公開）に置き換えられつつある — [GRADE Handbook](https://gdt.gradepro.org/app/handbook/handbook.html)
- GRADE-CERQual（質的研究の統合向け）：観点は methodological limitations、coherence、adequacy of data、relevance の4つ。段階は high / moderate / low / very low。所見ごとに個別に評価する — [Lewin et al. 2018, paper 3 (PMC5791044)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5791044/)
- CERQual の relevance は「支える一次研究のデータが、問いで指定した文脈にどれだけ当てはまるか」 — [PMC5791044](https://pmc.ncbi.nlm.nih.gov/articles/PMC5791044/)

### Inferences
- GRADE の単位は「介入の効果推定」で、te の前提（政策の数値、制度の事実、定義など）とは対象が違う。段階名をそのまま `empirical-*` に替えると、意味が合わない。
- 取り込む価値があるのは観点の語彙。特に indirectness（GRADE）と relevance（CERQual）は、te の失敗「孫引き」「別の文脈の数値を流用」と同じ種類の問題を名指ししている。前提に `concerns = ["indirectness", ...]` のような任意の欄を足せば、`empirical-checked` でも「一次資料だが文脈がずれる」を記録できる。
- 単独利用者のファイル型ツールでは、4段階の採点手順（複数人で議論して決める）は重い。観点のリストだけ借りるのが釣り合う。

### Gaps
- GRADE Handbook にはオープンライセンスの表示がない（転載は許可制）。GRADE Book 側のライセンスは未確認。
- CERQual の coherence・adequacy の詳細基準は今回読んでいない。

## IPCC の較正された不確実性の言葉（Mastrandrea et al. 2010）

### Takeaway
IPCC AR5 のガイダンスは「確信度（confidence：根拠の量・質 × 合意の度合い、定性的）」と「尤度（likelihood：確率の言葉、定量的）」を別の尺度に分け、確信度を確率として読むなと明記する。te のラベルは「根拠の種類」で、どちらの尺度とも別軸なので、置き換えるより「根拠×合意」の2軸を足すかどうかが論点。

### Cited Findings
- 文書：Mastrandrea, Field, Stocker ほか, 2010, "Guidance Note for Lead Authors of the IPCC Fifth Assessment Report on Consistent Treatment of Uncertainties"。2010年7月の作業部会横断会合の成果で、IPCC 第32回総会が実施を促した（p.1: "At its 32nd session, the IPCC Panel urged the implementation of this Guidance Note."） — [IPCC 公式 PDF](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)、sha256 `d5754b11d70c36aed86188bae3427dd1890b1bef0487c8ebcd1682fd7e84a9c2`（6ページ）。前の版で使った Berkeley のミラーは7ページの別ファイルでバイト一致しないため、出典から外した
- 2つの指標：確信度は「根拠の種類・量・質・一貫性と合意の度合いに基づく、所見の妥当性への確信。定性的に表す」。もう一つは確率で表す定量的な不確実性 — [同上](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)
- 根拠の要約語は limited / medium / robust、合意は low / medium / high。「独立した高品質の根拠が複数あって一貫するとき、根拠は最も robust」。評価の「追跡できる説明（traceable account）」を本文に書く — [同上 §8](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)
- 合意も根拠も高ければ確信度か定量値を示す。片方だけなら可能なら示す。両方低ければ要約語（例 "robust evidence, medium agreement"）だけを付ける。他の所見に条件づけられた所見は、別に評価して報告する — [同上 §8](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)
- 確信度は very low / low / medium / high / very high の5段階。根拠×合意から確信度への対応には幅がある。「確信度は確率として解釈してはならず、統計的信頼度とも別」 — [同上 §9, p.4](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)
- 尤度（Table 1）：virtually certain 99–100%、very likely 90–100%、likely 66–100%、about as likely as not 33–66%、unlikely 0–33%、very unlikely 0–10%、exceptionally unlikely 0–1%。AR4 の extremely likely 95–100%、more likely than not >50–100%、extremely unlikely 0–5% も使える — [同上 Table 1](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)
- 「about as likely as not を知識の欠如の表現に使ってはならない」。十分な情報があれば言葉より確率分布や範囲を示すほうがよい — [同上 §10, p.4](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)
- 変数があいまい、または過程がよく分かっていない場合は確信度を付けず、根拠と合意の要約語だけを付ける — [同上 §11 A, p.4](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf)
- この枠組みは AR5 の3作業部会に共通の方式として作られた（p.675: "A goal for the Fifth Assessment Report, which is currently under development, is the application of a common framework with associated calibrated uncertainty language ..."） — Mastrandrea, Mach, Plattner, Edenhofer, Stocker, Field, Ebi, Matschoss (2011) Climatic Change 108:675–691（doi:10.1007/s10584-011-0178-6）。TIB のリポジトリにある出版社版 [PDF](https://oa.tib.eu/renate/bitstreams/a1f84060-8578-4aff-b467-d2ff6fe3c006/download)、sha256 `eb214b1485fa9c7875c009a836d0c872506bd893b4f5bf31c4def43bb8c9414d`。前の版は第一著者を Mach とし、SR1.5 でも使われたと書いていたが、第一著者は Mastrandrea で、2011年の論文は SR1.5（2018）での使用を支えられない。SR1.5 での使用は SR1.5 本体で確かめるまで書かない

### Inferences
- 「確信度と確率を混ぜない」「知らないことを 50% と書かない」「条件づけられた所見は条件側と分けて評価する」の3点は、te の `prediction.confidence` と結論の前提に直接効く。`confidence` を数値にするなら尤度の言葉、根拠の質を言うなら別の欄、と分けるのがよい。
- 「traceable account」は te の `sources` と `note` がすでに担っている。IPCC の語を借りるなら、`argued` / `empirical-*` の前提に `agreement`（low / medium / high：出典どうしが一致しているか）を任意で足すのが最小の追加。
- IPCC の作成物はガイダンス文書で、ライセンスの付いた語彙ではない。語を引用して使う分には問題が小さいと考えるが、利用条件は未確認。

### Gaps
- AR6 で尺度に変更があったかは確認していない（未確認。AR6 も同じ2指標を使ったと記憶しているが、一次資料で確かめていない）。
- IPCC 文書の利用条件は未確認。

## ICD 203（米国情報機関の分析基準、推定確率の言葉）と NUSAP

### Takeaway
ICD 203 は、尤度（事象について）と確信度（判断の土台について）を同じ文で混ぜることを禁じ、さらに「情報」と「仮定・判断」を区別して書くことを求める。後者は te の `empirical-*` と `argued` / `value` の区別とほぼ同じ発想で、te のラベル体系の外部の裏づけになる。NUSAP は数値1つに「幅・評価・来歴（pedigree）」を付ける記法で、`outputs/` の数値の記述に向く。

### Cited Findings
- ICD 203 は2015年1月2日署名、その後技術的改正（2022年8月の覚書に基づく Analytic Ombuds の改正を含む） — [ICD 203 PDF（archive.dni.gov）](https://archive.dni.gov/files/documents/ICD/ICD-203.pdf)
- 5つの分析基準（客観的、政治的考慮から独立、適時、入手できるすべての情報に基づく、分析技法基準を実施）と9つの分析技法基準 — [ICD 203](https://archive.dni.gov/files/documents/ICD/ICD-203.pdf)
- 技法基準(1)：情報源と方法の質・信頼性を記述する。正確さ、欺瞞の可能性、情報の古さ、アクセス、動機、偏りなどを挙げ、ICD 206 の情報源記述子を使う — [ICD 203](https://archive.dni.gov/files/documents/ICD/ICD-203.pdf)
- 技法基準(2)：尤度は2組の言葉のどちらかを使う。almost no chance / remote 01–05%、very unlikely / highly improbable 05–20%、unlikely / improbable 20–45%、roughly even chance / roughly even odds 45–55%、likely / probable 55–80%、very likely / highly probable 80–95%、almost certain / nearly certain 95–99%。組を混ぜるなら注記が必要 — [ICD 203](https://archive.dni.gov/files/documents/ICD/ICD-203.pdf)
- 「確信度（例 high confidence）と尤度を同じ文で組み合わせてはならない」。確信度は論理と根拠（情報源の量と質、主題の理解）に基づく — [ICD 203](https://archive.dni.gov/files/documents/ICD/ICD-203.pdf)
- 技法基準(3)：基礎となる情報を伝える文と、仮定・判断を伝える文を明確に区別する。仮定は「議論の枠組みを作る、または支える想定」、判断は「情報・分析・仮定に基づく結論」。論の要（linchpin）になる仮定は明示し、仮定が誤っていたときの影響を説明する — [ICD 203](https://archive.dni.gov/files/documents/ICD/ICD-203.pdf)
- 技法基準(4)：代替仮説を体系的に評価し、それぞれの尤度を変える兆候を示す。(7)：以前の判断からの変更・一貫性を説明する — [ICD 203](https://archive.dni.gov/files/documents/ICD/ICD-203.pdf)
- ICD 203 は米国政府の文書（著作権の扱いは未確認だが、米国連邦政府の著作物は一般に著作権の対象外とされる。本件文書での明示は確認していない）
- NUSAP：Funtowicz と Ravetz（1990）が提案した記法（"NUSAP is a notational system proposed by Funtowicz and Ravetz (1990)"）。Numeral、Unit、Spread、Assessment（情報についての定性的な判断。例 "optimistic" "pessimistic"）、Pedigree（情報の生産過程の評価。基準ごとに 0（弱）〜4（強）の pedigree matrix で採点） — van der Sluijs, Janssen, Petersen, Kloprogge, Risbey, Tuinstra, Ravetz (2004) "RIVM/MNP Guidance for Uncertainty Assessment and Communication: Tool Catalogue for Uncertainty Assessment"（Report NWS-E-2004-37）p.21、PBL 公式サイトの [PDF](https://pbl.nl/downloads/rivm-mnp-2004-guidance-uncertainty-toolcataloguepdf)、sha256 `6a4898bdcd7271f5463c0ffdd4fc1fe479cb543a23824cce3135f1682af1071f`
- NUSAP は RIVM/MNP（現 PBL、オランダ環境評価庁）の不確実性評価ガイダンスの道具集に手法として収録されている — 同上

### Inferences
- ICD 203 の(3)（情報と仮定・判断の区別、要の仮定の明示、誤っていたときの影響）は、te の結論の `premises` に「この前提が崩れたら結論はどう変わるか」の欄を足す根拠になる。段階C の攻撃の観点としても使える。
- (4) 代替仮説と兆候、(7) 判断の変更の説明は、te の `rival` と `correction` がすでに担っている。te の設計が情報分析の標準と同じ方向にあることの確認になる。
- 確率の言葉は IPCC と ICD 203 で境界が違う（likely は IPCC 66–100%、ICD 55–80%）。te が言葉で確率を書くなら、どちらの表を使うかを `rules.toml` で固定するか、数値で書かせるほうが安全。
- NUSAP の Pedigree は te の `sources.level`（一次/二次）を多軸にしたもの。`outputs/` の数値に `spread` と `assumptions` を付ける程度なら軽いが、pedigree matrix の採点は単独利用者には重い。

### Gaps
- NUSAP の原典（Funtowicz & Ravetz 1990 の書籍）は公開の全文がなく読んでいない。上の記述は RIVM/MNP の公式ガイダンス（Ravetz が共著者）による。
- ICD 206（情報源記述の要件）は読んでいない。

## 主張・根拠・来歴の語彙：CiTO、Micropublications、nanopublications、PROV-O、ORKG、schema.org Claim/ClaimReview

### Takeaway
te のファイルに最も素直に写せるのは、PROV-O の最小部分（Entity / Activity / Agent と wasDerivedFrom・wasAttributedTo・hadPrimarySource・wasQuotedFrom・wasRevisionOf）と、CiTO の「引用の性格」の語（supports / disputes / usesDataFrom / citesAsEvidence など）。RDF のまま採る必要はなく、欄の名前と値の語彙として借りれば十分。Micropublications は te の「結論・前提・根拠・反論」の形に最も近い先行モデルだが、OWL 前提で重い。nanopublications と ORKG は公開・共有のための仕組みで、単独利用者のファイル型ツールには過剰。

### Cited Findings
- **PROV-O**：W3C 勧告、2013年4月30日。PROV-DM の OWL2 表現 — [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- PROV-O の出発点の語：Entity、Activity、Agent、wasGeneratedBy、used、wasDerivedFrom、wasAttributedTo、wasAssociatedWith、actedOnBehalfOf、startedAtTime など — [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- 派生の特殊形：Revision（wasRevisionOf）、Quotation（wasQuotedFrom、元の一部または全部を繰り返して作った実体）、PrimarySource（hadPrimarySource、主題について直接の経験を持つ agent が作った先行の実体） — [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- Agent の下位クラス：Person、SoftwareAgent（「動いているソフトウェア」）、Organization — [W3C PROV-O](https://www.w3.org/TR/prov-o/)（Organization はページの後半にあり、今回の取得範囲では未確認）
- PROV-O の文書は W3C の著作権表示と文書利用規則に従う（オープンソースのライセンス名は書かれていない） — [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- **CiTO**：SPAR オントロジーの一つ。版 2.9.2、2026-11-12 更新、CC BY 4.0 — [CiTO](https://sparontologies.github.io/cito/current/cito.html)
- CiTO の根拠に関する語：支持側 supports、obtainsSupportFrom、confirms、agreesWith。反対側 disputes、disagreesWith、refutes、critiques、corrects。根拠・データ citesAsEvidence、citesAsAuthority、citesAsDataSource、usesDataFrom。方法・結論 usesMethodIn、usesConclusionsFrom。限定・拡張 qualifies、extends。それぞれ逆向きの語がある — [CiTO](https://sparontologies.github.io/cito/current/cito.html)
- CiTO は cito:Citation で引用そのものを対象にでき、hasCitingEntity、hasCitedEntity、hasCitationCharacterization を持つ — [CiTO](https://sparontologies.github.io/cito/current/cito.html)
- **Micropublications**：Clark, Ciccarese, Goble, *J Biomed Semantics* 5:28 (2014)。論文の主要な議論と根拠を表し、本文に注釈を重ねるための Web 向けモデル。OWL 2 と SWRL で実装、語彙は purl.org/mp — [arXiv:1305.3506](https://arxiv.org/abs/1305.3506)、[DOI](https://dx.doi.org/10.1186/2041-1480-5-28)。出版社版は Europe PMC が配信する [PDF](https://europepmc.org/articles/PMC4530550?pdf=render)（CC BY 2.0）、sha256 `f2d42a6509272218487b851bc5b26652985ece72e29f8c32da39e84ccc81a636`。以下のページはこの PDF
- 扱う対象：自然言語の文、データ、方法・材料、議論と論評、反論と不一致。他の文献の文を引用でき、主張の「支持・類似・反論」を表せる。arXiv 版は CC BY 3.0 — [arXiv:1305.3506](https://arxiv.org/abs/1305.3506)
- 最小形は「文＋帰属（attribution）」、最大形は「文＋支える議論全体（根拠、解釈、議論、反論）」（p.1: "The minimal form of a micropublication is a statement with its attribution. The maximal form is a statement with its complete supporting argument ..."）
- 既存モデルとの差として、nanopublications は文だけ、SWAN は同じ論文内の支持だけ、BEL と SWAN は他論文を論文単位でしか引けない、と著者が挙げる（p.3）
- 主なクラスは Claim（Micropublication が主張する単一の主たる Statement）・Statement・Data・Method・Material・Attribution・Representation。関係は supports（推移的）と challenges。challenges には、支えている要素を攻撃する indirectlyChallenges（undercut）も含む（p.10: "The challenges property is inferred when a Representation either directlyChallenges another, or indirectlyChallenges it by undercutting (directlyChallenges) a Representation which supports it."）
- **nanopublications**：assertion、provenance、publication info の3つの RDF グラフと、それらを結ぶ head グラフ。provenance は assertion のグラフ識別子に必ず結びつく。publication info には帰属と時刻を入れるべき。例では prov:wasDerivedFrom、prov:wasAttributedTo を使う。改変検出に trusty URI を推奨 — [nanopub.net guidelines](https://nanopub.net/guidelines/working_draft/)
- nanopublication ガイドラインは版・日付・正式な位置づけを明記していない（working draft の URL） — [nanopub.net guidelines](https://nanopub.net/guidelines/working_draft/)
- **ORKG**：論文を構造化して記述する計画。TIB、ハノーファー大学、L3S、InfAI のロゴと EU Horizon 2020 の資金表示 — [ORKG about](https://www.orkg.org/about)
- ORKG は RDF の上に作られ、論文の contribution を方法・材料・実装・結果の構造化した属性で記述する。template は内容の型の構造（属性と値）を定める — [CoRDI 2023](https://www.tib-op.org/ojs/index.php/CoRDI/article/download/272/519)、[Jaradeh et al. arXiv:2006.01747](https://arxiv.org/pdf/2006.01747)（検索結果の要約から）
- ORKG の公開データは CC0 1.0 Universal。ただし Papers With Code 由来のデータは元の CC BY-SA のまま再公開している（"The published data is licensed under CC0 1.0 Universal except data sourced from the following third-party sources ... Data sourced from Papers With Code licensed CC BY-SA"）。コードは MIT。Terms of use §4.1 も CC0 での再利用を認める。License ページには CC BY-SA 4.0 のバッジ画像が残っているが、本文は CC0 — ORKG 公式の [License](https://orkg.org/page/license)（2023-11-06 更新。ページはクライアント描画のため、同サイトの CMS API が返す本文を保存。sha256 `7b9216a45437cb777d47eac84be351b623e1556b7ee9886b7c5ca6f9d4bf5b04`）、[Terms of use](https://orkg.org/page/terms-of-use)（sha256 `ab056a1e603c6fa5773781cbb4fe08a0aa2b9140e08a3bf8668809b4259a8d68`）。前の版の「CC BY-SA と CC BY 3.0 DE で食い違う」は、論文と動画の記述によるもので、公式の現行表示ではない
- **schema.org Claim**：CreativeWork の下位型。「具体的で事実指向の主張」で、ClaimReview の itemReviewed になりうる。appearance、firstAppearance、claimInterpreter を持つ。schema.org V30.1（2026-09-16） — [schema.org/Claim](https://schema.org/Claim)
- **ClaimReview**：「作品の中でなされた主張のファクトチェック」。claimReviewed（主張の短い要約）、itemReviewed、reviewRating、author、datePublished。例では reviewRating.alternateName に "True" のような判定を入れる — [schema.org/ClaimReview](https://schema.org/ClaimReview)
- ClaimReview のページは Google のファクトチェック表示での利用に触れていない — [schema.org/ClaimReview](https://schema.org/ClaimReview)（Google 側の文書は未確認）

### Inferences
- te の出来事の `by` は PROV の Agent、`te add` の1回は Activity、`sources.toml` の1件と `outputs/` の1ファイルは Entity にそのまま対応する。`by = "claude"` は SoftwareAgent、`user` は Person、`reviewer:<lens>` は「SoftwareAgent が user の依頼で（actedOnBehalfOf）動いた」と書ける。対応表を文書に置くだけで、te を変えずに外部へ写せる。
- `sources.toml` の `primary/secondary` は PROV の hadPrimarySource、`quote` は wasQuotedFrom、`correction` 出来事は wasRevisionOf に当たる。二次資料に `primary_of = "<一次資料の id>"`（= hadPrimarySource）の欄を足すと、「孫引きを見つけたが一次をまだ取っていない」状態を記録でき、不変条件 `checked-needs-primary` の違反メッセージで一次資料の候補を示せる。
- CiTO の語は、前提→出典の結びつきに「どう使ったか」を付けるのに使える。たとえば `sources = [{id="s3", role="usesDataFrom"}, {id="s7", role="disputes"}]`。特に `disputes` / `refutes` を持てると、反対の証拠を探した記録（`holder` の反対側、段階C の攻撃）を前提ごとに残せる。語の数は多いので、te では5〜6語（citesAsEvidence、usesDataFrom、usesMethodIn、supports、disputes、qualifies）に絞るのが釣り合う。
- Micropublications の「支持と反論のグラフ」は te の `conclusion.premises` と `attack.objections` の組と同じ形。indirectlyChallenges（支える要素への攻撃）は ASPIC+ の undercut に当たり、te に欠けている `objections.target = inference` と同じ区別を持つ。te が独自に作った形が先行研究と一致していることの確認として引用できるが、OWL・SWRL での実装を取り込む利点は小さい。
- nanopublications の3部構成（主張 / 主張の来歴 / 記録そのものの来歴）は、te の「結論（主張）」「前提と出典（主張の来歴）」「events の by と at（記録の来歴）」の分け方と一致する。trusty URI（内容から作る識別子）は te の sha256 と同じ考え。ただし公開・署名・分散サーバーの仕組みは単独利用者には不要。
- ORKG は論文の比較を共有する Web サービスで、ファイル型の te とは目的が違う。template の考え方（型ごとに欄を決める）は te の JSON Schema が既に担う。
- schema.org の Claim / ClaimReview は Web 公開向けの構造化データで、判定（True / False など）は te のラベル（根拠の種類）とは別物。te の README を Web に出すときの出力形式としてなら使えるが、内部の記録には向かない。

### Gaps
- Micropublications の `mp:` 接頭辞つきの語彙（Additional file 1 の OWL）は読んでいない。クラス名と関係名は本文 p.10 で確認した。
- PROV-O の後半（Organization、Influence の限定形）は読んでいない。

## 単独利用者・ファイル型の te にどれが合うか（まとめ）

### Takeaway
採るべきは「語彙を借りて欄の値にする」ことで、RDF やオントロジーを導入することではない。優先度の高い順に、(1) ICD 203 / IPCC の「確信度と確率を混ぜない」「情報と仮定・判断を分ける」規則、(2) PROV の最小の対応（by=Agent、出来事=Activity、資料・出力=Entity、hadPrimarySource）、(3) CiTO から絞った「出典の使い方」の語、(4) GRADE / CERQual の下げる観点（indirectness / relevance）。GRADE の4段階、NUSAP の pedigree matrix、Micropublications の OWL、nanopublications、ORKG は過剰。

### Cited Findings
- te の5ラベル（definitional / argued / empirical-checked / empirical-unverified / value）は「根拠の種類と確認状態」を表す — te-design.md §3.2（ローカルの設計文書）
- ICD 203 は情報と仮定・判断の区別を求める — [ICD 203](https://archive.dni.gov/files/documents/ICD/ICD-203.pdf)
- IPCC は確信度を確率として読むことを禁じ、根拠と合意を分けて評価する — [IPCC guidance note](https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf) p.4
- ICD 203 は確信度と尤度を同じ文で組み合わせることを禁じる — [ICD 203](https://archive.dni.gov/files/documents/ICD/ICD-203.pdf)

### Inferences
- te のラベルは「種類」の軸で、GRADE・IPCC・ICD の「確かさの度合い」の軸と直交する。置き換えではなく、必要なら度合いの軸を任意の欄として足す。候補：前提に `agreement`（IPCC の low / medium / high）と `concerns`（GRADE / CERQual の観点のリスト）、`if_false`（ICD 203 の「仮定が誤っていたときの影響」）。
- `value` ラベルは、GRADE・IPCC・ICD のどれにも対応する段階がない（どれも事実や推定の確かさを扱う）。te の独自の部分として残す理由になる。ICD 203 の「仮定」が最も近いが、価値判断とは区別されていない。
- `definitional` も外部標準に対応物がない。PROV では「計算（Activity）が生んだ Entity」として `outputs/` と結べるので、`te check` の再計算と組み合わせる現行設計が適切。
- `prediction.confidence` は、IPCC/ICD の教訓に従い、確率（数値または固定した表の言葉）だけを入れる欄と定め、根拠の質は別の欄に分けるのがよい。
- 新しい欄を足すたびに `te check` の述語と `rules.toml` が増えるので、最小の版では対応表（文書）と `concerns` の語彙リストだけに留め、評価（設計 §8 の3）で必要が出たら欄を足す、が過剰な設計を避ける順番。

### Gaps
- 上の対応づけを実際の記録（life-value-in-flood-bc）に当てて、足りない欄があるかは試していない。
