# リダイレクトの連鎖を状態の遷移として写すと、1 回きりの筋書きでは支えられなかった列の性質に、ブラウザの値で根拠を与えられるか

- 状態: 設定中
- 開始: 2026-11-24
- 更新: 2026-11-24
- 関連: [plan/browser-semantics-soundness/TREE.md](../plan/browser-semantics-soundness/TREE.md)、[experiments/2026-11-23-observed-values-inclusion.md](2026-11-23-observed-values-inclusion.md)（反例: 途中の応答の COOP を無視するモデルでも 109 件はすべて内側）、[experiments/2026-11-24-axis-generated-scenarios.md](2026-11-24-axis-generated-scenarios.md)、[SpecIsolation.tla](models/site-isolation/SpecIsolation.tla)
- 木の節: browser-semantics-soundness/D1、browser-semantics-soundness/C2

## 問い

これまでのモデルの演算子は 1 回きりの関数で、1 回きりの筋書きでの包含は、列の性質を支えなかった。前の思考実験の攻撃は、途中の応答の COOP を無視するモデルでも WPT の 109 件がすべて内側に入る、という反例を挙げた。そこで、ナビゲーションのリダイレクトの連鎖を状態の遷移（各段の応答ごとに、COOP の施行の結果やグループの切り替えの判断を更新する）として写し、段数と各段のヘッダーを軸にした筋書きでブラウザの値を確かめる。

1. 列として写したモデルで、列の性質（例: 連鎖のどこかで COOP の不一致があれば、最後の文書は開いた側と切れる）が成り立つか。
2. 列の筋書きのブラウザの値は、モデルの許す値に入るか。
3. 途中の段を無視する変異体（最初の応答だけ、最後の応答だけを見るなど）を、ブラウザの値で殺せるか。

問いの出し方（ユーザーの判断）: 作業の木の D1 と C2 を並行で進める。この記録は D1 と、C2 のリダイレクトの軸を受け持つ。C2 の残りの軸は [2026-11-24-popup-sandbox-axes.md](2026-11-24-popup-sandbox-axes.md)。

## 前提

- 仕様: HTML（0e292f4）のナビゲーションの段（navigate、create navigation params by fetching の中で、リダイレクトのたびに COOP の施行の結果を更新する段、obtain a browsing context to use for a navigation response）と、Fetch（d7fc0fd）のリダイレクトの段。どの段で何を更新するかは、本文から確かめる（前の攻撃は記憶で述べた）。
- 軸: 段数 0〜2、各段の応答のオリジンの関係（同一オリジン、同じサイト、別サイト）、各段の COOP、最後の応答の COEP、ナビゲーションの起点（popup の中か、最上位か）。
- 観測: 最後の文書の opener が切れたか、crossOriginIsolated、開いた側から見た popup の closed、history.length。
- モード: 構成的（列のモデルを作り、確かめる）。

対立仮説:

- R1 支えられる。列のモデルの許す値に、ブラウザの値が入り、途中の段を無視する変異体はブラウザの値で殺される。
- R2 ブラウザと食い違う。リダイレクトの途中の段の扱いが、ブラウザで仕様と違う（あるいは仕様の読みと違う）。
- R3 途中の段は観測に映らない。途中の段の COOP の効果が、最後の文書の観測できる値に現れず、変異体が等価になる。
- R4 費用が律速になる。列の状態の空間か、筋書きの数が増えすぎる。

設定の欠陥: 列はリダイレクトだけで、履歴の移動と bfcache は入れない（D1 の残り）。観測できるのは最後の文書の値で、途中の文書は作られない。

## 条件を変える

（段階B で書く）

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 次の問い

（段階C で書く）

## 経過

- 2026-11-24 段階A。問い、軸、対立仮説 R1〜R4 を置いた。

## 具体

（段階B で書く）
