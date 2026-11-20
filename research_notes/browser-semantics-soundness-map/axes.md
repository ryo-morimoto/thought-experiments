# 地図「ブラウザの意味論から検証モデルへの変換の根拠」の軸

地図は 2 枚で、合わせて元の問いを覆う。

- 仕様の側: [maps/browser-semantics-soundness/map.toml](../../maps/browser-semantics-soundness/map.toml)
- 実装の側: [maps/browser-implementation-correspondence/map.toml](../../maps/browser-implementation-correspondence/map.toml)

元の思考実験: [experiments/2026-11-20-browser-semantics-soundness.md](../../experiments/2026-11-20-browser-semantics-soundness.md)。

## 今の軸（ユーザーの判断、2026-11-21）

- 仕様の側の行: 仕様の形式性。Common Criteria v3.1 R5 Part 1 の用語集の informal・semiformal・formal。
- 実装の側の行: 表現の段。Common Criteria v3.1 R5 Part 3 の ADV クラスの機能仕様（ADV_FSP）・設計（ADV_TDS）・実装の表現（ADV_IMP）と、Part 1 の評価対象（target of evaluation）。
- 列（2 枚とも）: 仕様の中身の種類。W3C QA Framework: Specification Guidelines の 2.3.2（必須）と 2.4 Managing Variability（2.4.2 の options の 3 種、2.4.3 拡張、2.4.4 廃止予定、2.4.5 誤りの扱い）。

どれも本文で定義を確かめた。

## 行を自作から Common Criteria に置き換えた経緯

2 つ目の版の行は自作の「何に対する健全性か」（散文の仕様、段ごとに取り出した参照、形式的な元から生成した仕様、出荷中のブラウザ）だった（コミット bf226d8）。地図の候補に従って、既存の分類と突き合わせた。

| 突き合わせた分類 | 分かったこと |
| --- | --- |
| Common Criteria の形式性（informal・semiformal・formal）と表現の段（機能仕様・設計・実装の表現） | 自作の軸は「仕様をどう書いたか」と「どの段か」の 2 つの次元を 1 本に並べていた。設計文書（Chromium の設計文書を基準点に使っていた）と、実装のソースコードの値が欠けていた |
| Barr ら「The Oracle Problem in Software Testing: A Survey」（IEEE TSE 2015）の specified・derived・implicit・human | 取り出した参照と他のブラウザがどちらも derived に、散文を読む人と WPT がどちらも human に入り、答えの違う基準点が同じ値にまとまる。WPT のような試験の期待値の値も欠けていた |

ユーザーに 3 案（自作のまま値を足す、Barr らに置き換える、Common Criteria の形式性に置き換えて実装は別の地図にする）を示し、自作の利点と弱点を説明したうえで、ユーザーが 3 つ目を選んだ。セルの移し方は次のとおり。

- 散文の仕様 → 非形式、段ごとに取り出した参照 → 半形式、形式的な元 → 形式（同じ地図の中で移した）。取り出しは段の形を限るが条件の文の意味は定まらないので、半形式の定義を満たしきらないことをセルに書いた。
- 出荷中のブラウザの 2 セル → 実装の側の地図の「評価対象そのもの」へ移した。
- 実装の側の地図には、思考実験の結果から「設計 × 必須」（設計文書と 39 件の対応づけ）と「実装の表現 × 必須」（修正 CL から読んだ根本原因と判定基準）を足した。

残る欠け: WPT のような試験の期待値は、Common Criteria の行の値にも無い（Common Criteria では試験は ATE クラスで、表現の段ではない）。

## 最初の版を取り下げた理由

最初は「攻撃者の模型（Akhawe ら 2010、Reis ら 2019）× 性質の種類（Clarkson と Schneider 2010）」で作った（コミット 2d5a7c5）。ユーザーが「ずれてきていないか」と指摘した。思考実験で題材にしたサイト分離の切り口（攻撃者、セキュリティ性質）を軸にしたため、地図の問いが「どの攻撃者・どの性質について」に変わり、元の問い（変換の根拠）から離れていた。題材の結論のうち、変換について言えること（反証の記録と追跡可能性しか得られない、手書きのモデルは段を落とす）は新しい地図に移した。攻撃者の軸で書いたセルの言い方は捨てた。

## 捨てた候補

| 候補 | 捨てた理由 |
| --- | --- |
| 攻撃者の模型 × 性質の種類 | 上のとおり、題材の切り口で、元の問いからずれる |
| 何に対する健全性か × 変換で保たれる性質の種類（Clarkson と Schneider） | 過近似が安全性しか保たない点は置けるが、取り出しの実測（残りが仕様のどこに集まるか）が置けない。ユーザーが列を仕様の中身の種類にした |
| 攻撃者 × 根拠の種類（SWEBOK など） | 根拠の種類は問いの答えそのもので、軸にすると答えを先に区切ってしまう |

## 軸の欠け

- 列: QA Framework の分類には、並行（in parallel）、タスクの投入、待ちが無い。取り出しの実測では、取り出せない段の約半分がこれだった（並行 80、タスク 46、待ち 22）。必須の段の中の並行は「必須」の列に置き、並行の意味が決まっていないことはセルの中で扱う。分類を探して足すかは後で決める。
- 列: 2.4.1 の profile・module・level は、WHATWG の Living Standard に無いので除いた。
- 行: 自作で、既存の分類は見つけていない。
