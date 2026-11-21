# 出荷中のブラウザで、支援するかを選べる機能の部分に、検証モデルとの対応の根拠を与えられるか

- 状態: 検討中
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

## 結果を攻撃する

（段階C で書く）

## 結論

（段階C で書く）

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
- 操作 2 の出典（subagent が取得、2026-11-21）: https://chromium.googlesource.com/chromium/src/+/main/components/policy/resources/templates/policy_definitions/ContentSettings/DefaultJavaScriptSetting.yaml 、同じディレクトリの JavaScriptBlockedForUrls.yaml、https://github.com/mozilla/policy-templates/blob/master/docs/index.md 、https://html.spec.whatwg.org/ の「scripting is enabled」
  > Setting the policy to 2 denies JavaScript.
- 操作 3 の出典（subagent が取得、2026-11-21、chromium/src 0b06350a4d5436997354d84fdf3fce356fa4ab31）: https://chromium.googlesource.com/chromium/src/+/main/testing/variations/fieldtrial_testing_config.json 、policy_definitions/Miscellaneous/ の SitePerProcess.yaml・SitePerProcessAndroid.yaml・IsolateOrigins.yaml・OriginAgentClusterDefaultEnabled.yaml、https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md
  > sites on which a given user has entered a password, logged in via an OAuth provider, or encountered a Cross-Origin-Opener-Policy (COOP) header

## 経過

- 2026-11-21 段階A。試し打ち（暫定）: 判定基準を変える。toe/mandatory で欠陥が見つかったのは、必須の段では試験の失敗がそのまま欠陥を意味したから。WPT の `.optional` の規約では、支援しない選択が許されるので、試験の失敗は欠陥とは限らない。エンジンは失敗を「支援しないと選んだ」と読み替えられる。すると、この列では試験が反例を出しても欠陥の主張にならず、確かめられるのは「支援すると称する構成での振る舞い」だけになる。R1 に不利、R4 に有利（支援すると決めれば必須に帰着する）。ただし領域に (a) の例がほぼ無いので、この効き目は小さい。
- 2026-11-21 段階B。ユーザーの判断で、操作 1〜3 を並行して進めた（「条件を変える」）。R1 が落ち、R2 が支えられた。R4 は部分的に当たり、R5 は「制限が能力と結びついているか」に形を変えて残った。R3 は未判定。

## 次の問い

（段階C で書く）
