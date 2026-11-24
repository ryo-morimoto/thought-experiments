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

**操作 2（2 巡目）: 一致しない組の影響を確かめる**（中間の攻撃を受けて。[premises/round2/](models/site-isolation/premises/round2/RESULTS.md)、assess.tsv）

<!-- data-source: original（subagent の評価の集計） -->
| 評価 | 組の数 |
| --- | --- |
| 害が無い（TLC か議論で） | 17（1 つは深さ 2 まで） |
| 主張の範囲を狭める（範囲を書く） | 5 |
| 直すべき | 2 |

- 直すべき 2 つ: 安全な文脈で書いた性質と方策の容れ物で書いた性質の結論の「同意」が広い。https の最上位の下の http の文書（安全な文脈）で、誤読の変異体 samesite-scheme のもとでも元の形は真のまま。CorpPermits で直すと成り立つ（SpecIsolation への取り込みは作業の木の F7）。
- ほかの同意の行は害が無い（その性質の要求元は、最上位では https、または https の最上位の下だけなので、スキームの条件はいつも成り立つ。DIP、支配の条件、差し込み、ORB で、元の形も直した形も、変異のあるなしにかかわらず真）。
- 欠けていた場合を足して確かめ直した（安全な文脈に localhost を含め、ポートつきのオリジンと不透明な要求元を足した写し）: すべての性質が成り立つ。空でない: 前提が成り立つ組が 1,162、うち http://localhost の最上位が 166。
- 範囲を狭めるもの: 文書だけ（data: と about: の最上位の URL と worker は無い）、入れ子は深さ 2 まで、リダイレクトの列の性質に noopener-allow-popups は無い、Signature は CORS の検査の読み方を区別しない。
- 非対称を確かめた: https の要求元が CORP same-site の http の応答を受けるのは許され、逆は止められる。Fetch の条件の文どおりで、モデルの CORP の検査とも一致する。潜む問題: モデルはスキームの検査を Secure で書いており、Secure を「潜在的に信頼できる」に広げると誤る（http://localhost が https://localhost に通る）。SchemeHttps に分ければ直る。
- SameSite の他の使い方: CORP は正しい。サイトのエージェントクラスタの鍵はスキームを落として誤り（81 の筋書きでは、各オリジンの組がスキームを共有するので影響なし）。sandbox は不透明なオリジンが 1 つなら正しく、2 つなら衝突する。
- Permissions Policy の本当の前提は「iframe に allow が無く、応答に Permissions-Policy のヘッダーが無い」で、既定の自分のオリジンが効く。最上位の文書の getter、リダイレクトの COI の行、生成の段がこれを仮定し、生成器はどちらも出さないので満たす。アクセス制御の性質はこれに依らない。
- 分析の定義 15 個: すべてに理由がある。13 個には、誤った定義を暴く試験がある。2 個（観測の時間と大きさの通り道、差し込みの種類）には無い。

読み取れること（2 巡目）: すべての前提の概念が、仕様の定義か、印のついた分析の定義に対応づき、一致しない 24 組はすべて評価した。直すべき 2 つは直した書き方で成り立つ。範囲を狭める 5 つは、主張と一緒に書く範囲になる。

## 結果を攻撃する

（2026-11-24 の中間の攻撃。段階C はまだ）経緯を知らない subagent 2 体の攻撃で、次の反論を受け入れた。狭い・広い対応の 24 組（直した 4 つの外）は、性質を空にしうるか（狭い前提）、仕様の外の理由で崩しうるか（広い前提）を確かめていないので、「済」は言えない。CORP same-site の条件は非対称（https の文書が http の応答を取るのは許す）で、直した書き方がそれを写しているかを確かめ直す。「スキームを問わない同じサイト」は CORP にだけ正しく、エージェントクラスタの鍵では誤り。Permissions Policy の既定の許可は前提ではなく既定で、本当の前提は「iframe に allow が無く、応答に Permissions-Policy のヘッダーが無い」。作業の木の A1 を「一部」に戻し、2 巡目でこれらを確かめる。

## 結論

（段階C で書く）

## 次の問い

（段階C で書く）

## 経過

- 2026-11-24 段階A。問いと対立仮説を置いた。
- 2026-11-24 段階B の 2 巡目。一致しない 24 組を評価した（害なし 17、範囲を狭める 5、直すべき 2）。欠けていた場合（localhost、ポート、不透明な要求元）を足しても性質は成り立ち、空でない。
- 2026-11-24 段階B。36 の性質の 83 の概念を仕様に対応づけた。直すべき食い違い 4 つを見つけ、直した書き方を TLC で確かめた。定義の無い 24 の組は分析の定義と外部の仕様として印をつけた。

## 具体

- 対応の表、直した書き方: [premises/](models/site-isolation/premises/RESULTS.md)（premises.tsv、PremisesFix.tla、PremisesFix.cfg、PremisesFix-samesite-scheme.cfg）。
