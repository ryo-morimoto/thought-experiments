# popup の系譜、sandbox、about:blank を軸に足すと、等価のまま残った変異体を見分けられるか

- 状態: 設定中
- 開始: 2026-11-24
- 更新: 2026-11-24
- 関連: [plan/browser-semantics-soundness/TREE.md](../plan/browser-semantics-soundness/TREE.md)、[experiments/2026-11-24-axis-generated-scenarios.md](2026-11-24-axis-generated-scenarios.md)（等価のまま残った 24 個）、[gen/](models/site-isolation/gen/RESULTS.md)
- 木の節: browser-semantics-soundness/C2

## 問い

入れ子・スキーム・COEP の軸で筋書きを作ったとき、等価のまま残った変異体が 24 個あった（Origin-Agent-Cluster、COOP と popup、CORP same-site、画像の Mixed Content など、軸に入れていない部分）。popup の系譜、sandbox、about:blank の軸を足すと、その変異体を見分けられるか。見分けられないまま残るものは、どの軸の外にあるか。

問いの出し方（ユーザーの判断）: 作業の木の D1 と C2 を並行で進める。この記録は C2 のリダイレクト以外の軸を受け持つ。リダイレクトの軸は [2026-11-24-redirect-sequence-model.md](2026-11-24-redirect-sequence-model.md)。

## 前提

- 軸を足す: 開いた側と popup の COOP（unsafe-none、same-origin-allow-popups、same-origin）とオリジンの関係、noopener、popup の最初の about:blank のあとのナビゲーション、iframe の sandbox（allow-scripts、allow-same-origin の有無）、Origin-Agent-Cluster のヘッダー（無し、?0、?1）、CORP same-site、画像の取得。
- モデル: 直したモデル（SpecIsolation.tla と gen/GenModel.tla の Permissions Policy の段）。popup と Origin-Agent-Cluster は既存の演算子を使う。sandbox が要る段は、無ければ新しいモジュールに足す。
- 判別の力: 前と同じ数え方。基準は、前の生成（殺した 29〜31）と WPT の 109 件の和（51〜53）。全体をモデルの上で先に調べて、見分けに効く筋書きだけをブラウザで動かす。
- 安全の配慮: 隔離を緩める側にモデルの外の値が出て、公開されていないものに見える場合は、詳細をリポジトリに書かず保留の場所に分け、ユーザーに確かめる。
- Chrome の Origin-Agent-Cluster の既定は未統合の whatwg/html#7617 に従うので、モデルにはその既定をパラメータとして入れる（前の記録の判定）。
- モード: 構成的。

対立仮説:

- R1 見分けられる。等価のまま残った 24 個のうち、足した軸の部分の変異体は殺される。
- R2 外れが出る。popup と sandbox の文脈で、モデルの外の値が多く出る。
- R3 費用が律速になる。popup は窓を開くので、筋書きあたりの時間が入れ子より大きい。
- R4 まだ見分けられない。足した軸でも、変異体の差が観測できる値に現れない。

設定の欠陥: 軸は筆者が選んだもので、履歴の移動、bfcache、service worker は入れない。popup の系譜の深さは 1 に限る。

## 条件を変える

（段階B で書く）

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 次の問い

（段階C で書く）

## 経過

- 2026-11-24 段階A。問い、足す軸、対立仮説 R1〜R4 を置いた。

## 具体

（段階B で書く）
