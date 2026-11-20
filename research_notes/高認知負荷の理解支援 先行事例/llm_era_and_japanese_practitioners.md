# LLM 時代のコード・変更の説明支援：人物・資産・失敗・設計原則（含む日本語圏の実務者）

調査日: 2026-11-21。一次資料を読めたものと、検索結果の要約（二次）しか読めていないものを区別する。「（二次）」と付けたものは、本文を直接読んでいない。引用は短く「」で示し、直後に URL を置く。

---

## 問い1: AI 生成の PR 要約・コード説明・レビューコメントが、人の理解とレビュー結果に与える効果を誰が測ったか

### Takeaway
測定された効果は「処理量・マージ率・解決率」には正、「人の理解・レビューの網羅性・自信」には中立〜負という形で揃っている。とくに Tufano ら（AI レビューを出発点にするとレビュアーが指摘箇所しか見なくなる）と Shen & Tamkin（AI 利用群は理解テストが低い）が、pr-tour / pr-review の設計に直接効く反証側の根拠になる。

### Cited Findings

**人物と主要な仕事（研究者・産業研究）**

- **Tao Xiao, Hideaki Hata（畑秀明）, Christoph Treude, Kenichi Matsumoto（松本健一）** — "Generative AI for Pull Request Descriptions: Adoption, Impact, and Developer Interventions"（FSE 2024, PACMSE, DOI 10.1145/3643773）。Copilot for PRs で説明文の一部が生成された PR 18,256 件を分析。NAIST 系の日本の研究者が著者に入っている。 — [arXiv 2402.08967](https://arxiv.org/abs/2402.08967); [FSE 2024 ページ](https://2024.esec-fse.org/details/fse-2024-research-papers/105/Generative-AI-for-Pull-Request-Descriptions-Adoption-Impact-and-Developer-Interven)
  - 結果: 生成説明付き PR はレビュー時間が短く、マージされやすい。開発者は生成文に自分の記述を足すことが多い（abstract より）。 — [arXiv 2402.08967](https://arxiv.org/abs/2402.08967)
  - 注意: 測っているのはレビュー時間とマージ確率で、レビュアーの理解ではない。

- **Rosalia Tufano, Gabriele Bavota ら（USI）** — "Deep Learning-based Code Reviews: A Paradigm Shift or a Double-Edged Sword?"。29 人の専門家が品質問題を仕込んだ 6 プロジェクトで計 72 回レビュー。手動 / ChatGPT Plus 生成レビューを出発点 / 生成レビューの指摘を全部既知とする条件の 3 群。 — [arXiv 2411.11401](https://arxiv.org/abs/2411.11401v3)（二次: 検索結果の要約から）
  - 結果: LLM が見つけた問題の多くはレビュアーに妥当と判断された。一方で、生成レビューを出発点にすると、レビュアーは生成レビューが指摘した箇所に集中した。時間短縮にも自信の向上にもならなかった。 — [arXiv 2411.11401](https://arxiv.org/html/2411.11401v3)（二次）
  - 後続: Crupi, Tufano, Bavota（2026）は、AI レビューは手動点検の「後の追加チェック」としての方がよく働くと報告。 — [arXiv 2602.11925](https://arxiv.org/abs/2602.11925)（二次）。同論文は人間のコメント 739 件と ChatGPT 出力を比べ、ChatGPT はコード変更を約 2.4 倍多く勧めるが、人間が報告した品質問題の 10% しか見つけないとする。 — [arXiv 2602.11925](https://arxiv.org/html/2602.11925v1)（二次）

- **Judy Hanwen Shen, Alex Tamkin（Anthropic）** — "How AI Impacts Skill Formation"（2026-01-29）。52 人（主に若手）の RCT。未経験の非同期ライブラリ Trio を学ぶ課題。 — [Anthropic research](https://www.anthropic.com/research/AI-assistance-coding-skills); [arXiv 2601.20245](https://arxiv.org/abs/2601.20245)（二次: 検索結果の要約から）
  - 結果: AI 利用群の事後クイズ平均 50%、手書き群 67%。完了時間の差は有意でない。差が最大だったのはデバッグの設問。概念的な追加質問や説明を求めた参加者はスコアが高かった（相関）。 — [Anthropic research](https://www.anthropic.com/research/AI-assistance-coding-skills)（二次）
  - 著者の結論として「AI-enhanced productivity is not a shortcut to competence」と報じられている。 — [InfoQ](https://www.infoq.com/news/2026/02/ai-coding-skill-formation)（二次）
  - 限界: 小標本、1 ライブラリ、「新しいライブラリの学習」を測っていて一般的なプログラミング能力ではないという批判がある（同上、二次）。

- **Daye Nam, Andrew Macvean, Vincent Hellendoorn, Bogdan Vasilescu, Brad Myers（CMU / Google）** — "Using an LLM to Help With Code Understanding"（ICSE 2024）。IDE 内プラグイン GILT（GPT-3.5-turbo、選択コードの説明・API 呼び出しの説明などのプリセット要求でプロンプト不要）を 32 人で Web 検索と比較。 — [arXiv 2307.08177](https://arxiv.org/abs/2307.08177v3); [ICSE 2024](https://conf.researchr.org/details/icse-2024/icse-2024-research-track/187/Using-an-LLM-to-Help-With-Code-Understanding)（二次: 検索結果の要約から）
  - 結果: Web 検索より理解課題の達成を助けたが、効果は経験によって異なり、学生と実務者で使い方・評価が違った。著者は「プロンプト不要の IDE 内対話」を有望とする。（二次）

- **Alexander Frömmgen, Jacob Austin, Peter Choy, Nimesh Ghelani ほか（Google）** — "Resolving Code Review Comments with Machine Learning"（ICSE-SEIP 2024）。レビュアーのコメントに対して ML が修正案を出す。 — [Google Research pub](https://research.google/pubs/resolving-code-review-comments-with-machine-learning/); [Google Research blog 2023-05](https://research.google/blog/resolving-code-review-comments-with-ml/)
  - 数値: オフライン評価で精度 50% 目標時に 52% のコメントに対応（blog）。展開後はレビュアーコメントの約 7.5% に対応（論文 PDF）／約 5%（ICSE ページ）。 — [Google Research blog](https://research.google/blog/resolving-code-review-comments-with-ml/); [ICSE ページ](https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-in-practice/35/Resolving-Code-Review-Comments-with-Machine-Learning)（二次。5% と 7.5% は資料間で食い違っている。時期の違いと推測されるが未確認）
  - 注意: 測っているのは「コメントの解決（修正）」で、理解ではない。

- **Umut Cihan ほか（Bilkent 大学 + 産業パートナー）** — "Automated Code Review In Practice"（ICSE-SEIP 2025）。Qodo PR Agent ベースの bot を 238 人・10 プロジェクトに導入し、3 プロジェクト 4,335 PR（うち 1,568 が自動レビュー）を分析。 — [arXiv 2412.18531](https://arxiv.org/abs/2412.18531)（二次: 検索結果の要約から）
  - 結果: bot コメントの 73.8% が受け入れ・実装された。品質は「わずかに改善」と多くが回答。一方、PR のクローズ時間は平均 5h52m → 8h20m に増加（プロジェクト別では 1 つは短縮、2 つは増加）。誤ったレビュー・不要な修正・無関係なコメントという欠点が報告された。（二次）

- **Kla Tantithamthavorn（Monash / Atlassian）ほか** — "RovoDev Code Reviewer: A Large-Scale Online Evaluation of LLM-based Code Review Automation at Atlassian"（ICSE 2026）。1,900 超のリポジトリで 1 年間に 54,000 超のコメント。 — [arXiv 2601.01129](https://arxiv.org/abs/2601.01129v2); [ICSE 2026 SEIP](https://conf.researchr.org/details/icse-2026/icse-2026-software-engineering-in-practice/2/RovoDev-Code-Reviewer-A-Large-Scale-Online-Evaluation-of-LLM-based-Code-Review-Autom)（二次）
  - 結果: LLM コメントのコード解決率 38.70%、人間のコメント 44.45%（相対 12.9% 低い）。生成器のほかに「事実の正しさ」でコメントを落とす品質チェック（LLM-as-judge）を置く。採否は人間のレビュアーが決めると Atlassian blog は述べる。 — [Atlassian blog](https://www.atlassian.com/blog/artificial-intelligence/developer-productivity-improved-with-rovo-dev)（二次。blog の「PR サイクルタイム 30.8% 短縮」は論文で未確認）

- **Saul Goldman, Hong Yi Lin, Jirat Pasuksmit, Patanamon Thongtanunam, Kla Tantithamthavorn ほか 14 名** — "What Types of Code Review Comments Do Developers Most Frequently Resolve?"（ASE 2025）。LLM-as-a-Judge で 5 分類。 — [arXiv 2510.05450](https://arxiv.org/abs/2510.05450)
  - 結果（abstract）: 可読性・バグ・保守性のコメントは、コード設計のコメントより解決率が高い。LLM と人間のレビュアーはプロジェクト文脈によって強み・弱みが異なる。LLM コメントのかなりの部分が実際に解決される。 — [arXiv 2510.05450](https://arxiv.org/abs/2510.05450)
  - Thongtanunam（メルボルン大学。NAIST の Matsumoto 研出身で、日本の研究グループとの共著が多い）が LLM レビューの産業評価に関わっている点が、問いの人物リストと接続する。所属・経歴は今回一次確認していない。

- **Meta**: "AI-Assisted Fixes to Code Review Comments at Scale"（arXiv 2507.13499, 2025-07）が Google の仕事の後続として存在。 — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499)（中身は未読）

### Inferences
- 産業研究の大半は「コメントが解決されたか」「マージされたか」「時間」を成果変数にしており、**レビュアーやチームが変更を理解したか**を測った産業研究は見つからなかった。理解を測ったのは Nam ら（課題達成）と Shen & Tamkin（事後クイズ）の実験研究だけで、どちらもレビューではなく「書く・学ぶ」場面。PR の説明・ツアーがレビュアーの理解に与える効果は、ほぼ未測定の領域と推論する。
- Tufano らのアンカリング（生成レビューが指摘した箇所に注意が集中する）は、pr-tour が「読む順番」を決めること自体が同じ種類の注意誘導になりうることを示唆する。順番に乗らなかった箇所が読まれなくなるリスク。
- Cihan らの「受け入れ率 73.8% なのにクローズ時間は伸びる」は、AI コメントへの対応コストが人間側に乗ることを示す。pr-review の「エージェントが下書き、人間が判断」は、下書きの量が判断の負荷を上げうる。
- RovoDev の「事実の正しさでコメントを落とす」段は、幻覚コメントの抑制を独立した評価器で行う設計例（pr-review の evaluator と同型）。

### Gaps
- Google の AutoCommenter（ベストプラクティス違反を指摘する LLM レビュー、Vijayvergiya ら 2024 と記憶）は今回検索・確認していない。
- Microsoft の AI 支援コードレビュー（社内展開の研究）、JetBrains Research の研究は今回確認できなかった。
- CHI/CSCW 系の「AI 説明への過信（overtrust）」をコードレビューで測った研究は今回見つけられていない。
- Tufano ら・Cihan ら・Nam ら・Shen & Tamkin の本文は直接読んでおらず、数値は検索要約経由。最終報告で使う前に本文確認が必要。

---

## 問い2: 実務者の発言と「comprehension debt / cognitive debt」の系譜

### Takeaway
「comprehension debt」は Jason Gorman（Codemanship, 2025-09）発、Addy Osmani（2026-03）が普及、「cognitive debt」は Margaret-Anne Storey（2026-02, Naur の「理論としてのプログラム」に依拠）が整理し Simon Willison が「最良の説明」と紹介、という系譜が二次資料ではほぼ一致する。ただし Gorman の原文は読めていない。

### Cited Findings
- **Margaret-Anne Storey**（ビクトリア大学、ソフトウェア工学研究者） — blog "Cognitive debt"（2026-02-09）。認知負債を、速く進むチームに溜まる共有理解の喪失とし、コードではなく開発者の頭の中にあるものとする。Peter Naur の「プログラムは開発者の頭の中の理論」に依拠。 — [margaretstorey.com](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)
  - 事例: 起業コースの学生チームが 7〜8 週目に簡単な変更もできなくなり、最初は技術的負債を疑ったが、実際は設計判断の理由や部品のつながりを誰も説明できなかった。 — 同上
  - 対策: 「velocity without understanding is not sustainable」、「at least one human on the team fully understands each AI-generated change before it ships」、変更の「何」だけでなく「なぜ」を記録、コードレビュー・ふりかえり・知識共有を共有理解の再構築の場とする、ペアプロ・リファクタリング・TDD、兆候（変更をためらう、口伝への依存、ブラックボックス感）を観察。 — [margaretstorey.com](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)
  - 「intent debt」や「Cognitive Tours」というツールの話は LinkedIn の二次要約にのみあり、このブログ記事本文には出てこない。 — [LinkedIn（二次）](https://lk.linkedin.com/in/murshidazher)
- **Simon Willison** — Storey の記事を「the best explanation of the term cognitive debt I've seen so far」と紹介（2026-02-15）。 — [simonwillison.net](https://simonwillison.net/2026/Feb/15/cognitive-debt)（二次: 検索要約経由）
- **Simon Willison** — "Your job is to deliver code you have proven to work"（2025-12-18）。証明は手動テストと自動テストの 2 段で、省くとレビュー負担がメンテナに移る。LLM が生成した大きなパッチ単体には価値が乏しく、PR にテストの証拠を含めるべきとする。 — [simonwillison.net](https://simonwillison.net/2025/Dec/18/code-proven-to-work)（二次: 検索要約経由）
- **Addy Osmani** — blog "Comprehension debt"（2026-03-14）。定義「Comprehension debt is the growing gap between how much code exists in your system」…（and how much of it any human genuinely understands）。「Making code cheap to generate doesn’t make understanding cheap to skip.」「What used to be a quality gate is now a throughput problem.」 — [addyosmani.com](https://addyosmani.com/blog/comprehension-debt/)
  - 主張: コードはきれいでテストも通るので誤った自信を生む／速度・DORA・カバレッジは理解を測らない／「テストが通った」と「何をなぜするか分かっている」を区別せよ／深いシステム文脈を持つ人をレビュー役に置け／AI を出力生成でなく質問・トレードオフ探索に使え。 — 同上
  - Anthropic の RCT を「17% lower」（50% vs 67%）と引用。これはパーセントポイント差であり、相対差（約 25%）ではない点に注意。 — 同上; [Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills)
  - 出典名なしで「委任した開発者は理解テスト 40% 未満、概念的な質問に使った開発者は 65% 超」とも書く（出典不明、未検証）。 — 同上
- **Jason Gorman（Codemanship）** — 2025-09-30 の投稿で「comprehension debt」を「the extra time it takes to understand code so that we can change it without breaking it」と定義したとされる。 — [graphify blog（二次）](https://graphify.com/blog/comprehension-debt); arXiv 2604.13277 も Gorman を導入者とする（二次） — [arXiv 2604.13277](https://arxiv.org/html/2604.13277)。原文は未取得。
- MIT Media Lab の "Your Brain on ChatGPT: Accumulation of Cognitive Debt"（Kosmyna ら, 2025）が「cognitive debt」の語の別系統として Osmani と @IT 記事に引かれている。 — [addyosmani.com](https://addyosmani.com/blog/comprehension-debt/); [@IT](https://atmarkit.itmedia.co.jp/ait/spv/2603/12/news016.html)（論文本体は未読）
- **Thoughtworks** は Storey の見方を「技術的負債より大きなリスクになりうる」と要約。 — [Thoughtworks blog](https://www.thoughtworks.com/insights/blog/generative-ai/cognitive-debt-real-organizational-risk)（二次）

### Inferences
- Storey の「出荷前に少なくとも 1 人の人間が各 AI 生成変更を完全に理解する」は、pr-review の「人間が判断」と目的が一致するが、より強い（理解の所在を人に固定する）条件。pr-review のゴール「チームの共有メンタルモデル」は、Storey の「共有理論の喪失」をちょうど反転させたものとして位置づけられる。
- Osmani の「品質ゲートからスループットの問題へ」は、レビューの説明支援ツールが「速く通す」方向に最適化されると負債を加速させる、という警告として読める。

### Gaps
- Kent Beck、Birgitta Böckeler（martinfowler.com）、Charity Majors、Hillel Wayne の AI とレビュー/理解についての一次資料は、今回の検索予算内で確認できなかった。@IT 記事は Martin Fowler の「Fragments」に認知負債のメモがあるとするが未確認。
- Jason Gorman の原文（Codemanship blog, 2025-09-30）未取得。

---

## 問い3: 日本語圏の実務者・研究者（コードリーディング、レビュー、理解）

### Takeaway
日本の研究者では NAIST 松本研系（畑秀明・松本健一、および同研出身の Thongtanunam）が LLM と PR/レビューの実証研究に直接関わっている。実務側では 2026 年に「理解負債・認知負債」が @IT で紹介され、AI 生成コードのレビュー負担を示す国内調査（レビュアーの 86.3% が負担増、49.5% が「作成者本人が説明できなかった」経験）が出ている。和田卓人の「レビュー解体」は一次資料未確認。

### Cited Findings
- **畑秀明・松本健一（NAIST 系）** — 上記 Xiao ら FSE 2024 の共著者。 — [arXiv 2402.08967](https://arxiv.org/abs/2402.08967)
- **Patanamon Thongtanunam** — 上記 ASE 2025 の共著者（Atlassian の LLM レビューコメント解決研究）。 — [arXiv 2510.05450](https://arxiv.org/abs/2510.05450)
- **国内調査（キッカケクリエイションズ、IDEATECH のリサーチサービス利用、2026-02-24〜27、レビューを行う IT エンジニア 322 人、うち AI 生成コードのレビュー経験者 277 人）**: 負担が「大いに増えた」30.0%＋「やや増えた」56.3%＝86.3%。最多の経験は「作成者本人がコードの内容を説明できなかった」49.5%、「動作するが理由が分からないコード」33.6%。6 カ月以内に AI 生成コード由来のバグを経験 78.6%。 — [@IT 2026-06-16](https://atmarkit.itmedia.co.jp/ait/spv/2606/16/news041.html)（ページの文字化けで数値の読み取り誤りの可能性あり。調査会社のプレスリリース原本は未確認）
- **@IT「Deep Insider Brief」（2026-03-12）**: 技術負債に続く「理解負債」「認知負債」を紹介。出典として Codemanship、Storey、Martin Fowler の Fragments、Simon Willison、MIT Media Lab を挙げる。 — [@IT](https://atmarkit.itmedia.co.jp/ait/spv/2603/12/news016.html)（本文の一部が文字化けで読めず。著者名未確認）
- **KINTO テクノロジーズ（Developers Summit 2025 KANSAI）**: AI が書く冗長なコードがレビュー工数を増やす構造を分析し、AI の説明能力で要約を作ってコミュニケーションコストを下げる手法を提案。事例として、複雑な修正がレビューを経て 1 行になり、原因は「コードの意図・背景への理解不足」とされた。 — [CodeZine 22314](https://codezine.jp/article/detail/22314)（二次: 検索要約経由。登壇者名未確認）
- **CodeRabbit 中津川氏の登壇**: AI によるコード量増加でシニアエンジニアのレビュー負担が急増。 — [CodeZine 23536](https://codezine.jp/article/detail/23536)（二次）
- **CodeRabbit 日本語ガイド**: 「作者は変更を理解している」という従来のレビューの前提が AI 生成 PR では成り立たない。 — [CodeRabbit](https://www.coderabbit.ai/ja/guides/code-explainability-for-ai-generated-prs-a-reviewers-guide)（二次）
- **kenimo49（Zenn）**: レビューを層に分け、設計（責務分割・API 境界・「このパターンを増やすべきか」）は人間が主に担う。「AI が指摘しなかった部分こそ人間が念入りに見る」。レビュー方針を review.md に書き AI ツールにも読ませる。 — [Zenn: 6 stages](https://zenn.dev/kenimo49/articles/code-review-6-stages-ai-human-boundary); [Zenn: 3 layer](https://zenn.dev/kenimo49/articles/code-review-3layer-model-design)（二次）
- **atama plus**: エージェント由来の PR 増でレビュー待ちが詰まり、影響範囲が小さく品質に問題ない PR は人間のレビューなしでマージする仕組みを検討。「すべてのPRに人間がレビューコメントをつける従来のフローでは明らかにスケールしません。」 — [Zenn atama plus](https://zenn.dev/atamaplus/articles/resolve-review-bottleneck)（二次）
- **和田卓人（t_wada）**: 「TDD in AI era」資料で、人が書くと遅いが制御・状況把握が高く、AI に委託すると速いが制御・状況把握が下がりレビューが課題になる、と整理したとされる。 — [Speaker Deck](https://speakerdeck.com/twada/tdd-in-ai-era-202604-edition)（二次）。「レビュー解体」は AI 生成の要約記事でしか確認できず、未検証。 — [st-hakky](https://book.st-hakky.com/news/ai-code-review-human-verification-t-wada)
- **『プログラマー脳』（Felienne Hermans 著、水野貴明・水野いずみ訳、秀和システム、2023-02、ISBN 4798068535）**: 認知科学からコードの読解を扱い、混乱の 3 種（知識不足・情報不足・処理能力不足）、コードの臭いや悪い命名が認知負荷を上げる理由を論じる。 — [紀伊國屋書店](https://www.kinokuniya.co.jp/f/dsg-01-9784798068534)（二次）

### Inferences
- 国内調査の「作成者本人が説明できない」49.5% は、PR の説明を AI が作る仕組みが、作者自身の理解の欠落を覆い隠す方向にも働きうることを示す。説明の生成元が「作者の理解」なのか「diff の再記述」なのかを区別する必要がある。
- 日本語圏の実務記事は「どこを人間が見るか」（層分け・リスクでの振り分け）を中心に論じており、「人間が理解したかをどう確かめるか」を扱ったものは見つからなかった。

### Gaps
- JJUG、PHPerKaigi、Regional Scrum Gathering Tokyo、YAPC でのコードリーディング・レビュー理解の登壇は、今回の予算内で個別に確認できなかった。
- 畑秀明の現所属（信州大学と記憶）、Raula Gaikovina Kula の LLM×レビュー研究は未確認。
- 日本語のコードリーディング書籍（例: 『ルールズ・オブ・プログラミング』訳書など）の著者・訳者の AI 時代の発言は未調査。

---

## 問い4: 人が「承認するだけ」でなく実際に理解し続けるための設計原則（候補）

### Takeaway
以下は上の知見からの推論（Claude の推論であり、ユーザーの判断ではない）。いずれも PR 説明・ツアーの効果が「理解」で測られた証拠は乏しく、仮説として扱う。

### Cited Findings
- 生成レビューを出発点にすると指摘箇所に注意が集中し、時間も自信も改善しない。 — [Tufano ら arXiv 2411.11401](https://arxiv.org/html/2411.11401v3)（二次）
- AI レビューは手動点検の後の追加チェックとして有効。 — [Crupi ら arXiv 2602.11925](https://arxiv.org/abs/2602.11925)（二次）
- 説明や概念的な質問を求める使い方は理解テストの得点と関連し、受け身の委任は低い。 — [Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills)（二次）
- 「なぜ」を記録し、レビューを共有理解の再構築の場にし、各 AI 生成変更を少なくとも 1 人が完全に理解する。 — [Storey](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)
- 事実の正しさを別の評価器で確かめてからコメントを出す。 — [RovoDev arXiv 2601.01129](https://arxiv.org/abs/2601.01129v2)（二次）
- 動作の証拠（手動・自動テスト）を PR に含める。 — [Willison](https://simonwillison.net/2025/Dec/18/code-proven-to-work)（二次）

### Inferences（設計原則の候補）
1. **人の先読みを先に、AI の説明を後に。** 人間が先に変更を読み（または予想を書き）、そのあとで AI の説明・指摘を見せる。アンカリング（Tufano）を避ける。pr-tour なら、ツアー順を見せる前に「この PR で何が変わると思うか」を一行書かせる、などの選択肢。
2. **ツアーの外側を明示する。** 生成された順番・要約が触れなかったファイルや箇所を一覧で出し、「ここは説明していない」と言う。注意誘導の副作用への対策。
3. **説明を「質問を返す形」に寄せる。** 説明を渡すより、レビュアーに問い（なぜこの境界か、何が壊れうるか）を出す方が、Anthropic の結果（概念的質問をした群が高得点）と整合する。
4. **「なぜ」は作者から取る。** AI が diff から推測した rationale は幻覚の rationale になりうる。作者が書いた意図・ADR・議論へのリンクを優先し、推測した部分は推測と表示する（国内調査の「作成者本人が説明できない」49.5% への対策）。
5. **理解の所在を記録する。** Storey の「少なくとも 1 人が完全に理解」を運用するなら、誰が理解したか（承認者 ≠ 理解者もありうる）を残す。pr-review の「チームの共有メンタルモデル」をコメント単位で蓄積する目的と合う。
6. **事実確認を独立の段にする。** 生成した説明・コメントを別の評価器で根拠（パーマリンク・テスト）と照合し、通らないものは出さない（RovoDev、pr-review の evaluator）。
7. **成果変数を「解決率・時間」だけにしない。** 先行研究のほとんどは解決率・マージ・時間で効果を測っており、理解は測っていない。自前の評価には、レビュー後の事後質問（変更の意図・影響範囲を答えられるか）を入れる。

### Gaps
- 上の原則を PR レビューで実験的に検証した研究は見つからなかった。とくに「PR ツアー（読む順番の提示）」がレビュアーの理解・欠陥発見に与える効果の測定は未発見。
- 過信（overtrust）の定量研究（AI の説明が誤っているときにレビュアーが見抜く率）は今回見つけられなかった。

---

## 未検証の一覧（まとめ）
- Jason Gorman による「comprehension debt」の初出（2025-09-30）— 二次資料のみ。
- Storey の「intent debt」「Cognitive Tours」— LinkedIn 二次要約のみ。ブログ本文には無い。
- Osmani の「委任群 40% 未満 / 概念質問群 65% 超」— 出典不明。
- Google ML コメント解決の 5% と 7.5% の食い違い。
- Atlassian の「PR サイクルタイム 30.8% 短縮」— blog のみ。
- 和田卓人「レビュー解体」— AI 生成要約記事のみ。
- Tufano ら、Cihan ら、Nam ら、Shen & Tamkin、Crupi ら、RovoDev の数値 — 検索要約経由で、本文未読。
- Kent Beck、Birgitta Böckeler、Charity Majors、Hillel Wayne、Google AutoCommenter、Microsoft・JetBrains の研究 — 未調査。
