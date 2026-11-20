# 論証と対立仮説を表す標準構造（te への採用候補）

対象: `te` の設計（`plugins/thought-experiments/docs/te-design.md`）の出来事 `frame` / `rival` / `probe`・`operation` / `attack` / `conclusion` / `correction` に、既存の標準をどう対応させるか。調査日 2026-11-21。GitHub の数値は `gh api` で同日に取得した。

## Toulmin モデル（claim, data, warrant, backing, qualifier, rebuttal）と te の前提・結論

### Takeaway
Toulmin の6要素のうち、te にないのは **warrant（推論の許可）を前提と別に持つ欄**と **qualifier（結論の強さ）**。rebuttal は「warrant の例外」と読むのが形式論証での標準的な解釈で、te の `attack` は前提を攻撃する欄しかないため、warrant への攻撃（undercut）を表せない。

### Cited Findings
- Toulmin の図式は Data・Claim・Qualifier・Warrant・Backing・Rebuttal を分ける。warrant は推論の許可、backing は warrant の裏付け、rebuttal は warrant による結論の例外を述べる — [Verheij, Toulmin 章 2009](https://www.ai.rug.nl/~verheij/publications/pdf/toulmin2009.pdf)
- qualifier は warrant が結論に与える力の程度を示す（「必然的に」など） — [Verheij 2009](https://www.ai.rug.nl/~verheij/publications/pdf/toulmin2009.pdf)、[ICAR Dicoplantin: Layout of Argument](https://icar.cnrs.fr/dicoplantin/layout-of-argument-toulmin-e/)
- Bex と Prakken は「necessarily」「certainly」の qualifier は演繹、それ以外は defeasible と読み、Toulmin の rebuttal を Pollock の意味での undercutter（推論への攻撃）と解釈している — [Prakken ほか COMMA 2026 論文](https://webspace.science.uu.nl/~prakk101/pubs/comma26TAL.pdf)（検索要約経由。本文の該当箇所は未確認）
- 学生向け教材では rebuttal を「反論一般」の意味で使い、undercut と rebut を区別しない — [UTSA Toulmin Model](https://www.utsa.edu/twc/documents/Toulmin_Model_of_Argumentation.pdf)
- SEP「Informal Logic」は Toulmin を歴史上の基準点として挙げるだけで、6要素の定義はしていない — [SEP: Informal Logic](https://plato.stanford.edu/entries/logic-informal/)

### Inferences
- 対応案: claim → `conclusion.answer`、data → `conclusion.premises`（`label` が `empirical-*`）、backing → `sources` / `outputs`、qualifier → 結論の確信度（今は `prediction.confidence` にしかない）、rebuttal → `attack.objections`。
- warrant に当たるのは te の `label: argued` や `definitional` の前提だが、「どの前提から結論を出す規則か」は区別されていない。premises に `role: datum | warrant` を足すと、undercut（warrant への攻撃）を `objections.premise` で指せるようになる。
- 形式として採用する価値は低い（スキーマも仕様もない、概念の型）。語彙の参照先にとどめるのがよい。

### Gaps
- Toulmin『The Uses of Argument』原典の該当頁は確認していない。

## IBIS（issue, position, argument）と Compendium・gIBIS

### Takeaway
IBIS の3種のノードは te の「問い（experiment.toml）→ rival → probe/operation の favours/eliminates」とほぼ一対一に対応する。ただしツール（Compendium）は 2014 年で更新が止まっており、形式として取り込むものはない。

### Cited Findings
- IBIS は Kunz と Rittel が考案した。原典は 1970 年7月の working paper「Issues as elements of information systems」（UC Berkeley） — [Wikipedia: Issue-based information system](https://en.wikipedia.org/wiki/Issue-based_information_system)
- IBIS はソフトウェアではなく記法で、issue・position・argument の3種のノードを使う。1つの issue に、それを解く代替の position が複数つく — [Wikipedia: IBIS](https://en.wikipedia.org/wiki/Issue-based_information_system)、[Wikipedia: Design rationale](https://en.wikipedia.org/wiki/Design_rationale)
- gIBIS は Begeman と Conklin によるグラフィカル版で、Sun ワークステーションで動いた（1987 年ごろ） — [Wikipedia: IBIS](https://en.wikipedia.org/wiki/Issue-based_information_system)
- Compendium は IBIS を実装したソフトの1つで、無料・オープンソースの Java デスクトップアプリ。最後のリリースは 2.1.3（2014-01-21） — [Wikipedia: Compendium (software)](https://www.wikiwand.com/en/articles/Compendium_(software))（ミラー経由）、[UTS CIC: Knowledge cartography](https://cic.uts.edu.au/tools/knowledge-cartography/)

### Inferences
- 対応: issue → `experiment.toml` の問い（分岐した下位の問いは `branch`）、position → `rival`、argument（pro/con） → `operation` の `favours` / `eliminates`。
- IBIS には「対立仮説を消す」概念（elimination）も「反対の命題を必ず置く」規則もない。te の `rival.is_opposite` と `eliminates` は IBIS より強い。
- 採用するなら語彙だけ。地図（maps/）の「問いの木」には IBIS の issue の入れ子が合う。

### Gaps
- Compendium のライセンス名（LGPL など）と、後継の Compendium-NG の現状は確認できなかった（GitHub の `Compendium-NG/compendium` は 404）。

## AIF（Argument Interchange Format）、AIFdb、OVA

### Takeaway
AIF は「命題（I-node）と、命題どうしの関係を必ず中間ノード（推論 RA・衝突 CA・選好 PA）で表す」グラフの抽象オントロジー。te の `operation` が rival に `eliminates` / `favours` を付ける形は、AIF の「関係を型つきの中間ノードで明示する」原則と同じ発想なので、保存形式として採用するより、`te render` の書き出し先（交換形式）として扱うのが妥当。

### Cited Findings
- AIF の原典は Chesñevar ほか「Towards an Argument Interchange Format」Knowledge Engineering Review 21:293–316, 2006 — [AIF Specification (Dundee, 2011) の参考文献](https://arg-tech.org/wp-content/uploads/2011/09/aif-spec.pdf)
- AIF の目的は、論証ツール間の交換と共通のコアオントロジーで、ASPIC+、Description Logic 形式、Rationale の形式などの間の「中間言語」になること — [AIF Specification 2011](https://arg-tech.org/wp-content/uploads/2011/09/aif-spec.pdf)
- ノードは I-node（情報）と S-node（scheme の適用）。S-node は RA-node（推論）、CA-node（衝突）、PA-node（選好）。グラフの辺は E ⊆ V×V \ I×I で、I-node どうしを直接つなげない。関係の理由を表す scheme を必ず介す — [AIF Specification 2011](https://arg-tech.org/wp-content/uploads/2011/09/aif-spec.pdf)
- 衝突 scheme は「conflicting element」と「conflicted element」を持ち、対称性は仮定しない（対称な衝突は2回適用する）。例: 「専門家が信頼できない」は Expert Opinion の推論（RA-node）を攻撃する — [AIF Specification 2011](https://arg-tech.org/wp-content/uploads/2011/09/aif-spec.pdf)
- scheme は Forms Ontology（F-node）で定義し、premise・conclusion・exception の記述子を持つ。データベース形式は nodes（nodeID, text, type）と edges（edgeID, fromID, toID）の表などで表す。AIF-DL は RDF/XML、OWL/XML などで提供される — [AIF Specification 2011](https://arg-tech.org/wp-content/uploads/2011/09/aif-spec.pdf)
- OVA3 の GitHub リポジトリ（arg-tech/ova3）は archived、ライセンス表示なし、最終 push 2025-05-22 — [GitHub: arg-tech/ova3](https://github.com/arg-tech/ova3)

### Inferences
- 対応: I-node → `rival.text`、`premises.text`、`operation.result`。RA-node → `operation`（varied と result から rival を支持する推論）。CA-node → `operation.eliminates` と `attack.objections`。PA-node → te には直接の対応なし（BA 型の判定を入れるなら必要）。
- AIF の「I-node 同士を直接つながない」は、te で「rival を消すときは必ずどの operation で消したかを残す」という不変条件（`eliminates` は operation の欄としてだけ書ける）と同じ。te の今の形はこれを満たしている。
- 保存形式に採用しない理由: AIF は RDF/OWL 系で、te の「標準ライブラリだけ・辞書とリスト」の方針と重い。`te render --format aif-json` のような片方向の書き出しで十分。

### Gaps
- AIFdb の現行 JSON 形式（nodes/edges/locutions）の仕様文書と、AIFdb サービスの稼働状況は確認していない（未検証）。
- OVA の現行版（OVA+ / OVA3 のウェブ版）の公開状況とライセンスは未確認。

## Carneades（論証評価と proof standard）

### Takeaway
Carneades の要点は「命題ごとに証明基準（proof standard）を割り当て、pro と con の論証から受理を計算する」ことと、「前提を ordinary / assumption / exception の3種に分ける」こと。te の `conclusion.options.status`（生き残り・脱落）を手で書く代わりに、基準を欄として持って `fold` で計算する案の根拠になる。

### Cited Findings
- 原典は Gordon, Prakken, Walton「The Carneades model of argument and burden of proof」Artificial Intelligence 171(10-11):875–896, 2007 — [著者版 PDF](https://tfgordon.github.io/publications/GordonPrakkenWalton2007b.pdf)
- 前提は ordinary premise・assumption・exception の3種で、命題の対話上の状態（stated, questioned, accepted, rejected）を使う。critical question は追加の前提（assumption か exception）として表す — [Gordon ほか 2007](https://tfgordon.github.io/publications/GordonPrakkenWalton2007b.pdf)
- proof standard の定義: SE（Scintilla of Evidence）＝少なくとも1つの defensible な pro 論証がある。BA（Best Argument）＝ある defensible な pro 論証が、すべての defensible な con 論証より優先する。DV（Dialectical Validity）＝defensible な pro 論証が1つ以上あり、con 論証はどれも defensible でない。強さは DV > BA > SE — [Gordon ほか 2007](https://tfgordon.github.io/publications/GordonPrakkenWalton2007b.pdf)
- pro と con を入れ替えた「補集合の基準」も定義でき、弱い基準では命題とその補集合が両方満たされうる（受理と真理の違い） — [Gordon ほか 2007](https://tfgordon.github.io/publications/GordonPrakkenWalton2007b.pdf)
- 対話の段階によって基準を変えてよい（ブレインストーミングでは弱い基準） — [Gordon ほか 2007](https://tfgordon.github.io/publications/GordonPrakkenWalton2007b.pdf)
- 実装: carneades/carneades-4（Go）は LICENSE が Mozilla Public License 2.0、最終 push 2024-10-15、star 68。旧版 carneades/carneades は最終 push 2019-10-17 — [GitHub: carneades-4](https://github.com/carneades/carneades-4)、[GitHub: carneades](https://github.com/carneades/carneades)

### Inferences
- 対応: te の `options.status` を、rival ごとの `standard`（SE / BA / DV）と、`favours`（pro）・`eliminates` と未回答の `objections`（con）から `fold` で計算できる。DV は「生き残った con が1つもない」で、te の「脱落」の判定に最も近い。
- 前提の種類は te の `label`（証拠の確かさ）と直交する別の軸。`assumption`（反証がなければ置く）と `exception`（出されたら崩す）を区別すると、`attack` の「bar」（例外として除く）と対応がつく。
- コードの採用は不要（Go、MPL-2.0、2024 以降更新なし）。定義（3つの基準）だけを `rules.toml` の述語にするのがよい。

### Gaps
- Carneades 4 の入力形式（YAML の論証グラフ）の現行仕様は未確認。

## Argdown（Markdown 風の論証記法）

### Takeaway
Argdown は MIT ライセンスで 2026 年も保守されている唯一の候補。support（`+`）・attack（`-`）・undercut（`_`）を区別でき、YAML のメタデータを命題に付けられる。te の保存形式にはしないが、`te render` の書き出し先（論証マップの可視化）として最も現実的。

### Cited Findings
- 文書は statement と argument のブロックからなる。`[Title]: text` が命題（同じ題は同値類）、`<Title>: ...` が論証。番号付きの前提と横線で premise-conclusion structure を書く — [Argdown Syntax](https://argdown.org/syntax/)
- 関係は `+`（支持）・`-`（攻撃）・`_`（undercut）、strict モードでは `><`（矛盾）。`<` `>` で向きを指定する。`{key: value}` で YAML メタデータを付けられる。JSON 書き出しでは関係に `relationType` が付く — [Argdown Syntax](https://argdown.org/syntax/)
- ライセンス: README に「All code is published under the MIT license」。GitHub の API ではライセンス未検出（リポジトリ直下に LICENSE ファイルがない）。npm `@argdown/core` は license MIT、最新版 2.0.1（2026-04-28 更新） — [GitHub: christianvoigt/argdown README](https://github.com/christianvoigt/argdown)、[npm: @argdown/core](https://www.npmjs.com/package/@argdown/core)
- 保守: 最終 push 2026-11-12、最終コミット 2026-05-20、star 1058、archived でない。開発資金は KIT の DebateLab — [GitHub: christianvoigt/argdown](https://github.com/christianvoigt/argdown)

### Inferences
- 対応: `rival` → statement、`operation` → argument（前提＝固定した条件と varied、結論＝result）、`favours` → `+>`、`eliminates` → `->`、前提への objection → 前提の statement への `-`、推論への objection → `_`。`label` や `sources` は `{label: empirical-checked}` の YAML で持てる。
- `te render --argdown` を足せば、VS Code 拡張などの既存の可視化をそのまま使える。保存は events.jsonl のまま（Argdown は追記の出来事列ではなく、現在の状態の表現なので）。
- Node.js が要るのは描画側だけで、te.py（標準ライブラリだけ）の方針とは衝突しない。

### Gaps
- Argdown の JSON 書き出しの完全なスキーマ、graphml などの他形式は確認していない。

## Kialo、DebateGraph

### Takeaway
どちらも利用者向けのサービスで、公開された交換形式は確認できなかった。te の採用候補にはならない。

### Cited Findings
- Kialo は稼働中のオンライン構造化討論サービスで、論証マップを討論の木（pro/con）で表す。教室向けの Kialo Edu がある — [Wikipedia: Kialo](https://en.wikipedia.org/wiki/Kialo)

### Inferences
- Kialo の pro/con の木は、1つの主張を根にする形で、複数の rival を並べて消していく te の構造には合わない。

### Gaps
- Kialo の書き出し機能の仕様、DebateGraph の現状（稼働しているか）は、信頼できる情報源を見つけられなかった（未検証）。

## ACH（Heuer の対立仮説の分析）と Structured Analytic Techniques

### Takeaway
ACH の「仮説×証拠の行列」「診断性（すべての仮説と整合する証拠は価値がない）」「反証の少ない仮説を残す」「少数の要の証拠への感度分析」は、te の `rival` × `operation`、`eliminates`、`attack` にそのまま対応し、`te check` の検査にできる。ただし実験的な評価では、ACH を使っても確証バイアスが減るとは言えず、判断の不整合や誤差を増やしうるという結果が出ている。

### Cited Findings
- ACH の8段階: (1) 仮説を挙げる（異なる視点の集団で） (2) 各仮説に対する証拠と論拠を列挙 (3) 仮説を横、証拠を縦に並べた行列を作り診断性を分析 (4) 行列を洗練し、診断価値のない証拠を外す (5) 仮説を証明するのではなく反証しようとして暫定の結論を出す (6) 少数の決定的な証拠への感度を分析 (7) 最有力だけでなくすべての仮説の相対的な尤度を報告 (8) 将来の観察の目印（milestones）を決める — [Heuer, Psychology of Intelligence Analysis, ch. 8（CIA）](https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf)
- 診断性: 証拠がすべての仮説と整合するなら診断価値はない。行列の各セルに C / I / N/A（整合・不整合・無関係）などの記号を付ける — [Heuer ch. 8](https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf)
- 「不整合（マイナス）が最も少ない仮説がおそらく最有力」。整合する証拠は意味が小さい。ただしマイナスの数による順位は粗く、不整合の度合いは1つの記号では表せない — [Heuer ch. 8](https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf)
- 判断を支える論述は、検討して退けた別の判断とその理由を論じなければ不完全である — [Heuer ch. 8](https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf)
- 2009 年の CIA「A Tradecraft Primer」は、key assumptions check、indicators/signposts、ACH を「診断的技法」に、devil's advocacy を「反対的（contrarian）技法」に分類する — [CIA: A Tradecraft Primer (2009)](https://www.cia.gov/resources/csi/static/955180a45afe3f5013772c313b16face/Tradecraft-Primer-apr09.pdf)、[CIA 紹介ページ](https://www.cia.gov/resources/csi/books-monographs/a-tradecraft-primer)
- 評価: Dhami, Belton, Mandel (2019, Applied Cognitive Psychology 33(6):1080–1090) は分析官 50 人を ACH 使用群と対照群に無作為に分けた。ACH 群は ACH の全段階を守らず、確証バイアスの軽減は混在した結果で、ACH は判断の不整合と誤差を増やしうる。著者は ACH がいつ有用かを再考し、代替の技法を検討するよう勧めている — [Strathprints: Dhami ほか 2019](https://strathprints.strath.ac.uk/69049/)
- 同じ実験の別の分析では、ACH 群は対照群より base rate を使わなかった。Mandel, Karvetski, Dhami (2018) では、ACH を指示された分析官の確率判断は一貫性が低く、正確さもわずかに低かった — 検索結果の要約経由（[Karvetski ほか JDM 2020](https://dlab.sauder.ubc.ca/sjdm/journal/20/200430/jdm200430.html)、本文は接続できず未確認）
- Dhami ほか (2024, Cognitive Research: Principles and Implications) は、行列の向き（仮説を行、証拠を列）を変えると確証バイアスが有意に減ったと報告している — [Springer: s41235-024-00560-y](https://link.springer.com/article/10.1186/s41235-024-00560-y)（検索要約経由。本文の詳細は未確認）

### Inferences
- 対応:
  - 行列の行（仮説） → `rival`。列（証拠） → `operation`。セルの I → `eliminates`、C → `favours`、N/A → どちらにもない。
  - 段階4の「診断価値のない証拠」 → `eliminates` も `favours` も空の operation か、全 rival を favours する operation。`te check` で警告できる。
  - 段階5の「反証しようとする」 → 生き残りを `favours` の多さでなく、未回答の `eliminates` がないことで決める（Carneades の DV と同じ形）。
  - 段階6の感度分析 → `attack` で、結論を支える少数の前提（linchpin）を名指しして攻撃する。`te brief` が premises のうち結論への寄与が大きいものを reviewer に示すと合う。
  - 段階7 → `conclusion.options`（`status`、`reason`）。退けた選択肢とその理由を必須にする規則は ACH の主張と一致する。
  - 段階8の milestones → te に欄がない。`conclusion` に「何が観察されたら考えを変えるか」の欄を足す候補（`prediction` と対になる）。
- 評価の結果から言えるのは「行列の形式を課すだけでは判断がよくならない」こと。te は ACH の採点（マイナスの数え上げ）を自動の判定に使わず、記録と検査（診断性のない operation、退けた理由の欠落）にとどめるのが安全。

### Gaps
- Heuer & Pherson『Structured Analytic Techniques for Intelligence Analysis』の内容は確認していない。
- Tradecraft Primer の ACH の節の本文（手順の書き方）は未確認（目次と分類のみ）。
- Dhami 2019 の本文（どの段階を飛ばしたか）は未確認。

## 攻撃の類型（rebut / undercut / undermine、Pollock、ASPIC+）と te の応答の型

### Takeaway
論証理論の標準は「何を攻撃するか」（結論・推論・前提）の分類で、te の応答の型（surrender / bar / restrict / reinterpret / incorporate）は「攻撃を受けてどうするか」の分類。両者は直交するので、te の objection に `target`（premise / inference / conclusion）を足すのがよい。今の `premise` 欄だけでは undermine しか表せない。

### Cited Findings
- ASPIC+ では、論証は ordinary premise・結論・推論規則の3点で攻撃でき、それぞれ undermining・rebutting・undercutting と呼ぶ — [Modgil & Prakken, ASPIC+ tutorial (2014)](https://dspace.library.uu.nl/bitstream/handle/1874/304259/ASPICtutorial.pdf?sequence=1)、[Argument & Computation 掲載ページ](https://content.iospress.com/articles/argument-and-computation/869766)
- rebut と undercut は defeasible な推論規則にだけ適用され、strict な規則には適用されない。攻撃が defeat になるかは選好で決まるが、undercut は推論規則の例外を表すので選好によらず defeat になる — [ASPIC+ tutorial](https://dspace.library.uu.nl/bitstream/handle/1874/304259/ASPICtutorial.pdf?sequence=1)（検索要約経由。定義の本文は未照合）
- Pollock の区別は undercutting と rebutting。Toulmin の rebuttal は undercut と読める — [Prakken ほか COMMA 2026](https://webspace.science.uu.nl/~prakk101/pubs/comma26TAL.pdf)、[Verheij 2009](https://www.ai.rug.nl/~verheij/publications/pdf/toulmin2009.pdf)
- AIF でも、例外（exception）は conflict scheme の conflicting element になり、推論（RA-node）そのものを攻撃できる — [AIF Specification 2011](https://arg-tech.org/wp-content/uploads/2011/09/aif-spec.pdf)
- Carneades では critical question を assumption か exception として前提に足し、どちらかで立証責任の移り方が変わる — [Gordon ほか 2007](https://tfgordon.github.io/publications/GordonPrakkenWalton2007b.pdf)
- Argdown は `-`（attack）と `_`（undercut）を記法で区別する — [Argdown Syntax](https://argdown.org/syntax/)

### Inferences
- 対応表（攻撃の対象）:
  - undermine（前提を攻撃） → 今の `objections.premise`。
  - undercut（推論を攻撃：「前提は正しいが、そこから結論は出ない」） → 欄なし。思考実験では「この変化を思考実験で再現したことが現実の判断に効く、という橋渡しが成り立たない」型の攻撃がこれに当たる。
  - rebut（結論に反対の結論を立てる） → 欄なし。`rival` を追加する出来事で間接的に表せる。
- te の応答の型の名前は Lakatos『Proofs and Refutations』の surrender / monster-barring / exception-barring / monster-adjustment / lemma-incorporation に近い（出典は今回確認していない。推測）。これは攻撃を受けた側の「修復の方法」で、ASPIC+ の分類とは別の軸。
- 提案: `objections` を `{target: premise|inference|conclusion, ref, response, reason}` にする。`target=inference` の objection が `response=bar` で答えられた場合は Carneades の exception に、`restrict` は qualifier の縮小に対応する。undercut は選好で負けないので、`fold` は未回答の undercut がある rival を「生き残り」にしない、という規則が ASPIC+ と整合する。

### Gaps
- Pollock の原典（Cognitive Carpentry 1995 など）は直接確認していない。
- te の応答の型と Lakatos の対応は、te の設計文書にも出典の記載がなく、今回の調査でも確認していない。

## 全体のまとめ（採用の判断）

### Takeaway
形式（ファイルの書式）として取り込む価値があるのは Argdown（書き出し先）だけ。概念として取り込む価値が高いのは、ASPIC+ の攻撃対象の3分類（objection の `target`）、Carneades の proof standard（生き残りの判定を規則データにする）、ACH の診断性と milestones（`te check` の警告と `conclusion` の欄）。

### Cited Findings
- Argdown: MIT、2026 年に保守あり — [GitHub: christianvoigt/argdown](https://github.com/christianvoigt/argdown)
- Carneades 4: MPL-2.0、最終 push 2024-10 — [GitHub: carneades-4](https://github.com/carneades/carneades-4)
- OVA3: archived — [GitHub: arg-tech/ova3](https://github.com/arg-tech/ova3)
- Compendium: 最終リリース 2014 — [Wikipedia ミラー: Compendium](https://www.wikiwand.com/en/articles/Compendium_(software))
- ACH の効果は実験で支持されていない — [Dhami ほか 2019](https://strathprints.strath.ac.uk/69049/)

### Inferences
- 優先順位の案: (1) `objections.target` を足す（スキーマの小さな変更で、undercut を表せるようになる） (2) `rules.toml` に DV 型の生き残り判定の述語を足す (3) `te check` に「診断性のない operation」の警告 (4) `te render --argdown`。AIF の書き出しは需要が出てから。

### Gaps
- 各候補を te の既存記録（`experiments/2026-11-21-life-value-in-flood-bc.md`）に当てて、対応表が実際に足りるかは試していない。
