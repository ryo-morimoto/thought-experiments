# 出荷中のブラウザの「機能を支援しない構成」を、検証モデルでどう扱うかの手引き

- 対象: 手書きの検証モデル（TLA+ など）でブラウザのサイト分離を確かめ、どの構成に試験を当てるかを決める人
- 元の記録: [experiments/2026-11-21-toe-optional-feature.md](../experiments/2026-11-21-toe-optional-feature.md)（思考実験。前提・反論・引用・検査の出力をすべて残している）
- **新しさについての注意:** 中心の主張「出荷中のブラウザには健全性の根拠は与えられず、試験による確信にとどまる」は、既存の見方の確認です。Common Criteria では、構成の違いは configuration として扱われ、許した構成のどれもが要件を満たさなければなりません（CC Part 1 v3.1 R5 の 189〜193 段）。新しく足せたのは、次の判断の手順と、再現できる試験とモデルです。
- 作成: 2026-11-21（ryo-morimoto の依頼で Claude Opus 5.5 がまとめた。実務の専門家による査読は受けていない）

## 主張

ある機能を支援しない構成で何が消えるかは、機能の種類ではなく、**モデルの保証が能力を条件にして書かれているか**で決まる。

- 能力を条件にした保証（「cross-origin isolated なら、埋め込んだ別オリジンの中身は CORP で許したか資格情報なしで取ったもの」）は、支援しない構成では能力が与えられないので保たれる。ただしそれは、定義から出ているだけ（前件を満たす場合が 0 個）。
- ヘッダーだけの約束（「COOP same-origin を送れば、別オリジンのポップアップと切り離される」）は、支援しない構成では黙って消える。

さらに、能力を条件にした保証が「保たれる」のは、仕様の述語（cross-origin isolated capability）について言える範囲に限られる。出荷物は、別の経路で能力を与えることがある。

## 判断の手順

1. **モデルの保証を 2 つに分ける。** 能力を条件にして書いたもの（含意の形）と、ヘッダーを送ったことだけを条件にしたもの。
2. **能力を条件にした保証には、前件を満たす場合の数を添える。** 支援しない構成で 0 個なら、そこでの「保たれる」は定義から出ているだけなので、根拠として数えない。
3. **能力を別の経路で与える構成を探す。** 例: Chromium の企業ポリシー SharedArrayBufferUnrestrictedAccessAllowed（有効にすると「sites can use SharedArrayBuffer with no restrictions」）。見つかったら、能力そのもの（SharedArrayBuffer、高精度タイマー）を前件にした性質を別に書く。
4. **ヘッダーの読みを、消費者ごとに試験する。** 隔離の判定、取得の検査、ブラウジングコンテキストの切り替えが、同じヘッダーを同じように読んでいるか。判定の側だけが値を知っていると、全部を支援する構成でも保証が破れる（モデルで確認。実在の版で起きたかは確かめていない）。
5. **試験する構成を、出しそうな 1 つに絞らない。** Chromium の試験の構成（fieldtrial_testing_config.json）は study ごとに 1 群で、ブランド版は既定でそれを使わない。モデルの領域の大きな違いは、プラットフォーム（Full、Partial、None のサイト分離）、企業ポリシー、機能のスイッチから来る。

## 具体例

COOP same-origin の効き目を、Chrome for Testing 159.0.8154.6 で、既定の構成と `--disable-features=CrossOriginOpenerPolicy` の構成で試験した。

<!-- data-source: original -->
| 構成 | ポップアップが COOP same-origin を送る（開かれた側の window.opener） | opener が COOP same-origin を送る（開いた側から見た closed） |
| --- | --- | --- |
| 既定 | null（効いた） | true（効いた） |
| COOP を切った構成 | present（効いていない） | false（効いていない） |
| 対照（ヘッダー無し） | present | false |

「出しそうな構成を 1 つ試験する」だけでは、COOP を切った構成で約束が消えることは見えない。Chromium の services/network/public/cpp/features.cc の注釈には、COOP は「enabled for all platforms except WebView」とある（WebView の実機では確かめていない）。

## この手引きが言わないこと

- 出荷中のブラウザについて、健全性を与える方法は言わない。ここで言う根拠は、どれも試験による確信。
- ページからの観測（opener、closed、crossOriginIsolated）は、ページのスクリプトがレンダラーの中で行う。乗っ取られたレンダラーのもとでの保証にはならない。JavaScript を切った構成では観測できない。
- Origin-Agent-Cluster のように、仕様が「要求」として書いた機能を支援しないとき、安全上の損失は小さいとは言わない。損失はプロセスへの割り当て（実装依存）で決まる。
- Safari と Firefox の構成は確かめていない。

## 再現の方法

- 試験: `experiments/models/site-isolation/coop-detect/` で、`CHROME=<Chromium の実行ファイル> sh run.sh`（開かれた側）と `CHROME=... SERVER=server-closed.py sh run.sh`（開いた側）。
- モデル: `experiments/models/site-isolation/Unsupported.tla`（支援する機能の組 7 通り）と `UnsupportedSplit.tla`（写像の分割と、前件を満たす場合の数）。TLC（tla2tools v1.7.4）で、各 `.cfg` を `-config` に渡す。コマンドと出力は元の記録の「具体」にある。
