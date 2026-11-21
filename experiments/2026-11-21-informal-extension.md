# 散文の仕様の拡張点がある中で、手書きのモデルの結論に根拠を与えられるか

- 状態: 設定中
- 開始: 2026-11-21
- 更新: 2026-11-21
- 関連: [maps/browser-semantics-soundness/map.toml](../maps/browser-semantics-soundness/map.toml) のセル「非形式 × 拡張」、[experiments/2026-11-20-browser-semantics-soundness.md](2026-11-20-browser-semantics-soundness.md)、[experiments/2026-11-21-informal-enumerated-choice.md](2026-11-21-informal-enumerated-choice.md)、[SpecIsolation.tla](models/site-isolation/SpecIsolation.tla)

## 問い

HTML・Fetch には、他の仕様（CSP、Service Workers、Permissions Policy、Storage など）が振る舞いを足せる点がある。手で書いた HTML・Fetch のモデルは、その拡張点を含めて、結論（たとえば OptInOnlySecure や NoUndeclaredLeak）に根拠を与えられるか。与えられるなら、どんな条件のもとでか。

問いの出し方（ユーザーの判断）: `/thought-experiments:mapping-thought-experiments` の候補から、このセルを選んだ。候補の理由: 同じ行の「必須」（散文からモデルへの橋は反証可能な仮説にとどまる。段の欠落は WPT に捕まりにくい）と、同じ列の「半形式」（他の仕様からの差し込みは HTML・Fetch の原稿に現れず、閉包の境界は手で選ぶしかない）を前提に組み立てる。

## 前提

- 行「非形式」: 自然言語で書かれていること（CC v3.1 R5 Part 1 の用語集 55）。WHATWG の原稿を読み、手でモデルに写す場合。
- 列「拡張」: 他の仕様や実装が振る舞いを足せる点（W3C QA Framework: Specification Guidelines 2.4.3）。WHATWG では「applicable specifications」（HTML に 10 箇所、Fetch には 0 箇所）と、他の仕様からの差し込み。Fetch の原稿は「他の標準が Fetch に差し込むための便宜」の算法を持ち、CSP の form-action は「HTML の navigate か form submission に直接差し込む必要がある」と注記する（fetch.bs d7fc0fd、1678 行と 2006 行付近）。
- 拡張点には少なくとも 3 つの形がある（Claude の推論、未検証）。
  1. 呼び出しの形の差し込み: HTML・Fetch の段が他の仕様の算法を名前で呼ぶ（Fetch が CSP の「要求を CSP で止めるか」を呼ぶ、など）。呼び先は閉包に入れられる。
  2. 開いた差し込み: 「applicable specifications」のように、呼び先を名指さない。将来の仕様も入りうる。
  3. 書き換え（monkey patch）: 他の仕様の本文が HTML・Fetch の段を書き換える。HTML・Fetch の原稿には現れない（隣のセル「半形式 × 拡張」）。
- 本記録以前のモデル（SpecIsolation.tla）は、HTML・Fetch の隔離に関わる段だけを写し、拡張点は扱っていない（閉じた世界）。
- モード: 構成的（扱い方と条件を組み立てる）。採らなかった候補は、破壊的（拡張があるので根拠は無いと示す）と探索的。

対立仮説:

- R1 閉じた世界にする。拡張点を無いものとして写し、結論を「拡張が何も足さないなら」という条件つきで述べる。根拠は、仮定を明示したこと。
- R2 拡張点を環境として扱う（assume-guarantee）。各拡張点に「足せるのは止める側だけ」のような契約を置き、契約を満たすどの拡張のもとでも性質が成り立つことを示す。根拠は契約で、契約を各仕様が満たすかは別に確かめる。
- R3 拡張する仕様を閉包に入れる。CSP や Service Workers の算法もモデルに写す。根拠は閉包を広げたことだが、境界は他の仕様の側から逆にたどるしかない。
- R4（破壊的な対抗）根拠は与えられない。開いた差し込みは将来の仕様も含むので、どの有限のモデルも、ある時点の仕様の集合についてしか言えない。

設定の欠陥: 3 つの形の区別は筆者の読みで、数えていない。「足せるのは止める側だけ」という契約が、アクセス制御の性質（OptInOnlySecure）には効いても、情報流の性質（NoUndeclaredLeak）に効くかは分からない。応答を作って返せる差し込み（Service Workers の fetch イベントなど）は、止める側だけの契約に入らない。

## 試行（段階B の前の見込み）

隔離の判断に関わる拡張点を、その差し込みが「止めるか通すかの真偽だけを返し、既存の検査と論理積で合わさる」もの（単調）と、「応答や状態を作って返せる」もの（非単調）に分ける。単調なものは、アクセス制御の性質を保つ（足しても、通る要求の集合が狭まるだけ）。非単調なものは保たない。見込み: 隔離に関わる拡張点の多くは単調で R2 が効くが、少数の非単調な拡張点（応答を作る差し込み）が残り、そこでは R3 にするしかない。

## 条件を変える

（段階B で書く）

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 次の問い

（段階C で書く）

## 経過

- 2026-11-21 段階A。問いと対立仮説 R1〜R4 を置いた。拡張点の 3 つの形と、単調・非単調の分け方を見込みとして書いた（未検証）。

## 具体

- 「applicable specifications」の数: HTML の原稿（0e292f4）に 10 箇所、Fetch の原稿（d7fc0fd）に 0 箇所（`grep -c` で数えた。ファイルはジョブの一時ディレクトリの extract/data/）。
- Fetch の原稿で、他の標準からの差し込みに触れる箇所: 1678 行付近（他の標準が Fetch に差し込むための便宜）、2006 行付近（CSP の form-action は HTML の navigate か form submission に直接差し込む必要がある）。
