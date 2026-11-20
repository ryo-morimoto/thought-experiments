# エージェントのスキル・プラグイン・MCP サーバーのセキュリティ、ガバナンス、評価（2026年11月21日時点）

調査日: 2026-11-21。読み方の表記:
- 【全文】本文を読んだ
- 【AI要約】alphaXiv が生成した論文レポートで読んだ（原文ではない。数値は原文で確かめていない）
- 【抄録】抄録・序論の冒頭だけ読んだ
- 【一次Web】ベンダーの公式ページを WebFetch で読んだ
- 【二次】検索結果の要約か報道記事だけで、一次資料は開いていない
- 【題名のみ】alphaXiv 検索結果の題名と抄録の冒頭だけを見た

---

## 問い1: 脅威とインシデント（スキル内容によるプロンプトインジェクション、悪意あるスクリプト、MCP のツールポイズニングとラグプル、マーケットプレイスのサプライチェーン攻撃、データ持ち出し、過剰な権限）

### 要点
- 公開スキルの約1/4〜1/3に、危険になりうるパターンがある。高い深刻度か確認済みのマルウェアは数%。
- 開かれたマーケットプレイス（ClawHub）では、2026年2月以降、組織的なマルウェア配布キャンペーンが実際に起きた。
- MCP では、2025年4月にツールポイズニングとラグプルが実証された。同年9月には、正規パッケージを装った悪意ある npm パッケージ（postmark-mcp）が実際に出回った。
- 2026年後半の研究では、単体では無害なスキル同士の組み合わせや、メタデータだけを汚染する攻撃のように、スキャナが単体検査で見逃す攻撃が主題になっている。

### 出典つきの事実

**スキルの脆弱性の大規模測定**
- Liu ら「Agent Skills in the Wild」(arXiv 2601.10338, 2026年1月)【AI要約】
  - 対象: skills.rest と skillsmp.com から2025年12月に42,447件を収集し、重複除去などで31,132件にした。
  - 結果: 26.1%（8,126件）に危険になりうるパターンが1つ以上あった。不確実性を考えた範囲は23〜30%。
  - 深刻度の内訳: 高5.2%、中8.1%、低12.8%。
  - カテゴリ別: データ持ち出し13.3%、権限昇格11.8%、サプライチェーン7.4%、プロンプトインジェクション0.7%（検出が難しいためと著者は推測）。
  - スクリプトを同梱するスキルは、そうでないスキルより脆弱性のオッズが2.12倍。500行を超えるスキルは2.14倍。
  - 直近90日に保守されているかどうかは、脆弱性と関係しなかった（p=0.47）。
  - 検出器 SkillScan の性能: 精度86.7%、再現率82.5%（人手で付けた200件の正解に対して）。
  - 責任ある開示により、100件以上のスキルが削除された。
  - [arXiv 2601.10338](https://arxiv.org/abs/2601.10338)
- Snyk「ToxicSkills」(2026年2月)【二次】
  - 対象: 2026年2月5日時点の ClawHub と skills.sh の3,984件。
  - 結果: 36.82%に欠陥が1つ以上、13.4%が critical、76件で悪意あるペイロードを確認。
  - Snyk の一次ブログは開いていない。数値は検索要約と CSA の文書による。
  - [Snyk blog](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)、[CSA research note (2026-05)](https://labs.cloudsecurityalliance.org/research/csa-research-note-skill-md-agent-context-poisoning-20260506)
- 同じ年の Liu らの USENIX Security 2026 論文「"Do not mention this to the user": Detecting and understanding malicious agent skills in the wild」は、悪意あるスキルの検出を扱う。本文は未読で、Skill Constellations の参考文献として題名を確認しただけ。[USENIX Sec '26](https://www.usenix.org/conference/usenixsecurity26/presentation/liu-yi)

**マーケットプレイスでの実際の事件（OpenClaw / ClawHub）**【二次】
- Koi Security による2026年2月の監査:
  - ClawHub の2,857件のうち341件が悪意あるスキルだった。
  - そのうち335件は「ClawHavoc」と呼ばれる単一の組織的キャンペーンによるもの。偽の前提条件（prerequisites）を装って、macOS 用の情報窃取マルウェア Atomic Stealer (AMOS) を入れさせる手口。
  - 2週間後の追跡調査では、掲載数が10,700件超に増え、悪意あるスキルは824件に倍増した。
- Trend Micro は、39の攻撃者が1,100件超を投稿したと報告している。
- Unit 42 は、ClawHub が審査を導入した後も、ブロックされていない悪意あるスキルを5件見つけた。
- ClawHub は VirusTotal と ClawScan を組み込んだ。
- 1,184件という数字も出回っているが、出典の間で計上の仕方が合っていない。
- 出典: [The Hacker News](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)、[Unit 42](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain/)、[CSA note 2026-07](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/07/CSA_research_note_openclaw_clawhub_supply_chain_risk_20260707-csa-styled.pdf)

**MCP のツールポイズニング、ラグプル、シャドウイング**
- Invariant Labs (2025-04-01)【一次Web】
  - ツールポイズニング: ツールの description に、ユーザーには見えずモデルには見える指示を埋め込む攻撃。間接プロンプトインジェクションの一種と位置づけている。
  - 実証: Cursor で、偽の `add` ツールが `~/.cursor/mcp.json` と `~/.ssh/id_rsa` を引数の `sidenote` に入れて送らせた。確認ダイアログには入力の全文が出なかった。
  - ラグプル: 承認された後でツールの説明を書き換える攻撃。
  - クロスサーバーのシャドウイング: 悪意あるサーバーが、信頼された別のツール（`send_email`）の送信先を書き換える攻撃。
  - 推奨策: ツール説明を UI で全文表示する、サーバーとツールのバージョンをハッシュで固定する、サーバー間のデータの流れを制御する。
  - [Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- postmark-mcp (2025年9月, Koi Security の報告)【二次】
  - 正規の Postmark MCP サーバーのコードを写し、v1.0.16 で全メールを攻撃者へ BCC する1行を加えた npm パッケージ。
  - それ以前の15バージョンは無害だった。信頼を得てから悪意あるコードを入れる、ラグプル型の手口。
  - ダウンロード数は1週間で約1,500件。総数を1,643件超とする報道もある。
  - Postmark 社は関与を否定した。
  - [The Hacker News](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)、[The Register](https://www.theregister.com/2025/09/29/postmark_mcp_server_code_hijacked/)

**MCP の公式仕様が挙げる攻撃**【一次Web】
- 列挙されている攻撃: confused deputy、token passthrough、SSRF、セッションハイジャック、ローカル MCP サーバーの侵害（悪意ある起動コマンドの例: `npx malicious-package && curl ... ~/.ssh/id_rsa`）、OAuth の認可 URL を使った XSS や RCE、過大なスコープ。
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)（取得時の本文は 2025-11-25 版の仕様を参照していた）

**2026年後半の攻撃研究の流れ**【題名のみ】数値は未確認
- 組み合わせ攻撃
  - 「Benign in Isolation, Harmful in Composition」2606.15242
  - CoSA 2610.35082
  - Skill Cascading 2609.30383
  - Runaway Reaction 2610.05943
  - capability-flow graph による検出 2610.32155
- スキャナ回避
  - ColluSkill 2608.09732: スキル間の分担で回避する
  - 「Seeing Is Not Screening」2606.18198: 画像などマルチモーダルに隠した指示
- メタデータだけの汚染: MetaCascade 2610.14836
- 手順の汚染: StealthyPoison 2611.12155
- 動的に悪性化するスキル: Dynamic Malicious Skills 2606.16287
- 監督を外させる指示: 「When Skills Tell Agents Not to Ask」2610.37734。ユーザーに確認しないよう指示する行の大規模調査。
- 衝突: 「One Skill Takes Over」2610.25064。同じ用途のスキルが同時に有効になったときの乗っ取り。
- [検索の起点](https://www.alphaxiv.org/abs/2606.15242)

**過剰な権限と認証**
- Hasan ら 2506.13538【AI要約】
  - mcp-scan が見逃した例として、`apple-notes-mcp` がフルディスクアクセスを要求すること、`godot-mcp` が危険な操作を既定で自動承認することを挙げている。
  - [arXiv 2506.13538](https://arxiv.org/abs/2506.13538)
- 以下は【題名のみ】
  - 「Auditing MCP Servers for Over-Privileged Tool Capabilities」2603.21641
  - 「My Credentials, Please: Filesystem Capability Laundering」2610.22301
  - 「A First Measurement Study on Authentication Security in Real-World Remote MCP Servers」2605.22333
  - 「When Neither Side Confirms: Destructive Tool Approval」2611.02527
  - [arXiv 2603.21641](https://arxiv.org/abs/2603.21641)

### 推論
- 割合は分母、収集日、「脆弱」の定義によって数倍変わる（5.2%〜36.82%）。公開リポジトリが「何%が危険か」を示すなら、定義（パターンがあるだけか、悪意を確認したか）と分母を必ず添える必要がある。
- スクリプトの同梱と skill の大きさは、脆弱性と一貫して関係していた。審査の負荷を配分するとき、スクリプトがあるか・何行あるかで振り分けるのは理にかなう。
- ClawHavoc も postmark-mcp も、信頼させてから悪性化するか、偽の前提条件でインストールさせる手口だった。公開時に1回審査するだけでは足りず、更新ごとに差分を見直す必要がある。

### 未解決
- Snyk ToxicSkills の一次レポートを直接読んでいないため、数値は二次情報である。
- ClawHub の悪意あるスキルの総数（824件と1,184件）は、出典の間で整合していない。
- 2026年後半の攻撃論文（組み合わせ、メタデータ汚染など）は題名と抄録冒頭しか見ておらず、成功率は未確認。
- 公式の Anthropic マーケットプレイス（claude-plugins-official）で悪性のプラグインが見つかった事件は、見つからなかった。

---

## 問い2: 緩和策（権限モデル、サンドボックス、署名と来歴、許可リスト、マーケットプレイスの審査）。何が標準で、何がベンダー固有か

### 要点
- 標準として決まっているのは、ほぼ MCP 仕様の部分だけ。具体的には、OAuth まわりの MUST と SHOULD、ローカルサーバーの起動前に同意を取ること、サンドボックスを推奨することである。
- スキルのパッケージ署名、来歴、バージョン参照は、標準化されていない。
- 実際に効いている制御はベンダー固有である。Claude Code の場合は、OS レベルのサンドボックス、管理設定による marketplace の許可リストと拒否リスト、フックの制限がそれにあたる。
- 公式 MCP Registry の掲載の方針は意図的に緩く、脆弱なサーバーや重複したサーバーを削除しない。

### 出典つきの事実

**MCP 仕様（標準）**【一次Web】
- MCP サーバーは、自分宛てに発行されたもの以外のトークンを受け付けてはならない（MUST NOT）。token passthrough の禁止。
- プロキシ型のサーバーは、クライアントごとに同意を取らなければならない（MUST）。redirect_uri は完全一致で検証し、state は1回限りにする。
- ワンクリックでローカルサーバーを設定するクライアントは、次のことをしなければならない（MUST）。
  - 実行するコマンドを省略せずに表示する。
  - 明示的な承認を得る。
- 同じ場面で、次のことをすべき（SHOULD）とされている。
  - 危険なパターン（sudo、rm -rf、ネットワーク）を強調表示する。
  - サンドボックスで最小権限で動かす。
- スコープは最小から始め、必要になった時点で段階的に昇格する。`*` のような包括的なスコープはよくある誤りとされている。
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)

**MCP Registry（公式、プレビュー版）**【二次】
- 名前空間の所有権を、GitHub、DNS、HTTP のいずれかで検証する。
- 削除するのは、違法なもの、マルウェア、スパム、完全に壊れたものだけ。低品質、脆弱、重複しているだけでは削除しない。
- 深い審査は、上流のパッケージレジストリ（npm、PyPI）とサブレジストリに任せている。
- [MCP Registry moderation policy](https://modelcontextprotocol.io/registry/moderation-policy)、[Registry about](https://modelcontextprotocol.io/registry/about)

**Claude Code（ベンダー固有）**【一次Web】
- サンドボックス (2025-10-20)
  - Linux では bubblewrap、macOS では seatbelt で、ファイルシステムとネットワークを隔離する。子プロセスにも及ぶ。
  - ネットワークは外部のプロキシを経由し、新しいドメインはユーザーに確認する。
  - 社内での利用では、許可を求めるプロンプトが84%減った。
  - 脅威モデルはプロンプトインジェクションで、「成功したインジェクションも隔離する」ことを目標にしている。
  - [Anthropic Engineering](https://www.anthropic.com/engineering/claude-code-sandboxing)
- 組織での管理設定
  - `strictKnownMarketplaces`（marketplace の取得元の許可リスト。`[]` にすると公式も含めて全部を遮断する）
  - `blockedMarketplaces`
  - `enabledPlugins`（強制的に有効にする、または禁止する）
  - `disableSideloadFlags`（`--plugin-dir` などを拒否する）
  - `allowManagedHooksOnly`
  - `strictPluginOnlyCustomization`（ユーザーやプロジェクト由来の skills、agents、hooks、mcp を遮断する）
  - `allowedMcpServers`
  - `pluginTrustMessage`
  - marketplace ごとの `autoUpdate` と `DISABLE_AUTOUPDATER`
  - 監査用の OpenTelemetry イベント `plugin_installed` と `plugin_loaded`
  - 許可リストは marketplace の取得元を照合する。marketplace の中の個々の項目までは制限しない。
  - 許可リストは素の SKILL.md（manifest のないもの）には適用されない。
  - [Manage plugins for your organization](https://code.claude.com/docs/en/plugins/org)
- marketplace.json
  - git 系の取得元は `ref` か `sha` で固定できる。
  - `claude plugin validate` が検査するのは、構文と必須フィールドだけ。
  - 公式名 `claude-plugins-official` などは予約されている。
  - 公開先として「Anthropic のディレクトリへの提出」という経路がある。
  - [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
- Agent Skills の公式ドキュメント
  - 「信頼できる出典（自作か Anthropic 製）のスキルだけを使う」よう勧めている。
  - 同梱ファイル（スクリプトや画像を含む）を全部監査するよう勧めている。
  - 外部 URL を取得するスキルには特にリスクがあるとしている。依存先が後から変わる可能性があるため。
  - 実行環境の違い: Claude API ではネットワークなしのサンドボックスで動く。Claude Code では、ユーザーのマシン上の他のプログラムと同じネットワーク権限で動く。
  - Enterprise では、claude.ai と Cowork にアップロードされたスキルの内容をスキャンする機能がある。Skills API 経由のスキルは対象外。
  - [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

**第三者のスキャナとマーケットプレイスの対策**【二次】
- ClawHub: VirusTotal と ClawScan を組み込んだ。Koi は Clawdex を出したが、全部は捕まえられないと自分で認めている。
- Tessl: Snyk と提携し、全公開スキルに Snyk のセキュリティスコアを表示する（2026年3月）。
- [The Hacker News](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)、[Snyk × Tessl](https://snyk.io/blog/snyk-tessl-partnership)

**スキャナの信頼性**【抄録】
- Chen ら「Rethinking MCP Security」(2607.11086)
  - 64,611件の固有 MCP サーバーのうち、37,288件を動的に解析できた。
  - 既存のスキャナは96.89%を「危険」と判定した。しかし手作業で確かめると、真陽性はサンプルの50%未満だった。スキャナ同士の判定も一致しなかった。
  - [arXiv 2607.11086](https://arxiv.org/abs/2607.11086)
- Hasan ら【AI要約】
  - 汎用の SAST（SonarQube）が見つけた脆弱性は、7.2%のリポジトリにとどまった（PyPI 46%、npm 40% と比べて少ない）。著者はこれを、MCP に固有の問題を検出できていないためと解釈している。
  - mcp-scan は説明文だけを見るので、過剰な権限を見逃す。
  - [arXiv 2506.13538](https://arxiv.org/abs/2506.13538)
- 「SkillsMetric: Mapping the Detection Boundary of Static Analysis for Malicious Agent Skills」(2608.08468) や MaliciousSkillBench (2608.19901) は、静的解析の限界を測るベンチマーク【題名のみ】。

**配布の形（来歴）**【全文】
- Seddik「Skill Constellations」(2610.11169)
  - データ: GitSkills の git 履歴を使い、2,193,119件のスキル採用の事例を分析した。
  - スキルの配布はコピーで行われており、レジストリ、バージョン、来歴がない。
  - ソースで行われた修正がコピー先に届く割合は20.9%。コード一般のファイルコピーでは、上流のセキュリティ修正が47〜84%届く。
  - 共有されているスキルの集まりのうち、全コピーが同じ変更をした例は11.1%だけ。
  - 監査の効果: コピーの元になりやすいリポジトリを予測するモデルで上位100リポジトリを監査すると、その後の高リスクな採用の14.9%を防げた。スター数の上位100では0.5%だった。
  - 拡散の速さ: 7日目までに最終的な採用者の7.7%、56日目までに半数。
  - エージェントをまたぐコピーが約1/3ある。
  - 結論として、コピーではなく、バージョンを付けた参照で配布すべきだと提言している。
  - [arXiv 2610.11169](https://arxiv.org/abs/2610.11169)

### 推論
- 標準として決まっているのは、通信と認可の層（MCP の OAuth 部分）だけである。「スキルの中身を誰がどう保証するか」（署名、来歴、審査）には標準がない。そのため、公開リポジトリは自分でポリシーを決める必要がある。
- スキャナには誤検知が多く（真陽性が50%未満）、回避攻撃もある。自動スキャンは、人のレビューに回す優先度を決めるための前段として使うのが妥当で、単独の公開判定には向かない。
- Skill Constellations の結果から、公開側が持てる効果の大きい手段は次の3つと言える。
  - 利用者がバージョン参照（git の sha 固定など）で取得できるようにする。
  - 修正を伝える経路（更新の通知）を用意する。
  - 拡散が始まる最初の数週間に審査する。

### 未解決
- Anthropic の公式プラグインディレクトリの審査基準（何をどう審査するか）は、一次資料で確かめていない。
- スキル用の署名の仕組み（Sigstore や npm provenance をスキルに使うもの）が標準化されたり、広く採用されたりしているという資料は見つからなかった。
- OpenAI（Codex のスキルや Apps SDK）と GitHub（Copilot）の権限モデルは、今回は一次資料を開いていない。

---

## 問い3: 評価（スキルが行動を改善するか。ありなしのアブレーション、発火精度、コストとトークン増）

### 要点
- 厳密な評価の基本形は、同じタスク、同じモデル、同じハーネスで、スキルあり・なしを対にして比べることである。
- 人が作ったスキルは平均で+16.6ポイント（pp）の改善を示した。ただし13/87のタスクでは悪化した。モデル自身に書かせたスキルはむしろ悪化させた。
- 短いスキルほど効いた。網羅的に長いスキルはほぼ無効だった（+0.7pp）。
- AGENTS.md のような文脈ファイルは、成功率をほとんど変えず、コストを約20%増やした。
- 害の主な原因は、無関係なスキルではない。「関係はあるが手順が誤っている」スキル、または過剰な検証手順を課すスキルである。

### 出典つきの事実

**SkillsBench (arXiv 2602.12670, 2026-02-13)**【AI要約。読んだのは改訂版と思われる】
- 規模: 87タスク、8領域、18のモデルとハーネスの組み合わせ。3試行、temperature 0。
- 全体: スキルなし33.9% → 人が作ったスキルあり50.5%（+16.6pp、正規化ゲイン25.5%）。組み合わせごとの幅は+4.1〜+25.7pp。
- 自己生成スキル: モデルが skill-creator で自分用のスキルを書いてから解く条件では、3つの組み合わせで-8.1〜-11.5pp。
- 悪化したタスク: 13/87。原因は、重いパイプラインを押し付ける、より強い既定の戦略を押しのける、デバッグできない枠組みに縛る、の3つ。
- スキルの数: 1個で+18.0pp、2〜3個で+19.0pp、4個以上で+10.1pp。
- スキルの長さ: Compact +19.0、Standard +21.5、Detailed +14.5、Comprehensive +0.7pp。
- 領域別: 自然科学+28.8pp、ソフトウェア工学+11.6pp。
- スキルが呼び出される率は高かった。著者は、ボトルネックは発見ではなく、読んだ後に使いこなすことにあるとしている。
- タスクの品質管理: スキルに解答が漏れていないかの検査と、人による30分のレビューを行った。
- [arXiv 2602.12670](https://arxiv.org/abs/2602.12670)

**Gloaguen ら「Evaluating AGENTS.md」(arXiv 2602.11988, 2026-02-12, ETH Zürich と LogicStar.ai)**【AI要約】
- 設定: 4エージェント、SWE-bench Lite の300件と、新しく作った CTXBENCH の138件（12リポジトリ）。
- LLM が生成した文脈ファイル: 成功率は-0.5%（SWE-bench）と-2%（CTXBENCH）で、有意ではない。コストは20%超増えた（p<0.001）。ステップ数は+2.45〜3.92。
- 開発者が書いた文脈ファイル: 成功率+2.4%で、有意ではない。コストは最大+19%。
- リポジトリ概要の部分は、関係するファイルにたどり着くまでのステップを減らさなかった。
- エージェントは記載された指示に従い、テストや探索を増やした。推論トークンは10〜22%増えた。
- 既存のドキュメントを取り除くと、LLM 生成ファイルは+2.7%改善した。つまり既存のドキュメントと重複しているから効かない、という解釈。
- [arXiv 2602.11988](https://arxiv.org/abs/2602.11988)

**Dong ら「Agent Skills Can Be Harmful」(arXiv 2608.11888, 2026年8月, Microsoft Research ほか)**【AI要約】
- 方法: SkillsBench と SWE-Skills-Bench に、smithery.ai と skillsmp.com から意味の近い公開スキルを足した。これで、比較できる対の数を826から20,664に増やした。
- 対象: スキルによって起きたと確認できた失敗307件（機能の失敗125件、効率の悪化182件）。モデルは Claude Opus 4.6、ハーネスは OpenCode。
- 機能の失敗の内訳:
  - 適用対象の取り違え: 1.6%
  - タスクの実装の誤り: 68.8%（誤った方法や値で埋める36.8%、必要な要素の欠落28.8%）
  - 成果物の置き場所の誤り: 19.2%
  - 環境の不一致: 10.4%
- 効率の悪化の内訳:
  - 過剰な手順: 62.6%（うち過剰な検証36.8%）
  - 文脈の肥大: 25.3%（ほぼすべてがスキル本文によるもの）
  - 依存関係の解決: 12.1%
- 自動で原因を判定するツール SkillTriage の正解率: 機能の失敗で大分類93.6%、効率の悪化で79.7%。
- [arXiv 2608.11888](https://arxiv.org/abs/2608.11888)

**Anthropic の skill-creator の評価手順**【一次Web、GitHub の SKILL.md】
- 出力の評価
  - 現実的なテストプロンプトを2〜3個用意する。
  - 各ケースを「スキルあり」と「ベースライン（新しいスキルならスキルなし、既存のスキルなら旧版）」で同時に走らせる。
  - 検証できる assertion で採点し、合格率、時間、トークンを平均±標準偏差と差分で出す。
  - どちらの条件でも合格する、差の出ない assertion と、ばらつきの大きい eval を洗い出す。
- 発火の最適化
  - 発火すべきクエリと発火すべきでないクエリを、8〜10件ずつ、計20件作る。発火すべきでない側には、キーワードが重なるのに別のツールを使うべき「惜しい」例を含める。
  - 60%を学習用、40%を検証用に分ける。
  - 各クエリを3回走らせる。
  - 最大5回改良し、検証用データの成績で採用する説明文を選ぶ。
- [anthropics/skills skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- 公式ドキュメントでの文脈コスト: metadata は1スキル約100トークンで常に読み込まれる。SKILL.md 本文は5kトークン未満を目安とし、発火したときに読み込まれる。同梱リソースは読まれるまでコストがかからない。[Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

**MCP のベンチマーク**（スキルではなくツール連携の能力を測るもの）
- MCP-Universe (Salesforce, 2508.14704)【抄録】: 6領域、11の実 MCP サーバー。最高の GPT-5 でも43.72%。[arXiv](https://arxiv.org/abs/2508.14704)
- MCPMark (2509.24002)【抄録】: 127タスク。最高の gpt-5-medium で pass@1 52.56%、pass^4 約33.86%。平均16.2ターン、17.4回のツール呼び出し。[arXiv](https://arxiv.org/abs/2509.24002)
- 以下は【題名のみ】
  - MCP-Bench (2508.20453)
  - MCP-Atlas (2602.00933)
  - Alibaba「Evaluation Report on MCP Servers」(2504.11094)
  - [arXiv 2508.20453](https://arxiv.org/abs/2508.20453)

**その他の評価研究**【題名のみ】
- SkillBuffBench (2611.22017): ハーネス、モデル、スキルへのアクセス方式、記憶をまたいで、スキルの寄与を測る。
- 「Skill Roulette」(2611.23266): エージェントごとのスキル呼び出し率を測る。
- 「An Empirical Study of Agent Skills' Downstream Utility」(2610.08875)
- 「When Instruction Files Go Stale」(2611.09802): 指示ファイルが古くなることによるコスト。
- 「Do They Do as They Are Told?」(2611.13709): 文脈ファイルの指示がどれだけ守られるか。
- [arXiv 2611.22017](https://arxiv.org/abs/2611.22017)

### 推論
- 公開リポジトリが各スキルに付ける証拠として最低限必要なのは、次の2つである。
  - ありなしの対比較: 合格率の差と、トークン・時間の増分。
  - 発火精度: 発火すべき場面と、すべきでない「惜しい」場面の両方で測る。
- SkillsBench と Dong らの結果から、「悪化するタスク」と「コストの増加」も報告すべき項目である。平均の改善だけを示すのは誤解を招く。
- 長いほど効かず、自己生成は悪化させ、検証手順は過剰になりやすい。このため、短く適用範囲を明記したスキルを推奨する根拠になる。
- AGENTS.md の結果は、スキル本文にも当てはまる可能性が高い。既存のドキュメントと重複する概要は、コストを増やすだけになりうる。これは推論であり、直接検証した研究ではない。

### 未解決
- SkillsBench の v1（2026年2月）と、ここで読んだ版の数値の違い。読んだ要約は GPT-5.5 や Opus 4.7 に言及しているので、改訂版と思われる。v1 の数値（記憶では86タスク、7構成、+16.2pp）は今回確かめていない。
- 発火精度（呼び出し率、誤った発火の率）を大規模に測った研究は、題名を見つけた段階で、数値は未取得。
- スキルの安全性評価（SkillSafetyBench 2605.12015、OpenSkillRisk 2607.20121、MalSkillBench 2606.07131）の数値は未取得。

---

## 問い4: 実際のエコシステムの測定研究（MCP サーバー、GPT Store / GPTs、ChatGPT プラグイン、スキルのマーケットプレイス）。規模、品質、重複、保守、ライセンス

### 要点
- どのエコシステムでも、見かけの規模は重複で膨らんでいる。スキルでは GitHub 上の SKILL.md の半分が逐語コピーで、MCP では同じテンプレートが537回使い回されていた。
- 保守と修正の伝播は弱い。修正がコピー先に届くのは20.9%で、MCP サーバーの78.6%はデプロイ用の成果物を持たない。
- GPTs ではセキュリティ対策の欠如が95%超にのぼる。ただしこれは主に、プロンプトの漏洩やジェイルブレイクへの耐性を測ったもの。
- スター数は質やリスクの指標として当てにならない。

### 出典つきの事実

**スキル**
- Skill Constellations (2610.11169)【全文】
  - 引用元の GitSkills (Destefanis ら, MSR 2027 採択予定, arXiv 2608.10906) によると、259,596リポジトリに1,612,846の異なるスキルがあり、SKILL.md の半分は他のファイルの逐語コピーだった。
  - 64.2%のリポジトリは、他のどのリポジトリともスキルを共有していない。
  - スキルの広がり方: 一括コピー（bulk）が58.6%、バンドル単位のコピーが33.3%、個別の採用が8.1%。
  - 上位1%のリポジトリが、コピー元になった件数の94.7%を占める。
  - スター数と、コピー元になった数の相関は Kendall τ = -0.10 で、ほぼ無関係。
  - Gao ら (2607.00911) を引用し、レジストリから再利用されたスキルの53%は一度も変更されないとしている。
  - [arXiv 2610.11169](https://arxiv.org/abs/2610.11169)
- Liu ら (2601.10338)【AI要約】
  - 2025年12月時点で、2つのマーケットプレイスから42,447件を集め、31,132件が固有だった。
  - スター100未満のリポジトリのスキルは46.1%が脆弱で、100以上では35.2%だった。
  - [arXiv 2601.10338](https://arxiv.org/abs/2601.10338)
- 以下は【題名のみ】
  - 「What Keeps Agent Skills from Being Reusable? Evidence from 138K SKILL.md Files」(2608.08453)
  - 「How Agent Skills Evolve」(2611.04456)
  - 「From registry to repository」(Gao ら 2607.00911)
  - [arXiv 2608.08453](https://arxiv.org/abs/2608.08453)

**MCP サーバー**
- Hasan ら (2506.13538)【AI要約】
  - 星10以上の583サーバーが対象。
  - SonarQube の結果:
    - 脆弱性が1つ以上: 7.2%（277件、42サーバー、13の CWE）
    - 最も多いのは認証情報の露出: 3.6%
    - 公式サーバーでは0件
  - mcp-scan の結果: 動的に解析した73サーバーのうち5.5%で、ツールポイズニングの可能性があった。
  - critical 以上のコードスメル: 66%
  - critical 以上のバグ: 14.4%
  - 健全性の指標は14項目中9項目で、一般の OSS 以上だった。
  - [arXiv 2506.13538](https://arxiv.org/abs/2506.13538)
- Chen ら「MCPZoo」(2607.11086)【抄録】
  - 64,611の固有サーバー（総数113,927）。
  - 規模は重複で膨らんでいて、最も使い回されたテンプレートは537回。
  - 78.6%は Dockerfile のようなデプロイ用の成果物を持たない。
  - Dockerfile、README、設定がすべて揃ったプロジェクトでも、実際に動いたのは19.6%。
  - [arXiv 2607.11086](https://arxiv.org/abs/2607.11086)
- 時間による変化【題名のみ】
  - 「Same Name, Different Server: Silent Drift」(2609.14119)
  - 「Registry Descriptions Go Stale Unevenly: An 89-Day Measurement」(2608.00997)
  - どちらも、レジストリ上の記述が時間とともに静かに変わる問題を扱う。
  - [arXiv 2609.14119](https://arxiv.org/abs/2609.14119)
- 「Exposed by Design」(2608.00150)【題名のみ】: インターネットから到達できる MCP サーバーのインスタンスが21,000超あるとしている。[arXiv](https://arxiv.org/abs/2608.00150)

**GPTs と ChatGPT プラグイン**
- Ogundoyin ら (2505.08148)【抄録】
  - 14,904件のカスタム GPT について、7つの脅威への耐性を調べた。
  - 95%超で対策が不十分だった。
  - 脅威別: ロールプレイ型攻撃に弱いものが96.51%、システムプロンプトの漏洩が92.20%、フィッシング文の生成が91.22%。
  - 基盤モデルの弱点を継承するか、増幅している。
  - [arXiv 2505.08148](https://arxiv.org/abs/2505.08148)
- 以下は【題名のみ】数値は未取得
  - Iqbal ら「LLM Platform Security: ... ChatGPT Plugins」(2309.10254)
  - 「Exploring ChatGPT App Ecosystem」(2408.14357)
  - 「GPT Store Mining and Analysis」(2405.10210)
  - GPTZoo (2405.15630)
  - 「When GPT Spills the Tea」(2506.00197): 知識ファイルの漏洩
  - 「Confused ChatGPT: Cross-App Context Poisoning」(2606.00485): 2025年10月に始まった ChatGPT Apps が対象
  - [arXiv 2309.10254](https://arxiv.org/abs/2309.10254)

### 推論
- スキルのエコシステムは、ブラウザ拡張や npm の初期と同じ道をたどっている。爆発的に増え、コピーで重複し、審査は事後になっている。
- ただし、配布にレジストリがない（GitHub でのコピーが主流である）点が、npm より悪い。
- 公開リポジトリが示すべき指標は次のものと考えられる。スター数は使えない。
  - 来歴（どこから派生したか）
  - バージョン（固定できる参照）
  - 最終の検証日
  - 実際に動くか（実行できるか）
- ライセンスについては、今回見た研究に直接の数値がない。GitSkills の逐語コピーの多さから、帰属表示とライセンス表記が失われている可能性は高い。これは推論である（Jahanshahi らの論文 2606.23495 は、コピーによる再利用とライセンス遵守を扱っているが、未読）。

### 未解決
- スキルや MCP サーバーのライセンスの分布を定量化した研究は、見つけられなかった。
- Claude の公式プラグインディレクトリや、ClawHub 以外のスキル市場（skills.sh、Tessl、smithery）の規模と品質を比べた研究は未確認。
- GPT Store の規模（掲載数）や、重複率、放棄率の数値は、今回の資料からは取れていない。
