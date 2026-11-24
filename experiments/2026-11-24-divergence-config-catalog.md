# これまでの食い違いと、版と構成で変わる選択を、パラメータか欠陥か前提かに分けられるか

- 状態: 検討中
- 開始: 2026-11-24
- 更新: 2026-11-24
- 関連: [plan/browser-semantics-soundness/TREE.md](../plan/browser-semantics-soundness/TREE.md)、[experiments/2026-11-21-toe-optional-feature.md](2026-11-21-toe-optional-feature.md)、[experiments/2026-11-23-observed-values-inclusion.md](2026-11-23-observed-values-inclusion.md)
- 木の節: browser-semantics-soundness/C4、browser-semantics-soundness/C7

## 問い

これまでに見たブラウザと仕様（あるいはモデル）の食い違い（Chrome の Origin-Agent-Cluster の既定と #7617、Firefox の別オリジンの子の crossOriginIsolated、Firefox の same-origin-allow-popups のリダイレクト、Firefox の sandbox の子の CORP、w014 の試験の作り、ほか）と、版と構成で変わる選択（cross-origin isolation mode の platform による違い、企業ポリシー、Android の部分的なサイト分離、COOP の支援の有無）を、すべて一覧にし、それぞれをモデルのパラメータ（配備の仮定）、ブラウザの欠陥、モデルの前提のどれかに決め、根拠を書く。

問いの出し方（ユーザーの判断）: 作業の木の効きが高・中の節がなくなるまで進める（/goal）。Claude は、互いにぶつからない作業の束に分けて並行で進め、この記録はその束の 1 つ。

## 前提

- 決める規則を先に置く: 仕様に取り込まれた変更か、提案中で出荷されたものはパラメータ、公開の失敗の試験があり仕様に反するものは欠陥、版や構成で変わり仕様が実装に委ねるものは前提。
- モード: 構成的（一覧と決定）。

対立仮説:

- R1 すべて規則で決まる。
- R2 規則で決まらないものがある（仕様が曖昧、提案が止まっている）。

設定の欠陥: 決定は 1 人の判断で、仕様の読みに依る。

## 条件を変える

subagent が、これまでの結果から食い違いと構成の選択を集め、公開の事実（仕様、PR、wpt.fyi、ブラウザの文書、企業ポリシー）を 2026-11-24 に確かめ、段階A の規則で分けた（[catalog/](models/site-isolation/catalog/RESULTS.md)、divergences.tsv、configs.tsv、Params.tla）。筆者は報告を読んだ。wpt.fyi の stable の実行は rev e00a7b14e8（Chrome 158 は 6313827378135040、Firefox 160 は 5108994293891072、Safari 27.2 は 6234878279155712）。

**食い違い（10 件）**

<!-- data-source: original（subagent の分類の要約） -->
| 項目 | 段階A の規則での決定 | 根拠 |
| --- | --- | --- |
| D1 Chrome は Origin-Agent-Cluster のヘッダーが無いとオリジンで区切る | 決まらない（パラメータの条件と欠陥の条件の両方に当たる） | #7617 は未統合で「まだ統合しない」の札と変更の要求（2026-09-30）、Chrome は出荷。Chrome は公開の OAC の試験の一部に失敗 |
| D2 Chrome の document.domain が効かない | D1 に従う | 同じ原因 |
| D3 Firefox の別オリジンの子が crossOriginIsolated を真と返す | ブラウザの欠陥 | cross-origin-isolated-permission-iframe が Chrome 8/8、Firefox 3/8、Safari 3/8 |
| D4 Firefox の same-origin-allow-popups のリダイレクトの連鎖 | ブラウザの欠陥 | popup-redirect-same-origin-allow-popups が Chrome 2/2、Firefox 0/2、Safari 2/2 |
| D5 Firefox の sandbox の子の枠が CORP で止められる | 決まらない（公開の試験が無い） | 仕様は、枠のナビゲーションの CORP を容れ物の文書で確かめる |
| D6 w014 の http の画像の誤り | パラメータ（応答が引き上げ先で配られるか）と、古い試験 | 3 エンジンとも 0/1。引き上げはポートを保ち、wptserve の 8000 番に TLS が無い |
| D7 Chrome は noopener の別サイトへのナビゲーションのあと window.name を残す | 決まらない（モデルの外） | 近い公開の試験は 3 エンジンとも失敗 |
| D8 Firefox は試験の作りの下で bfcache から戻さない | 前提（試験の作りの限界） | bfcache に入れるかはブラウザに委ねられる |
| D9 Safari の credentialless | パラメータ（支援の有無） | 今は Safari 3/5 |
| D10 Chrome の版が繰り返しの間に変わった | 食い違いではない | 値は同じ |

**構成の選択（16 件）**: Origin-Agent-Cluster の既定と企業ポリシー（パラメータ）、cross-origin isolation mode（前提、観測では concrete）、SharedArrayBuffer を隔離なしで許す企業ポリシー（決まらない）、Android・WebView・iOS のプロセスの隔離（前提）、Origin-Agent-Cluster のプロセスへの配置（前提）、WebView の COOP の支援（パラメータ）、DIP・noopener-allow-popups・credentialless の支援（パラメータ）、画像の Mixed Content の引き上げ（パラメータ）、任意のグループの切り替え（前提）、ほか。15 件は段階A の規則で決まり、すべてを Params.tla と configs.tsv にパラメータか前提として書いた（TLC で誤りなし）。

**段階A の規則で決まらなかったもの**: 食い違いの D1・D2・D5・D7、構成の SharedArrayBuffer の企業ポリシー。

**規則の追補**（データを見たあとに足した。Claude の判断で、段階C の攻撃にかける）:

1. 優先の順: 一方のエンジンが出荷した提案で、仕様に取り込まれていないものは、欠陥より先にパラメータにする（モデルを配備の仮定として使う目的に沿うため）。D1 と D2 はパラメータ。
2. 仕様に反するが、隔離を厳しくする側の食い違いは「厳しい側の食い違い」として分け、公開の試験が無くてもよい。D5 はここ（仕様の読み: 枠のナビゲーションの要求のオリジンは、sandbox の子ではなく親の文書のもの）。
3. モデルが写していない値（window.name）の食い違いは「モデルの範囲の外」と記録する。D7 はここ。
4. 試験の作りと実行の環境の限界は、独立の類にする（D6 の後半、D8）。
5. 仕様がブラウザに委ねていないが、配備の設定で変わるもの（SharedArrayBuffer の企業ポリシー）は、「その設定が切られている」という前提にする。

読み取れること:

- R1（すべて規則で決まる）は当たらず、R2（決まらないものがある）が当たった。段階A の規則は、出荷された未統合の提案と、厳しい側の食い違いと、試験の作りの限界を扱えなかった。
- 追補した規則のもとでは、10 件の食い違いと 16 件の選択がすべて決まる。ただし追補はデータを見たあとで、決め方を結果に合わせた疑いがある。

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 次の問い

（段階C で書く）

## 経過

- 2026-11-24 段階A。問いと対立仮説を置いた。
- 2026-11-24 段階B。食い違い 10 件と構成の選択 16 件を集めた。段階A の規則では 5 件が決まらず（R2）、規則を追補した（データを見たあと、段階C の攻撃にかける）。構成の選択は Params.tla と configs.tsv に書いた。

## 具体

- 一覧と結果: [catalog/](models/site-isolation/catalog/RESULTS.md)（divergences.tsv、configs.tsv、Params.tla）。wpt.fyi の応答は入れず、sha256 を RESULTS.md に書いた。
