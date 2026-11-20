# 研究記録の梱包・出来事の表現・決定の記録に関する標準（te への採用候補）

対象設計: `te`（実験1本＝1ディレクトリ。`experiment.toml`、`events.jsonl`、`sources.toml`、`scripts/`、`outputs/`、生成物の `README.md`。規則は `rules.toml`、出来事の形は JSON Schema）。設計文書: plugins リポジトリの `plugins/thought-experiments/docs/te-design.md`（te-design worktree）。

凡例: 「未確認」は、取得したページで確かめられなかった事柄。出典のない推論は各節の「Inferences」に分けた。

## RO-Crate：実験ディレクトリを RO-Crate にできるか、単独利用のファイルツールにとっての費用と利点

### Takeaway
最小の RO-Crate は「ディレクトリ直下に `ro-crate-metadata.json` を1つ置き、ルート（Dataset）に name・description・datePublished・license を書く」だけで成り立つ。そのため te のディレクトリは、構造を変えずに RO-Crate にできる。ただし、毎回それを保守する利点は単独利用では小さい。勧めるのは、`te render` か `te export --ro-crate` が派生物として生成する形にとどめ、正本のデータ（events.jsonl など）は JSON-LD にしないこと。

### Cited Findings
- RO-Crate は、自分自身を説明する RO-Crate Metadata Descriptor を含まなければならない（MUST）。その @id は `ro-crate-metadata.json` で、`about` でルートデータ実体（Root Data Entity）の @id を指す（MUST） — [RO-Crate 1.2 Root Data Entity](https://www.researchobject.org/ro-crate/specification/1.2/root-data-entity.html)
- ルートデータ実体は `@type: Dataset`、`@id`、`name`、`description`、`datePublished`（ISO 8601 の単一文字列）、`license` を持たなければならない（MUST） — [同上](https://www.researchobject.org/ro-crate/specification/1.2/root-data-entity.html)
- Descriptor の `conformsTo` は、版つきの固定 URI（`https://w3id.org/ro/crate/1.2` など）を1つ持つべき（SHOULD）。1.2 では、プロファイルは `conformsTo` ではなくルート側で宣言することを勧める — [同上](https://www.researchobject.org/ro-crate/specification/1.2/root-data-entity.html)
- 仕様サイトのナビゲーションでは、1.3 が最新版として表示されていた（1.3 の差分の中身は未確認） — [同上](https://www.researchobject.org/ro-crate/specification/1.2/root-data-entity.html)
- 来歴は schema.org の Action で表す。ファイルの作成は CreateAction（`instrument`＝道具、`result`＝作られたファイル、`agent`＝責任者）で書く。Dataset 全体への変更は UpdateAction で書く。`endTime` は SHOULD、`startTime` は MAY — [RO-Crate 1.2 Provenance](https://www.researchobject.org/ro-crate/specification/1.2/provenance.html)
- ソフトウェアは `SoftwareApplication`（`version` 付き）として書く。複数の道具をまとめたスクリプトなら、`instrument` は `SoftwareSourceCode` を指すべき — [同上](https://www.researchobject.org/ro-crate/specification/1.2/provenance.html)
- ファイルを訂正するときは古い版を残すべき（SHOULD）。CreateAction の `object` に元の版を、`result` に新しい版を置く — [同上](https://www.researchobject.org/ro-crate/specification/1.2/provenance.html)
- Workflow Run RO-Crate は、計算ワークフローの実行の来歴（入力・出力・コード）を記録するための RO-Crate と schema.org の拡張。プロファイルは Process Run Crate、Workflow Run Crate、Provenance Run Crate の3つ。実装には Galaxy（Workflow, 23.1.1 以降）、Nextflow（nf-prov 1.4.0 以降, Provenance）、Snakemake、StreamFlow、COMPSs、runcrate などがある。論文は Leo et al. 2024, PLoS ONE 19(9): e0309210 — [Workflow Run RO-Crate](https://www.researchobject.org/workflow-run-crate/)
- Quilt は、取得と処理の行為を記録するために Process Run Crate 0.6 を勧めている — [同上](https://www.researchobject.org/workflow-run-crate/)
- 利用分野は生命情報学、デジタル人文学、規制科学など。Zenodo に公開して DOI を付けられる — [About RO-Crate](https://www.researchobject.org/ro-crate/about_ro_crate)
- ro-crate-py は、RO-Crate の作成と読み込みを行う Python ライブラリ（Apache-2.0、Python 3.9 以上、`rocrate` CLI 付き）。RO-Crate 1.3 を既定とし、1.2・1.1・1.0 にも対応する。ディレクトリや zip への書き出しと、metadata だけの detached 形式を扱える — [ro-crate-py](https://github.com/ResearchObject/ro-crate-py)
- 仕様文書のライセンスは、取得したページに書かれていなかった（「© 2021-2024 University of Technology Sydney, The University of Manchester UK and RO-Crate contributors」の表記だけ）。**未確認** — [About RO-Crate](https://www.researchobject.org/ro-crate/about_ro_crate)

### Inferences
- te の要素との対応。`experiment.toml` の問いと開始日はルートの name・description・datePublished になる。`sources.toml` の項目は文脈実体（CreativeWork など、URL を @id とする）になる。`scripts/` は SoftwareSourceCode に、`te run` の1回は CreateAction（`instrument`＝スクリプト、`result`＝outputs の JSON）になる。これは Process Run Crate の型に近い。
- 単独利用のファイルツールでの費用。JSON-LD の @context と @graph は、標準ライブラリだけの te.py でも書けるが、人が読む・手で直す対象としては重い。正本にすると二重管理になる。license が MUST なのも、私的な思考実験には余計な欄になる。
- 利点が出るのは、実験を Zenodo などに公開して DOI を付けるとき、または WorkflowHub 系の道具に渡すときだけ。したがって「派生物として生成し、正本にはしない」のが費用対効果の釣り合う線である。te の「README.md は生成物」という方針と同じ扱いになる。
- `sha256` と URL を持つ sources.toml は、RO-Crate の Web 上のデータ実体（@id が URL）にそのまま写せる。sha256 の入れ先（schema.org の欄名）は未確認。

### Gaps
- RO-Crate 1.3 の変更点と、仕様文書のライセンス（CC-BY 系と思われるが確認できていない）。
- rocrate-validator の有無と使い方は、取得したページでは確認できなかった。
- Process Run Crate 0.6 の必須項目の細部は、未取得。

## CloudEvents：te の出来事の外枠（エンベロープ）として使えるか

### Takeaway
CloudEvents 1.0 は CNCF の Graduated 仕様で、必須の属性は `id`・`source`・`specversion`・`type` の4つだけと軽い。それでも te の外枠にそのまま採る必要は薄い。システム間の配送を前提にした語彙（source は URI、data の入れ子、属性名は英小文字と数字だけ）が、1ファイルに追記する te の記録では冗長になるからである。勧めるのは、te 独自の短い外枠（`id`・`at`・`kind`・`by`・`v`）を保ち、意味を CloudEvents に合わせておくこと。必要になったら、機械的に変換できる対応表を設計文書に1つ書けば足りる。

### Cited Findings
- 必須の属性は `id`、`source`、`specversion`、`type`。任意の属性は `datacontenttype`、`dataschema`、`subject`、`time` — [CloudEvents spec](https://raw.githubusercontent.com/cloudevents/spec/main/cloudevents/spec.md)
- 「Producers MUST ensure that `source` + `id` is unique for each distinct event.」同じ `id` での再送は重複と見なしてよい — [CloudEvents spec](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md)
- `specversion` には `1.0` を使わなければならない。文書自体の版表記は 1.0.3-wip — [同上](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md)
- `source` は空でない URI-reference（絶対 URI を推奨）。`type` は推奨として逆 DNS の接頭辞を付ける。`time` は RFC 3339。`subject` は source の文脈での対象。`dataschema` は data が従うスキーマの URI — [CloudEvents spec (raw)](https://raw.githubusercontent.com/cloudevents/spec/main/cloudevents/spec.md)
- 属性名は ASCII の英小文字 [a-z] と数字 [0-9] だけでなければならない（MUST）。20文字以下を推奨し、`data` は使えない — [同上](https://raw.githubusercontent.com/cloudevents/spec/main/cloudevents/spec.md)
- JSON 形式では、JSON の内容は `data` に JSON の値として直接入れる。バイナリは `data_base64` に入れる。拡張属性はトップレベルに置く。媒体型は単体が `application/cloudevents+json`、配列のバッチが `application/cloudevents-batch+json` — [JSON Event Format](https://github.com/cloudevents/spec/blob/main/cloudevents/formats/json-format.md)
- すべての実装は JSON 形式に対応しなければならない — [CloudEvents spec](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md)
- CNCF への受け入れは 2018-05-15、Incubating は 2019-10-24、Graduated は 2024-01-25。SDK は9言語ある。CNCF 内では Argo、Falco、Harbor、Knative、Serverless Workflow が使っている（検索結果の要約による） — [CNCF announcement](https://cncf.io/announcements/2024/01/25/cloud-native-computing-foundation-announces-the-graduation-of-cloudevents); [cloudevents.io blog](https://cloudevents.io/blog/2024-01-25/)
- 仕様が想定する用途（配送か保存か）は、明示されていない。source から destination への移動を記述し、形式は「storage medium」に依らないと書くだけ — [CloudEvents spec (raw)](https://raw.githubusercontent.com/cloudevents/spec/main/cloudevents/spec.md)
- 仕様文書のライセンスは、取得したページに書かれていなかった。**未確認**（GitHub リポジトリは Apache-2.0 と思われるが確かめていない） — [CloudEvents spec (raw)](https://raw.githubusercontent.com/cloudevents/spec/main/cloudevents/spec.md)

### Inferences
- 対応表の案（te → CloudEvents）は次のとおり。
  | te の欄 | CloudEvents | 注 |
  | --- | --- | --- |
  | `id`（連番） | `id` | source 内で一意。連番で足りる |
  | ディレクトリ（実験 id） | `source` | `te:experiments/<slug>` のような URI-reference |
  | `kind` | `type` | 逆 DNS の接頭辞を付けるなら `io.github.ryo-morimoto.te.frame` |
  | `at` | `time` | RFC 3339 にそろえる |
  | スキーマの版 | `dataschema` | `schema.json` の版つき URI |
  | `correction.target` | `subject` か拡張属性 | 対象の出来事 id |
  | `kind` 固有の欄 | `data` | CloudEvents では入れ子になる |
- `by` に相当する標準の属性はない。拡張属性の `by` は名前の規則（英小文字と数字）を満たすが、値の `reviewer:<lens>` は拡張属性の値として自由に使える。
- 準拠すると、各行に `specversion` と `source` が繰り返され、固有の欄が `data` の下に1段下がる。手で読む・`jq` で扱うときに見にくくなり、その代わりに得るのは「将来どこかへ配送する」可能性だけである。単独のファイルツールでは、得るものが小さい。
- 採るべきは、CloudEvents が示す設計判断のほう。(1) 外枠と本体を分ける。(2) id の一意性の範囲を定義する（te では「実験ディレクトリ内で一意」）。(3) 時刻を RFC 3339 にする。(4) スキーマの版を出来事に書く（`dataschema` 相当）。

### Gaps
- CloudEvents をファイルへの永続化（イベントストア）に使う公式の推奨や事例は、見つけていない。
- 仕様のライセンスは確認できていない。

## イベントソーシングの実践と JSON Lines：追記だけ、スナップショット、スキーマの進化、補償の出来事

### Takeaway
te の「追記だけ・畳み込みで状態を求める・訂正は新しい出来事」は、Fowler の Event Sourcing と同じ形である。実務で最も問題になるのはスキーマの進化で、業界調査では「最初は版つきの出来事と弱いスキーマで始め、必要になったら upcasting に進む」のが勧められている。te では、各出来事に `v`（スキーマの版）を入れ、`fold` の手前で古い版を新しい版に読み替える純粋関数（upcaster）を置くのが筋である。保存形式は JSON Lines が追記と1行1出来事の差分に合い、TOML の配列より向いている。

### Cited Findings
- Fowler の定義は「Capture all changes to an application state as a sequence of events.」。出来事の記録は、問い合わせ、過去の状態の再構築、履歴の訂正に使える — [Fowler, Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- 毎回はじめから再計算すると遅いので、現在の状態をスナップショットとして保持するのがふつうである。状態は記録から導けるので、どこにキャッシュしてもよい。「New snapshots can be made at any time in parallel without bringing down the running application.」 — [同上](https://martinfowler.com/eaaDev/EventSourcing.html)
- 取り消し（reversal）は、出来事が差分（+10）を記録していれば簡単で、値の上書き（110 にする）なら前の値を出来事に持たせる必要がある。「reversal is never absolutely needed for functionality」で、スナップショットからの再生でも同じ結果になる — [同上](https://martinfowler.com/eaaDev/EventSourcing.html)
- 外部への問い合わせは、再生のときに結果が変わりうる。対策は (1) 外部系に過去の値を問い合わせる、(2) 出来事の協調の履歴に頼る、(3) ゲートウェイで応答を記録し、再生でそれを使う、の3つ — [同上](https://martinfowler.com/eaaDev/EventSourcing.html)
- コードの変更は3種類ある。新機能は再処理で取り込める。バグ修正はコードを直して再処理するが、外部への副作用が難しい。時間に依存する規則は domain model に置く。bitemporal は「can get very messy」 — [同上](https://martinfowler.com/eaaDev/EventSourcing.html)
- Greg Young の『Versioning in an Event Sourced System』の目次には、「Why can't I update an event?」（Immutability, Consumers, Audit, Worms, Crime）、Weak Schema（Mapping, Wrapper）、Negotiation、Copy and Replace、Versioning Process Managers の「Upcasting State」などの章がある。本文は未取得のため、主張の細部は**未確認** — [Leanpub 目次](https://leanpub.com/esversioning/read)
- Overeem ら（JSS 2021）は、技術者25人への聞き取りで19のイベントソーシングの系を調べた。系を更新する戦術として、versioned events、weak schema、upcasting、in-place transformation、copy-and-transform の5つを挙げた。最初は versioned events と weak schema で始め、のちに upcasting や copy-and-transform に進むことを勧めている — [arXiv:2104.01146](https://arxiv.org/abs/2104.01146)（検索結果の要約による。本文は未読）
- InfoQ の報道によると、copy-transform が最も使われた手法だった。「出来事は決して変えない」と言う人は多かったが、実際にそれを守っていた人はほとんどいなかった — [InfoQ 2018](https://www.infoq.com/news/2018/02/evolving-cqrs-event-sourcing/)（検索結果の要約による）
- 前の論文は Overeem, Spoor, Jansen, Brinkkemper「The dark side of event sourcing: Managing data conversion」（SANER 2017）。イベントストアの更新操作と更新の枠組みを提案した — [Crossref](https://api.crossref.org/works/10.1109%2FSANER.2017.7884621)（検索結果の要約による）
- JSON Lines の要件は3つ。UTF-8、1行が1つの妥当な JSON の値、行区切りは `\n`（`\r\n` も可）。拡張子は `.jsonl`。媒体型 `application/jsonl` は提案だが「not yet standardized」。用途として、ログファイル、プロセス間のメッセージ、Unix のテキスト処理とパイプラインを挙げる — [jsonlines.org](https://jsonlines.org/)

### Inferences
- JSON Lines か TOML の配列か（設計文書 §9 の未決事項）。結論は JSON Lines。理由は4つある。(1) 追記が「1行を末尾に足す」だけで済み、パースし直さなくてよい。TOML の `[[event]]` 表でも追記はできるが、入れ子の表（`premises` の配列など）を含むと1出来事が複数行に広がり、差分が読みにくい。(2) git の差分は、1出来事が1行の追加として見える。(3) 1行ずつ読めるので、壊れた末尾行（書き込み途中での中断）を検出して捨てられる。(4) `jq` や `grep` でそのまま扱える。人が読む頻度の高い面は `README.md`（生成物）が受け持つので、JSON の読みにくさは問題になりにくい。
- 欠点は、`note` の長い Markdown が1行の JSON 文字列（`\n` のエスケープ）になって読みにくいこと。対策は2つある。`note` を `notes/<id>.md` に分けて出来事からパスで参照するか、長さに上限を設ける（§9 の `note` 上限の論点と関係する）。
- スキーマの進化。各出来事に `v`（出来事のスキーマの版）を書き、`fold` の前に `upcast(event) -> event` を純粋関数として挟む。これは Overeem らの「versioned events」から「upcasting」への順路と一致し、データ指向の方針（コードとデータを分ける）とも合う。copy-and-transform（記録を書き換えて移行する）は、追記だけの約束を破るので、「既存の Markdown の記録を移す」一回だけの移行にとどめる。
- 訂正は、Fowler の reversal の考え方どおり、対象 id を持つ `correction` を足す。値を上書きする種類の出来事（`conclusion` など）は、`fold` が「同じ対象への後の出来事が勝つ」規則で反映すればよい。前の値を出来事に持たせる必要はない。記録は消えないので、取り消しの情報は記録自体にある。
- スナップショットは、単独利用で1実験に数十〜数百行の規模なら不要。毎回の `fold` で足りる（規模の見積もりは推論）。
- 外部への問い合わせの問題（再生で結果が変わる）は、`te source add` が sha256 と取得日を記録することで、Fowler の (3)「応答を記録して再生に使う」に当たる。`te check` が URL を取り直して照合するなら、差分を「外部が変わった」として、記録の誤りとは区別して報告すべきである。

### Gaps
- Greg Young の書籍の本文（weak schema、negotiation の具体的な主張）は取得できなかった。
- Overeem ら（2021）の本文の数値（各戦術の使用件数）は未読で、検索結果の要約に頼っている。

## アーキテクチャ決定記録（ADR）：MADR、Nygard、Y-statement、道具と、te の conclusion / options / decision への写像

### Takeaway
ADR の要素（文脈、決定の要因、考えた選択肢、選択肢ごとの長所と短所、結果、帰結、状態と置き換え）は、te の `frame` / `rival` / `operation` / `conclusion.options` / `decision` / `correction` に、ほぼそのまま対応する。te が ADR の形式で記録する必要はない。勧めるのは、`te render` が README に MADR に近い節の並びを出すこと、`conclusion.options` に MADR の「pros/cons」と Nygard の「consequences（良いものも悪いものも全部）」に当たる欄を持たせること、そして置き換えを `supersedes` の参照で表すことの3つ。

### Cited Findings
- ADR は「captures a single AD and its rationale」。AD は「a justified design choice that addresses a functional or non-functional requirement that is architecturally significant」。1つのプロジェクトの ADR の集まりが decision log になる — [adr.github.io](https://adr.github.io/)
- Nygard（2011）の節は Title（短い名詞句）、Context（「value-neutral」に力関係を書く）、Decision（「We will …」）、Status、Consequences（「All consequences should be listed here, not just the "positive" ones.」） — [Nygard, Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- Nygard の状態は proposed、accepted、deprecated / superseded。「If a decision is reversed, we will keep the old one around, but mark it as superseded.」「Numbers will not be reused.」 — [同上](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- MADR 4.0.0（2024-09-17）の完全な雛形は次の節からなる。Title、Context and Problem Statement、Decision Drivers（任意）、Considered Options、Decision Outcome（任意の Consequences と Confirmation）、Pros and Cons of the Options（任意）、More Information（任意）。front matter は status、date、decision-makers、consulted、informed（すべて任意）。ライセンスは「MIT OR CC0-1.0」 — [MADR](https://adr.github.io/madr/)
- Y-statement は、文脈（ユースケースか部品）、懸念（品質の要求）、選んだ選択肢、退けた選択肢、目指す品質、受け入れる短所の6つを、1文につなげる形式。Zimmermann によるもので、Fairbanks の Architecture Haikus を下敷きにし、Zdun ら『Sustainable Architectural Decisions』が出典とされる。最も簡潔な ADR の形式で、可逆で局所的な決定に向く — [Zimmermann, Y-Statements](https://medium.com/olzzio/y-statements-10eb07b5a177); [adr.github.io](https://adr.github.io/)（いずれも検索結果の要約による。雛形の文言そのものは未取得）
- WICSA 2015 の論文が、7つの雛形を比べている（雛形の名前はページに書かれていなかった） — [adr.github.io](https://adr.github.io/)
- 道具には次のものがある。adr-tools（「bash scripts to manage ADRs in the Nygard format」）、log4brains（ADR を見やすく表示し、CLI で作成する）、ADG（Go 製。Nygard・MADR・QOC の雛形）、adr-viewer（Python。ADR から Web サイトを生成）、pyadr（提案・承認・却下・廃止・置き換えのライフサイクル用 CLI）、adr-log（MADR から決定ログを生成。保守終了） — [ADR Tooling](https://adr.github.io/adr-tooling/)

### Inferences
- 写像の案（ADR の要素 → te）は次のとおり。
<!-- data-source: original（調査担当による整理） -->
  | ADR の要素 | te の出来事・欄 |
  | --- | --- |
  | Title / Context and Problem Statement | `experiment.toml` の問いとゴール、`frame.terms` |
  | Decision Drivers | `frame` の価値の確認、ゴール（誰のどの判断） |
  | Considered Options | `rival`（`rid`、`text`、`is_opposite`） |
  | Pros and Cons of the Options | `operation.favours` / `eliminates`、`attack.objections` |
  | Decision Outcome | `conclusion.answer` と `options[].status` / `reason` |
  | Consequences（良いものも悪いものも） | `conclusion` に欠けている。`consequences` か「受け入れる短所」の欄を足す候補 |
  | Confirmation | `te check`（規則と scripts の再実行） |
  | Status / superseded | `close.state`、`correction.target`（置き換え） |
  | decision-makers / consulted | `by`、`decision`（利用者が選んだこと）、`attack.by=fresh` |
- te に欠けているのは2点。(1) Nygard と Y-statement が要求する「受け入れる短所（accepting that …）」を、結論の必須の欄にしていない。(2) 結論を後から覆すときの `supersedes`（置き換え）の関係。`correction` は誤りの訂正であり、方針の変更とは意味が違う。Nygard は、この2つを「superseded」として区別している。
- Y-statement の1文は、`te render` が返答の骨組みの「結論の1行要約」として生成する雛形に向く。欄は `conclusion` の中身からすべて埋まる。
- adr-tools や log4brains を te が使う必要はない。ただし「CLI だけが書く、番号を再利用しない、置き換えた記録を消さない」という運用の約束は、te の `te add` だけが書く方針と同じである。

### Gaps
- Y-statement の雛形の文言そのものを、一次資料（Zdun ら, IEEE Software 2013）で確認していない。
- MADR の Confirmation の節の詳しい説明は、未取得。

## スキーマの記述：JSON Schema 2020-12 と代替（CUE、TOML のスキーマ）、Frictionless Data Package、OSF の雛形、W3C PROV への写像

### Takeaway
出来事の形の検査には、JSON Schema 2020-12 が現実的な選択である。現行版で、TOML を読んだ辞書にも JSON Lines の各行にも同じスキーマを当てられる。ただし te.py は標準ライブラリだけで書くので、検証器は同梱しない。te は「スキーマを正本として持ち、te.py は使う部分（type、required、enum、properties、additionalProperties）だけを小さく検査する」のが釣り合う。CUE は JSON Schema と相互に変換できるが、Go の道具が必要になり、標準ライブラリだけの方針に合わない。Frictionless Data Package と OSF の雛形は、te のディレクトリ構造の参考になる程度で、採るほどの利点はない。W3C PROV は、出来事の意味を説明するための写像として、設計文書に1節書く程度が適当である。

### Cited Findings
- JSON Schema の現行版は 2020-12（前の版は 2019-09） — [json-schema.org/specification](https://json-schema.org/specification)
- JSON Schema は、このページでは IETF の RFC とは書かれていない。安定性の方針の記述もない。ライセンスはページに書かれておらず、「Copyright © 2026 JSON Schema. All rights reserved.」の表記だけ。**未確認** — [同上](https://json-schema.org/specification)
- CUE は JSON Schema に「first class support」を持つ。`cue import` で JSON Schema を CUE に、`cue def --out jsonschema` で CUE から JSON Schema に変換でき、`cue vet` でデータを JSON Schema に照らして検査できる。ページの例は JSON のデータだけで、Python のライブラリには触れていない — [CUE and JSON Schema](https://cuelang.org/docs/concept/how-cue-works-with-json-schema/)
- Data Package v2 では、ディレクトリ形式なら記述子を最上位の `datapackage.json` に置かなければならない（MUST）。必須の欄は `resources`（1件以上）だけで、`name`、`id`、`licenses`、`profile` は推奨。`$schema` で `https://datapackage.org/profiles/2.0/datapackage.json` を指す。著者は Pollock、Walsh、Kariv、Karev、Desmet と Data Package Working Group — [Data Package v2](https://datapackage.org/standard/data-package/)
- OSF には、COS が定める唯一のフォルダ構造は見つからなかった。雛形は研究室や共同体が作ったもので、雛形からプロジェクトを作ると、部品と題だけを受け継いで中身は受け継がない — [OSF Help: Creating a Project](https://help.osf.io/article/383-creating-a-project)（検索結果の要約による）
- 心理学の透明性ガイド（ケルン大学）は、Project TIER の DRESS Protocol に倣ったフォルダ構成を示す。最上位に readme を置き、生データは「rawest」の形で置く — [Psych Transparency Guide: Folder structure](https://psych-transparency-guide.uni-koeln.de/folder-structure.html)（検索結果の要約による）
- PROV-O は W3C 勧告（2013-04-30）。起点のクラスは Entity、Activity、Agent。起点の性質は wasGeneratedBy、used、wasAssociatedWith、wasDerivedFrom、wasAttributedTo、startedAtTime。拡張の性質に wasRevisionOf（wasDerivedFrom の下位）と wasInvalidatedBy がある — [W3C PROV-O](https://www.w3.org/TR/prov-o/)

### Inferences
- PROV への写像（説明用）は次のとおり。各出来事は Activity で、`by` は wasAssociatedWith の Agent。`sources` の各資料は、その Activity が used した Entity。`te run` の outputs は wasGeneratedBy で作られた Entity。`conclusion` は、前提（`premises`）から wasDerivedFrom で導かれる Entity。`correction` は、対象を wasInvalidatedBy で無効にし、新しい値を wasRevisionOf でつなぐ。RO-Crate の CreateAction（object → result）と同じ骨組みなので、RO-Crate を出力するときにもこの写像を再利用できる。
- JSON Schema の検査を te.py に自作すると、2020-12 の全機能（`$ref`、`if/then`、`unevaluatedProperties` など）は扱えない。スキーマ側で使ってよいキーワードを限るか、CI だけ `check-jsonschema` などの外部の検証器で全体を検査する二段構えにする（外部の道具の名前は本調査で確認していない）。
- 各出来事にスキーマの版を書くこと（前の節の `v`）と、JSON Schema の `$id` に版を入れることをそろえれば、CloudEvents の `dataschema` と同じ役割を果たせる。
- Data Package は、表形式のデータ資源の記述が中心である。te の outputs（JSON）や sources（URL と sha256）は表ではないので、採る価値は低い。sources.toml の欄名（`path`、`hash` など）を合わせる程度にとどめる（Data Resource の欄の定義は未取得）。
- OSF の雛形と TIER の構成から te が学べるのは、「最上位に README、生のデータと派生物を分ける」という原則だけ。te はすでに、正本（events.jsonl、sources.toml、scripts）と派生物（outputs、README.md）を分けている。

### Gaps
- JSON Schema の公式なライセンスと、2020-12 の次の版の予定は確認できなかった。
- Data Resource 仕様の `hash` 欄の書式（アルゴリズムの接頭辞の有無）は未取得。
- TOML 用のスキーマ標準（Taplo の JSON Schema 対応など）は調べていない。TOML は読み込めば辞書になるので、JSON Schema を当てられる（推論）。
- CI が te.py をどう入手するか（§9）に直接答える標準は、見つからなかった。RO-Crate の `SoftwareApplication`（`version` 付き）で、使った te.py の版を記録する案はありうる（推論）。
