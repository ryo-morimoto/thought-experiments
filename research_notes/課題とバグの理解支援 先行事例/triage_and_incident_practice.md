# 課題・障害のトリアージと評価を実践・研究する人々とその資産

調査日: 2026-11-21。一次資料は WebFetch で本文を読んだもの。読めなかったものは「要旨のみ」（論文の abstract や公式ページの要約だけ）、「検索要約のみ」（検索エンジンの要約だけで本文未確認）と記す。引用は短く、直後に URL を書く。

## 1. 人とグループ（誰が実践・研究しているか）

### Takeaway
トリアージの実践知は、大規模プロジェクトの「役割を名指しされた人」（Mozilla の Triage Owner、カーネルの regression tracker、Kubernetes の SIG）と、その負担を引き受けて疲弊した個人（Thorsten Leemhuis、Daniel Stenberg）に集まっている。研究側はバグ報告の品質・再現不能・テンプレート・ボットの害を実証し、インシデント分析側は「根本原因」「後知恵」への批判を理論化している。

### Cited Findings

<!-- data-source: original（調査ノートの整理） -->
| 人・グループ | 立場 | 主な資産 | 確認状態 |
| --- | --- | --- | --- |
| Marco Castelluccio, Sylvestre Ledru（Mozilla） | 実践者・研究者 | BugBug（ML によるコンポーネント振り分け）、再現不能バグの研究 | 本文確認 |
| Emma Humphries（Mozilla Developer Workflow） | プロセス設計者 | 2020 年の Severity 必須化の告知 | 本文確認 |
| Mozilla Triage Owner（コンポーネントごと） | 役割 | Triage for Bugzilla | 本文確認 |
| Chromium Security | 役割 | Security Severity Guidelines | 本文確認 |
| Thorsten Leemhuis | Linux カーネル regression tracker | regzbot、reporting-regressions 文書、LPC/Maintainers Summit での発表 | 本文確認（LWN 経由） |
| Rust release/triage（rustbot / triagebot） | 役割 | Forge の Issue triaging | 本文確認 |
| CPython triage team | 役割 | devguide の Triaging an issue | 本文確認 |
| Kubernetes SIG / k8s-triage-robot | 役割 | Issue triage guide | 本文確認 |
| Daniel Stenberg（curl） | メンテナ | AI slop 報告、CVSS 拒否、バグバウンティ終了の記録 | 本文確認 |
| Mairieli Wessel, Igor Steinmacher, Marco Gerosa ほか | 研究者 | stale bot の設定研究、ボットの「ノイズ」研究 | 要旨のみ |
| Khatoonabadi, Costa, Mujahid, Shihab | 研究者 | stale bot 導入の効果（貢献者減少） | 要旨のみ（arXiv abstract） |
| Zimmermann, Bettenburg, Premraj ほか | 研究者 | What Makes a Good Bug Report? | 検索要約のみ |
| Erfani Joorabchi, Mesbah ほか / Rahman, Khomh, Castelluccio | 研究者 | 再現不能バグ報告の研究 | 検索要約のみ |
| Sülün, Saçakcı, Tüzün | 研究者 | Issue テンプレートの実証分析（TOSEM 2024） | 検索要約のみ |
| Nadia Eghbal（Asparouhova） | 著者 | Working in Public（2020） | 検索要約のみ（書評経由） |
| Richard Cook | 安全研究者 | How Complex Systems Fail | 本文確認 |
| John Allspaw | 実践者・研究者 | The Infinite Hows、Etsy の Debriefing Facilitation Guide | Infinite Hows は本文確認、Etsy ガイドは取得失敗（403） |
| Lorin Hochstein | 実践者 | Surfing Complexity ブログ（no root cause） | 検索要約のみ |
| Drew DeVault | メンテナ | GitHub stale bot considered harmful（2021） | タイトルのみ（本文取得失敗） |

### Inferences
- 「トリアージの役割を名指しする」ことと「その役割の負担と権限の不足」が、大規模プロジェクト全体に共通する論点になっている。

### Gaps
- Nora Jones / Jeli、Laura Maguire、Learning From Incidents コミュニティ、Google VRP、HackerOne のトリアージ文書は、今回の呼び出し回数の範囲では読めていない（第6節）。

## 2. ソースごとの資産（知識・洞察・意図）

### Takeaway
どのプロジェクトも、判断に決定的な情報を「再現手順・再現物」「回帰の範囲（最後に動いた版と最初に壊れた版、bisect）」「正しい担当（コンポーネント・SIG）」に置いている。不確かさは、ラベルで状態として明示する（`needs-info`、`S-needs-repro`、`regression-untriaged`、`priority/awaiting-more-evidence`）。

### Cited Findings

**Mozilla: Triage for Bugzilla（本文確認）**
- コンポーネントごとに Triage Owner を置き、triage の責任者にする。ローテーションのコンポーネントでは Bugzilla 上の triage owner が自動で切り替わる — [Triage for Bugzilla](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)
- 「triaged」の定義は、defect が UNTRIAGED 以外のコンポーネントと、`--` でも `N/A` でもない severity を持つこと。task と enhancement は `N/A` でよい — [同](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)
- 新規バグは毎日セキュリティ観点で見て、1週間以内に triage を終えるか調査中にする。S1 と sec-critical は2営業日以内に担当を付ける — [同](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)
- severity を変えるときは理由をコメントに書くことが必須（判断理由の記録）— [同](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)
- needinfo は2週間以上放置しない。返答のない UNCONFIRMED は RESOLVED INCOMPLETE にできる。返答のない needinfo が10日を超えたバグは triage クエリに戻ってくる — [同](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)
- 停滞したバグには `stalled` キーワードを付けて triage リストから外す（閉じずに状態を表す）— [同](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)
- Severity のガイドは定義を BMO の User Guide に委ね、例だけを示す。S2 の例は「could reasonably be expected to cause a Firefox user to switch browsers」 — [Defect Severity](https://firefox-source-docs.mozilla.org/bug-mgmt/guides/severity.html)
- 優先度のガイドラインは「under review」と書かれている — [Triage for Bugzilla](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)

**Mozilla: BugBug（本文確認）**
- Castelluccio と Ledru が 2019 年に発表。人手のコンポーネント振り分けは「fails to scale」。新規バグに product/component を付ける — [Teaching machines to triage Firefox bugs](https://hacks.mozilla.org/2019/04/teaching-machines-to-triage-firefox-bugs/)
- 訓練データは、バグを「起票時点の状態」に巻き戻して作る（後から付いた情報が漏れないように）— [同](https://hacks.mozilla.org/2019/04/teaching-machines-to-triage-firefox-bugs/)
- 確信度 60% 以上のときだけ自動で振り分け、精度（precision）は 80% 超。再現率は書かれていない。対象は、最大コンポーネントのバグ数の 1% 以上のバグがあるコンポーネントに限る。開発者が手を付けるまでの中央値は 2日（人手の平均は約1週間）— [同](https://hacks.mozilla.org/2019/04/teaching-machines-to-triage-firefox-bugs/)
- 現在も Firefox::General のバグは「confidence is high enough」のときに BugBug のモデルで振り分けられる — [Triage for Bugzilla](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)

**Chromium: Security Severity Guidelines（本文確認）**
- Critical（S0）から Low（S3）、「Not a security bug」まで。緩和要因で下げる規則が明文化されている。「Mitigating factors will generally reduce an issue's severity by one level.」 — [Severity Guidelines](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md)
- 影響が一部のユーザー（特定 OS など）に限られることは緩和要因にしない。「we do not consider it a mitigating factor if a vulnerability applies only to a particular group of users.」 — [同](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md)
- 「most crashes do not indicate vulnerabilities.」。DoS や大半のクラッシュはセキュリティバグにしない — [同](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md)
- 前提条件の扱い: 攻撃者が自分のコンテンツを正当に読み込めるプロセス（web renderer）だけを「侵害済み」と仮定してよい — [同](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md)
- 不確かなとき最悪を仮定せよ、という規則は書かれていない（WebFetch の要約による確認）。

**Linux カーネル: regression の報告と追跡（本文確認）**
- 「no regressions」規則の理由。「Users should feel safe when updating kernel versions and not have to worry something might break.」 — [Reporting regressions](https://docs.kernel.org/admin-guide/reporting-regressions.html)
- 決定的な情報は、最後に動いた版と最初に壊れた版、そして bisect による原因コミット。開発者が該当ハードを持たないことが多いため、原因の特定は報告者に求められることが多い — [同](https://docs.kernel.org/admin-guide/reporting-regressions.html)
- 報告に `#regzbot introduced:` を書くと regzbot が追跡し、返信や `Link:` タグ付きパッチを監視する。tracker（Leemhuis）は無給・best-effort と明記 — [同](https://docs.kernel.org/admin-guide/reporting-regressions.html)
- 2022 年の Maintainers Summit で、regzbot は見落とされていた regression を捉えていたと報告された — [LWN 908324](https://lwn.net/Articles/908324)（検索要約のみ）

**Rust: Issue triaging（本文確認）**
- 誰でも triage できる。書き込み権限がなくても `@rustbot` で `triagebot.toml` が許すラベルを付けられる — [Issue triaging](https://forge.rust-lang.org/release/issue-triaging.html)
- `needs-triage` は「an _initial_ checkpoint」で、軽い最初の通過でよい。目的は追跡票を「more searchable for future reference」にすること — [同](https://forge.rust-lang.org/release/issue-triaging.html)
- 情報の欠けをラベルで表す: `S-needs-repro`、`E-needs-mcve` → `S-has-mcve`、`E-needs-bisection`（cargo-bisect-rustc）→ `S-has-bisection`、`S-needs-info`。迷ったら再現物を求める — [同](https://forge.rust-lang.org/release/issue-triaging.html)
- regression は `regression-untriaged`（性質が未確定）と、stable→stable / stable→beta,nightly で区別する — [同](https://forge.rust-lang.org/release/issue-triaging.html)

**CPython: Triaging an issue（本文確認）**
- チェックリスト: 本文とコメントを読む、重複を探す、タイトルを具体化、ラベル、次の行動を短くコメントし、長いスレッドは要約する、明らかに無効なものは not planned + `invalid`。AI ツール方針に反する投稿には AI policy ラベル — [Triaging an issue](https://devguide.python.org/triage/triaging/)
- 実行可能なバグ報告の条件: 再現できる説明、プラットフォーム情報、影響を受ける Python のバージョン — [同](https://devguide.python.org/triage/triaging/)

**Kubernetes: Issue triage（本文確認）**
- `needs-triage` が自動で付き、所有 SIG が `/triage accepted` を付ける。情報不足は `triage/needs-information` — [Issue triage guide](https://github.com/kubernetes/community/blob/master/contributors/guide/issue-triage.md)
- 優先度は `critical-urgent`、`important-soon`、`important-longterm`、`backlog`、`awaiting-more-evidence`。優先度ラベルがないことは「まだ見ていない」を意味する — [同](https://github.com/kubernetes/community/blob/master/contributors/guide/issue-triage.md)
- 再現できないバグは報告者と連絡を取り、双方が合意したら閉じる。20日返答がなければ閉じる。90日動きがなければ k8s-triage-robot が `lifecycle/stale` を付け、最終的に自動で閉じる（`/lifecycle frozen` で止められる）。ページに理由は書かれていない — [同](https://github.com/kubernetes/community/blob/master/contributors/guide/issue-triage.md)

**curl / Daniel Stenberg（本文確認）**
- 2024 年初め時点で、バグバウンティの 415 件のうち確認されたセキュリティ問題は 64 件 — [The I in LLM stands for intelligence](https://daniel.haxx.se/blog/2024/01/02/the-i-in-llm-stands-for-intelligence/)
- よく書けた偽報告ほど棄却に時間がかかる。「The better the crap, the longer time and the more energy we have to spend on the report until we close it.」 — [同](https://daniel.haxx.se/blog/2024/01/02/the-i-in-llm-stands-for-intelligence/)
- セキュリティ報告は他の作業より優先されるので、偽報告は本物のバグや機能の作業から人を引き離す — [同](https://daniel.haxx.se/blog/2024/01/02/the-i-in-llm-stands-for-intelligence/)
- AI の使用そのものは失格理由にしない（翻訳の手助けは正当）— [同](https://daniel.haxx.se/blog/2024/01/02/the-i-in-llm-stands-for-intelligence/)
- curl は CVSS を使わず、low/medium/high/critical の4段階を自分たちで付ける。CVSS は「has a limited set of input factors that tend to result in a fairly high number for a network product.」。curl が low とした問題に CVSS 9.1 が付けられた例がある — [CVSS is dead to us](https://daniel.haxx.se/blog/2025/01/23/cvss-is-dead-to-us/)
- 補足: heise は、CVE に CVSS を付けることは必須ではないと、Stenberg の当初の記述を訂正している — [heise](https://heise.de/-10265929)（検索要約のみ）

**研究: バグ報告の質・再現不能・テンプレート**
- 開発者は再現手順とスタックトレースを最も求め、不正確な再現手順と不完全な情報を最大の障害とした。しかもそれらは報告者にとって最も用意しにくい（情報の不一致）— [Bettenburg et al. TR 2007](https://www.st.cs.uni-saarland.de/publications/files/bettenburg-tr-2007.pdf)、[Zimmermann et al. TSE 2010](https://thomas-zimmermann.com/publications/files/zimmermann-tse-2010.pdf)（検索要約のみ。回答数が版で 156 と 466 に分かれる）
- 再現不能の報告は全体の約 17%、他より約3か月長く開いたまま（6リポジトリ、32K 件）— [Erfani Joorabchi et al. MSR 2014](https://people.ece.ubc.ca/amesbah/resources/papers/mona-msr14.pdf)（検索要約のみ）
- Firefox と Eclipse の 576 件から、再現不能の要因 11 個を挙げ、開発者 13 人に調査。先行研究は「起票時にどう検出・改善するか」に実行可能な示唆がなかったと指摘 — [Rahman, Khomh, Castelluccio EMSE 2022](https://link.springer.com/10.1007/s10664-022-10153-2)（検索要約のみ）
- 100 プロジェクト、約 190 万 issue の分析で、テンプレートのあるプロジェクトの issue は解決が速くコメントが少ない。YAML の issue forms は解決時間、再オープン数、議論の長さを減らす。メンテナの 85% が利点に同意。観察研究なので因果は示していない — [Sülün et al. TOSEM 2024](https://repository.bilkent.edu.tr/items/a0c0b7c6-621e-4ca8-b17f-2843dfa072bf)（検索要約のみ）

**インシデント分析**
- 「Because overt failure requires multiple faults, there is no isolated 'cause' of an accident.」。根本原因への帰属は「the social, cultural need to blame specific, localized forces or events」の表れ — [How Complex Systems Fail](https://how.complexsystems.fail/)
- 「Hindsight bias remains the primary obstacle to accident investigation」。実務者の行動はすべて不確かさの下での賭けで、成功は気づかれず、失敗は後から厳しく裁かれる — [同](https://how.complexsystems.fail/)
- 原因に基づく見方（個人を責める）は防御を制限し、結合と複雑さを増やす — [同](https://how.complexsystems.fail/)
- Allspaw は Five Whys を捨てるべきだとする。「why」は個人や「human error」に向かい、「how」は作業の条件を語らせる。「Cause is something we construct, not find.」。当事者は「they thought what they were doing made sense」（局所合理性）— [The Infinite Hows](https://www.oreilly.com/radar/the-infinite-hows/)
- Hochstein は「no root cause」の立場で、寄与要因は鎖ではなく網に近いと書く。投稿「The problem with a root cause is that it explains too much」がある — [Surfing Complexity](https://surfingcomplexity.blog/author/lorinh)（検索要約のみ。該当記事の URL は 404）

**OSS メンテナの注意資源**
- Eghbal は、メンテナの注意を奪い合う利用者の過剰な参加が問題だとし、評価にかかる手間が貢献の価値を上回る「extractive」な貢献を区別した。解決策として、Twitch のモデレーターのような curator が価値の低い issue/PR をふるい落とす案を示した — 書評経由: [wsvincent.com](https://www.wsvincent.com/working-in-public-book-review/)、[dev.to](https://dev.to/emma/working-in-public-how-can-we-solve-the-problems-of-open-source-3ohl)（検索要約のみ。原文で語句を要確認）

### Inferences
- 決定的な情報（再現手順、bisect、版の範囲）は報告者のほうが用意しにくい（Zimmermann の不一致）。そのため各プロジェクトは「欠けている情報」をラベルとして可視化し、誰が次に何をすべきかを状態で示している。
- Chromium の規則は、判断を「前提条件と緩和要因の列挙」に分解している。severity の値だけでなく、どの前提を置いたかを記録できる形になっている。
- BugBug は「確信が高いときだけ自動化し、残りは人に回す」設計と、「起票時点の情報だけで学習する」設計の2点で、評価支援の仕組みの手本になる。

### Gaps
- Mozilla の S1〜S4 の正式定義（BMO User Guide）は本文未確認。
- Chromium の sheriffing（バグの当番）文書は未確認。

## 3. 何がうまくいかないか（重要度の水増し、重複、再現不能、stale bot、AI 生成報告、燃え尽き）

### Takeaway
失敗は、(a) 評価コストの非対称（作るのは安く、棄却は高い）、(b) 単一の数値への圧縮（CVSS、Priority 一本）、(c) 時間だけを根拠にした自動クローズ、(d) 権限のない追跡役への負担集中、として現れている。

### Cited Findings
- **AI 生成報告**: 2025 年以降、curl の確認率は 15% 超から 5% 未満に落ちた。報告者の一部は修正を助けるより severity を言い張ることに集中した。「The never-ending slop submissions take a serious mental toll to manage」 — [the end of the curl bug bounty](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/)
- **重要度の水増し**: 汎用ライブラリに CVSS を付けると高めの数値になり、スキャナが警報を出す。curl が付けないと CISA が推測で付ける — [CVSS is dead to us](https://daniel.haxx.se/blog/2025/01/23/cvss-is-dead-to-us/)、CISA の部分は検索要約のみ
- **再現不能**: 約 17% を占め、長く開いたままになる — [MSR 2014](https://people.ece.ubc.ca/amesbah/resources/papers/mona-msr14.pdf)（検索要約のみ）
- **stale bot**: 導入後、PR の滞留は減り、レビューも速くなったが、「the projects experienced a considerable decrease in their number of active contributors after the adoption」。ボットだけに頼ると「an increased probability of contributor abandonment」 — [Khatoonabadi et al. arXiv 2305.18150](https://arxiv.org/abs/2305.18150)（要旨のみ）
- **ボットのノイズ**: OSS のボットは disruptive で noisy、情報過多を招く — [Wessel et al. CSCW 2021 "Don't Disturb Me"](https://arxiv.org/abs/2103.13950)（要旨のみ）
- Wessel らの BotSE 2019 は 765 プロジェクトの stale bot の設定を調べたもので、害を主張する論文ではない。設定がほとんど見直されていないことなどを報告 — [BotSE 2019](https://www.ime.usp.br/~gerosa/papers/BotSE2019.pdf)（検索要約のみ）。依頼文の「Wessel on stale bots harms」は、害の実証としては Khatoonabadi らのほうが近い
- Django の議論では、メンテナが「有効な issue を自動で放棄する試みは役に立たない」と述べた — [django-developers](https://groups.google.com/g/django-developers/c/RAGuVJhT_3M/m/i2h1k-U-AAAJ)（検索要約のみ）
- **追跡役の燃え尽き**: Leemhuis は 2024 年、regression 追跡をやめることを考えていると述べた。資金が切れ、メンテナに催促すると摩擦が生じ、権限がないと言われる。多くのメンテナや Torvalds も返答しない。regressions リストへの CC や Closes タグが少ない。「the most important task is to establish some real deadlines for regression response」 — [LWN 990599](https://lwn.net/Articles/990599/)
- **後知恵**: 結果を知る者には警告サインが実際より明らかに見え、「should have known」と結論しがち — [How Complex Systems Fail](https://how.complexsystems.fail/)

### Inferences
- AI 生成報告の問題は「真偽の判定」よりも「棄却のコスト」の問題として記述されている。理解支援の仕組みは、報告の主張を検証可能な部分（再現物、該当コード、版）に分け、検証できない主張を早く見分けられることが価値になる。
- stale bot の害は「時間経過」を「無効」の代理指標にしたことから来る。Mozilla の `stalled` のように、閉じずに状態として表すほうが情報を失わない。

### Gaps
- 重複検出の失敗（誤った重複クローズ）に関する一次資料は今回読めていない。
- Chromium の sheriff や Google VRP の内部での誤トリアージの事例は未確認。

## 4. 廃止・変更されたプロセスと、その理由

### Takeaway
変更の多くは「一つの値に複数の意味を詰めていた」ことと「金銭や自動化による誘因が判断の質を下げた」ことへの対応である。

### Cited Findings
- **Mozilla: Priority 中心から Severity 必須へ（2020年5月4日から）**。Emma Humphries の告知。「Using Priority alone conflates severity with scheduling.」。旧 Severity の既定値が NORMAL だったため「we could not easily determine when it was modified.」。目的は、どのバグがリリースの品質に影響するかを一貫して評価すること — [mozilla.tools.bmo](https://groups.google.com/g/mozilla.tools.bmo/c/uAZpsT_vd64)
- 既定値を `--` にしたことは、「未判断」と「判断して普通」を区別するための設計と読める（上記の引用からの推論）。現在も Priority は任意で、ガイドラインは「under review」 — [Triage for Bugzilla](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)
- **curl: バグバウンティの終了（2026年1月31日）**。2019 年以来、87 件の確認済み脆弱性に 10 万 USD 超を払った。金銭の誘因が濫用の大きな原因とみなされた。報告料を取る案は、複雑さと正当な報告者を排除するおそれから採らなかった。報告は GitHub の private vulnerability reporting とメールで受ける — [the end of the curl bug bounty](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/)。報道では 78 件・約 86,000 USD という数字もあり、本人のブログと食い違う — [TechRadar](https://www.techradar.com/pro/security/curl-will-stop-bug-bounties-program-due-to-avalanche-of-ai-slop)（検索要約のみ）。その後 HackerOne に（報酬なしで）戻ったという記述もあるが、時期は未確認（検索要約のみ）
- **curl: CVSS の放棄（2025年1月）**。独自の4段階に置き換えた — [CVSS is dead to us](https://daniel.haxx.se/blog/2025/01/23/cvss-is-dead-to-us/)
- **stale bot の撤去**: AssemblyScript は 2021 年に「Stale bot is dead, long live stale action」をマージ（Probot の stale から GitHub Action へ置き換えで、廃止ではない）。Semantic-UI-React はコアリポジトリから撤去。Meteor は stale bot をやめてラベルに移行 — [AssemblyScript #1880](https://github.com/AssemblyScript/assemblyscript/pull/1880)、[Meteor forum](https://forums.meteor.com/t/oh-no-its-stale-bot/51074)（いずれも検索要約のみ）。Drew DeVault「GitHub stale bot considered harmful」（2021-10-26）— [drewdevault.com](https://drewdevault.com/blog/stalebot/)（本文未取得）
- **regzbot の移管（2026年5月）**: regzbot は KernelCI プロジェクトに加わる — [kernelci.org](https://kernelci.org/2026/05/)（検索要約のみ）。2022 年5月から Meta の資金で支えられていた（検索要約のみ）

### Inferences
- Mozilla の変更は、「影響の大きさ（事実寄りの評価）」と「いつやるか（資源配分の決定）」を別の欄に分けた。評価支援の仕組みでも、この2つを一つのスコアにまとめないほうがよい。
- curl の事例は、報告者への誘因の設計が受け手の評価コストを直接決めることを示す。

### Gaps
- Mozilla が Priority のガイドラインを「under review」にしている理由と、その後の結論は未確認。
- Kubernetes が stale/rotten のライフサイクルを採った理由（fejta-bot 時代の議論）は未確認。

## 5. 「この issue を理解・評価する」仕組みの設計原則の候補

### Takeaway
資料から次の原則が導ける。各原則には根拠を添える。これらは Claude の推論であり、ユーザーの判断ではない。

### Cited Findings（原則と根拠）
1. **影響の評価と予定の決定を分ける。** Mozilla は Priority 一本では severity と scheduling が混ざると判断した — [mozilla.tools.bmo](https://groups.google.com/g/mozilla.tools.bmo/c/uAZpsT_vd64)
2. **「未判断」と「判断済み」を区別できる既定値にする。** 旧既定値 NORMAL では変更されたかどうかがわからなかった — [同](https://groups.google.com/g/mozilla.tools.bmo/c/uAZpsT_vd64)
3. **評価の変更には理由を残す。** Mozilla は severity の変更にコメントを必須にしている — [Triage for Bugzilla](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)
4. **評価を「前提条件と緩和要因」に分解して見せる。** Chromium は緩和要因ごとに何段階下げるかを定め、侵害を仮定してよいプロセスを限定している — [Severity Guidelines](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md)。curl は文脈を見ない数値（CVSS）を拒否した — [CVSS is dead to us](https://daniel.haxx.se/blog/2025/01/23/cvss-is-dead-to-us/)
5. **欠けている情報を状態として示し、次に誰が何をするかを書く。** Rust の `S-needs-repro` / `E-needs-bisection`、Kubernetes の `triage/needs-information`、CPython の「次の行動を短くコメント」 — [Rust](https://forge.rust-lang.org/release/issue-triaging.html)、[Kubernetes](https://github.com/kubernetes/community/blob/master/contributors/guide/issue-triage.md)、[CPython](https://devguide.python.org/triage/triaging/)
6. **決定的な証拠（再現物、最後に動いた版と最初に壊れた版、bisect の結果）を中心に置く。** — [kernel](https://docs.kernel.org/admin-guide/reporting-regressions.html)、[Rust](https://forge.rust-lang.org/release/issue-triaging.html)
7. **自動化は確信が高いときだけ行い、確信度を見せ、残りを人に回す。** BugBug の 60% の閾値 — [Mozilla Hacks](https://hacks.mozilla.org/2019/04/teaching-machines-to-triage-firefox-bugs/)
8. **後から付いた情報で評価を学ばない／見せない（起票時点の情報で判断の妥当性を見る）。** BugBug の巻き戻し、Cook の後知恵バイアス — [Mozilla Hacks](https://hacks.mozilla.org/2019/04/teaching-machines-to-triage-firefox-bugs/)、[How Complex Systems Fail](https://how.complexsystems.fail/)
9. **単一の根本原因に収束させず、寄与要因を並べる。「why」より「how」を問う。** — [How Complex Systems Fail](https://how.complexsystems.fail/)、[The Infinite Hows](https://www.oreilly.com/radar/the-infinite-hows/)
10. **時間経過だけで閉じない。閉じる理由を区別する（無効・重複・情報不足・停滞）。** stale bot 導入後の貢献者減少、Mozilla の `stalled` — [arXiv 2305.18150](https://arxiv.org/abs/2305.18150)、[Triage for Bugzilla](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)
11. **検証可能な主張と検証できない主張を分け、棄却のコストを下げる。** よく書けた偽報告ほど棄却に時間がかかる — [daniel.haxx.se 2024](https://daniel.haxx.se/blog/2024/01/02/the-i-in-llm-stands-for-intelligence/)
12. **長いスレッドを要約し、チームで理解を共有する。** CPython のチェックリスト — [CPython](https://devguide.python.org/triage/triaging/)
13. **担当（誰が判断するか）と期限を明示する。** Mozilla の Triage Owner、Leemhuis の「real deadlines for regression response」 — [Triage for Bugzilla](https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html)、[LWN 990599](https://lwn.net/Articles/990599/)
14. **通知を増やしすぎない。** ボットはノイズと情報過多を生む — [Wessel et al. CSCW 2021](https://arxiv.org/abs/2103.13950)（要旨のみ）

### Inferences
- 原則 4・8・9 は互いに支え合う。評価を分解して記録すれば、後から結果を知った人がどの前提が違ったのかを見られ、「誰が間違えたか」ではなく「どの前提が外れたか」として学べる。
- 原則 7 と 11 は、AI を使う評価支援そのものにも当てはまる。仕組みが出す評価も「よく書けた、もっともらしい主張」になりうるので、確信度と検証可能な根拠を添えなければ、curl が受けたのと同じ棄却コストを利用者に負わせる。
- 上流に報告すべきか（upstream）の判断は、今回の資料では kernel の「upstream と distro の版の違い」以外に直接の規則がない。

### Gaps
- 「上流に報告すべきか」「誰が担当すべきか」を決める明文化された基準は、Kubernetes の SIG 振り分けと Mozilla の Triage Owner 以外に見つけていない。

## 6. 未確認（要旨のみ・検索要約のみ・未着手）

### Takeaway
インシデント分析コミュニティの主要な資料と、バグバウンティのトリアージ文書は本文を読めていない。報告書でこれらを根拠にするなら、追加の確認が要る。

### Cited Findings
- Etsy の Debriefing Facilitation Guide（Allspaw ほか）: 取得失敗（HTTP 403）— [etsy.com](https://www.etsy.com/codeascraft/debriefing-facilitation-guide)
- Drew DeVault の stale bot 批判: リダイレクトで本文取得失敗 — [drewdevault.com](https://drewdevault.com/blog/stalebot/)
- Hochstein の root cause 記事: URL が 404。主張は検索要約のみ — [Surfing Complexity](https://surfingcomplexity.blog/author/lorinh)
- Wessel らの研究（BotSE 2019、CSCW 2021）、Khatoonabadi ら、Sülün ら、Zimmermann/Bettenburg ら、Erfani Joorabchi ら、Rahman ら: abstract または検索要約のみ。
- Eghbal『Working in Public』: 書評経由のみ。「extractive」の定義の原文は未確認。

### Gaps
- 未着手: Nora Jones / Jeli（Howie ガイド）、Laura Maguire（インシデント中の協調の研究）、Learning From Incidents サイト、Google VRP のトリアージ方針、HackerOne のトリアージ文書、Chromium の bug sheriffing、Python の Triage Team ページ、Rust の compiler prioritization procedure。
- 依頼にあった「Wessel の stale bot の害」は、Wessel 本人の論文では確認できなかった。害を示したのは Khatoonabadi らの研究（Wessel は著者ではない）。
