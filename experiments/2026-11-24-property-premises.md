# モデルのすべての性質の前提は、仕様の定義に対応づくか

- 状態: 検討中
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

subagent が、モデルの 36 の性質の前提と結論の概念を、HTML（0e292f4）と Fetch（d7fc0fd）の定義に一つずつ対応づけた（83 の組。[premises/](models/site-isolation/premises/RESULTS.md)、premises.tsv）。食い違いには直した書き方を新しいモジュール（PremisesFix.tla）に書き、TLC で確かめた。筆者は報告を読んだ。

<!-- data-source: original（subagent の対応づけの集計） -->
| 対応 | 組の数 |
| --- | --- |
| 一致 | 31 |
| 仕様より狭い | 12 |
| 仕様より広い | 12 |
| 狭い所と広い所がある（安全な文脈は狭く、同意は広い） | 4 |
| 仕様に定義が無い | 24（分析の定義 15、外部か未統合の仕様 7、既に直した誤った前提 2） |

直すべき食い違い:

<!-- data-source: original（subagent のモデルを TLC で検査した結果の要約） -->
| id | 食い違い | 直し方 | TLC |
| --- | --- | --- | --- |
| M1 | 同意（HasOptIn）が広い。CORP same-site の「オリジンのスキームが https か、応答の URL のスキームが https でない」の条件を落としている（fetch.bs 4459 行） | 条件を足した CorpPermits | 安全な文脈・方策の容れ物・COI の上と入れ子の形で真。誤読の変異体 samesite-scheme で、直した形は偽になり、元の形は真のまま（元の結論はこの誤読を見落とす） |
| M2 | SameSite が、HTML の「同じサイト」ではなく「スキームを問わない同じサイト」（html.src 94870 行と 94821 行） | スキームを問わない方として読むか、CorpPermits を使う | HTML の「同じサイト」で書くと偽（https の文書が http の同じサイトから CORP same-site の不透明な応答を受ける）。Mixed Content を経路に入れると真 |
| M3 | 入れ子の COI の性質の前提が、最上位のグループの mode で、子の能力（Permissions Policy の「使ってよい」、既定は自分のオリジン）より広い | 前提を「グループの mode が concrete で、子が親と同一オリジン」に | 真 |
| M4 | Key がスキームを落とし、オリジンの鍵とサイトの鍵が等しくなりうる（gen2 の Origin-Agent-Cluster の行） | KeyHTML | AllOrigins で 48 の衝突。81 の筋書きでの結果は変わらない |

- 分析の定義（Declared、Observe、HookReads、Signature など）は、仕様の言葉ではないことを、理由とともに印をつけた。
- 仕様の概念の方が広いもの（安全な文脈の data: と localhost と worker、オリジンのポートと document.domain、埋め込みの方策の継承と report-only、opener policy の noopener-allow-popups、要求のモード）は、写していない範囲として残る。

読み取れること:

- R1（すべて対応づく）は当たらなかった。4 つの食い違いがあり、24 の組には HTML・Fetch の定義が無い（印をつけた）。
- R2（モデル独自の概念が前提にある）は一部当たった。Declared などが前提に出るが、分析の定義として印をつけた。
- R3（仕様の概念の方が広い）が当たった。
- M1 は、元の性質の結論が、CORP same-site のスキームの条件の誤読を見落とすことを示した。性質を仕様の言葉で書き直すと、検査の判別の力が上がる。

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

## 次の問い

（段階C で書く）

## 経過

- 2026-11-24 段階A。問いと対立仮説を置いた。
- 2026-11-24 段階B。36 の性質の 83 の概念を仕様に対応づけた。直すべき食い違い 4 つを見つけ、直した書き方を TLC で確かめた。定義の無い 24 の組は分析の定義と外部の仕様として印をつけた。

## 具体

- 対応の表、直した書き方: [premises/](models/site-isolation/premises/RESULTS.md)（premises.tsv、PremisesFix.tla、PremisesFix.cfg、PremisesFix-samesite-scheme.cfg）。
