# スキルは OS の機能を得たが保護をまだ持たない

2026年11月時点で、エージェントのスキルを「OS のように管理する」仕組みは、**読み込み・名前空間・パッケージといった機能面ではすでに実装されている。一方で、権限の強制・署名・来歴・依存の解決といった保護面は、研究と各社の独自実装にとどまり、標準になっていない**。標準化が済んでいるのは下の層だけである。手順の知識を表す Agent Skills（`SKILL.md`）と、スキルと MCP を束ねる Agent Plugins 1.0 がそれにあたる。マーケットプレイス、版の解決、権限は Claude Code などの各社が独自に作っている。スキルライブラリの研究からは、設計上の制約が3つ出ている。人が選んだ短いスキルは平均十数ポイント効くこと、モデルが自分で書いたスキルは効かないこと、無関係なスキルが増えると関連スキルすら読まれなくなることである。安全性の測定では、公開スキルの約4分の1に危険なパターンが見つかった。またコピーで配られたスキルには、元の修正が約2割しか届かない。`ryo-morimoto/plugins` の「1資産1 plugin」という既定は、この証拠とよく合っている。ただし Claude Code が Agent Plugins 形式を読むことは、一次資料では確認できなかった。このため「Claude Code で動いた」ことは「Agent Plugins に準拠している」ことの証明にならない。両方の manifest を置き、別々に検証する構成が必要になる。

## OS の比喩は「機能」を移し、「保護」を移していない

「LLM を OS とみなす」研究は3系統に分かれる。1つ目は、エージェントの下に新しいカーネルを置く系統である。AIOS は LLM・memory・storage・tool の4種類の syscall と、スケジューラ・コンテキスト管理・アクセス管理のモジュールを持つ。成果は、GPU 1枚を250エージェントで共有する条件で**最大2.1倍のスループット**を出したことだった（[AIOS](https://arxiv.org/abs/2403.16971)）。MemGPT はコンテキストを RAM、外部記憶をディスクとみなし、ページングで長期記憶を扱った。Deep Memory Retrieval の精度は GPT-4 で **32.1% から 92.5%** に上がった（[MemGPT](https://arxiv.org/abs/2310.08560)）。2つ目は、Claude Code などの実運用エージェントがすでに OS だとみなし、欠けている部品を数える系統である。この系統の AaOS 論文は、MCP をデバイスドライバ、skills と plugins をパッケージ、hooks を割り込みベクタ表に対応づけた。そのうえで116の OS 機構を照合し、**56%（65個）が欠けている**と報告した（[AaOS](https://arxiv.org/abs/2610.33753)）。3つ目は名前だけが OS のもので、SkillOS は RL で学習したキュレータが SKILL.md を insert/update/delete する学習手法である（[SkillOS](https://arxiv.org/abs/2605.06614)）。

焦点は2024年から2026年にかけて、推論資源の多重化から権限と供給網の保護へ移った。AaOS の結論は「**関数は移植されたが保護は移植されていない**」というものである。3つの CLI で行った実験では、ファイルツールが拒否した書き込みがシェル経由で通ること、偽造したトランスクリプトを resume 時にユーザー発話として読み込むこと、サブエージェントが親の権限を継承することを確認している。パッケージの層については、スキルは中身がそのまま指示なので「**インストールは実行と同じ**」だと指摘する。そのうえで、ロード時に検査する署名と固定版、ハーネスが強制する権限マニフェスト、インストール後の description 変更の検出を必要な対策に挙げた（[AaOS](https://arxiv.org/abs/2610.33753)）。Agent libOS は同じ問題を形式化した。中心原則は「**スキルを有効化しても capability は増えない**」で、モデルに見せる面と呼び出せるツール表を分けている（[Agent libOS](https://arxiv.org/abs/2606.03895)）。IBM の Agent-OS 提案は13のプリミティブを挙げ、Skills registry と Context management を「Open / Long」（新しい理論が必要）に分類した。Skills registry については、ドメイン・モデル互換性・呼び出すツールをロード時に強制する「semantic SBOM」を提案している（[IBM](https://arxiv.org/abs/2607.25076)）。

これらの研究がスキルリポジトリに渡せる教訓は、「権限はプロンプトの外で強制する」ことである。今日のハーネスが強制できる手段は、Claude Code の `disallowed-tools`、`Skill(name)` の allow/deny、managed policy、名前空間に限られる。なお Claude Code の `allowed-tools` は、呼び出したターンだけ確認を省く「一時的な付与」で、ツールを制限する仕組みではない（[Claude Code skills](https://code.claude.com/docs/en/skills)）。

## 標準は下の層だけで、上の層ほど各社の独自実装になる

標準と実装を層で並べると、どこまで決まっているかが分かる。

| 層 | 標準 | 主な実装・状態 |
| :- | :- | :- |
| 手順の知識 | Agent Skills（`SKILL.md`、frontmatter 6フィールド） | Claude Code、Codex、Cursor などが採用。Claude Code は独自フィールドを多数追加 |
| 実行時のツール | MCP（スキーマ 2026-07-28、AAIF 管理） | 「Skills over MCP」が拡張として進行中 |
| パッケージ | Agent Plugins 1.0（2026-08-06） | ChatGPT/Codex、Cursor、Copilot、Kiro、VS Code。Claude は独自の `.claude-plugin/` |
| カタログ・配布 | なし | Claude の `marketplace.json`、skills.sh など |
| 依存・版・署名 | なし | Claude Code の semver 依存、コミュニティのロックファイル |

**Agent Skills** は Anthropic が2025年12月18日にオープン標準として公開した。必須フィールドは `name`（64字以下の小文字・数字・ハイフンで、**親ディレクトリ名と一致**）と `description`（1024字以下）の2つである。任意フィールドは `license`・`compatibility`・`metadata`・`allowed-tools` で、`allowed-tools` は実験的扱いになっている（[Agent Skills Specification](https://agentskills.io/specification)）。読み込みは3段階で、起動時はメタデータ約100トークン、起動後は本文（**5000トークン未満・500行未満**を推奨）、必要になったら参照ファイルを読む（[同上](https://agentskills.io/specification)）。Claude Code はこの形式に `when_to_use`、`disable-model-invocation`、`context: fork`、`paths`、`hooks` などを足している。しかし claude.ai へのアップロードと Skills API は、標準の6フィールド以外を**ハードエラー**にする（[Claude Code skills](https://code.claude.com/docs/en/skills.md)）。

**Agent Plugins 1.0** は Vercel が起草した。運営委員会には Amazon、Cursor、Microsoft、OpenAI、Vercel の個人が入っている。標準化するのは、ルートの `plugin.json`（閉じたスキーマで、必須は `$schema` と `name`）、`skills/`、`mcp.json` の3つだけである。commands、agents、hooks、マーケットプレイス、依存関係、署名は対象外とされた（[spec 1.0.0](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.0.0.md)）。hooks は 1.1.0 の Working Draft で追加された（[spec 1.1.0](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.1.0.md)）。依存、署名、権限の UX は「将来の検討事項」で、文書は「**現在、プラグインは他のプラグインへの依存を宣言できない**」と明記している（[FUTURE_CONSIDERATIONS](https://raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/FUTURE_CONSIDERATIONS.md)）。公開時の対応クライアント一覧にも運営委員会にも、**Anthropic と Claude Code の名前はない**（[Vercel changelog](https://vercel.com/changelog/introducing-agent-plugins-1-0-0)）。Claude Code の文書にも「Agent Plugins」という語は出てこない。VS Code はこの事情を吸収するため、ルートに正規の `$schema` を持つ `plugin.json` があれば Agent Plugins、`.claude-plugin/plugin.json` があれば Claude 形式、と自動で判別している（[VS Code reference](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference.md)）。

**Claude Code のプラグイン**は、上の層を独自に実装している。主な仕組みは次のとおりである。

- マーケットプレイス：`.claude-plugin/marketplace.json` に書き、取得元には relative・github・git-subdir・archive・npm などを使える（[Create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces)）。
- 依存関係：`dependencies` に semver 範囲で書き、`<plugin>--v<version>` タグの最大版に解決する（[Plugin dependencies](https://code.claude.com/docs/en/plugins/dependencies.md)）。
- `version` の扱い：書いた値でキャッシュが固定され、値を変えるまで更新が届かない。省くとコミットを追う（[Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace.md)）。
- 名前の変更と削除：`renames` で移行し、削除は `forceRemoveDeletedPlugins` で行う。
- 検証：`claude plugin validate --strict` で行う。
- 署名：署名や出自を検証する仕組みは見つからない。固定手段は `sha` と `archive` の `sha256` だけである。

公式の指針は、プラグインに分けるのは「一緒に配り、一緒に版を上げたい単位」としている。また、有効にしたプラグインのスキルの名前と説明は、**使わないセッションでも毎ターンのコンテキストに入る**（[Plugins overview](https://code.claude.com/docs/en/plugins/overview.md)）。

## ライブラリが大きくなると、関連スキルすら読まれなくなる

スキルライブラリの研究は、2023〜2025年の「エージェントが自分でスキルを作って溜める」系統から変わった。Voyager や ASI がこの系統にあたる。ASI は、実行して検証したコードスキルが WebArena でテキスト保存の AWM より +11.3% 高いと報告した（[ASI](https://arxiv.org/abs/2504.06821)）。2026年には、SKILL.md を対象にした実証研究へ移った。最も多く引用される SkillsBench では、**人が選んだスキルは平均約16pp 通過率を上げ、自己生成スキルは平均で悪化させた**。なお版によって数値が違い、初版は86タスクで +16.2pp と −1.3pp、改訂版は87タスクで +16.6pp と −8.1〜−11.5pp だった（[SkillsBench](https://arxiv.org/abs/2602.12670)）。同じ研究では、スキルの長さも効果を分けた。Compact は +19.0pp、Detailed は +14.5pp で、Comprehensive は **+0.7pp** にとどまった。同時に与えるスキルは4個以上になると +10.1pp に下がった。悪化したタスクも13/87あった（[SkillsBench](https://arxiv.org/abs/2602.12670)）。

粒度の研究も同じ向きを示す。Break It Down は、タスク全体から誘導したスキルが成功率を下げ、**サブタスク単位のスキルは上げる**ことを示した（[Break It Down](https://arxiv.org/abs/2608.20274)）。Demystifying Agent Skills は、同じ経験を SKILL.md に蒸留したもの（61.9%）が生の作業記録（55.9%）より効くことを示した。効く仕組みの **65.7% は「手順のアンカー」**で、知識の注入は4.5%にとどまった（[Demystifying](https://arxiv.org/abs/2608.14036)）。スキルが悪さをする経路も測られている。Agent Skills Can Be Harmful によると、スキルが原因の機能失敗のうち、無関係なスキルの誤適用は1.6%だけだった。**68.8% は関連するスキルが誤った実装を招いたもの**である。効率の悪化では、過剰な検証手順が36.8%を占めた（[Harmful](https://arxiv.org/abs/2608.11888)）。

規模の問題は、OS の比喩で言えば「スケジューラ不在」にあたる。Lost in Implicit Routing は、正解スキルを固定したまま無関係なスキルを0個から1,000個まで増やした。このとき**読み込まれたスキルの再現率は73.6%から27.4%に落ち、1つも読み込まない率は9.3%から51.6%に上がった**。それでも Pass@3 は51.6%から38.6%と緩やかにしか下がらないので、成功率だけを見るとこの崩壊を見逃す。原因は文脈の長さではない。無関係なスキルの説明文だけを隠すと、再現率は63.3%まで戻る。つまり**他のスキルの description が意味的に干渉している**（[Lost in Implicit Routing](https://arxiv.org/abs/2610.18522)）。CMU のサーベイも、フラットな検索は64〜128スキル程度で精度が落ちやすいこと、目的を絞ったライブラリのほうが網羅的なライブラリより良いことが多いことをまとめている。また、剪定を止めたシステムではリポジトリが4.5倍に膨らみ、通過率が下がった（[Dynamic Agent Skills](https://arxiv.org/abs/2607.10113)）。ただし、現実的な配備条件で測る SkillBuffBench と Skill Roulette は、まだ結果を出していない（[SkillBuffBench](https://arxiv.org/abs/2611.22017)、[Skill Roulette](https://arxiv.org/abs/2611.23266)）。

## 公開スキルの4分の1は危険で、修正は2割しか届かない

安全性の測定は、スキルの配布が npm の初期より悪い状態にあることを示す。31,132件の公開スキルを調べた研究では、**26.1% に危険になりうるパターン**があった。高深刻度は5.2%である。危険パターンのオッズは、スクリプトを同梱するスキルで2.12倍、500行を超えるスキルで2.14倍だった（[Agent Skills in the Wild](https://arxiv.org/abs/2601.10338)）。開かれたマーケットプレイスの ClawHub では、2026年2月に2,857件中341件が悪意あるスキルと判明した。そのうち335件は、偽の前提条件で情報窃取マルウェアを入れさせる単一のキャンペーンによるものだった（[The Hacker News](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)）。MCP では、承認後にツール説明を書き換える「ラグプル」が実証されている（[Invariant Labs](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)）。実際にも、15版を無害に出したあと v1.0.16 で全メールを BCC させた postmark-mcp が出回った（[The Hacker News](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)）。自動スキャナは頼りにならない。MCP サーバーを調べた研究では、既存のスキャナが96.89%を危険と判定したのに対し、手で確かめた真陽性は50%未満だった（[Rethinking MCP Security](https://arxiv.org/abs/2607.11086)）。

公開側にとって最も示唆が大きいのは、来歴の研究である。Skill Constellations は219万件の採用事例を分析した。スキルはレジストリも版もない**コピーで広がり、元の修正がコピー先に届くのは20.9%** だった。一般のコードのファイルコピーでは、上流のセキュリティ修正が47〜84%届く。スター数はコピー元になる回数とほぼ無関係だった（τ = −0.10）。拡散は速く、最終的な採用者の半数が56日目までに採用していた。著者は、コピーではなく**版付きの参照で配る**よう提言している（[Skill Constellations](https://arxiv.org/abs/2610.11169)）。評価についても、最小限の型はすでにある。Anthropic の skill-creator は、スキルありとベースラインを並べて走らせ、合格率・時間・トークンの差を出す。発火については、発火すべき例と、キーワードが重なる「惜しい」非発火例を合わせて20件作り、学習用と検証用に分けて description を改良する（[skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)）。

## ryo-morimoto/plugins の構成に落とすとこうなる

まず、「1資産1 plugin」という既定は証拠に支えられている。有効化の単位はプラグインなので、利用者は使わない資産を無効にできる。そうすれば常時コンテキストのコストを抑えられ（[Plugins overview](https://code.claude.com/docs/en/plugins/overview.md)）、他のスキルの description による干渉源も減る（[Lost in Implicit Routing](https://arxiv.org/abs/2610.18522)）。Claude Code ではスキルが `plugin:skill` の名前空間で呼ばれるので、プラグイン名は呼び出し名の一部として設計する。後から名前を変えると `renames` での移行が必要になる。逆に、まとめるべきなのは「一緒に使い、一緒に版を上げる」資産だけである。束ねたい場合も、メタプラグインの `skills/` からシンボリックリンクで参照できる（[Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace.md)）。

以下の設計判断は、上の調査から導いた推論である。

<!-- data-source: original -->
| 論点 | 推奨する構成 | 根拠 |
| :- | :- | :- |
| manifest | 各 plugin にルートの `plugin.json`（Agent Plugins、正規の `$schema`）と `.claude-plugin/plugin.json` を併置する。`skills/<name>/SKILL.md` は共有する | 置き場所が違うので衝突しない。Claude Code が Agent Plugins を読むかは未確認 |
| SKILL.md の frontmatter | 標準の6フィールドに限る。Claude 固有の挙動は Claude 側の manifest か、必要最小限にとどめる | 標準外のキーは claude.ai や Skills API でハードエラーになる |
| 名前 | `name` をディレクトリ名と一致させ、`claude-`・`anthropic-`・`cc-plugin-` で始めない。plugin 名は kebab-case にし、`.` は使わない | Agent Plugins は `.` を許すが、Claude は kebab-case を求める |
| 版 | plugin ごとに `version` を書き、`<plugin>--v<version>` タグを打つ。省略と混在させない | 書き忘れると更新が届かない。依存の範囲解決もタグに頼る |
| 依存 | Agent Plugins 側では宣言しない。必要なら Claude 側の `dependencies` だけに書く | Agent Plugins 1.0 は依存を持たない |
| MCP・hooks | 持つ plugin では `mcp.json`（`${PLUGIN_ROOT}`）と `.mcp.json`（`${CLAUDE_PLUGIN_ROOT}`）を二重に持つ。hooks は 1.1 が確定するまで Claude 側だけに置く | ファイル名・形式・プレースホルダが違う |
| CI | `claude plugin validate --strict` に加えて、ルートの `plugin.json` を Agent Plugins の JSON Schema で別途検証する | Claude Code で動いても Agent Plugins に適合しているとは限らない |
| 評価 | 資産ごとに、ありなしの対比較（合格率・トークン・悪化したタスク）と、惜しい非発火例を含む発火テストを置く | 平均の改善だけでは害と崩壊を見逃す |
| 安全と来歴 | スクリプトの同梱は必要なときだけにし、本文は500行より十分短くする。README で sha 固定のインストールを案内し、更新ごとに差分をレビューする。`metadata` に検証日と根拠を残す | 危険パターンのオッズはスクリプト同梱と長さで約2倍になる。修正の伝播は20.9%にとどまる |

この表のうち2つは、未確認の事実に依存している。1つは「Claude Code が Agent Plugins 形式を読まない」という前提で、文書に記載がないことからの推定である。Anthropic が対応を表明すれば、二重の manifest は1つに減らせる。もう1つは、Agent Plugins の公式 validator の有無で、確認していない。スキーマ URL が固定されているので、汎用の JSON Schema 検証で代用できる。権限については、どちらの標準にもハーネスが強制する権限マニフェストがない。現実的なのは、`compatibility` や `metadata` に「呼ぶツール」「ネットワークの要否」を宣言的に書いておくことである。そうすれば IBM の semantic SBOM や AaOS の権限マニフェストが標準化されたとき、そのまま移せる。

## Conclusion

「スキルを OS のように管理する」という問いの答えは、OS の比喩をどの層に当てるかで変わる。読み込みと名前空間はすでに OS 並みに整っている。足りないのはスケジューラ（多数のスキルからの事前選択）と参照モニタ（ハーネスによる権限の強制）で、この2つは2026年後半の研究の主戦場になっている。個人が公開するリポジトリは、どちらも自前では作れない。それでも、ハーネスが自分で選び間違えにくく、利用者が版で固定できる形にすることはできる。具体的には、資産を小さく分け、description の重なりを減らし、版付きの参照で配ることである。これは研究が示した最大の失敗要因（description の干渉と、コピーによる修正の断絶）を、公開側から抑えられる数少ない手段である。

もう1つの示唆として、Agent Plugins と Claude Code の分断は当面続くと見るべきである。「Claude Code で動作確認する」方針は、移植性の検証を兼ねられない。両方の形式を CI で別々に検証することが、このリポジトリが2つの標準のあいだで価値を持つための条件になる。評価については、成功率が保たれていても読み込み率が崩れることが示された。今後は「スキルが使われたか」を測る発火テストを、ありなしの比較と同じ重みで扱う必要がある。
