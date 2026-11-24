# 筋書きを構造の軸に沿って機械的に作ると、1 回きりの WPT の筋書きでは見えなかった欠落が見えるようになるか

- 状態: 検討中
- 開始: 2026-11-24
- 更新: 2026-11-24
- 関連: [experiments/2026-11-23-observed-values-inclusion.md](2026-11-23-observed-values-inclusion.md)（ブラウザの値との包含と、入れ子の枠の修正が見えなかったこと）、[experiments/2026-11-23-havoc-unmodeled-steps.md](2026-11-23-havoc-unmodeled-steps.md)、[research_notes/2026-11-23-model-fidelity-survey.md](../research_notes/2026-11-23-model-fidelity-survey.md)（litmus と herd）、[fixes/FIXES.md](models/site-isolation/fixes/FIXES.md)、[observe/](models/site-isolation/observe/RESULTS.md)
- 木の節: browser-semantics-soundness/C2、browser-semantics-soundness/C3

## 問い

前の 2 つの思考実験で、WPT の期待値との照合とブラウザの値との包含は、入れ子の枠についての修正（安全な文脈を最上位から決める段、子の枠の埋め込みの方策への適合の検査）を見なかった。109 件の筋書きに入れ子の枠が無かったためである。メモリモデルの検証では、litmus の試験を軸（緩和の種類）に沿って機械的に作ることで、この種の偏りを減らした（diy）。同じように、筋書きを構造の軸に沿って機械的に作ると、

1. 直したモデルの修正（`false:secure-ctx-top`、`false:nav-coep-adherence`、`false:nav-corp-check` の変異体）を、ブラウザの値が見分けられるようになるか。
2. ブラウザの値は、生成した筋書きでもモデルの許す値に入るか。入らないなら、入れ子の文脈でモデルが外れている所はどこか。

問いの出し方（ユーザーの判断）: 前の思考実験の「次の一手」の 1。手始めに、入れ子の深さと最上位が安全な文脈かの 2 軸から作る。

## 前提

- 軸（手始め）: 入れ子の深さ（0、1、2）、各段の文書のスキーム（https、http）、各段の親とのオリジンの関係（同一オリジン、同じサイトの別オリジン、別サイト）、各段の COEP（unsafe-none、require-corp、credentialless）、子の文書の応答の CORP（無し、same-origin、cross-origin）。組み合わせは、上限の中ですべて作り、意味の無い組み合わせ（http の下の https の COEP など、どれも許されるもの）も落とさずに残す。
- 観測: 各段の文書で、crossOriginIsolated、isSecureContext、子の枠が読み込まれたか止められたか、子の文書からの別オリジンの no-cors の取得の結果（basic、opaque、誤り）。
- モデルが許す値の集合: 直したモデル（SpecIsolation.tla、3b9239d）で、各筋書きについて求める。cross-origin isolation mode は 2 つとも許す。
- 判別の力: 各変異体について、変異の無いモデルの集合に入り変異体の集合に入らない観測があれば殺したと数える。基準は、前の 109 件で殺した集合。
- 安全の配慮: 生成した筋書きで、隔離を緩める側にモデルの外の値が出て、wpt.fyi などで公開されていないものに見える場合は、詳細をリポジトリに書かず、保留用の場所に分け、扱いをユーザーに確かめる。
- モード: 構成的（筋書きを作る道具を作り、動かす）。採らなかった候補は、探索的（手で筋書きを足す）。

対立仮説:

- R1 見えるようになる。生成した筋書きは、入れ子の修正の変異体を殺し、ブラウザの値はほとんどモデルの内側に入る。
- R2 外れが出る。入れ子の文脈では、ブラウザの値がモデルの外に多く出て、モデル（直したもの）がまだ入れ子を正しく写していないことが分かる。
- R3 費用が律速になる。軸の組み合わせが爆発し、ブラウザで動かす時間か、入れ子を作る試験の部品の手間で、軸を増やせない。
- R4 まだ見えない。修正の差が出る筋書きを作っても、観測できる値（crossOriginIsolated、読み込みの成否、取得の結果）がその差を映さない。

設定の欠陥: 軸は筆者が選ぶので、選ばなかった軸（リダイレクト、履歴、popup の系譜、sandbox）の偏りは残る。上限（深さ 2 など）の外は測らない。観測は 1 つの構成の 1 つの版。

## 条件を変える

固定: 直したモデル（SpecIsolation.tla、3b9239d）。変える: 筋書きの作り方（WPT の 109 件 → 軸に沿って機械的に作ったもの）。

subagent が生成器と試験と手順を書き、podman の中で Chrome 158.0.8127.36（2 回目は .88）と Firefox 160.0.1 に 2 回ずつ動かした（[gen/](models/site-isolation/gen/RESULTS.md)）。筆者は報告を読んだ。

**生成**: 最上位は、スキーム × COEP × COOP の 12 通り。子の各段は、スキーム × 親とのホストの関係 × COEP × 応答の CORP の 54 通り。深さ 0〜2 の全体は 35,652 通り。深さ 0 と 1 は全部（660）、深さ 2 は固定の種で層別に選んだ 1,296。計 1,956 の筋書き、ブラウザごとに観測 8,280 行。各軸の値は均等に覆った。読み込みの判定は、子からの postMessage が 12 秒以内に届くか（onload だけでは、Chrome は動かなかった 204 の枠でも発火した）。

**費用**: 1 回の繰り返しで、ブラウザごとに約 10.5 分（2 つのブラウザを並行）。TLC は包含の検査で 18 秒、全体の 35,652 通りで 181 秒。2 回の繰り返しで全行の値が一致した。

**判別の力**（変異体 55 個。殺したの数え方は前の思考実験と同じ）

<!-- data-source: original（subagent の観測と TLC の検査の集計） -->
| 筋書き | 殺した（cross-origin isolation mode は 2 つとも許す） | 殺した（concrete だけ） |
| --- | --- | --- |
| 生成した 1,956（どちらのブラウザでも同じ集合） | 29 | 31 |
| WPT の 109 件（直したモデルで計算し直した） | 41 | 43 |
| 合わせて | 51 | 53 |

- 入れ子の修正の 3 つの変異体は、どれも殺された（WPT の 109 件ではどれも等価だった）。`false:secure-ctx-top` は 1,075 行（isSecureContext と、http の最上位の下の https の子が require-corp を無視すべき取得から）、`false:nav-coep-adherence` は 80 行、`false:nav-corp-check` は 118 行。すべて深さ 1 で見分けられ、深さ 2 を要する変異体は無かった。
- ほかに、`false:mc-block` と、WPT の 109 件で等価だった 3 つ（credentialless の資格情報の扱いなど）も殺した。
- 等価のまま残った 24 個は、標本でも全体の 35,652 通りでも同じだった（この軸で見分けられる変異体はすべて殺した）。残ったのは、軸に入れていない部分の変異体（Origin-Agent-Cluster、COOP と popup、CORP same-site、画像の Mixed Content の引き上げなど）。

**包含**（ブラウザごとに 8,280 行）

- モデルに無かった段が 1 つ見つかった。別オリジンの子の枠での crossOriginIsolated は、Permissions Policy（cross-origin-isolated の機能、既定の許可は自分のオリジンだけ）にも依る。subagent が生成側のモジュール（GenModel.tla）にこの段を足した（切り替えられる。仕様の読みは subagent のもの）。
- この段を足すと、Chrome は 8,280 行すべてが内側、Firefox は 26 行が外に出た。26 行はどれも、隔離された最上位の下の、別オリジンで CORP cross-origin の https の子で、Firefox は crossOriginIsolated を真と返す（モデルは偽）。
- Firefox の 26 行は隔離を緩める側だが、wpt.fyi で既に失敗として公開されている（html/cross-origin-embedder-policy/cross-origin-isolated-permission-iframe.https.window.html が Firefox 160.0.1 で 3/8、Chrome 158 で 8/8。手元でも同じ）。保留に回すものは無かった。
- 段を足さない SpecIsolation のままだと、cross-origin isolation mode を concrete に限ったとき、Chrome の同じ 26 行が外に出る（モデルの欠落）。

読み取れること:

- R1（見えるようになる）が当たった。軸に沿って作った筋書きは、1 回きりの WPT の筋書きでは等価だった入れ子の修正を、どれもブラウザの値で見分けた。
- R2（外れが多い）は当たらなかった。外れは 1 つの型だけで、しかもそれが、モデルに無い段（Permissions Policy）を指した。軸に沿った筋書きは、変異体を殺すだけでなく、モデルの欠落も見つけた。
- R3（費用が律速）は、この上限では当たらなかった。深さ 2 を全部動かすと 27 倍になるが、全体の検査では、それで殺せる変異体は増えない（モデルの上で先に分かる）。
- R4（まだ見えない）は、安全な文脈と入れ子のナビゲーションについては当たらなかった。軸が届かない Mixed Content の 2 つの段については当たった。
- 生成した筋書きと WPT の 109 件は、殺す変異体が重ならない部分を持つ。どちらか一方では足りない。

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 次の問い

（段階C で書く）

## 経過

- 2026-11-24 段階A。問い、軸、対立仮説 R1〜R4、判別の力の数え方を置いた。
- 2026-11-24 段階B。1,956 の筋書きを機械的に作って動かし、入れ子の修正の 3 つの変異体をどれも殺した。外れは 1 つの型で、モデルに無い Permissions Policy の段を指した（Firefox の 26 行は wpt.fyi で既知）。R1 が当たり、R2〜R4 はこの範囲では当たらなかった。

## 具体

- 生成器、試験、観測した値、モデル: [gen/](models/site-isolation/gen/RESULTS.md)（gen.py、scenarios.tsv、observed.tsv、GenModel.tla、GenAllowed.tla、GenEnum.tla、driver/）。生のログと TLC の出力は、ジョブの一時ディレクトリの gen/。
- wpt.fyi の stable の実行 5108994293891072（Firefox 160.0.1）。
