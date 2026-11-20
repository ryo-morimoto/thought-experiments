# 認知負荷理論・教授設計と、コード理解への応用（人物起点の調査）

調査日: 2026-11-21。対象は、PR・大きな diff・仕様・設計判断のように内在的負荷（intrinsic load）が高い成果物を理解しやすくする仕組み（pr-tour、pr-review など）の設計者です。

読み方の注意:
- 「一次資料を読んだ」と書いたのは、本文を取得してテキストを確かめた2本（Kalyuga 2007、de Jong 2010）だけです。ほかは要旨・書誌・二次引用での確認です。各項目に確認の深さを書きます。
- Sweller, van Merriënboer & Paas (2019)「20 Years Later」は Springer と CORE の両方で取得に失敗しました（403、HTML のみ）。2019 年版の内容（germane load の再定義など）は未検証として Gaps に回しています。
- 読んだ PDF の sha256（取得元 URL のバイト列。リポジトリには置いていません）:
  - Kalyuga (2007) `acbd290d5478168ad5fd351f4193c7f03dbaffc70eec492548e01398d54a85f6` ← https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf
  - de Jong (2010) `2488a7962ff40590dd451bf4732e16509fe70eec335fe72b4a77f7ea78698c68` ← https://ris.utwente.nl/ws/files/6597420/Jong10cognitive.pdf

---

## 問1: 主要人物は誰か（名前・選んだ理由・主要著作）

### Takeaway
理論の中核は Sweller（CLT と element interactivity）、Paas（負荷の測定）、van Merriënboer（4C/ID）、Kalyuga（熟達化反転）、Mayer（マルチメディア学習の原則）です。プログラミングへの応用は Margulieux / Morrison / Guzdial（サブゴールラベル）と、Duran / Sorva（プログラムの複雑さを要素の相互作用として測る CCCP）が中心です。開発者の負荷の生体計測は Fakhoury / Arnaoudova（fNIRS とアイトラッキング）が直接の先行研究です。

### Cited Findings
**理論側**
- **John Sweller**（UNSW）: CLT の創始者。1998 年の総説 Sweller, van Merriënboer & Paas "Cognitive Architecture and Instructional Design"（Educational Psychology Review）と、その 20 年後の改訂版 Sweller, van Merriënboer & Paas (2019)（EPR 31, 261–292、DOI 10.1007/s10648-019-09465-5）。出版社版は有料で、CORE にリポジトリ版がある。 — [検索結果（Springer / CORE の書誌）](https://link.springer.com/article/10.1007/s10648-019-09465-5); [CORE](https://core.ac.uk/download/237588613.pdf)（本文の取得は失敗）
- **Fred Paas**: 負荷の自己評定尺度の作者。de Jong によれば、教育科学で最もよく使われる自己評定尺度は Paas (1992) が導入した 9 段階評定です（"The most frequently used self-report scale in educational science was introduced by Paas (1992)"）。 — [de Jong 2010（一次資料を読んだ）](https://ris.utwente.nl/ws/files/6597420/Jong10cognitive.pdf)
- **Slava Kalyuga**: 熟達化反転効果（expertise reversal effect）。Kalyuga, Ayres, Chandler & Sweller (2003) "The Expertise Reversal Effect", Educational Psychologist 38(1), 23–31（著者順はリポジトリによって異なる）。総説 Kalyuga (2007) "Expertise Reversal Effect and Its Implications for Learner-Tailored Instruction", EPR 19, 509–539。 — [UOW の記録](https://ro.uow.edu.au/edupapers/136); [Kalyuga 2007（一次資料を読んだ）](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)
- **Richard E. Mayer**: マルチメディア学習。Mayer & Moreno (2003) "Nine Ways to Reduce Cognitive Load in Multimedia Learning", Educational Psychologist 38(1), 43–52。Cambridge Handbook of Multimedia Learning の章 "Principles for managing essential processing ... segmenting, pretraining, and modality principles"。 — [T&F の書誌](https://www.tandfonline.com/doi/abs/10.1207/S15326985EP3801_6); [Cambridge の章ページ](https://www.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning-segmenting-pretraining-and-modality-principles/4110A2275F6DCD02DAB1F8B37BA7E5CE)
- **Ton de Jong**（Twente）: CLT の内側からの批判者。"Cognitive load theory, educational research, and instructional design: some food for thought", Instructional Science 38(2), 105–134 (2010)。同じ号に Mayer の反論的コメントがある。 — [de Jong 2010](https://ris.utwente.nl/ws/files/6597420/Jong10cognitive.pdf); [検索結果の要約（Mayer のコメント）](https://link.springer.com/article/10.1007/s11251-009-9113-x)
- **Pollock, Chandler & Sweller**: isolated-interacting elements 法。"Assimilating complex information", Learning and Instruction 12(1), 61–86 (2002)。 — [UOW の記録](https://ro.uow.edu.au/edupapers/145)

**プログラミング・ソフトウェア工学への応用**
- **Lauren Margulieux / Mark Guzdial / Richard Catrambone**: プログラミングのサブゴールラベル付き worked example（ICER 2012）。統計学での Catrambone (1998) の結果をプログラミングに移したもの。 — [二次引用（escholarship）](https://escholarship.org/content/qt35z8842x/qt35z8842x.pdf)（ICER 2012 本体は未読）
- **Briana Morrison / Margulieux / Adrienne Decker**: サブゴールを入門講義全体に適用した追試（IJ STEM Education 2020）。 — [Springer Open の書誌](https://link.springer.com/content/pdf/10.1186/s40594-020-00222-7.pdf)（本文の取得は失敗）
- **Rodrigo Duran / Juha Sorva / Otto Leite**: "Towards an Analysis of Program Complexity From a Cognitive Perspective", ICER '18, 21–30。CCCP（Cognitive Complexity of Computer Programs）という枠組みで、plan depth（推論に必要なスキーマの深さ）と maximal plan interactivity（プログラムの合成で生じるスキーマ間の相互作用）の2つの指標を出す。 — [検索結果（ResearchGate の PDF の書誌）](https://researchgate.net/profile/Rodrigo-Duran-2/publication/326918081_Towards_an_Analysis_of_Program_Complexity_From_a_Cognitive_Perspective/links/5b9f7d28299bf13e60381085/Towards-an-Analysis-of-Program-Complexity-From-a-Cognitive-Perspective.pdf)（PDF は 403）; [Aalto の学位論文の記録](https://aaltodoc.aalto.fi/items/67ae951e-fc1d-4b46-a8c6-13fc7d164581)
- **Sarah Fakhoury / Venera Arnaoudova / Olusola Adesope**（WSU）: "The effect of poor source code lexicon and readability on developers' cognitive load", ICPC 2018, 286–296, DOI 10.1145/3196321.3196347。fNIRS で負荷を、アイトラッキングで負荷が生じた識別子を測った。 — [NSF PAR](https://par.nsf.gov/biblio/10090357-effect-poor-source-code-lexicon-readability-developers-cognitive-load)

### Inferences
- 人物の系譜は2本に分かれる。教育心理の CLT 本流（Sweller–Paas–van Merriënboer–Kalyuga、批判側に de Jong）と、計算機科学教育（Guzdial–Margulieux–Morrison、Sorva）です。後者は前者の「効果」を移植しており、ソフトウェア工学の計測系（Fakhoury、Siegmund、Sharif）は CLT の三分類をほとんど使わず「負荷の総量」を測っている、という違いがある（後者については計測系の論文1本からの推論）。

### Gaps
- **未検証（一次資料を読めていない人物）**: van Merriënboer の 4C/ID（Ten Steps to Complex Learning）、Paul Kirschner（Kirschner, Sweller & Clark 2006 "Why minimal guidance ... does not work" が代表作のはず）、Juhani Tuovinen（Tuovinen & Sweller 1999、探索学習 vs worked example と事前知識の交互作用のはず）、Raymond Lister（BRACElet、ネオピアジェ的発達段階）、Felienne Hermans（The Programmer's Brain, 2021）、Janet Siegmund（fMRI によるプログラム理解、2014）、Bonita Sharif（アイトラッキング）、Norman Peitek。いずれも今回の調査で原典を確認していないため、記憶による推定として扱うこと。
- "Jan-Philipp Steghöfer" が CLT をコード理解に応用した研究は見つけられていない（検索していない）。

---

## 問2: 内在的負荷（intrinsic load）は減らせるのか。どう管理するのか

### Takeaway
初期の CLT は「内在的負荷は教材と学習者の熟達度で決まり、教え方では変えられない」としていました。しかし同じ系譜の研究が、(a) 要素をいったん切り離して提示する（isolated-interacting elements）、(b) 事前訓練で部品の名前と性質を先に教える（pretraining）、(c) 学習者のペースで区切る（segmenting）ことで「本質的な処理」の過負荷を管理できると示しています。ただし「減った」のは課題を一時的に変えた結果か、熟達度を上げた結果で、最終的に要素をすべて相互作用させて理解する必要は残ります。つまり内在的負荷は消せず、時間方向に分散させるか、学習者側のスキーマを先に育てて相対的に下げるしかない、というのが確認できた範囲の結論です。

### Cited Findings
- 内在的負荷・element interactivity の考え方: 同時に作業記憶で処理しなければならない要素の数が負荷を決める。低相互作用の例は語彙（単語は独立に覚えられる）、高相互作用の例は文法や電気回路の働き。 — [Pollock et al. 2002 の要旨と引用論文の要約（検索結果）](https://ro.uow.edu.au/edupapers/145)
- **isolated-interacting elements 法**（Pollock, Chandler & Sweller 2002）: 第1段階で複雑な教材を孤立した要素として提示し、要素の相互作用を人為的に下げる。第2段階で全体を提示する。統制群は両段階とも全情報を受け取った。初心者でこの方法が統制群を上回り、熟達度が利益の鍵とされた。 — [UOW の記録・要旨（検索結果経由。本文は未読）](https://ro.uow.edu.au/edupapers/145)
- **Mayer の「本質的処理（essential processing）」の管理**: Mayer は内在的負荷にあたるものを essential processing と呼び、その過負荷を避ける方法として segmenting・pretraining・modality の3原則を挙げる。segmenting は "people learn more deeply when a multimedia message is presented in learner-paced segments rather than as a continuous unit"、pretraining は "when they know the names and characteristics of the main concepts"。 — [Cambridge Handbook の章（検索結果の抜粋）](https://www.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning-segmenting-pretraining-and-modality-principles/4110A2275F6DCD02DAB1F8B37BA7E5CE); [Mayer & Moreno 2003 の PDF（uky.edu）](https://www.uky.edu/~gmswan3/575/9_ways_to_reduce_CL.pdf)
- de Jong は、内在的負荷と germane load の区別も学習者の熟達度に依存していると指摘する（内在的負荷は教材そのものという「もの」を指し、germane load は「過程」を指すので、存在論的に別の種類の概念を並べている）。 — [de Jong 2010（一次資料を読んだ, pp. 112–113 付近）](https://ris.utwente.nl/ws/files/6597420/Jong10cognitive.pdf)
- worked example → 問題解決への移行（fading）: Kalyuga (2007) は、学習中に rapid test を繰り返し、成績に応じて段階的に手がかりを減らし（worked example の手順を問題解決の手順に置き換える）、学習者に合わせた条件が知識の伸びで有意に優れたと報告している。 — [Kalyuga 2007（一次資料を読んだ, 1410–1425 行付近 = 本文 pp. 525–527 付近）](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)
- プログラムの内在的複雑さを測る試み: Duran, Sorva & Leite の CCCP は、プログラムに含まれる認知的要素とその絡み合いを分析し、plan depth と maximal plan interactivity を出す。 — [Aalto の学位論文の記録](https://aaltodoc.aalto.fi/items/67ae951e-fc1d-4b46-a8c6-13fc7d164581)（ICER 論文本文は未読）
- サブゴールラベル: worked example の手順のまとまりにラベルを付けると、例の構造が浮き上がり、学習者が情報を頭の中で整理し、自己説明を促す、と説明されている。 — [二次引用（escholarship）](https://escholarship.org/content/qt35z8842x/qt35z8842x.pdf)

### Inferences
- PR に当てはめると、「変更全体」を一度に見せる Files changed は全要素の同時提示にあたる。pr-tour のようにコードの流れ順に1ファイルずつ見せるのは segmenting と isolated-interacting elements の第1段階に近い。ただし Pollock らの設計は「第2段階で全体を相互作用させて見せる」ことまでが手法なので、ツアーの最後に「全体の相互作用（どの変更がどの変更を前提にしているか）」をまとめる段階がないと、手法の半分しか移していないことになる。
- 定義プレビュー（呼ばれる関数・型の定義を先に見せる）は pretraining（部品の名前と性質を先に知る）にあたる。
- サブゴールラベルは、diff の塊に「この塊は何のための変更か」という目的のラベルを付けることに対応する。手順そのものではなく、手順のまとまりに名前を与える点が肝。
- CCCP の考え方（理解に要るスキーマの深さとスキーマ間の相互作用）は、PR の「難しさ」をファイル数や行数ではなく、同時に頭に置く必要がある概念の数で見積もる根拠になりうる。

### Gaps
- **未検証**: Sweller 2010 "Element interactivity and intrinsic, extraneous, and germane cognitive loads"（EPR）と 2019 年改訂版で、germane load を「独立した負荷の源」から「内在的負荷を扱うために割かれる作業記憶資源（germane resources）」へ再定義した、という理解は記憶によるもので、本文で確認できていない。
- **未検証**: 4C/ID の4要素（learning tasks / supportive information / procedural information / part-task practice）と、単純から複雑への課題クラスの順序づけ。van Merriënboer の原典を読めていない。
- completion problem（途中まで解かれた問題）の効果の原典（van Merriënboer の 1990 年前後の研究と思われる）は未確認。
- Pollock 2002 の効果量・サンプルサイズは未確認。

---

## 問3: 境界条件（熟達化反転・冗長性・一過性情報・注意の分割）と、熟練開発者向けツールへの含意

### Takeaway
最も重要な境界条件は熟達化反転効果です。初心者に効く手がかり（worked example、統合された説明、詳しい誘導）は、熟練者には冗長になり、学習も遂行も悪くします。プログラミング領域（PLC のプログラミング）でも、worked example の優位は経験とともに消え、より複雑な課題では問題解決の練習の方が良くなりました。熟練開発者向けの理解支援は、既定で詳しく説明するのではなく、相手の既有知識を素早く診断して手がかりの量を変える必要があります。

### Cited Findings
- 熟達化反転効果の定義: 初心者にうまく働く教え方が、学習者が経験を積むと価値を失い、ときに学習を害する。 — [UOW の記録（要旨）](https://ro.uow.edu.au/articles/journal_contribution/The_expertise_reversal_effect/27724950/1)
- 機構: 熟練者は長期記憶の知識構造を内的な誘導として使えるので、外から詳しい誘導を与えると、両者を照合・統合する処理が余計な作業記憶負荷になる。 "Presenting knowledgeable learners with detailed external guidance may hinder their learning and performance relative to the levels they could achieve with minimal instructional support." — [Kalyuga 2007, p. 513（一次資料を読んだ）](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)
- 冗長性効果との関係: 熟達化反転は当初、冗長性効果の一種として予測された。初心者には有益（冗長でない）な情報が、熟練者には冗長になる。初心者には図と文を統合して注意の分割（split-attention）を除くのが効き、熟練者には冗長な表現を取り除く方が効くと予想された。その後、提示モダリティや誘導の量にも拡張され、狭い意味の冗長性効果とは区別されるようになった（熟達化反転では、外部情報が学習者の内部の知識に対して冗長になる）。 — [Kalyuga 2007, pp. 513–514（一次資料を読んだ）](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)
- 図＋ナレーションの例: 初期段階では図＋ナレーション群が優れていたが、集中訓練の後は図だけの群が上回り、第1段階の結果が逆転した。主観的な難しさの評定も負荷による説明を支持した。 — [Kalyuga 2007（一次資料を読んだ）](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)
- **プログラミング領域の反転**: Kalyuga et al. (2001b) では、PLC（programmable logic controller）のプログラミングで worked example が問題解決の練習より優れるという効果が、訓練者の経験とともに消えた。リレー回路のスイッチング式の課題では、集中訓練の後、より複雑な課題で問題解決の練習の方が worked example より良かった。 — [Kalyuga 2007, p. 520 付近（一次資料を読んだ）](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)
- **熟達度の素早い診断**: Kalyuga は first-step 診断法（問題を見せて最初の一歩だけを答えさせ、その一歩で熟達度を推定する）と rapid verification 法（解の候補を見せて正誤を素早く判断させる）を開発し、時間のかかる従来のテストとの併存的妥当性が十分に高かったと報告している。 — [Kalyuga 2007, pp. 525–526 付近（一次資料を読んだ）](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)
- de Jong は、冗長な情報でも短ければ有利という研究を引いている（冗長性効果自体にも境界条件がある）。 — [de Jong 2010（一次資料を読んだ）](https://ris.utwente.nl/ws/files/6597420/Jong10cognitive.pdf)
- 熟練者の負荷は課題によって変わり、どの「悪さ」が負荷を上げるかも一様ではない。Fakhoury et al. では、語彙の不整合（linguistic antipattern）は負荷を有意に上げ、それは不整合な識別子だけでなくスニペット全体に及んだ。一方、構造の不整合が平均負荷を上げる統計的証拠は見つからなかった（どちらも時間と正答率は下げた）。 — [検索結果の要約（NSF PAR・WSU の記録）](https://par.nsf.gov/biblio/10090357-effect-poor-source-code-lexicon-readability-developers-cognitive-load)

### Inferences
- PR レビュアーは多くの場合、そのコードベースの熟練者である。pr-tour のような「全変更を丁寧に順に説明する」ガイドは、変更された領域を知らないレビュアーには効くが、その領域の作者・常連には冗長性効果・熟達化反転で逆効果になりうる。既定値を「全部説明」にするのは危うい。
- 熟練者向けの手がかりは「誘導」よりも「スキーマの起動」に寄せるべき。短いラベル（何のための変更か）と、既有知識とのズレ（どこが慣習から外れているか）だけを示し、詳細は求められたときに出す。
- first-step 診断は、ツールが読者の熟達度を推定する方法の手本になる。例: ツアーの冒頭で「この PR は何を変えると思うか」を一言答えさせる、あるいは読者のそのファイル群への過去のコミット・レビュー履歴を熟達度の代理にする（後者は CLT の研究では検証されていない、私の推論）。
- Fakhoury の結果は、内在的負荷とは別に「名前の不整合」という外在的負荷がスニペット全体の理解を重くすることを示す。PR 理解支援は、説明を足すだけでなく、名前とふるまいが食い違っている箇所を指摘することでも負荷を下げられる。

### Gaps
- **未検証**: transient information effect（音声・アニメーションなど消えていく情報は、長く複雑だと作業記憶に保持できず、静的な文字や図より不利になる。Leahy & Sweller 2011 など）。原典を読めていない。PR ガイドを動画やライブ説明にする場合に関わる。
- **未検証**: split-attention effect の原典（Chandler & Sweller 1991, 1992）。Kalyuga 2007 経由で名前と関係のみ確認。
- 熟練開発者を対象に熟達化反転を直接検証したソフトウェア工学の研究は見つけられていない。

---

## 問4: 批判・論争・失敗した試み

### Takeaway
最大の論点は、三種類の負荷（とくに germane load）の定義と測定です。de Jong (2010) は、germane load が事後的な説明に使われていること、「良い負荷は良い、悪い負荷は悪い」という同語反復になっていること、熟達度によって同じ処理が germane にも extraneous にもなること、を指摘しました。また、負荷はしばしば直接測られず、測る場合も1項目の自己評定で、形式も統一されていません。ソフトウェア工学の計測研究でも、自己報告・生体計測・注視時間が互いに相関せず、別のものを測っているように見えます。

### Cited Findings
- **germane load の事後的説明**: Sweller et al. (1998) は、変化の大きい練習問題の群が高い負荷を報告し、転移テストの成績も良かったことを「その負荷は germane だった」と説明した。de Jong はこれを "post-hoc" な説明だとし、正しいスキーマ獲得につながる処理の方が高い負荷を課すと考える根拠はないと述べる。 — [de Jong 2010, p. 111 付近（一次資料を読んだ）](https://ris.utwente.nl/ws/files/6597420/Jong10cognitive.pdf)
- **同語反復**: 負荷が無関係な活動から来れば悪く、関係する活動から来れば良い、という定義について "quite tautological character (what is good is good, what is bad is bad)"。 — [de Jong 2010, p. 113 付近（一次資料を読んだ）](https://ris.utwente.nl/ws/files/6597420/Jong10cognitive.pdf)
- **熟達度依存**: Paas et al. (2004) の「初心者に germane な負荷は熟練者には extraneous になりうる」、Kalyuga (2007) の「germane load を高める方法が初心者には過負荷になる」を引き、de Jong は処理の性質ではなく働き方で区別していることになると結論する。さらに、何が germane かは学習目標によっても変わる（Gerjets & Scheiter 2003: 構造を強調した群は学習時間が長かったが、同型問題では表層を強調した群に負けた）。 — [de Jong 2010（一次資料を読んだ）](https://ris.utwente.nl/ws/files/6597420/Jong10cognitive.pdf)
- **測定の問題**: 多くの研究で負荷は直接測られず、転移テストの成績から間接的に推定されている。測定法は自己評定・生体計測（心拍変動、fMRI など）・二次課題の3群。最もよく使われる Paas (1992) 由来の質問紙は標準の形式がない。Paas (1992) の原研究では、学習中の投入努力に条件間の差は見つかっていない。 — [de Jong 2010, pp. 120–123 付近（一次資料を読んだ）](https://ris.utwente.nl/ws/files/6597420/Jong10cognitive.pdf)
- 反論側: Mayer は同じ号のコメントで de Jong の論文を詳細で体系的な総説と評価しつつ、三種の負荷を分けて測れる証拠として DeLeeuw & Mayer (2008) を挙げた。 — [検索結果の要約（Mayer のコメント, Instructional Science 38(2)）](https://link.springer.com/article/10.1007/s11251-009-9113-x)
- CLT は de Jong 以前から、概念の明確さ（Schnotz & Kürschner 2007）と方法論（Gerjets et al. 2009a）について批判されていた。 — [検索結果の要約](https://link.springer.com/article/10.1007/S11251-009-9110-0)
- **ソフトウェア工学での測定の食い違い**: Fakhoury et al. では、自己報告の難しさ、（fNIRS で測った）負荷、注視時間は相関せず、課題の難しさの別の側面を測っているように見えた。 — [検索結果の要約（NSF PAR・WSU の記録）](https://par.nsf.gov/servlets/purl/10135165)

### Inferences
- 「このツールで germane load が増えた」と主張する評価設計は避けるべき。測定の妥当性が理論の内側でも争われている。評価するなら、理解の結果（レビューで見つかる欠陥、後から説明できる設計意図、チームの共有メンタルモデルの一致度）と、所要時間を直接測る方が堅い。
- 「同じ説明が熟達度によって germane にも extraneous にもなる」という de Jong の指摘は、問3の熟達化反転と同じことを別の側から言っている。説明の量を読者で変える設計が、理論上も批判上も支持される唯一の安定した方向。
- 自己報告と生体計測が食い違うので、利用者アンケートの「わかりやすかった」は理解の指標としては弱い。

### Gaps
- **未検証**: CLT の効果の再現性（大規模な追試、メタ分析での効果量の縮小）について、今回は一次資料を見つけていない。「CLT は再現性危機の影響を受けた」と書くには根拠が足りない。
- **未検証**: 2019 年改訂版で Sweller らが germane load の扱いをどう変えたか（問2の Gaps を参照）。de Jong の批判への応答になっているはずだが確認できていない。
- Kirschner, Sweller & Clark (2006) をめぐる発見学習派との論争（Hmelo-Silver らの反論）も未確認。

---

## 問5: コード理解の仕組みに移せる設計原則の候補

### Takeaway
確認できた資料から、PR・コード理解支援に移せる原則は次の7つです。共通の前提は「内在的負荷は消せない。時間方向に分散させ、読者のスキーマを先に起動し、読者の熟達度に合わせて手がかりを減らす」です。

### Cited Findings（各原則の根拠）
1. **要素を切り離してから相互作用させる（2段階）** — isolated-interacting elements 法、初心者で有効。 — [Pollock et al. 2002（要旨）](https://ro.uow.edu.au/edupapers/145)
2. **部品の名前と性質を先に示す（pretraining）** — [Mayer, Cambridge Handbook の章（抜粋）](https://www.cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning-segmenting-pretraining-and-modality-principles/4110A2275F6DCD02DAB1F8B37BA7E5CE)
3. **読者のペースで区切る（segmenting）** — 連続した一塊ではなく学習者のペースの区切りで提示する方が深く学ぶ。 — 同上
4. **手順のまとまりに目的のラベルを付ける（subgoal labels）** — 構造を浮き上がらせ、整理と自己説明を促す。 — [二次引用（escholarship）](https://escholarship.org/content/qt35z8842x/qt35z8842x.pdf)
5. **熟達度を素早く診断し、手がかりを段階的に減らす（first-step 診断 + fading）** — [Kalyuga 2007（一次資料を読んだ）](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)
6. **熟練者には冗長な説明を出さない（熟達化反転・冗長性）** — [Kalyuga 2007](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)
7. **名前とふるまいの不整合を外在的負荷として扱う** — 語彙の不整合は負荷を上げ、スニペット全体に及ぶ。 — [NSF PAR](https://par.nsf.gov/biblio/10090357-effect-poor-source-code-lexicon-readability-developers-cognitive-load)

### Inferences（pr-tour / pr-review への具体化。いずれも私の推論で、検証されていない）
- **(1) の具体化**: ツアーの各ステップは1つの変更単位に絞る（切り離し）。最後に「相互作用の段」を必ず置き、変更どうしの依存（A の型変更が B の呼び出しを前提にしている、など）を一枚で見せる。今の pr-tour の「コードの流れ順」は第1段階のみに相当する可能性がある。
- **(2) の具体化**: ツアーの前に、この PR で新しく出てくる型・関数・用語の一覧と一行の性質を出す。定義プレビューはこの原則の即時版。
- **(3) の具体化**: 自動で流す（動画・スライドの自動送り）より、読者が自分で次へ進む形を保つ。一過性情報効果（未検証）もこの方向を支持するはず。
- **(4) の具体化**: diff の塊ごとに「何のための変更か」を目的の言葉で付ける。手順の説明（何をしているか）ではなく目的（なぜこのまとまりがあるか）。pr-review のレビューコメントも、指摘を「サブゴール」の単位でまとめると共有メンタルモデルの単位になる。
- **(5)(6) の具体化**: 既定の説明量を「最小（ラベルと依存図だけ）」にし、展開で詳細を出す。読者の熟達度の代理として、そのファイル群への過去の関与や、ツアー冒頭の一問（first-step 型の問い）を使う。作者・常連には、慣習からの逸脱箇所だけを強調する。
- **(7) の具体化**: 理解支援の一部として、PR 内で名前とふるまいが食い違う箇所（get なのに副作用がある、など）を指摘する。説明を足すより、負荷の源を取り除く方向。
- **評価の原則**: germane load や自己報告のわかりやすさでなく、理解の結果（設計意図を後から説明できるか、見落とした欠陥の数）と時間で評価する（問4）。

### Gaps
- これらの原則は、ほぼすべて「学習（スキーマ獲得）」を目的とした研究から来ている。PR レビューの目的は学習だけでなく判断（マージしてよいか）であり、遂行時の負荷と学習時の負荷が同じ原則に従うかは、確認できた資料では示されていない。Kalyuga 2007 は熟達化反転が「学習と遂行」の両方に出ると書くが、遂行課題としてのコードレビューでの検証は見つけていない。
- チーム（複数人）での理解については、CLT の collective working memory effect（Kirschner らの協調学習の研究のはず）が関係しそうだが、**未検証**。pr-review の「共有メンタルモデル」とつなぐなら、ここを一次資料で確かめる必要がある。
