# 思考実験の方法論・分類と、結果の価値・新規性の判定の標準（`te` に取り込む候補）

対象: `te` の設計書（plugins リポジトリ worktree te-design の `plugins/thought-experiments/docs/te-design.md`）。現行スキルのモード（破壊・構成・自由探索・例示）、段階A〜C、対立仮説3つ以上（本命の逆を含む）、設定の欠陥の確認、条件を1つずつ変えて結論が反転する点を探す手順、文脈を持たない reviewer による反例の思考実験での攻撃、価値の確認3点（先行する答え、攻撃する立場の実在の保持者、事情に通じた実務者の予想の記録と結果との比較）を、確立された分類と手順に照らす。

凡例: 【未検証】＝一次資料で文言を確認していない、または二次資料の要約だけで確認したもの。

一次資料による確認（2026-11-21）: 各項目の出典を、著者自身の出版物か発行元の公式文書に差し替えた。取得したファイルの sha256 とページを本文に書く（確認作業のファイルはコミットしていない）。一次資料で確かめられなかった主張は、各問の Gaps の「一次資料で確認できず」に移し、推論や結論の根拠には使わない。

SEP「Thought Experiments」（Brown & Fehige、2023-11-28 改訂）の取得物: https://plato.stanford.edu/entries/thought-experiment/ 、sha256 `a88ea672fc7cbac6324332bcdabf4572d5559447ce81a39b128eb2ab6f02decd`（§2 Taxonomies、§4.2 を照合）。以下 [SEP] はこれを指す。

## 問1: 科学哲学の分類はどれが標準で、te のモードにどう対応するか

### Takeaway
「標準の分類」は存在しない。SEP は目的による分類、Sorensen の論理構造による分類、Brown の破壊／構成の分類を並べ、どれも標準とは呼んでいない。最も広く参照されるのは Brown の「破壊的／構成的」で、te の「破壊・構成」はこれと一致する。Brown の破壊的の4つの下位区分は SEP（Brown 自身が共著）で確認でき、te にはまだ入っていない。構成的の下位区分としてよく挙がる「媒介的・推測的・直接的」は、Brown 自身の文章では確認できなかったので、Brown の分類としては扱わない。

### Cited Findings
- SEP「Thought Experiments」は1996年初出、2023年11月28日に実質改訂された。複数の分類を並べ、どれも標準とは言っていない。Brown の分類には「異論がないわけではない（Norton 1993b 参照）」と注記している — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- 目的による分類（SEP 第2節）: 娯楽、教育、抽象的な事態の例示、概念分析、理論の発見、理論に賛成または反対する証拠。原則は「想像上の実験は、その特定の目的で判定すべきだ」（Krimsky 1973, p.331 の引用）。区分は互いに排他的ではない — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- Sorensen (1992) の論理構造による分類: 「必然性の反駁」（ある言明が不可能とするものが可能だと示して反駁する。例は Gettier 事例）と、「可能性の反駁」（内容の可能性は主張せず「共可能性」を示す）— [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- Brown (1991, 2章) の主区分は構成的と破壊的で、Popper の「弁明的／批判的」に対応する。Popper は「発見的」も挙げた。破壊的の下位区分は次の4つ。(a) 内部矛盾を暴く（Galileo の落体）、(b) 他の信念と衝突させる（Schrödinger の猫）、(c) 論証の中心の前提を崩す（Thomson のバイオリニスト）、(d) 反例の思考実験。構成的は理論を支持し、しばしば例示によって「なるほど効果」を生む — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- 原文: "A third taxonomy (see Brown 1991, chapter 2), which has not gone unchallenged (see Norton 1993b), ... the main division is constructive vs. destructive and resembles Karl Popper's distinction between apologetic and critical thought experiments." 破壊的の第4の下位区分は "counter thought experiments" — [SEP §2](https://plato.stanford.edu/entries/thought-experiment/)（sha256 は冒頭）
- Brown の「Platonic（プラトン的）」は分類ではなく立場で、「ごく特別な場合には、古い経験的データを大きく超えて、自然についてのア・プリオリな知識を得る」とする — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- Norton の議論説は分類ではなく説明で、「どの思考実験も、実は（偽装されているかもしれない）議論である」とする — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- El Skaf (2021, Synthese 199:6119–6147) は、多くの思考実験が、既存の理論的な言明の不整合を暴き、それを解消する推測を出すという2段の働きをすると論じた。要旨: "A TE reveals an inconsistency in part of our previously held, sometimes empirically well-established, theoretical statements. A TEer or her critic then proposes a resolution in the form of a conjecture, a hypothesis that merits further investigation." — Springer が Crossref に登録した要旨 [api.crossref.org/works/10.1007/s11229-021-03063-1](https://api.crossref.org/works/10.1007/s11229-021-03063-1)（sha256 `040c02bb19f142d778bf220611ac8db2d002f0c654c14294fcdeac0f7625b6c9`。本文は未取得）。これを Brown の破壊と構成を1つの思考実験が兼ねる例と読むのは、このノートの解釈である
- 評価について SEP は、設定が欠陥を持つ場合と、引き出した結論が正当化されない場合を区別する。また「想像の場面が関連する点で詳しいほど良い思考実験だ」とする。Dennett は「直観ポンプはよく濫用される。故意であることはまれだが」と警告した — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- 反例の思考実験は、Brown (2007) と、Norton の「思考実験／反思考実験の対」（2004, pp.45–49）で論じられている。例は Newton のバケツに対する Mach、Jackson の Mary に対する Dennett の青いバナナ。SEP は「反例の思考実験は、効果を持つためにそれほどもっともらしい必要はない」とする — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- 機能的な思考実験（Borsboom et al. 2002）は理論の中で特定の機能を果たすもの。Häggqvist は哲学の思考実験の規範的なモデルを作ったが、通常の例はどれもそれを満たさないと SEP は述べる — [SEP](https://plato.stanford.edu/entries/thought-experiment/)

te のモードとの対応（推論を含む）:

| te のモード | 対応する分類 | ずれ |
| --- | --- | --- |
| 破壊 | Brown 破壊的（a〜d）、Sorensen の反駁、Popper 批判的 | te は下位区分（内部矛盾、他の信念との衝突、前提の否定、反例）を持たない |
| 構成 | Brown 構成的、Popper 弁明的 | 構成的の下位区分は一次資料で確認できず、対応づけない |
| 例示 | SEP の目的「教育」「抽象的な事態の例示」 | 対応は良い |
| 自由探索 | Popper 発見的、SEP の目的「理論の発見」 | Brown の分類に対応する型はない |

### Inferences
- te のモードは Brown と Popper の区分にほぼ沿っており、名前を変える必要は小さい。取り込む価値があるのは、破壊モードの下位区分（内部矛盾／他の信念との衝突／前提の否定／反例）を `frame.mode` の副欄にすることである。何を確認すべきかが決まる。たとえば内部矛盾なら、無矛盾性の確認が要る。
- El Skaf の「不整合を暴き、推測で解消する」という2段の働きを、破壊と構成を兼ねるものと読むなら（このノートの解釈）、te が `mode` を1つだけ選ばせる設計への反例になる。`modes_not_picked` を残す現在の設計は妥当だが、複数のモードを選べるようにする余地がある。
- SEP の「目的で判定せよ」は、te の `experiment.toml` の「ゴール（誰のどの判断）」と同じ考え方で、te はこれに沿っている。
- 「反例の思考実験は、もっともらしくなくても効く」という指摘は、te の段階C で reviewer の反例を「非現実的だから」と退けることを戒める根拠になる。

### Gaps
- 一次資料で確認できず:
  - 構成的の下位区分「媒介的（mediative）・推測的（conjectural）・直接的（direct）」を Brown の分類とする主張。現行の SEP にも、Brown 単著の SEP 旧版（2004、2007、2010、2014、2019 年の版）にも "mediative" "conjectural" の語はない。典拠とされる Brown (1991)『The Laboratory of the Mind』第2章は書籍で、philarchive の写しは 403。El Skaf 2021 の要旨にもこれらの語はない（前の版のノートの「El Skaf の要旨でも確認」は誤り）。
  - El Skaf (2021) が Krimsky の内部／外部の不整合の区別を使い、Norton の消去テーゼの強い読みを退けたという主張。要旨には書かれておらず、本文は Springer と PhilSci-Archive の bot 検査で取得できなかった。
- Gendler の分類（SEP にはない。Gendler は見解として扱われている）、Routledge Companion (2018) の章構成と分類は確認できなかった。

## 問2: 科学教育・工学・法・経済などの手順（what-if、シナリオ、反事実推論）

### Takeaway
Tetlock & Belkin (1996) は反事実の主張を判定する「6つの暫定的な基準」を挙げるが、基準の本文は一次資料で読めなかった。そのため、基準の名前や文言（「明確さ」「共立可能性」など）を te の手順の根拠には使わない。te の「条件を1つずつ変える」は、外部の根拠を持たない te 自身の手順として扱う。英国防省の Red Teaming Handbook の what-if 分析、前提の確認（assumptions check）、代替未来分析は、段階A・B の手順の型として借りられる。

### Cited Findings
- Tetlock & Belkin 編『Counterfactual Thought Experiments in World Politics』(1996) の第1章 p.5: "In this spirit, we advance a provisional list of six standards for judging counterfactual claims, illustrating each standard with examples drawn from later chapters." — 第1章冒頭の出版社版スキャン（Belkin 自身のサイト）[PDF](https://aaronbelkin.org/pdfs/Counterfactual%20Thought%20Experiments%20in%20World%20Politics%20-%201st%20chpt.pdf)、sha256 `28cf4e5752355089fae893e3400456b6e46f081dd6bfc9b80b3172f7faac5942`（画像 PDF、p.11 まで。基準の本文はこの範囲にない）
- 英国防省 Red Teaming Handbook 第3版（2021年6月、DCDC）の what-if 分析: 従来の what-if は「計画が失敗したと想像し、原因へさかのぼる」。red team mindset 版は逆に、最初から失敗への複数の経路を想像する。手順は、問題を簡潔に述べる → 「損失」と「利得」の円を置く → 高い水準の分類で列挙する → マインドマップ式に枝分かれさせる — [Red Teaming Handbook（PDF, para 4.10–4.11）](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 同書の前提の確認（assumptions check, para 5.24 以降）: 経験に基づく暗黙と明示の前提を調べる。説明文から明示の前提と暗黙の前提を拾い、それぞれに「この前提はどれほど妥当か」などを問う — [Red Teaming Handbook](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 同書は、高影響・低確率分析と、代替未来分析（para 10.7–10.8、複雑で不確かな状況を複数の未来に分ける。テンプレートは図10.4）も挙げる — [Red Teaming Handbook](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)

### Inferences
- te の `operation.varied`（変えた条件を1つに限る）を `te check` で検査するのは、te 自身の手順「条件を1つずつ変える」を機械で守らせるもので、外部の標準の裏づけはない（推論）。`frame.flaw`（設定の欠陥）の確認項目（固定した条件・理想化・変えた条件が互いに矛盾しないか）は、SEP の「設定が欠陥を持つ場合と、引き出した結論が正当化されない場合を区別する」に対応させて `show` に入れられる。
- reviewer の反例を「非現実的」の一言で退けない規則の根拠は、SEP の「反例の思考実験は、効果を持つためにそれほどもっともらしい必要はない」に置く。
- 赤チーム式の what-if（失敗への経路を前向きに枝分かれさせる）は、te の段階B の「反転点を探す」を体系化する型として使える。損失と利得の2方向に枝を出すのは、対立仮説の「本命の逆」を必ず置く規則と同じ発想。

### Gaps
- 一次資料で確認できず:
  - Tetlock & Belkin の基準の名前と文言（「明確さ（前件と後件を特定する。1度に1つの原因を操作する）」「論理的一貫性または共立可能性」）、「minimal rewrite」「projectability」が基準に入るか、「surrealism-whining」への懸念。いずれも Turku 大学のブログの解説（二次資料）でしか読めていない。基準の本文（p.11 以降）は、De Gruyter が WAF の検査で、JSTOR と Project MUSE が購読で、cuni.cz がログインで取得できなかった。fes.de の PDF は Lebow 2000 の書評論文で、Lebow 自身の8基準であり、Tetlock & Belkin の一次ではない。「1度に1つの原因を操作すべきだ」はブログの言い換えの可能性がある。
- 科学教育（例: Clement の想像によるシミュレーション）、法（仮想事例による法的推論）、経済（反事実の政策評価）、シナリオプランニング（Shell や Schwartz の2軸の手法）の手順は、今回の検索の範囲では一次資料で確認していない。地図スキルの2軸と比べる価値があるが、未調査。

## 問3: 事前登録・予測の記録と、驚き（予想とのずれ）の採点

### Takeaway
事前登録の要点は「結果を見る前に、仮説・予測・分析を固定する」ことである。Registered Reports では、問いの重要性と仮説の妥当性を結果より前に審査する。te の `prediction` 出来事はこの考え方に沿っているが、確率で書かれていないため、Brier スコアのような採点も、事前と事後の差を「驚き」として測ることもできない。

### Cited Findings
- Registered Reports の Stage 1 では、査読者は「研究の問いの重要性と、提案された仮説の論理・根拠・もっともらしさ」を評価する。Stage 1 の原稿は、序論、方法（分析計画を含む）、予備データだけを含む — [PNAS Nexus Registered Reports Guidelines](https://academic.oup.com/pnasnexus/pages/registered-reports-guidelines); [TU Delft 版ガイドライン](https://filelist.tudelft.nl/Library/Themaportalen/Open.tudelft.nl/publishing/about/Registered-Reports-Guidelines.pdf)
- PNAS Nexus の Registered Reports の指針は、Bayes 因子で分析する研究には「Bayes 因子を計算できるように理論の予測を特定しなければならない」と求める（Stage 1 の Methods: "For studies involving analyses with Bayes factors, the predictions of the theory must be specified so that a Bayes factor can be calculated."）。Bayes 的な検定は推奨（"encouraged"）にとどまり、すべての投稿への要件ではない — [PNAS Nexus Registered Reports Guidelines](https://academic.oup.com/pnasnexus/pages/registered-reports-guidelines)（公式ページを Web で読んだ。Cloudflare のためファイルと sha256 はない）
- OSF の事前登録テンプレートは、研究の問い、標本の大きさ、除外基準、計画した分析を記述する。OSF には Registered Report 用の共同テンプレートもある — [Keele 大学の案内](https://www.keele.ac.uk/korsa/quantitative/pre-registration/); [OSF テンプレート wiki](https://osf.io/x4gzt/wiki/Preregistration%20Template)【テンプレートの欄の文言は未取得】
- Good Judgment Project の予測は Brier スコアで採点された。確率の訓練は参照クラスの使用を促し、1年目の Brier スコアを改善した（p.1 要旨、p.4: "Training improved Year 1 Brier scores, F(2, 1586) = 14.29, p < .001. Probability training was more effective than scenario training"）。1年目の上位2%を superforecaster としてエリートのチームにまとめると、2年目に他のすべての群を大きく上回り、平均への回帰は見られなかった（p.6: "There was no evidence of Year 2 regression to the mean"）。2年目の superforecaster の Brier は最初の週 0.25、最後の週 0.07（p.5 Table 1） — Mellers et al. 2014, Psychological Science（eScholarship の出版社版 [PDF](https://escholarship.org/content/qt4rg4n9vr/qt4rg4n9vr_noSplash_4ff67e56b3dac616e0163b75090705e6.pdf)、sha256 `77b1414013ed56fb7258204be1968506eaf29430c85531785a6e58986fadf9c4`）
- 予測の説明で「比較の群（comparison classes）」を挙げた予測は正確さと、「事後の検討（post-mortem）」を挙げた予測は不正確さと関連した。後者について著者は、事後の検討は外れた予測の後に行うのが普通だからだろうと説明している（pp.515–516: "The P principle likely increased Brier scores because post-mortems are normally conducted after inaccurate forecasts."）。つまり因果が逆で、事後の検討が有害だという意味ではない — Chang, Chen, Mellers & Tetlock (2016) Judgment and Decision Making 11(5):509–526（Cambridge の出版社版 OA PDF、[doi:10.1017/S1930297500004599](https://doi.org/10.1017/S1930297500004599)、sha256 `edda0d1b3c44afa6d748dec9ead314fda5c488b94e12a755d560865c0d4b25fb`）
- Tetlock らは、予測のトーナメントを、議論の透明性を高め、論争を改善する道具として提案している（2014年の論文の題名「Forecasting tournaments: tools for increasing transparency and improving debate」）【本文は未取得】 — [Wharton の PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2015/07/2014---forecasting-tournaments-tools-for-increasing-transparency-and-improving-debate.pdf)
- 驚きの定量化: Baldi と Itti は、驚きを「観察者の事前と事後の信念分布の距離」と定義した — [Baldi & Itti, "Of Bits and Wows"（PMC）](https://pmc.ncbi.nlm.nih.gov/articles/PMC2860069); これを使い、LLM エージェントの仮説に対する事前と事後の信念のずれ（Bayesian surprise）を報酬として仮説を探す AutoDiscovery（NeurIPS 2025）がある。人による評価では、発見の約3分の2が領域の専門家にとっても驚きだったと報告している — [arXiv 2507.00310](https://arxiv.org/abs/2507.00310)

### Inferences
- te の `prediction` に `confidence` があるのは良い。ただし、比べる対象が「答え」の文字列なので、ずれを採点できない。`prediction` を対立仮説（`rival`）ごとの確率の配分にすると、`conclusion` 後に (a) 予測の Brier スコア、(b) 事前と事後の分布の距離（驚き）を `fold` で計算できる。「価値の確認(3) 予想との比較」が、感想から数値になる。
- Registered Reports の考え方からは、`prediction` は段階B の `operation` より前に記録されなければ意味がない。te の段階A の `requires` に `prediction` が入っているのはこれと一致する。加えて、`operation` の後に `prediction` を訂正（`correction`）するのを禁止する不変条件を足すと、事前登録の「後から変えない」を構造で守れる。
- GJP で、参照クラスの使用を促す確率の訓練が Brier スコアを改善し（Mellers 2014）、比較の群を挙げた予測が正確さと関連した（Chang 2016、相関）ことは、`prediction` を書くときに参照クラス（似た問いで分野がどう答えたか）を書かせる指示の根拠になる。これは「価値の確認(1) 先行する答え」とつながる。事後の検討と不正確さの関連は逆の因果で説明されているので、事後の検討を省く根拠にはならない。

### Gaps
- OSF の標準の事前登録テンプレートで、仮説・予測を書く欄の正確な文言は取得していない。
- 一次資料で確認できず:
  - 「ある年の superforecaster の70%が翌年も superforecaster だった」。Mellers et al. (2015) Perspectives on Psychological Science 10(3) が出典と思われるが、SAGE の購読が要り取得できなかった。
  - 「数千人が500件以上の出来事に確率を付け、100万件を超える予測を出した」「全選択肢に等確率なら Brier 0.53」。Harvard の Zeckhauser のページの PDF は取得時に HTML が返り、照合できなかった。

## 問4: 敵対的共同研究・赤チーム・pre-mortem・steelman と、独立した批判者の効果の証拠

### Takeaway
敵対的共同研究では、意見の対立する当事者が、反証の条件に事前に合意し、互いに信頼する仲介者を置き、結果を問わず公表する。赤チームでは「計画に利害を持たない外部の者」が新しい視点をもたらすとされる。これらは te の「文脈を持たない reviewer」と「実在の保持者」の確認に対応する。効果の実証は、一次資料で確かめられた範囲では見つからなかった（よく引かれる Schwenk 1990 のメタ分析は一次資料を取得できなかった）。

### Cited Findings
- 敵対的共同研究（adversarial collaboration）では、意見の異なる研究者が次のことをする。協力して真理を追う。公正で偏りのない方法を共同で設計する。反証の条件に合意する。結果を問わず公表する。成功させるには、相手を慎重に選び、互いに信頼する仲介者を入れ、全員が合意するまで対立点と競合する見方を明確に定義し、方法と分析に合意した後に事前登録する。課題は、時間がかかることと脱線しやすいことで、そのため事前登録などの予防策が要る — [Clark の講演スライド（ASN 2022, PDF）](https://nutrition.org/wp-content/uploads/2022/11/Clark_ASN_Adversarial-Collaboration.pdf)、sha256 `117db7db511db48256c777f6d566616f5c81e254450047a5f590c520bb9787fb`（スライド4: "Commit to conditions of falsifiability • Publish results regardless of outcome"、スライド7: "Include a mutually trusted moderator ... After methods and analyses are agreed upon, preregister plans"）
- Isch, Tetlock & Clark (2025) "Reflections on adversarial collaboration from the adversaries: was it worth it?" Theory and Society 54:929–946 は、参加者29人への調査から、両者に信頼される中立の第三者（"trusted and respected by both parties"）を置くことと、方法を事前に十分に事前登録することを推奨し、これが Clark et al. 2022 などの推奨と一致すると書く（p.939） — 出版社版 OA を Tetlock の Wharton のページに置いたもの [PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2026/02/Reflections_on_adversarial_collaboration.pdf)、sha256 `408c71ae8381017cd87b80fb2a78bcf7d12224cb71eda254c77487bc62b3bca6`
- 論文は Clark, Costello, Mitchell, Tetlock (2022) "Keep your enemies close: Adversarial collaborations will improve behavioral science", Journal of Applied Research in Memory and Cognition, DOI 10.1037/mac0000004。本文は未取得（書誌のみ）
- 英国防省 Red Teaming Handbook は red teaming を「利用者がより良い情報に基づいて判断し、より頑健な成果物を作るのを助けるために、構造化された・創造的な・批判的な思考技法を独立して適用すること」と定義する。手順は数時間かかることがあり、個人でもできるが「別の red team が行うのが最善」とする — [Red Teaming Handbook para 1.9](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 外部の red team の利点として、同書は次を挙げる。計画に投資しておらず成否に中立。既存の偏りに影響されない。計画と意思決定に関わっていないので、既存の問題に新しい視点をもたらせる。構成員には、その分野の専門家と、分野を知らないが分析力のある非専門家の2種類が適し、後者は「新鮮で新しい視点」をもたらす。人数は4〜8人が最適で6人が理想 — [Red Teaming Handbook para 7.1–7.6](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 同書の red cell は、敵対者や主要な利害関係者の視点、あるいは人格を採ることを主な目的とするチーム — [Red Teaming Handbook para 1.13](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 同書の悪魔の代弁者（devil's advocacy, para 6.8–6.10）: 計画の欠陥を見つける簡単な技法。個人でもできる。批判の口調が敵対的すぎると要点が失われると注意している — [Red Teaming Handbook](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 同書の pre-mortem 分析（para 11.2）の手順: (1) 計画が見事に失敗したと仮定する。(2) 失敗の姿を定義する。(3) 直接の原因を2〜6個定義する。(4) 各原因から因果の鎖をさかのぼる。(5) 意思決定者が制御できる行動や決定点に達したら止める（根本原因）。(6) 各原因で繰り返す。(7) 緩和策を決める — [Red Teaming Handbook](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- Klein の premortem（"Performing a Project Premortem"、HBR 2007年9月号）でよく引かれる「30%」は、Mitchell, Russo & Pennington（1989）に由来するとされる。ただし同論文の要旨によれば、測ったのは出来事の説明の長さ、理由の種類、時制で、説明を変えたのは時間の視点（未来か過去か）ではなく、結果が確実と告げられたかどうかだった（"temporal perspective showed little influence while outcome uncertainty strongly affected the nature of explanations for events. Explanations for sure events tended to be longer, to contain a higher proportion of episodic reasons, and to be expressed in past tense."）。「30%」の数値は一次で確認していない。いずれにせよ、プロジェクトの成功率の改善を示した結果ではない — Journal of Behavioral Decision Making 2(1):25–38、Wiley が Crossref に登録した要旨 [api.crossref.org/works/10.1002/bdm.3960020103](https://api.crossref.org/works/10.1002/bdm.3960020103)、sha256 `e7240435074672fd43621cdf986804429116212956e26fdba267c84c086e2132`
- Fjermestad の総説は、構造化された対立の技法を調べた52件の研究を数え、実験研究は悪魔の代弁者を支持すると報告している — [now publishers ISY-013](https://nowpublishers.com/article/DownloadSummary/ISY-013)（出版社の要約ページ。今回の一次資料の照合の対象外で、本文は未読。推論の根拠には使わない）
- 思想的チューリングテスト（Ideological Turing Test, Caplan 2011）は、反対の立場の保持者が自分たちの仲間と区別できないほど、その立場を述べられるかを問う。steelman（自分の基準で最も強い版）とは違い、保持者自身の述べ方への忠実さを目標にする。そのため、磨かれた steelman でも不合格になり得る。合格しても反対の立場が正しいとは示せず、実際の保持者に聞く代わりにもならない — [LessWrong: Ideological Turing Tests](https://lesswrong.com/w/ideological-turing-tests); [Caplan 2011（Econlib）](https://www.econlib.org/archives/2011/06/how_to_make_me.html); 行動指標として操作化したもの — [Brand, Brady, Stafford 2025, Cognitive Science](https://eprints.whiterose.ac.uk/id/eprint/233236/1/Cognitive%20Science%20-%202025%20-%20Brand%20-%20The%20Ideological%20Turing%20Test%20%20A%20Behavioral%20Measure%20of%20Open%E2%80%90Mindedness%20and.pdf)

te との対応（推論を含む）:

| 確立した手順 | te の対応 | ずれ・取り込む候補 |
| --- | --- | --- |
| 敵対的共同研究: 反証の条件に事前に合意する | `rival` と `prediction` | 対立仮説ごとに「何が出たらこれを捨てるか」を段階A で書く欄がない |
| 敵対的共同研究: 互いに信頼する仲介者 | なし | 利用者を仲介者として `decision` に記録できる |
| 赤チーム: 計画に投資していない外部の者 | `attack.by=fresh`、`te brief` | 対応は良い。専門家と非専門家の2種類の lens も使える |
| red cell: 敵対者の人格を採る | `holder` | te は実在の保持者の証拠を求めるが、その立場で反論させる段階はない |
| pre-mortem: 失敗を仮定して原因をさかのぼる | 段階C の攻撃 | 「結論が誤りだったと判明した」と仮定する依頼文を `brief` に入れられる |
| 思想的チューリングテスト | `holder.strawman` | 保持者の言葉の引用（`sources`）で忠実さを確かめるのは ITT の考え方に近い |

### Inferences
- te の「文脈を持たない reviewer」は、赤チームの外部チームの利点（計画に投資していない、新しい視点）と同じ理屈で、独立して作られた設計と言える。Handbook の「専門家と非専門家の2種類」は、`te brief --lens` の lens の既定の組として使える。
- 敵対的共同研究の「反証の条件に事前に合意する」は、te にいちばん欠けている部分。`rival` に `would_reject_if`（何が出たら捨てるか）を持たせ、段階A の `requires` に含めると、段階C の結論が「後付けの解釈」になるのを防げる。
- pre-mortem は「何がまずいか」ではなく「失敗した、なぜか」と問う。GJP で post-mortem を挙げた予測が不正確さと関連したのは、外れた後に振り返るからという逆の因果で説明されており（Chang et al. 2016）、pre-mortem の効果を否定するものではない。pre-mortem の効果の数値（「30%」）も一次では確認できていないので、`brief` に pre-mortem の問い方を入れる根拠は、Red Teaming Handbook の手順（公式文書）に置く。
- 独立した批判者がより多くの誤りを見つけるという直接の実証は、一次資料で確かめられた範囲では見つからなかった。「独立した reviewer」と「自己批判」を直接比べた研究も確認できなかった。

### Gaps
- Clark et al. 2022 の本文（手順の正式な段階）は未取得。講演スライドと Isch, Tetlock & Clark 2025 で代用した。
- TRADOC（米陸軍の Red Team Handbook / Applied Critical Thinking Handbook）は未確認。
- コードレビューや査読で「独立した評価者が誤りの検出を増やす」ことの定量的な証拠は未調査。
- 一次資料で確認できず:
  - Schwenk (1990) のメタ分析（OBHDP 47(1):161–176）の「悪魔の代弁者は専門家だけの方法より全般に効果的。弁証法的探究の優位は構造の緩い課題では示されなかった」。ScienceDirect は bot 検査と 403、Crossref に要旨の登録なし。確認できたのは書誌（題名 "Effects of devil's advocacy and dialectical inquiry on decision making: A meta-analysis"）だけ。前の版の出典は IDEAS/RePEc と二次のデータベースだった。
  - Clark et al. (2022) が査読の過程に敵対的共同研究を組み込むことを提案しているという主張（前の版は Wikipedia と UVA Law が出典）。PsycNet は JavaScript が必要で、Crossref に要旨なし。
  - Mitchell, Russo & Pennington (1989) の「30%」。本文は Wiley の検査で取得できず、Klein の HBR 記事も要約しか取得できなかった。

## 問5: 結論の新規性・価値の判定（資金提供機関・誌の定義、事前の予想に対する驚き）

### Takeaway
資金提供機関は新規性を「既存の研究や実践の枠組みに挑み、変えようとするか」で問う。一方で NIH 自身が、査読者向けの指針で「革新的な性質でなくても分野に影響する重要な研究がある」とし、革新性の評点が低くても総合評価を高くしてよいとしている。つまり新規性と価値は別の軸で、te の価値の確認が「新しさ」だけでなく「誰のどの判断を変えるか」を問う構造は、この区別と合っている。驚きは、事前と事後の信念の距離として定量化できる。

### Cited Findings
- NIH の革新性（Innovation）の問い: 「その申請は、新しい理論的概念、手法、方法論、装置、介入を使って、現在の研究や臨床実践の枠組みに挑み、変えようとしているか」（"Does the application challenge and seek to shift current research or clinical practice paradigms ..."） — [NIAID Review Criteria](https://www.niaid.nih.gov/research/review-criteria)（現行ページは bot 検証で 405。Internet Archive の 2026-07-23 の保存版 20260723140203 で読んだ。sha256 `94c8012a1bfd4c9b6ca1c1f6eef0baf9a512c876762ed1e5929304b6c0a4a8c8`、"Content last reviewed on January 8, 2025"）
- 2025年1月25日以降の締め切りでは、NIH は簡素化した査読の枠組みを使い、5つの基準（意義、研究者、革新性、方法、環境）を3つの要素にまとめ直した — [NIAID Review Criteria](https://www.niaid.nih.gov/research/review-criteria)
- NIH の査読者向けの指針「Writing Effective Critiques for Research Applications」（PDF の作成日 2024-10-21）の p.2（3. Innovation）: "Innovation need not be a driver of impact. High innovation is often related to high significance, but there is important work that will impact the field that is not innovative by nature. You can assign a weak innovation criterion score and still assign a strong Overall Impact score." — [NIH PDF](https://grants.nih.gov/sites/default/files/Reviewer_Guidance_Writing%20Effective%20Critiques.pdf)（現行は 403。Internet Archive の保存版 20260727185311 で読んだ。sha256 `c87d5de1d87b6bea225a9bdf20ad2e96744b8d2f22e231f50f47fa1a26ba5e24`）。前の版はこの文の出典を NIAID のページとしていたが、そのページにこの文はない
- CSR の Review Matters の投稿は、革新性はそれ自体では有用な分類ではないと論じた。従来の方法が適切なら、申請者が革新性で減点されるべきではないからだ — [CSR Review Matters](https://www.csr.nih.gov/reviewmatters/?p=131)
- CSRAC の作業部会（2020）は、要素「科学の重要性」を「意義」と「革新性の概念的な側面」から導くよう提案した — [CSRAC 推奨（PDF）](https://public.csr.nih.gov/sites/default/files/2021-04/Recommendations_of_the_CSRAC_Working_Group_on_Simplifying_Review-non-CT_and_CT.pdf)
- 科学の新規性を「分野が将来の進歩について持つ予想を裏切ること」と捉え、論文や特許の内容と文脈の組み合わせの確率から驚きを測る研究がある — [PMC10039062](https://pmc.ncbi.nlm.nih.gov/articles/PMC10039062)
- 驚きは、事前と事後の信念分布の距離として定義される（Baldi & Itti） — [PMC2860069](https://pmc.ncbi.nlm.nih.gov/articles/PMC2860069)

### Inferences
- te の価値の確認3点は、外部の基準と次のように対応する。(1) 先行する答え → 新規性（NIH の革新性、組み合わせの驚き）。(2) 実在の保持者 → 意義（攻撃する立場が実際に誰かの判断を動かしているか）。(3) 実務者の予想との比較 → 事前と事後の驚き（Baldi & Itti）。3点は「新しさ」「重要さ」「驚き」という別々の軸を測っているので、1つの合否にまとめず、軸ごとに記録するのがよい。
- NIH の「革新的でなくても重要な研究がある」に従えば、「先行する答えがすでにある」ことは、結論の価値をゼロにする理由にはならない。分野の答えを利用者の判断に適用すること自体に価値があり得る。te が `prior_answer.found` で実験を止めるのではなく、ゴール（誰のどの判断）に照らして続けるかを利用者の `decision` で決める形が、この区別に合う。
- 驚きを数値にするには、問3 の推論のとおり、`prediction` を対立仮説ごとの確率の配分にする必要がある。

### Gaps
- 主要誌（Nature、Science など）の編集方針での「新規性」の定義は未調査。
- 欧州研究会議（ERC）の「画期的（ground-breaking）」の基準は未調査。
- 思考実験の結論に限った新規性の評価法を扱う文献は見つからなかった。
