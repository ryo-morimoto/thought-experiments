# バグ報告・課題報告を「理解される対象」として研究した人々と、その資産

対象は PR ではなく、GitHub Issues / Bugzilla / Jira の課題・バグ報告。理解（再現・期待動作の確定・原因の所在）と評価（妥当性・重複・重大度・誰がどう扱うか）を助ける仕組みを作る人のための調査ノート。

確認の度合いの表記:
- 「本文確認」: PDF 本文を取得し、該当箇所を読んだ（pdftotext で抽出し grep・通読）。
- 「要旨のみ」: 要旨（abstract）か、著者・出版社ページの要約だけを読んだ。
- 「検索要約のみ」: 検索エンジンの要約だけで、一次資料は開けていない。
- 「記憶のみ・未確認」: 今回の調査で一次資料を開けていない。数値は書かない。

## 1. 鍵となる人物（誰を・なぜ・主な仕事）

### Takeaway
系譜は大きく三つある。(a) Saarland 大学 → Microsoft Research の Zimmermann・Bettenburg・Premraj・Just・Breu が 2008〜2010 年に「開発者が要る情報」と「報告者が出す情報」のずれを測った系譜。(b) Chaparro・Marcus・Moran・Poshyvanyk・Ng が、そのずれを OB/EB/S2R（観測動作・期待動作・再現手順）の単位まで分解し、検出器 → 品質評価 → 対話型報告（Burt）と道具を作り続けている系譜。(c) Kang・Yoo（LIBRO）や Mündler・Vechev（SWT-Bench）、Vijayvargiya・Neubig（Ambig-SWE）など、LLM に課題を「再現テスト」や「明確化の質問」に変換させる新しい系譜。並行して、Guo・Zimmermann・Nagappan・Murphy の Microsoft Windows 研究が「評価（どれが直され、誰に回り、再オープンされるか）」の社会的な側面を測っている。

### Cited Findings
<!-- data-source: original（調査ノートの整理） -->
| 人物 | なぜ重要か | 主な仕事（確認の度合い） |
| --- | --- | --- |
| Thomas Zimmermann（Microsoft Research） | 開発者と報告者のずれを最初に大規模に測り、以後の系譜の起点になった | "What Makes a Good Bug Report?" TSE 2010（本文確認） — [PDF](https://thomas-zimmermann.com/publications/files/zimmermann-tse-2010.pdf) |
| Nicolas Bettenburg / Rahul Premraj / Sascha Just | 上記の共著者。CUEZILLA（品質計）、infoZilla（スタックトレース等の抽出）、重複報告の価値の再評価 | "Duplicate Bug Reports Considered Harmful... Really?" ICSM 2008（本文確認） — [PDF](https://thomas-zimmermann.com/publications/files/bettenburg-icsm-2008.pdf) |
| Silvia Breu（＋Sillito, Premraj, Zimmermann） | コメントスレッド上の「質問」を 947 件集め、理解が時間とともにどう変わるかを示した | "Information Needs in Bug Reports" CSCW 2010（本文確認） — [PDF](https://thomas-zimmermann.com/publications/files/breu-cscw-2010.pdf) |
| Philip J. Guo（＋Zimmermann, Nagappan, Murphy） | 「どのバグが直されるか」「なぜ再割り当てされるか」「なぜ再オープンされるか」を Windows で測った。評価の社会的要因 | ICSE 2010（要旨のみ）— [要旨](https://pg.ucsd.edu/publications/Microsoft-Windows-which-bugs-get-fixed_ICSE-2010.txt)；CSCW 2011 再割り当て（本文確認）— [PDF](https://pg.ucsd.edu/publications/Microsoft-Windows-which-bugs-get-reassigned_CSCW-2011.pdf)；ICSE SEIP 2012 再オープン（検索要約のみ）— [MSR](https://www.microsoft.com/en-us/research/publication/characterizing-and-predicting-which-bugs-get-reopened/) |
| Oscar Chaparro（William & Mary） | OB/EB/S2R の欠落検出・品質評価・対話型報告を一貫して作り、評価している中心人物 | DeMIBuD FSE 2017、Euler FSE 2019、Burt FSE 2022（いずれも本文確認）、学位論文 — [publications](https://ojcchar.github.io/publications/8-fse17)、[dissertation](https://ojcchar.github.io/files/14-dissertation.pdf) |
| Andrian Marcus（UT Dallas → George Mason） | Chaparro の指導教員。上記すべての共著者 | 同上 |
| Kevin Moran / Denys Poshyvanyk | Android の GUI 解析で S2R を補う（FUSION、Euler、Burt の基盤） | Euler・Burt（本文確認）。FUSION（記憶のみ・未確認） |
| Vincent Ng（UT Dallas） | 自然言語処理側の共著者。談話パターンの抽出 | DeMIBuD、Euler（本文確認） |
| Mona Erfani Joorabchi / Ali Mesbah（UBC） | 「再現できない」報告の原因分類 | "Works for Me!" MSR 2014（本文確認）— [PDF](https://people.ece.ubc.ca/amesbah/resources/papers/mona-msr14.pdf) |
| Mohammad Masudur Rahman / Foutse Khomh / Marco Castelluccio | Joorabchi の追試・対比（Mozilla の実務者を含む） | "Works for Me! Cannot Reproduce" EMSE 2022（検索要約のみ）— [Springer](https://link.springer.com/10.1007/s10664-022-10153-2) |
| Jorge Aranda / Gina Venolia | リポジトリだけでは「バグの物語」が再構成できないことを示した | "The Secret Life of Bugs" ICSE 2009（要旨のみ）— [MSR](https://www.microsoft.com/en-us/research/publication/the-secret-life-of-bugs-going-past-the-errors-and-omissions-in-software-repositories/) |
| Sungmin Kang / Juyeon Yoon / Shin Yoo（KAIST） | 報告から LLM で再現テストを作る LIBRO。「確からしいときだけ提示する」設計 | ICSE 2023（本文確認）— [arXiv](https://arxiv.org/abs/2209.11515) |
| Niels Mündler / Mark Niklas Müller / Martin Vechev（ETH） | 課題 → 再現テストのベンチマーク SWT-Bench | NeurIPS 2024 系（本文の要旨部確認）— [arXiv](https://arxiv.org/abs/2406.12952) |
| Sanidhya Vijayvargiya / Graham Neubig（CMU） | 課題文の曖昧さを検出し、質問して補う能力の評価 | Ambig-SWE, ICLR 2026（要旨確認）— [arXiv](https://arxiv.org/abs/2502.13069) |
| Emre Sülün / Eray Tüzün（Bilkent）、Zhixing Li / Yue Yu ほか | GitHub の課題テンプレートの効果 | TOSEM 2024（検索要約のみ）— [Bilkent](https://repository.bilkent.edu.tr/items/a0c0b7c6-621e-4ca8-b17f-2843dfa072bf)；TSE 2022（検索要約のみ）— [PDF](https://yuyue.github.io/res/paper/template-TSE2022.pdf) |
| John Anvik / Gail Murphy | トリアージ（誰に割り当てるか）の推薦の起点 | "Who Should Fix This Bug?" ICSE 2006（記憶のみ・未確認。PDF の取得に失敗） |
| Chengnian Sun / David Lo | 重複報告の検出（REP など） | （記憶のみ・未確認） |
| Andrew J. Ko | 利用者が問題をどう言葉にするか、オープンなバグ報告での「パワーユーザー」の役割 | Ko & Chilana CHI 2010 ほか（記憶のみ・未確認。PDF の取得に失敗） |

### Inferences
- 「人」で見ると、Zimmermann 系（2008〜2012）が問いを立て、Chaparro 系（2017〜）がそれを道具に落とし、LLM 系（2023〜）が「再現テスト」「明確化質問」という別の出力形式に移した、という流れになる。三つの系譜を通して残っている問いは「報告者が出せない情報を、誰が・いつ補うか」。

### Gaps
- Anvik、Sun/Lo、Ko、Moran の FUSION は、今回 PDF を取得できず数値を確認していない（第 5 節）。
- Tao Xie は今回の範囲では、バグ報告の理解に関する代表的な一次資料を特定できなかった。

## 2. 研究が示すこと: 情報ニーズ、ずれ、理解しにくいバグ、スレッドでの理解の変化

### Takeaway
開発者が最も必要とするのは再現手順で、次がスタックトレースとテストケース。どれも報告者には出しにくい。報告者は何が要るかを知っているが、出せていない（知識ではなく収集の難しさの問題）。遅れの最大の原因は「誤った情報」より「欠けている情報」。理解に要る情報はバグの一生のなかで変わり、初期は欠落情報と原因の特定、後期は修正と状況確認の質問になる。「再現できない」報告の最大の原因は欠落ではなく、別の修正で直っていたこと（バグ間の依存）だった。

### Cited Findings

**Zimmermann, Premraj, Bettenburg, Just ほか "What Makes a Good Bug Report?" TSE 2010（本文確認）** — [PDF](https://thomas-zimmermann.com/publications/files/zimmermann-tse-2010.pdf)
- 知識: Apache・Eclipse・Mozilla で、開発者 156 件、報告者を合わせて計 466 件の回答。整合性検査で開発者 156 件中 26 件（16.7%）を除外した。
- 知識: 開発者が最もよく使う項目は再現手順・観測/期待動作・スタックトレース・テストケース。重要度では再現手順が抜きん出ていて、次がスタックトレースとテストケース。期待動作、要約、必須欄（バージョン・OS・製品・ハードウェア）は「比較的低い」重要度だった。
- 知識: 開発者が使うものと報告者が出すものの順位相関は Spearman 0.321、開発者が重要とするものと報告者が出すものでは 0.035。一方、報告者が「役立つと思うもの」と開発者の重要度は 0.839。原文 "ignorance of reporters is not a reason for the aforementioned information mismatch"。
- 知識: 報告者にとってテストケースが最も出しにくく、再現手順とコンポーネントも出しにくい。コンポーネントは「どこで起きたか報告者には分からない」という声があった。
- 知識: 開発者が最もよく遭遇した問題は情報の欠落。最も深刻なのは再現手順の誤りと情報の欠落。開発者の声 "The biggest causes of delay are not wrong information, but absent information."
- 洞察: 重複報告は、先行研究が言うほど開発者を困らせていなかった。別の書き方の報告が役立つこともあるため。
- 意図: 報告者に入力中に何が重要かを伝え（例: スクリーンショット）、同時に capture/replay のような収集を助ける道具を BTS に統合すべき、と結論した。

**Breu, Premraj, Sillito, Zimmermann "Information Needs in Bug Reports" CSCW 2010（本文確認）** — [PDF](https://thomas-zimmermann.com/publications/files/breu-cscw-2010.pdf)
- 知識: Eclipse と Mozilla の 600 件の報告から 947 件の質問を抽出し、8 カテゴリ・40 サブカテゴリに分けた。修正（Correction）は "by far the largest category"、デバッグは 2 番目、欠落情報は 3 番目に大きい（本文の明記）。件数は 240 件（25.3%）、176 件（18.6%）、143 件（15.1%）、114 件（12.0%）、94 件（9.9%）、80 件（8.4%）、68 件（7.2%）、25 件（2.6%）。この順位の明記から、修正 240、デバッグ 176、欠落情報 143 と対応する。残りは本文の配置から、明確化 114、トリアージ 94（重複か否か・誰が直すか）、状況確認 80、解決 68、プロセス 25 と読んだ（2 段組の PDF からの抽出で、件数とカテゴリの対応は配置による推定）。
- 知識: 940 件の質問のうち 11.3% が投稿後 1 時間以内、35.9% が 1 日以内に出た。解決済みの報告では 65.8% がバグの寿命の前半に出た。
- 知識: 940 件中 636 件（67.66%）に応答があった。応答のうち 34.2% が 1 時間以内、79.4% が 1 日以内。Mozilla では利用者に向けた質問の 50.0% が未回答だった。
- 洞察: 初期は欠落情報やデバッグの詳細（原因の場所を突き止めるため）の質問が多く、後期は修正と状況確認に移る。著者はこれを "evolving information needs" と呼ぶ。
- 意図: 報告の状態とは別に「議論の状態」を明示する（重要な質問に印をつけ、"answers pending" 状態にする。情報不足で止まっているバグを専用ダッシュボードに集める）。報告フォームが「情報を出すこと」を強調し「やりとり」を強調していないため、報告者は報告したら仕事は終わったと感じる、という指摘。
- 洞察: 利用者が開発者の専門用語を理解できず、「一緒に取り組んでほしい」という明示的な依頼が要る、という解釈（著者の推測として書かれている）。

**Chaparro ほか "Detecting Missing Information in Bug Descriptions"（DeMIBuD）ESEC/FSE 2017（本文確認）** — [PDF](https://vince-nlp.github.io/papers/fse17.pdf)
- 知識: 約 3k 件の報告を手作業で分析。OB は 93.5% に含まれるが、EB を明示的に書くのは 35.2%、S2R は 51.4%。三つすべてを含むのは 22.1%。
- 知識: 報告者は 154 個の談話パターンを繰り返し使う。EB は "should" "shall" を含む文が EB を書く報告の 44.2% に現れる。
- 知識: 最良の設定で、欠落 EB を平均適合率 85.9%・再現率 93.2%、欠落 S2R を 69.2%・83% で検出した。
- 意図: 報告時に報告者へ欠落を警告することで、記述の質を上げることを狙う。

**Joorabchi, Mirzaaghaei, Mesbah "Works for Me! Characterizing Non-Reproducible Bug Reports" MSR 2014（本文確認）** — [PDF](https://people.ece.ubc.ca/amesbah/resources/papers/mona-msr14.pdf)
- 知識: 産業 1・OSS 5 のリポジトリで再現不能（NR）報告 32K 件を集め、1,643 件を原因で分類した。NR は全報告の平均 17%。他の解決状態の報告より約 3 か月長く開いていて、議論量と関与者数は同程度。
- 知識: 原因の内訳: バグ間の依存（別の修正で暗黙に直った、どのパッチで直ったか不明、重複の可能性）45%、環境の違い 24%、情報不足 14%、期待の食い違い 12%、非決定的な振る舞い 3%。
- 知識: NR の 68% は初期状態（New/Open）から直接解決された。後に Fixed になるのは 3% だけで、そのうち 66% は実際に再現され、コード修正で直された。
- 洞察: 「期待の食い違い」には、仕様どおりの動作の誤解（文書の欠如）、サポート外機能、要求の変更が含まれる。つまり「期待動作の確定」の失敗が、再現の失敗として表に出る。

**Bettenburg, Premraj, Zimmermann, Kim "Duplicate Bug Reports Considered Harmful... Really?" ICSM 2008（本文確認）** — [PDF](https://thomas-zimmermann.com/publications/files/bettenburg-icsm-2008.pdf)
- 知識: Anvik らの数字を引用し、Mozilla の約 30%、Eclipse の約 20% が重複。Eclipse では、同じタイトル・説明・製品・コンポーネントで、同じ利用者が 10 分以内に再送した「誤送信」由来の重複が 521 件。
- 洞察: 重複が生まれる理由: 検索の手間を惜しむ・不慣れ、検索機能の弱さ（ある報告は約 900 日間に 33 人が報告）、一つの欠陥が複数の故障として現れる、修正されないことへの苛立ちによる意図的な再送、二重送信。
- 意図: 重複を別扱いにせず、主報告に統合すべきと提案した。重複は追加情報を持ち込み、自動トリアージの精度も上がる。

**Guo, Zimmermann, Nagappan, Murphy（Microsoft Windows）**
- 知識（要旨のみ）: 評判の良い人が報告したバグ、同じチーム・近い場所の人が扱ったバグほど直されやすい。358 人の Microsoft 社員への調査で裏付けた。Vista で学習したモデルは Windows 7 の修正を適合率 68%・再現率 64% で予測した。報告者の年次や対人スキルも影響すると回答があった — [要旨](https://pg.ucsd.edu/publications/Microsoft-Windows-which-bugs-get-fixed_ICSE-2010.txt)
- 洞察（本文確認）: 再割り当ては常に有害ではなく、最適な担当者を見つけるのに役立つ。主な理由は五つ: 根本原因の探索、所有の決定、報告の質の低さ、適切な修正の決めにくさ、負荷分散。最も多いのは根本原因の探索で、報告者には根本原因を突き止める専門性がないことが多い — [PDF](https://pg.ucsd.edu/publications/Microsoft-Windows-which-bugs-get-reassigned_CSCW-2011.pdf)
- 再オープン（検索要約のみ）: 358 人の調査と大規模な定量分析で再オープンの主因を分類し、ICSE SEIP 2012 の最優秀論文賞 — [MSR](https://www.microsoft.com/en-us/research/publication/characterizing-and-predicting-which-bugs-get-reopened/)

**Aranda & Venolia "The Secret Life of Bugs" ICSE 2009（要旨のみ）** — [MSR](https://www.microsoft.com/en-us/research/publication/the-secret-life-of-bugs-going-past-the-errors-and-omissions-in-software-repositories/)
- 洞察: 単純なバグの履歴でさえ、社会的・組織的・技術的な知識に強く依存していて、電子的なリポジトリの自動処理だけでは取り出せない。リポジトリの調整の記録は "incomplete and often erroneous"。

### Inferences
- 「理解」の主要な障害は、報告者の無知ではなく収集の難しさ（Zimmermann の相関 0.839 対 0.035）。したがって「もっと書け」と促すより、収集を代行する（ログ・スタックトレース・環境の自動取得、GUI 操作の記録）ほうが筋がよい。
- 「再現できない」の半分近くは、報告の質の問題ではなく、すでに別の修正で直っていた（Joorabchi 45%）。評価の仕組みは、報告を単独で見るのではなく、近い時期の修正や類似報告と突き合わせる必要がある。
- 期待動作（EB）は開発者の重要度では低く出た（Zimmermann）が、明示されるのは 35.2% だけ（Chaparro）で、再現不能の 12% は期待の食い違いだった（Joorabchi）。開発者は OB から EB を推測できると思っているが、その推測が外れると「仕様どおり」「再現できない」で閉じられる、と読める（推論）。
- 理解はスレッドのなかで変わる（Breu）。「理解支援」は報告の時点だけでなく、スレッドの各時点で「いま何が分かっていて、何が未回答か」を示す形が要る。

### Gaps
- コメントスレッドを通して理解（再現の成否、原因の仮説）がどう収束していくかを時系列で追った研究は、Breu の質問分析以外に一次資料で確認できなかった。
- Zimmermann 2010 の調査は 2008 年の Apache・Eclipse・Mozilla が対象。GitHub Issues 中心の現在の OSS や、企業の Jira で同じずれがあるかは確認していない。
- 重大度・優先度の判定の妥当性を扱う研究（重大度予測など）は今回確認していない。

## 3. 作られた道具・試作品と、その成否・放棄

### Takeaway
道具は「品質を測る」→「欠落を警告する」→「対話で引き出す」→「LLM が再現テストに変換する」と進んだ。品質計 CUEZILLA は精度 43〜50% で、利用者評価の前に止まった。欠落検出（DeMIBuD）と品質評価（Euler）は精度が上がったが、評価は外部評価者による注釈の正しさまで。対話型の Burt は利用者評価でテンプレートより良い S2R を集めたが、「何が起きたか（OB）」を画面と結びつけるのは 54 会話中 3 件しか正しくできなかった。LLM 系は「確からしいときだけ提示する」「生成した再現テストを修正の検証に使う」という設計に収束しつつある。

### Cited Findings

**CUEZILLA（Zimmermann ほか TSE 2010、本文確認）** — [PDF](https://thomas-zimmermann.com/publications/files/zimmermann-tse-2010.pdf)
- 知識: 開発者が評価した 289 件で学習。プロジェクト内評価の最良精度は Apache 50%（線形カーネル SVM 回帰）、Mozilla 43%（RBF カーネル SVM 分類）、Eclipse 45%（決定木）。12 のモデルで明確な勝者はなかった。
- 意図: 報告中に品質メーターを見せ、何を足せばよいかを推薦し、履歴から掘った事実（例: スタックトレース付きの報告は早く直る）を動機づけとして示す。モックアップのみ。
- 失敗・中断: 原文 "the presented version of CUEZILLA is an early prototype and we plan to further enhance the accuracy before we will conduct user studies"。利用者評価は行われていない（後続の利用者評価は今回見つけていない）。

**infoZilla（Bettenburg ほか）**
- パッチ・スクリーンショット・スタックトレースを報告から「確実に」抽出できる道具として TSE 2010 で使われた（本文確認）。単独の評価は今回確認していない。

**DeMIBuD（FSE 2017、本文確認）** — [PDF](https://vince-nlp.github.io/papers/fse17.pdf)
- 欠落 EB/S2R の検出（数値は第 2 節）。意図は報告時の警告。報告者の行動が変わったかの利用者評価は、この論文には含まれない。

**Euler（Chaparro ほか ESEC/FSE 2019、本文確認）** — [arXiv](https://arxiv.org/abs/1906.07107)
- 知識: 外部評価者の判定で、既存の S2R の 98%、欠落した S2R の 58% を特定し、品質注釈の 73% が正しかった。
- 意図: 各手順をアプリの GUI 実行モデルに対応づけ、「曖昧な手順」「語彙の不一致（アプリの用語と違う）」「欠落した手順」を報告者に返す。報告時に書き直しを促し、開発者には欠落した手順を補って渡す、という二つの使い方を想定。
- 洞察: 語彙の不一致の誤検出は、一つの手順に複数の操作が含まれる場合に起きた。

**Burt（Song ほか ESEC/FSE 2022、本文確認）** — [PDF](https://ojcchar.github.io/files/21-fse22-burt.pdf)；デモ ICSE 2023（本文確認）— [arXiv](https://arxiv.org/abs/2302.06050)
- 知識: Android 向けの対話型の報告チャットボット。36 人の利用者が 6 アプリの 12 バグを報告。テンプレート型の Web フォーム（Itrac）と比べ、Burt の報告は S2R の質が高く、EB は同程度。
- 失敗: OB の記述を正しい 1 画面に対応づけられたのは 54 会話中 3 件（5.5%）。複数画面への対応づけは 35 件（64.8%）。Burt の 18 件の報告のうち 14 件で、利用者は最初に OB/EB を誤って書き、Burt が言い直しを促したが、それでも誤ったまま報告された。著者の結論は、OB の収集の改善が必要。原因は OB/EB の言い回しへの対応の限界。
- 意図: 対話システムの構造で、報告者と開発者の知識の差を埋める。初心者ほど効くと予想したが、その予想の検証は「新人と経験者」の比較として書かれている（結果の詳細は未読）。

**課題テンプレート（検索要約のみ）**
- Sülün ほか TOSEM 2024: 大規模 100 プロジェクトのうち 99 がテンプレートを使い、YAML のフォームが増えている。テンプレートのあるプロジェクトは解決時間が短く、YAML 形式はさらに解決時間・再オープン・議論の長さの減少と関連。保守者の 85% が利点に同意 — [Bilkent](https://repository.bilkent.edu.tr/items/a0c0b7c6-621e-4ca8-b17f-2843dfa072bf)。相関で因果ではない。
- Li ほか TSE 2022: 802 の人気プロジェクトで、課題・PR テンプレートの内容・影響・受け止め方を混合手法で調査 — [PDF](https://yuyue.github.io/res/paper/template-TSE2022.pdf)
- テンプレートの自動生成（GIRT-Model）もある — [arXiv](https://arxiv.org/pdf/2402.02632)（検索要約のみ）

**LLM 系**
- LIBRO（Kang, Yoon, Yoo ICSE 2023、本文の要旨・導入確認）: Defects4J の 750 件中 251 件（33%）で失敗を再現するテストを生成し、149 件で 1 位に提示。学習データ締め切り後の 31 件では 32%。意図は "suggest generated tests to the developer only when the results are reliable"（確からしいときだけ提示）— [arXiv](https://arxiv.org/abs/2209.11515)。Codex の廃止で既定を GPT-3.5 に変えた（検索要約のみ）— [repo](https://github.com/coinse/libro)
- Google での追試（検索要約のみ）: 社内課題トラッカーの人間が報告した 80 件で、エージェント方式は妥当な再現テストを 28% 生成、LIBRO は 10% — [arXiv](https://arxiv.org/abs/2502.01821)
- SWT-Bench（Mündler ほか、要旨確認）: 課題をテストに「形式化」する能力のベンチマーク。修正用のコードエージェントがテスト生成専用の手法を上回り、生成テストで修正案を絞ると SWE-agent の適合率が 2 倍になる。導入で、課題の再現は職業開発者に嫌われがちだと引用している — [arXiv](https://arxiv.org/abs/2406.12952)
- Ambig-SWE（Vijayvargiya ほか ICLR 2026、要旨確認）: SWE-bench Verified の課題文を曖昧にした版。モデルは十分に指定された指示と曖昧な指示を見分けるのが苦手だが、曖昧な入力で利用者とやりとりすると、非対話より最大 74% 性能が上がる — [arXiv](https://arxiv.org/abs/2502.13069)
- SWE-bench Verified（検索要約のみ）: 93 人の開発者が 1,699 件を注釈し、課題文が不十分に指定されているものやテストが厳しすぎるものを除いて 500 件にした — [OpenAI](https://openai.com/index/introducing-swe-bench-verified/)。不十分と判定された割合の数値は確認できていない。

### Inferences
- 放棄・停滞のパターン: (1) 品質を一つのスコアにする試み（CUEZILLA）は、開発者の評価を真似る精度が低く、利用者評価に進まなかった。(2) 後継は「スコア」をやめ、「どの要素（EB/S2R）が欠けているか」「どの手順が曖昧か」という個別の指摘に変えた。これは設計の意図の転換と読める（推論。著者がそう明言した箇所は確認していない）。
- 「何が起きたか（OB）」の把握が対話でも最も難しい（Burt）。利用者は症状をうまく言語化できず、誤った OB のまま報告が通る。理解支援の仕組みは、OB を言葉だけでなく画面・ログ・録画で受け取る必要がある。
- LLM 系は「理解」を「失敗する再現テスト」という検証可能な形に変えることで、理解の正しさを確かめられるようにした。これは、品質スコアが「開発者の主観の評価」を真似るしかなかった時代との大きな違い。

### Gaps
- DeMIBuD や Euler が実際のバグトラッカーに組み込まれ、継続して使われたかどうかは確認できなかった（研究試作で終わった可能性が高いが、未確認）。
- Burt の GitHub リポジトリの保守状況は確認していない。
- テンプレートの研究は相関で、テンプレートが報告の理解しやすさそのものを上げたかは分からない。

## 4. 「この課題を理解・評価する」仕組みの設計原則の候補

### Takeaway
一次資料から導ける原則は七つ。どれも「報告を一つの文書として採点する」のではなく、「欠けている要素・未回答の問い・関連する修正」を個別に示し、検証可能な形（再現テスト）に変えることを指す。

### Cited Findings（原則と根拠）
1. **再現手順を中心に置き、欠落は要素ごとに示す。** 開発者の重要度で再現手順が抜きん出ている（[Zimmermann 2010](https://thomas-zimmermann.com/publications/files/zimmermann-tse-2010.pdf)）。EB 35.2%、S2R 51.4% しか明示されない（[DeMIBuD](https://vince-nlp.github.io/papers/fse17.pdf)）。単一の品質スコアは精度 43〜50% で止まった（CUEZILLA）。
2. **報告者に「書け」と言うより、収集を代行する。** 報告者は何が要るかを知っている（相関 0.839）が、出せていない（0.035）。スタックトレースはログに埋もれ、テストケースは最も出しにくい（[Zimmermann 2010](https://thomas-zimmermann.com/publications/files/zimmermann-tse-2010.pdf)）。
3. **報告の状態とは別に「議論の状態」を持つ。** 未回答の質問、誰に向けた質問かを明示する（"answers pending"）。Mozilla では利用者向けの質問の 50% が未回答だった（[Breu 2010](https://thomas-zimmermann.com/publications/files/breu-cscw-2010.pdf)）。
4. **理解の段階に応じて表示を変える。** 初期は欠落情報と原因の特定、後期は修正と状況（[Breu 2010](https://thomas-zimmermann.com/publications/files/breu-cscw-2010.pdf)）。
5. **「再現できない」と判定する前に、近い修正・類似報告・環境の差を突き合わせる。** NR の 45% は別の修正で直っていた、24% は環境の違い（[Joorabchi 2014](https://people.ece.ubc.ca/amesbah/resources/papers/mona-msr14.pdf)）。
6. **重複は捨てずに統合し、追加情報として使う。** 重複は開発者をそれほど困らせず、情報を足す（[Bettenburg 2008](https://thomas-zimmermann.com/publications/files/bettenburg-icsm-2008.pdf)）。
7. **理解を検証可能な形（失敗する再現テスト）にし、確からしいときだけ提示する。** LIBRO の設計意図（[arXiv](https://arxiv.org/abs/2209.11515)）。生成テストは修正案の絞り込みに効く（[SWT-Bench](https://arxiv.org/abs/2406.12952)）。曖昧なら推測せず質問する（[Ambig-SWE](https://arxiv.org/abs/2502.13069)）。

### Inferences
- 追加の候補（推論）: 「期待動作」を明示的に確定する欄・手順を持つ。EB は開発者に低く見積もられるが、食い違うと「仕様どおり」「再現できない」で閉じられる（第 2 節の推論）。
- 追加の候補（推論）: 担当者の推薦は「誰が直せるか」だけでなく「根本原因がどこにありそうか」「所有が不明確か」を示す。再割り当ての主因が根本原因の探索と所有の決定だったため（[Guo CSCW 2011](https://pg.ucsd.edu/publications/Microsoft-Windows-which-bugs-get-reassigned_CSCW-2011.pdf)）。
- 注意（推論）: 評価（直されるか）には報告者の評判や組織の近さが効く（[Guo ICSE 2010](https://pg.ucsd.edu/publications/Microsoft-Windows-which-bugs-get-fixed_ICSE-2010.txt)）。これを予測に使うと、新参の報告者の正しい報告を下げる偏りを仕組みに埋め込む恐れがある。
- 注意（推論）: リポジトリの記録は不完全で誤りを含む（[Aranda & Venolia](https://www.microsoft.com/en-us/research/publication/the-secret-life-of-bugs-going-past-the-errors-and-omissions-in-software-repositories/)）。課題の文章とコメントだけから理解を組み立てる仕組みには上限がある。

### Gaps
- 上の原則のうち、実運用で効果が測られたのはテンプレート（相関）と Burt（小規模の利用者評価）くらい。他は研究の知見からの推論。

## 5. 未検証の事項（要旨のみ・検索要約のみ・記憶のみ）

### Takeaway
次の項目は、今回一次資料の本文で確かめていない。報告に使うときは確認の度合いを添えること。

### Cited Findings
- Joorabchi の 6 つ目の原因カテゴリの名前と割合: 本文の要約部では 5 つ（計 98%）しか挙げられておらず、6 つ目を確認していない — [PDF](https://people.ece.ubc.ca/amesbah/resources/papers/mona-msr14.pdf)
- Rahman・Khomh・Castelluccio EMSE 2022 が Joorabchi の結果とどう対比したか（検索要約のみ）— [Springer](https://link.springer.com/10.1007/s10664-022-10153-2)
- 再オープンの主因の一覧と割合（ICSE SEIP 2012、検索要約のみ）— [MSR](https://www.microsoft.com/en-us/research/publication/characterizing-and-predicting-which-bugs-get-reopened/)
- SWE-bench Verified で「不十分に指定」と判定された割合（数値未確認）— [OpenAI](https://openai.com/index/introducing-swe-bench-verified/)
- 課題テンプレートの効果の詳細な数値（検索要約のみ）— [Bilkent](https://repository.bilkent.edu.tr/items/a0c0b7c6-621e-4ca8-b17f-2843dfa072bf)

### Inferences
- 記憶のみ・未確認（URL なし。今回 PDF を取得できなかった、または探さなかった）: Anvik, Hiew, Murphy "Who Should Fix This Bug?" ICSE 2006（担当者推薦）、Sun・Lo らの重複検出（REP ほか）、Moran ほか FUSION（Android の報告を自動補完）、Ko & Chilana CHI 2010（オープンなバグ報告でのパワーユーザーの役割）、Ko ほかの問題記述の言語分析、Herzig・Just・Zeller ICSE 2013（課題の種別の誤分類）、Rastkar・Murphy のバグ報告の要約。いずれも設計に関係しうるが、数値・結論はこのノートでは主張しない。

### Gaps
- Tao Xie、Aranda & Venolia の本文、Ko の仕事は、次の調査で一次資料を取得して確かめる必要がある。
