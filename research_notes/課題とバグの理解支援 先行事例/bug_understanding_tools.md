# 課題とバグの理解・評価を助ける道具を作った人々と、その資産

調査日: 2026-11-21。対象は PR ではなく issue／バグ報告の「再現・期待動作の確定・原因の特定・妥当性／重複／深刻度の判断・上流への報告の判断」を助ける仕組み。スター数では並べていない。

表記: 無印は一次資料を取得して読んだもの。「検索要約のみ」は検索結果の要約しか見ていないもの。「要旨のみ」は論文の abstract だけを読んだもの。引用は英語の短い原文で、直後に URL を書く。

## 1. 人と道具の一覧

<!-- data-source: original（調査ノートの整理） -->
| 道具 | 人（役割） | 解く問題（一言） | 主な一次資料 |
| --- | --- | --- | --- |
| rr | Robert O'Callahan ほか（Mozilla 発、論文著者） | 再現しにくい失敗を一度記録し、決定的に再生する | arXiv 1705.05937（USENIX ATC 2017） |
| Pernosco | Robert O'Callahan, Kyle Huey（共同創業） | 記録から全状態を事前計算し「データ解析としてのデバッグ」と共有 | pernos.co/about, robert.ocallahan.org |
| Replay.io | Jason Laster（元 CEO）, Brian Hackett（共同創業・元 CTO→CEO） | ブラウザの記録・再生で、顧客の再現困難なバグを開発者に渡す | replay.io/blog |
| Undo LiveRecorder | Greg Law（共同創業） | テスト失敗・CI 失敗を記録して「再現し直す」必要をなくす | undo.io, docs.undo.io（検索要約のみ） |
| Microsoft TTD | Microsoft（WinDbg チーム） | 巻き戻し可能な記録で、再現の繰り返しをなくす | learn.microsoft.com, MSRC blog（検索要約のみ） |
| Sentry の issue grouping | David Cramer（創業者）; AI grouping は Tillman Elser, Josh Ferge | 大量のエラーイベントを「1 issue」にまとめる（fingerprint） | docs.sentry.io, blog.sentry.io |
| Honeycomb / BubbleUp | Charity Majors, Christine Yen（共同創業） | 予測できない「未知の未知」の失敗を、事前に問いを決めずに調べる | honeycomb.io（一部検索要約のみ） |
| BugBug | Marco Castelluccio, Sylvestre Ledru（Mozilla） | 毎日数百件の Firefox バグ報告の振り分けを ML で自動化 | hacks.mozilla.org 2019-04 |
| Socorro（crash-stats） | Mozilla | クラッシュ報告をシグネチャでまとめる | wiki.mozilla.org/Breakpad/SkipList（検索要約のみ） |
| ClusterFuzz / OSS-Fuzz | Google | ファズで見つけたクラッシュの重複排除・最小化・二分探索・修正確認・自動起票と自動クローズ | google.github.io/clusterfuzz |
| GitHub issue forms | GitHub | 必須項目のある構造化フォームで、情報不足の報告を減らす | GitHub changelog 2021-06-23 |
| SWE-bench Verified | OpenAI と SWE-bench 著者（Princeton） | issue の記述不足・テストの不当さを人手で注釈し、解けない課題を除く | openai.com/index/introducing-swe-bench-verified |
| LIBRO | Sungmin Kang, Juyeon Yoon, Shin Yoo（KAIST） | 一般のバグ報告から再現テストを LLM で生成し、いつ信じるかを決める | arXiv 2209.11515（ICSE 2023） |
| SWT-bench | Niels Mündler, Mark Niklas Müller, Jingxuan He, Martin Vechev（ETH） | issue→再現テストの能力を測る | arXiv 2406.12952 |
| Otter | Toufique Ahmed ほか（IBM の研究者と思われるが所属はページに記載なし） | 修正前に issue からテストを生成（TDD） | arXiv 2502.05368（ICML 2025） |
| Issue2Test | Nashid, Bouzenia, Pradel, Mesbah | issue に書かれた理由で失敗するテストを生成 | arXiv 2503.16320（ICSE 2026、検索要約のみ） |
| Agentless | Chunqiu Steven Xia ほか（UIUC） | 位置特定→修正→再現テストで検証、の単純な 3 段 | arXiv 2407.01489（要旨のみ） |
| AutoCodeRover / SpecRover | Yuntong Zhang, Haifeng Ruan, Abhik Roychoudhury（NUS） | 意図（仕様）を推定し、reproducer と reviewer で確信度を出す | arXiv 2404.05427, 2408.02232 |
| curl の AI 報告問題（反面教材） | Daniel Stenberg（curl 作者） | LLM 生成の偽バグ報告が保守者の時間を奪う | daniel.haxx.se 2024-01-02 |

## 2. 道具ごとの資産

### rr（Robert O'Callahan ほか）

- 問題: 記録と再生は逆実行デバッグや再現しにくいテスト失敗の診断に使えるが、既存手法は VM 全体の記録・カーネル改変・重い計装・コンパイラ改変を要し、配備しにくかった。 — [arXiv 1705.05937](https://arxiv.org/abs/1705.05937)（要旨のみ）
- 設計意図と捨てたもの: 全部ユーザ空間、既存のハードウェア・コンパイラ・OS のまま動くことを優先し、その代わり低並列のワークロードに限定した。"records and replays real-world low-parallelism workloads with low overhead" — [arXiv 1705.05937](https://arxiv.org/abs/1705.05937)
- 示唆: 「再現の道具」は、導入の手間（配備性）がそのまま採用を決める。機能を絞ってでも既存環境で動くことを選んだ。

### Pernosco（Robert O'Callahan, Kyle Huey）

- 問題と意図: "Record your program once and debug at your leisure"。全プログラム状態を事前計算し、値の出所（dataflow）を遡れるようにする。デバッグを "a data analysis problem" として扱う。 — [Pernosco overview](https://pernos.co/about/overview/)
- 再現と診断の分離: "Pernosco makes it convenient to separate _reproducing_ a bug from _debugging_ a bug"。QA が再現して記録をアップロードし、URL を開発者に渡す。URL は時点とスタックフレームを含み、ノートブックの記述が残って共有される。調査を詳しい人へ "forward" できる。 — [The Power Of Collaborative Debugging (2019-11-11)](https://robert.ocallahan.org/2019/11/the-power-of-collaborative-debugging.html)
  - 注意: 製品開発者自身による逸話で、計測結果はない（同記事）。
- 事業上の教訓（検索要約のみ）: 「デバッガは売れない」と何度も言われたという記述（2019 "Your Debugger Sucks"）。Pernosco を使うには rr の記録が要るので、rr だけで満足する人もいる、という 2024 年の講演の記述。対象は当初 x86-64 Linux と C/C++/Rust に限られた。 — [Your Debugger Sucks](https://robert.ocallahan.org/2019/11/your-debugger-sucks.html), [DEBT workshop 2024](https://robert.ocallahan.org/2024/10/debt-workshop.html), [Pernosco demo video](https://robert.ocallahan.org/2019/10/pernosco-demo-video.html)

### Replay.io（Jason Laster, Brian Hackett）— 2 度の方向転換

- 経緯（会社名義の投稿、2024-07-24）:
  - 2021 年秋: 顧客の再現困難な問題を開発者が再生できるよう、バグ報告向けに公開。利用者は機密データの記録と専用ブラウザの必要を懸念した。さらに **多くのバグは動画とネットワークリクエストがあれば再現でき、タイムトラベルデバッグの必要が下がった** と分かった。
  - 2022 年春: 不安定なブラウザテスト（flaky test）へ転換。しかし利用者は "most users were okay fixing the test so that it would pass eventually"（原因を調べるより、通るまでテストを直す）。
  - 2024-08-31 に Replay Test Suites を終了し、初の人員削減。"We started with a solution and have been searching for a problem." — [A new direction](https://www.replay.io/blog/a-new-direction)
- 2024-09-24、Brian Hackett が CEO に（Jason Laster は顧問へ）: "Replay's devtools have not had the impact we wanted." Chrome devtools で日常の問題は足り、Replay は最も難しいバグ用のニッチな道具になった。記録は実行のデータベースで、問い合わせを自動化できる。"Analysis is great at making tasks simpler, and AIs are great at doing simple tasks." 今後は先にデモを作り、重要な問題を解くと確信してから製品にする。 — [Changelog 67: Demos](https://www.replay.io/blog/changelog-67-demos)
- 示唆: 「理解の道具」は、利用者が実際に選ぶ最安の手段（動画＋ネットワークログ、テストの書き直し）と競争する。深い再生は、安価な証拠で足りない少数の問題にしか効かない。

### Undo LiveRecorder（Greg Law）（検索要約のみ）

- テスト失敗から、失敗の時点に置かれたタイムトラベルデバッガへ 1 クリックで行く流れ。記録があれば再現し直す必要がない。 — [undo.io](https://undo.io/?p=3714), [On Software Failure Replay. Q&A with Greg Law](https://odbms.org/?p=13538)
- テストとの統合は 3 通り: 全テストを記録して失敗分だけ残す（遅くなる）、失敗したテストを記録しながら再実行（間欠的な失敗には失敗するまで繰り返す）、通常実行の後に失敗分だけ記録して再実行。記録はストレージを圧迫し、全メモリ状態を含むので顧客の機密データを含みうる。 — [Recording test failures](https://docs.undo.io/java/integration/), [Workflow integration](https://docs.undo.io/LiveRecorderWorkflowIntegration.html)

### Microsoft Time Travel Debugging（検索要約のみ）

- 社内で、複雑な問題の根本原因を通常のデバッガの半分の時間で見つけられたという主張。記録は決定的なので、全員が同じ振る舞いを見る。 — [MSRC blog 2019-05](https://msrc.microsoft.com/blog/2019/05/time-travel-debugging-its-a-blast-from-the-past)
- 代償: 記録時に典型的に 10〜20 倍遅くなり、数分でトレースが数 GB になる。記録は機密データを含みうるので共有に注意。 — [TTD overview](https://learn.microsoft.com/windows-hardware/drivers/debugger/time-travel-debugging-overview), [TTD FAQ](https://learn.microsoft.com/en-us/archive/blogs/windbg/time-travel-debugging-faq)

### Sentry のイベントのまとめ方（grouping）

- 仕組み: 全イベントに fingerprint があり、同じ fingerprint のイベントが 1 issue。優先順は fingerprint → stack trace → exception → message。stack trace はアプリ自身のフレーム（in-app）だけを使う。stack trace がないと exception の type と value を使うが "a lot less reliable because of changing error messages"。 — [Sentry docs: Event Grouping](https://docs.sentry.io/concepts/data-management/event-grouping/)
- 版管理: グルーピングの変更は新しい版として出し、新しいイベントにだけ適用する（既存の issue のまとまりを壊さない）。 — 同上
- 既知の問題: 最小化された JS（source map が要る）、デコレータでフレームが増えるとまとまりがずれる。チャンク読み込みやハイドレーションのような揺れの大きいエラーには組み込みルール（"Sentry Defined Fingerprint"）。手動で merge/unmerge でき、unmerge したものは再びまとめない。 — 同上
- AI grouping（Tillman Elser, Josh Ferge, 2025-02-05）: 旧方式は "did not sufficiently group similar errors together"（フレームの並び替えや行番号のずれで重複 issue と重複アラート）。従来の fingerprint を先に走らせ、新しい hash だけを埋め込みで既存と比べる。閾値は "very conservative" にし、誤ってまとめる率は社内試験で "virtually zero"。新規 issue 約 40% 減、アラート約 40% 減、処理 100ms 未満。量子化はストレージを最大 32 倍減らしたが精度が落ちたので float32 のまま。 — [How Sentry decreased issue noise with AI](https://blog.sentry.io/how-sentry-decreased-issue-noise-with-ai)
  - docs: AI は新しい issue にだけ働き、fingerprint でまとめた既存の issue を分割しない。 — [Sentry docs](https://docs.sentry.io/concepts/data-management/event-grouping/)
  - 第 2 版（検索要約のみ）: 重複をさらに約 20% 防ぎ、誤った merge を半減。 — [Enhancing issue grouping](https://blog.sentry.io/enhancing-issue-grouping), [changelog](https://sentry.io/changelog/enhanced-issue-grouping)
- 示唆: 「同じ問題か」の判断は、誤って分けるより誤ってまとめる方が害が大きいとみなし、非対称に保守的にしている（記事は明言していないが、閾値と「分割しない」設計からの推論）。

### Honeycomb（Charity Majors, Christine Yen）（一部検索要約のみ）

- 取得した Honeycomb の記事（現行版は 2026-04-10 更新、著者 Emil Protalinski。創業者本人の文章ではない）: 観測可能性を "asking any question about its behavior without needing to predict those questions in advance" と定義。監視は事前定義の指標と閾値に依存し既知の問題向き。高カーディナリティのデータで、影響を受けた構成要素・取引・利用者を特定する。 — [Observability: What's in a Name?](https://www.honeycomb.io/blog/observability-whats-in-a-name)
- Charity Majors の「既知の未知から未知の未知へ」という言い方（検索要約のみ）。 — [Chaos Conf 2018 transcript](https://gremlin.com/blog/charity-majors-closing-the-loop-on-chaos-with-observability-chaos-conf-2018)
- BubbleUp（検索要約のみ）: ヒートマップで異常な領域を選ぶと、その部分集合が他とどの属性で違うかを差の大きい順に並べる。「どの属性を見ればよいか分からない」状態に応える。 — [BubbleUp](https://www.honeycomb.io/bubbleup), [identify outliers docs](https://docs.honeycomb.io/investigate/analyze/identify-outliers/)
- 示唆: 「原因の場所」の候補を、仮説なしに「正常群との差」として出す方法は、issue の理解にも転用できる（例: 報告者の環境と非報告者の環境の差）。

### Mozilla BugBug（Marco Castelluccio, Sylvestre Ledru）

- 問題: 毎日数百件の Firefox バグ報告。"Unfortunately, this process fails to scale" — [Teaching machines to triage Firefox bugs (2019-04-09)](https://hacks.mozilla.org/2019/04/teaching-machines-to-triage-firefox-bugs/)
- 設計: 20 年分の振り分け済みバグで XGBoost。題・最初のコメント・キーワード/フラグを特徴量に使う。学習時はバグを **起票時点の状態に巻き戻し**、振り分け後の情報が漏れないようにした。件数の少ないコンポーネントは除外。バグか機能要望かを分ける別モデルも先にあった。 — 同上
- 運用: 確信度がおよそ 60% を超えたときだけ自動で振り分け、検証集合で精度 80% 超。2019-02 下旬から約 350 件。重複検出や「再現手順がない」の検出へ広げられると述べる。 — 同上
- 関連研究（検索要約のみ）: Castelluccio らの再現不能バグの研究で引かれる数値として、約 65% の報告が期待動作を欠き、49% が再現手順を全く含まない。 — [non-reproducibility ICSME 2020](https://https-marco-c_github_io.proxy.bugsmash.io/publications/non_reproducibility-icsme2020.pdf)（プロキシ経由の URL で、原典は未確認）
- Mozilla の振り分け手引き（検索要約のみ）: 再現手順がなければ報告者に needinfo で求め、返答がなければ INCOMPLETE で閉じうる。BugBot は、バグとその重複の間で深刻度が食い違うと担当者に needinfo する。 — [triage-bugzilla.rst](https://firefox-source-docs.mozilla.org/_sources/bug-mgmt/policies/triage-bugzilla.rst.txt), [BugBot](https://wiki.mozilla.org/BugBot)

### Mozilla Socorro（crash-stats）のシグネチャ（検索要約のみ）

- クラッシュシグネチャはスタックの上位フレームから作り、無関係なフレーム（`mach_msg_trap`, `_sigtramp`, `std::__terminate` など）を飛ばすリスト（SkipList）で調整する。変更は毎週レビューされ、"every SkipList change affects our crash metrics"。過剰なまとめ（macOS の SIGABRT が 1 つのシグネチャに集まる）を分けるための依頼が繰り返し出ている。 — [Breakpad/SkipList](https://wiki.mozilla.org/Breakpad/SkipList), [Bug 1410580](https://bugzilla.mozilla.org/show_bug.cgi?id=1410580), [Bug 1471379](https://bugzilla.mozilla.org/show_bug.cgi?id=1471379)
- 示唆: まとめ方の規則は人手で育つ運用物で、変えると過去の統計が比べられなくなる（Sentry の「版を分けて新規だけに適用」と同じ問題）。

### ClusterFuzz / OSS-Fuzz（Google）

- 機能: "Accurate deduplication of crashes"、"Testcase minimization"、"Regression finding through bisection"、"Fully automatic bug filing, triage and closing"。Google 内で 25,000 件超、OSS-Fuzz で 550 超のプロジェクトから約 36,000 件（2022-05 時点）。 — [ClusterFuzz](https://google.github.io/clusterfuzz/)
- 修正の確認: 最新ビルドに対して毎日テストケースを再実行し、修正を検出すると Fixed を Yes にし、修正を含むコミット範囲（Fixed Revision Range）を示し、バグにコメントして状態を変える。頻出クラッシュは約 2 週間出なければ Verified で閉じる。報告のない再現不能なものは 1 週間見なければ閉じる。バグにはテストケースとビルド、元のクラッシュのコマンドラインと環境変数が付く。 — [Fixing a bug](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/fixing-a-bug/)
- 示唆: 「理解しやすいバグ」とは、最小の入力・回帰範囲（いつ壊れたか）・再現コマンド・修正範囲が機械的に付いたバグ。人の判断（妥当か、閉じてよいか）を再実行という検証で置き換えている。

### GitHub issue forms

- 2021-06-23 公開のベータ。"Issues submitted to open source projects often lack important information." Markdown テンプレートは自由に編集できるので "can miss details or get confused"。YAML で必須項目のある構造化フォームを作る。 — [GitHub changelog](https://github.blog/changelog/2021-06-23-issues-forms-beta-for-public-repositories/)

### SWE-bench Verified（OpenAI と SWE-bench 著者）

- 動機: SWE-bench には解けない／ほぼ解けない課題があり、モデルの能力を過小評価しうる。 — [Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)
- 注釈: Python 経験のある 93 人が 1,699 件を各 3 人で注釈し、最も厳しいラベルを採用。基準は (1) issue の記述が不十分か (2) FAIL_TO_PASS テストが正しい解を落とすか (3) 難しさ（除外には使わない）。各 0〜3 で、2・3 は除外。38.3% が記述不足、61.1% がテストの不当さで指摘され、計 68.3% を除外し 500 件。除外は過剰気味だと認めている。GPT-4o は 16% → 33.2%。 — 同上
- 示唆: issue の「評価」で最初に問うべきは、それが一意に解ける程度に指定されているか（期待動作が確定しているか）。人の注釈者でも 3 人の最悪値を取る保守的な集約をしている。

### LIBRO（Kang, Yoon, Yoo; ICSE 2023）

- 問題: 既存のテスト生成は "generating tests to reproduce a given bug report" のような意味的な目的に届かず、再現手法はクラッシュに偏る。 — [arXiv 2209.11515](https://arxiv.org/abs/2209.11515)
- 結果: Defects4J の 750 件中 251 件（33.5%）で再現テスト、149 件で 1 位に正しいテスト。学習データ以後の報告 31 件で 32%。 — 同上
- 「いつ信じるか」の設計（PDF 本文から）:
  - 再現テスト（BRT）の必要条件は「バグのある版で失敗する（FIB）」だが、FIB が BRT とは限らない。クラッシュ再現はスタックトレース比較で確認できるが、一般のバグはそうはいかない。全候補を開発者に見せるのは "generally undesirable"。
  - 同じ失敗出力（例外の型とメッセージ）でテストをまとめ、最大のまとまりの大きさを LLM の「合意」とみなす。閾値を高くすれば有意な合意があるときだけ見せる。
  - 順位付けは、(1) 失敗メッセージやテストが報告に書かれた振る舞いを含むか (2) 合意の大きさ (3) テストの短さ（短い方が理解しやすい）。同じまとまりは似た誤りをするので、まとまりをまたいで多様に見せる。
  - 33% のバグを安全に捨てつつ、成功した再現の 87% を残せた。精度 0.84・再現率 0.42 の設定もある。 — [LIBRO PDF](https://arxiv.org/pdf/2209.11515)

### SWT-bench（Mündler, Müller, He, Vechev, ETH）

- issue からテストを作る能力を測る。修正用に作られたコードエージェントが、テスト生成専用の手法を上回った。生成テストで修正案をふるいにかけると SWE-Agent の精度が約 2 倍。"generated tests are an effective filter for proposed code fixes, doubling the precision of SWE-Agent" — [arXiv 2406.12952](https://arxiv.org/abs/2406.12952)（要旨のみ）

### Otter（Ahmed ほか; ICML 2025）

- 修正がまだない状態で issue からテストを作る（TDD、エージェントの修正の検証）。LLM の出力を規則ベースの解析で検査・修理し、自己省察型の行動計画を使う。TDD-Bench-Verified を導入。数値は要旨にない。 — [arXiv 2502.05368](https://arxiv.org/abs/2502.05368)（要旨のみ）

### Issue2Test（Nashid, Bouzenia, Pradel, Mesbah; ICSE 2026）（検索要約のみ）

- 文脈収集 → 候補テスト生成 → コンパイルと実行の結果で修正。通るテストではなく「issue に書かれた理由で失敗するテスト」を狙う。SWT-bench-lite で 32.9%。 — [arXiv 2503.16320](https://arxiv.org/html/2503.16320v4)

### Agentless（Xia ほか）（要旨のみ）

- 位置特定・修正・検証の単純な 3 段。"Do we really have to employ complex autonomous software agents?" SWE-bench Lite で 32.00%（96 件）、1 件 0.70 ドル。手で分類すると、Lite には正解の修正がそのまま issue に書かれたものや、記述が不十分／誤解を招くものがあり、除いた Lite-S を作った。 — [arXiv 2407.01489](https://arxiv.org/abs/2407.01489)

### AutoCodeRover / SpecRover（Zhang, Ruan, Roychoudhury, NUS）

- AutoCodeRover はコード検索を「プログラム構造から仕様を推定する手段」として使い、テストがあれば spectrum-based fault localization も使う（検索要約のみ）。 — [arXiv 2404.05427](https://arxiv.org/abs/2404.05427)
- SpecRover: reproducer エージェントが issue から再現テストを書く（"the reproducer test can be _incorrect_, due to the non-determinism of the LLM"）。reviewer エージェントが元と修正後で再現テストを実行し、修正とテストの両方に二値の判定と "explanations for both decisions" を出す。両方が正しいと判断したときだけ受理し、そのときだけ開発者が見る。再現テストを生成できた 119 件で、正解率 64.7%、精度 50.0%、再現率 61.9%。 — [arXiv 2408.02232v2](https://arxiv.org/html/2408.02232v2)
- 示唆: LLM が出す「確信」は、再現テストという実行可能な証拠に結びつけても精度 5 割程度。説明は付けるが、受理の判断材料としてはまだ弱い。

### curl と LLM 生成の報告（Daniel Stenberg）— 反面教材

- 2024-01-02。バグ報奨金で 415 件の脆弱性報告、確認された問題は 64 件、約 66% はセキュリティ問題でも通常のバグでもなかった。"A crap report does not help the project at all." 見た目の整った偽報告ほど却下に時間がかかる。例: WebSocket のバッファオーバーフローとする整形済みの報告と修正案が、質問を重ねた末に "There was no buffer overflow"。報告者は AI の出力を検証せずに出していた。 — [The I in LLM stands for intelligence](https://daniel.haxx.se/blog/2024/01/02/the-i-in-llm-stands-for-intelligence/)
- 示唆: 「理解・評価の仕組み」が LLM で報告を書けば、検証のコストを報告者から保守者へ移すだけになりうる。主張は実行可能な証拠（再現）と結びつけないと、上流への報告として害になる。

## 3. 終了・放棄・方向転換とその理由

- Replay.io バグ報告向け（2021）→ flaky test 向け（2022）→ Test Suites 終了（2024-08-31）、人員削減、CEO 交代（2024-09）。理由: 解決策から始めて問題を探していた。バグは動画とネットワークで大半が再現できた。利用者は原因を調べるよりテストを通るように直した。機密データと専用ブラウザへの懸念。日常は Chrome devtools で足りた。 — [A new direction](https://www.replay.io/blog/a-new-direction), [Changelog 67](https://www.replay.io/blog/changelog-67-demos)
- Pernosco の事業性への懐疑（「デバッガは売れない」）と、rr で足りる利用者の存在（検索要約のみ）。 — [Your Debugger Sucks](https://robert.ocallahan.org/2019/11/your-debugger-sucks.html), [DEBT workshop](https://robert.ocallahan.org/2024/10/debt-workshop.html)
- SWE-bench の 68.3% 除外、Agentless の Lite-S: 「解けない／記述不足の issue」をベンチマークから捨てた。現実の issue ではこれらを捨てられないので、理解支援はまさにここを扱う必要がある。 — [OpenAI](https://openai.com/index/introducing-swe-bench-verified/), [Agentless](https://arxiv.org/abs/2407.01489)
- Sentry の従来のグルーピング（stack trace の文字列ベース）は、重複 issue と重複アラートの不満から AI で補われた（置き換えではなく、新 hash だけに追加の段を足した）。 — [Sentry blog](https://blog.sentry.io/how-sentry-decreased-issue-noise-with-ai)
- BugBug は精度確保のため、件数の少ないコンポーネントを対象外にし、確信度が低いものは自動処理しない（自動化の範囲を意図的に狭めた）。 — [Mozilla Hacks](https://hacks.mozilla.org/2019/04/teaching-machines-to-triage-firefox-bugs/)

## 4. 横断するパターン

1. **自動再現**: 記録（rr・Pernosco・Undo・TTD・Replay）と、テスト生成（LIBRO・SWT-bench・Otter・Issue2Test・SpecRover）の 2 系統。前者は確実だが重く（TTD で 10〜20 倍遅い、GB 単位）、機密データを含む。後者は軽いが 3 割前後しか再現できず、成功の判定が難しい。
2. **再現と診断の分離**: Pernosco の「QA が記録し URL を渡す」、Undo の「失敗時点に置かれたデバッガ」、ClusterFuzz の「テストケース＋ビルド＋コマンド」。再現を成果物（URL・テスト・記録）にして人の間で渡せるようにする。
3. **最小化と回帰範囲**: ClusterFuzz は最小化・二分探索で「いつ・何が」を付け、修正範囲も自動で付ける。LIBRO は短いテストを優先する（短い方が理解しやすい）。
4. **まとめ（重複排除）**: fingerprint/シグネチャ（Sentry, Socorro, ClusterFuzz）＋人手で育つ例外規則（SkipList、組み込み fingerprint）＋埋め込みによる保守的な追加（Sentry）。変更は過去の統計を壊すので版を分ける／毎週レビューする。誤ったまとめを避ける方向に非対称。
5. **報告の補強**: issue forms（必須項目）、needinfo で再現手順を求める、BugBug の「起票時点に巻き戻して学習」、Honeycomb の高カーディナリティ属性と「正常群との差」（BubbleUp）。
6. **確信度と検証**: BugBug の確信度閾値（〜60%）で自動処理を絞る。LIBRO の「合意」（同じ失敗出力のまとまりの大きさ）と、報告の記述との一致。SpecRover の reviewer（精度 50%）。SWT-bench の「生成テストで修正をふるう」と精度 2 倍。SWE-bench Verified の 3 人中最悪値。ClusterFuzz の毎日の再実行による修正確認。
7. **期待動作の確定が最初の関門**: SWE-bench で 38.3% が記述不足、Castelluccio らが引く 65% が期待動作を欠く（検索要約のみ）。Issue2Test は「issue の理由で失敗する」ことを要件にする。

## 5. 設計原則の候補とアンチパターン

以下は上の資料からの推論（Claude の推論）で、検証済みの結論ではない。

### 原則の候補

- **P1 主張には実行可能な証拠を付ける**: 「再現した」「重複だ」「原因はここ」は、再現テスト・記録・最小入力・同じ fingerprint のイベントなど、他人が再実行できる形で示す（ClusterFuzz, Pernosco, SpecRover, curl の反面教材）。
- **P2 何も言わない選択肢を持つ**: 確信度や合意が閾値未満なら結果を出さない／自動処理しない（BugBug の 60%、LIBRO の Thr、Sentry の保守的閾値）。見せる候補の数も絞る（LIBRO: 全候補を見せるのは望ましくない）。
- **P3 誤ってまとめる方を重く見る**: 重複判定は新規の追加だけ、既存を分割しない、unmerge を尊重する（Sentry）。重複の誤判定は報告を消してしまう。
- **P4 期待動作を先に確定させ、記述不足は「評価結果」として返す**: SWE-bench Verified の 0〜3 の記述不足ラベルのように、「この issue は一意に解ける程度に指定されているか」を独立の判定にする。足りなければ needinfo のように具体的に何が欠けているかを求める。
- **P5 回帰範囲・最小化で「いつ・何が」を付ける**: 二分探索と最小化は、説明の生成よりも検証しやすい理解の材料（ClusterFuzz）。
- **P6 安い証拠から使う**: 動画・ネットワークログ・ログで足りるものが多い（Replay の発見）。重い記録や深い解析は、安い証拠で足りないときに段階的に使う。
- **P7 再現と診断を分け、成果物として渡せるようにする**: 再現した人と診断する人が違ってよい（Pernosco）。URL に時点と文脈を含める。
- **P8 修正の確認を自動で続ける**: 再現テストを毎日回し、直ったら範囲を付けて閉じる（ClusterFuzz）。報告の評価は起票時だけでなく継続する。
- **P9 学習・評価の情報漏れを防ぐ**: 起票時点の情報だけで判断する設計にする（BugBug の巻き戻し）。後から付いた情報で判断を評価しない。
- **P10 規則の変更は版を分ける**: まとめ方を変えると過去の統計が比べられなくなる（Sentry の版、Socorro の SkipList）。

### アンチパターン

- **A1 解決策から始める**: 強力な再生技術から用途を探した（Replay の自己評価）。
- **A2 検証していない LLM の説明をそのまま上流に出す**: 整った偽報告ほど保守者のコストが大きい（curl）。
- **A3 全候補を並べて人に選ばせる**: 判断の負担を移すだけ（LIBRO の指摘）。
- **A4 文字列の類似だけで重複を決める**: フレームの並び替えや行番号で分かれ、逆に無関係なものが似る（Sentry）。逆に、上位フレームだけで過剰にまとまる（Socorro の SIGABRT）。
- **A5 記録の機密性を無視する**: 記録は全メモリ・全通信を含む（Replay の利用者の懸念、Undo・TTD の注意書き）。
- **A6 利用者の最安の手段を見落とす**: 原因を調べず通るまで直す、Chrome devtools で足りる、rr で足りる（Replay, Pernosco）。理解の道具は「調べる価値がある」と判断できる場面でしか使われない。

## 6. 未確認・空白

- Kyle Huey 自身の発言、Pernosco の利用者数や事業の数字は見つけていない。O'Callahan の 2018/2019/2024 の投稿は検索要約のみ。
- David Cramer 本人の grouping に関する文章（初期設計の意図）は未取得。Sentry AI grouping 第 2 版の数値は検索要約のみ。
- Bugsnag, Rollbar のグルーピング設計は未調査。
- Google 社内のバグ振り分け ML の公開資料は未調査（ClusterFuzz 以外）。
- ClusterFuzz の最小化・二分探索の具体的な手順と、それが開発者の対応時間をどれだけ縮めたかの数値は未取得。
- BugBug のその後（重複検出・再現手順欠如検出・LLM 導入の有無と精度）は未確認。Castelluccio らの 65%/49% はプロキシ経由の検索要約で、原典で未確認。
- Honeycomb の創業者本人の一次資料（charity.wtf の記事）は未取得。BubbleUp と Christine Yen の関係は未確認。
- Agentless の再現テストの段の詳細、Otter と Issue2Test の詳細な数値は要旨または検索要約のみ。
- AutoCodeRover に reproducer があるかは確認できなかった（SpecRover にはある）。
- LLM を使った issue 振り分けボットに対する保守者の反応は、curl の事例以外は調べていない（GitHub の AI triage 機能など）。
- Microsoft TTD の設計論文（著者・設計意図）と Undo の情報は検索要約のみ。
