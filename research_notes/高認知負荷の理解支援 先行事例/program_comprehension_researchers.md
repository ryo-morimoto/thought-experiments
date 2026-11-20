# プログラム理解・コードレビュー理解の研究者と、その資産（知識・洞察・意図）

調査日: 2026-11-21。対象: pr-tour（変更ファイルをコードの流れ順に辿る HTML ガイド）や pr-review（レビューコメントでチームの共有メンタルモデルを育てるプラグイン）のような「高い内在的認知負荷の成果物を理解しやすくする仕組み」を作る人のための、人起点の先行研究調査。

凡例:
- 「知識」= 測られた・観察された事実、「洞察」= 作り手が失敗や観察から学んだこと、「意図」= なぜそう作ったか／何を捨てたか。
- 引用は英語原文のまま短く「> 」で示し、直後に出典 URL を置く（DATA_POLICY の限定的な引用として扱う）。
- 一次資料（論文 PDF 本文）を読んで確かめたものと、要旨・二次資料のみのものを区別し、後者は「（要旨のみ）」「（二次資料）」と書く。

---

## 問い1: 最も関係の深い人物は誰か（10〜20人）

### Takeaway
中心は Alberto Bacchelli（チューリッヒ大学 ZEST）を軸にした共著ネットワークで、Baum（変更部分の順序と作業記憶）、Fregnan（ファイル位置の効果）、Wurzel Gonçalves（レビュー理解モデル・認知負荷）、Spadini（テストの扱い・既存コメントの効果）、Pascarella（情報ニーズ）、di Biase（変更の分解）がそこから出ている。もう一つの軸は Microsoft Research（Bird, Barnett, DeLine, Venolia, Begel）で、Bacchelli & Bird 2013、ClusterChanges、Ko/LaToza の情報ニーズ研究がここに繋がる。認知そのもの（作業記憶・負荷の測定）は Crichton、Siegmund、Fritz、Hermans が担う。

### Cited Findings

人物一覧（所属は原則として該当論文に記載された当時のもの。現所属は未検証）

<!-- data-source: original（各論文の書誌情報から筆者が作った人物一覧） -->
| 人物 | 所属（出典での記載） | なぜ重要か | 代表的な仕事 |
|---|---|---|---|
| Tobias Baum | Leibniz Universität Hannover（論文記載時） | 変更部分をどの順で見せるべきかの理論を作り、それを実験で検証して「効果は確認できなかった」と報告した。pr-tour の設計に最も直結 | On the Optimal Order of Reading Source Code Changes for Review (ICSME 2017) — [PDF](https://tobiasbaum.github.io/rp/optimalordering.pdf)。Associating Working Memory Capacity and Code Change Ordering with Code Review Performance (EMSE) — [PDF](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)。博士論文（認知支援レビューツール、CoRT）— [DNB](https://nbn-resolving.org/urn:nbn:de:101:1-2020021115194615374977) |
| Alberto Bacchelli | University of Zurich, ZEST（2018 年の論文記載時） / 2013 年は University of Lugano | 「レビューの核心は理解」という発見の起点。以後の共著網のハブ | Expectations, Outcomes, and Challenges of Modern Code Review (ICSE 2013) — [PDF](https://sback.it/publications/icse2013.pdf) |
| Christian Bird | Microsoft Research（2013 記載時） | 上記 2013 論文の共著者、ClusterChanges の共著者 | 同上、ClusterChanges (ICSE 2015) — [MSR](https://www.microsoft.com/en-us/research/publication/helping-developers-help-themselves-automatic-decomposition-of-code-review-changesets/) |
| Enrico Fregnan | （Bacchelli 研究室、共著より） | 表示順（ファイル位置）がレビュー結果を変えることを大規模データと実験で示した | First Come First Served: The Impact of File Position on Code Review (ESEC/FSE 2022) — [arXiv](https://arxiv.org/abs/2208.04259) |
| Pavlína Wurzel Gonçalves | （Bacchelli 研究室、共著より） | レビュー中の理解過程をプログラム理解理論（Letovsky）で説明する CRCM を提案。チェックリストと認知負荷の実験 | Code Review Comprehension (arXiv 2025) — [arXiv](https://arxiv.org/html/2503.21455v1)。Do explicit review strategies improve code review performance? (EMSE 2022) — [Springer](https://link.springer.com/10.1007/s10664-022-10123-8) |
| Davide Spadini | TU Delft（リポジトリより） | テストコードのレビュー、テストを先に読む（TDR）、既存コメントの効果 | Test-Driven Code Review (ICSE 2019) — [TU Delft](https://repository.tudelft.nl/record/uuid:b275d9ed-47b7-432a-8d22-4e1456a9ff7c)。Primers or Reminders? (ICSE 2020) — [TU Delft](https://repository.tudelft.nl/record/uuid:e9e6a336-d5d8-4167-8c3d-d5aaf6598da6) |
| Luca Pascarella | TU Delft（リポジトリより） | レビュアーの質問を情報ニーズの代理指標として分類 | Information Needs in Contemporary Code Review (CSCW 2018) — [TU Delft](https://research.tudelft.nl/en/publications/information-needs-in-contemporary-code-review) |
| Martín di Biase | （TU Delft / Bacchelli と共著） | 混ざった変更を分けると何が変わるかを統制実験で測った | The effects of change decomposition on code review (PeerJ CS 2019) — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7924728/) |
| Margaret-Anne Storey | （所属未検証） | 1990 年代に「メンタルモデル構築を支える認知的設計要素」を体系化。現在も CRCM やテストレビュー研究の共著者 | Cognitive design elements to support the construction of a mental model during software exploration (JSS 1999) — [dblp（前身 IWPC 1997）](https://dblp.org/rec/conf/iwpc/StoreyFM97) |
| Mike Barnett / Shuvendu Lahiri | Microsoft Research（MSR ページより） | 変更セットの自動分解（定義と使用で束ねる）を作り、Office の開発者で評価 | ClusterChanges (ICSE 2015) — [MSR](https://www.microsoft.com/en-us/research/publication/helping-developers-help-themselves-automatic-decomposition-of-code-review-changesets/) |
| Yida Tao / Sunghun Kim | HKUST（PDF のホストより） | 複合変更の頻度と分割手法、産業界での「変更理解」の調査 | Partitioning Composite Code Changes (MSR 2015) — [PDF](https://hunkim.cse.ust.hk/papers/tao-msr2015.pdf)。How do software engineers understand code changes? (FSE 2012) — [MSR](https://www.microsoft.com/en-us/research/publication/how-do-software-engineers-understand-code-changes-an-exploratory-study-in-industry/) |
| Caitlin Sadowski | Google（論文記載時） | Google の大規模ログで「小さい変更・単一レビュアー」の実態を示した。Tricorder で「レビュー時に出す情報の誤検知を極端に絞る」方針 | Modern Code Review: A Case Study at Google (ICSE SEIP 2018) — [Google Research](https://research.google/pubs/modern-code-review-a-case-study-at-google/)。Tricorder (ICSE 2015) — [PDF](https://www.cs.umd.edu/class/spring2019/cmsc414/papers/tricorder-building-a-program-analysis-ecosystem.pdf) |
| Will Crichton | Brown（CEL のページより） | 作業記憶の限界をプログラム追跡で測り、その結果からツール（Flowistry Focus Mode）を作って評価し、限界も報告 | The Role of Working Memory in Program Tracing (CHI 2021) — [arXiv](https://arxiv.org/abs/2101.06305)。博士論文 — [PDF](https://willcrichton.net/assets/pdf/dissertation.pdf) |
| Andrew J. Ko | CMU（2007 記載時） | 開発者の情報ニーズ 21 種を現場観察で分類。最も満たされにくいのは設計意図 | Information Needs in Collocated Software Development Teams (ICSE 2007) — [PDF](https://faculty.washington.edu/ajko/papers/Ko2007InformationNeeds.pdf) |
| Thomas D. LaToza | （2006 は Microsoft Research との共同研究） | 暗黙知（メンタルモデル）は文書でなく会話とコードで共有されることを示した | Maintaining Mental Models (ICSE 2006) — [MSR](https://www.microsoft.com/en-us/research/?p=154508) |
| Robert DeLine / Gina Venolia | Microsoft Research | 上記 Ko 2007 と LaToza 2006 の共著者 | 同上 |
| Jonathan Sillito / Gail C. Murphy | （UBC、ライブラリ記録より） | 変更作業中に開発者が問う 44 種の質問。Murphy は Mylyn（タスク文脈）も | Asking and Answering Questions during a Programming Change Task (TSE 2008) — [UBC](https://open.library.ubc.ca/collections/831/items/1.0052042)。Using task context to improve programmer productivity (FSE 2006, Kersten & Murphy) — [bibtex](https://bibtex.github.io/FSE-2006-KerstenM.html) |
| Janet Siegmund | （Saarland 系サイトにホスト） | プログラム理解を fMRI などで測る方法論。理解に要する時間は 30 年変わらないと指摘 | Program Comprehension: Past, Present, and Future (FoSE 2016) — [PDF](https://www.se.cs.uni-saarland.de/publications/docs/FoSE16.pdf)。fMRI 研究 (2014) — [PDF](https://www.se.cs.uni-saarland.de/publications/docs/SKA+14.pdf) |
| Thomas Fritz / Andrew Begel | UZH / Microsoft Research（論文記載時） | 生体信号で理解課題の難しさを予測 | Using Psycho-Physiological Measures to Assess Task Difficulty in Software Development (ICSE 2014) — [MSR](https://www.microsoft.com/en-us/research/?p=166326) |
| Chris Parnin | （Georgia Tech、2011 記載時：未検証） | 「自動デバッグは本当に人を助けているか」で、ツールの暗黙の前提が人の行動と合わないことを示した | Are Automated Debugging Techniques Actually Helping Programmers? (ISSTA 2011) — [PDF](https://web.eecs.umich.edu/~weimerw/2018-481/readings/debugging-helping.pdf) |
| Titus Barik | （所属未検証） | 開発者がエラーメッセージを実際に読むか、読むのがどれだけ難しいかを視線計測 | Do Developers Read Compiler Error Messages? (ICSE 2017) — [preprint](https://jssmith1.github.io/assets/pdf/ICSE_2017_EYE.pdf) |
| Austin Z. Henley | （所属未検証） | コードナビゲーション UI（Patchworks）を作り比較評価。研究試作が製品化されなかった経緯をブログで語る | The Patchworks Code Editor (CHI 2014) — [PDF](https://austinhenley.com/pubs/Henley2014CHI_Patchworks.pdf)。Toward Principles for the Design of Navigation Affordances (CHI 2017) — [PDF](https://austinhenley.com/pubs/Henley2017CHI_CodeEditors.pdf) |
| Felienne Hermans | Leiden（出版物ページより） | 認知科学（短期記憶・チャンク・認知負荷の種類）を開発者向けに翻訳した | The Programmer's Brain (Manning 2021) — [Leiden](https://universiteitleiden.nl/en/research/research-output/science/the-programmers-brain) |
| Emma Söderberg / Lo Gullstrand Heander | Lund（学位論文ホストより） | レビューを「意思決定」としてモデル化（CRDM）。完全自動化が知識共有を失わせると警告 | Code Review as Decision-Making (arXiv 2025) — [arXiv](https://arxiv.org/abs/2507.09637) |
| Md Shamimur Rahman / Zadia Codabux / Chanchal K. Roy | University of Saskatchewan | 1,355 人調査でアルファベット順の不満を定量化（2026） | Breaking the Alphabet (ICSE 2026) — [researchr](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/310/Breaking-the-Alphabet-Rethinking-File-Ordering-in-Code-Review) |
| Abir Bouraffa / Carolin Brandt / Andy Zaidman / Walid Maalej | TU Delft ほか | GitHub 上で実際にレビュアーがどの順に読んでいるかを採掘（2025） | Not One to Rule Them All (EASE 2025) — [TU Delft](https://repository.tudelft.nl/record/uuid:523eb4a8-a52c-4ef7-ab23-3a3601a5d978) |
| Vladimir Kovalenko ほか | JetBrains（IntelliJ IDEA のレビュー過程を対象） | 産業プロジェクトでファイル順の効果を再確認 | Assessing the Impact of File Ordering Strategies on Code Review Process (EASE 2023 industry / arXiv) — [arXiv](https://arxiv.org/abs/2306.06956) |

共著網の確認（論文の著者欄から確認したもの）
- Baum の順序理論の論文の共著者は Kurt Schneider と Alberto Bacchelli — [PDF](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)。
- CRCM 論文の著者は Wurzel Gonçalves, Rani, Storey, Spinellis, Bacchelli — [arXiv](https://arxiv.org/html/2503.21455v1)。Storey と Bacchelli の系統がここで合流している。
- TDR 論文 (ICSE 2019) は Spadini, Palomba, Baum, Hanenberg, Bruntink, Bacchelli — [検索結果に基づく、TU Delft](https://repository.tudelft.nl/record/uuid:b275d9ed-47b7-432a-8d22-4e1456a9ff7c)。
- 「When Testing Meets Code Review」(ICSE 2018) は Spadini, Aniche, Storey, Bruntink, Bacchelli — [researchr](https://conf.researchr.org/details/icse-2018/icse-2018-Technical-Papers/55/When-Testing-Meets-Code-Review-Why-and-How-Developers-Review-Tests)。
- Barik 2017 の著者に Emerson Murphy-Hill と Chris Parnin が入っている — [DBLP](https://dblp.dagstuhl.de/rec/conf/icse/BarikSLHFMP17.html)。
- Ko 2007 は Ko, DeLine, Venolia。LaToza 2006 は LaToza, Venolia, DeLine — [Ko PDF](https://faculty.washington.edu/ajko/papers/Ko2007InformationNeeds.pdf), [MSR](https://www.microsoft.com/en-us/research/?p=154508)。
- Fritz 2014 は Fritz, Begel, Müller, Yigit-Elliott, Züger — [MSR](https://www.microsoft.com/en-us/research/?p=166326)。

### Inferences
- pr-tour に最も近いのは Baum（順序）→ Fregnan（位置効果）→ Bouraffa/Rahman（2025–26 の実地データ）の線。pr-review（共有メンタルモデル）に最も近いのは Bacchelli & Bird（理解と知識移転）→ LaToza/Ko（暗黙知は会話で流れる）→ Wurzel Gonçalves の CRCM（仕様・実装・注釈の 3 層モデル）→ Söderberg（自動化で知識共有を失う警告）の線。
- 「認知負荷を下げれば成績が上がる」という前提を、作った本人たち（Baum, Gonçalves）が実験で確かめきれていない点が、この分野で最も価値のある資産だと考える。

### Gaps
- 指示にあった Brad Myers、Amy Ko の近年の仕事、Thomas LaToza の近年の仕事（プログラミング戦略など）、Emerson Murphy-Hill / Ciera Jaspan の Google 開発者生産性研究、Chris Parnin の割り込み・展望記憶研究は、今回の時間内に一次資料を読めていない。
- ICPC / CHASE / VL/HCC / PLATEAU の運営者・招待講演者の名簿は確認していない（人選の網羅性は未検証）。
- 各人の現所属は確認していない。

---

## 問い2: 各仕事から取り出せる資産（知識・洞察・意図）

### Takeaway
測られた事実として強いのは (1) レビューの最大の課題は「変更の理解」で、特に「なぜ変えたか」、(2) 表示順は注意の配分を変え、後ろのファイルほど見落とされる、(3) 作業記憶は約 7 項目で、遠く離れた（delocalized）欠陥の発見にだけ効く、(4) 変更を分けても欠陥発見数は増えなかったが誤指摘は減った、の 4 点。作り手の意図として強いのは Baum の「関連する変更部分をまとめよ。まとめ方の規則はレビュアーに見えるようにせよ」。

### Cited Findings

#### Bacchelli & Bird, Expectations, Outcomes, and Challenges of Modern Code Review (ICSE 2013) — 本文 PDF を読んだ
- 知識: Microsoft の 16 チームで 17 人を観察・面接し、570 件のコメントを分類し、管理者 165 人と開発者 873 人に調査した — [PDF](https://sback.it/publications/icse2013.pdf)
- 知識: 動機の 1 位は欠陥発見だが、実際の成果は欠陥より知識移転・チームの認知・代替解の発見などに広がる — [PDF](https://sback.it/publications/icse2013.pdf)
- 知識: 面接で最もはっきり現れた課題は変更の理解だった。引用:
  > "the most difficult thing when doing a code review is understanding the reason of the change"
  — [PDF](https://sback.it/publications/icse2013.pdf)
- 知識: 慣れないファイルのレビューは時間がかかると答えたのは 798 人（91%）— [PDF](https://sback.it/publications/icse2013.pdf)
- 知識: レビュアーは理解のために説明文を読む、コードを動かす、メールする、20〜40% の頻度で対面で作者に聞く。当時のツールは差分・行コメント・構文強調しか提供していない — [PDF](https://sback.it/publications/icse2013.pdf)
- 洞察: 作者が文脈と方向づけを与えるとレビュアーはよりよく速く応答できる、と開発者が述べた — [PDF](https://sback.it/publications/icse2013.pdf)

#### Baum, Schneider, Bacchelli, On the Optimal Order of Reading Source Code Changes for Review (ICSME 2017) — 本文 PDF を読んだ
- 知識（方法）: 産業界の 292 のツールでのレビューセッションのログ、専門開発者 12 人の課題つき面接、関連分野の文献、201 人のレビュアーへの課題つき調査を組み合わせた — [PDF](https://tobiasbaum.github.io/rp/optimalordering.pdf)
- 知識: ログでは 53% のセッションでツールが最初に示したファイルから読み始めた（=ツールの順序がそのまま読む順序になりやすい）— [PDF](https://tobiasbaum.github.io/rp/optimalordering.pdf)（該当箇所の数値は抽出テキストから読み取ったもの。文脈の全文確認は未了）
- 意図（6 原則）— [PDF](https://tobiasbaum.github.io/rp/optimalordering.pdf):
  1. 関連する変更部分をできるだけ近くにまとめる（> "Group related change parts as closely as possible."）
  2. 必要になる前に情報を与える（> "Provide information before it is needed."）
  3. 1 と 2 が衝突したらまとめる方を優先する
  4. 密接に関連する変更部分はチャンクとして扱い、それ単位で並べる
  5. 最も近い距離は「同時に画面に見えている」こと
  6. レビュアーが理解できる規則で並べ、まとめ方を明示する（> "making the grouping explicit to the reviewer."）
- 知識: 調査で、呼び出し関係について bottom-up（呼ばれる側から）を好んだのは 130 人中 111 人（85%）。面接では top-down を好む人も多く、方向は主観的 — [PDF](https://tobiasbaum.github.io/rp/optimalordering.pdf)
- 知識: 「関連」の種類として、データフロー、呼び出し、クラス階層、宣言と使用、ファイル順、類似、論理的依存、開発の流れ の 8 種が挙がった — [PDF](https://tobiasbaum.github.io/rp/optimalordering.pdf)
- 洞察: 最初に要求（変更のきっかけ）と全体像を知りたい、テストケースなどの使用例が助けになる。その後の入り方は人により、(T1) 易しいところ、(T2) 自然な入口（GUI・Servlet・CLI）、(T3) 最重要部分、(T4) 新しいもの、(T5) 浮いている部分。終わりは全体のまとめか、重要でない残り — [PDF](https://tobiasbaum.github.io/rp/optimalordering.pdf)
- 洞察: 理解できない順序は思考の流れを壊す。面接の引用:
  > "If the parts had been grouped, the groups made visible and ideally given sensible names, I would have been"（文の途中まで）
  — [PDF](https://tobiasbaum.github.io/rp/optimalordering.pdf)
- 意図: 大きなハンクはメソッド単位などに分けた方がよい場合がある（「変更部分」は diff のハンクとは限らない）— [PDF](https://tobiasbaum.github.io/rp/optimalordering.pdf)

#### Baum, Schneider, Bacchelli, Associating Working Memory Capacity and Code Change Ordering with Code Review Performance (EMSE) — 本文 PDF を読んだ
- 知識: 主に専門開発者 50 人の確認的実験。小さな変更 1 つと大きな変更 2 つに欠陥を植え込んだ。45 人で作業記憶容量を測った — [PDF](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)
- 知識: 作業記憶容量は「離れた場所にまたがる欠陥（delocalized defects）」の発見率と中程度に関連したが、他の欠陥とはほぼ無関係 — [PDF](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)
- 知識: 小さい変更の方がレビューの有効性が有意に高い — [PDF](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)
- 知識（否定的結果）: 順序の効果は確かめられなかった。
  > "We cannot conclude reliably whether the order of presenting the code change parts influences the efficiency of code review."
  — [PDF](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)
- 洞察: レビュー支援ツール研究の多くは「レビュアーの精神的負荷を減らせば成績が上がる」という仮定に明示的・暗黙的に立っている、と著者自身が指摘 — [PDF](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)

#### Baum 博士論文（認知支援レビューツール、CoRT）— 要旨のみ
- 意図: 大きな変更のレビューで認知負荷を下げることが支援の最有望路線であり、効果的な読み順へ導くこと、認知支援ツールの要求カタログ、CoRT のアーキテクチャが寄与とされる — [DNB](https://nbn-resolving.org/urn:nbn:de:101:1-2020021115194615374977), [ホームページ](https://tobiasbaum.github.io)（要旨・検索要約による。本文未読）

#### Fregnan et al., First Come First Served (ESEC/FSE 2022) — arXiv 要旨
- 知識: 138 の Java プロジェクトの 219,476 PR で、先に表示されるファイルほどコメントが多い（議論スレッドや追加行数を統制しても）— [arXiv](https://arxiv.org/abs/2208.04259)
- 知識: 106 人の実験で、ある種類の欠陥は位置の効果なし、別の種類では最後に置くと発見のオッズが 64% 低い — [arXiv](https://arxiv.org/abs/2208.04259)
- 引用: > "the relative position in which files are presented has an impact on code reviews' outcome" — [arXiv](https://arxiv.org/abs/2208.04259)

#### Bagirov, …, Kovalenko, Assessing the Impact of File Ordering Strategies (2023) — arXiv 要旨
- 知識: IntelliJ IDEA のレビュー過程で、下にあるファイルほど注意が少ないことを再確認。差分量順は問題のあるファイルをアルファベット順より上に置く — [arXiv](https://arxiv.org/abs/2306.06956)

#### Bouraffa, Brandt, Zaidman, Maalej, Not One to Rule Them All (EASE 2025) — リポジトリの要旨
- 知識: 100 リポジトリ（Java/Python）の 23,241 PR で、44.6% は非アルファベット順にコメントされていた。差分の大きい順 20.6%、PR のタイトル・説明との類似順 17.6%、本番とテストの両方を含む PR のうちテスト先行 29% — [TU Delft](https://repository.tudelft.nl/record/uuid:523eb4a8-a52c-4ef7-ab23-3a3601a5d978)
- 知識: 非アルファベット順のレビューはレビューされたファイルの割合が有意に高く、承認はやや少ない — [TU Delft](https://repository.tudelft.nl/record/uuid:523eb4a8-a52c-4ef7-ab23-3a3601a5d978)

#### Rahman, Codabux, Roy, Breaking the Alphabet (ICSE 2026) — プログラムページの要旨
- 知識: 182 OSS の開発者 1,355 人の調査で、アルファベット順を最適と考えるのは 10.2%、57.6% が文脈切替・論理的推論の妨げ・疲労を挙げ、63.9% が見落としを懸念、66% が順序のカスタマイズを望み、依存関係に基づくまとめを期待 — [researchr](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/310/Breaking-the-Alphabet-Rethinking-File-Ordering-in-Code-Review)

#### Wurzel Gonçalves, Rani, Storey, Spinellis, Bacchelli, Code Review Comprehension (arXiv 2025) — arXiv HTML
- 知識: 経験あるレビュアー 10 人が実際の 25 レビューを発話思考（約 14.7 時間）。Letovsky の理解モデルで分析 — [arXiv](https://arxiv.org/html/2503.21455v1)
- 知識: レビューは機会主義的。まず文脈を作り、読む・議論を管理する・テストするで検査する。大きな変更では線形の読み方から「難しさ順」や「チャンク化」に切り替え、複数回に分けて範囲を決める — [arXiv](https://arxiv.org/html/2503.21455v1)
- 知識: レビュアーは仕様・実装・注釈の 3 層のメンタルモデルを作り、実際の変更を「予想した解」「理想の解」と比べる — [arXiv](https://arxiv.org/html/2503.21455v1)
- 洞察（ツールへの含意）: 範囲決め、変更のチャンク化、既存コメントの表示切替、ナビゲーション・テスト・レビューを一つの環境で、複数のメンタルモデルの構築と比較を支援すべき — [arXiv](https://arxiv.org/html/2503.21455v1)
- 洞察: 再レビューでは近道をする（> "I can take shortcuts."）、事前合意があると挑戦が減る — [arXiv](https://arxiv.org/html/2503.21455v1)

#### Gonçalves, Fregnan, Baum, Schneider, Bacchelli, Do explicit review strategies improve code review performance? (EMSE 2022) — 要旨・二次資料
- 知識: 主に初心者の 70 人が、自由・チェックリスト・ガイドつきチェックリストの 3 条件で 3 課題をレビュー。単純な課題ではガイドつきが、複雑な課題ではチェックリストが有効だったが、ガイドと成績の強い関係は見いだせず — [Springer](https://link.springer.com/10.1007/s10664-022-10123-8)（検索要約による）
- 知識: チェックリストは認知負荷を下げる可能性があるが、認知負荷が高い方が成績がよかった（参加者全体の成績が低かったためかもしれない）— [Springer](https://link.springer.com/10.1007/s10664-022-10123-8)（検索要約による）
- 洞察（第三者の論評）: ガイドそのものを理解する負荷が加わる、誤誘導もありうる — [Staron のブログ](https://metrics.blogg.gu.se/?p=747)（二次資料）

#### Gullstrand Heander, Söderberg, Rydenfält, Code Review as Decision-Making (arXiv 2025)
- 知識: 10 人・34 レビューの民族誌的発話思考。オリエンテーション段階（文脈と理由づけの確立）と分析段階（理解・評価・残りの計画）の 2 段階。再認主導型意思決定に似る — [arXiv](https://arxiv.org/abs/2507.09637)
- 意図・警告: レビューを完全自動化すると知識移転や共有された所有感など対人的な利点を失いうる — [arXiv](https://arxiv.org/abs/2507.09637)

#### Pascarella et al., Information Needs in Contemporary Code Review (CSCW 2018) — 要旨のみ
- 知識: レビューの議論スレッドの質問を情報ニーズの代理として分類し、7 つの上位カテゴリ（例: 変更されたメソッド・変数がどう使われているか、変更の理由、コード文脈）を得た — [TU Delft](https://research.tudelft.nl/en/publications/information-needs-in-contemporary-code-review)（7 カテゴリ全部の名前は未確認）

#### Spadini et al. — 要旨・スライド
- 知識（ICSE 2018）: 30 万件超のレビューと 12 人の面接で、テストファイルのレビューは本番コードと大きく異なり、レビュー内のナビゲーションが主な問題の一つ — [TU Delft](https://research.tudelft.nl/en/publications/when-testing-meets-code-review-why-and-how-developers-review-test/)（要旨）
- 知識（ICSE 2019, TDR）: テストを先に読むと本番コードの欠陥発見率は同じ、テストの欠陥は多く見つかる、本番コードの保守性指摘は減る。多くの開発者は本番コードを先に読みたがる。障壁はテストの質の低さとツール支援の不在 — [TU Delft](https://repository.tudelft.nl/record/uuid:b275d9ed-47b7-432a-8d22-4e1456a9ff7c)（要旨。92 人などの数値はスライドの二次情報 — [SlideShare](https://www.slideshare.net/DavideSpadini/testdriven-code-review-an-empirical-study)）
- 知識（ICSE 2020, Primers or Reminders）: 85 人の約 70% が利用可能性バイアスに傾きやすいと判定されたが、既存コメントは一般には偏りを生まず、普段考えない種類の欠陥についてのコメントがあると同種の欠陥をよく見つけた（＝プライマーよりリマインダー）— [ICSE 2020](https://2020.icse-conferences.org/details/icse-2020-papers/17/Primers-or-Reminders-The-Effects-of-Existing-Review-Comments-on-Code-Review), [TU Delft](https://repository.tudelft.nl/record/uuid:e9e6a336-d5d8-4167-8c3d-d5aaf6598da6)（要旨）

#### di Biase, Bruntink, van Deursen, Bacchelli, The effects of change decomposition on code review (PeerJ CS 2019) — 本文 HTML
- 知識: 28 人（統制 14・処置 14）。7 ファイル約 100 行の変更を、混ざった 1 PR として見せるか、分けた 2 PR として見せるか。欠陥発見数に有意差なし（20 対 17, p=0.6）。誤検知は分けた方が有意に少ない（6 対 1, p=0.03）。理由の理解には有意差なし。所要時間にも有意差なし — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7924728/)

#### Barnett, Bird, Brunet, Lahiri, ClusterChanges (ICSE 2015) — MSR ページと検索要約
- 意図: 変更された定義（型・フィールド・メソッド）と、差分内でのその使用を束ねて独立した部分に分割 — [MSR](https://www.microsoft.com/en-us/research/publication/helping-developers-help-themselves-automatic-decomposition-of-code-review-changesets/)
- 知識: Office 2013 の 1,000 変更セットに適用。変更の作者に聞くと多くは分割に同意し、レビュアーの理解に役立つと考えた — [MSR](https://www.microsoft.com/en-us/research/publication/helping-developers-help-themselves-automatic-decomposition-of-code-review-changesets/)（検索要約による）

#### Tao & Kim, Partitioning Composite Code Changes (MSR 2015) — 要旨
- 知識: 453 件の OSS 変更のうち最大 29% が複合変更 — [PDF](https://hunkim.cse.ust.hk/papers/tao-msr2015.pdf)（検索要約による）
- 意図: 書式・依存・類似の手がかりでヒューリスティックに分割 — 同上（二次資料）

#### Ko, DeLine, Venolia, Information Needs in Collocated Software Development Teams (ICSE 2007) — 本文 PDF を読んだ
- 知識: Microsoft の開発者 17 人を観察し、21 種の情報ニーズを分類。最も頻繁なのは成果物と同僚についての「認知（awareness）」。最も先送りされたのは設計とプログラムの振る舞いに関する知識（なぜこう書かれたか、何をするはずか、失敗の原因）— [PDF](https://faculty.washington.edu/ajko/papers/Ko2007InformationNeeds.pdf)
- 知識: 設計知識は設計文書・バグ報告・個人の記憶に散らばり、2 人を除く全員が設計知識の欠如で判断を先送りした — [PDF](https://faculty.washington.edu/ajko/papers/Ko2007InformationNeeds.pdf)
- 引用: > "The most difficult to satisfy were design questions" — [PDF](https://faculty.washington.edu/ajko/papers/Ko2007InformationNeeds.pdf)

#### LaToza, Venolia, DeLine, Maintaining Mental Models (ICSE 2006) — 要旨・検索要約
- 知識: 2 つの調査と 11 人の面接。暗黙知の回復に大きな労力。開発者は設計文書やメールの知識庫を避け、知識は対面の会話とコードで共有される — [MSR](https://www.microsoft.com/en-us/research/?p=154508)（検索要約による）

#### Sillito, Murphy, De Volder (TSE 2008)
- 知識: 変更作業中にプログラマーが問う質問を 44 種に分類し、その答え方を記述 — [UBC](https://open.library.ubc.ca/collections/831/items/1.0052042)（要旨。44 種の一覧は未読）

#### Kersten & Murphy, Using task context to improve programmer productivity (FSE 2006)
- 知識: Mylar（Mylyn の前身）を自発的に日常使いした産業界のプログラマー 16 人で、生産性の統計的に有意な向上 — [bibtex](https://bibtex.github.io/FSE-2006-KerstenM.html), [PDF](https://www.st.cs.uni-saarland.de/edu/softmine2007/Papers/mylar.pdf)（要旨）
- 意図: タスクに関係する要素の「関心度モデル」を作り、タスク切替のたびの再探索を省く — 同上

#### Crichton, Agrawala, Hanrahan, The Role of Working Memory in Program Tracing (CHI 2021) と博士論文
- 知識: 人は約 7 個の変数・値の組を作業記憶に保持でき、負荷が高いと対応を取り違える。参加者の半分は上から線形に、半分は下からデータ依存で必要に応じて追跡した — [arXiv](https://arxiv.org/abs/2101.06305)
- 意図: 記憶負荷の高い部分を解析で見つける、追跡の仕方に合わせて情報を対話的に示す、プログラム状態を外在化する — [arXiv](https://arxiv.org/abs/2101.06305)
- 知識（Focus Mode の評価）: Rust に慣れた 18 人がデバッグ課題を Focus Mode あり／なしで実施。予期しない依存を浮かび上がらせ、無関係なコードを薄くするのに役立った — [博士論文 PDF](https://willcrichton.net/assets/pdf/dissertation.pdf)
- 洞察（失敗の報告）: スライスの外にあるコードがバグ理解に必要な場合があり、スライサーは関連コードを無視させるよう誤誘導しうる。引用:
  > "the longstanding definition of slices as “relevant code” does not match reality."
  — [博士論文 PDF](https://willcrichton.net/assets/pdf/dissertation.pdf)
- 知識: Focus Mode は無償のオープンソースで、2022 年時点で VSCode 拡張として 1,800 回ダウンロード — [博士論文 PDF](https://willcrichton.net/assets/pdf/dissertation.pdf)

#### Siegmund, Program Comprehension: Past, Present, and Future (FoSE 2016) ほか
- 知識: 開発者がコード理解に費やす時間の多さは 30 年間ほぼ変わっていない — [PDF](https://www.se.cs.uni-saarland.de/publications/docs/FoSE16.pdf)（検索要約による）
- 知識: 17 人の fMRI 研究、理解を要しない対照課題との差分で理解特有の脳領域を同定する方法 — [PDF](https://www.se.cs.uni-saarland.de/publications/docs/SKA+14.pdf)（要旨）

#### Fritz et al., Using Psycho-Physiological Measures to Assess Task Difficulty (ICSE 2014)
- 知識: 専門開発者 15 人、視線・皮膚電気・脳波で理解課題の難しさ（易/難）を予測。新しい課題に対して適合率 84.38%・再現率 69.79%。NASA TLX と難易度順位は相関（r=0.587）— [MSR](https://www.microsoft.com/en-us/research/?p=166326)（要旨）

#### Barik et al., Do Developers Read Compiler Error Messages? (ICSE 2017)
- 知識: 56 人の視線計測。メッセージは読まれていて、読むのはソースコードを読むのと同程度に難しく、読みにくさが課題成績を予測。課題時間の 13〜25% をメッセージに使う — [preprint](https://jssmith1.github.io/assets/pdf/ICSE_2017_EYE.pdf), [Never Work in Theory（二次資料）](https://neverworkintheory.org/2021/09/20/do-developers-read-compiler-error-messages.html)

#### Hermans, The Programmer's Brain (2021)
- 知識（共著論文から）: 内在的負荷は課題そのもの、外在的負荷は提示の仕方から来る不要な負荷 — [NSF PAR](https://par.nsf.gov/servlets/purl/10580377)（本の本文は未読）

#### Sadowski et al., Modern Code Review at Google (ICSE SEIP 2018)
- 知識: 12 人の面接、44 人の調査、2 年間・900 万レビューのログ。レビューは他の文脈より軽量で、単一レビュアー・素早い反復・小さな変更・ツールとの統合が特徴 — [Google Research](https://research.google/pubs/modern-code-review-a-case-study-at-google/)（要旨）

### Inferences
- 「なぜ変えたか（変更のきっかけ）」が最大の情報ニーズであることは、2007（Ko）・2013（Bacchelli & Bird）・2017（Baum の「最初に要求を知りたい」）・2025（CRDM のオリエンテーション段階、CRCM の文脈構築）で繰り返し独立に出てくる。理解支援の仕組みの冒頭に置くべき最優先の要素と推論する。
- 表示順の効果は「注意の配分」には確かにある（Fregnan, Kovalenko）が、「関係順に並べると効率が上がる」ことは確かめられていない（Baum EMSE）。順序で救えるのは見落としの偏りであって、理解の速さではないかもしれない。
- 作業記憶が効くのは離れた場所にまたがる欠陥だけ（Baum）。Principle 5「同時に画面に見える」はまさにこの種の欠陥に効くはずの設計で、pr-tour の「定義プレビュー」はこれに当たる。

### Gaps
- Baum の博士論文、Pascarella 2018、Tao 2012、Sadowski 2018、Kersten & Murphy 2006 の本文は読めていない（PDF 取得失敗または時間切れ）。数値は要旨か二次資料に依拠。
- Pascarella の 7 カテゴリ、Sillito の 44 質問の完全な一覧は未取得。
- Tao & Kim 2015 の分割精度 69% はスライド由来の二次情報で未確認。

---

## 問い3: 作られて、捨てられた・効かなかった道具や試みと、その理由

### Takeaway
報告された「失敗」は、ツールが外れたというより、ツールの前提（関連コード＝スライス、順序を変えれば効率が上がる、ガイドがあれば楽になる、ランキングを出せば人は上から順に見る）が人の実際の理解と合わなかった、という形で出ている。製品化されなかった理由として明示されているのは、研究試作の完成度（Henley）と、元実装が非公開で再実装が必要だったこと（ClusterChanges）くらいで、「なぜ捨てたか」を正面から書いた一次資料は少ない。

### Cited Findings
- 順序づけ（Baum）: 理論から予測した「よい順序で効率が上がる」を 50 人の実験で確かめようとしたが、確実な結論を出せなかった — [PDF](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)
- 変更の分解（di Biase ら）: 分けても欠陥発見数・理由の理解・時間に有意差なし。誤検知だけが減った — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7924728/)
- ClusterChanges: 元の実装が公開されていなかったため、別の大学が JClusterChanges としてオープンソースで再実装した — [UFCG 修士論文](https://bdtd.ufcg.edu.br/jspui/bitstream/riufcg/765/3/VICTOR%20DA%20CUNHA%20LUNA%20FREIRE%20-%20DISSERTA%c3%87%c3%83O%20%28PPGCC%29%202016.pdf)（検索要約による）。Microsoft の CodeFlow に製品として組み込まれたかどうかは確認できなかった。
- Flowistry Focus Mode（Crichton）: スライスの外に理解に必要なコードがある課題では、ツールが関連コードを無視させる方向に誤誘導した — [博士論文 PDF](https://willcrichton.net/assets/pdf/dissertation.pdf)
- 自動デバッグ（Parnin & Orso 2011）: 疑わしい文のランキングは、より速くよい診断には繋がらず、手法が置く前提のいくつかは実際には成り立たない — [PDF](https://web.eecs.umich.edu/~weimerw/2018-481/readings/debugging-helping.pdf)（要約は検索結果。「バグの行をクリックしても調査をやめたのは 10 人中 1 人」はスライドの二次情報 — [SlideShare](https://www.slideshare.net/slideshow/are-automated-debugging-techniques-actually-helping-programmers/8654857)）
- チェックリスト／ガイド（Gonçalves ら）: ガイドと成績の強い関係は見いだせず、認知負荷が高い方が成績がよいという予想外の結果 — [Springer](https://link.springer.com/10.1007/s10664-022-10123-8)（検索要約による）
- テスト先行レビュー（Spadini ら）: 本番コードの保守性指摘が減るトレードオフ。開発者の多くは本番コード先行を好み、テストの質の低さとツール不在が採用を阻む — [TU Delft](https://repository.tudelft.nl/record/uuid:b275d9ed-47b7-432a-8d22-4e1456a9ff7c)（要旨）
- Patchworks（Henley）: 比較実験で優れた結果を出し Google・Microsoft の開発者から問い合わせがあったが、製品としては公開されなかった。本人の言葉:
  > "far too embarrassed to let anyone use outside of the lab."
  — [Henley のブログ](https://austinhenley.com/blog/coderibbon.html)。一方で National Instruments の LabVIEW に実装され、後継として学生が CodeRibbon（Atom プラグイン）を作った — 同上
- Patchworks の意図: Code Bubbles の自由なキャンバスは自由すぎると考え、制約を加えた。
  > "We worried this was too much freedom."
  — [Henley のブログ](https://austinhenley.com/blog/coderibbon.html)
- Tricorder（Sadowski ら, Google）: 以前の FindBugs の試みでは誤検知のせいで開発者がツール全体への信頼を失った。Tricorder は「NOT USEFUL」ボタンで「実効誤検知（利用者が対応しなかった報告）」を継続監視し、レビュー時の表示を厳しく絞った — [Tricorder PDF](https://www.cs.umd.edu/class/spring2019/cmsc414/papers/tricorder-building-a-program-analysis-ecosystem.pdf)（検索要約による。「10% 未満でなければ外す」という閾値は一次資料で未確認）
- 2013 年時点の評価: 実務のレビューツールは理解ニーズに基本的な支援しかしていない（差分・行コメント・構文強調）— [PDF](https://sback.it/publications/icse2013.pdf)
- 2016 年時点の評価: ツール研究が多くあるのに、理解に要する時間は 30 年ほぼ不変 — [Siegmund FoSE16](https://www.se.cs.uni-saarland.de/publications/docs/FoSE16.pdf)（検索要約による）

### Inferences
- 「関連コード」をアルゴリズム的に定義（スライス、定義-使用の束）すると、人が理解に必要とする範囲とずれる。自動の束ね方や絞り込みは、隠すより「薄く見せる・理由を示す・人が外せる」形が安全だと推論する（Crichton の誤誘導、Baum の Principle 6）。
- 研究試作が製品化されない主な理由は、評価で勝つことと日常で使える完成度の差（Henley）。pr-tour のように既存の Files changed の「伴走」に留める設計は、この差を小さくする選択と言える。
- Tricorder の教訓は、レビュー時に差し込む情報（AI 生成の解説も含む）は「役に立たない」と判断される割合を測って絞らないと、仕組み全体の信頼を失うということ。

### Gaps
- CoRT（Baum のツール）がその後どう使われたか、使われなくなったかの記録は見つけられなかった。
- ClusterChanges が CodeFlow 等に組み込まれたか、なぜ組み込まれなかったかの一次資料は見つけられなかった。
- Henley の Yestercode の評価結果は未取得。
- Tricorder・CACM「Lessons from Building Static Analysis Tools at Google」の本文は未読。

---

## 問い4: 「この PR・変更を理解しやすくする」仕組みの設計原則の候補

### Takeaway
証拠の強さで分けると、(A) 測られた事実に基づく原則は「最初に変更の理由と全体像を出す」「後ろに置いたものは見落とされる前提で、重要なものを前に置くか全体を網羅したことを確かめる」「離れた場所の関係は同時に見せる」「変更は小さく・関心ごとに分ける（誤指摘が減る）」。(B) 作り手の意図・理論止まりの原則は「関連でまとめ、まとめ方を名前つきで見せる」「必要になる前に情報を出す」。(C) 失敗から来る原則は「自動の絞り込みで隠さない」「役に立たない差し込みを測って減らす」「自動化で対人の知識共有を消さない」。

### Cited Findings（原則ごとの根拠）
1. 冒頭に「なぜ」と全体像: 最大の課題は変更理由の理解 — [Bacchelli & Bird](https://sback.it/publications/icse2013.pdf)。設計知識が最も満たされにくい — [Ko 2007](https://faculty.washington.edu/ajko/papers/Ko2007InformationNeeds.pdf)。レビュー開始時に要求と概観、使用例（テスト）が助けになる — [Baum 2017](https://tobiasbaum.github.io/rp/optimalordering.pdf)。オリエンテーション段階 — [CRDM](https://arxiv.org/abs/2507.09637)。
2. 関連でまとめ、規則を見せる（名前つきのグループ）: Principle 1, 3, 4, 6 — [Baum 2017](https://tobiasbaum.github.io/rp/optimalordering.pdf)。依存関係でのまとめを 66% が期待 — [Rahman et al. 2026](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/310/Breaking-the-Alphabet-Rethinking-File-Ordering-in-Code-Review)。ただし効率向上は未確認 — [Baum EMSE](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)。
3. 宣言は使用より前、呼び出しの向きは選べるようにする: 宣言→使用の向きは好まれたが、呼び出し方向は人により（調査は bottom-up 85%、面接は top-down 派も多い）— [Baum 2017](https://tobiasbaum.github.io/rp/optimalordering.pdf)。追跡戦略は線形と必要に応じて（on-demand）で半々 — [Crichton 2021](https://arxiv.org/abs/2101.06305)。
4. 関係する離れた部分は同時に見せる（定義プレビュー、並置）: Principle 5 — [Baum 2017](https://tobiasbaum.github.io/rp/optimalordering.pdf)。作業記憶は離れた欠陥の発見にだけ効く — [Baum EMSE](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)。約 7 組の保持限界と状態の外在化 — [Crichton 2021](https://arxiv.org/abs/2101.06305)。並置が多くナビゲーションの誤りが少ない — [Henley 2017 CHI（検索要約）](https://austinhenley.com/pubs/Henley2017CHI_CodeEditors.pdf)。
5. 順序は注意を配分する、と自覚して設計する: 後ろのファイルは注意が減り、ある種の欠陥の発見オッズが 64% 下がる — [Fregnan 2022](https://arxiv.org/abs/2208.04259), [Kovalenko 2023](https://arxiv.org/abs/2306.06956)。レビュー済みのファイルの割合を示す等の網羅の確認が候補（推論）。
6. 大きな変更では読み方が変わることを前提に、範囲決め・チャンク化・複数回に分けることを支える: [CRCM](https://arxiv.org/html/2503.21455v1)。小さい変更ほど有効性が高い — [Baum EMSE](https://tobiasbaum.github.io/rp/memoryCodeOrderAndReview.pdf)。Google は小さな変更が標準 — [Sadowski 2018](https://research.google/pubs/modern-code-review-a-case-study-at-google/)。
7. 混ざった変更は分ける（ただし期待は「誤指摘が減る」まで）: [di Biase 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7924728/)、複合変更は最大 29% — [Tao & Kim 2015（要旨）](https://hunkim.cse.ust.hk/papers/tao-msr2015.pdf)。
8. 「予想した解」「理想の解」と比べられるようにする（意図と実装の対比）: 仕様・実装・注釈の 3 層モデル — [CRCM](https://arxiv.org/html/2503.21455v1)。
9. 自動の絞り込みは隠さず薄くする、外れうることを示す: [Crichton 博士論文](https://willcrichton.net/assets/pdf/dissertation.pdf)。ランキングを出しても人はそこで調査を止めない — [Parnin & Orso 2011](https://web.eecs.umich.edu/~weimerw/2018-481/readings/debugging-helping.pdf)。
10. 差し込む情報の「役に立たない」率を測る: [Tricorder](https://www.cs.umd.edu/class/spring2019/cmsc414/papers/tricorder-building-a-program-analysis-ecosystem.pdf)（検索要約）。
11. 既存のコメントは見せてよい（リマインダーとして働く）、表示の切替を用意する: [Spadini 2020](https://2020.icse-conferences.org/details/icse-2020-papers/17/Primers-or-Reminders-The-Effects-of-Existing-Review-Comments-on-Code-Review), [CRCM](https://arxiv.org/html/2503.21455v1)。
12. 共有メンタルモデルは文書より会話とコードで流れる。自動化で対人のやりとりを消さない: [LaToza 2006（要約）](https://www.microsoft.com/en-us/research/?p=154508), [Bacchelli & Bird](https://sback.it/publications/icse2013.pdf)（20〜40% は対面で聞く）, [CRDM](https://arxiv.org/abs/2507.09637)。
13. 手引き自体の負荷を勘定に入れる（ガイドを理解する負荷）: [Gonçalves 2022](https://link.springer.com/10.1007/s10664-022-10123-8), [Staron の論評（二次）](https://metrics.blogg.gu.se/?p=747)。
14. テストを「使用例」として入口か締めに使う。ただしテスト先行は本番コードの保守性指摘を減らす: [Baum 2017](https://tobiasbaum.github.io/rp/optimalordering.pdf), [Spadini 2019（要旨）](https://repository.tudelft.nl/record/uuid:b275d9ed-47b7-432a-8d22-4e1456a9ff7c)。

### Inferences
- pr-tour への含意（推論）: 「コードの流れ順」は Baum の関連の 8 種のうちデータフロー・呼び出しに当たる。Principle 6 からは、なぜこの順なのか（例: 「呼ばれる側から」）をツアーの冒頭とグループ見出しで明示することが重要。呼び出し方向の好みが割れる以上、向きを切り替えられるか、少なくとも明示した方がよい。後ろに回したファイルの見落としを防ぐため、ツアーの末尾に「残り（重要度の低いもの）」をまとめて示すのは Baum の面接の終わり方の戦術と一致する。
- pr-review への含意（推論）: 共有メンタルモデルを育てるには、レビューコメントが「仕様・実装・注釈」のどの層のずれを指しているかを明示する書き方が CRCM に沿う。既存コメントは他のレビュアーにとってリマインダーとして働くので、「普段見落とされる種類」の指摘を残す価値が高い（Spadini 2020）。
- 評価への含意: この分野の否定的結果（Baum の順序、di Biase の分解、Gonçalves のガイド）は、「理解が楽になった」という主観と、欠陥発見・時間・理解度という客観指標がずれうることを示す。pr-tour / pr-review を評価するなら、効率ではなく「誤指摘の減少」「後半ファイルの見落とし」「理由の理解」など、効果が出やすいと報告された指標を別々に測るべき。

### Gaps（未検証事項のまとめを含む）
- 未検証: Storey、Barik、Henley、Parnin の現所属。
- 未検証: Baum の博士論文の正式な題名と年（DNB の記録のみ）。
- 未検証: Tricorder の「実効誤検知 10% 未満」という閾値（ベンダーの二次資料のみ）。
- 未検証: Google のレビューの中央値 24 行などの数値（学生のスライド由来のため本文では採らなかった）— [スライド](https://plg.uwaterloo.ca/~migod/846/current/summaries/10-Youssef-GoogleCodeReview-slides.pdf)
- 未検証: TDR 実験の 92 人・150 レビューなどの数値（スライド由来）。
- 未検証: Tao & Kim 2015 の 69% 分割精度と小規模ユーザー研究の結果（スライド由来）。
- 未検証: Henley 2017 CHI の「32 人の LabVIEW プログラマー」等の数値（検索要約のみ）。
- 未調査: AI（LLM）による変更要約・レビュー支援を、上記の研究者自身が 2024–2026 年にどう評価したか（例: Google の ML によるコメント解決、Jaspan/Murphy-Hill の研究）。今回の範囲では一次資料を確認していない。
- 未調査: 仕様書・設計判断（コード以外の高負荷成果物）の理解支援については、本調査の人物群からは直接の資料を得ていない。
