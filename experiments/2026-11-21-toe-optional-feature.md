# 出荷中のブラウザで、支援するかを選べる機能の部分に、検証モデルとの対応の根拠を与えられるか

- 状態: 設定中
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

（段階B で書く）

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

## 経過

- 2026-11-21 段階A。試し打ち（暫定）: 判定基準を変える。toe/mandatory で欠陥が見つかったのは、必須の段では試験の失敗がそのまま欠陥を意味したから。WPT の `.optional` の規約では、支援しない選択が許されるので、試験の失敗は欠陥とは限らない。エンジンは失敗を「支援しないと選んだ」と読み替えられる。すると、この列では試験が反例を出しても欠陥の主張にならず、確かめられるのは「支援すると称する構成での振る舞い」だけになる。R1 に不利、R4 に有利（支援すると決めれば必須に帰着する）。ただし領域に (a) の例がほぼ無いので、この効き目は小さい。

## 次の問い

（段階C で書く）
