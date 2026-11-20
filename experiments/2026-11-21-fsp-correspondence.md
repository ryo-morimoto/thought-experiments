# 検証モデルと機能仕様（WHATWG の仕様）の対応に、どんな根拠を与えられるか

- 状態: 検討中
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

段階A の欠陥（「網羅」の意味のずれ）に合わせて、網羅を 2 つの意味に分け、それぞれ別に測った（どちらも subagent が測り、筆者は結果と表を読んだ）。

固定: WHATWG の HTML（0e292f4）と Fetch（d7fc0fd）、NDSS 2026 の 39 件、本記録以前の検証モデル（SpecIsolation.tla、OriginOracle.tla）。変える: 網羅の測り方。

1. **隣の設計のセルと同じ尺度（失敗が基準点のどの項目に収まるか）**: 39 件のうち、Web のページから起こせて、HTML・Fetch・URL の必須の段に違反するもの（FSP）は 2 件（5%: CVE-2024-1671、CVE-2019-13738）。乗っ取られたレンダラーのもとで、仕様の段が定める値を破るもの（FSP-uc）は 9 件（23%）。仕様に段が無いもの（BELOW: 配置、寿命、拡張機能、標準外の機能、ブラウザの内部）は 26 件（67%）。不明 2 件。他の Web の仕様（Clipboard、Push、Notifications、File API など）まで数えると FSP-uc は 15 件。設計文書では 39 件中 26 件が 1 項目に収まったので、この尺度では機能仕様は設計文書より網羅が狭い。
2. **モデルが仕様の段を落とさないか**: 根の 12 算法と依存する段の 108 段のうち、扱う範囲（報告などを除く）の 92 段で、モデルが直接か簡略化して表すのは 74 段（80%）。必須なのにモデルに無い段が 18 段あった。この尺度では、網羅を欠くのは仕様の側ではなくモデルの側。

脱落: R2「機能仕様は網羅を担保し、欠くのはモデルの側」は、尺度 2 では支持されるが、尺度 1 では機能仕様の網羅は 5〜28% で、設計文書（67% が 1 項目に収まる）より狭い。同じ「網羅」で逆の判定になるので、R2 も R1 もそのままでは立たず、尺度を言わない主張は脱落。R3（地図 A と重なる）は、尺度 1 が地図 A に無い見方（失敗の位置）を与えたので弱まった。R4（範疇が合わない）は、この操作では区別できない。

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 具体

**尺度 1 の対応づけ**: subagent が NDSS 2026 の論文の Table V（39 件）の順に、33 件の元の報告（Chromium の課題 29 件、Bugzilla 4 件）と CVE の記録を読み、HTML・Fetch・URL の段（取り出しの一覧の行や原稿の行）に当てた。表全体はジョブの一時ディレクトリ（classification.tsv）にあり、コミットしていない。主な行:

- CVE-2024-1671: HTML「get session history entries」6.1.1（入れ子の履歴は親の文書の状態に属する）に違反。Web のページから起こせる。
- CVE-2019-13738: HTML「create and initialize a Document object」の手順 7（Window の再利用は、初期の about:blank で、かつオリジンが同じときだけ）に違反。Web のページから起こせる。
- CVE-2022-1637: 「create a new browsing context and document」の手順 7（作り手のオリジン）。Web から起こせるが、仕様の範囲で見える誤りは無く（ダイアログの表示だけ）、FSP-uc。
- CVE-2018-16074、CVE-2018-16073: 配置の問題で、仕様に段が無い（BELOW）。本記録以前の判定基準では CVE-2018-16074 をサイトの比較で捕まえたと数えていたが、この分類では仕様の外になる。

**尺度 2 の測定**: subagent がモデルの演算子と仕様の段を 1 段ずつ突き合わせた（判断を含む）。必須なのにモデルに無い段の主なもの:

- noopener-allow-popups の値と、その段（COOP の値の一覧に無い）。
- popup の判定に、COEP を含めて解釈した COOP の値（same-origin-plus-COEP）を渡す段。
- 似たオリジンのエージェントの取得の手順 5.2（履歴の鍵の表への書き込み）。モデルは状態を持たず、過近似になる。
- 安全でない文脈の COEP は unsafe-none とする段（obtain an embedder policy の手順 2）。subagent が TLC で確かめたところ、この段を入れると、http の文書から require-corp での no-cors の取得の結果が error から opaque に変わり、**本記録以前の思考実験でモデルの中で成り立つとした性質 OptInOnly が偽になる**。OptInOnly は、この段の欠落のおかげで成り立っていた。
- COEP allows credentials の段（既知の欠落）。
- 混在コンテンツの遮断（main fetch の手順 7）。

キーの計算で scheme を落としている（http と https の同じホストが同じ鍵になる）など、出力が変わる簡略化も見つかった。

測定の作業ファイルはジョブの一時ディレクトリ（stepcov/、fspmap/）にあり、コミットしていない。

## 経過

- 2026-11-21 段階A。試し打ち: 機能仕様を「形式的」に変えてみる（Wasm の SpecTec 型）。Common Criteria の要求では、対応は提示ではなく証明になる。WHATWG のように非形式なら提示でよい、という扱いは、形式性の水準によって根拠の種類が変わることを、規格自身が認めていることになる。R1 に有利。ただし R4（評価対象 1 つの機能仕様として WHATWG を見てよいか）は残る（暫定）。
- 2026-11-21 段階B（ユーザーの判断: 2-c）。網羅を「失敗が基準点に収まるか」と「モデルが仕様の段を落とさないか」に分けて測った。前者では機能仕様は 39 件中 2〜11 件しか覆わず設計文書より狭い。後者ではモデルが 92 段中 18 段の必須の段を落としていた。尺度を言わない主張は脱落。モデルの欠落が、元の思考実験の OptInOnly の成立を支えていたことが分かった。

## 次の問い

（段階C で書く）
