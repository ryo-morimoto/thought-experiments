# これまでの食い違いと、版と構成で変わる選択を、パラメータか欠陥か前提かに分けられるか

- 状態: 設定中
- 開始: 2026-11-24
- 更新: 2026-11-24
- 関連: [plan/browser-semantics-soundness/TREE.md](../plan/browser-semantics-soundness/TREE.md)、[experiments/2026-11-21-toe-optional-feature.md](2026-11-21-toe-optional-feature.md)、[experiments/2026-11-23-observed-values-inclusion.md](2026-11-23-observed-values-inclusion.md)
- 木の節: browser-semantics-soundness/C4、browser-semantics-soundness/C7

## 問い

これまでに見たブラウザと仕様（あるいはモデル）の食い違い（Chrome の Origin-Agent-Cluster の既定と #7617、Firefox の別オリジンの子の crossOriginIsolated、Firefox の same-origin-allow-popups のリダイレクト、Firefox の sandbox の子の CORP、w014 の試験の作り、ほか）と、版と構成で変わる選択（cross-origin isolation mode の platform による違い、企業ポリシー、Android の部分的なサイト分離、COOP の支援の有無）を、すべて一覧にし、それぞれをモデルのパラメータ（配備の仮定）、ブラウザの欠陥、モデルの前提のどれかに決め、根拠を書く。

問いの出し方（ユーザーの判断）: 作業の木の効きが高・中の節がなくなるまで進める（/goal）。Claude は、互いにぶつからない作業の束に分けて並行で進め、この記録はその束の 1 つ。

## 前提

- 決める規則を先に置く: 仕様に取り込まれた変更か、提案中で出荷されたものはパラメータ、公開の失敗の試験があり仕様に反するものは欠陥、版や構成で変わり仕様が実装に委ねるものは前提。
- モード: 構成的（一覧と決定）。

対立仮説:

- R1 すべて規則で決まる。
- R2 規則で決まらないものがある（仕様が曖昧、提案が止まっている）。

設定の欠陥: 決定は 1 人の判断で、仕様の読みに依る。

## 条件を変える

（段階B で書く）

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 次の問い

（段階C で書く）

## 経過

- 2026-11-24 段階A。問いと対立仮説を置いた。

## 具体

（段階B で書く）
