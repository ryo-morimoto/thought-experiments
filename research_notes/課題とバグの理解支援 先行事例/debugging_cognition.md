# デバッグの認知・仮説形成・故障位置特定の実際：人物と資産

調査日: 2026-11-21。対象: issue やバグ報告を「再現する・期待される挙動を確かめる・原因を突き止める・妥当性と深刻度を判断する」のを助ける仕組みを作る人のための、人起点の先行研究調査（PR は対象外）。

凡例:
- 「知識」= 測られた・観察された事実、「洞察」= 失敗や観察から得たこと、「意図」= なぜそう設計したか／何を捨てたか。
- 引用は英語原文のまま短く「> 」で示し、直後に出典 URL を置く（DATA_POLICY の限定的な引用として扱う）。
- 論文 PDF 本文を pdftotext で読んで確かめたものは「（本文確認）」、要旨や紹介ページのみは「（要旨のみ）」、検索結果の要約のみは「（検索要約のみ）」、調査者の既存知識で今回一次資料を開いていないものは「（未確認・記憶）」と書く。

---

## 1. 人物一覧

### Takeaway
中心は二系統。(a) 自動デバッグ（故障位置特定・Delta Debugging）を作った側が、自ら「人を助けていない」と検証した系統（Zeller, Böhme, Parnin & Orso）と、(b) 人がどう問い・仮説を立てるかを観察してツールを作った系統（Ko の Whyline、LaToza & Alaboudi の仮説研究）。実務側では O'Callahan（記録再生・全知デバッグ）、Regehr（テストケース縮小）、Julia Evans・Agans（心構えの言語化）が、研究の知見と同じ方向のことを独立に言っている。

### Cited Findings

<!-- data-source: original（調査ノートの整理） -->
| 人物 | 所属（出典での記載） | なぜ重要か | 代表的な仕事（確認状態） |
|---|---|---|---|
| Andreas Zeller | Saarland University（DBGBench 論文記載時） | 科学的デバッグ（問い→仮説→予測→実験→記録）を教科書化。Delta Debugging の作者。自動化側の代表でありながら DBGBench で人の診断を測った | The Debugging Book「Introduction to Debugging」— [debuggingbook.org](https://www.debuggingbook.org/html/Intro_Debugging.html)（本文確認）。Why Programs Fail（書籍、未確認・記憶） |
| Marcel Böhme | National University of Singapore（論文記載時） | 実務者 180 人の調査と 12 人の観察で「診断」を測り、合意された診断を正解データ（DBGBench）にした | How Developers Diagnose and Repair Software Bugs (and what we can do about it) — [PDF](https://www.st.cs.uni-saarland.de/debugging/dbgbench/dbgbench.pdf)（本文確認） |
| Chris Parnin / Alessandro Orso | Georgia Institute of Technology（論文記載時） | 順位付き故障位置特定（Tarantula）を人に使わせ、前提が成り立たないことを示した | Are Automated Debugging Techniques Actually Helping Programmers? (ISSTA 2011) — [PDF](https://web.eecs.umich.edu/~weimerw/2018-481/readings/debugging-helping.pdf)（本文確認） |
| Amy J. Ko / Brad A. Myers | CMU HCII（論文記載時） | 「なぜ起きた／なぜ起きなかった」という出力についての問いから始める Whyline | Debugging Reinvented: Asking and Answering Why and Why Not Questions about Program Behavior (ICSE 2008) — [PDF](https://faculty.washington.edu/ajko/papers/Ko2008JavaWhyline.pdf)（冒頭と評価の一部を本文確認） |
| Abdulaziz Alaboudi / Thomas D. LaToza | George Mason University（論文記載時） | 仮説の数・正しさと成功の関係を統制実験で測り、「故障位置ではなく仮説を渡す」と効くことを示した | Using Hypotheses as a Debugging Aid (VL/HCC 2020) — [arXiv](https://arxiv.org/abs/2005.13652)（本文確認）。An Exploratory Study of Debugging Episodes — [arXiv](https://arxiv.org/abs/2105.02162)（本文確認） |
| Moritz Beller / Andy Zaidman / Diomidis Spinellis | TU Delft / AUEB（論文記載時） | IDE の計測で、デバッガが実際にはあまり使われず printf が健在であることを示した | On the Dichotomy of Debugging Behavior Among Programmers (ICSE 2018) — [PDF](https://www.spinellis.gr/pubs/conf/2018-ICSE-debugging-analysis/html/BSSZ18.pdf)（要旨と一部を本文確認） |
| Robert O'Callahan | rr / Pernosco 作者 | 記録再生（rr）と全知デバッグ（Pernosco）。「値はどこから来たか」を辿れること、調査を共有できることを設計の中心に置く | Pernosco 概要 — [pernos.co](https://pernos.co/about/overview/)（本文確認）。ブログ robert.ocallahan.org は 503 で読めず（未確認） |
| John Regehr | University of Utah（未検証） | テストケース縮小（C-Reduce）。縮小が理解と報告を助ける理由と、縮小の失敗モードを書いている | ブログ記事 — [blog.regehr.org/archives/1678](https://blog.regehr.org/archives/1678)（本文確認） |
| Nicolas Bettenburg ほか | （未検証） | 「良いバグ報告」で開発者が最も必要とする情報を調査（2008） | What Makes a Good Bug Report? — The Debugging Book「Tracking Bugs」経由で確認（[debuggingbook.org](https://www.debuggingbook.org/html/Tracking.html)、二次資料） |
| Julia Evans | 実務者（jvns.ca） | デバッグの心構えを 8 項目に言語化 | A debugging manifesto — [jvns.ca](https://jvns.ca/blog/2022/12/08/a-debugging-manifesto/)（本文確認） |
| David J. Agans | 実務者（書籍著者） | 『Debugging: The 9 Indispensable Rules』 | 公式サイト [debuggingrules.com](https://debuggingrules.com/) にはルール本文が載っていない（未確認・記憶） |
| Michael Perscheid / Robert Hirschfeld | HPI（未検証） | 実務デバッグの調査（"Studying the advancement in debugging practice of professional software developers"） | 今回は一次資料を開いていない（未確認・記憶） |
| David Lo / Xin Xia ほか | SMU ほか（未検証） | 実務者の故障位置特定への期待の調査（"Practitioners' expectations on automated fault localization", ISSTA 2016） | 今回は一次資料を開いていない（未確認・記憶） |

### Inferences
- 「自動化を作った人が人で検証して失敗を報告した」系統（Parnin & Orso、Böhme & Zeller、Alaboudi & LaToza の故障位置条件）が、設計判断の根拠として最も強い。

### Gaps
- Perscheid/Hirschfeld、Lo らの論文、Hillel Wayne の該当記事は今回開いていない。
- O'Callahan 本人のブログ（全知デバッグがなぜ理解を変えるかの論考）は 503 で読めなかった。

---

## 2. 仕事ごとの資産

### 2.1 Parnin & Orso (ISSTA 2011) — 順位付き故障位置特定は人を速くしたか

#### Takeaway
順位の上下は成績を変えず、故障行を見ても理解は終わらず、人は順位どおりに見ない。人が欲しがったのは「値・概観・説明（なぜこの行が候補か）」だった。

#### Cited Findings
- 知識: 34 人、2 課題（Tetris, NanoXML）、Tarantula の順位を Eclipse プラグインで提示（本文確認） — [PDF](https://web.eecs.umich.edu/~weimerw/2018-481/readings/debugging-helping.pdf)
- 知識: 故障行の順位を Tetris で 7→35 に下げ、NanoXML で 83→16 に上げても成績に有意差なし（Tetris/NanoXML の所要時間比はどちらの群も .79）。ツールで速くなったのは熟練者の Tetris 課題のみ（本文確認） — 同上
- 知識: 人は順位を線形にたどらない。37% の移動が 1 つ以上飛ばし、平均 10 位飛ばし、平均 10.3 回の折り返し。例外は 1 課題も終えなかった低成績者で、95% が順に巡回（本文確認） — 同上
- 知識（「完全なバグ理解」仮定の否定）: 故障行をクリックした 10 人のうち、そこでツール使用をやめたのは 1 人だけ。残りは平均さらに 10 分、時間の 61% をツールでの点検に使い続けた（本文確認） — 同上
  > "perfect bug understanding is generally not a realistic assumption" — [PDF](https://web.eecs.umich.edu/~weimerw/2018-481/readings/debugging-helping.pdf)
- 洞察: ツールなし群の一部は、故障（fault）でなく失敗（failure）を止める回避策を入れた（Tetris で回転計算を書き換える）。ツール群にはいなかった（本文確認） — 同上
- 洞察: 参加者は「なぜこの文が一覧にあるのか」の説明、実行時の値、例外連鎖との統合、スライスやテストとの対応を求めた。結果を信頼できない・計算方法が分からないとすぐツールを捨てた（本文確認） — 同上
  > "Developers were quick to disregard the tool if they felt they could not trust the results or understand how such results were computed." — [PDF](https://web.eecs.umich.edu/~weimerw/2018-481/readings/debugging-helping.pdf)
- 洞察: 順位付けは文を「開発者が関係づけられるメンタルモデルのない並び」に混ぜ、デバッガやスライスの一貫性を壊す（本文確認） — 同上
- 洞察: 「index」「colon」などの語で絞り込めば故障行は上位 5 件に入った。開発者の頭の中の情報と組み合わせる検索が鍵（本文確認） — 同上
- 意図（研究への提言）: 「割合順位でなく絶対順位で評価せよ」「検索や強調表示に寄せよ」。導入コスト（カバレッジ収集、テストの合否ラベル付け）が節約時間を上回りうる（本文確認） — 同上

#### Inferences
- 「原因箇所の候補リスト」を出すだけの仕組みは、理解支援としては効かない可能性が高い。候補ごとに根拠（どのテスト・どの値・どの依存）を辿れることが前提。

#### Gaps
- 標本は小さく（故障行クリックの分析は 10 人）、学生を含む。著者自身も予備的研究としている。

### 2.2 Alaboudi & LaToza (VL/HCC 2020) — 仮説をデバッグの補助にする

#### Takeaway
開発者の仮説は少なく（1 欠陥あたり中央値 2）、多くは誤り。早く正しい仮説を持つことが成功を強く予測し、故障位置を渡しても効かず、「仮説＋確かめ方」を渡すと成功が 6 倍になった。

#### Cited Findings
- 知識: 20 人の統制実験。段階 1 の仮説の正解率 11%（27 中 3）、段階 2 で 25%、段階 3 で 39%（本文確認） — [arXiv PDF](https://arxiv.org/pdf/2005.13652)
- 知識: 段階 2 で正しい仮説を報告した参加者は修正成功が 5 倍（ロジスティック回帰、p = 0.01）（本文確認） — 同上
- 知識: 故障位置を渡しても正しい仮説は増えず（p = 0.1320）、修正成功も増えなかった（p = 0.6710）。仮説を渡すと 6 倍成功（本文確認） — 同上
  > "offering potential hypotheses made developers six times more likely to succeed" — [arXiv](https://arxiv.org/abs/2005.13652)
- 洞察（予備研究）: 誤った仮説は無関係な情報の調査に導き、進捗を止める（本文確認） — 同上
- 洞察（参加者の声）: 故障行を見ても「直し方がまだ分からなかった」。故障位置は、すでにある程度の知識がある時にだけ役立つ（本文確認） — 同上
- 意図: 渡した仮説は「Hypothesis: … / How To Test: …」の形式で、正しい仮説と誤った仮説を混ぜて提示した（表 II、本文確認） — 同上

#### Inferences
- 仮説は「主張」と「確かめ方」の対で表すのが、この実験で効いた形式。誤った候補を混ぜても効いたことは、候補を「検証すべきもの」として出すなら誤りを含んでもよいことを示唆する（ただし誤り候補の効果を分離した分析は見ていない）。

#### Gaps
- 課題は小さな JS/React の欠陥で、大規模・未知コードベースへの一般化は不明。

### 2.3 Alaboudi & LaToza (arXiv 2021) — 実務のデバッグ・エピソード

#### Cited Findings
- 知識: 配信された 15 セッション（11 人のプロ、30 時間）、デバッグ活動 2137・プログラミング活動 1407 をコード化。デバッグは約 8 分に 1 回、ほとんどのエピソードは数分以内だが、時間の大半は少数の長い（100 分超を含む）エピソードに費やされる。単一の活動が支配することはない（本文確認） — [arXiv](https://arxiv.org/abs/2105.02162)
- 洞察: 関連研究の整理として、困難の原因に「原因と症状の大きな時間的・空間的隔たり」、欠陥の再現の困難が挙がる（本文確認、引用元は別論文） — [arXiv PDF](https://arxiv.org/pdf/2105.02162)

#### Inferences
- 支援の価値は、短い大多数ではなく長いエピソードに集中する。長いエピソードは多様な活動を含むため、単機能の道具より「調査の状態」を保持する仕組みが合う。

### 2.4 Böhme, Soremekun, Chattopadhyay, Ugherughe, Zeller — DBGBench

#### Takeaway
診断（なぜ起きるかの説明）は人の間で 85% 一致し、正解データにできる。一方、テストを通る修正の 4 割は誤り。実務者は「位置」より「説明」を欲しがる。

#### Cited Findings
- 知識（調査 180 人）: 開発時間の 36% がデバッグ、そのうち 47% が診断。バグ報告からの再現に、修正と同程度の時間を使う。約 3 人に 2 人は対象コードへの習熟が中程度以下（本文確認） — [PDF](https://www.st.cs.uni-saarland.de/debugging/dbgbench/dbgbench.pdf)
- 知識: 自動診断の出力として望まれたもの: 「なぜ起きるかの説明」28%、「再現できる最も一般的な条件」23%、失敗入力での関数実行列 19%。40% が疑わしい文を指すツールを望み、40% が位置だけでなく洗練された診断を出すツールを望む。13% は診断の代わりに自動パッチを望む（本文確認） — 同上
- 知識: 修正の正しさの確認は、修正版での再現 95%、新規テスト作成 57%、回帰テスト 54%。妥当な診断に頼ると答えた人は少数（本文確認） — 同上
- 知識（観察 12 人）: 診断に要した延べ時間は修正の約 2 倍（14 時間 20 分 vs 7 時間 11 分）。非常に難しい 4 件中 3 件は 1 行修正。難しさの理由は文書の欠如と、誤った仮説から始めること（例: ヒープ破壊の箇所とクラッシュ箇所が遠い）（本文確認） — 同上
- 知識: 85% の参加者が本質的に同じ診断を出した。診断は 3〜4 の連続領域を参照し、関数・ファイルをまたぐ。多くは 10 文以下（本文確認） — 同上
  > "the understanding and explanation of an error is no subjective endeavor" — [PDF](https://www.st.cs.uni-saarland.de/debugging/dbgbench/dbgbench.pdf)
- 知識: 提出パッチの 97%（282/291）がテストを通るが、正しいのは 58%（170）。修正箇所が診断で参照された文に含まれるのは 69%。正しいパッチを出した人は診断に 25%（5 分）長く時間をかけた。コード理解と正しさの相関 ρ = 0.52（本文確認） — 同上
- 知識: 戦略として前向き推論（FR）、後ろ向き推論（BR）、入力の改変（IM）、オフライン解析（OA）を分類。多くの参加者が入力の改変を使った（本文確認、頻度の詳細は一部のみ） — 同上
- 意図: ベンチマークに「故障位置」「診断（実行時の出来事の簡潔な説明）」「正しいパッチと、テストは通るが誤ったパッチの例」を収録した。位置だけの評価を捨て、説明を正解データにした（本文確認） — 同上

#### Inferences
- 「妥当性の判断」に関して: テスト通過は正しさの弱い代理指標。診断（因果の説明）を明示して残すことが、誤った修正を見抜く材料になる。
- 「再現できる最も一般的な条件」を求める声（23%）は、深刻度判断（影響範囲）に直結する。

### 2.5 Ko & Myers (ICSE 2008) — Whyline

#### Takeaway
開発者は「出力についての問い」を「コードについての問い」に翻訳する段階で推測し、外す。Whyline は問いそのものを出力から選ばせ、推測を省いた。

#### Cited Findings
- 知識: 先行調査で、開発者の初期の推測は約 90% 外れた（本文確認、出典は同著者の先行研究 [7,8]） — [PDF](https://faculty.washington.edu/ajko/papers/Ko2008JavaWhyline.pdf)
  > "developers' initial guesses were wrong almost 90% of the time" — [PDF](https://faculty.washington.edu/ajko/papers/Ko2008JavaWhyline.pdf)
- 知識: 一課題の評価で、Whyline を使う初心者は使わない熟練者の 2 倍速かった。RGB スライダの課題で従来手法は中央値 10 分（3〜38）、多くは「color」で検索して 9 ファイル 62 件の一致を見た（本文確認） — 同上
- 洞察: ブレークポイントは行を、スライスは変数を、問い合わせツールは式を選ばせるため「garbage-in garbage-out」になる。開発者の選択が原因と無関係なら答えも無関係（本文確認） — 同上
- 意図: 「why did / why didn't」の問いを、プログラムのコードと実行記録から導出し、出力（画面上の要素）を起点に選ばせる。なぜ起きなかったか（実行されなかった行）にも答える（本文確認） — 同上

#### Inferences
- バグ報告は本質的に「なぜ X が起きた／なぜ Y が起きなかった」の形をしている。報告をこの形に正規化すると、期待挙動（Y）が明示される。

#### Gaps
- 評価は 1 課題のみ。記録のオーバーヘッドや大規模系への適用の限界は本文後半を読み切っていない。

### 2.6 Beller, Spruit, Spinellis, Zaidman (ICSE 2018)

#### Cited Findings
- 知識: 調査 176 人、IDE 計測 458 人。IDE セッションの 91% でデバッガは起動されず、デバッガを使うのはセッション時間の 14% 未満（本文確認） — [PDF](https://www.spinellis.gr/pubs/conf/2018-ICSE-debugging-analysis/html/BSSZ18.pdf)
- 知識: 回答者はデバッガ（81.3%）のほか、ログファイルの確認（72.2%）、print 文（71.6%）を使う（本文確認） — 同上
- 洞察: printf デバッグは多くのプログラマにとって依然として実行可能な選択肢。高度な機能の知識と利用はともに低い（要旨、本文確認） — 同上

#### Inferences
- 理解支援をデバッガ内機能として作ると、多くの人の実際の作業経路（ログ・print）に乗らない。

### 2.7 Zeller — The Debugging Book（科学的デバッグ、記録をつける）

#### Cited Findings
- 意図: 問いを立てる→仮説→予測→実験→仮説・予測・観察が一致するまで繰り返す。修正の前に、因果（欠陥がどう失敗を生むか）と誤り（なぜそのコードが間違いか）の両方を示す診断が必要（本文確認） — [debuggingbook.org](https://www.debuggingbook.org/html/Intro_Debugging.html)
- 意図: 入力・期待出力・実際の出力・結果を表に記録し、仮説に番号を振る。新しい仮説を過去の観察と照合でき、中断・再開・他者への引き継ぎができる。記憶に頼ると集中を消耗し誤る。マスターマインドの比喩（新しい推測は過去の全結果と整合しなければならない）（本文確認） — 同上
- 洞察（避けるべき方法）: 場当たり的な printf、テストが通るまで無作為に変える「debugging into existence」、症状への特別扱い（本文確認） — 同上
  > "Fix the problem, not the symptom." — [debuggingbook.org](https://www.debuggingbook.org/html/Intro_Debugging.html)
- 知識（二次資料経由）: Bettenburg ら（2008）の調査で開発者が最も必要とする報告情報は、再現手順 83%、スタックトレース 57%、テストケース 51%、観察された挙動 33%、スクリーンショット 26%、期待される挙動 22%（The Debugging Book「Tracking Bugs」による紹介） — [debuggingbook.org](https://www.debuggingbook.org/html/Tracking.html)

### 2.8 Regehr — テストケース縮小（C-Reduce）

#### Cited Findings
- 洞察: 小さい失敗入力はデバッグを速くし、無関係な細部を除き、同じバグの縮小例どうしが似てくる（重複判定に効く）。元の非公開コードを隠せるので外部報告がしやすい（本文確認） — [blog.regehr.org](https://blog.regehr.org/archives/1678)
- 意図: Delta Debugging の系譜。外部の「interestingness test」（多くはシェルスクリプト）が、候補がまだバグを起こすかを判定する。実行時間より最終出力の小ささを優先（本文確認） — 同上
- 洞察（失敗モード）: 誤コンパイルのバグでは、縮小が未定義動作を持ち込み、別の（不正な）テストケースに変わる。積極的に防がないと「ほぼ確実に」持ち込む。interestingness test に抜け穴があればそこを突く（例: 空ファイルを受け入れる）。暴れるパスは放棄する（本文確認） — 同上

#### Inferences
- 「最小再現」は理解に効くが、縮小で「同じバグ」かどうかの判定条件を明示しないと別のバグに化ける。最小再現には、何を保存したか（判定条件）を添える必要がある。

### 2.9 O'Callahan — rr / Pernosco

#### Cited Findings
- 意図: 一度記録して、後から好きなだけデバッグする。バグを何度も再現する必要がない。記録は CI を含む任意の機械で可能（本文確認） — [pernos.co](https://pernos.co/about/overview/)
- 意図: データ値を、複数のコピーや共有メモリをまたいで発生源まで辿る（従来のウォッチポイントは一段ずつ）。時間軸に沿った状態を事前計算し、呼び出し先も見せる。特定の関数・行の全実行を一括で問い合わせる（本文確認） — 同上
- 意図: 従来のデバッグの進捗は見えず、一時的で共有しにくい。Pernosco はセッションとノートブックを共有して共同で理解する（本文確認） — 同上

#### Inferences
- 「再現の一回性」と「調査の共有不能性」を同時に解いている。issue 理解の仕組みにとって、再現記録とその上の調査ノートを issue に添付できる形は参考になる。

### 2.10 Julia Evans — A debugging manifesto

#### Cited Findings
- 8 項目: Inspect, don't squash / Being stuck is temporary / Trust nobody and nothing / It's probably your code / Don't go it alone / There's always a reason / Build your toolkit / It can be an adventure（本文確認、見出しは WebFetch の要約経由） — [jvns.ca](https://jvns.ca/blog/2022/12/08/a-debugging-manifesto/)
- 洞察: バグはメンタルモデルの誤りを示す。「ランダム」な挙動にも理由がある（同上）

---

## 3. 失敗した・捨てられたアプローチと、その理由

### Takeaway
最も明確な失敗は「疑わしい文の順位リスト」。理由は一貫していて、(1) 位置を見ても理解は終わらない、(2) 説明がないと信頼されない、(3) 人の仮説・検索語と結びつかない、(4) 導入コストが節約を上回る。

### Cited Findings
- 順位付き故障位置特定: 順位の改善が成績に効かず、「完全なバグ理解」仮定が成り立たない（Parnin & Orso、本文確認） — [PDF](https://web.eecs.umich.edu/~weimerw/2018-481/readings/debugging-helping.pdf)
- 故障位置の提示: 正しい仮説も修正成功も増やさない（Alaboudi & LaToza、本文確認） — [arXiv PDF](https://arxiv.org/pdf/2005.13652)
- 実務での不使用: 実務者の多くは統計的故障位置特定ツールを使ったことがない。自動化はほぼなく、手作業・場当たり的（Böhme ら、本文確認） — [PDF](https://www.st.cs.uni-saarland.de/debugging/dbgbench/dbgbench.pdf)
- 位置ベースの評価そのもの: 研究評価が割合順位だったことへの批判（絶対順位で評価せよ）（Parnin & Orso、本文確認）。DBGBench は位置でなく「診断」を正解に据え直した（本文確認）
- 行・変数・式を先に選ばせる道具（ブレークポイント、スライス、問い合わせ）: 選択が外れれば答えも外れる（Ko & Myers、本文確認） — [PDF](https://faculty.washington.edu/ajko/papers/Ko2008JavaWhyline.pdf)
- 高度なデバッガ機能: 知識・利用ともに低く、printf が残る（Beller ら、本文確認） — [PDF](https://www.spinellis.gr/pubs/conf/2018-ICSE-debugging-analysis/html/BSSZ18.pdf)
- テスト通過による修正の検証: 通過パッチの 4 割が誤り（Böhme ら、本文確認）
- 素朴なテストケース縮小: 未定義動作の混入、判定条件の抜け穴で別物に化ける（Regehr、本文確認） — [blog.regehr.org](https://blog.regehr.org/archives/1678)

### Inferences
- 「位置」から「説明」へ、「答えを出す」から「問いと仮説を構造化する」への移動が、研究コミュニティ内部の自己修正として起きている。

---

## 4. 「このバグを理解・評価する」仕組みの設計原則の候補（調査者の推論）

以下はすべて上の知見からの推論で、検証されていない。

1. **報告を「why did / why didn't」に正規化する**（Ko & Myers）。観察された挙動と期待される挙動を対で書かせる。Bettenburg の調査では「期待される挙動」は重視度 22% と低いが、Whyline の why didn't は期待なしには問えない。
2. **観察と推論を分ける**。観察（入力・出力・ログ・再現環境）と仮説を別の欄にし、仮説には番号と「確かめ方」を付ける（Zeller の記録表、Alaboudi & LaToza の Hypothesis / How To Test）。
3. **候補を出すなら位置でなく仮説として出し、根拠を辿れるようにする**。位置だけの提示は効かなかった。候補にはどのテスト・値・依存から来たかを付ける（Parnin & Orso）。
4. **仮説の履歴を残し、新しい仮説を過去の観察と照合する**（マスターマインド）。誤った初期仮説は約 9 割（Ko）・正解率 11%（Alaboudi）なので、棄却された仮説も記録として価値がある。
5. **再現を最初の一級成果物にする**。再現に修正と同程度の時間がかかる（Böhme）。記録再生（rr）のように再現を一度で済ませ、共有可能にする。
6. **最小再現には保存条件を添える**（Regehr）。何を「同じバグ」とみなしたかを明示しないと縮小で別のバグになる。
7. **妥当性・修正の評価は診断と照合する**。テスト通過は弱い（97% 通過、58% 正しい）。診断（因果の連鎖、3〜4 領域・10 文以下が多い）を明文化し、修正がそれに触れているかを見る（69% のみ一致）。
8. **影響範囲の判断には「再現する最も一般的な条件」を求める**（実務者の 23% が希望）。深刻度判断の材料になる。
9. **長いエピソードを支える**。時間の大半は少数の長い調査にある（Alaboudi & LaToza 2021）。中断・再開・引き継ぎ（Zeller）に耐える調査状態の保存。
10. **既存の作業経路（ログ・print・検索）に乗る**（Beller、Parnin & Orso の検索語の知見）。

---

## 5. 未確認事項

- Andreas Zeller『Why Programs Fail』の内容（感染連鎖、cause-effect chain の章など）は今回開いていない（未確認・記憶）。
- Delta Debugging（Zeller & Hildebrandt, TSE 2002）の原論文は今回開いていない（未確認・記憶）。
- Agans の 9 ルール（Understand the system / Make it fail / Quit thinking and look / Divide and conquer / Change one thing at a time / Keep an audit trail / Check the plug / Get a fresh view / If you didn't fix it, it ain't fixed）は記憶によるもので、公式サイトの本文では確認できなかった（未確認・記憶）。
- O'Callahan のブログでの全知デバッグに関する論考は 503 で読めなかった。
- Perscheid/Hirschfeld（実務デバッグ調査）、Kochhar・Xia・Lo・Li「Practitioners' Expectations on Automated Fault Localization」（ISSTA 2016）は今回開いていない（未確認・記憶）。
- Bettenburg ら（2008）の数値は The Debugging Book 経由の二次資料。原論文は未確認。
- Beller らのスライドにある「デバッグセッションの 88% が 10 分未満」は検索要約のみで、論文本文で確認していない（検索要約のみ） — [検索で得たスライド](https://www.slideshare.net/inventitech/on-the-dichotomy-of-debugging-behavior-among-programmers)
- 熟練度差: Parnin & Orso（ツールで速くなったのは熟練者のみ、低成績者は順に巡回）と Whyline（初心者＋ツール ＞ 熟練者）以外に、熟練度差を正面から測った研究（例: Gugerty & Olson 1986）は今回確認していない。
