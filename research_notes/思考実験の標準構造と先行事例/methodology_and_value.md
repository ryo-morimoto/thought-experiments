# 思考実験の方法論・分類と、結果の価値・新規性の判定の標準（`te` に取り込む候補）

対象: `te` の設計書（plugins リポジトリ worktree te-design の `plugins/thought-experiments/docs/te-design.md`）。現行スキルのモード（破壊・構成・自由探索・例示）、段階A〜C、対立仮説3つ以上（本命の逆を含む）、設定の欠陥の確認、条件を1つずつ変えて結論が反転する点を探す手順、文脈を持たない reviewer による反例の思考実験での攻撃、価値の確認3点（先行する答え、攻撃する立場の実在の保持者、事情に通じた実務者の予想の記録と結果との比較）を、確立された分類と手順に照らす。

凡例: 【未検証】＝一次資料で文言を確認していない、または二次資料の要約だけで確認したもの。

## 問1: 科学哲学の分類はどれが標準で、te のモードにどう対応するか

### Takeaway
「標準の分類」は存在しない。SEP は目的による分類、Sorensen の論理構造による分類、Brown の破壊／構成の分類を並べ、どれも標準とは呼んでいない。最も広く参照されるのは Brown の「破壊的／構成的」で、te の「破壊・構成」はこれと一致する。ただし Brown の構成的の下位区分（媒介的・推測的・直接的）と、SEP の「目的で判定せよ」という原則は te に入っていない。

### Cited Findings
- SEP「Thought Experiments」は1996年初出、2023年11月28日に実質改訂された。複数の分類を並べ、どれも標準とは言っていない。Brown の分類には「異論がないわけではない（Norton 1993b 参照）」と注記している — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- 目的による分類（SEP 第2節）: 娯楽、教育、抽象的な事態の例示、概念分析、理論の発見、理論に賛成または反対する証拠。原則は「想像上の実験は、その特定の目的で判定すべきだ」（Krimsky 1973, p.331 の引用）。区分は互いに排他的ではない — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- Sorensen (1992) の論理構造による分類: 「必然性の反駁」（ある言明が不可能とするものが可能だと示して反駁する。例は Gettier 事例）と、「可能性の反駁」（内容の可能性は主張せず「共可能性」を示す）— [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- Brown (1991, 2章) の主区分は構成的と破壊的で、Popper の「弁明的／批判的」に対応する。Popper は「発見的」も挙げた。破壊的の下位区分は次の4つ。(a) 内部矛盾を暴く（Galileo の落体）、(b) 他の信念と衝突させる（Schrödinger の猫）、(c) 論証の中心の前提を崩す（Thomson のバイオリニスト）、(d) 反例の思考実験。構成的は理論を支持し、しばしば例示によって「なるほど効果」を生む — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- 構成的の下位区分は次の3つ【二次資料経由、Brown の原文では未確認】。媒介的（既存の理論の形式的な側面を明らかにする。主に教育用。例は Maxwell の悪魔）、推測的（新しい理論を要する問題のある現象を立てる。「その現象は実際には起きない」と批判されやすい）、直接的（破壊と構成を兼ね、ある理論を批判して別の理論に置き換える）— [検索結果の要約（philarchive PICAPA-4、取得は403）](https://philarchive.org/archive/PICAPA-4); 下位区分の名前は El Skaf 2021 の要旨でも確認 — [El Skaf 2021, Synthese](https://link.springer.com/article/10.1007/s11229-021-03063-1)
- Brown の「Platonic（プラトン的）」は分類ではなく立場で、「ごく特別な場合には、古い経験的データを大きく超えて、自然についてのア・プリオリな知識を得る」とする — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- Norton の議論説は分類ではなく説明で、「どの思考実験も、実は（偽装されているかもしれない）議論である」とする — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- El Skaf (2021) は、物理の思考実験の多くが破壊と構成を兼ね、「不整合を暴き、解消する」ものとして働くと論じ、その共通構造を提案した。Krimsky の内部／外部の不整合の区別を使い、Norton の消去テーゼの強い読みを退けた（外部の不整合は常に内部の不整合に変換できるわけではない）【共通構造の中身は本文が取得できず未確認】 — [El Skaf 2021](https://link.springer.com/article/10.1007/s11229-021-03063-1)
- 評価について SEP は、設定が欠陥を持つ場合と、引き出した結論が正当化されない場合を区別する。また「想像の場面が関連する点で詳しいほど良い思考実験だ」とする。Dennett は「直観ポンプはよく濫用される。故意であることはまれだが」と警告した — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- 反例の思考実験は、Brown (2007) と、Norton の「思考実験／反思考実験の対」（2004, pp.45–49）で論じられている。例は Newton のバケツに対する Mach、Jackson の Mary に対する Dennett の青いバナナ。SEP は「反例の思考実験は、効果を持つためにそれほどもっともらしい必要はない」とする — [SEP](https://plato.stanford.edu/entries/thought-experiment/)
- 機能的な思考実験（Borsboom et al. 2002）は理論の中で特定の機能を果たすもの。Häggqvist は哲学の思考実験の規範的なモデルを作ったが、通常の例はどれもそれを満たさないと SEP は述べる — [SEP](https://plato.stanford.edu/entries/thought-experiment/)

te のモードとの対応（推論を含む）:

| te のモード | 対応する分類 | ずれ |
| --- | --- | --- |
| 破壊 | Brown 破壊的（a〜d）、Sorensen の反駁、Popper 批判的 | te は下位区分（内部矛盾、他の信念との衝突、前提の否定、反例）を持たない |
| 構成 | Brown 構成的（推測的・直接的） | 媒介的は te の「例示」に入る |
| 例示 | Brown 構成的のうち媒介的、SEP の目的「教育」「例示」 | 対応は良い |
| 自由探索 | Popper 発見的、SEP の目的「理論の発見」 | Brown の分類に対応する型はない |

### Inferences
- te のモードは Brown と Popper の区分にほぼ沿っており、名前を変える必要は小さい。取り込む価値があるのは次の2つ。(1) 破壊モードの下位区分（内部矛盾／他の信念との衝突／前提の否定／反例）を `frame.mode` の副欄にすると、何を確認すべきかが決まる。たとえば内部矛盾なら、無矛盾性の確認が要る。(2) 「推測的な思考実験は、その現象は起きないと批判されやすい」という指摘は、te の「設定の欠陥の確認」を推測的な構成モードで強めるべき理由になる。
- El Skaf の「破壊と構成を兼ねる」という観察は、te が `mode` を1つだけ選ばせる設計への反例になる。`modes_not_picked` を残す現在の設計は妥当だが、複数のモードを選べるようにする余地がある。
- SEP の「目的で判定せよ」は、te の `experiment.toml` の「ゴール（誰のどの判断）」と同じ考え方で、te はこれに沿っている。
- 「反例の思考実験は、もっともらしくなくても効く」という指摘は、te の段階C で reviewer の反例を「非現実的だから」と退けることを戒める根拠になる。

### Gaps
- Brown の原文での「mediative / conjectural / direct」の定義の文言（philarchive が403で取得できなかった）。
- Gendler の分類（SEP にはない。Gendler は見解として扱われている）、Routledge Companion (2018) の章構成と分類は確認できなかった。
- El Skaf の共通構造の段階の中身（Springer が認証へリダイレクトした）。

## 問2: 科学教育・工学・法・経済などの手順（what-if、シナリオ、反事実推論）

### Takeaway
最も直接に使えるのは Tetlock & Belkin (1996) の反事実の思考実験の評価基準である。「明確さ（1度に1つの原因を操作する）」と「共立可能性（つなぐ原理が互いに、また前件と両立する）」は、te の「条件を1つずつ変える」と「設定の欠陥の確認」にそのまま対応する。英国防省の Red Teaming Handbook の what-if 分析、前提の確認（assumptions check）、代替未来分析は、段階A・B の手順の型として借りられる。

### Cited Findings
- Tetlock & Belkin 編『Counterfactual Thought Experiments in World Politics』(1996) は反事実の評価基準を挙げる。「明確さ: 独立変数と従属変数（仮定した前件と後件）を特定して範囲を決める。思考実験は1度に1つの原因を操作すべきだ」。「論理的一貫性または共立可能性: 前件と後件をつなぐ原理を特定し、それらが互いに、また前件と両立するようにする」【二次資料（ブログの解説）経由】 — [Squeezing Water out of Stones（Turku 大学ブログ）](https://blogit.utu.fi/futuresofscience/2020/09/18/squeezing-water-out-of-stones-on-historical-counterfactuals/); 書誌 — [CASBS](https://casbs.stanford.edu/counterfactual-thought-experiments-world-politics-logical-methodological-and-psychological)
- 「最小限の書き換え（minimal rewrite）」は Tetlock の後の章で、前件の条件をごくわずか書き換えるだけで歴史が変わり得たという「紙一重の反事実」の議論に出てくる。1996年の基準の正式な一項目かどうかは未確認。「projectability」が基準に含まれるかも未確認 — [Turku 大学ブログ](https://blogit.utu.fi/futuresofscience/2020/09/18/squeezing-water-out-of-stones-on-historical-counterfactuals/)
- 同じ解説は、前件が奇跡や介入を要するように見えるという理由で反事実を退ける傾向（「surrealism-whining」）への懸念も紹介している — [Turku 大学ブログ](https://blogit.utu.fi/futuresofscience/2020/09/18/squeezing-water-out-of-stones-on-historical-counterfactuals/)
- 英国防省 Red Teaming Handbook 第3版（2021年6月、DCDC）の what-if 分析: 従来の what-if は「計画が失敗したと想像し、原因へさかのぼる」。red team mindset 版は逆に、最初から失敗への複数の経路を想像する。手順は、問題を簡潔に述べる → 「損失」と「利得」の円を置く → 高い水準の分類で列挙する → マインドマップ式に枝分かれさせる — [Red Teaming Handbook（PDF, para 4.10–4.11）](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 同書の前提の確認（assumptions check, para 5.24 以降）: 経験に基づく暗黙と明示の前提を調べる。説明文から明示の前提と暗黙の前提を拾い、それぞれに「この前提はどれほど妥当か」などを問う — [Red Teaming Handbook](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 同書は、高影響・低確率分析と、代替未来分析（para 10.7–10.8、複雑で不確かな状況を複数の未来に分ける。テンプレートは図10.4）も挙げる — [Red Teaming Handbook](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)

### Inferences
- Tetlock & Belkin の「明確さ」は te の `operation.varied`（変えた条件を1つに限る）を支える外部の根拠になる。「共立可能性」は te の `frame.flaw`（設定の欠陥）を具体化する。「固定した条件・理想化・変えた条件」が互いに矛盾しないかを確認する項目として、規則データの `show` に入れられる。
- 「surrealism-whining」への懸念は、SEP の「反例の思考実験はもっともらしくなくても効く」と同じ向きで、te の reviewer の反例を「非現実的」の一言で退けない規則の根拠になる。
- 赤チーム式の what-if（失敗への経路を前向きに枝分かれさせる）は、te の段階B の「反転点を探す」を体系化する型として使える。損失と利得の2方向に枝を出すのは、対立仮説の「本命の逆」を必ず置く規則と同じ発想。

### Gaps
- 科学教育（例: Clement の想像によるシミュレーション）、法（仮想事例による法的推論）、経済（反事実の政策評価）、シナリオプランニング（Shell や Schwartz の2軸の手法）の手順は、今回の検索の範囲では一次資料で確認していない。地図スキルの2軸と比べる価値があるが、未調査。

## 問3: 事前登録・予測の記録と、驚き（予想とのずれ）の採点

### Takeaway
事前登録の要点は「結果を見る前に、仮説・予測・分析を固定する」ことである。Registered Reports では、問いの重要性と仮説の妥当性を結果より前に審査する。te の `prediction` 出来事はこの考え方に沿っているが、確率で書かれていないため、Brier スコアのような採点も、事前と事後の差を「驚き」として測ることもできない。

### Cited Findings
- Registered Reports の Stage 1 では、査読者は「研究の問いの重要性と、提案された仮説の論理・根拠・もっともらしさ」を評価する。Stage 1 の原稿は、序論、方法（分析計画を含む）、予備データだけを含む — [PNAS Nexus Registered Reports Guidelines](https://academic.oup.com/pnasnexus/pages/registered-reports-guidelines); [TU Delft 版ガイドライン](https://filelist.tudelft.nl/Library/Themaportalen/Open.tudelft.nl/publishing/about/Registered-Reports-Guidelines.pdf)
- Bayes 因子を使う研究では「Bayes 因子を計算できるように理論の予測を特定しなければならない」とする誌がある — [検索結果の要約（PNAS Nexus/TU Delft のいずれか）](https://academic.oup.com/pnasnexus/pages/registered-reports-guidelines)【どの誌の文言かは未確認】
- OSF の事前登録テンプレートは、研究の問い、標本の大きさ、除外基準、計画した分析を記述する。OSF には Registered Report 用の共同テンプレートもある — [Keele 大学の案内](https://www.keele.ac.uk/korsa/quantitative/pre-registration/); [OSF テンプレート wiki](https://osf.io/x4gzt/wiki/Preregistration%20Template)【テンプレートの欄の文言は未取得】
- Good Judgment Project では、数千人のボランティアが500件以上の出来事に数値の確率を付け、100万件を超える予測を出した。採点は Brier スコアで、低いほど良く、0が完全。ある問題群では、全選択肢に等確率を付けると0.53になる — [Mellers, Tetlock ほか（Harvard, Zeckhauser のページの PDF）](https://scholar.harvard.edu/sites/scholar.harvard.edu/files/rzeckhauser/files/improving_the_accuracy_of_geopolitical_risk_assessments.pdf)
- 上位2%が superforecaster で、ある年の superforecaster の70%が翌年も superforecaster だった。訓練のうち「比較の群（参照クラス）」は正確さと相関し、「事後の検討（post-mortem）」は不正確さと相関した【二次資料（AI Impacts の要約）】 — [AI Impacts](https://aiimpacts.org/?p=1283); [EA Forum の同記事](https://forum.effectivealtruism.org/posts/W94KjunX3hXAtZvXJ/evidence-on-good-forecasting-practices-from-the-good)
- Tetlock らは、予測のトーナメントを、議論の透明性を高め、論争を改善する道具として提案している（2014年の論文の題名「Forecasting tournaments: tools for increasing transparency and improving debate」）【本文は未取得】 — [Wharton の PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2015/07/2014---forecasting-tournaments-tools-for-increasing-transparency-and-improving-debate.pdf)
- 驚きの定量化: Baldi と Itti は、驚きを「観察者の事前と事後の信念分布の距離」と定義した — [Baldi & Itti, "Of Bits and Wows"（PMC）](https://pmc.ncbi.nlm.nih.gov/articles/PMC2860069); これを使い、LLM エージェントの仮説に対する事前と事後の信念のずれ（Bayesian surprise）を報酬として仮説を探す AutoDiscovery（NeurIPS 2025）がある。人による評価では、発見の約3分の2が領域の専門家にとっても驚きだったと報告している — [arXiv 2507.00310](https://arxiv.org/abs/2507.00310)

### Inferences
- te の `prediction` に `confidence` があるのは良い。ただし、比べる対象が「答え」の文字列なので、ずれを採点できない。`prediction` を対立仮説（`rival`）ごとの確率の配分にすると、`conclusion` 後に (a) 予測の Brier スコア、(b) 事前と事後の分布の距離（驚き）を `fold` で計算できる。「価値の確認(3) 予想との比較」が、感想から数値になる。
- Registered Reports の考え方からは、`prediction` は段階B の `operation` より前に記録されなければ意味がない。te の段階A の `requires` に `prediction` が入っているのはこれと一致する。加えて、`operation` の後に `prediction` を訂正（`correction`）するのを禁止する不変条件を足すと、事前登録の「後から変えない」を構造で守れる。
- GJP の「参照クラスが効き、事後の検討は効かない」という結果は、`prediction` を書くときに参照クラス（似た問いで分野がどう答えたか）を書かせる指示の根拠になる。これは「価値の確認(1) 先行する答え」とつながる。

### Gaps
- OSF の標準の事前登録テンプレートで、仮説・予測を書く欄の正確な文言は取得していない。
- Mellers et al. 2014（Psychological Science）の一次の数値（チーム化の効果など）は二次資料でしか確認していない。

## 問4: 敵対的共同研究・赤チーム・pre-mortem・steelman と、独立した批判者の効果の証拠

### Takeaway
敵対的共同研究では、意見の対立する当事者が、反証の条件に事前に合意し、中立の仲介者を置き、結果を問わず公表する。赤チームでは「計画に利害を持たない外部の者」が新しい視点をもたらすとされる。これらは te の「文脈を持たない reviewer」と「実在の保持者」の確認に対応する。効果の実証は限られるが、悪魔の代弁者が専門家だけの判断より良いというメタ分析はある。

### Cited Findings
- 敵対的共同研究（adversarial collaboration）では、意見の異なる研究者が次のことをする。協力して真理を追う。公正で偏りのない方法を共同で設計する。反証の条件に合意する。結果を問わず公表する。成功させるには、相手を慎重に選び、互いに信頼する仲介者を入れ、全員が合意するまで対立点と競合する見方を明確に定義し、方法と分析に合意した後に事前登録する。課題は、時間がかかることと脱線しやすいことで、そのため事前登録などの予防策が要る — [Clark の講演スライド（ASN 2022, PDF）](https://nutrition.org/wp-content/uploads/2022/11/Clark_ASN_Adversarial-Collaboration.pdf)
- 論文は Clark, Costello, Mitchell, Tetlock (2022) "Keep your enemies close: Adversarial collaborations will improve behavioral science", Journal of Applied Research in Memory and Cognition, DOI 10.1037/mac0000004。査読の過程に敵対的共同研究を組み込むことを提案している — [Wikipedia](https://www.wikipedia.org/wiki/Adversarial_collaboration); [UVA Law](https://content.law.virginia.edu/node/2174641)
- 英国防省 Red Teaming Handbook は red teaming を「利用者がより良い情報に基づいて判断し、より頑健な成果物を作るのを助けるために、構造化された・創造的な・批判的な思考技法を独立して適用すること」と定義する。手順は数時間かかることがあり、個人でもできるが「別の red team が行うのが最善」とする — [Red Teaming Handbook para 1.9](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 外部の red team の利点として、同書は次を挙げる。計画に投資しておらず成否に中立。既存の偏りに影響されない。計画と意思決定に関わっていないので、既存の問題に新しい視点をもたらせる。構成員には、その分野の専門家と、分野を知らないが分析力のある非専門家の2種類が適し、後者は「新鮮で新しい視点」をもたらす。人数は4〜8人が最適で6人が理想 — [Red Teaming Handbook para 7.1–7.6](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 同書の red cell は、敵対者や主要な利害関係者の視点、あるいは人格を採ることを主な目的とするチーム — [Red Teaming Handbook para 1.13](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 同書の悪魔の代弁者（devil's advocacy, para 6.8–6.10）: 計画の欠陥を見つける簡単な技法。個人でもできる。批判の口調が敵対的すぎると要点が失われると注意している — [Red Teaming Handbook](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- 同書の pre-mortem 分析（para 11.2）の手順: (1) 計画が見事に失敗したと仮定する。(2) 失敗の姿を定義する。(3) 直接の原因を2〜6個定義する。(4) 各原因から因果の鎖をさかのぼる。(5) 意思決定者が制御できる行動や決定点に達したら止める（根本原因）。(6) 各原因で繰り返す。(7) 緩和策を決める — [Red Teaming Handbook](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1027158/20210625-Red_Teaming_Handbook.pdf)
- Klein の "Performing a Project Premortem"（HBR 2007年9月号、85(9):18–19）。よく引かれる「30%」は Klein 自身の研究ではなく、Mitchell, Russo, Pennington (1989) の「予期的な後知恵（prospective hindsight）が、将来の結果の理由を挙げる能力を30%高めた」という結果で、プロジェクトの成功の改善ではない — [Wikipedia: Premortem](https://www.Wikipedia.org/wiki/Premortem); [Klein の記事の写し（PDF）](https://comprobo24.github.io/assignments/performing_a_project_premortem.pdf)
- 独立した批判の効果の証拠: Schwenk (1990) のメタ分析（OBHDP 47(1):161–176）では、悪魔の代弁者は専門家だけの方法より全般に効果的だった。弁証法的探究（対立する計画を立てる方法）の優位は、構造の緩い課題では示されなかった — [IDEAS/RePEc](https://ideas.repec.org/a/eee/jobhdp/v47y1990i1p161-176.html); 要旨の文言 — [zhenzhi のデータベース](https://data.zhenzhi.com/details/1/999233521)【要旨は二次のデータベースで確認】
- Fjermestad の総説は、構造化された対立の技法を調べた52件の研究を数え、実験研究は悪魔の代弁者を支持すると報告している — [now publishers ISY-013](https://nowpublishers.com/article/DownloadSummary/ISY-013)
- 思想的チューリングテスト（Ideological Turing Test, Caplan 2011）は、反対の立場の保持者が自分たちの仲間と区別できないほど、その立場を述べられるかを問う。steelman（自分の基準で最も強い版）とは違い、保持者自身の述べ方への忠実さを目標にする。そのため、磨かれた steelman でも不合格になり得る。合格しても反対の立場が正しいとは示せず、実際の保持者に聞く代わりにもならない — [LessWrong: Ideological Turing Tests](https://lesswrong.com/w/ideological-turing-tests); [Caplan 2011（Econlib）](https://www.econlib.org/archives/2011/06/how_to_make_me.html); 行動指標として操作化したもの — [Brand, Brady, Stafford 2025, Cognitive Science](https://eprints.whiterose.ac.uk/id/eprint/233236/1/Cognitive%20Science%20-%202025%20-%20Brand%20-%20The%20Ideological%20Turing%20Test%20%20A%20Behavioral%20Measure%20of%20Open%E2%80%90Mindedness%20and.pdf)

te との対応（推論を含む）:

| 確立した手順 | te の対応 | ずれ・取り込む候補 |
| --- | --- | --- |
| 敵対的共同研究: 反証の条件に事前に合意する | `rival` と `prediction` | 対立仮説ごとに「何が出たらこれを捨てるか」を段階A で書く欄がない |
| 敵対的共同研究: 中立の仲介者 | なし | 利用者を仲介者として `decision` に記録できる |
| 赤チーム: 計画に投資していない外部の者 | `attack.by=fresh`、`te brief` | 対応は良い。専門家と非専門家の2種類の lens も使える |
| red cell: 敵対者の人格を採る | `holder` | te は実在の保持者の証拠を求めるが、その立場で反論させる段階はない |
| pre-mortem: 失敗を仮定して原因をさかのぼる | 段階C の攻撃 | 「結論が誤りだったと判明した」と仮定する依頼文を `brief` に入れられる |
| 思想的チューリングテスト | `holder.strawman` | 保持者の言葉の引用（`sources`）で忠実さを確かめるのは ITT の考え方に近い |

### Inferences
- te の「文脈を持たない reviewer」は、赤チームの外部チームの利点（計画に投資していない、新しい視点）と同じ理屈で、独立して作られた設計と言える。Handbook の「専門家と非専門家の2種類」は、`te brief --lens` の lens の既定の組として使える。
- 敵対的共同研究の「反証の条件に事前に合意する」は、te にいちばん欠けている部分。`rival` に `would_reject_if`（何が出たら捨てるか）を持たせ、段階A の `requires` に含めると、段階C の結論が「後付けの解釈」になるのを防げる。
- pre-mortem は「何がまずいか」ではなく「失敗した、なぜか」と問う。GJP では post-mortem が不正確さと相関したが、これは別の操作（事後の振り返り）なので、pre-mortem の効果を否定するものではない。
- 独立した批判者がより多くの誤りを見つけるという直接の実証は、今回見つけた範囲では、悪魔の代弁者のメタ分析（専門家だけの判断より良い）が中心で、「独立した reviewer」と「自己批判」を直接比べた研究は確認できなかった。

### Gaps
- Clark et al. 2022 の本文（手順の正式な段階）は未取得。講演スライドで代用した。
- TRADOC（米陸軍の Red Team Handbook / Applied Critical Thinking Handbook）は未確認。
- コードレビューや査読で「独立した評価者が誤りの検出を増やす」ことの定量的な証拠は未調査。
- Schwenk 1990 の効果量は未取得。

## 問5: 結論の新規性・価値の判定（資金提供機関・誌の定義、事前の予想に対する驚き）

### Takeaway
資金提供機関は新規性を「既存の研究や実践の枠組みに挑み、変えようとするか」で問う。一方で NIH 自身が「革新的でなくても影響の大きい重要な研究がある」と明記している。つまり新規性と価値は別の軸で、te の価値の確認が「新しさ」だけでなく「誰のどの判断を変えるか」を問う構造は、この区別と合っている。驚きは、事前と事後の信念の距離として定量化できる。

### Cited Findings
- NIH の革新性（Innovation）の問い: 「その申請は、新しい理論的概念、手法、方法論、装置、介入を使って、現在の研究や臨床実践の枠組みに挑み、変えようとしているか」 — [NIAID Review Criteria](https://www.niaid.nih.gov/research/review-criteria)
- 2025年1月25日以降の締め切りでは、NIH は簡素化した査読の枠組みを使い、5つの基準（意義、研究者、革新性、方法、環境）を3つの要素にまとめ直した — [NIAID Review Criteria](https://www.niaid.nih.gov/research/review-criteria)
- NIH の2024年10月の査読者向けの指針: 「高い革新性は高い意義と関係することが多いが、革新的な性質でなくても分野に影響する重要な研究がある」【検索結果の要約経由】 — [NIAID Review Criteria](https://www.niaid.nih.gov/research/review-criteria)
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
