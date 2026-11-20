# 検証モデルと機能仕様（WHATWG の仕様）の対応に、どんな根拠を与えられるか

- 状態: 設定中
- 開始: 2026-11-21
- 更新: 2026-11-21
- 関連: [maps/browser-implementation-correspondence/map.toml](../maps/browser-implementation-correspondence/map.toml) のセル「機能仕様 × 必須」、[maps/browser-semantics-soundness/map.toml](../maps/browser-semantics-soundness/map.toml)、[experiments/2026-11-20-browser-semantics-soundness.md](2026-11-20-browser-semantics-soundness.md)

## 問い

隣のセル「設計 × 必須」の結論（設計文書を基準点にしても、段ごとの網羅は文書に担保されない）は、「機能仕様 × 必須」にも移るか。移らないなら、何が違うせいか。

問いの出し方（ユーザーの判断）: 地図 B の候補から、このセルを指定した。

## 前提

- 行「機能仕様」: 外から TSF に入るすべての手段（インターフェース）を記述するもの（Common Criteria v3.1 R5 Part 3 の ADV_FSP）。ブラウザでは、Web に見える振る舞いを定める WHATWG の仕様。
- 列「必須」: すべての実装が従う決まった要求（W3C QA Framework 2.3.2）。
- Common Criteria の要求（Part 3 の ADV_SPM.1、本文で確認）:

> ADV_SPM.1.3D The developer shall provide a formal proof of correspondence between the model and any formal functional specification.
>
> ADV_SPM.1.4D The developer shall provide a demonstration of correspondence between the model and the functional specification.
>
> ADV_SPM.1.3C The correspondence between the model and the functional specification shall be at the correct level of formality.

出典: https://www.commoncriteriaportal.org/files/ccfiles/CCPART3V3.1R5.pdf

つまり Common Criteria は、形式的な機能仕様には対応の証明を、そうでない機能仕様には「適切な形式性の水準での」対応の提示を求める。

- モード: 破壊的（隣の結論が移るかを試す）。採らなかった候補は、構成的と探索的。

対立仮説:

- R1 移る。WHATWG の仕様も段ごとの網羅を担保せず、対応は提示（demonstration）にとどまる。Common Criteria の枠組みでも、非形式の機能仕様にはそれで足りるとされる。
- R2 移らない。機能仕様は設計文書と違い、外から見える振る舞いをすべて決める規範なので、段ごとの網羅は仕様の側に担保される（取り出しで 9 割の段に位置が付いた）。網羅を欠くのはモデルの側。
- R3 このセルは地図 A（仕様の書き方）と重なり、地図 B では扱う意味が無い（扱わない）。
- R4（R1 の逆）範疇が合わない。Common Criteria の機能仕様は評価対象 1 つのインターフェースの記述で、複数のブラウザに共通の WHATWG の仕様はそれに当たらない。

設定の欠陥: 「網羅」の意味が隣のセルとずれうる。設計のセルでは「バグが文書の項目に収まるか」だったが、機能仕様では「モデルが仕様の段を落とさないか」になりうる。同じ言葉で別のことを測ると、移る・移らないの判定が言葉の選び方で決まってしまう。

## 条件を変える

（段階B で書く）

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 具体

（段階B 以降で書く）

## 経過

- 2026-11-21 段階A。試し打ち: 機能仕様を「形式的」に変えてみる（Wasm の SpecTec 型）。Common Criteria の要求では、対応は提示ではなく証明になる。WHATWG のように非形式なら提示でよい、という扱いは、形式性の水準によって根拠の種類が変わることを、規格自身が認めていることになる。R1 に有利。ただし R4（評価対象 1 つの機能仕様として WHATWG を見てよいか）は残る（暫定）。

## 次の問い

（段階C で書く）
