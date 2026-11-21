# 散文の仕様が列挙した選択肢を、手書きのモデルはどう扱えば根拠を与えられるか

- 状態: 検討中
- 開始: 2026-11-21
- 更新: 2026-11-21
- 関連: [maps/browser-semantics-soundness/map.toml](../maps/browser-semantics-soundness/map.toml) のセル「非形式 × 列挙した選択肢からの選択」、[experiments/2026-11-20-browser-semantics-soundness.md](2026-11-20-browser-semantics-soundness.md)、[SpecIsolation.tla](models/site-isolation/SpecIsolation.tla)

## 問い

散文の仕様（WHATWG）が「X か Y のどちらか（実装が選ぶ）」と列挙した選択肢を、手で書いた検証モデルがどう扱えば、そのモデルの結論に根拠を与えられるか。

問いの出し方（ユーザーの判断）: 地図の候補から、このセルを `/thought-experiments:mapping-thought-experiments maps/browser-semantics-soundness informal/opt-enum` で選んだ。候補の理由: 同じ行の「必須」（手書きのモデルは反証可能な仮説にとどまる）と、同じ列の「半形式」（隔離を決める段そのものが実装の選択で、非決定にすると情報流を保てない）を前提に組み立てる。

## 前提

- 行「非形式」: 自然言語で書かれていること（Common Criteria v3.1 R5 Part 1 の用語集 55）。WHATWG の原稿を読み、手でモデルに写す場合。
- 列「列挙した選択肢からの選択」: よく定義された値や振る舞いの列挙から実装が選ぶもの（W3C QA Framework: Specification Guidelines 2.4.2 の options の 2 つ目）。代表例は、HTML の「obtain a browsing context to use for a navigation response」の、ブラウジングコンテキストグループの cross-origin isolation mode を「"logical" か "concrete" のどちらか（実装が決める）」にする段。
- 本記録以前のモデル（SpecIsolation.tla）は、この選択を "concrete" に固定していた。
- モード: 構成的（扱い方を組み立てる）。採らなかった候補は、破壊的と探索的。

対立仮説:

- R1 非決定にする。列挙したすべての選択肢を非決定に許せば、安全性の結論は仕様に従うどの実装にも当てはまる。根拠は「モデルの読みに対して、選択肢をすべて覆った」こと。
- R2 パラメータにする。ブラウザごとに選んだ値を固定し、その値を Web から観測して確かめる。根拠は、選択を観測で決めたこと。
- R3 列挙は易しい場合。選択肢が仕様に有限の一覧で書かれているので、散文の仕様でも、この次元についてはモデルを完全にできる。危ないのは列挙の見落としだけ。
- R4（R3 の逆）列挙の要素の意味が定まらない。"logical" が何を保証するかは段の形で書かれていない（仕様は「プラットフォームによっては求められる安全の性質を与えるのが難しい」と書くだけ）。要素の意味が無ければ、選択肢を覆っても性質に根拠は出ない。

設定の欠陥: QA Framework の「よく定義された列挙」と、WHATWG の列挙は一致しない場合がある（要素の意味が定まっていない）。また、手元の例はほぼ cross-origin isolation mode の 1 つだけで、列挙の全体の数を数えていない。

## 条件を変える

固定: SpecIsolation.tla（2 段を足した版）、WPT の 109 件の期待値と各エンジンの結果（[wpt-cases.tsv](models/site-isolation/wpt-cases.tsv)、wpt.fyi の 2026-11-20 の stable）。変える: 列挙の扱い方（ユーザーの判断: 操作 1 と 2 を並行）。

**操作 2: cross-origin isolation mode の選択をパラメータにしてモデルで動かす**

モデルに `COIChoice` を入れ、"concrete" と "logical" を切り替えた（"logical" は `Mutant = "param:coi-logical"` で選ぶ。誤読ではなくパラメータなので、誤読の数には入れない）。

<!-- data-source: original（筆者のモデルを TLC で検査した結果） -->
| 選択 | 18 件との食い違い | 109 件との食い違い |
| --- | --- | --- |
| concrete（今までの固定） | 無し | 無し |
| logical | coi-cl-https | w063、w067、w068、w069、w070、w071 |

食い違う 6 件はどれも、COOP と COEP を送った文書で crossOriginIsolated が真になることを期待する試験。各エンジンの結果（wpt-cases.tsv）では、Chrome と Firefox は 6 件とも通り、Safari は require-corp の 3 件（w069〜w071）を通して credentialless の 3 件に失敗する（Safari が credentialless を持たないため）。仕様では、エージェントクラスタの鍵は mode が "none" でなければ "logical" でも "concrete" でもオリジンになるので、2 つの選択の違いは crossOriginIsolated（と、それに結びつく SharedArrayBuffer などの機能）だけに現れる。

読み取れること:

- この選択は Web のページから観測できる。観測できた範囲では、3 つのエンジンとも "concrete" を選んでいる。
- WPT は列挙の一方（concrete）を期待値として書いており、選択肢を非決定にしたモデルは WPT との一致で確かめられない（R1 の「非決定にして WPT で確かめる」は成り立たない）。
- パラメータにして、ブラウザごとの選択を WPT の結果から決める扱い（R2）は、この選択については成り立つ。

**操作 1: HTML と Fetch の列挙した選択肢の数え上げ**

（subagent の報告を待って書く）

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 具体

（段階B 以降で書く）

## 経過

- 2026-11-21 段階A。試し打ち: モデルの固定を "concrete" から {"logical", "concrete"} の非決定に変えてみる。仕様の「cross-origin isolated capability」は、エージェントクラスタの mode が "concrete" のときだけ真になる（元の思考実験の調査で引用）。すると "logical" を選んだ実行では、COOP と COEP を送っても crossOriginIsolated は偽になる。WPT の credentialless の試験は真を期待しているので、非決定のモデルは WPT と食い違う。WPT は列挙の一方（concrete）を前提にしている。R2 に有利（選択は観測でき、パラメータとして決められる）で、R1 の「非決定にして WPT で確かめる」は成り立たない。R4 の疑いは残る（暫定、モデルではまだ動かしていない）。
- 2026-11-21 段階B の操作 2。選択をパラメータにしてモデルで動かすと、"logical" では WPT の 6 件（と 18 件の 1 件）と食い違い、"concrete" では全件一致した。観測できる範囲では 3 エンジンとも concrete。R1 の「非決定にして WPT で確かめる」は成り立たず、R2 がこの選択について成り立つ。

## 次の問い

（段階C で書く）
