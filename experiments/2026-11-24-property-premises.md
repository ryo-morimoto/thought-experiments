# モデルのすべての性質の前提は、仕様の定義に対応づくか

- 状態: 設定中
- 開始: 2026-11-24
- 更新: 2026-11-24
- 関連: [plan/browser-semantics-soundness/TREE.md](../plan/browser-semantics-soundness/TREE.md)、[fixes/FIXES.md](models/site-isolation/fixes/FIXES.md)、[SpecIsolation.tla](models/site-isolation/SpecIsolation.tla)
- 木の節: browser-semantics-soundness/A1

## 問い

モデルの性質（OptInOnly 系、COIOnlyWithOptIn 系、NoUndeclaredLeak、BodyOnlyByOptIn、リダイレクトの列の性質、gen と gen2 の性質など）の前提と結論に出てくる概念（安全な文脈、オリジン、COEP、資格情報、cross-origin isolated、opener など）を一つずつ、仕様（HTML 0e292f4、Fetch d7fc0fd）の定義に対応づける。対応づかない概念はあるか。

問いの出し方（ユーザーの判断）: 作業の木の効きが高・中の節がなくなるまで進める（/goal）。Claude は、互いにぶつからない作業の束に分けて並行で進め、この記録はその束の 1 つ。

## 前提

- 前に、前提を「https のオリジン」から「安全な文脈」に、ヘッダーの COEP から方策の容れ物の COEP に直した。
- 完了の条件は、各性質の前提の概念が仕様の定義に対応づいていること（作業の木の A1）。
- モード: 構成的（対応の表を作る）。

対立仮説:

- R1 すべて対応づく。残りの性質の前提は、直した 2 つのほかは仕様の概念で書かれている。
- R2 対応づかないものがある。モデル独自の概念（Declared、Observe の値など）が、仕様に定義の無い言葉で前提を書いている。
- R3 対応づくが、仕様の概念の方が広い（例: 安全な文脈の判定に、最上位の作成時の URL 以外の条件がある）。

設定の欠陥: 対応の判定は 1 人で、仕様の読みの誤りは残る。

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
