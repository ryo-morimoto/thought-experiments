# コード・変更の理解を支援する業界ツールと、それを作った人々（レビューツール・コードツアー・理解支援製品）

調査日: 2026-11-21。一次資料（公式ブログ、論文、ドキュメント、GitHub API）を優先した。WebFetch は小型モデルによる要約を経由しているため、引用は短く、取得元 URL を直後に置く。検索結果の要約だけに依拠した項目は「(検索要約のみ)」と記す。

## 1. 人とツールの一覧（どのツール、誰が作ったか）

### Takeaway
系譜は大きく 3 つ。(a) 「変更を小さく分けて順に読ませる」系（Phabricator/Evan Priestley → Meta の stacked diffs → Graphite/Tomas Reimers・Greg Foster、Sapling ReviewStack）、(b) 「何を読んだか・何が変わったかを追跡する」系（Review Board/Christian Hammond、Reviewable/Piotr Kaminski、Jane Street Iron/Yaron Minsky、Google Critique）、(c) 「コードの地図・ツアー・説明を作る」系（CodeTour/Jonathan Carter、CodeSee/Shanea Leven、Swimm、Sourcegraph/Quinn Slack・Beyang Liu、Unblocked/Dennis Pilarinos）。2025〜2026 年に (c) が AI 生成の「PR ウォークスルー」（CodeRabbit Change Stack、Cursor/Graphite Code Tours、Sourcegraph guided diff tour、balade、pr-tour）として PR レビューへ合流した。

### Cited Findings
- pr-tour: 作者 GitHub アカウント YunSinLee、所属 UNIST（蔚山）とプロフィールに記載。他の公開リポジトリは Coursera 課題や React 講座の練習などで、pr-tour が初の本格的な公開ツールに見える — [GitHub profile](https://github.com/YunSinLee)。リポジトリ作成 2026-09-12、最終 push 2026-10-23、v0.8.1（GitHub API `repos/YunSinLee/pr-tour` で確認）— [repo](https://github.com/YunSinLee/pr-tour)
- CodeTour: Jonathan Carter（Microsoft。Codespaces・Live Share・IntelliCode を担当し、CodeTour・GistPad などを保守と自己紹介）— [dev.to/lostintangent](https://dev.to/lostintangent)（検索要約のみ）。リポジトリ作成 2020-03-07、アーカイブされていない、最終 push 2026-05-05（GitHub API）— [microsoft/codetour](https://github.com/microsoft/codetour)
- CodeTour の利用研究: Grace Taylor・Steven Clarke（Microsoft）「A Tour Through Code」PPIG 2022 — [PDF](https://ppig.org/files/2022-PPIG-33rd-taylor.pdf)
- CodeSee: 共同創業者・CEO Shanea Leven。2019 年サンフランシスコ創業、CodeSee Maps（2021-11）、CodeSee 2.0（2022-08）— [Product Hunt launches](https://www.producthunt.com/products/codesee/launches)（検索要約のみ）
- Swimm: code-coupled docs と Auto-sync — [Swimm blog](https://swimm.io/blog/how-does-swimm-s-auto-sync-feature-work/)
- Sourcegraph: Quinn Slack・Beyang Liu が 2013 年に創業（検索要約のみ）。2025 年に Amp が独立会社化し、Slack と Liu は Amp Inc. を創業、Sourcegraph の CEO は Dan Adler — [Sourcegraph blog](https://sourcegraph.com/blog/why-sourcegraph-and-amp-are-becoming-independent-companies)
- Graphite: Tomas Reimers は共同創業前に Meta で約 2.5 年勤務 — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/stacked-diffs)（検索要約のみ）。Greg Foster も Graphite ブログの著者 — [Why Facebook doesn't use Git](https://graphite.com/blog/why-facebook-doesnt-use-git)（検索要約のみ）
- Phabricator: phacility/phabricator の description は "Effective June 1, 2021: Phabricator is no longer actively maintained."（GitHub API）— [repo](https://github.com/phacility/phabricator)
- Google Critique: Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko（Google）と Alberto Bacchelli「Modern Code Review: A Case Study at Google」ICSE-SEIP 2018 — [PDF](https://sback.it/publications/icse2018seip.pdf)
- Review Board: Christian Hammond と David Trowbridge が VMware でのレビューへの不満から作り、のち Beanbag を設立 — [LWN](https://lwn.net/Articles/265239/)、[Beanbag 設立告知](https://www.reviewboard.org/news/2010/11/12/announcing-the-formation-of-beanbag-inc)（検索要約のみ）
- Difftastic: Wilfred Hughes。リポジトリ作成 2018-12-18、現役（GitHub API）— [Wilfred/difftastic](https://github.com/Wilfred/difftastic)
- SemanticDiff: Michael Müller — [blog](https://semanticdiff.com/blog/language-aware-diff-how-far/)
- Greptile: 共同創業者 Daksh Gupta — [make llms shut up](https://greptile.com/blog/make-llms-shut-up)
- Ellipsis（YC W24）: CEO Hunter Brooks、共同創業者 Nick Bradford — [YC](https://www.ycombinator.com/companies/ellipsis)、[Bradford の記事](https://nickbradford.substack.com/p/lessons-from-27-months-building-llm)
- Unblocked: Dennis Pilarinos（前職 Buddybuild を創業し 2018 年に Apple へ売却、Xcode Cloud に従事）— [TechCrunch](https://techcrunch.com/?p=3002251)、[Unblocked origin video](https://getunblocked.com/videos/the-origin-story-of-unblocked/)（検索要約のみ）
- Pull Panda: Abi Noda（創業者・CEO）— [GitHub blog](https://github.blog/news-insights/company-news/github-acquires-pull-panda/)
- 最近の PR ウォークスルー: CodeRabbit Change Stack（Priyanka Kukreja, 2026-05-13）— [blog](https://www.coderabbit.ai/blog/introducing-change-stack-the-first-ai-native-code-review-interface)、CodeRabbit Review（Yiwen Xu, 2026-06-09）— [blog](https://coderabbit.ai/blog/coderabbit-review-reads-a-pr-how-author-would-explain-it)、Graphite Code Tours（Peter Stakoun, 2026-04-01）— [blog](https://graphite.com/blog/code-tours)（本文 404、検索要約のみ）、Cursor Origin Code Tours — [docs](https://cursor.com/docs/origin/code-tours)、Sourcegraph guided diff tour（Felix Kling, Stefan Hengl, Kalan Chan, 2026-08-17）— [changelog](https://sourcegraph.com/changelog/guided-diff-tour-beta)、balade — [GitHub](https://github.com/basaltbytes/balade)、Guided Review・prtour・Warp pr-walkthrough skill（存在のみ確認、本文未読）— [Guided Review](https://alternativeto.net/software/guided-review/about/)、[prtour](https://skillsmp.com/creators/2018kguo/prtour)、[pr-walkthrough](https://tessl.io/registry/skills/github/warpdotdev/common-skills/pr-walkthrough)

### Inferences
- pr-tour の作者は大学所属の個人開発者と見られ、会社の製品ではない。設計判断は README と SKILL.md にすべて書かれており、それが一次資料になる（ブログ・講演は見つからなかった）。
- 2026 年に「PR をツアーにする」機能が 5 社以上でほぼ同時に出た。差別化の軸は「並べ方」より「誰が説明を書くか」「信頼をどう担保するか」に移っている。

### Gaps
- Gerrit（Shawn Pearce）、Meta 社内の Phabricator 後継、Atlassian Crucible の設計者については、時間内に一次資料（設計文書・講演）に当たれなかった。
- Reviewable の作者 Piotr Kaminski 本人の設計文書は見つからず、ドキュメントにも著者名がない。
- Jonathan Carter による CodeTour の動機を書いた投稿は見つからなかった。

## 2. ツールごとの資産（知識・洞察・意図）

### Takeaway
最も効く洞察は 3 つ。(1) レビューの元の目的は欠陥発見ではなく、理解しやすさと知識の共有だった（Google）。(2) 「つまらない部分を読ませない」こと、つまり前回から変わった差分だけを見せることが注意を保つ（Iron、Reviewable、Review Board）。(3) ツアーは読むファイルを絞るが、その分探索を減らす。品質は書いた人次第（CodeTour の研究）。

### Cited Findings

**pr-tour（YunSinLee）**
- 目的: "Follow the execution flow, read the real diff, and open the definitions you need without losing your place." — [README](https://github.com/YunSinLee/pr-tour)
- 並べ方: ファイルパス順ではなくコードの流れ順。同じファイルが複数の step に出てよい — [README](https://github.com/YunSinLee/pr-tour)
- 説明を書くのはエージェントで、スクリプトではない: "The Python script alone does not generate explanations from a PR URL." — [README](https://github.com/YunSinLee/pr-tour)
- 定義リンクは IDE ではなく人が書いた対応表: "Definition links are authored mappings, not an IDE language server." — [README](https://github.com/YunSinLee/pr-tour)
- step 間の遷移（transition）を必須にし、未検証のつながりは `inferred` と具体的な `uncertainty` で示し、実行順ではない並べ替えは `reading` と区別する。`source` 引用は「自動で証明された呼び出し辺ではなく解釈の記録」と明記 — [SKILL.md](https://github.com/YunSinLee/pr-tour/blob/main/skills/pr-tour/SKILL.md)
- 読者はリポジトリにもドメインにも新しいと仮定し、まず問題と最小限の背景から書く。変更した振る舞いは before/after と呼び出し側への影響を先に書き、各 step の最後に確認すべき具体的なことを置く — [SKILL.md](https://github.com/YunSinLee/pr-tour/blob/main/skills/pr-tour/SKILL.md)
- 全変更ファイル（テスト・設定・削除・リネーム・バイナリ）を必ず網羅する。機械的な変更はまとめて短く。ファイル名や PR 説明だけから振る舞いを推測しない — [SKILL.md](https://github.com/YunSinLee/pr-tour/blob/main/skills/pr-tour/SKILL.md)
- ビルダーはソースの再構成と行範囲を検証するが、説明の正しさは保証しない — [README](https://github.com/YunSinLee/pr-tour)
- 読者のコメントはブラウザに保存し、AI 会話用の Markdown として出せる。GitHub には投稿しない — [README](https://github.com/YunSinLee/pr-tour)

**CodeTour（Jonathan Carter, Microsoft）**
- "It's like a table of contents, that can make it easier to onboard (or re-board!)" ツアーはリポジトリにコミットして共有できる — [README](https://github.com/microsoft/codetour)
- 研究の動機: 関係をたどってみるまで、その関係が関係あるかどうか分からないので後戻りが生じる。ツアーはツールだけでは見つけにくい関係を示せる — [Taylor & Clarke, PPIG 2022](https://ppig.org/files/2022-PPIG-33rd-taylor.pdf)
- 結果: ツアー群は無関係なファイル（PencilPaint.java など）を開かず、ファイル名を頼りに探す行動が減った。一方、開いたファイル数は少なく、H2（もっと探索させる）は否定された。著者は「ツアーにない部分は重要でないと思わせ、偶然の発見を減らすこと」を懸念 — [同上](https://ppig.org/files/2022-PPIG-33rd-taylor.pdf)
- 参加者はファイル名ではなく、ツアーの step を通じてコードを参照するようになった — [同上](https://ppig.org/files/2022-PPIG-33rd-taylor.pdf)
- 読む人は損得を計る: バグを直したいだけの参加者はツアーを読むコストに見合わないと判断した。テキスト中心のツアーに圧倒され、デバッガで追う方がよかったと言う参加者もいた — [同上](https://ppig.org/files/2022-PPIG-33rd-taylor.pdf)
- "It instills a level of confidence that somebody has thought this through."（参加者 ct5）— [同上](https://ppig.org/files/2022-PPIG-33rd-taylor.pdf)
- 限界: "CodeTour's usefulness is limited by the authors' ability to share helpful annotations"。参加者が少なく統計的に有意でない — [同上](https://ppig.org/files/2022-PPIG-33rd-taylor.pdf)

**Google Critique（Sadowski ほか）**
- レビュー導入の主目的は、他の開発者が理解できるコードを書かせることだった。"code must act as a teacher for future developers"。バグ発見は歓迎されるが主目的ではない — [ICSE-SEIP 2018](https://sback.it/publications/icse2018seip.pdf)
- 期待は 4 つ（education, maintaining norms, gatekeeping, accident prevention）で、どれが主になるかは作者とレビュアーの関係による。レビュー履歴は後から、変更の経緯やバグの混入を理解するのにも使われる — [同上](https://sback.it/publications/icse2018seip.pdf)
- 変更の 35% 超が 1 ファイルのみ、約 90% が 10 ファイル未満、変更行数の中央値は 24。初回フィードバックまでの中央値は小さい変更で 1 時間未満、非常に大きい変更で約 5 時間。全体の中央値は 4 時間未満 — [同上](https://sback.it/publications/icse2018seip.pdf)
- 80% 超の変更は、コメント解決のやりとりが 1 回以内。スナップショットの任意の 2 つの間の差分を見られる。静的解析の結果は人のコメントと並べて色を変えて表示される。開発者の 97% が Critique に満足 — [同上](https://sback.it/publications/icse2018seip.pdf)

**Phabricator（Evan Priestley / Phacility）**
- "Each commit should do one thing." / "The complexity of understanding, testing and reviewing a change often increases faster than its size" / "The real goal is for each change to have minimal complexity, line size is just a proxy" / コミットメッセージは理由を書くことが最重要 — [Writing Reviewable Code](https://secure.phabricator.com/book/phabflavor/article/writing_reviewable_code/)
- 事前レビューは事後監査より強い。変更が承認まで止まるので、作者に小さくよく説明された変更を書く動機が生まれ、設計への指摘も安いうちにできる — [Review vs Audit](https://secure.phabricator.com/book/phabricator/article/reviews_vs_audit/)

**Meta（Sapling ReviewStack、レビュー時間の改善）**
- 既存ツールの多くは "optimized for reviewing the entire pull request at once instead of individual commits"。ReviewStack は stack 内の 1 コミットごとに会話と状態を 1 ページに置き、stack 内を移動するナビゲーションを持つデモ UI — [Sapling 発表](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)
- North star は Time In Review の P75（満足度調査と相関したため）。速度の代償で流し読み（rubber-stamp）が起きないよう、ガードレールとして Eyeball Time を置いた — [Meta engineering](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/)
- Next Reviewable Diff で 1 日あたりのレビュー操作が 17% 増。Nudgebot で平均 Time In Review が 7% 減、3 日超待つ diff が 12% 減 — [同上](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/)

**Jane Street Iron（Yaron Minsky）**
- "Humans are bad at carefully thinking about boring things" — 変更のない部分を読み直させない。レビュアーは前回見た版からの差分（F1→F2）だけを読む。衝突したマージは diff-of-diffs で示す。コードではなくレビューを rebase する — [Code review that isn't boring](https://blog.janestreet.com/code-review-that-isnt-boring/)

**Reviewable**
- "Keep track of who reviewed which revision of each file to ensure that no changes are missed." / rebase や amend されても前回見たときからの差分を示す / 議論ごとに参加者の立場を追跡し、解決するまで消えない — [docs](https://docs.reviewable.io/)

**Review Board（Christian Hammond）**
- パッチが変わるとコメントがどのコードに対するものか追えなくなる問題に対し、パッチの任意の 2 版を比較できるようにした。2009 年初頭には VMware の大半と推定 50〜100 社が採用 — [chipx86 blog](https://blog.chipx86.com/2009/01/19/review-board-10-alpha-1-released)（検索要約のみ）

**Graphite（Tomas Reimers, Greg Foster）**
- "Stacking lets you make many small PRs easily, and without having to wait for review."（Reimers）— [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/stacked-diffs)（検索要約のみ）
- 2026-04 に Code Tours を発表（PR を変更のガイド付きウォークスルーにする）— [graphite.com/blog/code-tours](https://graphite.com/blog/code-tours)（本文 404、検索要約のみ）

**Swimm（Auto-sync）**
- 静的解析は使わず、コードを文字列として扱って言語非依存にする。結び付ける対象は snippet、smart token（識別子）、smart path（ファイル・フォルダ）と Git 履歴 — [Swimm blog](https://swimm.io/blog/how-does-swimm-s-auto-sync-feature-work/)
- 判定は「動いただけか」「自明な変更（リネーム・削除）か」「近くの token はどうなったか」と順に問う決定木。自信がなければ人に snippet の選び直しを頼む: "We'd rather ask you to reselect a snippet than offer a strange suggestion." — [同上](https://swimm.io/blog/how-does-swimm-s-auto-sync-feature-work/)
- 完全な Git 履歴が必要（shallow clone は不可）。CI を遅くしないことが制約 — [同上](https://swimm.io/blog/how-does-swimm-s-auto-sync-feature-work/)

**Difftastic（Wilfred Hughes）・SemanticDiff（Michael Müller）**
- 構文 diff の難所: 区切り記号の移動（"x has changed its depth in the tree, but x itself is unchanged"）、同一ノードの slider、書き換えが細切れの変更に見えること、長い文字列リテラル。"unordered tree diffing is NP-hard" なので順序変更は常に報告する。パースに失敗したら行 diff に戻る — [tricky cases](https://difftastic.wilfred.me.uk/tricky_cases.html)
- SemanticDiff は無関係な変更を 4 段階に分け、意味的に等価な変更（段階 3）の途中までを隠す。"Developers will only use a diff/code review tool if they can trust it" ので、意味を変えうる変更（import の並べ替えなど）は既定で隠さない — [How far](https://semanticdiff.com/blog/language-aware-diff-how-far/)

**CodeSee（Shanea Leven）**
- コードを読んで理解することに少なくとも時間の 60% を使うと推定。理解しようとしている間にも同僚がコードを出荷し続ける — [girlgeek.io](https://girlgeek.io/?p=11033)（検索要約のみ）
- 製品は自動生成のマップ（ディレクトリ、依存、変更）と Review Maps、Review Map Tours — [VentureBeat](https://venturebeat.com/business/codesee-helps-developers-visualize-and-understand-complex-codebases)、[Review Map Tours](https://learn.codesee.io/introducing-review-map-tours-guide-reviewers-through-a-pull-request/)（ドメイン消滅で本文取得不可、タイトルのみ）

**Sourcegraph / Amp（Quinn Slack, Beyang Liu）**
- 分社の理由: "totally different distribution engines and target audiences"。Sourcegraph はエンタープライズ向けの安定した提供、Amp はモデル・エージェントの最前線での実験が必要 — [Sourcegraph blog](https://sourcegraph.com/blog/why-sourcegraph-and-amp-are-becoming-independent-companies)
- Sourcegraph は自らを、コーディングエージェントに文脈を与えるインフラと位置付け直した — [同上](https://sourcegraph.com/blog/why-sourcegraph-and-amp-are-becoming-independent-companies)
- guided diff tour（Beta）: 大きな diff のために、重要なファイルを先に置き、残りを section にまとめて短い説明を付ける。生成したツアーはキャッシュする — [changelog](https://sourcegraph.com/changelog/guided-diff-tour-beta)

**AI レビュー（Greptile, Ellipsis, CodeRabbit）**
- Greptile: 既存コメントを監査すると良いもの約 19%、誤り 2%、nit 79%。nit は "technically true but not something the dev cared about"。プロンプト調整は nit と一緒に重要なコメントも減らした。LLM に重大度を 1〜10 で採点させる方法はほぼランダムだった。チームごとに過去コメントを埋め込み、downvote されたものに似たコメントを止める方式で、address rate が 2 週間で 19% から 55% 超になった — [Daksh Gupta, 2024-12-18](https://greptile.com/blog/make-llms-shut-up)
- Ellipsis: 誤検出は AI レビューへの "most common complaint"。多段のフィルタ（信頼度の閾値、重複除去、コード上の証拠を使う幻覚チェック）を通す。止めたコメントも理由と共に残して見えるようにする。LLM は行番号・列番号の特定が苦手なのでシンボル名で照合する — [Nick Bradford](https://nickbradford.substack.com/p/lessons-from-27-months-building-llm)
- CodeRabbit Change Stack: 2008 年以来のアルファベット順のファイル一覧では、作者が物語として理解している変更をレビュアーが自分で組み立て直す必要がある。関連する変更を少数の独立した cohort に分け、各 cohort を読む順の layer に分ける。図は役立つときだけ出す。AI コメントを PR スレッドに足すことはかえって認知負荷を増やすと明言。GitHub を記録の正本とし、opt-in — [Change Stack](https://www.coderabbit.ai/blog/introducing-change-stack-the-first-ai-native-code-review-interface)
- CodeRabbit Review: cohort は依存の順（スキーマ → ビジネスロジック → 呼び出し側 → フロントエンド → テスト）。関係が明確なときだけ cohort を作る。動機として、レビュアーが "no longer meaningfully engaging with the changes" になったことを挙げる — [CodeRabbit Review](https://coderabbit.ai/blog/coderabbit-review-reads-a-pr-how-author-would-explain-it)
- Cursor Code Tours: 変更の内容と理由から始め、関連する変更をまとめて、レビューに適した順に並べる。他のコードが依存する振る舞いなど、注意すべき箇所を示す。section ごとに reviewed にでき、Diff 表示と同期する。非常に大きい PR は "Too large for a tour" — [Cursor docs](https://cursor.com/docs/origin/code-tours)
- balade: "Human-readable walkthroughs for diffs too large to scan"。ウォークスルーを Markdoc ファイルとしてリポジトリにコミットし、frontmatter に PR 番号とコミット SHA を記録する。CI で検証し、PR の head が先に進むと stale 表示を出す。グループ分けはファイルを隠さない — [balade](https://github.com/basaltbytes/balade)
- Unblocked: コードの「what」ではなく「why」を、散らばった開発ツールの情報から集める "collective memory" — [radical.vc](https://radical.vc/portfolio/unblocked/)（検索要約のみ）

### Inferences
- Google の「レビューの主目的は理解しやすさと教育」は、pr-review の「チームの共有メンタルモデルを育てる」という目標の先行根拠になる。ただしこれは 2018 年の Google 内部の話である。
- Iron・Reviewable・Review Board・Critique はいずれも「前回読んだ版からの差分」を中心にしている。ツアー系の製品（pr-tour 含む）は 1 回読むことを前提にしており、PR が更新されたときの再読（どの step が変わったか）はまだ薄い。balade の stale 表示が例外。

### Gaps
- Google Critique の UI 設計（attention set など）を扱う、論文以外の builder 自身の記事は未確認。
- Iron の後続記事（scrutiny 管理など）は未読。

## 3. 終了・放棄されたものとその理由

### Takeaway
公表された理由は「プラットフォーム側が同じ機能を内製した」「会社の戦略」「理由を書かない」のいずれかで、「理解支援が役に立たなかった」という形の事後分析は見つからなかった。

### Cited Findings
- Phacility（Phabricator）: "Phacility is winding down operations." 理由は書かれておらず、理由を尋ねたコメントにも返答はない。新規ホスティングとサポート契約は 2021-06-01 で終了 — [Phacility 告知](https://admin.phacility.com/phame/post/view/11/phacility_is_winding_down_operations/)。コミュニティのフォーク Phorge が継続（このセッションでは未確認）
- CodeSee: GitKraken が 2024-05-14 に買収し、DevEx platform に統合。金額は非公開 — [GitKraken press](https://gitkraken.com/press/gitkraken-acquires-codesee-launches-devex-platform)（検索要約のみ）。CodeSee 社員の LinkedIn 投稿によれば、商業運営は 2 月 22 日（年は投稿断片からは不明。2024 年と推定）に停止 — [LinkedIn](https://sk.linkedin.com/in/daniel-ivanyi-16845458)（検索要約のみ）。codesee.io と learn.codesee.io は 2026-11 時点で DNS 解決不可（WebFetch のエラーで確認）
- Pull Panda: 2019-06 に GitHub が買収し無料化。Pull Reminders と Pull Assigner は GitHub 内製のレビュー割り当てと scheduled reminders に置き換えて先に終了し、残りも利用の大幅な減少と legacy であることを理由に 2022 年に前倒しで終了 — [GitHub changelog](https://github.blog/changelog/2022-03-23-pull-panda-is-shutting-down/)（検索要約のみ）
- Atlassian Fisheye/Crucible: 新規販売は 2025-05-13 に終了、サポート終了は 2028-05-15。basic maintenance mode — [Atlassian licensing](https://www.atlassian.com/licensing/fisheye-and-crucible)（検索要約のみ）
- Sourcegraph Cody: 個人向けプラン（Free/Pro/Enterprise Starter）を 2025 年に終了しエンタープライズ限定へ。Amp を分社 — [Sourcegraph blog](https://sourcegraph.com/blog/why-sourcegraph-and-amp-are-becoming-independent-companies)。プラン終了日は資料によって食い違う（2025-07-23 とする [Wikiwand](https://www.wikiwand.com/en/articles/Sourcegraph)、2025 年半ばに新規登録停止とする [PromptQuorum](https://www.promptquorum.com/power-local-llm/sourcegraph-cody-review)）
- Graphite: Cursor が 2025-12-19 に買収で合意。独立した製品として継続。Cursor は理由を、レビューとマージが "have increasingly become the bottlenecks" になったことと説明 — [Cursor blog](https://www.cursor.com/blog/graphite)
- Meta ReviewStack は「デモ」と位置付けて公開された — [Sapling 発表](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)。現状の保守状態は未確認

### Inferences
- Pull Panda の運命は「レビュー周辺の小さな改善はプラットフォームに吸収される」ことを示す。GitHub の外の HTML として独立する pr-tour は吸収されにくい一方、GitHub の PR 画面から遠いので使われにくい。
- CodeSee（自動生成の地図）は買収で終わり、2026 年には AI 生成の「PR ツアー」が各社で同時に出た。「全体の地図」から「この変更の順路」へ単位が移ったと読める。ただし CodeSee の失敗理由は公表されておらず、これは推論にとどまる。

### Gaps
- CodeSee の創業者による事後分析（何が売れなかったか）は見つからなかった。
- CodeTour がその後どう使われたか（利用データ）は見つからなかった。

## 4. 横断パターン

### Takeaway
(1) 並べ方: ファイル名順から依存順・流れ順へ。(2) 大きい変更は、分割（stack）と説明（ツアー）が補い合う。(3) 説明を作者が書くか生成するか: 作者の知識は品質を上げるが書くコストが高く、生成は安いが信頼とノイズが課題。(4) ドキュメントの鮮度: SHA で固定し、変化を検出し、自信がなければ人に戻す。(5) UI: ファイル単位からまとまり（概念）単位へ移りつつも、既読の追跡と「隠さない」保証は残す。

### Cited Findings
- 並べ方: アルファベット順のファイル一覧が問題の出発点（CodeRabbit）— [Change Stack](https://www.coderabbit.ai/blog/introducing-change-stack-the-first-ai-native-code-review-interface)。依存順（CodeRabbit Review）— [blog](https://coderabbit.ai/blog/coderabbit-review-reads-a-pr-how-author-would-explain-it)、実行の流れ順で同じファイルを複数回出してよい（pr-tour）— [README](https://github.com/YunSinLee/pr-tour)、重要なファイルを先頭に（Sourcegraph）— [changelog](https://sourcegraph.com/changelog/guided-diff-tour-beta)、内容と理由から始める（Cursor）— [docs](https://cursor.com/docs/origin/code-tours)
- 分割 vs 説明: Phabricator の「1 変更 1 アイデア」— [Writing Reviewable Code](https://secure.phabricator.com/book/phabflavor/article/writing_reviewable_code/)、Google の小さい変更と速いレビュー — [ICSE-SEIP 2018](https://sback.it/publications/icse2018seip.pdf)。説明系は大きい diff が対象: balade（"diffs too large to scan"）— [balade](https://github.com/basaltbytes/balade)、Sourcegraph（"reviewing large diffs"）— [changelog](https://sourcegraph.com/changelog/guided-diff-tour-beta)。ただし Cursor は非常に大きい PR ではツアーを出さない — [docs](https://cursor.com/docs/origin/code-tours)
- 作者が書く vs 生成: CodeTour は作者の力量に依存 — [PPIG 2022](https://ppig.org/files/2022-PPIG-33rd-taylor.pdf)。pr-tour はエージェントが書き、推論したつながりに印を付ける — [SKILL.md](https://github.com/YunSinLee/pr-tour/blob/main/skills/pr-tour/SKILL.md)。balade はエージェントが下書きし、リポジトリにコミットして CI で検証 — [balade](https://github.com/basaltbytes/balade)。Cursor は作成したエージェントによる書き直しも可能 — [docs](https://cursor.com/docs/origin/code-tours)。生成コメントの 79% が nit だった — [Greptile](https://greptile.com/blog/make-llms-shut-up)
- 鮮度: Swimm は自信がなければ人に戻す — [Swimm](https://swimm.io/blog/how-does-swimm-s-auto-sync-feature-work/)。balade は SHA を記録し stale を表示 — [balade](https://github.com/basaltbytes/balade)。pr-tour は head と base のコミットを固定し、更新時も明示的に頼まれない限り固定を維持 — [SKILL.md](https://github.com/YunSinLee/pr-tour/blob/main/skills/pr-tour/SKILL.md)
- 既読の追跡: ファイル × リビジョン単位（Reviewable）— [docs](https://docs.reviewable.io/)、前回からの差分のみ（Iron）— [Jane Street](https://blog.janestreet.com/code-review-that-isnt-boring/)、section 単位の reviewed（Cursor）— [docs](https://cursor.com/docs/origin/code-tours)、stack 内のコミット単位（ReviewStack）— [Sapling](https://engineering.fb.com/2022/11/15/open-source/sapling-source-control-scalable/)
- 隠さない保証: balade のグループ分けはファイルを隠さない — [balade](https://github.com/basaltbytes/balade)、pr-tour は全ファイルを網羅し、プレビューできないものも明示 — [SKILL.md](https://github.com/YunSinLee/pr-tour/blob/main/skills/pr-tour/SKILL.md)、SemanticDiff は信頼のため意味を変えうる変更を隠さない — [SemanticDiff](https://semanticdiff.com/blog/language-aware-diff-how-far/)
- 記録の正本はプラットフォームに置く: CodeRabbit は GitHub に書き戻す — [Change Stack](https://www.coderabbit.ai/blog/introducing-change-stack-the-first-ai-native-code-review-interface)。Reviewable も GitHub 専用 — [docs](https://docs.reviewable.io/)

### Inferences
- 「作者の説明」と「生成された説明」の中間として、エージェントが下書きし、リポジトリにコミットし、機械で検証し、人が直す形（balade、pr-tour）が出てきている。CodeTour の「作者の力量に依存する」という限界への答えと読める。
- 「ツアーが探索を狭める」（PPIG）という副作用に正面から対処している製品は見当たらなかった。対処に近いのは、全ファイルを網羅し diff へ戻れることだけ。

### Gaps
- 生成ツアーが理解や欠陥発見を改善したという公開された対照実験は見つからなかった。CodeRabbit の「約 20 分の把握が約 30 秒に」は 1 事例の逸話 — [Change Stack](https://www.coderabbit.ai/blog/introducing-change-stack-the-first-ai-native-code-review-interface)

## 5. 設計原則の候補とアンチパターン

### Takeaway
原則の候補: 変更の理由と前後の違いから入る／依存・実行の流れで並べ、並べ替えの種類を明示する／全変更を網羅し隠さない／推論と検証済みを区別する／スナップショットに固定し鮮度を検出する／再訪時は前回からの差分だけを見せる／生成物は「対処率」で測りノイズを削る／分割できるなら分割を先に勧める。アンチパターン: ファイル名順、nit の量産、ツアーを唯一の入口にすること、AI コメントの上乗せ、信頼できない省略。

### Cited Findings（各原則の根拠）
- 理由から入る: コミットメッセージは理由を書くのが最重要 — [Phabricator](https://secure.phabricator.com/book/phabflavor/article/writing_reviewable_code/)。Cursor のツアーは内容と理由から始める — [Cursor](https://cursor.com/docs/origin/code-tours)。"Code review should show more than what changed." — [CodeRabbit](https://www.coderabbit.ai/blog/introducing-change-stack-the-first-ai-native-code-review-interface)
- 推論と検証の区別: pr-tour の `inferred`／`reading` — [SKILL.md](https://github.com/YunSinLee/pr-tour/blob/main/skills/pr-tour/SKILL.md)。Ellipsis はコード上の証拠で幻覚を検査 — [Bradford](https://nickbradford.substack.com/p/lessons-from-27-months-building-llm)
- 測定: Greptile は address rate — [Greptile](https://greptile.com/blog/make-llms-shut-up)。Meta は速度を測りつつ Eyeball Time をガードレールにした — [Meta](https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/)
- 自信がなければ人に戻す — [Swimm](https://swimm.io/blog/how-does-swimm-s-auto-sync-feature-work/)
- アンチパターン「AI コメントの上乗せ」: CodeRabbit 自身が、PR スレッドへの AI コメントの追加は認知負荷を増やすと書いている — [Change Stack](https://www.coderabbit.ai/blog/introducing-change-stack-the-first-ai-native-code-review-interface)。nit は全体を無視させる — [Greptile](https://greptile.com/blog/make-llms-shut-up)
- アンチパターン「ツアーを唯一の入口にする」: ツアーにない部分は重要でないと思わせるおそれ — [PPIG 2022](https://ppig.org/files/2022-PPIG-33rd-taylor.pdf)
- アンチパターン「信頼できない省略」— [SemanticDiff](https://semanticdiff.com/blog/language-aware-diff-how-far/)
- 読む人の損得: タスクだけ片付けたい読者はツアーを読まない — [PPIG 2022](https://ppig.org/files/2022-PPIG-33rd-taylor.pdf)。Cursor はツアーの長さを変更の大きさに合わせる — [Cursor](https://cursor.com/docs/origin/code-tours)

### Inferences（設計原則の候補。pr-tour / pr-review 向け）
1. 入口は「何の問題を、何が前後でどう変わるか」。ファイル一覧ではない。
2. 並べ方は依存順か実行の流れ順にする。読みやすさのための並べ替えは、実行順と区別して印を付ける（pr-tour の `reading` はよい先例）。
3. 全変更を網羅し、グループ分けは並べ方であって隠すことではないと保証する。diff 本体へいつでも戻れるようにする（PPIG の「探索が狭まる」への対策）。
4. 説明は検証可能なもの（行範囲・引用）と推論とに分け、推論には不確かさを書く。
5. 説明は SHA に固定し、PR が更新されたら、どの step が古くなったか（前回からの差分）を示す。この点は既存ツアーで手薄（Iron・Reviewable の発想をツアーに移す）。
6. 生成物の価値は量ではなく「読者が行動したか」で測る（address rate、Eyeball Time のようなガードレール）。
7. 分割できる変更は分割を勧め、分割できない大きい変更（生成コード、横断リファクタ）にツアーを使う。Cursor が非常に大きい PR ではツアーを出さないことから、ツアーにも上限があると推定される。
8. pr-review の「共有メンタルモデル」については、Google の「レビューは教育」という知見と、関係（新人・同僚・他チーム）によって期待が変わるという知見から、コメントの種類を読み手との関係に合わせる設計が考えられる。
9. 記録の正本は既存プラットフォーム（GitHub）に置き、外部のビューは読み物にとどめるか、書き戻す。

### Gaps
- これらの原則が理解度を上げるかどうかを直接測った研究は、PPIG の小規模研究以外に見つからなかった。

## 6. 未検証・注意

- CodeSee の商業運営停止日（2/22）の年、Phorge の現状、ReviewStack の保守状態は未確認。
- Graphite Code Tours の本文（graphite.com/blog/code-tours）は 404 で読めず、著者と日付は検索要約のみ。
- Graphite の stacked PR に関する Reimers・Foster の一次記事（graphite.com/blog/stacked-prs）は 404。引用は Pragmatic Engineer 経由の検索要約のみ。
- Review Board の起源、Pull Panda の終了理由、Crucible の日付、Unblocked の経歴、Shanea Leven の「60%」発言は検索要約のみで、本文は未読。
- 「CodeTour は社内の開発チームの知識共有とオンボーディングの研究から生まれた」という dev.to のコメントは、Carter 本人の発言か確認できない — [dev.to](https://dev.to/gracegtaylor/comment/n7n3)
- Gerrit、Meta の Phabricator 後継、Google Critique の UI 設計者の記事、SemanticDiff の「なぜ作ったか」は未調査。
- Greptile の 19%→55% は自社ブログの数字で、第三者の検証はない。CodeRabbit の「20 分→30 秒」は 1 事例。
