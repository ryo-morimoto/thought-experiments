# popup の系譜、sandbox、about:blank を軸に足すと、等価のまま残った変異体を見分けられるか

- 状態: 検討中
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

固定: 直したモデルと、gen/ の Permissions Policy の段。変える: 筋書きの軸（popup の系譜、Origin-Agent-Cluster のヘッダー、sandbox、CORP same-site と画像）。

subagent が生成器と試験と手順を書き、モデルの上で全体を先に調べてから、見分けに効く筋書きと層別の標本を Chrome 158.0.8127.88 と Firefox 160.0.1 に 2 回ずつ動かした（[gen2/](models/site-isolation/gen2/RESULTS.md)）。筆者は報告を読んだ。

**軸と数**: popup（開いた側と popup の COOP × popup のオリジン × 直接・about:blank のあと・noopener）108、Origin-Agent-Cluster（最上位と子 2 段のヘッダー）81、sandbox 324、CORP と画像 360。計 873。モデルの上で全体を調べ、変異体 64 個のうち 63 個が見分けられると分かったので、各変異体を少なくとも 2 回覆う 32 の筋書きと、30% の層別の標本を選んで 285 を動かした。

**足したモデルの段**（Gen2Model.tla、それぞれ変異体つき、計 9 個）: sandbox の枠（allow-same-origin 無し）は不透明なオリジン、cross-origin-isolated の機能の既定の許可は自分のオリジン、noopener はいつも開いた側と切る、安全でないページの COOP は unsafe-none として扱う、popup の最初の about:blank は開いた側の COOP を受け継ぐ。Origin-Agent-Cluster の既定は、仕様の時点と whatwg/html#7617 の 2 値のパラメータにした。

**費用**: 1 回の繰り返しで Chrome 約 2 分、Firefox 約 3 分。TLC は 1 つの設定で 2〜5 秒。2 回の繰り返しで全行一致。

**包含**

<!-- data-source: original（subagent の観測と TLC の検査の集計） -->
| Origin-Agent-Cluster の既定 | Chrome（709 行） | Firefox（688 行） |
| --- | --- | --- |
| 仕様の時点 | 696 が内側、13 が外 | 682 が内側、6 が外 |
| #7617 | 709 がすべて内側 | 669 が内側、19 が外 |

- Chrome は、#7617 の既定をパラメータにすると、すべてモデルの内側に入った。Firefox は仕様の時点の値に近い。どちらの既定が「正しい」かではなく、ブラウザごとにどの仕様の時点を取っているかが、パラメータで読める。
- Firefox の外の値は 2 つの型。1 つは、別オリジンの子（sandbox で allow-same-origin つきを含む）が crossOriginIsolated を真と返すもので、gen/ で見た既知の公開の失敗と同じ。もう 1 つは、allow-scripts だけの sandbox の同じホストの子が、COEP require-corp と CORP 無しか same-origin のときに止められるもの。仕様は CORP を容れ物の文書のオリジンで確かめるが、Firefox は不透明なオリジンで確かめているように見える。仕様より厳しい側の食い違いで、手元の WPT のクローンには、これを確かめる試験が見当たらなかった。
- 保留に回すものは無かった。不透明なオリジンの sandbox の枠が crossOriginIsolated を真と返すことは無く、モデルが切るべき popup はすべて切れ、COEP のもとで CORP の無い別オリジンの読み込みはすべて止められた。

**判別の力**（どちらのブラウザでも、Origin-Agent-Cluster のどちらの既定でも、同じ集合を殺した）

<!-- data-source: original（subagent の TLC の検査の集計） -->
| 筋書き | 殺した（2 つの mode） | 殺した（concrete だけ） |
| --- | --- | --- |
| gen2 だけ（前の 55 個のうち） | 53 | 54 |
| gen2 だけ（新しい 9 個のうち） | 9 | 9 |
| gen/ と WPT の 109 件の和（基準） | 51 | 53 |
| gen2 と gen/ と WPT の和 | 53 | 55 |

- 前に等価のまま残った 24 個は、すべて殺された。うち 22 個は WPT の 109 件でも殺せていたもので、和を超えて新しく殺したのは Mixed Content の 2 つの段（画像の引き上げと、祖先の条件）。
- 2 つの mode を許すとき、cross-origin isolated を真の側に足すだけの 2 個は、前と同じく生き残る（logical が偽を許すため）。concrete に限ると、和で 55 個すべてを殺した。

読み取れること:

- R1（見分けられる）が当たった。等価のまま残った 24 個は、足した軸の部分にあり、すべて殺された。
- R2（外れが多い）は当たらなかった。外れは 3 つの型（パラメータで説明できるもの、公開の既知の失敗、仕様より厳しい食い違い）。
- R3（費用が律速）は当たらなかった。モデルの上で先に選んだので、1 回の繰り返しは数分。
- R4（まだ見分けられない）は当たらなかった。
- 軸を足すたびに、モデルの段も足した（今回 5 つ）。筋書きを生成すると、変異体を殺すだけでなく、写していない段がどこに要るかが分かる。

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 次の問い

（段階C で書く）

## 経過

- 2026-11-24 段階A。問い、足す軸、対立仮説 R1〜R4 を置いた。
- 2026-11-24 段階B。popup・Origin-Agent-Cluster・sandbox・CORP と画像の軸で 873 の筋書きを作り、285 を動かした。前に等価だった 24 個はすべて殺され、和で 55 個すべてを殺した（concrete に限ると）。Chrome は #7617 の既定をパラメータにするとすべて内側。外れは 3 つの型で、保留は無し。

## 具体

- 生成器、試験、観測した値、モデル: [gen2/](models/site-isolation/gen2/RESULTS.md)（gen2.py、space.tsv、selected.tsv、observed.tsv、Gen2Model.tla、Gen2Enum.tla、Gen2Allowed.tla、driver/）。生のログと TLC の出力は、ジョブの一時ディレクトリの gen2/。
