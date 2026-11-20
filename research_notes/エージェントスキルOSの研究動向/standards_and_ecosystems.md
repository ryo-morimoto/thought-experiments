# スキルとプラグインのパッケージング・配布の標準と業界実装（2026年11月21日時点）

調査方法の注記：一次資料は、WebFetch による取得と curl で Markdown 版（`*.md`）を落として grep・sed で読んだものの2通りで読んだ。どちらで読んだかは各項目に書いた。ページの多くに日付が付いていない。その場合は「取得日 2026-11-21」とし、Claude Code の機能には文書に書かれた最低バージョン（v2.1.x）を添えた。二次報道（ニュース・ブログ）は、一次資料で確かめられなかったときに限って使い、その旨を明記した。

---

## 1. Agent Skills（SKILL.md、agentskills.io）：必須フィールド、段階的な読み込み、推奨上限、採用状況

### Takeaway
Agent Skills は Anthropic が作り、2025年12月18日に「オープン標準」として agentskills.io で公開した。中身は「`SKILL.md`（YAML frontmatter + Markdown）を持つフォルダ」という最小の形式である。必須は `name`（64字以下、小文字・数字・ハイフンのみ、親ディレクトリ名と一致）と `description`（1024字以下）の2つ。任意フィールドは `license`・`compatibility`・`metadata`・`allowed-tools` の4つで、合わせて6フィールドになる。読み込みは3段階に分かれる。起動時は名前と説明だけ（約100トークン）、起動されたら本文（5000トークン未満、500行未満を推奨）、必要になったら参照ファイル、という順である。Claude Code はこの形式を土台にしつつ独自のフィールドを多く足している。ただし claude.ai へのアップロードと Skills API は標準の6フィールド以外を受け付けず、エラーにする。

### Cited Findings
- **フォルダの構造**：`SKILL.md` が必須で、`scripts/`・`references/`・`assets/` は任意。それ以外のファイルを置いてもよい — [Agent Skills Specification](https://agentskills.io/specification)（WebFetch、日付なし、取得日 2026-11-21）
- **`name` の規則**：1〜64字。使えるのは `a-z0-9-` だけ。先頭・末尾にハイフンを置けず、`--` も禁止。**親ディレクトリ名と一致しなければならない** — [同上](https://agentskills.io/specification)
- **`description` の規則**：1〜1024字で、空にはできない。「何をするか」と「いつ使うか」の両方を書き、エージェントが場面を見分けられるキーワードを入れることを推奨している — [同上](https://agentskills.io/specification)
- **任意フィールド**：
  - `license`：短く書く。
  - `compatibility`：1〜500字。動作環境の要件を書く。仕様は「ほとんどのスキルには不要」としている。
  - `metadata`：文字列から文字列への写像。キーは衝突しにくい名前にするよう推奨。
  - `allowed-tools`：空白区切り。**実験的**で、実装によって対応がばらつく。

  — [同上](https://agentskills.io/specification)
- **段階的な読み込み（progressive disclosure）**：
  1. メタデータ（約100トークン）：起動時にすべてのスキルについて読み込む。
  2. 指示（5000トークン未満を推奨）：スキルが起動されたら `SKILL.md` 本文を全部読み込む。
  3. リソース：必要なときだけ読む。

  「メインの `SKILL.md` は500行未満に」「ファイル参照は `SKILL.md` から1階層まで」とも書かれている — [同上](https://agentskills.io/specification)
- **検証ツール**：参照実装の `skills-ref validate ./my-skill` が、frontmatter と命名規則を検査する — [同上](https://agentskills.io/specification)
- **出自と運営**：「Anthropic が開発し、オープン標準として公開した。ほかのエコシステムからの寄与を受け付ける」。議論の場は GitHub の agentskills/agentskills と Discord — [Agent Skills Overview](https://agentskills.io/)（WebFetch）
- **公開日と3段階モデルの説明**：Anthropic のエンジニアリングブログ（2025-10-16 公開）は、2025-12-18 の追記で「Agent Skills をクロスプラットフォームで持ち運べるオープン標準として公開した」と書いている。3段階の読み込みを「Agent Skills を柔軟でスケーラブルにする中心的な設計原則」と呼ぶ — [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)（WebFetch）
- **Claude Code は標準を拡張している**：「Claude Code のスキルは Agent Skills オープン標準に従い、invocation control・subagent 実行・動的コンテキスト注入などの機能を足している」。追加フィールドは次のとおり。

  | 種類 | フィールド |
  | :- | :- |
  | 呼び出し・引数 | `when_to_use`、`argument-hint`、`arguments`、`disable-model-invocation`、`user-invocable` |
  | ツール制御 | `disallowed-tools` |
  | 実行環境 | `model`、`effort`、`context: fork`、`agent`、`background`、`shell` |
  | フック・発火条件 | `hooks`、`paths` |

  Claude Code では `name` も**任意**で、省くとディレクトリ名が使われる — [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills.md)（curl で取得し grep、取得日 2026-11-21）
- **標準外のフィールドは配布経路によって失敗する**：claude.ai へのスキルのアップロード、Skills API、`package_skill.py` によるパッケージ化で使えるのは6フィールドだけである。それ以外を書くと `Unexpected key(s) in SKILL.md frontmatter: argument-hint. Allowed properties are: allowed-tools, compatibility, description, license, metadata, name` というハードエラーになる — [同上](https://code.claude.com/docs/en/skills.md)
- **Claude Code での実際の上限**：
  - スキル一覧（listing）では、`description` と `when_to_use` を合わせて1,536字で切り詰める。上限は `skillListingMaxDescChars` で変えられる。
  - 一覧全体の予算はモデルのコンテキストの1%。超えると、使われていないスキルから順に説明を落とす。予算は `skillListingBudgetFraction` で変えられる。
  - 自動圧縮（compaction）のあとは、各スキルを先頭5,000トークンまで、合計25,000トークンまで再添付する。
  - `/skill-doctor` で、スキルごとのコストと使用頻度を見られる。

  — [同上](https://code.claude.com/docs/en/skills.md)
- **Anthropic の作成ガイドの追加制約**：`name` と `description` に XML タグを入れてはいけない。`name` に予約語 `anthropic` と `claude` を入れてはいけない — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)（curl で取得し grep）
- **他ツールでの採用**：
  - agentskills.io の Client Showcase（[clients](https://agentskills.io/clients.md)）は JavaScript で描画されるため、curl では一覧を取れなかった。
  - 二次資料によると、Cursor、OpenAI Codex、Gemini CLI、VS Code、JetBrains Junie、GitHub Copilot など「16以上」（2026年3月）、あるいは「32以上」のツールが対応している。ただし探索パス（`.github/skills/`、`.agents/skills/`、`.gemini/skills/` など）については資料同士が食い違っている — [DEV: AI Agent Skills Guide 2026](https://dev.to/serenitiesai/ai-agent-skills-guide-2026-build-skills-for-16-ai-tools-1jea)、[DEV: SKILL.md goes multi-ecosystem](https://dev.to/nathanielc85523/skillmd-goes-multi-ecosystem-how-the-agent-skills-standard-jumped-from-anthropic-to-openai-and-3oeg)（検索スニペットのみ。二次資料）
- **Agent Plugins の扱い**：Agent Plugins 1.0 は、スキルが「外部の Agent Skills 仕様に従わなければならない」と定めている。仕様に合わないスキルは読み飛ばす — [Agent Plugins spec 1.0.0](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.0.0.md)（WebFetch）

### Inferences
- 移植性を最優先するなら、frontmatter は標準の6フィールドに絞るのが最も安全である。そうすれば Claude Code、claude.ai の同期、Agent Plugins 準拠クライアントのどれでも通る。Claude Code 独自のフィールドは Claude Code ではそのまま効く。しかし claude.ai へアップロードすると失敗する。
- 実際の運用で効く上限は、仕様の1024字よりも Claude Code の1,536字（`when_to_use` 込み）と一覧予算1%である。スキルの数を増やすほど、使われないスキルから説明が落ちるので、発火の精度が下がる。
- 仕様は `name` とディレクトリ名の一致を MUST にしている。Claude Code は `name` を省いても動くが、それに頼ると他クライアントで不適合になる。

### Gaps
- agentskills.io の公式なクライアント一覧を本文として取得できなかった（JavaScript で描画されるため）。各ツールの公式の探索パスも、一次資料では確かめていない（Codex、Copilot、Cursor、Gemini CLI）。
- agentskills の仕様そのものにバージョン番号や改訂日が書かれているかは確認できなかった。
- Agent Skills が AAIF（Agentic AI Foundation）などの財団に移管されたかどうかは、確認できる資料がなかった。

---

## 2. Agent Plugins 仕様（agent-plugins.org、spec 1.0.0）：何を標準化するか、誰が保守するか、どこまで採用されたか

### Takeaway
Agent Plugins は Vercel が起草した。2026年8月6日に 1.0.0 を公開した、ベンダー中立のパッケージ仕様である。1.0 が標準化するのは3つだけ。**ルートの `plugin.json`（閉じたスキーマ）、`skills/`（Agent Skills 形式）、`mcp.json`** である。コマンド、エージェント、フック、LSP、マーケットプレイス、依存関係、署名は 1.0 の対象外になっている。フックは 1.1.0 の Working Draft で追加された。運営委員会（TSC）は Amazon、Cursor、Microsoft、OpenAI、Vercel の個人で構成される。公開時の対応クライアントは ChatGPT/Codex、Cursor、GitHub Copilot、Kiro、VS Code。**Anthropic と Claude Code は、どの一次資料にも名前が出てこない。**

### Cited Findings
- **定義**：「スキルと MCP サーバーを持ち運べるプラグインにまとめる、オープンでベンダー中立な標準」。1.0.0 が現在の公開版で、1.1.0 は Working Draft — [agent-plugins.org](https://agent-plugins.org/)、[GitHub agentplugins/agent-plugins-spec README](https://github.com/agentplugins/agent-plugins-spec)（WebFetch。GitHub のスターは約1.5k）
- **`plugin.json`（1.0.0）**：
  - **置き場所**：プラグインのルートに置く。
  - **スキーマ**：閉じたスキーマで、トップレベルに書けるのは `$schema`、`name`、`version`、`description`、`author`、`homepage`、`repository`、`license`、`keywords`、`extensions` だけ。
  - **必須**：`$schema` と `name` の2つ。`$schema` は `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` 固定で、これが仕様バージョンの識別子を兼ねる。`name` は1〜64字で、`a-z0-9-.` が使える。先頭・末尾は英数字。`--` と `..` は禁止。
  - **`version`**：SemVer を推奨するが、強制はしない。
  - **エラーの扱い**：未知のトップレベルフィールドは報告して無視する。それ以外のスキーマ違反は致命的で、プラグインを拒否しなければならない。

  — [spec/1.0.0.md](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.0.0.md)（WebFetch）
- **スキル**：`skills/` の直下の子ディレクトリのうち `SKILL.md` を持つものを、1つのスキルとして扱う。再帰的には探さない — [同上](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.0.0.md)
- **`mcp.json`**：
  - **置き場所と形式**：ルートに置く。`$schema` と `mcpServers` だけを持つ。`plugin.json` へのインライン記述は禁止。
  - **サーバーの型**：`type` で `stdio`、`streamable-http`、`sse`（非推奨）のいずれかを選ぶ。
  - **プレースホルダ**：`${PLUGIN_ROOT}` と `${PLUGIN_DATA}` を展開する。`command` の中では展開しない。
  - **通信**：ループバック以外は HTTPS が必須。ヘッダーに秘密情報を入れてはいけない。

  — [同上](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.0.0.md)
- **クライアント固有の拡張**：
  - マニフェストの中では `extensions` の下に、逆ドメインの名前空間をキーにして書く。
  - ファイルは、名前空間と同じ名前のトップレベルディレクトリ（例：`com.example.client/`）に置く。
  - 自分が実装していない名前空間は、検証せずに無視する。

  — [同上](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.0.0.md)
- **1.0 の対象外**：commands、hooks、agents、rules、LSP servers は「v1 形式の外」と明記されている — [同上](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.0.0.md)
- **1.1.0（Working Draft）**：持ち運べる構成要素に **hooks** を加える。`hooks.json` をルートに置き、`$schema` は `https://agent-plugins.org/schemas/1.1.0/hooks.schema.json` — [spec/1.1.0.md](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.1.0.md)（curl で取得）
- **将来の検討事項（非規範）**：1.0 で扱わない領域として、次のものが列挙されている。
  - 権限と承認の UX
  - 出自の検証（署名、attestation）
  - 秘密情報の扱い
  - 企業向けの制御
  - 監査ログ
  - **依存関係の解決**：「現在、プラグインは他のプラグインへの依存を宣言できない」
  - テスト・検証ツール

  — [FUTURE_CONSIDERATIONS.md](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/FUTURE_CONSIDERATIONS.md)（curl で取得）
- **運営**：
  - TSC のメンバーは Clare Liguori（Amazon）、Roshan Sadanani（Cursor）、Harald Kirschner（Microsoft）、Gav Verma（OpenAI）、Jonathan Hefner（Vercel、Lead Core Maintainer）。
  - 「役職は個人が持ち、企業に席を割り当てない」「単一のベンダーが Core Maintainer の過半数を占めてはならない」。

  — [MAINTAINERS.md](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/MAINTAINERS.md)、[GOVERNANCE.md](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/GOVERNANCE.md)（curl で取得）
- **公開日と対応クライアント**：2026-08-06 に 1.0.0 を発表した。公開時の対応は ChatGPT と Codex、Cursor、GitHub Copilot、Kiro、VS Code。インストール・配布・ポリシー・UX・クライアント固有の機能は各クライアントに委ねる — [Vercel changelog: Introducing Agent Plugins 1.0.0](https://vercel.com/changelog/introducing-agent-plugins-1-0-0)（WebFetch）
- **AAIF との関係**：Agent Plugins は「AAIF のプロジェクトではなく、加入の提案もしていない」。一方、MCP は AAIF のプロジェクトである。MCP 側で進む「Skills over MCP」は Agent Plugins を補うものと位置づけられている。2026-08-06 公開、著者は Harald Kirschner — [AAIF blog: From skills and tools to portable agent plugins](https://aaif.io/blog/from-skills-and-tools-to-portable-agent-plugins)（WebFetch）
- **VS Code の形式自動判別**：VS Code は次の4形式を見分ける。

  | 形式 | 判別の目印 | ルートのプレースホルダ |
  | :- | :- | :- |
  | Agent Plugins 1.0 | ルートの `plugin.json` に正規の `$schema` がある | `${PLUGIN_ROOT}` |
  | Copilot | `plugin.json`（目印がなければこの形式とみなす） | `${PLUGIN_ROOT}` または `${CLAUDE_PLUGIN_ROOT}` |
  | Claude | `.claude-plugin/plugin.json` | `${CLAUDE_PLUGIN_ROOT}` |
  | Legacy OpenPlugin | `.plugin/plugin.json` | `${PLUGIN_ROOT}` |

  Copilot 固有の構成要素は名前空間 `com.github.copilot` の下に置く — [VS Code: Agent plugin authoring reference](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference.md)（curl で取得し grep）
- **報道どうしの食い違い**：Google の関与の度合いと、公開日（7月24日とする報道もある）が報道によって違う — [The Next Web](https://thenextweb.com/news/openai-agent-plugins-open-standard-skills-mcp)、[the-decoder](https://the-decoder.com/amazon-cursor-microsoft-openai-and-vercel-unite-on-a-shared-standard-for-ai-agent-plugins/)、[Google Developers Blog](https://developers.googleblog.com/agent-plugins-package-your-skills-tools-and-more/)（検索結果のみ。本文は未読）

### Inferences
- 「Agent Plugins の構成に従い、Claude Code で検証する」リポジトリを作るなら、**ルートの `plugin.json`（Agent Plugins）と `.claude-plugin/plugin.json`（Claude）を両方置く**構成が自然である。2つは置き場所が違うので衝突しない。`skills/<name>/SKILL.md` は両者で同じ場所なので共有できる（推論）。
- MCP の設定はファイル名と形式が違う。Agent Plugins は `mcp.json`（`type` が必須で、値は `streamable-http` など）、Claude は `.mcp.json`。プレースホルダも `${PLUGIN_ROOT}` と `${CLAUDE_PLUGIN_ROOT}` で異なる。そのため、MCP やフックを持つプラグインでは設定を二重に持つ必要がある。スキルだけのプラグインなら差はほぼ生じない（推論）。
- Agent Plugins のマニフェストは閉じたスキーマなので、Claude 固有の `userConfig` や `dependencies` はルートの `plugin.json` に書けない。書く先は `.claude-plugin/plugin.json` か、`extensions` の名前空間になる（推論）。

### Gaps
- **Claude Code が Agent Plugins 形式（ルートの `plugin.json`、`mcp.json`）を読むかどうかは確認できなかった。** Claude Code の文書（llms.txt の索引、plugins 関連の11ページを grep）に「Agent Plugins」「agent-plugins.org」は1件も出てこない。Anthropic が TSC にも対応クライアントの一覧にもいないことと合わせると、2026-11 時点では**未対応か、表明していない**と推定される。ただし、これは「資料がない」ことからの推論である。
- 1.0.0 の文書に正式な公開日が書かれていない（ニュースでは2026-08-06）。
- 適合テスト（conformance tests）や公式の validator が公開されているかは確認していない。

---

## 3. Claude Code のプラグインとマーケットプレイス

### Takeaway
Claude Code のプラグインは `.claude-plugin/plugin.json`（任意。必須フィールドは `name` だけ）と、決まった場所に置く構成要素からなる。構成要素は skills/commands/agents/hooks/.mcp.json/.lsp.json/output-styles/workflows/bin など。マーケットプレイスは `.claude-plugin/marketplace.json`（`name`・`owner`・`plugins` が必須）を持つ git リポジトリやディレクトリで、取得元（source）として relative/github/git-subdir/url/archive/npm/command が使える。

バージョン管理の主な仕組みは次のとおり。
- `version` を書くか、省いてコミット SHA で追う。
- `ref`/`sha` で固定する。
- `<plugin>--v<version>` タグに対して semver 範囲で依存を解決する。
- `renames` で名前変更を移行する。

検証は `claude plugin validate [--strict]` で行う。スキルは `plugin:skill` の名前空間に入り、インストールスコープは user/project/local の3つ。claude.ai と同期したスキルやプラグインもある。

### Cited Findings
- **マニフェスト**：
  - **ファイル**：`.claude-plugin/plugin.json`。マニフェストは任意で、なければ標準の配置から読み込む。
  - **必須フィールド**：`name` だけ。kebab-case で、空白・`@`・`:`・パス区切りは禁止。
  - **名前空間**：すべての構成要素がこの名前の下に入る（例：`deploy-tools:reviewer`）。
  - **予約名**：`claude-`、`anthropic-`、`cc-plugin-` で始まる名前はエラーになる。

  — [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)（WebFetch、取得日 2026-11-21）
- **任意のフィールド**：

  | 用途 | フィールド |
  | :- | :- |
  | 表示・メタデータ | `displayName`、`version`、`description`、`author`、`homepage`、`repository`、`license`、`keywords`、`metadata` |
  | 有効化・互換性 | `defaultEnabled`、`engines.claude-code`（semver 範囲、v2.1.323 以降） |
  | 依存・設定 | `dependencies`、`network`、`userConfig`、`channels` |
  | 構成要素のパス | `skills`、`commands`、`agents`、`hooks`、`mcpServers`、`lspServers`、`outputStyles`、`workflows`、`experimental.{themes,monitors,evals}` |

  `skills` は既定の `skills/` に**追加**される。`commands` と `agents` は既定の場所を**置き換える**。`hooks` と `mcpServers` は既定のファイルと**マージ**される — [同上](https://code.claude.com/docs/en/plugins/manifest-reference)
- **パス変数**：
  - `${CLAUDE_PLUGIN_ROOT}`：バージョンごとのキャッシュの場所。更新のたびに変わる。
  - `${CLAUDE_PLUGIN_DATA}`：`~/.claude/plugins/data/<id>/`。更新しても残る。
  - `${CLAUDE_PROJECT_DIR}`

  プラグインのルートに置いた `CLAUDE.md` はコンテキストに読み込まれない（validate が警告する） — [同上](https://code.claude.com/docs/en/plugins/manifest-reference)
- **`version` の意味**：semver かどうかは検査しない。書いた値でキャッシュが固定され、値を変えるまで利用者に更新が届かない。省くとコミットを追う。`plugin.json` とマーケットプレイスのエントリの両方に書くと `plugin.json` が優先され、validate が不一致を報告する — [Host and maintain a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace.md)（WebFetch）
- **`marketplace.json`**：
  - **必須フィールド**：`name`、`owner`、`plugins`。各エントリには `name` と `source` が要る。
  - **相対パス**：マーケットプレイスのルートから書く。`..` は不可。
  - **インストール ID**：`<entry-name>@<marketplace>`。
  - **名前の一致**：エントリ名と、マニフェストの名前（スキルの接頭辞）を一致させることを推奨。
  - **予約名**：`claude-plugins-official` などは追加時に拒否される。

  — [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)（WebFetch）
- **取得元とホスティング**：
  - **取得元の種類**：relative、`github`、`git-subdir`、`url`、`archive`（`sha256` で固定、256MiB まで）、`npm`、`command`。
  - **ホスト**：GitHub、任意の git、`marketplace.json` の URL、共有ディレクトリ。
  - **ref の指定**：`#<ref>` でブランチやタグを固定できる。
  - **リリースチャネル**：「別名のマーケットプレイスを2つ作り、それぞれ別の ref を指す」形で実現する。
  - **名前変更と削除**：`renames`（追記専用の履歴）で移行する。`forceRemoveDeletedPlugins` で削除済みのプラグインをアンインストールさせる。
  - **非推奨の状態**：存在しない。
  - **自動更新**：既定はオフ。利用者か管理者が有効にする。

  — [Host and maintain a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace.md)
- **依存関係**：
  - **書き方**：`dependencies` に `"name"`、`"name@marketplace"`、`{name, marketplace, version}` のいずれかで書く。`version` には `^2.0` や `~2.1.0` のような semver 範囲を書ける。
  - **解決**：解決先は、その範囲を満たす最大の `<plugin-name>--v<version>` git タグ。タグは `claude plugin tag --push` で作る。
  - **複数の制約**：すべての範囲を満たす最大バージョンを選ぶ。
  - **他のマーケットプレイスへの依存**：`allowCrossMarketplaceDependenciesOn` で許可した場合だけ。
  - **解決結果の確認**：`claude plugin list` に `2.1.0-8713c5b11005` のような形で出る。

  — [Plugin dependencies](https://code.claude.com/docs/en/plugins/dependencies.md)（curl で取得し grep）
- **インストールスコープ**：

  | スコープ | 記録先 |
  | :- | :- |
  | user | `~/.claude/settings.json` |
  | project | `.claude/settings.json`。コミットするが、各自が一度 install を実行する必要がある |
  | local | `.claude/settings.local.json` |

  優先順位は local > project > user — [Install and manage plugins](https://code.claude.com/docs/en/plugins/install.md)（curl で取得し grep）
- **claude.ai からの同期**：
  - **プラグイン**：claude.ai アカウントのプラグインは `<name>@synced` という ID で出てくる — [Install and manage plugins](https://code.claude.com/docs/en/plugins/install.md)
  - **スキルの保存先と頻度**：アカウントで有効にしたスキルは `~/.claude/skills/synced/` にダウンロードされる。v2.1.273 以降は、セッション中も変更を反映する。
  - **向き**：ダウンロードだけで、アップロードはしない。ローカルで編集しても上書きされる。
  - **予約名**：`synced` と `anthropic-skills` は予約されている。

  — [Extend Claude with skills](https://code.claude.com/docs/en/skills.md)
- **組織への配布**：claude.ai の Organization settings > Plugins & skills から、リポジトリを同期して配布できる。条件は2つ。
  - github.com や gitlab.com 上のリポジトリは private か internal でなければならない。
  - トップレベルに `bin/` を持つプラグインは拒否される。

  — [Host and maintain a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace.md)
- **検証**：
  - **CLI**：`claude plugin validate <dir>` で検査する。`--strict` を付けると警告も失敗扱いになる（CI 向け）。
  - **検査内容**：JSON 構文、必須フィールド、命名、`..`、未知のフィールド（警告）、各プラグインの `plugin.json`、MCP エントリ（v2.1.281 以降）。
  - **検証では見つからない問題**：取得元が存在しないなど、インストール時に初めて出るものがある。

  — [Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)、[Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)
- **プラグインに分けるべきときの公式な指針**：「スキル、サブエージェント、フック、MCP は単体でも動く。プラグインは、複数をひとまとまりで配りたいとき、チームに渡したいとき、バージョン付きで公開したいときに使う」。有効にしたプラグインは、使わないセッションでも、各スキルやエージェントの名前と説明が毎ターンのコンテキストに入る — [Plugins overview](https://code.claude.com/docs/en/plugins/overview.md)（curl で取得）
- **マーケットプレイス内でのスキル共有**：同じマーケットプレイスの中のシンボリックリンクは、キャッシュにコピーするときに実体化される。そのため「メタプラグインの `skills/` から、他のプラグインのスキルへリンクする」ことができる — [Host and maintain a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace.md)

### Inferences
- `ryo-morimoto/plugins` のように1つのリポジトリに複数のプラグインを置く場合、relative の取得元とタグ `<plugin>--v<version>` を組み合わせれば、プラグインごとに独立した版の履歴を持てる。依存の範囲解決もそのまま使える（推論）。
- `version` は書くか、完全に省くかのどちらかに統一するのがよい。書き忘れて更新が届かない事故を避けられる。CI では `claude plugin validate --strict` を回すのがよい（推論）。
- スキル名は `plugin:skill` の形で呼ばれる。したがってプラグイン名は「スキル群の分類名」として設計する必要がある。名前を後から変えると、`renames` での移行が必要になる（推論）。

### Gaps
- Claude Code 側でマーケットプレイスやプラグインに署名・出自の検証を付ける仕組みは、読んだ範囲では見つからなかった。`archive` の `sha256` 固定と git の `sha` 固定はある。
- 利用者側のロックファイル（インストールした版を固定するファイル）が Claude Code にあるかどうかは確認していない。キャッシュディレクトリ `cache/<marketplace>/<plugin>/<version>/` はある。

---

## 4. 関連する標準：MCP、AGENTS.md、OpenAI、レジストリとパッケージマネージャ

### Takeaway
MCP は「実行時のツール・データ接続」を受け持つプロトコルで、スキルとは層が違う（スキルは手順の知識）。最新版の仕様（スキーマ 2026-07-28）では、「Skills over MCP」が拡張・作業部会として載っている。スキル単体の配布には、Vercel の `npx skills` と skills.sh、`skills-lock.json` など、ロックファイルを持つコミュニティツールがある。ただし公式の標準にはなっていない。依存・署名・ロックファイルを標準化した仕様は、2026-11 時点で見当たらない（Agent Plugins も将来の検討事項に挙げているだけ）。

### Cited Findings
- **MCP の現行仕様**：スキーマは `2026-07-28`。サーバーの機能は Resources、Prompts、Tools。クライアントの機能は Elicitation。拡張として Tasks、**Skills over MCP**（「エージェントの作業手順を記した構造化された指示を、MCP を通して見つけて使う」）、MCP Apps がある。ツールは「任意のコード実行」として扱い、ツールを呼ぶ前に利用者の同意を得なければならない — [MCP Specification (latest)](https://modelcontextprotocol.io/specification/latest)（WebFetch）
- **スキルと MCP の関係（Anthropic の見解）**：スキルは MCP の代わりではない。「より複雑な作業手順をエージェントに教えることで MCP サーバーを補う」方向を今後探る、としている — [Anthropic engineering blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **MCP の運営**：MCP は AAIF がホストするプロジェクトである — [AAIF blog](https://aaif.io/blog/from-skills-and-tools-to-portable-agent-plugins)
- **スキル用のパッケージマネージャとロックファイル（コミュニティ）**：
  - Vercel の `npx skills`（vercel-labs/skills）は、GitHub から取ってきたスキルをエージェントのスキルフォルダにインストールし、`skills-lock.json` を書き出す。項目は sourceType、sourceUrl、skillPath、skillFolderHash、installedAt。
  - 2026-08-07 に skills.sh へ「skill packs」が追加されたが、こちらにはロックファイルも版の固定もない、という批判がある。
  - ロックファイルの形式は頻繁に変わる、とも指摘されている。

  — [Mintlify: vercel-labs/skills lock files](https://www.mintlify.com/vercel-labs/skills/advanced/lock-files)、[Developers Digest](https://www.developersdigest.tech/blog/vercel-skill-packs-2026)、[explainx.ai](https://explainx.ai/blog/skills-lock-json-reproducible-agent-skills-2026)（いずれも検索結果の要約で、二次資料。Vercel 公式では確かめていない）
- **標準での依存・署名の扱い**：Agent Plugins 1.0 には依存関係も署名もない。どちらも将来の検討事項にとどまる — [FUTURE_CONSIDERATIONS.md](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/FUTURE_CONSIDERATIONS.md)
- **Claude Code の独自実装**：一方、Claude Code は semver 範囲による依存と git タグでの解決を独自に実装している — [Plugin dependencies](https://code.claude.com/docs/en/plugins/dependencies.md)

### Inferences
- 層で整理すると次のようになる（推論）。
  - **手順の知識**：Agent Skills
  - **実行時のツール**：MCP
  - **パッケージ**：Agent Plugins、または Claude プラグイン
  - **カタログと配布**：各社のマーケットプレイス（標準なし）
  - **依存と版の解決**：Claude Code の独自実装か、コミュニティのロックファイル（標準なし）
- 下の層ほど標準化が進み、上の層ほど各社の独自実装になっている。

### Gaps
- **AGENTS.md**：今回は一次資料を取得していない。AAIF のブログにも言及がない。仕様の現状と、スキルとの関係は未調査。
- **OpenAI**：Codex のプラグイン文書（developers.openai.com/codex/plugins → learn.chatgpt.com/docs/plugins にリダイレクト）は、呼び出し回数の都合で未取得。Apps SDK との関係、マニフェストの場所、Codex のスキルの探索パスは未確認。
- **MCP Registry**：版の固定や署名の有無も未確認。

---

## 5. スキル設計の公式ガイド：粒度、発火のための description、重複の回避、1つにするか分けるか、プラグインへの束ね方

### Takeaway
Anthropic の公式ガイドの要点は次の4つ。
- **簡潔さ**：Claude がすでに知っていることは書かない。
- **description**：三人称で、「何をするか」と「いつ使うか」を、具体的なキーワード付きで書く。
- **分割**：本文は500行未満にし、参照は1階層まで。組み合わせて使うことの少ない内容は別ファイルに分ける。
- **評価駆動**：実際の不足を3つのシナリオで確かめてから書く。

スキルの数を増やすと、一覧の予算が圧迫されて発火が劣化する。そのため、使われないスキルを削る道具（`/skill-doctor`）が用意されている。

### Cited Findings
- **description の書き方**：
  - 「必ず三人称で書く。description はシステムプロンプトに注入されるので、視点がぶれると発見に支障が出る」。
  - 「Claude は100以上あるスキルの中から、description だけを見て選ぶ」。
  - 悪い例は「Helps with documents」のような曖昧なもの。

  — [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)（curl で取得し sed で読んだ）
- **命名**：動名詞形（`processing-pdfs`）を推奨する。名詞句や命令形も許容する。`helper`、`utils`、`documents` のような曖昧・汎用の名前は避ける。スキル集の中では命名パターンを揃える — [同上](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)
- **構造**：
  - 本文は500行未満。
  - 参照は `SKILL.md` から1階層まで（入れ子の参照では部分的にしか読まれない恐れがある）。
  - 100行を超える参照ファイルには目次を付ける。
  - 時期で変わる情報は避ける。
  - 用語を統一する。
  - MCP ツールは `ServerName:tool_name` の形で書く。

  — [同上](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)
- **評価駆動**：「先に評価を作る」。不足を見つけたら、それを試すシナリオを3つ作る — [同上](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md)
- **粒度の決め方**：代表的なタスクで実際の能力の不足を見つけてから、少しずつスキルを作る。`SKILL.md` が扱いにくくなったら分割する。互いに排他的な文脈や、組み合わせて使うことの少ない文脈は別のパスに分ける — [Anthropic engineering blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **使わないスキルのコスト**：一覧に載ったスキルは、使われなくても毎ターンのコンテキストを消費する。`/skill-doctor` で、一度も呼ばれていないスキルとコストの大きいスキルを特定して無効化する。一覧の予算を超えると、使用頻度の低いスキルから説明が落ちる — [Extend Claude with skills](https://code.claude.com/docs/en/skills.md)
- **どこまで分けるか**：
  - 「説明だけで発火してほしくない」手動専用の作業には `disable-model-invocation: true` を付ける。
  - 「利用者が直接呼ばない背景知識」には `user-invocable: false` を付ける。
  - 優先度の低いスキルは `skillOverrides` で `"name-only"` にする。

  — [同上](https://code.claude.com/docs/en/skills.md)
- **スキルの評価**：Claude Code は、プラグイン用の評価機能 `claude plugin eval`（no-plugin のベースラインとの比較、CI でのゲート）を用意している。スキルの評価形式は agentskills.io の「Evaluating skill output quality」を参照するよう案内している — [Claude Code docs index](https://code.claude.com/docs/llms.txt)、[Extend Claude with skills](https://code.claude.com/docs/en/skills.md)

### Inferences
- **スキルの重なり**：明示的な「重複を避けよ」という一文は、読んだ範囲では見つからなかった。ただし「description だけで100以上から選ぶ」「一覧の予算は1%」という仕組みからは、description のキーワードが重なるスキルは互いに誤発火を起こす、と推論できる。境界は「いつ使うか」と「いつ使わないか（別スキルを使う）」で明示するのが合理的である。
- **プラグインへの束ね方**：公式の指針は「一緒に配り、一緒に版を上げたい単位」でまとめることである。有効化はプラグイン単位なので、使う場面が違うスキル群は別プラグインに分けるほうがよい。そうすれば利用者は使わない群を無効にでき、一覧のコストを抑えられる（推論）。

### Gaps
- 「1つの大きなスキルと、多数の小さなスキルのどちらがよいか」を定量的に比べた公式データは見つからなかった。
- スキル同士の重なりを検出する公式ツールは確認できなかった。`/skill-doctor` が見るのはコストと使用頻度で、重なりではない。
