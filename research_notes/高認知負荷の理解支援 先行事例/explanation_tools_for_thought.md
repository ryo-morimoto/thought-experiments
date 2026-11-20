# Explorable explanations・moldable development・malleable software・tools for thought の作り手が、複雑なシステムと変更を理解可能にすることについて言っていること

調査日: 2026-11-21。対象は pr-tour（PR の変更ファイルをコードの流れの順に、実 diff と定義プレビュー付きで案内する HTML）や pr-review（レビューコメントを通じてチームの共有メンタルモデルを育てる）のような仕組みを作る開発者。一次資料を WebFetch で読んだもののみ「確認済み」とし、引用は短く「」で区別して直後に URL を置く。読めなかったもの・記憶に基づくものは各節の Gaps に「未確認」と明記する。

## 問1: 誰が重要人物で、それぞれの作品と資産（知見・失敗からの洞察・意図）は何か

### Takeaway
系譜は「見えないものを見せる（データ・実行・状態）」(Victor, Guo, Edwards) と「問いごとに安く道具を作る」(Gîrba/feenk, Litt/Ink & Switch) と「読者が持ち帰れる媒体を作る」(Matuschak/Nielsen) の三つの流れに分かれる。成功例（Python Tutor）は範囲を極端に絞った一方、野心的な一般化（Subtext、Distill、literate programming）は作り手・書き手のコストで止まった。

### Cited Findings

**人物一覧（今回一次資料を読んだ人）**
- Bret Victor — Learnable Programming（2012）、Up and Down the Ladder of Abstraction、Explorable Explanations（2011, 2024 年に追記）、Dynamicland。
- Tudor Gîrba / feenk — moldable development、Glamorous Toolkit、Simon Wardley との共著 *Rewilding Software Engineering*。
- Geoffrey Litt, Josh Horowitz, Peter van Hardenberg, Todd Matthews（Ink & Switch）— "Malleable Software"（2025 年 6 月）。Litt 単独の "Malleable software in the age of LLMs"（2023 年 3 月）。
- Andy Matuschak & Michael Nielsen — "How can we develop transformative tools for thought?"（2019 年 10 月）、Quantum Country（mnemonic medium）。Matuschak の working notes。
- Philip Guo — Python Tutor。UIST 2021 の振り返り論文。
- Jonathan Edwards — Subtext（2004〜2020 の連作）。2025 年 9 月の振り返り。
- Kartik Agaram — "Literate programming: Knuth is doing it wrong"（2014）。
- Nicky Case — explorable explanations の設計パターン（2014）。
- Chris Olah ほか Distill 編集部 — Distill の休止告知（2021）。

**Bret Victor**
- Learnable Programming の原則は、環境側が「make meaning transparent」「follow the flow」「see the state」「show the data」「show comparisons」「create by reacting」「create by abstracting」を担うこと — [Learnable Programming](https://worrydream.com/LearnableProgramming/)
- 「If a programmer cannot see what a program is doing, she can't understand it.」 — [Learnable Programming](https://worrydream.com/LearnableProgramming/)
- 「Visualize data, not code.」／「We understand data by comparing it to other data.」 — [Learnable Programming](https://worrydream.com/LearnableProgramming/)
- 頭の中でのシミュレーションを否定している。「Working in the head doesn't scale.」 — [Learnable Programming](https://worrydream.com/LearnableProgramming/)
- 拒否したもの: 機能そのもの（「The features are not the point.」）、単独機能としてのライブコーディング（「live coding, as a standalone feature, misses the point.」）、見えない状態（「All state must be eliminated or shown.」） — [Learnable Programming](https://worrydream.com/LearnableProgramming/)
- Ladder of Abstraction: 独立変数を直接操作できるようにし、変数全体にわたって抽象化した図を作り、そこから具体的な一例へ降りる。「when creating abstractions, stepping down is as important as stepping up.」「the deepest insights are born — not at any one level of abstraction, but in the transitions between them」 — [Up and Down the Ladder of Abstraction](https://worrydream.com/LadderOfAbstraction/)
- Explorable Explanations（2011）は reactive documents、explorable examples、contextual information の三つを提案した。インタラクションは別の砂場に置かず、説明の中に織り込むべきとしている。2024 年の追記は「The reader's role is not to believe, but to critically evaluate, rebut, and come to a broad understanding.」 — [Explorable Explanations](https://worrydream.com/ExplorableExplanations/)
- Dynamicland は「a computer that is a place, where people work together in the real world」であり、「this technology cannot be a product, but must be a form of education and community practice.」と製品化を拒否している。「The lab itself is the experiment.」 — [dynamicland.org](https://dynamicland.org/)

**Tudor Gîrba / feenk（moldable development）**
- 定義は「a way of programming through contextual micro tools built for each problem」。原則として「There is no single dominant representation of anything in software」「Software should be explainable when we need it」、ソフトウェア工学は「primarily a decision making activity」 — [moldabledevelopment.com](https://moldabledevelopment.com/)
- literate programming との違い: literate programming はコードに結びついた一本の物語だが、moldable development はシステムのどの部分にも複数の物語を与える（FAQ の要旨） — [moldabledevelopment.com](https://moldabledevelopment.com/)
- 「Multiple studies reveal that typically more than half of the development time is being devoted to reading.」「Reading the code once is rarely sufficient to get an idea of the system.」 — [InfoQ, Gîrba 2022-09-27](https://www.infoq.com/articles/moldable-development/)
- 汎用ツールを拒否している。「generic tools never really work in practice.」 一方で道具は安くあるべきで、「a custom view is often a matter of minutes to create.」「often, these tools are only used once.」 — [InfoQ](https://www.infoq.com/articles/moldable-development/)
- 自ら認めるコスト: 「Moldable Development requires new technology that makes the creation of custom tools as inexpensive as possible.」「At first sight, the proposition can perhaps appear as a waste.」 効果の定量的な証拠は記事に示されていない — [InfoQ](https://www.infoq.com/articles/moldable-development/)
- 採用には新しいスキルが要り、ファシリテーターが文脈に応じた道具を作り、関係者がそれを使う。組織の変化も要るとしている（要旨） — [moldabledevelopment.com](https://moldabledevelopment.com/)

**Geoffrey Litt / Ink & Switch（malleable software）**
- 設計原則: ユーザーから作り手への gentle slope、アプリではなく道具、使っている場所で直せる in-place toolchain、必要になったときだけプログラムできるメディアエディタ、共同での制作 — [Malleable Software (Ink & Switch, 2025)](https://www.inkandswitch.com/essay/malleable-software/)
- 既存手段の失敗理由: 設定は「Settings only offer controls that the application developers have thought to expose.」、プラグインは「can only edit an app's behavior in specific authorized ways.」、OSS は「Modifying a serious open source codebase usually requires significant expertise and effort.」 — [Malleable Software](https://www.inkandswitch.com/essay/malleable-software/)
- 試作から得た教訓: PushPin（UI とデータを分けると別のビューは足しやすいが、埋め込みとコンポーネント間の協調が難しい）、Patchwork（気軽に使えるバージョン管理と環境内での道具作りが自分たちの仕事を支えたが、コードのブランチと共有ツールのガバナンスは未解決）、Potluck/Embark（非形式データと構造化データの均衡が難しい） — [Malleable Software](https://www.inkandswitch.com/essay/malleable-software/)
- AI について: AI によるコード生成は「does not address all the barriers to malleability」。道具の合成、データの共有、ユーザーによる精密な制御は残る — [Malleable Software](https://www.inkandswitch.com/essay/malleable-software/)
- チャットの限界: 「Chat is an essentially limited interaction mode, regardless of the quality of the bot.」 LLM は「a junior developer who is very fast at typing」に例えられ、初心者ほど誤りに気づかない。ユーザーの構造的な理解が LLM の出力を「audit」する助けになる — [Litt 2023](https://www.geoffreylitt.com/2023/03/25/llm-end-user-programming)

**Andy Matuschak & Michael Nielsen**
- 「the most powerful tools for thought express deep insights into the underlying subject matter.」 insight-through-making のループを提案している。「many tools for thought are public goods.」なので経済的に作られにくい — [How can we develop transformative tools for thought?](https://numinous.productions/ttft/)
- 自分たちの結果の一部を撤回している。「appears to be based on an error in our data analysis, and is now retracted.」 また「Isn't this 'just' an essay with flashcards embedded?」という批判には、ある水準では正しいと認めている — [ttft](https://numinous.productions/ttft/)
- 伝達のための動的表現は、読者が考える環境になりにくい。「one doesn't walk away from the article with the dynamic environment in one's pocket.」 記事末尾の砂場は「rarely leads to anything interesting.」 — [Most dynamic representations developed for communication aren't very enabling](https://notes.andymatuschak.org/zB5wf5crA1jVZb6CycZSjGRTjSkw2BpsdjG)
- （検索結果の要約による。原ツイートは未読）2020 年のスレッドで、explorable な記事は表現が単独で成り立つほど深くないため一回限りに感じられ、他の作者も影響に確信がないと私的に語ったとしている — [threadreaderapp](https://threadreaderapp.com/thread/1305264244045225984)

**Philip Guo（Python Tutor）**
- 10 の指針: Walk-up-and-use（インストールもアカウントも不要）、Should 'Just Work'、Sharing, Not Hosting、Minimize User Options、Be Stateless、Use Old Technologies、Minimize Dependencies、Single Developer、Start Specific、Ignore Most Users — [Guo, UIST 2021](https://par.nsf.gov/servlets/purl/10309256)
- 範囲の定義: 板書を真似る道具であり、「If your code can't fit on a blackboard or a single presentation slide, it's probably too long to visualize effectively in Python Tutor.」 — [Guo 2021](https://par.nsf.gov/servlets/purl/10309256)
- 自前のインタプリタで式単位のステップ実行を試したが、公式実装と細部が合わず、エラーメッセージが教材と食い違うため本番品質の公式インタプリタ・デバッガの拡張に切り替えた（表現力より「just works」を優先） — [Guo 2021](https://par.nsf.gov/servlets/purl/10309256)
- 共有は URL（コード・オプション・表示中のステップを埋め込む）で行い、ユーザー生成コンテンツはホストしない。URL は Stack Overflow、GitHub Issues、Slack などに貼られて広まった — [Guo 2021](https://par.nsf.gov/servlets/purl/10309256)
- 断った要望: 本格的な Web IDE、大規模な本番コードの視覚的デバッグ、LMS 機能、ギャラリー。「lean harder on that expertise to maintain your singularity of vision!」 — [Guo 2021](https://par.nsf.gov/servlets/purl/10309256)
- 「trying to be too general actually hinders scale and sustainability.」 — [Matuschak のノートによる Guo 2021 の抜粋](https://notes.andymatuschak.org/zVxPT5mYfnUZBWxMYSaTf7H)

**Jonathan Edwards（Subtext）**
- Example-Centric Programming（2004）は実行トレースを展開できるアウトラインで見せ、そこに付けた注釈を例からテストに変えた。Subtext 1 では実行トレースそのものをプログラムにした — [Subtext Retrospective (2025-09)](https://www.subtext-lang.org/retrospective.html)
- 失敗の原因は一度に多くを発明しようとしたことで、問題が絡み合った「tar pits」に次々はまった。glitch のない状態変更は実務家から作為的と見られ、React のようなライブラリ水準の解が採られた。Subtext 7 は関数型にしたため抽象の溝が広がり、Subtext 8 で具体性のため命令型へ戻った。Chorus（2016）のプログラミング体験は概ね失敗した（要旨） — [Subtext Retrospective](https://www.subtext-lang.org/retrospective.html)

**Kartik Agaram（literate programming の批評）**
- literate programming は組版を重視しすぎて構成を軽んじ、抽象の層を飛び越える。組版された PDF は「dead」で、手を入れて試せない。「a signalling device」として称賛されているが、互いの literate program は読まれていないと疑う — [Agaram 2014](https://akkartik.name/post/literate-programming)
- 代案: 提示の順序を読者のために設計し、文章は最小限にする（「Comments are like code: the less you write, the less there is to go bad.」）。機能を自己完結した層に分け、テストをコードと混ぜ、一部の層だけをビルドして「poke at it and run what-if experiments」 — [Agaram 2014](https://akkartik.name/post/literate-programming)

**Nicky Case**
- パターン: Do, Show, and Tell（インタラクションは効くところだけで使い、文章・図・アニメーションと併用する）、start small build big、cognitive gates（「by withholding an explanation, the explorable explanation can be more effective.」）、author-guided, player-driven — [Case 2014](https://blog.ncase.me/explorable-explanations/)
- Earth: A Primer では読者が読み飛ばして混乱したため、内容のゲートを加えた — [Case 2014](https://blog.ncase.me/explorable-explanations/)

### Inferences
- pr-tour は Victor の言う「follow the flow」（コードの流れの順）と「contextual information」（定義プレビュー）を実装しているが、「show the data」（実行時の値）と「show comparisons」（変更前後の振る舞いの比較）は持っていない。系譜からいちばん欠けて見えるのはここ。
- Gîrba の「a custom view is often a matter of minutes」「only used once」は、LLM が一回限りの説明ビューを作るコストを下げた今、PR ごとの使い捨てビューを正当化する根拠になりうる。ただし feenk 自身は効果の定量的な証拠を示していない。

### Gaps
- 未確認（今回は一次資料を読んでいない）: Maggie Appleton（AI インターフェース、digital garden）、Amelia Wattenberger、Omar Rizwan、Cyrus Omar（Hazel）、Hillel Wayne、Mike Bostock/Observable（Observable 2.0 の告知は HTTP 429 で取得できず）、Knuth の原論文、Peter van Hardenberg 単独の文章。
- Glamorous Toolkit の採用障壁を feenk 自身がまとめた振り返りは見つからなかった。検索で出たのは講演とインタビューだけ。
- Dynamicland のトップページには教訓も Oakland の拠点の扱いも書かれていない。進捗報告（2014–2022）は未読。

## 問2: 何が失敗し、放棄され、なぜか

### Takeaway
失敗の原因は「作るコスト」「一般化しすぎ」「読者が持ち帰れない」の三つにまとまる。どれも説明一本あたりの作者の労力と、説明が一回限りで終わることに関わる。

### Cited Findings
- **Distill の休止（2021-07-02）**: 「the primary bottleneck is the amount of effort it takes to produce these articles」。ボランティア編集者が燃え尽き、メンタリングは「overwhelming」だった。結論は「the future for most types of articles is probably self-publication」 — [Distill Hiatus](https://distill.pub/2021/distill-hiatus/)
- **伝達用の explorable は思考の道具にならない**: 作者の主張のために作られた環境は、読者が持ち帰って使えない。PhET のようなアプレットは「too shallow for serious thought」かつ「too complex to communicate anything without narrative」 — [Matuschak note](https://notes.andymatuschak.org/zB5wf5crA1jVZb6CycZSjGRTjSkw2BpsdjG)
- **literate programming の不採用**: 組版を重視して構成を軽んじたこと、top-down に main から始める思考、PDF が試せない「dead」な成果物であること — [Agaram 2014](https://akkartik.name/post/literate-programming)
- **Subtext**: 一度に発明しすぎて tar pit にはまった。新しいパラダイムとして採用を得られなかった。抽象の溝を広げた版（7）は後退だった — [Subtext Retrospective](https://www.subtext-lang.org/retrospective.html)
- **Python Tutor 自身の放棄**: 式単位のステップ実行のための自前インタプリタを放棄した。大規模コードの可視化は範囲外として断った — [Guo 2021](https://par.nsf.gov/servlets/purl/10309256)
- **Quantum Country**: データ分析の誤りによる主張の撤回。何を覚えるべきかを選ぶのは「not trivial」 — [ttft](https://numinous.productions/ttft/)
- **既存の拡張機構**: 設定・プラグイン・mod・OSS は、作り手が想定した範囲でしか変えられないか、変えるのに専門性が要る — [Malleable Software](https://www.inkandswitch.com/essay/malleable-software/)
- **Earth: A Primer**: 読み飛ばしで混乱が起きたため、内容のゲートを加えた — [Case 2014](https://blog.ncase.me/explorable-explanations/)
- **moldable development の未証明**: 道具作りは「waste」に見えうると認め、定量的な効果は示していない — [InfoQ](https://www.infoq.com/articles/moldable-development/)

### Inferences
- PR の説明は一回読まれて終わるので、Distill 型の手作りの説明は一本あたりのコストに見合わない。Python Tutor 型の「手作業ゼロで生成し、URL で共有する」形のほうが続きやすい。
- 大きな diff は Python Tutor の「黒板に収まる」制約を最初から超えている。全体を一枚で見せるより、ladder of abstraction のように全体図と具体例を行き来させるほうが系譜に沿う。

### Gaps
- 未確認: Victor が 2024 年に各エッセイへ付けた追記で、画面上の explorable からの方針転換（Dynamicland へ移った理由）を自ら述べているか。Explorable Explanations の追記の一部しか確認できていない。
- 未確認: Dynamicland の Oakland の拠点を閉じたことの事実関係と理由。
- 未確認: Observable が notebook から Framework（ローカルのファイルと git）へ舵を切った理由。記憶では「notebook は探索向きで、保守されるダッシュボードやバージョン管理には向かない」趣旨だが、一次資料を読めていない。

## 問3: この系譜は、説明を誰が書くべきか（変更の作者・レビュアー・ツール・AI）、一回限りか再利用かについて何を言っているか

### Takeaway
系譜は「環境（ツール）が意味を透明にする責任を負う」(Victor) と「問いを持つ人が、その場で安い道具を作る」(Gîrba, Litt) を支持する。作者が書いた一本の物語（literate programming、伝達用の explorable）は、作者の動機に染まり、持ち帰れないとして批判されている。AI は道具を作るコストを下げるが、理解や監査を置き換えるものとしては扱われていない。

### Cited Findings
- 責任は環境側にある: 「The environment is responsible for making meaning transparent.」 — [Learnable Programming](https://worrydream.com/LearnableProgramming/)
- 作者が書いた環境は作者の動機に染まる。Matuschak のノート「Authored environments are significantly colored by authors' motivations」と「Powerful enabling environments usually arise as a byproduct of projects pursuing their own intrinsically meaningful purposes」（リンク先の題名のみ確認） — [Matuschak note](https://notes.andymatuschak.org/zB5wf5crA1jVZb6CycZSjGRTjSkw2BpsdjG)
- 一本の物語より複数の物語: moldable development は literate programming と違い、システムのどの部分にも複数の物語を与える — [moldabledevelopment.com](https://moldabledevelopment.com/)
- 一回限りを容認: 「often, these tools are only used once.」 ただし作るコストが十分低いことが前提 — [InfoQ](https://www.infoq.com/articles/moldable-development/)
- 作るのは「facilitators」、使うのは関係者という役割分担 — [moldabledevelopment.com](https://moldabledevelopment.com/)
- 読者の役割は信じることではなく、批判的に評価し反論すること — [Explorable Explanations (2024 追記)](https://worrydream.com/ExplorableExplanations/)
- AI: 単独では malleability の障壁を解かない。malleable な環境と組み合わせたときに速くなる — [Malleable Software](https://www.inkandswitch.com/essay/malleable-software/)。チャットより直接操作。ユーザーの理解が LLM の出力を監査し、依存は減っていくのが望ましい — [Litt 2023](https://www.geoffreylitt.com/2023/03/25/llm-end-user-programming)
- 共有は URL でホストしない: 説明の状態（コード、ステップ）を URL に入れ、議論の場（Issues、Slack）に貼らせる — [Guo 2021](https://par.nsf.gov/servlets/purl/10309256)

### Inferences
- PR では、変更の作者が書く説明は「作者の主張を通すための伝達用の表現」になりやすい（Matuschak の批判がそのまま当てはまる）。レビュアーが自分の問いから引き出せるビューのほうが「enabling」に近い。pr-tour は作者側の伝達物で、pr-review は読み手の理解を共有知にする側なので、両者は系譜上の二つの役割に対応する。
- 一回限りの説明（PR ごと）は Gîrba の論理では作るコストが低ければ正当だが、説明は再利用できない。再利用できるのは説明を作る「道具」や「ビューの型」のほう（例: データ構造ごとのビュー、変更の種類ごとの見せ方）。説明は使い捨てにし、ビューの型を蓄積する、という分け方が系譜に沿う。
- AI が説明を書く場合も、Litt の議論からは「読者が自分で確かめられる経路（実 diff、実行値、定義）を一緒に出す」ことが条件になる。pr-tour が要約ではなく実 diff を見せている点はこれと合う。

### Gaps
- 「変更の作者 vs レビュアー」のどちらが PR の説明を書くべきかを直接論じた一次資料は、この系譜の中には見つからなかった。上の対応づけは推論。
- Maggie Appleton の AI インターフェース論（記憶では、LLM の出力を読者が検証できる形で見せる議論がある）は未確認。

## 問4: PR／コード理解の仕組みの設計原則の候補

### Takeaway
「データと実行を見せる」「抽象と具体を行き来させる」「問いごとの安いビュー」「範囲を極端に絞る」「状態を URL で共有する」「読者が反論できる形にする」の六つが、系譜から導ける候補。

### Cited Findings（各候補の根拠）
- **P1 コードではなくデータと振る舞いを見せる**: 変更前後で何が計算されるか、どの状態が変わるか。根拠: 「Visualize data, not code.」「All state must be eliminated or shown.」 — [Learnable Programming](https://worrydream.com/LearnableProgramming/)。Edwards の materialized execution と example-centric programming — [Subtext Retrospective](https://www.subtext-lang.org/retrospective.html)
- **P2 比較を見せる**: 「We understand data by comparing it to other data.」 — [Learnable Programming](https://worrydream.com/LearnableProgramming/)。diff は比較の一種だが、値や振る舞いの比較ではない
- **P3 抽象と具体を行き来させる**: 全体図（変更の地図）と一例（具体的な呼び出し・値）を往復させる。「stepping down is as important as stepping up」 — [Ladder of Abstraction](https://worrydream.com/LadderOfAbstraction/)
- **P4 一つの正しい表現はない。問いごとに安いビューを作る**: 「There is no single dominant representation」 — [moldabledevelopment.com](https://moldabledevelopment.com/)、「a matter of minutes」 — [InfoQ](https://www.infoq.com/articles/moldable-development/)
- **P5 範囲を絞り、walk-up-and-use にする**: インストールなし、オプションを最小にし、「黒板に収まる」範囲に限る。要望の多くを断る — [Guo 2021](https://par.nsf.gov/servlets/purl/10309256)
- **P6 状態ごと URL で共有し、議論の場に貼らせる**: 表示中のステップまで URL に入れる — [Guo 2021](https://par.nsf.gov/servlets/purl/10309256)
- **P7 読む順序を読者のために設計し、文章は最小にする**: 「the less you write, the less there is to go bad.」 — [Agaram 2014](https://akkartik.name/post/literate-programming)。ただし main から top-down に始めることは批判されている
- **P8 読者が前提を動かし、反論できるようにする**: reactive documents と 2024 追記の「critically evaluate, rebut」 — [Explorable Explanations](https://worrydream.com/ExplorableExplanations/)
- **P9 説明を読み飛ばすと壊れる箇所にはゲートを置く**: cognitive gates — [Case 2014](https://blog.ncase.me/explorable-explanations/)
- **P10 AI は道具を作る係で、理解の代わりではない**: チャットより直接操作。出力を監査できる構造を保つ — [Litt 2023](https://www.geoffreylitt.com/2023/03/25/llm-end-user-programming)、[Malleable Software](https://www.inkandswitch.com/essay/malleable-software/)
- **P11 一度に発明しすぎない**: [Subtext Retrospective](https://www.subtext-lang.org/retrospective.html)、「trying to be too general actually hinders scale and sustainability」 — [Guo 2021（Matuschak の抜粋）](https://notes.andymatuschak.org/zVxPT5mYfnUZBWxMYSaTf7H)

### Inferences
- pr-tour への具体化の例: (a) 変更された関数ごとに、テストやサンプル入力で変更前後の値を並べる（P1, P2）。(b) 冒頭に変更の地図を置き、各ステップから地図へ戻れるようにする（P3）。(c) URL のハッシュに現在のステップを入れる（P6）。(d) 「この PR で変わる振る舞いはこれだけ」という作者の主張を、読者が反例で突けるようにする（P8）。
- pr-review への具体化の例: レビューコメントで生じた問いを「次回から自動で出すビューの型」に昇格させる。これは Gîrba の「使い捨ての道具」と Matuschak の「持ち帰れる環境」を両立させる道で、チームの共有メンタルモデルが道具として蓄積される。
- 反対方向のリスク: P4（ビューを増やす）は P5（範囲を絞る）と衝突する。Python Tutor の成功は P5 側、moldable development は P4 側で、後者の普及の証拠は乏しい。

### Gaps
- これらの原則が PR レビューの理解度を実際に上げるかを測った研究は、この調査の範囲（作り手の文章）では見つかっていない。コードレビュー研究（別の調査範囲）との突き合わせが要る。
- 未確認: Cyrus Omar の Hazel（穴のあるプログラムでも常に型と値を出す live programming）が「不完全な変更の途中状態を見せる」原則の根拠になりうるか。一次資料を読んでいない。
