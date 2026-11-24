# バグの履歴が示した、モデルの段で書けるのに欠けた軸を足すと、包含と変異体の殺し方はどう変わるか

- 状態: 検討中
- 開始: 2026-11-24
- 更新: 2026-11-24
- 関連: [plan/browser-semantics-soundness/TREE.md](../plan/browser-semantics-soundness/TREE.md)、[experiments/2026-11-24-bug-history-mutants.md](2026-11-24-bug-history-mutants.md)（欠けた軸の順位）
- 木の節: browser-semantics-soundness/C11

## 問い

公開で直った欠陥から、モデルの段で書けるのに観測の軸に無いものが見つかった（sandbox の旗、リダイレクトで運ばれる COOP 以外の値（Origin の汚れ、referrer policy、CSP の報告の URL）、document.domain のオリジンの領域の検査と Window の再利用、worker の方策の容れ物、別オリジンの cors のモードの取得）。これらをモデルの段と軸として足し、ブラウザの値で包含と変異体の殺し方を確かめると、何が分かるか。

問いの出し方（ユーザーの判断）: 作業の木の効きが高・中の節がなくなるまで進める（/goal）。Claude は、互いにぶつからない作業の束に分けて並行で進め、この記録はその束の 1 つ。

## 前提

- 足す段ごとに C の形の変異体の id を付ける。モデルの上で全体を先に調べ、見分けに効く筋書きを動かす。
- 安全の配慮: 隔離を緩める向きで、公開されていない外れは、リポジトリに書かず保留の場所に分け、ユーザーに確かめる。
- モード: 構成的。

対立仮説:

- R1 足した軸で、バグの型に当たる変異体が殺され、ブラウザの値はほぼ内側。
- R2 外れが出る（足した段の読みがブラウザと違う）。
- R3 一部の軸は、観測できる値に映らない。

設定の欠陥: 軸の選び方はバグの集め方の偏りを受け継ぐ。

## 条件を変える

subagent が 5 つの軸の段をモデルに足し（Gen3Model.tla、変異体 84 個）、筋書きを作り、モデルの上で選んで、Chrome 158.0.8127.88 と Firefox 160.0.1 に 2 回ずつ順に動かした（[gen3/](models/site-isolation/gen3/RESULTS.md)）。筆者は報告を読んだ。

**足した段**: sandbox の旗（語の解析、popup、最上位のナビゲーション）、リダイレクトで運ばれる値（Origin の redirect-taint と直列化、Referrer-Policy、CSP の blockedURI）、document.domain のオリジンの領域の検査と Window の再利用、worker の方策の容れ物（専用、共有、blob:）、COEP のもとの別オリジンの cors の取得。仕様の曖昧さ 2 つ（最初の about:blank が作り手とオリジンを共有するか、referrer の仕様の「変えてもよい」）は、両方の値で動かした。

**規模と費用**: 空間 2,230、モデルの上での選別は 1 つの設定で 10〜12 秒、199 個の変異体のうち 122 個が見分けられる。783 の筋書き（ブラウザごとに 1,974 行、13 のファイル）を選んだ。1 回の繰り返しは Chrome 296 秒、Firefox 321 秒。すべての行が繰り返しで一致。

**包含**（1,974 行のうち内側）

<!-- data-source: original（subagent の観測と TLC の検査の集計） -->
| 設定 | Chrome | Firefox |
| --- | --- | --- |
| 曖昧さを開く（mode の選択、referrer をさらに落とす） | 1,947 | 1,964 |
| 曖昧さを閉じる（concrete、そのまま） | 1,939 | 1,914 |

**殺し方**: 新しい変異体のうち、見分けられる 80 個中 79 個を殺した（閉じた設定）。生き残りは「共有 worker の cross-origin isolated」（ブラウザは共有 worker で真を返さない）。前の思考実験で穴だった「別オリジンの cors の取得の検査を落とす」変異体は、68 行で殺された。モデルの段が欠けていた 15 件の欠陥のうち 11 件が、殺された変異体に当たった（残りは独自のプロトコル、履歴の 2 件、ORB、共有 worker の CSP）。

**モデルの外の値**

<!-- data-source: original（subagent の分類の要約） -->
| 行 | ブラウザ | 値 | 類 |
| --- | --- | --- | --- |
| no-cors の POST で、方策が no-referrer か same-origin のもの 14 | Chrome | "null" の代わりにオリジンを送る | 緩い側、公開の失敗（fetch/origin/assorted.window.html の 3 つの小試験） |
| 同一オリジンの URL が別オリジンにリダイレクトされたもの 12 | Chrome | オリジンの代わりに "null" | 厳しい側 |
| 挿入後に src を設定した iframe 1 | 両方 | Window を再利用しない | 厳しい側、公開の失敗（window-reuse-in-nested-browsing-contexts） |
| COEP の共有 worker 8 | 両方 | 偽 | 厳しい側、logical の選択で許される |
| allow-popups の無い sandbox 8 | Firefox | window.open が null を返さず InvalidAccessError を投げる | 厳しい側 |
| sandbox の無い別サイトの枠が top.location を設定 1 | Firefox | SecurityError | 厳しい側 |
| unsafe-url の別オリジン 42 | Firefox | 完全な URL ではなくオリジンだけ | 厳しい側、「変えてもよい」で許される |

緩い側の型は 1 つで、Chrome は Origin のヘッダーに referrer policy を当てない。14 行のうち 2 行は、方策をリダイレクトの応答のヘッダーだけで与える形で、公開の試験には無い。仕組みが同じなので公開の失敗の範囲に数えた（前の Firefox のリダイレクトの扱いでのユーザーの判断にならった Claude の判断）。

読み取れること:

- R1（殺され、ほぼ内側）が当たった（行の 97〜99% が内側）。
- R2（外れが出る）は一部当たった。7 つの型のうち緩い側は 1 つで、公開の失敗。
- R3（観測に映らない軸）は 3 か所で当たった（利用者の操作を要する語、共有 worker の隔離の選択、referrer の「変えてもよい」）。

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 次の問い

（段階C で書く）

## 経過

- 2026-11-24 段階A。問いと対立仮説を置いた。
- 2026-11-24 段階B。5 つの軸の段と筋書きを足し、783 を両方のブラウザで動かした。新しい変異体の 80 個中 79 個を殺し、行の 97〜99% が内側。緩い側の外れは 1 つの型（Chrome の Origin と referrer policy）で、公開の失敗の範囲に数えた。

## 具体

- モデル、生成器、試験、観測した値: [gen3/](models/site-isolation/gen3/RESULTS.md)。生のログ、TLC の出力、referrer と CSP の仕様の写しは、ジョブの一時ディレクトリの gen3/。
