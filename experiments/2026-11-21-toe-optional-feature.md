# 出荷中のブラウザで、支援するかを選べる機能の部分に、検証モデルとの対応の根拠を与えられるか

- 状態: 結論済み
- 開始: 2026-11-21
- 更新: 2026-11-21
- ゴール: 手書きの検証モデル（SpecIsolation.tla など）で出荷中のブラウザを確かめる人が、試験をどの構成（機能を支援する版・しない版、フィールドトライアルの群）に当てるか、また「確かめた」と言える範囲をどう書くかの判断を変えうる
- 関連: [maps/browser-implementation-correspondence/map.toml](../maps/browser-implementation-correspondence/map.toml) のセル「評価対象そのもの × 機能を支援するかの選択」（toe/opt-feature）、前提のセル toe/mandatory の記録 [experiments/2026-11-20-browser-semantics-soundness.md](2026-11-20-browser-semantics-soundness.md)

## 問い

出荷中のブラウザ（ある版とある構成）について、仕様が「支援するかしないかを実装が選べる」とした機能の部分に、検証モデルとの対応のどんな根拠を与えられるか。隣のセル toe/mandatory の結論（健全性の根拠は与えられず、試験による段階的な確信にとどまる）は、ここにも移るか。

問いの出し方（ユーザーの判断）: `/thought-experiments:mapping-thought-experiments maps/browser-implementation-correspondence toe/opt-feature` で、このセルを選んだ。候補の理由（地図の出力）: 隣の「必須」の結論がここにも移るか。移らないなら、何が違うせいかを条件を変えて探す。

## 前提

- 行「評価対象そのもの」: ソフトウェア・ファームウェア・ハードウェアの集まり（CC Part 1 の 89）。出荷中のブラウザの、ある版とある構成（プラットフォーム、企業の方針、フィールドトライアル）。
- 列「機能を支援するかの選択」: よく定義された機能を支援するかしないかを実装が選べる（W3C QA Framework: Specification Guidelines 2.4.2 の options の 1 つ目）。
- 「根拠」は、toe/mandatory と同じく、証明と経験的な裏付けの両方を含むと読む。
- モード: 破壊的（地図の候補どおり）。攻める命題は「toe/mandatory の結論がそのまま移る」。採らなかった候補は、構成的（構成ごとの根拠を組み立てる）と探索的。

### この列に入るものの区別（設定の欠陥への対処）

出荷中のブラウザで「ある機能が無い」には、少なくとも 3 つの別のものが混ざる。

- (a) 仕様が支援しないことを許す機能。HTML では「User agents are not required to support JavaScript.」（2 Scripting languages、https://html.spec.whatwg.org/ 、2026-11-21 取得）、apple-touch-icon・mask-icon（「user agents are not required to support it in any way」）。これだけがこの列の本来の例。
- (b) 仕様は求めるが、あるエンジンがまだ実装していない機能。仕様への不適合で、toe/mandatory に入る。
- (c) フィールドトライアルや企業の方針で、構成ごとに機能が入ったり外れたりするもの。行の「構成」の側の違い。

モデルの領域（COOP・COEP・Origin-Agent-Cluster・エージェントクラスタ）の中で、(a) にあたる機能は見つからなかった。Origin-Agent-Cluster の段（oacHeader を得て requestsOAC を決める段）は決まった形の必須の段で、(a) ではない。領域に掛かる (a) の候補は「JavaScript を支援しない」だけで、これは企業の方針などの (c) で実際に起こせる（未検証: どのブラウザのどの方針で起こせるかは一次資料で確かめていない）。

## 価値の確認

- **先行する答え**: 製品系列の解析の分類（Thüm, Apel, Kästner, Schaefer, Saake 2014, ACM Computing Surveys 47(1), DOI 10.1145/2580950）。製品ごとの解析は、全製品を解析するときだけ、元の解析に対して健全かつ完全で、標本をとると（optimized）それが崩れる。toe/mandatory で元の解析（試験）に健全性が無いと出ているので、「全構成を試験しても健全性は立たない」は既知とみなす。この記録はその先、「標本の取り方と、支援しない側の扱いで、確信の範囲がどう変わるか」を問う。
- **実在する相手**: Chromium の試験の構成（testing/variations/README.md）。各 study について出荷しそうな構成 1 つだけを試験と WPT に使い、複数の構成を CI で回す当初の目標は容量が足りず諦めた、と書いている。これは行の「構成」の側（c）の相手で、(a) について同じことを決めた記録は見つけていない。
- **予想**: 詳しい実務者なら「必須と同じ結論が移り、構成の数だけ組合せで悪くなる」と予想し、かなり確信する（8 割程度と推測）。

## 対立仮説

- R1 そのまま移る。支援する構成でも、しない構成でも、それぞれ試験による確信にとどまり、必須と違いはない。
- R2 悪くなる。構成ごとに別の評価対象になり、試験する構成は標本（Chromium では study ごとに 1 つ）なので、他の構成には確信すら届かない。
- R3 良くなる部分がある。支援しているかはページから観測できることがある（HTML の originAgentCluster の getter は、エージェントクラスタが origin-keyed かを返す）。支援の有無の対応だけは、構成ごとに直接確かめられる。
- R4 列が潰れる。版と構成を固定すれば、機能は支援されているかいないかに決まり、この列は「必須の段」か「段が無い」に帰着する。列は出荷物の段では区別にならない（軸の欠け）。
- R5 機能の向きで分かれる。機能が能力を足すもの（JavaScript）なら、支援しない構成の振る舞いは支援する構成の部分集合で、安全性の結論は移る。制限を足すもの（隔離の強化）なら、支援しない構成で安全性が崩れ、移らない。

## 条件を変える

段階B では、ユーザーの判断で 3 つの操作を並行して進めた（「1,2,3 を並列で進める」）。操作 1 は筆者が TLC で行った。操作 2 と 3 は、それぞれ subagent に一次資料での調査を任せ、報告を読んで採った。

固定したもの: モデル SpecIsolation.tla の仕様の読み（Mutant = "none"）、取得日 2026-11-21 の仕様と Chromium のソース。理想化したもの: 「支援しない」ブラウザはヘッダーを既定値として読む（HTML の obtain an embedder policy と obtain an opener policy は、知っている値だけを入れる）。

### 操作 1: 支援しない機能の向きを変える（R5）

Unsupported.tla で、支援する機能の組 Supported を 5 通りに変え、4 つの性質を TLC で調べた。

<!-- data-source: original -->
| 支援する機能 | P1 隔離の保証 | P2 credentialless が資格情報を外す | P3 COOP が切り離す | P4 OAC（履歴なし） | P4 OAC（どの履歴でも） |
| --- | --- | --- | --- | --- | --- |
| すべて | 真 | 真 | 真 | 真 | 偽 |
| credentialless なし | 真 | 偽 | 真 | 真 | 偽 |
| COOP なし | 真 | 真 | 偽 | 真 | 偽 |
| OAC なし | 真 | 真 | 真 | 偽 | 偽 |
| なし | 真 | 偽 | 偽 | 偽 | 偽 |

- P1（能力に結びついた保証: 隔離されたなら、埋め込んだ別オリジンの中身は CORP で許したか資格情報なしで取ったもの）は、どの組でも真。支援しないと隔離そのものが得られず、保証は空虚に保たれる（失敗しても閉じる側に倒れる）。P1 は、隔離の条件を緩める誤読（coi-coop-only）では偽になるので、空虚に真なのではない。
- P2（ヘッダーだけから読める約束）は、credentialless を支援しないと偽。ただし隔離も得られないので、P1 から見た損失はない。
- P3（制限だけで、結びついた能力のない機能）は、COOP を支援しないと偽。ページが COOP を送っても、別オリジンのポップアップとの繋がりは黙って残る。
- P4 の Origin-Agent-Cluster は、支援するブラウザでも、グループの履歴でサイト単位に決まっていれば効かない（「どの履歴でも」は常に偽）。仕様が最初から要求（request）として書いているので、支援しない構成で失う保証は「履歴がないときだけ」の分。

仮説への効き目: R5 は形を変えて残る。分かれ目は「能力を足すか制限を足すか」ではなく、「制限が能力と結びついていて、支援しないと能力ごと消えるか（COEP と隔離）」と「制限だけが黙って消えるか（COOP）」。R1（そのまま移る）は P3 で落ちる。

### 操作 2: 版と構成を固定して、列が潰れるか（R4、題材は JavaScript を支援しない）

subagent の報告（一次資料で確かめたもの）:

- Chrome の企業ポリシー DefaultJavaScriptSetting は JavaScript を拒否でき、JavaScriptBlockedForUrls は最上位の文書のオリジンで決める。埋め込まれた別オリジンのフレームは JavaScript を走らせられる。Firefox の企業ポリシーの文書（mozilla/policy-templates の docs/index.md）には JavaScript を切る項目が見つからなかった。Safari は一次資料で確認できず。
- HTML では、支援するかどうかは定義された述語「scripting is enabled」に現れ、どの粒度で切るかは user agent に任されている（「User agents may provide users with the option to disable scripting globally, or in a finer-grained manner」）。
- 「scripting is enabled/disabled」の 48 か所の前後に、opener policy・embedder policy・エージェントクラスタ・browsing context group の段は出てこない。隔離の段は JavaScript の有無で分かれない。

仮説への効き目: R4 は部分的に当たる。版と構成を固定すると、列は「段が無い」ではなく「必須の段（述語で分かれる段）＋実装依存の粒度（opt-impl）」に帰着する。粒度がフレームごとなので、1 つの評価対象の中でも支援する部分としない部分が混ざる。R5 の「能力を減らす向きなら結論が移る」は、この題材でも支持（隔離の段が述語に依存しないため）。

### 操作 3: 構成の標本の取り方（R2、行の (c) の側）

subagent の報告（一次資料で確かめたもの。chromium/src main の HEAD 0b06350a4d5436997354d84fdf3fce356fa4ab31、2026-11-21 取得）:

- fieldtrial_testing_config.json の 1160 の study のうち、モデルの領域（隔離、COOP、プロセス配置）に入るのは 7 件。7 件とも試験で使う群は 1 つだけ。OAC・COEP・credentialless・Document-Isolation-Policy・SitePerProcess の study は 0 件（サーバー側の試行の有無は一次資料で確認できず）。
- 企業ポリシーでは、SitePerProcessAndroid を Disabled にするとサイト分離が全部止まる。IsolateOrigins は任意のオリジンの列挙。OriginAgentClusterDefaultEnabled で、OAC が無いときの既定をプロファイルごとに戻せる。
- docs/process_model_and_site_isolation.md によると、Android（RAM 2GB 以上）の部分的なサイト分離では、パスワードを入れたサイト、OAuth でログインしたサイト、COOP に出会ったサイトを隔離する。Android（2GB 未満）、Android WebView、Chrome for iOS は隔離しない。

仮説への効き目: R2 は支えられ、強まる。試験の構成は study ごとの 1 群の 1 つだけで、領域の大きな違い（プラットフォームの 3 段、ポリシー、flags での opt-out）はその外にある。部分的なサイト分離では、隔離の範囲が利用者の履歴で変わる。そのため、版と構成を固定しても評価対象が実行中に変わり、R4 の「固定すれば潰れる」への反例になる（推論）。構成の総数は、ポリシーに列挙型があり、履歴に左右されるので、有限の数として出せない。

### 3 つを合わせて（暫定）

- R1（そのまま移る）: 落ちる。COOP を支援しない構成で、制限が黙って消える（操作 1）。
- R2（悪くなる）: 支えられる（操作 3）。
- R3（観測で良くなる）: 未判定。P3 が偽になる構成は、ページからは COOP の効き目として観測しにくい（未検証）。
- R4（列が潰れる）: 部分的。必須の段と実装依存の粒度に帰着し、Android の部分的な分離では固定そのものが成り立たない。
- R5（向きで分かれる）: 形を変えて残る。「制限が能力と結びついているか」で分かれる。

### 2 巡目（ユーザーの判断:「1,3 を並列で進める」）

#### 操作 4: 支援しているか・効いたかを、ページから観測できるか（R3）

subagent の報告（一次資料で確かめたもの、HTML と compromised-renderers.md、2026-11-21 取得）:

- 観測の手段は、crossOriginIsolated の getter、originAgentCluster の getter、opener の getter（opener のブラウジングコンテキストが null なら null）。COOP そのものに JavaScript の API は無く、違反の報告は送り手のサーバーの reporting endpoint に届く。
- COOP: 別オリジンの opener から開かれ、COOP same-origin を送ったページで window.opener が null でなければ、COOP は効いていない。操作 1 で P3 が偽になった構成は、こうして見分けられる。逆に、null でも効いた証拠にはならない。仕様は COOP が無くても切り替えを許している（「If browsingContext's group's browsing context set's size is 1, optionally set swapGroup to true.」）。
- COEP credentialless: COOP と合わせて送ったのに crossOriginIsolated が偽なら、どちらかが効いていない（どちらかまでは分からない）。資格情報が実際に外れたかは、ページから見えない。
- OAC: getter が偽なのは、履歴の対応表による正当な結果か、ヘッダーを支援していないためか、区別できない。支援そのものは、getter があるかで推測できるだけ（推論）。
- 観測するのはページ自身のスクリプトで、レンダラーの中で動く。乗っ取られたレンダラーのもとでの保証にはならない（推論。getter の値をどのプロセスが計算するかは一次資料で確認できず）。JavaScript を切った構成（操作 2）では、観測そのものができない。

仮説への効き目: R3 は条件つき。言えるのは「構成ごとに、効かなかったことを検出できる（反例を見つけられる）」までで、「効いた」ことは確かめられない。toe/mandatory の「試験による段階的な確信」と同じ種類で、健全性の根拠ではない。

#### 操作 5: 能力と結びついた制限か、制限だけか、の区別をほかの機能で確かめる（R5）

Unsupported.tla に 2 つの機能を足し、支援する機能の組を 7 通りにして TLC で調べた。

- Document-Isolation-Policy（WICG の Draft Community Group Report、23 April 2025。W3C の標準ではない）。isolate-and-require-corp か isolate-and-credentialless を送った安全な文書は、cross-origin isolated なエージェントクラスタに入り、no-cors の取得が検査される。制限が能力と結びついている型。取得の検査は、同じ名前の COEP の値で近似した（筆者の読み）。
- noopener-allow-popups（HTML の COOP の値）。開いた側との繋がりを、同一オリジンでも切る。制限だけの型。HTML は「it does not create a robust security boundary between those same-origin documents」とも書いている。

<!-- data-source: original -->
| 支援する機能 | P1 隔離の保証 | P5 DIP の保証 | P3 COOP が切り離す | P6 noopener-allow-popups が切り離す |
| --- | --- | --- | --- | --- |
| すべて | 真 | 真 | 真 | 真 |
| DIP なし | 真 | 真 | 真 | 真 |
| noopener-allow-popups なし | 真 | 真 | 真 | 偽 |
| COOP なし | 真 | 真 | 偽 | 偽 |
| なし | 真 | 真 | 偽 | 偽 |

- 予想どおり、能力と結びついた型（DIP）は、支援しない構成でも保証が空虚に保たれる。制限だけの型（noopener-allow-popups）は、黙って消える。P5 は、require-corp の既定の誤読（coep-default）で偽になるので、空虚に真なのではない。
- ただし、noopener-allow-popups について仕様自身が「頑健な境界ではない」と書いている。消えるのは、仕様が保証として約束していない性質。OAC（要求として書かれ、履歴で効かないことがある）と合わせると、制限だけの型のうち、仕様が保証として約束しているのは COOP same-origin（別オリジンとの切り離し）だけになる。

#### 2 巡目を合わせて（暫定）

- R5 の言い直し: 支援しない構成で失うものは、機能の型と仕様の約束の強さで決まる。(1) 能力と結びついた制限（COEP、DIP）は、能力ごと消えるので安全な側に倒れる。(2) 制限だけで、仕様が保証として約束するもの（COOP same-origin）は、黙って消える。ページから「効かなかった」ことは検出できる。(3) 制限だけで、仕様が約束しないもの（OAC、noopener-allow-popups）は、支援する構成でも頼れないので、失う分が小さい。
- R3: 条件つき。検出できるのは反例だけ（段階C で、COOP は開いた側から「効いた」ことも観測できると分かり、改めた）。

### 3 巡目（ユーザーの判断:「1,2 を並列で進める」）

#### 操作 6: 型 2 の COOP が効かなかったことを検出する試験

subagent が試験を書き、Chrome for Testing 159.0.8154.6（Playwright の chromium-1255）で動かした。筆者がリポジトリに写した版（[coop-detect/](models/site-isolation/coop-detect/run.sh)）でもう一度動かし、同じ出力を得た。

- 開かれた側から: 別オリジンの opener（http://127.0.0.1:18431）が、COOP same-origin を返すポップアップ（http://localhost:18432）を開く。既定の構成では、ポップアップの window.opener が null（効いた）。`--disable-features=CrossOriginOpenerPolicy` では present（効いていない）。ヘッダーを送らない対照では、どちらの構成でも present。
- 支援しない構成は、出荷版のバイナリでスイッチ 1 つで作れた。Chromium の services/network/public/cpp/features.cc の注釈には、COOP は「enabled for all platforms except WebView」とある（WebView の実機では確かめていない）。

試験は、この構成で両方向を区別した。限界: null は noopener や、HTML が任意に許す切り替えでも起こる。JavaScript を切った構成では動かない。乗っ取られたレンダラーは観測を偽れる。

## 結果を攻撃する

経緯を渡さない新しい subagent 3 体に、ブラウザのセキュリティの実務・形式手法・認識論と標準の視点で、段階B の時点の結論（C1〜C4）を攻撃させた。渡したのは、問い・用語・結論・前提とその種類だけ。報告の事実のうち、結論に使うものは筆者が一次資料で確かめ直した（「具体」）。

<!-- data-source: original -->
| 反論 | 視点 | 扱い | 理由と結果 |
| --- | --- | --- | --- |
| C2 の「型」は機能ではなく性質の書き方で決まる。同じ credentialless が、能力を条件にした性質（P1）では型 (1)、ヘッダーだけの約束（P2）では型 (2) になる | 形式（高）、認識論（中〜高、後づけの分類） | 受け入れる（言い直す） | 分け目を「機能の型」から「保証が能力を条件にして書かれているか」に改める |
| 型 (1) の「保たれる」は、支援しない構成では前件が偽になり、定義から出る（前件を満たす組は 0 個）。空虚でないことを示した変異も、全部を支援する構成でしか効かない | 形式（高、TLC で確認） | 受け入れる | 「保たれる」の中身は「能力が与えられない」ことだと読み直す。前件を満たす組が 0 個でないことも性質と組にして書くべきだった |
| 能力は隔離と別の経路で得られる。Chromium の企業ポリシー SharedArrayBufferUnrestrictedAccessAllowed を有効にすると「sites can use SharedArrayBuffer with no restrictions」になり、crossOriginIsolated が偽のまま能力だけが得られる | 実務（高、一次資料を確認）、形式（記憶） | 受け入れる（筆者が一次資料で確認） | 型 (1) の安全な側への倒れ方は、仕様の述語（cross-origin isolated capability）についてだけ成り立つ。出荷物の構成は、能力と制限の結びつきを外せる |
| 隔離の判定と取得の検査が、同じ写像（SeenCOEP）を使うと仮定している。判定の側だけが credentialless を知っていると、全部を支援する構成でも P1 が偽 | 形式（中、TLC で確認） | 受け入れる（未検証の前提として残す） | 消費者ごとに写像を試験することが根拠の対象になる。実在のブラウザで起きたかは確かめていない |
| COOP が効いたことも観測できる。COOP same-origin を送る側から開いた別オリジンのポップアップは「will appear closed to the opener」 | 実務（中） | 受け入れる（筆者が試験で確認） | 既定の構成で closed が true、ヘッダー無しと COOP を切った構成では false。操作 4 の「効いたことは確かめられない」は、開かれた側の向きに限る |
| C1 は、行を CC の評価対象に取った時点で決まっている（CC Part 1 の 20 段: assurance は「grounds for confidence」。ATE_IND は TSF の一部を試験する） | 認識論（高） | 受け入れる | 結論 C1 は「既存の見方の確認」と明記する |
| 列は行の中で消える。CC Part 1 の 189〜193 段では、選択肢の有効・無効は「configuration」で、複数の構成を許すなら「each such configuration must meet the requirements」 | 認識論（高、一次資料を確認） | 受け入れる（筆者が一次資料で確認） | 出荷物の段で、この列は「構成」の一部になる。地図の軸の扱いとして利用者に示す |
| 「領域に支援しなくてよい機能がほとんど無い」は誤り。HTML は logical と concrete の選択を「implementation-defined」とし、プロセスへの割り当ても実装に任せる | 実務（高） | 制限する | 指摘の例は、列の別の値（列挙した選択肢、実装依存）に入る。「支援するかの選択」に限れば C4 は残るが、領域の裁量の中心は別の列にある、と書き添える |
| 型 (3)「失う分が小さい」は誤り。OAC を無視するブラウザでは、同じサイトの別オリジンが同じプロセスに入りうるので、Spectre 型の攻撃のもとで失う分は最大になりうる | 認識論（中）、実務（Chromium は OAC を既定で有効にしており、仕様を読んだモデルの既定とずれる） | 受け入れる | 「仕様が約束する分が小さい」までに弱める。安全上の損失は、プロセスへの割り当て（実装依存の列）で決まる |
| C3 は層を混ぜている。モデルの側では 32 構成すべての解析が数秒で終わる。標本にとどまるのは試験の側 | 形式（中） | 受け入れる | 「全製品を解析すれば健全」の条件はモデルについては満たせる。欠けるのは、各構成でモデルと実装が対応しているかの根拠 |
| 試験の構成は出荷物の標本ですらない（README: 「Chrome branded builds do not use these definitions by default」） | 実務（中、一次資料を確認） | 受け入れる | C3 に加える |
| 利用者の履歴で隔離の範囲が変わる構成も、非決定で過大に近似すれば検査できる | 実務（中） | 受け入れる（制限する） | 「評価対象が定まらない」を「CC の意味の評価対象としては構成を固定できない。モデルでは非決定にできるが、None が最悪の場合だとは限らない」に改める |

再開した脱落: なし。R1 の脱落（COOP を支援しない構成で制限が黙って消える）は、攻撃のもとでも残った。

## 結論

**状態: supported**（C1 は既存の見方の確認。新しいのは、何を試験すべきかの区別と、再現できる試験）

前提:

1. 定義上: 行を CC の評価対象に取ると、構成の違いは「configuration」で、許した構成のどれもが要件を満たさなければならない（CC Part 1 の 189〜193 段）。この列は出荷物の段では構成の一部になる。
2. 論証: 支援しないブラウザはヘッダーを既定値として読む（HTML の obtain an embedder policy / obtain an opener policy は知っている値だけを入れる）。
3. 経験的（筆者の TLA+ モデルと TLC）: 能力を条件にした保証（P1、P5）は、支援しない構成では能力が与えられないので保たれる。ただし定義から出る（前件を満たす組は 0 個）。ヘッダーだけの約束（P2、P3、P6）は、支援しないと偽になる。
4. 経験的（一次資料）: Chromium は企業ポリシーで SharedArrayBuffer を隔離なしで許せる。試験の構成は study ごとに 1 群で、ブランド版は既定でそれを使わない。Android の部分的なサイト分離は利用者の履歴に依存する。Chromium は OAC を既定で有効にしている。
5. 経験的（試験）: COOP same-origin が効いたかどうかは、Chrome for Testing 159 で両方の向きから観測できた。
6. 未検証: 隔離の判定と取得の検査が同じ写像を使うこと。Android WebView が COOP を支援しないこと。DIP の取得の検査を COEP で近似したこと。

結論:

- C1（既存の見方の確認）: 出荷中のブラウザの、支援するかを選べる機能の部分にも健全性の根拠は与えられず、試験による段階的な確信にとどまる。toe/mandatory の結論が移る。
- C2（言い直し）: 支援しない構成で何が消えるかは、機能ではなく、保証が能力を条件にして書かれているかで決まる。能力を条件にした保証は、能力が与えられないので保たれる。ただしそれは仕様の述語についてだけで、出荷物は別の経路（SharedArrayBuffer の企業ポリシー）で能力を与えうる。ヘッダーだけの約束（COOP same-origin の切り離し）は黙って消えるが、ページから観測できる。
- C3: 根拠として与えられるのは、構成ごとに「ヘッダーの読み（Seen の写像）が実装と合っているか」を、消費者ごと（隔離の判定、取得の検査、ブラウジングコンテキストの切り替え）に確かめる試験である。モデルの側では全構成の解析ができる。欠けるのは、試験する構成の選び方（Chromium の試験の構成は出荷物の標本ですらない）と、能力を別の経路で与える構成（企業ポリシー）の扱い。

生き残った選択肢と脱落した選択肢:

| 仮説 | 結果 |
| --- | --- |
| R1 そのまま移る | 脱落（COOP を支援しない構成で、ヘッダーだけの約束が消える）。ただし C1 の健全性の部分は移る |
| R2 悪くなる | 生き残り（試験の構成は study ごとに 1 群、ブランド版は使わない） |
| R3 観測で良くなる部分がある | 条件つきで生き残り（COOP は両方の向きから観測できた。観測はレンダラーの中なので、攻撃者のもとでは保証にならない） |
| R4 列が潰れる | 生き残り（CC の構成の扱いで、列は構成の一部になる） |
| R5 向きで分かれる | 言い直して生き残り（分け目は保証の書き方。能力を別の経路で与える構成があると崩れる） |

価値の確認（段階C）:

- 予想との比較: 予想（そのまま移り、構成の組合せで悪くなる）と一致した。C1 は「既存の見方の確認」。新しいのは、(a) 保証の書き方による区別と、それが企業ポリシーで崩れること、(b) 消費者ごとの写像を試験の対象にすること、(c) COOP の効き目を両方の向きから観測できる、再現できる試験。
- 誰が考えを変えうるか: 手書きのモデルで出荷中のブラウザを確かめる人。試験する構成に、SharedArrayBuffer の企業ポリシー、COOP を切った構成（WebView を含む）、Android の部分的な分離を足すかどうかの判断。地図の持ち主にとっては、この列を toe の行で別に持つかどうかの判断。

## 具体

- HTML Living Standard（https://html.spec.whatwg.org/ 、2026-11-21 取得）からの引用:
  > User agents are not required to support JavaScript.

  > The originAgentCluster getter steps are to return the surrounding agent's agent cluster's is origin-keyed.
- WPT のファイル名の規約（https://github.com/web-platform-tests/wpt/blob/master/docs/writing-tests/file-names.md 、2026-11-21 取得）:
  > `.optional` : Indicates that a test makes assertions about optional behavior in a specification, typically marked by the [RFC 2119] "MAY" or "OPTIONAL" keywords.
- Chromium の testing/variations/README.md（https://chromium.googlesource.com/chromium/src/+/main/testing/variations/README.md 、2026-11-21 取得）:
  > For each study, the configuration most likely to launch should be listed and will be used as the default for Chromium builds.

  > the original goal was for CI to run multiple configurations of the same study. But in the end infra didn't have enough capacity for that
- Thüm ら 2014 の著者版（https://www.infosun.fim.uni-passau.de/publications/docs/TAK14.pdf 、sha256 6bdbb2edc6afaae5e7b3f6d829aed81eabd9f0c6bdd6fcdd33beee77aba22bb1。再配布不可の表示があるので、ファイルはリポジトリに入れない）の 3.2 節:
  > A specific advantage of an unoptimized product-based analysis is the soundness and completeness with respect to the analysis that is scaled from single-system engineering (i.e., the base analysis).
- HTML の obtain an embedder policy（https://html.spec.whatwg.org/ 、2026-11-21 取得）:
  > If parsedItem is non-null, parsedItem[0] is a token, and parsedItem[0] is compatible with cross-origin isolation: Set policy's value to parsedItem[0].
- 操作 1 のモデルと設定: [Unsupported.tla](models/site-isolation/Unsupported.tla)、Unsupported-{all,no-cl,no-coop,no-oac,none}.cfg。実行したコマンド（models/site-isolation で、tla2tools v1.7.4）:

  ```sh
  for n in all no-cl no-coop no-oac none; do
    podman run --rm -v $JAR:/tla.jar:ro -v $PWD:/m:ro -v $WORK:/w -w /w \
      docker.io/library/eclipse-temurin:21-jre \
      java -cp /tla.jar tlc2.TLC -metadir /w/$n -config /m/Unsupported-$n.cfg /m/Unsupported.tla
  done
  ```

  出力（PrintResults の行。どれも「Model checking completed. No error has been found.」）:

  ```text
  << "supported", {"credentialless", "coop", "oac"}, [ isolationGuarded |-> TRUE, credentiallessStrips |-> TRUE, coopSevers |-> TRUE, oacFresh |-> TRUE, oacAny |-> FALSE ] >>
  << "supported", {"coop", "oac"}, [ isolationGuarded |-> TRUE, credentiallessStrips |-> FALSE, coopSevers |-> TRUE, oacFresh |-> TRUE, oacAny |-> FALSE ] >>
  << "supported", {"credentialless", "oac"}, [ isolationGuarded |-> TRUE, credentiallessStrips |-> TRUE, coopSevers |-> FALSE, oacFresh |-> TRUE, oacAny |-> FALSE ] >>
  << "supported", {"credentialless", "coop"}, [ isolationGuarded |-> TRUE, credentiallessStrips |-> TRUE, coopSevers |-> TRUE, oacFresh |-> FALSE, oacAny |-> FALSE ] >>
  << "supported", {}, [ isolationGuarded |-> TRUE, credentiallessStrips |-> FALSE, coopSevers |-> FALSE, oacFresh |-> FALSE, oacAny |-> FALSE ] >>
  ```

  空虚でないことの確認（INSTANCE の Mutant だけを変えて、支援する機能はすべて）: coi-coop-only で isolationGuarded が偽、false:coep-cl-strips で credentiallessStrips が偽。cl-ignore-creds では isolationGuarded は真のまま（文書の側で資格情報を外す段が別に守るため）。
- 2 巡目で、Unsupported-*.cfg の内容を 5 つの機能の組に書き換え、no-dip・no-nap を足した。上の 1 巡目の出力は、コミット 24bbd65 の cfg（3 つの機能の組）によるもの。2 巡目の実行は、7 つの cfg について同じコマンド。出力（PrintResults の行、どれも「No error has been found.」）:

  ```text
  all:     [ dipGuarded |-> TRUE, napSevers |-> TRUE, isolationGuarded |-> TRUE, credentiallessStrips |-> TRUE, coopSevers |-> TRUE, oacFresh |-> TRUE, oacAny |-> FALSE ]
  no-cl:   [ dipGuarded |-> TRUE, napSevers |-> TRUE, isolationGuarded |-> TRUE, credentiallessStrips |-> FALSE, coopSevers |-> TRUE, oacFresh |-> TRUE, oacAny |-> FALSE ]
  no-coop: [ dipGuarded |-> TRUE, napSevers |-> FALSE, isolationGuarded |-> TRUE, credentiallessStrips |-> TRUE, coopSevers |-> FALSE, oacFresh |-> TRUE, oacAny |-> FALSE ]
  no-oac:  [ dipGuarded |-> TRUE, napSevers |-> TRUE, isolationGuarded |-> TRUE, credentiallessStrips |-> TRUE, coopSevers |-> TRUE, oacFresh |-> FALSE, oacAny |-> FALSE ]
  no-dip:  [ dipGuarded |-> TRUE, napSevers |-> TRUE, isolationGuarded |-> TRUE, credentiallessStrips |-> TRUE, coopSevers |-> TRUE, oacFresh |-> TRUE, oacAny |-> FALSE ]
  no-nap:  [ dipGuarded |-> TRUE, napSevers |-> FALSE, isolationGuarded |-> TRUE, credentiallessStrips |-> TRUE, coopSevers |-> TRUE, oacFresh |-> TRUE, oacAny |-> FALSE ]
  none:    [ dipGuarded |-> TRUE, napSevers |-> FALSE, isolationGuarded |-> TRUE, credentiallessStrips |-> FALSE, coopSevers |-> FALSE, oacFresh |-> FALSE, oacAny |-> FALSE ]
  ```

  空虚でないことの確認: coep-default で dipGuarded と isolationGuarded がともに偽。
- Document-Isolation-Policy（https://wicg.github.io/document-isolation-policy/ 、2026-11-21 取得、sha256 4ad38bcbe90a10cae87ac2f6ca2e693f43f5a5c12379a09f38398065a06e16da）:
  > If parsedItem[0] is "isolate-and-require-corp" or "isolate-and-credentialless", set policy's value to parsedItem[0].

  > It is not a W3C Standard nor is it on the W3C Standards Track.
- HTML の noopener-allow-popups（https://html.spec.whatwg.org/ 、2026-11-21 取得）:
  > While including a noopener-allow-popups value severs the opener relationship between the document on which it is applied and its opener, it does not create a robust security boundary between those same-origin documents.
- 操作 4 の出典（subagent が取得、2026-11-21）: https://html.spec.whatwg.org/ の crossOriginIsolated・originAgentCluster・opener の getter と、navigate の swapGroup の段、https://chromium.googlesource.com/chromium/src/+/main/docs/security/compromised-renderers.md
  > making security decisions based on trustworthy knowledge, calculated within the privileged browser process
- 操作 6 の試験: [coop-detect/run.sh](models/site-isolation/coop-detect/run.sh)、[server.py](models/site-isolation/coop-detect/server.py)（開かれた側から）、[server-closed.py](models/site-isolation/coop-detect/server-closed.py)（開いた側から）。実行（models/site-isolation/coop-detect で）:

  ```sh
  CHROME=~/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome sh run.sh
  CHROME=~/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome SERVER=server-closed.py sh run.sh
  ```

  出力:

  ```text
  Google Chrome for Testing 159.0.8154.6
  flags=[] coop=[same-origin] -> REPORT same-origin null
  flags=[] coop=[] -> REPORT  present
  flags=[--disable-features=CrossOriginOpenerPolicy] coop=[same-origin] -> REPORT same-origin present
  flags=[--disable-features=CrossOriginOpenerPolicy] coop=[] -> REPORT  present

  Google Chrome for Testing 159.0.8154.6
  flags=[] coop=[same-origin] -> REPORT same-origin true
  flags=[] coop=[] -> REPORT  false
  flags=[--disable-features=CrossOriginOpenerPolicy] coop=[same-origin] -> REPORT same-origin false
  flags=[--disable-features=CrossOriginOpenerPolicy] coop=[] -> REPORT  false
  ```
- Chromium の services/network/public/cpp/features.cc（subagent が取得、chromium/src f217d1a6809e4a2ec757973b8e2a2fe955d905ce、2026-11-21）:
  > // Currently this feature is enabled for all platforms except WebView.
- 段階C で筆者が確かめ直した一次資料（2026-11-21 取得）:
  - https://chromium.googlesource.com/chromium/src/+/main/components/policy/resources/templates/policy_definitions/Miscellaneous/SharedArrayBufferUnrestrictedAccessAllowed.yaml
    > When set to Enabled, sites can use SharedArrayBuffer with no restrictions.
  - HTML（https://html.spec.whatwg.org/ ）の COOP same-origin の説明:
    > any auxiliary browsing context created needs to contain same origin documents that also have the same opener policy or it will appear closed to the opener.
  - HTML の cross-origin isolation mode: 「The choice of which is implementation-defined.」
  - https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md : 「Origin-Agent-Cluster is now enabled by default」
  - CC Part 1 v3.1 R5（https://www.commoncriteriaportal.org/files/ccfiles/CCPART1V3.1R5.pdf ）の 193 段:
    > Note that if the guidance of the TOE still allows more than one configuration, these configurations are collectively called "the TOE" and each such configuration must meet the requirements levied on the TOE.
- 形式手法の攻撃者の TLC の実行（subagent が行った。モデルのコピーに、変異の定数・写像の分割・前件を満たす組の数を足したもの。作業ファイルはジョブの一時領域にあり、リポジトリには入れていない）。要点の出力:

  ```text
  s00 {} isoW 0 dipW 0: isolationGuarded TRUE, dipGuarded TRUE, credentiallessStrips FALSE, coopSevers FALSE
  m32 全部 coi-coop-only isoW 114: isolationGuarded FALSE
  m33 coop なし coi-coop-only isoW 0: isolationGuarded TRUE
  split 全部 Split=TRUE isoW 70: isolationGuarded FALSE
  ```
- 操作 2 の出典（subagent が取得、2026-11-21）: https://chromium.googlesource.com/chromium/src/+/main/components/policy/resources/templates/policy_definitions/ContentSettings/DefaultJavaScriptSetting.yaml 、同じディレクトリの JavaScriptBlockedForUrls.yaml、https://github.com/mozilla/policy-templates/blob/master/docs/index.md 、https://html.spec.whatwg.org/ の「scripting is enabled」
  > Setting the policy to 2 denies JavaScript.
- 操作 3 の出典（subagent が取得、2026-11-21、chromium/src 0b06350a4d5436997354d84fdf3fce356fa4ab31）: https://chromium.googlesource.com/chromium/src/+/main/testing/variations/fieldtrial_testing_config.json 、policy_definitions/Miscellaneous/ の SitePerProcess.yaml・SitePerProcessAndroid.yaml・IsolateOrigins.yaml・OriginAgentClusterDefaultEnabled.yaml、https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md
  > sites on which a given user has entered a password, logged in via an OAuth provider, or encountered a Cross-Origin-Opener-Policy (COOP) header

## 経過

- 2026-11-21 段階A。試し打ち（暫定）: 判定基準を変える。toe/mandatory で欠陥が見つかったのは、必須の段では試験の失敗がそのまま欠陥を意味したから。WPT の `.optional` の規約では、支援しない選択が許されるので、試験の失敗は欠陥とは限らない。エンジンは失敗を「支援しないと選んだ」と読み替えられる。すると、この列では試験が反例を出しても欠陥の主張にならず、確かめられるのは「支援すると称する構成での振る舞い」だけになる。R1 に不利、R4 に有利（支援すると決めれば必須に帰着する）。ただし領域に (a) の例がほぼ無いので、この効き目は小さい。
- 2026-11-21 段階B。ユーザーの判断で、操作 1〜3 を並行して進めた（「条件を変える」）。R1 が落ち、R2 が支えられた。R4 は部分的に当たり、R5 は「制限が能力と結びついているか」に形を変えて残った。R3 は未判定。
- 2026-11-21 段階B の 2 巡目。ユーザーの判断で、操作 4（R3: 観測）と操作 5（R5: DIP と noopener-allow-popups）を並行して進めた。R3 は条件つき（検出できるのは反例だけ）。R5 は「機能の型と仕様の約束の強さ」に言い直した。
- 2026-11-21 段階B の 3 巡目と段階C。ユーザーの判断で、操作 6（COOP の検出の試験）と段階C の攻撃を並行して進めた。試験は両方向を区別した。攻撃で、C2 の分け目を「保証が能力を条件にして書かれているか」に言い直し、企業ポリシーで能力が別の経路から得られることを加えた。C1 は既存の見方の確認とした。

## 次の問い

- 隔離の判定と取得の検査で、ヘッダーの読みが食い違う構成（判定の側だけが credentialless を知っている）は、実在のブラウザの版で起きたか。
- SharedArrayBuffer の企業ポリシーのように、能力を別の経路で与える構成を、モデルの性質（能力を条件にした保証）にどう入れるか。
- 地図: toe の行で、列「機能を支援するかの選択」は CC の構成に吸収される。行の値に「構成の集合」を足すか、列を toe で out_of_scope にするか（利用者の判断を待つ）。
- 地図の toe/opt-enum（logical か concrete か）と toe/opt-impl（プロセスへの割り当て）に、型 (3) の損失の大きさが移る。
