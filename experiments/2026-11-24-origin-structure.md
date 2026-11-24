# ポート、登録可能なドメイン、localhost、不透明なオリジンの継承をモデルに入れると、結論と領域の十分さはどう変わるか

- 状態: 設定中
- 開始: 2026-11-24
- 更新: 2026-11-24
- 関連: [plan/browser-semantics-soundness/TREE.md](../plan/browser-semantics-soundness/TREE.md)、[experiments/2026-11-24-finite-domain-adequacy.md](2026-11-24-finite-domain-adequacy.md)（データ独立の条件）、[adequacy/](models/site-isolation/adequacy/RESULTS.md)
- 木の節: browser-semantics-soundness/B7

## 問い

データ独立の議論は、モデルが写した演算子（等しさ、同じサイト、スキーム、同じホストの片割れ）に限られた。モデルが写していないオリジンの構造（ポート、登録可能なドメインの計算と公開の接尾辞の一覧の違い、登録可能なドメインの無いホスト、localhost の安全な文脈、about:blank・srcdoc・blob・sandbox の不透明なオリジンの継承）をモデルに入れると、性質の判定は変わるか。関係の型はどう増え、どの大きさの領域が要るか。入れないものは、入れない理由と、結論がどの範囲に限られるかを書く。

問いの出し方（ユーザーの判断）: 作業の木の効きが高・中の節がなくなるまで進める（/goal）。Claude は、互いにぶつからない作業の束に分けて並行で進め、この記録はその束の 1 つ。

## 前提

- 仕様: URL の origin と site と schemelessly same site、HTML の obtain a site、same site、secure context、不透明なオリジンの作り方と継承。
- モード: 構成的。

対立仮説:

- R1 判定は変わらない。構造を入れても、性質は今の書き方で成り立ち、関係の型の数が増えるだけ。
- R2 判定が変わる。ポートやサイトの計算を入れると、ある性質が崩れる（例: 同じサイトで別オリジンのポートの間の CORP same-site）。
- R3 一部は入れられない。公開の接尾辞の一覧がクライアントで違うことは、パラメータとしてしか扱えない。

設定の欠陥: 入れる構造の範囲は筆者が選ぶ。

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
