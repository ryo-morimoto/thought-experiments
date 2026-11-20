# エージェントを OS として扱う研究と実装（Agent OS / LLM OS）

調査日: 2026-11-21。原典（arXiv PDF 本文、公式ドキュメント、GitHub README）を優先した。要旨やアブストラクトしか読んでいないものには「（要旨のみ）」と書いた。出典が述べていることは「Cited Findings」に、私の推論は「Inferences」に分けた。

---

## 問1: 主な「Agent OS」系のシステム・論文と、それぞれが何をカーネル・syscall・管理資源とみなしているか

### Takeaway
「OS メタファー」の使い方は大きく3系統に分かれる。(a) OS for Agents（OS4A）: エージェントの下に新しいカーネルを置く。AIOS、MemGPT、Agent libOS、IBM の Agent-OS 提案がこれにあたる。(b) Agent as OS（AaOS）: Claude Code などの実運用エージェント自体がすでに OS だとみなし、欠けている保護機構を数える。(c) 名前だけが OS のもの: SkillOS は「OS 風のファイル I/O でスキルを管理する」RL 学習レシピで、カーネルは持たない。syscall や資源の定義が具体的なのは AIOS（モジュールごとに syscall 表がある）と Agent libOS（プロセス状態と許可述語を形式化している）。

### Cited Findings

**Karpathy の「LLM OS」（2023）**
- Karpathy は LLM を「新しい OS のカーネルプロセス」とみなす枠組みを示した。コンテキストウィンドウを RAM にたとえる図が広く引用されている。原典のツイートは取得できず、二次情報のみで確認した — [Illustrated LLM OS (HF blog)](https://huggingface.co/blog/shivance/illustrated-llm-os); [LLMs: Subroutine or Kernel (Substack)](https://aideas.substack.com/p/llms-subroutine-or-kernel)
- IBM の論文は「Karpathy の LLM-OS framing と AIOS が、OS アナロジーが生産的だと示した」と位置づけ、自分たちの貢献を次の段階である意味論の仕様化だとしている — [Steinder & Franke, IBM, arXiv 2607.25076 (2026-07-27)](https://arxiv.org/abs/2607.25076)

**AIOS（Rutgers, Mei et al.。初版 2024-03、v5 は 2025-08、COLM 2025 採択）**
- 3層構成（アプリ層・カーネル層・ハードウェア層）をとる。AIOS カーネルは従来の OS カーネルと並んで置かれ、LLM 関連のサービスを担う。カーネルのモジュールは LLM Core、Scheduler、Context Manager、Memory Manager、Storage Manager、Tool Manager、Access Manager — [AIOS, arXiv 2403.16971](https://arxiv.org/abs/2403.16971)
- 各 LLM インスタンスを「CPU コアに相当する core」として包む。エージェントのクエリは LLM / memory / storage / tool の4種類の syscall に分解され、syscall ごとにスレッドが割り当てられる（SysCall クラスが Thread を継承する）。キューはスケジューラに集中させている — [同上](https://arxiv.org/abs/2403.16971)
- 付録 Table 2 の syscall 一覧の例: Memory Manager は add/remove/update/retrieve memory、Storage Manager は sto_create_file / sto_mount / sto_write / sto_retrieve / sto_rollback / sto_share、Tool Manager は execute_tool_syscall / load_tool_instance、Access Manager は add_privilege / check_access / ask_permission — [同上](https://arxiv.org/abs/2403.16971)
- Context Manager は LLM の生成を途中で止めて再開するためのスナップショットと復元を持つ。復元方式は、テキストベース（logits が取れないクローズドモデル向け）と logits ベース（探索木の中間状態を保存する）の2種類 — [同上](https://arxiv.org/abs/2403.16971)
- Memory Manager はエージェントの対話履歴を RAM 上で管理する。割り当てブロックの 80% を超えると LRU-K 方式で Storage Manager 経由でディスクへ退避する。Storage Manager はローカルファイルとベクトル DB（chromadb など）で実装されている — [同上](https://arxiv.org/abs/2403.16971)
- 先行するビジョン論文「LLM as OS, Agents as Apps」（2023-12）は、LLM を OS、エージェントをアプリとみなすエコシステム像を示した（要旨のみ） — [Ge et al., arXiv 2312.03815](https://arxiv.org/abs/2312.03815)
- README によると、2024-11-30 の v0.2 でカーネルと SDK を分離した。2025-03-12 に大規模リファクタ（v0.2.2）、2025-05-24 に LiteCUA（「Computer as MCP Server」）を公開した。Tool Manager は VM Controller と MCP Server を含む構成に再設計された。デプロイは Mode 1（ローカルカーネル）と Mode 2（リモートカーネル）が対応済みで、Mode 3（個人用リモートカーネル）と Mode 4（仮想化カーネル）は進行中 — [agiresearch/AIOS README](https://github.com/agiresearch/AIOS)

**MemGPT（UC Berkeley, Packer et al.。v2 は 2024-02。現 Letta）**
- 副題は「Towards LLMs as Operating Systems」。仮想メモリのページングにならい、main context（プロンプトトークン＝RAM）と external context（ディスク）を分ける。main context は system instructions（読み取り専用）、working context（関数経由でのみ書き込める固定サイズ）、FIFO キュー（先頭に再帰要約を置く）の3つで構成される — [MemGPT, arXiv 2310.08560](https://arxiv.org/abs/2310.08560)
- 外部記憶は recall storage（全メッセージ履歴）と archival storage（任意長テキストの読み書き DB）の2つ。LLM が関数呼び出しで自分のメモリを出し入れする（「self-directed」） — [同上](https://arxiv.org/abs/2310.08560)
- Queue Manager は、トークン数が warning 閾値（例: 70%）を超えると「memory pressure」システムメッセージを入れ、flush 閾値（例: 100%）を超えると約 50% を退避して再帰要約を作り直す。イベント（ユーザー発話、システム警告、定期タイマー）を割り込みとして扱う。`request_heartbeat=true` で関数呼び出しを連鎖させる — [同上](https://arxiv.org/abs/2310.08560)
- 現在の Letta ドキュメントでは V1 SDK（memory blocks、archival、MCP tools など）が非推奨になり、Agent SDK へ移行中。Agent SDK は git で追跡するメモリ「MemFS」と「dreaming」、Skills、subagents、永続ファイルシステム、Permissions を挙げている。詳細は取得できなかった — [Letta docs](https://docs.letta.com/concepts/memgpt)

**OS-Copilot / FRIDAY（Shanghai AI Lab ほか, 2024-02, ICLR 2024 Workshop）**
- 「OS」は OS 上で動く汎用コンピュータエージェントという意味で、カーネルを新設するわけではない。Planner（DAG で計画）、Configurator（working / declarative / procedural memory）、Actor（executor と critic）で構成される。procedural memory はツールリポジトリで、ツールは API サービス（POST で呼ぶ）か Python ファイル（BaseAction を継承するクラス）として保存される — [OS-Copilot, arXiv 2402.07456](https://arxiv.org/abs/2402.07456)

**Agent libOS（Tsinghua, Yingqi Zhang。v3 は 2026-08-18）**
- 「agent-native library OS」。プロセス状態を ⟨id, img, status, mem, cwd, T(ツール表), S(ロード済み Skills), J(JIT ツール), C(Capability 集合), M(Task Authority Manifest), B(予算), L(ラベル), Q(キュー), children⟩ と形式化している。spawn / fork / exec / wait / signal / pause / resume / exit を明示的なライフサイクル状態として持つ — [Agent libOS, arXiv 2606.03895](https://arxiv.org/abs/2606.03895)
- 3つの平面を分ける。操作許可（OpAdmit = live ∧ cap ∧ ceiling ∧ policyOrHuman ∧ budget ∧ primitive の連言）、情報フロー許可（ラベルと Host が持つ Sink レジストリによる）、証拠（監査ログ。ただし「証拠は権限を与えない」）。中心原則は「自己進化するエージェントは要求できることを変えられても、影響を与えてよい範囲は変えられない」 — [同上](https://arxiv.org/abs/2606.03895)

**IBM「Towards an Agent Operating System」（2026-07-27）**
- POSIX と Kubernetes にならい、OS → Cloud-OS → Agent-OS の3段階の歴史として整理している。13個のプリミティブ（Agent lifecycle、Orchestrator、Skills registry、Tool mediation、Context management、A2A、Agent memory、Identity & AuthZ、Behavioral guardrails、Failure detection、Saga & checkpoint、Trajectory observability、AI-aware proxy）を提案し、それぞれに成熟度（Open / Partial / Early）を付けた。Skills registry と Context management は「Open / Long」（新しい形式理論が必要）とされている — [arXiv 2607.25076](https://arxiv.org/abs/2607.25076)
- 実装プロトタイプは Kubernetes 上の rossoctl（AuthBridge、SPIFFE/SPIRE、MCP Gateway、sidecar 型の Agent Execution Environment）— [同上](https://arxiv.org/abs/2607.25076)

**Agents as OS（AaOS）「Ring-0 by Default」（Nankai, 2026-10-24）**
- MemGPT、AIOS、AOS を「OS4A」と呼んで区別し、逆に「実運用のエージェント自体がすでに OS だ」と主張する。OS の条件として、資源の多重化、固定インターフェース（ツール呼び出し＝syscall 境界）を通した仲介アクセス、セッションをまたぐ永続状態の3つを挙げる。Claude Code、Codex CLI、Gemini CLI、OpenHands、AutoGPT はこれをほぼ満たすという — [AaOS, arXiv 2610.33753](https://arxiv.org/abs/2610.33753)
- 対応づけは次のとおり。MCP サーバー＝デバイスドライバ、skills/plugins＝パッケージ、CLAUDE.md や設定＝自動起動エントリ（レジストリの Run キー相当）、hooks＝割り込みベクタ表、checkpoint＝suspend/resume（ただし実際にはロールバックなので「mutated」）— [同上](https://arxiv.org/abs/2610.33753)

**SkillOS（UIUC / Google Cloud AI Research / MIT, 2026-05-07）**
- カーネルは持たない。凍結した Agent Executor と、RL で学習する Skill Curator の2つで構成される。Curator は外部の SkillRepo（Markdown の SKILL.md 形式で、YAML frontmatter は name と description だけ）を insert / update / delete の関数呼び出しで編集する。論文は「OS に似たファイル I/O 操作で管理する」と書いている — [SkillOS, arXiv 2605.06614](https://arxiv.org/abs/2605.06614)

**その他の 2026 年の「Agent OS」系（いずれも要旨のみ）**
- AOS: 分散エージェントシステムの参照運用アーキテクチャ（2026-08）— [arXiv 2608.03214](https://arxiv.org/abs/2608.03214)
- Agent Operating Systems: 従来 OS にエージェント制御プレーンを統合する提案（2026-06）— [arXiv 2606.01508](https://arxiv.org/abs/2606.01508)
- Qualixar OS: 「application-layer OS」を名乗り、AIOS を kernel-level と位置づけて対比している（2026-04）— [arXiv 2604.06392](https://arxiv.org/abs/2604.06392)
- AgentKernel: trust-native なエージェント OS（2026-08）— [arXiv 2609.29647](https://arxiv.org/abs/2609.29647)
- AOHP: OS レベルのエージェントハーネス（Tsinghua / PKU / HKU, 2026-06）— [arXiv 2606.23449](https://arxiv.org/abs/2606.23449)
- Kernel-Managed Shared Memory（Rutgers, 2026-09。AIOS 系の続編と思われる）— [arXiv 2609.10144](https://arxiv.org/abs/2609.10144)
- Toward Securing AI Agents Like Operating Systems（TU Berlin ほか, 2026-05）— [arXiv 2605.14932](https://arxiv.org/abs/2605.14932)
- When the Agent Becomes the Kernel（Huawei の SoK, 2026-09）— [arXiv 2609.23700](https://arxiv.org/abs/2609.23700)
- Self-evolving OS layer で基盤モデルを仮想化する position paper（HPE / UChicago / Argonne, 2026-09）— [arXiv 2609.19203](https://arxiv.org/abs/2609.19203)

### Inferences
- 「カーネル」が指すものは論文ごとに違う。AIOS ではスケジューラと資源マネージャの集まりで、LLM 自体は CPU 扱いになる。Karpathy と MemGPT では LLM 自体がカーネルやプロセッサになる。Agent libOS では許可を判定するランタイムで、LLM は信頼しない。スキルリポジトリを設計するうえで最も参考になるのは、モデルを信頼しない Agent libOS 型と AaOS の分析だと考える。
- 2024 年の AIOS は「LLM 推論資源の多重化（GPU 1枚を多数のエージェントで共有する）」が主眼だった。2026 年の論文群は「権限と供給網の保護」へ焦点が移っている。

### Gaps
- Karpathy の原ツイートは取得できず、日付が確定しない。二次情報では 2023-11 説が多い。私の記憶では 2023-09 末の投稿だが、未確認。2023-11 の講演「Intro to LLMs」で同じ図が示されたことは複数の二次情報が一致している。
- Letta の Agent SDK における Skills と Permissions の仕様は、ドキュメントの該当ページを取得できず未確認。
- AOS、Qualixar、AgentKernel、AOHP などは本文を読んでいないため、syscall や資源の定義は不明。

---

## 問2: ツールとスキルの管理（レジストリ、発見、遅延ロード、コンテキスト予算、スケジューリングと並行性、アクセス制御）

### Takeaway
研究系の Agent OS はツールを「コード実体」として扱う。登録、検証、並列数の制限、ハブ配布が中心になる（AIOS / Cerebrum、OS-Copilot）。2025〜2026 年の SKILL.md 系は、スキルを「プロンプトに入る指示文」として扱い、段階的な開示によるコンテキスト予算管理が中心になる。両者を結ぶ論点は、スキルを有効化しても権限は増えないこと（Agent libOS）と、署名・マニフェスト・ハーネスが強制する権限がまだ欠けていること（AaOS、IBM）。

### Cited Findings

**登録・ロード（コード型ツール）**
- AIOS の Tool Manager は統一インターフェースでツールを扱い、実行前にパラメータを検証する。名前で呼ばれるとツールインスタンスを動的にロードし、実行ファイルの初期化と依存関係の検証を行う — [AIOS](https://arxiv.org/abs/2403.16971)
- AIOS は並列アクセスに制約があるツールについて、ハッシュマップで実行中のインスタンス数を数える。衝突するリクエストは飛ばし、キュー内の次の衝突しない要求を処理する — [AIOS](https://arxiv.org/abs/2403.16971)
- Cerebrum（AIOS SDK, NAACL 2025 demo, 2025-03）は Agent Manager と Tool Manager を持ち、配布、バージョン管理、キャッシュ、パッケージング、アップロードとダウンロードを担う。エージェントは (author, name, version) の3つ組で識別され、`.agent` / `.tool` ファイルとしてハブへアップロードされる。ダウンロード時には整合性を検査する。ハブ上では暗号化・ハッシュ化・圧縮した形で保存する。著者自身が「アップロードされたエージェントに正式な審査プロセスがない」ことを限界として挙げている — [Cerebrum, arXiv 2503.11444](https://arxiv.org/abs/2503.11444)
- OS-Copilot の FRIDAY は、サブタスクごとに dense retrieval でツールを検索する。類似度が閾値未満なら Tool Generator が新しいツール（Python クラス）を生成する。成功時に critic が 0〜10 で採点し、8 を超えたものだけをリポジトリに保存する。失敗時は最大3回まで自己修正する — [OS-Copilot](https://arxiv.org/abs/2402.07456)

**登録・ロード（指示型スキル。SKILL.md）**
- SkillOS は BM25 で上位 k 件のスキルを取得して Executor のプロンプトに入れる。著者は限界として、検索が単純であること、単一 Markdown に単純化したため scripts や下位スキルの階層構成を捨てたことを挙げている — [SkillOS](https://arxiv.org/abs/2605.06614)
- Claude Code は Agent Skills オープン標準に準拠する。通常のセッションでは description だけを常にコンテキストへ入れ、本文は呼び出し時にロードする。`description` と `when_to_use` は合計 1,536 文字で切り詰められる。SKILL.md は 500 行以内を推奨し、詳細は別ファイルに分けて必要時に読ませる。呼び出し後の本文はターンをまたいで残る。自動コンパクション時はスキルごとに先頭 5,000 トークン、合計 25,000 トークンまで再添付される。サブディレクトリの `.claude/skills/` は、そのディレクトリのファイルに初めて触れたときにロードされる。`paths` の glob でも起動できる — [Claude Code Skills docs](https://code.claude.com/docs/en/skills)
- Claude Code のスキル配置と優先順位は enterprise > personal > project。plugin のスキルは `/plugin-name:skill-name` で名前空間が分かれるので常にロードされる。`context: fork` を指定するとサブエージェントで実行し、`agent` で種類を選べる — [Claude Code Skills docs](https://code.claude.com/docs/en/skills)
- Agent libOS では、Skills は SKILL.md パッケージ（指示、リソース、可視にする組み込みツール、任意の JIT ツール候補）で、発見と有効化は明示的な操作になる。モデルに見せる射影 V(T,S,J,…) と、呼び出し可能な完全なツール表を分けて持つ。Skill はツールの部分集合を必要なときに射影する — [Agent libOS](https://arxiv.org/abs/2606.03895)

**コンテキスト予算**
- MemGPT は、取得結果のページネーションで溢れを防ぐ、memory pressure 警告を出す、FIFO から退避して再帰要約を作る、の3つでコンテキストを管理する — [MemGPT](https://arxiv.org/abs/2310.08560)
- Agent libOS は LLM 呼び出しごとに Context Materialization Manifest を記録する。各オブジェクトが含まれたか省かれたか、その理由（selected、filter_mismatch、capability_denied、token_budget など）、変換（verbatim / compacted / truncated）が残る — [Agent libOS](https://arxiv.org/abs/2606.03895)
- IBM は「各スキルがコンテキストウィンドウを消費する。パッケージ管理には相当する概念がない」と指摘し、トークンの退避は時間的局所性（LRU）では原理的に扱えないとしている。Context management を「Open / Long」に分類した — [IBM 2607.25076](https://arxiv.org/abs/2607.25076)

**スケジューリングと並行性**
- AIOS は FIFO と Round Robin を実装している。RR は context interrupt を使ったタイムスライスで動く — [AIOS](https://arxiv.org/abs/2403.16971)
- AaOS は、並列ツール呼び出しやサブエージェントが同じファイルやメモに排他制御なしで書き込んでいることを指摘し、ツール境界にロックかバージョン付き書き込みが必要だとしている — [AaOS](https://arxiv.org/abs/2610.33753)
- Agent libOS の Durable Task Run v1 では、動的なバインディング変更として自動継続が認められるのは `activate_skill` を単独で呼ぶ非並列応答だけ。それ以外の Image / Tool / provider / Skill のバインディング変更は needs_attention で止まる — [Agent libOS](https://arxiv.org/abs/2606.03895)

**アクセス制御**
- AIOS の Access Manager は、エージェント ID を特権グループに対応づけるハッシュマップで、エージェント間のデータ読み書きを制御する。削除や上書きなど不可逆な操作の前には、ユーザー確認（ask_permission）を挟む — [AIOS](https://arxiv.org/abs/2403.16971)
- Agent libOS では、Skill を有効化してもファイルシステム、シェル、Git、MCP などの Capability は付与されない。ツールは各ドメインのプリミティブでの検査を受ける。JIT ツール（Deno/TypeScript）が触れられるランタイムの入口は `libos.syscall` だけで、static import、re-export、動的 import は拒否される — [Agent libOS](https://arxiv.org/abs/2606.03895)
- Claude Code の `allowed-tools` は、呼び出したターンに限り確認なしで使えるツールを与えるもので、利用可能なツールを制限するものではない。次のメッセージで解除される。`disallowed-tools` はスキルが有効な間ツールを外す。`Skill(name)` の allow / deny ルール、`skillOverrides`（on / name-only / user-invocable-only / off）、`disableSkillShellExecution`、`allowManagedPermissionRulesOnly`（project / personal スキルの allowed-tools を無視させる）がある。ドキュメントは「信頼していないフォルダでの `-p` 実行でも project スキルの allowed-tools が適用される」と警告している — [Claude Code Skills docs](https://code.claude.com/docs/en/skills)
- AaOS の packaging（SS_N）では、7つの仕組みのうち4つが missing。スキルは内容がそのまま指示なので「インストールは実行と同じ」になる。レジストリには署名も権限マニフェストもなく、バージョン管理も弱い。必要なものとして、ロード時に検査する署名と固定バージョン、モデルが読むのではなくハーネスが強制する権限マニフェスト、インストール後の description 変更の検出、残骸まで消すアンインストールを挙げている — [AaOS](https://arxiv.org/abs/2610.33753)
- IBM は Skills registry に「semantic SBOM」（ドメイン、モデル互換性、呼び出すツールの宣言を、ロード時に強制する）が必要だと提案している。また別研究を引用して、モデルの不一致だけでタスク性能が 15% 劣化すること、スキルの 26% に脆弱性が1件以上あることを挙げている（いずれも孫引き）— [IBM 2607.25076](https://arxiv.org/abs/2607.25076)

**スキル管理の周辺研究（要旨のみ。別担当の範囲と重なる可能性あり）**
- SkillBrowser: Selective Skill Exposure — [arXiv 2610.23554](https://arxiv.org/abs/2610.23554)
- Workday による Progressive Disclosure の実運用レポート — [arXiv 2609.35692](https://arxiv.org/abs/2609.35692)
- 同時にインストールしたスキル同士の衝突 — [One Skill Too Many, arXiv 2610.11647](https://arxiv.org/abs/2610.11647); [One Skill Takes Over, arXiv 2610.25064](https://arxiv.org/abs/2610.25064)
- スキルを構造化表現にする SSL（Scheduling-Structural-Logical）— [arXiv 2604.24026](https://arxiv.org/abs/2604.24026)

### Inferences
- スキルリポジトリの設計に移せそうな原則を挙げる。(1) モデルに見せる面（description、射影）と権限（capability）を分ける。(2) 有効化しても権限は増えない。(3) 権限マニフェストはモデルに読ませるのではなくハーネスに強制させる。(4) 署名とバージョン固定を、インストール時ではなくロード時に検査する。(5) どのスキルを入れ、どれを省いたかを理由つきで記録する。
- Claude Code の `allowed-tools` は、Agent libOS の意味での「権限付与」に近く、しかも一時的な付与になっている。権限の上限（ceiling）を絞る仕組みは、`disallowed-tools` と managed policy 側にある。

### Gaps
- Codex CLI、Cursor、Gemini CLI のスキルやプラグインのロード仕様（予算値や名前空間）は一次ドキュメントを読んでいない。AaOS 付録の記述（Codex の skills は MCP 設定を同梱できる、Gemini CLI は Agent Skills を持つ）にとどまる。
- AIOS のツールハブ（tool hub）の具体的な仕様は README に記述がない。

---

## 問3: 評価（ベンチマーク、スループット、成功率）と、著者自身が認める限界

### Takeaway
定量的な評価は、AIOS（推論資源の多重化による最大 2.1 倍の高速化）、MemGPT（長期記憶タスク）、OS-Copilot（GAIA）、SkillOS（ALFWorld / WebShop / 数学）に集中している。いずれも OS 的な分離がタスク成功率を大きく変えるわけではなく、効率や記憶の改善を示したものにとどまる。2026 年のセキュリティ寄りの論文（Agent libOS、AaOS）は、成功率ではなく「不正な効果ゼロ」や「保護機構の欠落数」で評価している。

### Cited Findings
- AIOS（GPT-4o-mini）の成功率は、AIOS なし→ありで次のとおり。ReAct: HumanEval 48.8→50.6、MINT 29.4→30.1、GAIA 5.5→7.3、SWE-Bench-Lite 3.9→4.3。Autogen: GAIA 7.3→9.7、他は同じ。改善の理由として、プロンプトの構造化と、ツール呼び出し前の regex によるパラメータ検証を挙げている — [AIOS](https://arxiv.org/abs/2403.16971)
- AIOS のスループットは、Reflexion と Llama-3.1-8b の組み合わせで最大 2.1 倍。RTX A5000 1枚、同時 250 エージェントという条件。エージェント数を 250 から 2000 に増やしても、実行時間と待ち時間はほぼ線形に伸びる。スケジューリングの比較（ReAct / HumanEval）では、全体実行時間が None 152.1s、FIFO 74.2s、RR 77.3s。p90 待ち時間は RR が 4.2s で FIFO の 5.0s より良い。context switch の有無で出力の BLEU / BERT がともに 1.0 — [AIOS](https://arxiv.org/abs/2403.16971)
- AIOS が自ら挙げる今後の課題は、エージェントとツールを統一的に扱うセマンティックなスケジューリング、コンテキストのスナップショットの効率化と圧縮、エージェント間の共有メモリと階層ストレージ、他エージェントのメモリへの不正アクセスや jailbreak への対策 — [AIOS](https://arxiv.org/abs/2403.16971)
- MemGPT の Deep Memory Retrieval の精度は、GPT-4 で 32.1% → 92.5%、GPT-4 Turbo で 35.3% → 93.4%、GPT-3.5 Turbo で 38.7% → 66.9%。nested KV 検索では、GPT-4 単体は3段のネストで 0% になるが、MemGPT+GPT-4 はネストの深さに影響されない — [MemGPT](https://arxiv.org/abs/2310.08560)
- FRIDAY の GAIA 成功率は Level1 40.86%、L2 20.13%、L3 6.12%。比較対象は GPT-4 Plugins が L1 30.3%、AutoGPT-4 が 15.05%。SheetCopilot-20 では自己学習なしで 0%、10 タスクを自己学習して 8 ツールを獲得した後は 60%（SheetCopilot の GPT-4 は 55%）— [OS-Copilot](https://arxiv.org/abs/2402.07456)
- SkillOS は最強ベースライン比で最大 +9.8% の相対改善と、ステップ数 −6.0%。8B の Curator が、Curator として使った Gemini-2.5-Pro を上回った。ALFWorld のアブレーションでは平均成功率が 61.2 から、グルーピングなしで 57.3、内容品質報酬なしで 58.6 に下がる。学習が進むと、操作の比率は insert 優位から update 優位へ移り、delete は少ないまま — [SkillOS](https://arxiv.org/abs/2605.06614)
- Agent libOS: ランタイム全体の評価で 33/33 タスク成功、不正な効果 0/119、誤った拒否 0/119。実モデルで 42 軌跡を試し、安全性 12/12、strict utility 12/12。Skills 射影とフルスキーマ基線の比較では、完全正解がどちらも 13/15 で差は出なかった。著者は「母集団についての率ではない」と明記している。prompt injection を消すこと、カーネル級のサンドボックス、不可逆な外部効果のロールバック、改ざん耐性のある証拠のいずれも主張しない — [Agent libOS](https://arxiv.org/abs/2606.03895)
- AaOS は 116 の OS 機構を 19 のサブシステムに分けて対応づけた。isomorphic 11、degraded 26、mutated 14、missing 65（56%）、novel 9。Claude Code、Codex CLI、Gemini CLI で 13 の実験を行い、25 の機構を検証した結果、16 は分析どおり、7 は記述がより精密になり、2 は判定が変わった。主な発見は次のとおり。ファイルツールが拒否した書き込みがシェル経由で通る。3つの CLI はいずれも、偽造したトランスクリプト記録を resume 時にユーザーメッセージとして読み込む。サブエージェントは親の権限を継承する。task id はプロセスではなくラッパーを指す — [AaOS](https://arxiv.org/abs/2610.33753)

### Inferences
- AIOS の 2.1 倍は、ローカル GPU 1枚を多数のエージェントで取り合うという特殊な条件での数字。API 経由の LLM を使い、ユーザーがエージェントを1つ使う今の CLI ハーネスでは、この効果はほとんど関係しないと推測する。
- スキルをコンテキストへ選択的に開示する効果（Agent libOS の 13/15 対 13/15）は、小規模では差が出ていない。射影の価値は、精度よりも権限と監査にあるという読み方ができる。

### Gaps
- AIOS の syscall あたりの絶対スループット値は、図が正規化値のため読み取れていない。
- SkillOS の ALFWorld / WebShop のベースライン別の絶対値（Table 1）は今回取得していない。

---

## 問4: 実運用のハーネス（Claude Code、Codex、Cursor など）に採用されたアイデアと、研究にとどまっているもの

### Takeaway
採用されたのは「機能面の OS 抽象」。ツール＝syscall、MCP＝ドライバ、Skills / plugins＝パッケージ、CLAUDE.md や AGENTS.md＝自動起動、hooks＝割り込み、サブエージェント＝プロセス、チェックポイント、コンパクション（MemGPT 的なページング）、段階的な開示によるコンテキスト予算がこれにあたる。研究にとどまるか欠けているのは「保護面」。ハーネスが強制する capability と権限の上限、スキルの署名と権限マニフェスト、改ざんできない監査、トークンの quota と rlimit、ロック、信頼できる時計、型付きのエラーがこれにあたる。AIOS 型の推論スケジューラは、ハーネスではなく推論サーバ側の課題として扱われ、ハーネスには入っていない。

### Cited Findings
- AaOS の Table 1 によると、Claude Code、Codex CLI、Gemini CLI、OpenHands、AutoGPT はいずれも、action loop、ツールの syscall インターフェース、永続メモリ、パッケージ化された拡張（skills）、ネットワーク、ホスト側のサンドボックスを持つ。MCP は 5 中 4 — [AaOS](https://arxiv.org/abs/2610.33753)
- AaOS 付録によると、Claude Code は hooks（block / allow / ask と引数の書き換え）、独立したコンテキストと権限を持つサブエージェント、Agent Skills、チェックポイントを持つ。チェックポイントについては、Bash による変更や大半のサブエージェントの編集が復元されないとドキュメントに書かれている。Codex CLI は Skills（MCP 設定を同梱可）、AGENTS.md、ライフサイクル hooks（SessionStart、PreToolUse、PostCompact など）、既定で有効なマルチエージェントを持ち、チェックポイントはない。Gemini CLI は Agent Skills、checkpoint と restore、GEMINI.md、実験的な auto-memory を持つ。OpenHands は project / user / global の優先順位を持つ公開スキルレジストリを持つ — [AaOS](https://arxiv.org/abs/2610.33753)
- Claude Code のスキルは、description を常時ロードし本文を遅延ロードする段階的な開示、1,536 文字の上限、コンパクション時の再添付予算（各 5,000 トークン、合計 25,000 トークン）、名前空間（plugin）、組織管理ポリシー（managed settings）を実装している — [Claude Code Skills docs](https://code.claude.com/docs/en/skills)
- AaOS の結論は、「関数は移植されたが保護は移植されていない」。11 個の isomorphic のうち保護機構は4つ（hooks、アドレス空間、仮想化、サンドボックス）で、すべてエージェントとホストの境界で働く。プロンプトに書いたルールは、Anderson の参照モニタの基準（迂回不能、改ざん不能、検証可能）をどれも満たさない — [AaOS](https://arxiv.org/abs/2610.33753)
- IBM は「あるハーネス向けに書いたスキルは別のハーネスに移らない」ことを Phase 1（実験期）の症状として挙げている。また UC Berkeley の調査を引用し、フレームワークはプロトタイプでは役立つが本番では捨てられることが多いと述べている — [IBM 2607.25076](https://arxiv.org/abs/2607.25076)
- 反証になりうる事実として、Claude Code のドキュメントでは、Agent Skills オープン標準の範囲外（claude.ai や Skills API）で使えるキーは `name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools` だけ。それ以外のキーはエラーになる。共通サブセットによる一定の可搬性はすでにある — [Claude Code Skills docs](https://code.claude.com/docs/en/skills)
- MemGPT 型の「LLM 自身がメモリを編集する」設計は、Letta で製品化されている。新しい Agent SDK は git で追跡する MemFS と Skills / subagents に移行中 — [Letta docs](https://docs.letta.com/concepts/memgpt)

### Inferences
- 採用されたものは、モデルの協力を前提とする「ソフトな」仕組みが多い。description による発見、自動コンパクション、プロンプト内のルールがそうだ。研究にとどまるものは、モデルを信頼しない「ハードな」仕組みが多い。capability の連言による許可、ラベルとシンクによる情報フロー制御、署名検証がそうだ。スキルリポジトリでは、ハーネスが今すでに強制できる手段（allowed / disallowed-tools、Skill ルール、managed policy、名前空間）に寄せて設計し、マニフェストや署名は将来ハーネスが強制できる形（宣言的なメタデータ）で先に記述しておくのが現実的だと考える。
- MemGPT のページングと Claude Code のコンパクションでのスキル再添付予算は、同じ「コンテキスト＝主記憶」という比喩の実装にあたる。ただし、退避の方針が LRU では原理的に足りないという IBM の指摘は、どちらも解決していない。

### Gaps
- Cursor のルールやプラグインのロード方式と権限モデルは、一次資料を確認していない。
- AIOS の考え方（推論資源のスケジューラ、logits スナップショット）がどの商用製品に入ったかを示す一次資料は見つからなかった。
- Codex の skills と plugins の公式ドキュメント（予算値、配置、優先順位）は今回読んでいない。
