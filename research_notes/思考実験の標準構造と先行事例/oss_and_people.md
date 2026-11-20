# te の先行事例：OSS ツールと人物（構造化推論・論証マップ・対立仮説分析・AI による調査と批判）

調査日: 2026-11-21。GitHub の数値（ライセンス、最終 push・コミット、スター数）は `gh api repos/<owner>/<repo>` で同日に取得した。リポジトリ URL を出典として示す。「最終コミット」はデフォルトブランチの最新コミット日時。
te の設計の前提: `/home/ryo/ghq/github.com/ryo-morimoto/plugins/.claude/worktrees/te-design/plugins/thought-experiments/docs/te-design.md`（追記だけの出来事の列、rules.toml による段階の判定、文脈を持たない reviewer への依頼文 `te brief`、`sources.toml` の sha256 付き出典、`te check` を CI で走らせる）。

## 1. OSS の論証マップ・推論ツール（Argdown、OVA/AIFdb、Carneades、Compendium、ACH、Rationale、Kialo、DebateGraph）

### Takeaway
te にもっとも近く、いま保守されている OSS は Argdown（MIT、テキスト形式、KIT の DebateLab が資金を出している）である。Carneades、Compendium、ACH の OSS 実装は、ライセンスは開いているが、ほぼ止まっている。Rationale、bCisive、Kialo は商用、または無償のサービスで、再利用できるのは考え方だけである。

### Cited Findings
**保守されているもの**
- Argdown: 「複雑な論証のための簡単な構文」。ライセンスは MIT（コードはすべて MIT、Argvu フォントは別の自由ライセンス）。開発資金は KIT（カールスルーエ工科大学）の DebateLab。スター 1058、最終 push 2026-11-12、main の最終コミット 2026-05-20、タグの最新は `argdown-vscode@1.8.1` — [GitHub argdown/argdown](https://github.com/argdown/argdown)（README の「Credits and license」と `packages/argdown-core/package.json` の `"license": "MIT"` を確認）
- Argdown の構文: 主張は `[ ]`、論証は `< >`、賛否は入れ子のリスト。前提と結論の構造（番号付きの前提、区切り線、結論）を書け、推論の段に「Modus ponens」などのラベルを付けられる。VS Code 拡張にライブプレビュー、lint、書き出しがある — [argdown.org](https://argdown.org/)
- Argdown はリポジトリに `llms.txt` を置き、LLM 向けの文書の入口を用意している — [argdown/llms.txt](https://github.com/argdown/argdown/blob/main/llms.txt)
- OVA3（Online Visualisation of Argument analysis）: Dundee 大学の Centre for Argument Technology（ARG-tech）の論証分析ツール。最新版は共同編集、PDF への注釈、発話のタイムスタンプを追加した — [arg-tech.org](https://arg-tech.org/)。ソースは [GitHub arg-tech/OVA3](https://github.com/arg-tech/OVA3)（LICENSE ファイルなし、最終コミット 2025-05-22、スター 14）。公開版は [ova.arg-tech.org](https://ova.arg-tech.org/)
- ARG-tech の GitHub 組織には、論証の自動抽出（argument mining）の部品が多数あり、2026 年も更新されている（例: `AMF_SchemeClassifier`「推論関係を二十数種の論証スキームに分類」、`AMF_PTC_VFP`「命題を価値・事実・政策に分類」、最終 push 2026-02〜03）。ほとんどのリポジトリに LICENSE がない — [GitHub arg-tech](https://github.com/arg-tech)
- AIFdb（AIF 形式の論証データベース）のコーパスは公開されている — [corpora.aifdb.org](http://corpora.aifdb.org/)。サーバー実装と思われる [johnlawrence/AIFdb](https://github.com/johnlawrence/AIFdb) は LGPL-3.0、最終 push 2020-06-30
- Fatebook（予測の記録）は第3節

**止まっている OSS**
- Carneades 4（Go 実装）: ライセンスは Mozilla Public License 2.0（LICENSE ファイルで確認、GitHub の判定は NOASSERTION）。最終リリース v4.3（2017-07-12）、最終コミット 2024-10-15 — [GitHub carneades/carneades-4](https://github.com/carneades/carneades-4)。第3版（Clojure）は 2019-10-17 が最終 push — [GitHub carneades/carneades](https://github.com/carneades/carneades)。サイトは Thomas F. Gordon 名義（2015〜2017、文書は CC BY-SA 4.0） — [carneades.github.io](https://carneades.github.io/)
- Compendium（IBIS の道具）: 2009 年1月に GNU LGPL でソースが公開され、2012 年から CompendiumNG として共同体が保守を始めた。現在は保守されていないとされる — [Wikipedia: Compendium (software)](https://www.wikipedia.com/wiki/GIBIS)。CompendiumNG を Web アプリにする個人のフォークが 2026-11-06 に push されている（LGPL-2.1） — [GitHub swami-gait/CompendiumNG](https://github.com/swami-gait/CompendiumNG)。旧サイト compendiuminstitute.org は 2026-11-21 時点で接続できなかった
- Open Source ACH（Matthew Burton 作、コードは Joshua Knowles）: CIA で 1970 年代に作られた対立仮説分析（ACH）を複数人で行う OSS。GPL-3.0、最終コミット 2012-01-08 — [GitHub Burton/Analysis-of-Competing-Hypotheses](https://github.com/Burton/Analysis-of-Competing-Hypotheses)。この OSS が情報機関の手続きを回避して作られた経緯 — [Route Fifty (2010)](https://www.route-fifty.com/digital-government/2010/08/open-source-cuts-through-intell-communitys-red-tape/277112)
- PARC ACH 2.0: PARC が Richards J. Heuer, Jr. と共同で開発した ACH のプログラム。証拠を入力し、信頼性と関連性を評価する — [Wikipedia: Analysis of competing hypotheses](https://en.wikipedia.org/wiki/Analysis_of_competing_hypotheses)。開発者 Mark Stefik による解説 — [markstefik.com](https://www.markstefik.com/?p=702)。現在のダウンロード先は確認できなかった
- arguman.org（論証マップの Web プラットフォーム）: スター 1417、最終コミット 2021-04-27、ライセンス判定は NOASSERTION — [GitHub arguman/arguman.org](https://github.com/arguman/arguman.org)

**商用・サービス**
- Rationale（論証マップ、Austhink 発）: サイトは稼働している（タイトル「Better thinking, clearer writing」） — [rationaleonline.com](https://www.rationaleonline.com/)。Austhink の背景は Tim van Gelder のブログ — [timvangelder.com](https://timvangelder.com/category/austhink)
- bCisive（意思決定マップ）: サイトは稼働している — [bcisiveonline.com](https://www.bcisiveonline.com/)
- Kialo Edu は「無料の授業向け討論ツール」と自称している — [kialo-edu.com](https://www.kialo-edu.com/)。Kialo 本体のソースは公開されていない。第三者のディレクトリは proprietary としている — [AlternativeTo](https://alternativeto.net/software/arguman)（弱い出典）
- DebateGraph: サイトは応答する（2026-11-21） — [debategraph.org](https://debategraph.org/)。「OSS だが終了」とする第三者の記載があるが、公式の確認はできない — [AlternativeTo](https://alternativeto.net/software/arguman)

**ACH を LLM と組み合わせる新しい小さな試み（いずれもスター 1〜2、2026年）**
- [vasquezbrandon205/achix](https://github.com/vasquezbrandon205/achix)（Apache-2.0、「科学のための ACH、Heuer 流の反証による判定」、最終 push 2026-10-11）、[danielneustadter/ach-workbench](https://github.com/danielneustadter/ach-workbench)（MIT、反証による仮説の順位付け、2026-07-28）、[ApartsinProjects/EMR-ACH](https://github.com/ApartsinProjects/EMR-ACH)（LLM による地政学の予測、2026-05-25、LICENSE なし）

### Inferences
- te の記録は Argdown と同じ「テキストで書き、道具が検査し、生成物を出す」型である。te の `conclusion.premises` を Argdown の前提・結論の構造（PCS）で書き出せば、VS Code のプレビューと地図化をただで得られる。依存せず、`te render` の出力先を1つ足すだけで済む。
- ARG-tech の論証スキーム分類（Walton のスキーム）は、te の `attack` の `lenses` を選ぶ語彙に使える。スキームごとの「批判的質問」は、reviewer への依頼文の観点として、そのまま規則データにできる。
- ACH の要点（仮説×証拠の行列、確証より反証を数える）は、te の `rival` と `operation.eliminates` / `favours` で既に表せる。`fold` が「仮説ごとの不整合の数」を出せば ACH の行列になる。
- Open Source ACH が「複数人」を前提にしたのに対し、te は単独の利用者と新しい reviewer の組である。fresh reviewer は、ACH が人数で得ていた独立性を代わりに担う。

### Gaps
- Kialo、DebateGraph、Rationale、bCisive の公式ライセンスと保守状況は確認していない（公式の利用規約を取得できなかった）。
- AIFdb と OVA の正式な配布ライセンス（ARG-tech の多くのリポジトリに LICENSE がない）は未確認。
- PARC ACH 2.0 の現在の入手先は未確認。

## 2. AI による調査と批判（debate、critique、STORM、PaperQA、deep research、AI co-scientist、factored cognition、Elicit）

### Takeaway
「独立した批判者」と「対立仮説の順位付け」には研究の系譜（AI safety via debate → 説得力の高い LLM 同士の debate → AI co-scientist のトーナメント）があり、OSS の実装も多い。ただし、どれも多数のエージェントを回すサーバー型で、te の「単独・ファイル・安い fresh reviewer」とは規模が違う。te が借りるべきは仕組み（一対比較、判定者に経緯を渡さない、出典付きの回答）である。

### Cited Findings
- AI safety via debate（Irving, Christiano, Amodei, 2018）: 2つのエージェントが議論し、人間が判定する枠組み — [arXiv:1805.00899](https://arxiv.org/abs/1805.00899)
- 後続: Scalable AI Safety via Doubly-Efficient Debate（Brown-Cohen ほか） — [arXiv:2311.14125](https://www.alphaxiv.org/abs/2311.14125)、Avoiding Obfuscation with Prover-Estimator Debate — [arXiv:2506.13609](https://www.alphaxiv.org/abs/2506.13609)、debate に基づくアラインメントの安全性論証の素描（Buhl, Pfau, Hilton, Irving） — [arXiv:2505.03989](https://www.alphaxiv.org/abs/2505.03989)
- Debating with More Persuasive LLMs Leads to More Truthful Answers（Ethan Perez が最終著者の1人） — [arXiv:2402.06782](https://www.alphaxiv.org/abs/2402.06782)。コードは MIT、最終コミット 2024-03-22 — [GitHub ucl-dark/llm_debate](https://github.com/ucl-dark/llm_debate)
- 多エージェントの debate で事実性と推論を改善する（Du ほか） — [arXiv:2305.14325](https://www.alphaxiv.org/abs/2305.14325)、多エージェントの debate で発散的思考を促す（Liang ほか） — [arXiv:2305.19118](https://www.alphaxiv.org/abs/2305.19118)
- debate の OSS: MALLM（Apache-2.0、EMNLP 2025 Demo、最終 push 2026-10-10） — [GitHub Multi-Agent-LLMs/mallm](https://github.com/Multi-Agent-LLMs/mallm)。Claude Code のスキルとして複数の LLM に匿名で批判し合わせる conclave（Apache-2.0、2026-03-20） — [GitHub tommasinigiovanni/conclave](https://github.com/tommasinigiovanni/conclave)
- Towards an AI co-scientist（Google, 2025-02-26 投稿, Gemini 2.0 の多エージェント）: Ranking エージェントが一対比較と模擬討論のトーナメントで仮説を順位付けし、Elo で更新する。Elo は自動評価で独立した正解に基づかないと著者側が断っている — [arXiv:2502.18864](https://arxiv.org/abs/2502.18864v1)、[Google Research blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/?hl=da)。2026-05-19 の DeepMind のブログは Nature 掲載に触れている（中身は未確認） — [DeepMind blog](https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/)
- AI co-scientist の OSS 再実装: [llnl/open-ai-co-scientist](https://github.com/llnl/open-ai-co-scientist)（MIT、最終コミット 2026-07-10、スター 82）、[jataware/open-coscientist](https://github.com/jataware/open-coscientist)（ライセンス判定 other、2026-02-25）、[The-Swarm-Corporation/AI-CoScientist](https://github.com/The-Swarm-Corporation/AI-CoScientist)（MIT、2026-07-13）
- The AI Scientist（Sakana AI）: スター 15026、最終コミット 2025-12-19、ライセンス判定 NOASSERTION — [GitHub SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist)
- STORM（Stanford OVAL）: 主題を調べて出典付きの長い報告を生成する。MIT、最新リリース v1.1.0（2025-01-23）、最終 push 2025-09-30、スター 31915 — [GitHub stanford-oval/storm](https://github.com/stanford-oval/storm)
- PaperQA（FutureHouse）: 科学文献から出典付きで答える高精度の RAG。Apache-2.0、最新リリース v2026.08.12、最終 push 2026-11-16 — [GitHub Future-House/paper-qa](https://github.com/Future-House/paper-qa)
- open deep research（LangChain）: MIT、2026-08-10 にアーカイブ済み — [GitHub langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research)。GPT Researcher: Apache-2.0、最終コミット 2026-11-09、スター 30801 — [GitHub assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher)
- Ought の Factored Cognition: 難しい問題を、小さくほぼ文脈を持たない個々の貢献の合成で解けるかを探る — [ought.org](https://ought.org/research/factored-cognition)。その道具 ICE（Interactive Composition Explorer、合成的な LM プログラムのデバッガ）: MIT、最終 push 2026-10-05 — [GitHub oughtinc/ice](https://github.com/oughtinc/ice)
- Elicit: 学術論文の検索と、システマティックレビューに倣った調査報告の生成を行う商用サービス — [elicit.com](https://elicit.com/)
- Logikon（Gregor Betz が創業）: LLM の推論の過程を分析し採点する（AGPL-3.0、最終 push 2024-09-01） — [GitHub logikon-ai/logikon](https://github.com/logikon-ai/logikon)。「熟慮を促すプロンプト」の文献集（CC0、2025-02-03） — [GitHub logikon-ai/awesome-deliberative-prompting](https://github.com/logikon-ai/awesome-deliberative-prompting)。LLM の信念が Bayes 的に整合するかの評価（MIT、2026-10-28） — [GitHub logikon-ai/belcy-eval](https://github.com/logikon-ai/belcy-eval)

### Inferences
- te の `brief(state, lens)` は Factored Cognition の「文脈を持たない小さな貢献」と同じ発想である。ICE の「合成の各段を記録して見られる」設計は、`events.jsonl` に reviewer の入力（依頼文）と出力をそのまま残す根拠になる。
- AI co-scientist の一対比較トーナメントは、te の対立仮説（`rival` が3件以上）を段階C で順位付けする方法の候補になる。ただし著者自身が Elo は独立した正解ではないと断っているので、te では「順位」ではなく「どの仮説が残ったか」の記録にとどめるのが安全である。
- debate の研究の要点は「判定者は弱くても、対立する2者がいれば真に近づく」こと。te の fresh reviewer は批判者1人だけなので、「擁護側の応答」（`attack.objections.response`）を記録に必須にしている現在の形は debate の片側を担っている。
- STORM と PaperQA は「出典付き」を担うが、出典の sha256 のような改竄検知はしていないと推測する（未確認）。te の `te source add` の差別化点になる可能性がある。

### Gaps
- STORM、PaperQA、GPT Researcher が出典の内容を保存・照合しているか（sha256 などの来歴の検査）は確認していない。
- OpenAI と Anthropic の「critique」系の研究（例: 批判を生成するモデル）の一次資料は今回取得していない。
- LLM-as-judge の枠組みの OSS（例: 評価ライブラリ）は個別に確認していない。参考として [openai/simple-evals](https://github.com/openai/simple-evals)（MIT、最終コミット 2026-04-22）だけ確認した。

## 3. 予測の記録と採点（Metaculus、Good Judgment、Fatebook、Brier）

### Takeaway
Metaculus は本体のコードを BSD-2-Clause で公開し、いまも活発に更新している。Fatebook（MIT）は個人の予測を記録する道具で、MCP サーバーもある。te の `prediction`（`expected`、`confidence`）を結論と照合して Brier 型の採点をすれば、利用者の較正を測れる。

### Cited Findings
- Metaculus 本体: BSD-2-Clause、最終 push 2026-11-20、最新リリース v1.1（2024-12-03） — [GitHub Metaculus/metaculus](https://github.com/Metaculus/metaculus)
- Metaculus の forecasting-tools（予測ボットの道具）: MIT、最終コミット 2026-11-19 — [GitHub Metaculus/forecasting-tools](https://github.com/Metaculus/forecasting-tools)
- Fatebook: 「予測を作り追跡するもっとも速い方法」。MIT、最終コミット 2026-06-12 — [GitHub Sage-Future/fatebook](https://github.com/Sage-Future/fatebook)、[fatebook.io](https://fatebook.io/)
- Fatebook の MCP サーバー（MIT、2025-12-29） — [GitHub an1lam/fatebook-mcp](https://github.com/an1lam/fatebook-mcp)。Emacs 版（GPL-3.0） — [GitHub sonofhypnos/fatebook.el](https://github.com/sonofhypnos/fatebook.el)
- Good Judgment: サイトは自動取得を拒んだ（403） — [goodjudgment.com](https://www.goodjudgment.com/)。Tetlock は Good Judgment Project の共同リーダー — [alphaXiv: Philip E. Tetlock](https://www.alphaxiv.org/@philip-e-tetlock)

### Inferences
- te の `prediction` には確率の欄がある（`confidence`）。`close` 時に「予想が当たったか」を二値で記録すれば、実験を重ねるごとに Brier スコアを `fold` で計算できる。Fatebook の MCP に送る形にもできるが、te はファイルだけで完結させる方が設計に合う。
- Metaculus が問いの「解決条件」を厳密に書かせる慣行は、te の `frame`（問いと用語）の書き方の手本になる（推論、未確認）。

### Gaps
- Good Judgment の公開ツールや OSS の有無は確認できなかった（サイトが自動取得を拒否）。
- Brier スコアを計算する専用の小さな OSS は、信頼できるものを見つけなかった（検索で出たのはスター0の個人リポジトリだけ）。

## 4. 人物（論証理論、情報分析、思考実験の哲学、敵対的共同研究、AI debate と論証抽出）

### Takeaway
連絡先として現実的で te との距離が近いのは、Gregor Betz（KIT、Argdown の資金元 DebateLab、Logikon AI を創業、LLM の推論評価）と、論証抽出に LLM を使う Francesca Toni（Imperial）である。AI debate の系譜は Geoffrey Irving（現 Resolution）。読むべき古典は Heuer（ACH）、Walton（論証スキーム）、Gordon（Carneades）、Prakken（ASPIC+）。

### Cited Findings
**論証理論・論証技術**
- Gregor Betz: KIT の科学哲学教授、Logikon AI の創業者。論証理論、応用倫理 — [alphaXiv: Gregor Betz](https://www.alphaxiv.org/@gregor-betz)。Argdown は KIT の DebateLab が資金を出している — [GitHub argdown/argdown](https://github.com/argdown/argdown)。Argdown の例の討論の作者として名前が出る — [argdown.org](https://argdown.org/)
- Thomas F. Gordon: ポツダム大学の論証技術の名誉教授、前 Fraunhofer FOKUS — [alphaXiv: Thomas F. Gordon](https://www.alphaxiv.org/@thomas-f-gordon)。Carneades のサイトの著作権者 — [carneades.github.io](https://carneades.github.io/)
- Henry Prakken: ユトレヒト大学の AI と法の教授、計算論的論証 — [alphaXiv: Henry Prakken](https://www.alphaxiv.org/@henry-prakken)
- Francesca Toni: Imperial College London の計算論理の教授、説明可能な AI のための論証の研究講座。LLM による関係ベースの論証抽出 — [alphaXiv: Francesca Toni](https://www.alphaxiv.org/@francesca-toni)、[arXiv:2402.11243](https://www.alphaxiv.org/abs/2402.11243)
- Anthony Hunter（UCL）: 論証マップの省略三段論法を論理ベースの論証につなぐ — [arXiv:2408.08648](https://www.alphaxiv.org/abs/2408.08648)
- Iryna Gurevych（TU Darmstadt UKP Lab）、Benno Stein（Bauhaus-Universität Weimar、LLM は論証の質の注釈者として信頼できるか） — [alphaXiv の検索結果](https://www.alphaxiv.org/@iryna-gurevych)、[arXiv:2404.09696](https://www.alphaxiv.org/abs/2404.09696)
- LLM と論証抽出の総説（Manchester, Nenadic ほか） — [arXiv:2506.16383](https://www.alphaxiv.org/abs/2506.16383)
- Chris Reed: alphaXiv の名前検索は別人（Queen Mary の法学者）に解決された — [alphaXiv: chris-reed-2](https://www.alphaxiv.org/@chris-reed-2)。ARG-tech（Dundee 大学）の所在は確認した — [arg-tech.org](https://arg-tech.org/)

**情報分析**
- Richards J. Heuer, Jr.: PARC と共同で ACH のプログラムを作った。ACH は CIA で 1970 年代に作られた — [Wikipedia: Analysis of competing hypotheses](https://en.wikipedia.org/wiki/Analysis_of_competing_hypotheses)、[GitHub Burton/Analysis-of-Competing-Hypotheses](https://github.com/Burton/Analysis-of-Competing-Hypotheses)
- Matthew Burton（Open Source ACH の作者） — [GitHub Burton/Analysis-of-Competing-Hypotheses](https://github.com/Burton/Analysis-of-Competing-Hypotheses)

**敵対的共同研究・予測**
- Cory Clark と Philip Tetlock: Penn の Adversarial Collaboration Project を運営。対立する見解の研究者が共同で、両方の主張を検証する研究を設計する。2021 年開始、Clark が所長 — [Penn Today](https://penntoday.upenn.edu/news/pursuit-scientific-truth-adversarial-collaboration-Tetlock-Clark)、[APA Monitor (2025)](https://www.apa.org/monitor/2025/04-05/adversarial-research-collaboration)。振り返りの論考 — [Reflections on adversarial collaboration (PDF)](https://faculty.wharton.upenn.edu/wp-content/uploads/2026/02/Reflections_on_adversarial_collaboration.pdf)
- Philip E. Tetlock: Penn の Annenberg University Professor、Good Judgment Project の共同リーダー — [alphaXiv: Philip E. Tetlock](https://www.alphaxiv.org/@philip-e-tetlock)

**AI debate**
- Geoffrey Irving: Resolution の共同創業者・チーフサイエンティスト、英国 AI Security Institute の助言者（前チーフサイエンティスト）。AI safety via debate の筆頭著者 — [alphaXiv: Geoffrey Irving](https://www.alphaxiv.org/@geoffrey-irving)、[arXiv:1805.00899](https://arxiv.org/abs/1805.00899)
- Jonah Brown-Cohen（Google DeepMind）: debate の論文5本、うち3本が筆頭 — [alphaXiv: Jonah Brown-Cohen](https://www.alphaxiv.org/@jonah-brown-cohen)
- Ethan Perez（Anthropic の Alignment Team Lead）: 説得力の高い LLM 同士の debate — [alphaXiv の検索結果](https://www.alphaxiv.org/@ethan-perez)、[arXiv:2402.06782](https://www.alphaxiv.org/abs/2402.06782)

### Inferences
- te の目的（単独の利用者が AI と思考実験を回し、独立した批判を受ける）に一番近い研究者は Gregor Betz である。Argdown（テキスト形式の論証）、DebateLab（討論の構造）、Logikon（LLM の推論の採点、belcy-eval の信念の整合性）と、te の3つの要素（記録の形式、批判、検査）すべてに接点がある。最初の連絡先の候補。
- Adversarial Collaboration Project の「対立する側が事前に、何が出たら自分が間違いと認めるかを決める」型は、te の `prediction` と `holder`（実在の立場か藁人形か）の組と同じ形である（推論）。
- Irving の debate の安全性論証（arXiv:2505.03989）は、「独立した reviewer が1人いれば十分か」を考えるときの理論的な参照になる。

### Gaps
- Chris Reed（ARG-tech）の現在の所属と役職は、一次資料で確認できなかった（alphaXiv は別人に解決し、Dundee 大学の個人ページは取得できなかった）。一般知識では ARG-tech の所長だが、未確認。
- Douglas Walton、Randolph Pherson、James Robert Brown、John Norton、Michael Stuart（思考実験の哲学）は、今回のツール呼び出しで所属や著作を確認していない。いずれも実在する研究者・実務家だが、出典 URL を付けられないため、ここでは未確認として扱う（Walton は論証スキーム、Pherson は構造化分析技法、Brown・Norton・Stuart は思考実験の認識論の文献で知られる）。
- 各人物への連絡の可否（受け入れ姿勢、連絡先）は調べていない。
