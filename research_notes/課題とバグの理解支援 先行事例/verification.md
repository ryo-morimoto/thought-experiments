# 本文での照合の記録（2026-11-21）

対象は [高認知負荷の理解支援 先行事例](../../reports/高認知負荷の理解支援%20先行事例.md)（以下「PR 報告」）と [課題とバグの理解支援 先行事例](../../reports/課題とバグの理解支援%20先行事例.md)（以下「課題報告」）である。両報告で「（要旨のみ）」「（検索要約のみ）」と書いた主張と、「未確認事項」の表に挙げた数値のうち確かめられるものを、一次資料の本文で照合した。

各項目は、報告での書き方、出典、本文の記述（引用は 2 文以内）、判定（確認・訂正・本文取得できず）、報告への反映の順に書く。判定と反映は Claude の作業で、ユーザーの判断ではない。

## 集計

- 確認: 20 件
- 訂正: 11 件（数値は一致して書き方・帰属・解釈を直したものを含む。うち結論の文に関わるもの 2 件は下の「結論に関わる訂正」）
- 本文取得できず: 2 件（Pollock 2002、Rahman・Codabux・Roy 2026。どちらも要旨だけ確認）

## 結論に関わる訂正

- **SWE-bench Verified の 38.3%**（課題報告「測られた事実」の節）。報告は「課題の 4 割近くは一意に解けるほど指定されていなかった」と書いていた。本文によれば、3 人の注釈者の最も重い判定を採る保守的な集計で、OpenAI 自身が「This approach leads to a higher false-positive rate in removing samples」と書いている（[OpenAI](https://openai.com/index/introducing-swe-bench-verified/)）。そこで「4 割近くに疑いが付いた」に弱めた。期待動作の確定が関門だという方向は変わらない。
- **Tricorder と FindBugs**（PR 報告「信頼はノイズと省略で失われる」と失敗の表）。報告は「誤検知のために開発者がツール全体を信頼しなくなった」と書いていた。本文では、FindBugs をレビューに出した試みは「ran into scaling problems (resulting in stale or delayed results) and produced many results developers were uninterested in addressing」で、信頼については「this trust is quickly lost if they do not understand the tool's output」と書いている（[Tricorder](https://www.cs.umd.edu/class/spring2019/cmsc414/papers/tricorder-building-a-program-analysis-ecosystem.pdf)）。理由を「結果の遅れと、対処されない結果の多さ」に直した。「ノイズによる信頼の喪失」という失敗の型の分類は、対処されない結果をノイズとみなせば保てるので、そのままにした（推論）。

## PR 報告（高認知負荷の理解支援 先行事例）

- **Tufano ほか**（生成レビューを出発点にすると指摘箇所に集中し、時間も自信も改善しない）。出典 [arXiv 2411.11401v3](https://arxiv.org/html/2411.11401v3)。本文は 29 人の専門開発者の統制実験で、「Reviewers tend to focus on the code locations indicated by the LLM rather than searching for additional issues in other parts of the code.」「the automated support did not result in saved time and did not increase the reviewers' confidence.」と書く。判定: 確認。反映: 印を「本文で確認」にし、29 人を足した。冒頭の結論の「指摘箇所しか見なくなる」は「指摘箇所に集中して他を探さなくなる」に合わせた。
- **Cihan ほか**（73.8% が受け入れられた。クローズ時間 5 時間 52 分→8 時間 20 分）。出典 [arXiv 2412.18531](https://arxiv.org/abs/2412.18531)。本文は「73.8% of automated code review comments were labeled as resolved」「increased from five hours 52 minutes to eight hours 20 minutes, with varying trends observed across different projects」。判定: 訂正（「受け入れられた」→「resolved とラベル付けされた」。プロジェクト差を追記）。
- **Shen & Tamkin**（52 人、50% 対 67%、完了時間に有意差なし）。出典 [Anthropic](https://www.anthropic.com/research/AI-assistance-coding-skills)。本文は「the AI group averaged 50% on the quiz, compared to 67% in the hand-coding group」「participants in the AI group finished about two minutes faster, although the difference was not statistically significant」。判定: 確認。
- **Osmani の「委任群 40% 未満、概念質問群 65% 超」**（出典不明としていた）。同じ Anthropic のページが「The average quiz scores in this group were less than 40%」（低得点の利用型）と、高得点の型を「65% or higher」と定義している。判定: 確認（出所を特定）。反映: 「出典が弱い」から外した。
- **Crupi ほか**。出典 [arXiv 2602.11925](https://arxiv.org/abs/2602.11925)。本文の要旨は ChatGPT が「can only spot 10% of the quality issues reported by humans」で、DL レビューは人の点検の上の追加チェックとして使えると書く。判定: 確認。
- **RovoDev**（38.70% 対 44.45%、事実の正しさで落とす段）。出典 [arXiv 2601.01129](https://arxiv.org/abs/2601.01129)。本文は「38.70%, which is 12.9% relatively less than a code resolution rate of human-written comments (44.45%)」で、「quality check on factual correctness to remove noisy comments」を置く。判定: 確認。
- **Google の ML によるコメント解決（5% と 7.5%）**。出典 [論文 PDF](https://storage.googleapis.com/gweb-research2023-media/pubtools/7525.pdf)。本文は「code-change authors at Google address 7.5% of all reviewer comments by applying an ML-suggested edit」で、週ごとの値は 5.4〜7.5% と書く。判定: 確認（食い違いを解消。5% は別箇所の「almost 5%」という言い回し）。
- **Rahman・Codabux・Roy ICSE 2026**（1,355 人、10.2%、66% が依存関係でまとめた順序を望んだ）。出典 [ICSE 2026 ページ](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/310/Breaking-the-Alphabet-Rethinking-File-Ordering-in-Code-Review)。要旨は「only 10.2% of reviewers consider alphabetical ordering optimal」「dependency-aware grouping and customizable file ordering (requested by 66% of reviewers)」。判定: 訂正、ただし本文取得できず（arXiv に見当たらない）。反映: 66% を「依存関係を考慮したまとめ方や並べ替えの設定」に直し、要旨のみの印を残した。
- **Pollock ほか 2002**（2 段階の isolated-interacting elements 法）。UOW の頁は 403、UNSW の全文も 403。Semantic Scholar が返した論文の要旨は「a two-phase, isolated-interacting elements learning approach was developed」「for certain groups of learners, information is better learnt through the isolated-interacting elements instructional method」（[DOI](https://doi.org/10.1016/S0959-4752(01)00016-0)）。判定: 本文取得できず（要旨とは一致）。反映: 印を残した。
- **Spadini ICSE 2020**（プライマーでなくリマインダー）。出典 [本文](https://sback.it/publications/icse2020.pdf)。「existing review comments about bugs in code changes are not negative primers, rather positive reminders for bugs that would otherwise be overlooked during code review.」判定: 確認。
- **LaToza ほか 2006**（暗黙知は対面の会話とコードで共有される）。出典 [本文](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/p492-latoza.pdf)。「knowledge is shared between developers through face-to-face communication and the code itself.」判定: 確認。
- **Tricorder の「実効誤検知 10% 未満」**。本文は「We still enforce a very low effective false positive rate here (< 10%).」で、「役に立たない」率が 10% 以上の解析は保護観察に置く。判定: 確認。FindBugs の理由は上の「結論に関わる訂正」を参照（訂正）。
- **Gonçalves 2022**（認知負荷が高い群の方が成績がよかった）。出典 [本文](https://rd.springer.com/content/pdf/10.1007%2Fs10664-022-10123-8.pdf)。「we did not identify a strong relationship between the guidance provided and code review performance」「higher cognitive load led to better performance possibly due to the generally low effectiveness and efficiency of the study participants.」判定: 訂正（群の比較ではなく認知負荷と成績の関係。参加者の多くが経験の浅いレビュアーだったことを追記）。
- **Pull Panda**（GitHub が同じ機能を内製した）。出典 [GitHub changelog](https://github.blog/changelog/2022-03-23-pull-panda-is-shutting-down/)。本文は Pull Reminders と Pull Assigners を「code review assignment and scheduled reminders」に置き換えた後、残りの機能の利用が大きく減ったとし、分析機能には「not immediate replacements」と書く。判定: 訂正。
- **CodeSee**（2024 年に GitKraken が買収）。出典 [GitKraken](https://gitkraken.com/press/gitkraken-acquires-codesee-launches-devex-platform)。2024-05-14 付の買収発表を確認。ドメインの消滅は確かめていない。判定: 確認（部分）。
- **Fakhoury ほか**（自己報告、fNIRS、注視時間が相関しない）。出典 [NSF PAR](https://par.nsf.gov/servlets/purl/10135165)。「self-reported task difficulty, cognitive load, and fixation duration do not correlate and appear to be measuring different aspects of task difficulty.」判定: 確認。
- **国内調査（@IT）**（49.5% が「作成者本人が説明できなかった」経験を挙げた。文字化け）。ページは Shift_JIS で、読み直すと文字化けは解消した。本文は、キッカケクリエイションが IT エンジニア 322 人に行った調査で、AI 生成コードのレビューで問題だと感じた点（3 つまで回答）の最多が「提出者本人がコードの内容を説明できなかった」（49.5％）、負担増の実感は 30.0％＋56.3％（[@IT](https://atmarkit.itmedia.co.jp/ait/spv/2606/16/news041.html)）。判定: 訂正（「経験」ではなく「問題だと感じた点」。数値は一致）。

## 課題報告（課題とバグの理解支援 先行事例）

- **Guo ICSE 2010**（評判・同じチーム・近い場所。適合率 68%・再現率 64%）。出典 [本文](https://pg.ucsd.edu/publications/Microsoft-Windows-which-bugs-get-fixed_ICSE-2010.pdf)。「bugs reported by people with better reputations were more likely to get fixed, as were bugs handled by people on the same team and working in geographical proximity」「precision of 68% and recall of 64%」。判定: 確認。反映: リンクを PDF に替えた。
- **再オープンの主因（ICSE SEIP 2012）**。出典 [本文](https://pg.ucsd.edu/publications/Microsoft-Windows-which-bugs-get-reopened_ICSE-SEIP-2012.pdf)。358 人の調査から理由を分類し、根本原因に関わるもの（再現が難しい、根本原因の誤解、情報不足）と優先度に関わるものに分けている。判定: 確認（割合は報告に書いていないので照合対象外）。
- **Aranda & Venolia**（リポジトリの記録は「incomplete and often erroneous」）。出典 [本文](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/secret.pdf)。要旨では、この語の主語は「such automation provides incomplete and often erroneous accounts of coordination」で、本文 4 節は、バグの記録が「erroneous or misleading in seven of our ten cases, and incomplete and insufficient in every case」と書く。判定: 訂正（主語を「自動で再構成した経緯」にし、7/10 と全件を追記）。
- **Khatoonabadi ほか**（stale bot 導入後に滞留は減ったが活動する貢献者が減った）。出典 [arXiv 2305.18150](https://arxiv.org/abs/2305.18150)。「the projects experienced a considerable decrease in their number of active contributors after the adoption.」判定: 確認。ただし表の「撤去や置き換えが相次いだ」はこの論文の記述ではないと注記した。
- **Wessel ほか CSCW 2021**（ボットのノイズ）。出典 [arXiv 2103.13950](https://arxiv.org/abs/2103.13950)。21 人の面接で「our findings indicate noise as a recurrent and central problem.」判定: 確認。
- **Ambig-SWE の最大 74%**。出典 [arXiv 2502.13069](https://arxiv.org/abs/2502.13069)。「significant improvements in performance, up to 74% over the non-interactive settings」。判定: 確認。
- **SWT-Bench の精度 2 倍**。出典 [arXiv 2406.12952](https://arxiv.org/abs/2406.12952)。「generated tests are an effective filter for proposed code fixes, doubling the precision of SWE-AGENT.」判定: 確認。
- **SWE-bench Verified**（1,699 件、38.3%、61.1%、68.3%）。出典 [OpenAI](https://openai.com/index/introducing-swe-bench-verified/)。「38.3% of samples were flagged for underspecified problem statements, and 61.1% were flagged for unit tests that may unfairly mark valid solutions as incorrect.」数値は確認。解釈は上の「結論に関わる訂正」を参照（訂正）。
- **curl のバグバウンティ**（87 件・10 万 USD 超、確認率 15% 超→5% 未満、2026-01-31 終了、報告料を取らない）。出典 [the end of the curl bug bounty](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/)。「87 confirmed vulnerabilities and over 100,000 USD paid as rewards」「Starting 2025, the confirmed-rate plummeted to below 5%.」判定: 確認。報告料の理由は、国際的な課金の手間とチャージバックの対応、正当な報告者まで減らしうること、の複数で、「当面」は採らないとしていたので、表の文を訂正した。報道の 78 件・約 86,000 USD の数え方は確かめていない。
- **「約 65% が期待動作を欠き、49% が再現手順を含まない」**（プロキシ経由で原典未確認）。出典 [ICSME 2020 本文](https://marco-c.github.io/publications/non_reproducibility-icsme2020.pdf)。筆頭著者は Rahman で、「According to Chaparro et al. [15], about 65% of the bug reports miss the correct behaviour (EB) and 49% of the reports do not contain any steps to reproduce the bugs.」[15] は DeMIBuD（FSE 2017）で、報告本文の EB 35.2%・S2R 51.4% の裏返しにあたる。判定: 確認（出典の帰属を訂正）。
- **Pernosco の事業性**（「デバッガは売れない」。rr だけで満足する人もいた）。出典 [Your Debugger Sucks](https://robert.ocallahan.org/2019/11/your-debugger-sucks.html)。「I have lost count of the number of people who have told me "you'll never make money selling a debugger"」。「rr だけで満足する人」にあたる記述は投稿とコメントに見当たらなかった。判定: 訂正（後半を削除）。失敗の型「利用者の最安の手段を見落とした」への分類は、無料の道具が最安の手段だと読めるので保った（推論）。
- **Breakpad/SkipList**。出典 [MozillaWiki](https://wiki.mozilla.org/Breakpad/SkipList)。「The Socorro team reviews these SkipList changes every Monday」「Every SkipList change affects our crash metrics.」判定: 確認。ただし古い wiki ページで、現在の運用かは未確認と注記した。
- **TTD**（記録の機密性）。出典 [Microsoft Learn](https://learn.microsoft.com/windows-hardware/drivers/debugger/time-travel-debugging-overview)。「The recording may contain personally identifiable or security related information」。判定: 確認。「半分の時間」はこのページに見当たらず、未確認のまま残した。
- **Beller ほか ICSE 2018 の「デバッグセッションの 88% が 10 分未満」**（調査ノートの記述。報告本文には出てこない）。出典 [本文](https://www.spinellis.gr/pubs/conf/2018-ICSE-debugging-analysis/html/BSSZ18.pdf)。「Most debugging sessions consume less than 10 minutes.」と、10 分を超えるのは約 12% とある。判定: 確認（報告の変更なし）。

## まだ確かめていないもの

PR 報告: Nam ほか、Pascarella 2018 の 7 カテゴリ、Sillito の 44 質問、Atlassian の 30.8%、Greptile の数値、Sourcegraph Cody の終了日、Pollock 2002 と Rahman・Codabux・Roy 2026 の本文。

課題報告: Sülün ら TOSEM 2024、Rahman・Khomh・Castelluccio EMSE 2022 の 11 要因、Google での LIBRO の追試、Sentry AI grouping 第 2 版、TTD の「半分の時間」、Issue2Test・Otter・Agentless の数値、報道側の curl の数値、Eghbal。
