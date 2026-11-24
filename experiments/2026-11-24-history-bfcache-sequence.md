# 履歴の移動と bfcache を列として写すと、2 つ目の断片でも同じ方法が働くか

- 状態: 設定中
- 開始: 2026-11-24
- 更新: 2026-11-24
- 関連: [plan/browser-semantics-soundness/TREE.md](../plan/browser-semantics-soundness/TREE.md)、[experiments/2026-11-24-redirect-sequence-model.md](2026-11-24-redirect-sequence-model.md)、[NestedHistory.tla](models/site-isolation/NestedHistory.tla)
- 木の節: browser-semantics-soundness/D1、browser-semantics-soundness/E1、browser-semantics-soundness/C2

## 問い

セッション履歴の移動（戻る・進む、traverse the history by a delta、apply the history step）と bfcache からの復元を、状態の遷移として写す。COOP によるグループの切り替え、opener の関係、crossOriginIsolated、Origin-Agent-Cluster の鍵が、履歴の移動と bfcache の復元でどう保たれるかの列の性質を立て、軸に沿って筋書きを作り、ブラウザの値で包含と変異体の殺し方を確かめる。これを 2 つ目の断片として、これまでの方法（モデル、生成、選別、包含、変異体）の手間と効き目を測る。

問いの出し方（ユーザーの判断）: 作業の木の効きが高・中の節がなくなるまで進める（/goal）。Claude は、互いにぶつからない作業の束に分けて並行で進め、この記録はその束の 1 つ。

## 前提

- NestedHistory.tla は session history の選び方の一部を写している。
- 方法の手間は、モデルの段の数、試験の部品の数、ブラウザで動かす時間で測る。効き目は、殺した変異体の数、見つけたモデルの欠落と食い違い。
- 安全の配慮は前と同じ（保留の場所）。
- モード: 構成的。

対立仮説:

- R1 働く。同じ手順で、列の性質に標本の根拠が付き、手間は前の断片と同じ程度。
- R2 写す手間が律速になる（履歴の段は状態が大きく、ブラウザの観測も難しい）。
- R3 観測が映さない。bfcache に入ったかどうかなどが、観測できる値に出にくい。
- R4 ブラウザどうし・仕様との食い違いが多い（履歴は相互運用性が低いことで知られる）。

設定の欠陥: 履歴の段の写し方は 1 人の読みで、深さと履歴の長さに上限を置く。

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
