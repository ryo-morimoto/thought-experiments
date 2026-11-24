# 事前登録: 凍結したモデルでの取り置きの実行（関係の型の穴を埋める筋書き）

- 登録: 2026-11-24（このファイルを含むコミットに `prereg-frozen-holdout-2026-11-24` のタグを付ける）
- 関連: [experiments/2026-11-24-frozen-holdout.md](../2026-11-24-frozen-holdout.md)（この試験を必要とした思考実験。対立仮説 R1〜R3）、[experiments/2026-11-24-finite-domain-adequacy.md](../2026-11-24-finite-domain-adequacy.md) と [adequacy/RESULTS.md](../models/site-isolation/adequacy/RESULTS.md)（関係の型の穴）
- 木の節: browser-semantics-soundness/C10、browser-semantics-soundness/C2

このファイルは、新しい種で筋書きを作ってブラウザで動かす前に、モデル、筋書きの作り方、観測の写し方、判定と数え方を固定するためのもの。登録の後で、下の固定物を変えない。変えるときは、変えたことと理由を「登録後の変更」に書き、変えた後に得た行だけで数え直す。

## 問い

これまでモデルはデータと一緒に育った。モデル・パラメータ・軸・判定を先に固定し、関係の型の穴（互いに別サイトの 3 つのオリジン、別々の http のオリジン、別サイトどうしで異なるリダイレクトの段、http の段）を埋める筋書きを新しい種で作ってブラウザで動かすと、ブラウザの値はモデルの許す値に入るか（R1）、新しい外れが出るか（R2）、変異体の殺し方が変わるか（R3）。

## 固定するもの

<!-- data-source: original（登録で固定するものの一覧） -->
| 固定物 | 値 |
| --- | --- |
| モデルのコミット | 登録の時点の HEAD `94deed8fb5c6e1116f63c5cbccdcf29bc48f05e9` |
| 凍結したモデル（編集しない） | [SpecIsolation.tla](../models/site-isolation/SpecIsolation.tla)（sha256 428184940267fe35c0d74c074263251ca0a7a213994fdf97825e4b84d2db50da）、[gen/GenModel.tla](../models/site-isolation/gen/GenModel.tla)（edba54cadfbd9f9e3bb956b2d4133ee1cc4a408138c6494c2082e627c1a807bb）、[redirect/RedirectSeq.tla](../models/site-isolation/redirect/RedirectSeq.tla)（140a6f8c8cd03ac0f09c920cd7f4aab0d20ef3657618f9b289f6e4e404d61a8a）。K_prev の計算にだけ [gen2/Gen2Model.tla](../models/site-isolation/gen2/Gen2Model.tla)（b676e71bfc4d88c5c29812faf43b7dfb440e2b8aaef2eed68de6837941cfed80）も使う |
| 取り置きの道具 | [holdout/](../models/site-isolation/holdout/) の下のファイル（登録の時点ではコミットしない。sha256 を下の「道具の sha256」に書く） |
| パラメータ | Origin-Agent-Cluster: Chrome は #7617、Firefox は spec。この 2 つの族のモデル（GenModel、RedirectSeq）は KeyKind を呼ばないので、値に効かない（K_prev の gen2/ の行にだけ効く）。権限ポリシーの段: GenModel の `WithPP = TRUE` を主にする |
| COI のモード | 主: COIChoice {concrete, logical}。副: {concrete}。入れ子の族は、副として `WithPP = FALSE` の 2 つも数える |
| 変異体 | [HoldMutants.tla](../models/site-isolation/holdout/HoldMutants.tla) の NMs（入れ子の族、115 個 = GenModel の 55 個 + 拡張 X 60 個）と RMs（リダイレクトの族、141 個 = RedirectSeq の 65 個 + RX 76 個）。X は SpecIsolation の判断 33 個のうち FixIds でない 27 個の `false:` と、33 個すべての `true:`。RX は X に RedirectSeq の 8 個の判断の `false:` と `true:` を足したもの |
| 種 | 20261125（前の gen/、gen2/、redirect/ は 20261124） |
| ブラウザ | podman `docker.io/library/python:3.12-bookworm`、WPT の clone 31362d122（overlay で載せ、手元の写しは変えない）、`--channel=stable --install-browser --install-webdriver`、`--headless --timeout-multiplier=4`、2 回の繰り返し。見込みの版は Chrome 158 と Firefox 160。実際の版はログから書く |
| コンテナの中だけの変更 | `tools/serve/serve.py` の既定の alternate_hosts に `alt2 = web-platform-c.test`、`alt3 = web-platform-d.test` を足す（config.json では新しい鍵を足せないため）。証明書は既定のもの。Chrome は SPKI で、Firefox は certutil なし（acceptInsecureCerts）で証明書の誤りを無視する。これは既定の 2 つのサイトと同じ扱い |

## 筋書きの作り方（[gen_holdout.py](../models/site-isolation/holdout/gen_holdout.py)）

オリジンは SpecIsolation と同じ (scheme, host, site) の組。サイトは a、b、c、d（ブラウザでは web-platform.test、not-web-platform.test、web-platform-c.test、web-platform-d.test）、ホストは裸・www・www1・www2、スキームは https と http。関係の型は、各要素のスキームと、各対の「同じオリジンか」「同じサイトか」（adequacy/types.py の粗い型）。

- **入れ子の族 N**（GenModel、深さ 2）: 最上位は裸の a で、スキームは型が決める。1 段目と 2 段目は 3 サイト × 4 ホスト × 2 スキーム。(最上位, 1 段目, 2 段目) の 66 の型のそれぞれから、代表の組を種で 1 つ選ぶ。軸は、最上位の COEP 3 × COOP 2、各段の COEP 3 × CORP 3、no-cors の取得先 3（`xs`: どの段にもないサイト d の https の裸のホスト、`ss`: 2 段目と同じサイトの別ホストの https、`ht`: 2 段目と同じホストの http）。直積は 96,228。事前の選別の空間は、396 の層（代表 × 最上位の構成）のそれぞれに、243 の組み合わせ（段の構成と取得先）から 48 を、種で並べ替えた列から順に割り当てたもの（19,008）。
- **リダイレクトの族 R**（RedirectSeq、popup）: 開く側は https の裸の a（SI!OA）。段と最後の文書のオリジンは 4 サイト × 4 ホスト × 2 スキーム。(A, 最後) の 5 型、(A, 段, 最後) の 33 型、(A, 段 1, 段 2, 最後) の 269 型のそれぞれから代表を種で 1 つ選ぶ。軸は開く側の COOP 4 × 始まり 2（空の popup、読み込んだ文書）× 段の符号 4（un、sap、so、so+rc）× 最後の COOP 3 × COEP 2。0 段と 1 段はすべての組み合わせ（240 + 6,336）、2 段は代表ごとに 768 の組み合わせから 48 を種で並べ替えた列から順に割り当てる（12,912）。計 19,488。
- **事前の選別**（[HoldEnum.tla](../models/site-isolation/holdout/HoldEnum.tla)、ブラウザなし）: 各筋書きについて、主と副の COI のモードのそれぞれで、許す値のベクトルが変異しないモデルと違う変異体の集合の対を求め、対の等しい筋書きを 1 つの類にする。N は `WithPP = TRUE` で数える。
- **選び方**: 種 20261126 の乱数で、各類から 2 つ（どの変異体も見分けない類からは 12）を選ぶ。N は、さらに各層に少なくとも 2 つの筋書きがあるように足す。R は、さらに各代表（型）に少なくとも 1 つの筋書きがあるように足す。選んだ筋書きはすべて動かす。

## 観測の写し方

- N（[hobs.js](../models/site-isolation/holdout/tests/resources/hobs.js)、gen/ の gobs.js と同じ）: 各段の `load`（12 秒の間に postMessage が届けば loaded）、`coi`（crossOriginIsolated）、`sec`（isSecureContext）。2 段目の `fetch` と `fetchc`（no-cors、credentials の既定と include）。最上位の `coi` と `sec` は試験のファイルごとに 1 回観測し、そのファイルの最初の筋書きの行として 1 回だけ数える。`LATE` は写さず、0 でなければ報告する。
- R（[hrobs.js](../models/site-isolation/holdout/tests/resources/hrobs.js)、redirect/ の robs.js と同じ）: `closed`、`opener`、`coi`、`hlen`。`error` の行は写さず、数を報告する。
- 行の観測値は、2 回の繰り返しの値の和集合。ログからの抜き出しは gen/driver/extract.py と redirect/driver/extract.py をそのまま使い、[driver/mkrows.py](../models/site-isolation/holdout/driver/mkrows.py) が HoldRows.tla を書く。

## 判定の規則

1. **包含**: 行の観測値の集合が、変異しないモデルの許す集合に含まれれば内側。ブラウザ・族・設定ごとに数える。主の数は、N が `HoldAllowed-N-both`（WithPP TRUE、{concrete, logical}）、R が `HoldAllowed-R-both`。
2. **外れの分類**: 外れた行を、(ブラウザ, 種類, 観測値, 許す値) と仕組みで型にまとめ、次のどれか 1 つに入れる。理由を書く。
   - **P パラメータ**: 登録した別のパラメータ値（WithPP FALSE、{concrete} と {concrete, logical} の違い）でなら内側になる。
   - **K 公開の既知の食い違い**: このリポジトリにすでに記録した型で、公開の失敗がある型と仕組みが同じ。K1 = Firefox が COI のグループの中の、親と別オリジンの子で crossOriginIsolated を TRUE にする（cross-origin-isolated-permission-iframe、gen/RESULTS.md）。K2 = Firefox が SAP の開く側の空の popup で、段ごとの比べ方を起点と比べる（popup-redirect-same-origin-allow-popups、redirect/RESULTS.md。値が変異体 `neg:hop-update` の許す集合に入ること）。
   - **M モデルの欠落**: 値が仕様の本文に合い、モデルにその段が無いか読み違えている。仕様の原文を引く。
   - **T 試験の作り**: 値が試験の作り（ホストの構成、時間切れ、読み込みの推定）による。対照（同じ筋書きを既定の 2 サイトで動かす、など）で示す。
   - **U 未分類の食い違い**: 上のどれでもない。向き（隔離が緩む・厳しい）を書く。
   - 安全の配慮: 隔離が緩む向きの外れで、wpt.fyi で公開の失敗になっていないもの（K でないもの）は、リポジトリに書かず、ジョブの一時ディレクトリの `holdout/w2/held/` に分け、ユーザーに確かめる。未公開の欠陥について Web を検索しない。
3. **変異体の殺し**: 変異体 m は、ブラウザ b のある内側の行で、観測値が m の許す集合に含まれないときに殺される。前の和 K_prev(b, 設定) は、gen/、gen2/、redirect/ のコミット済みの行で、登録した変異体の集合を同じ規則で数えたもの（[driver/prev.sh](../models/site-isolation/holdout/driver/prev.sh)。結果は下の「登録の前にしたこと」）。WPT の 109 行（observe/）は含めない（gen2/ だけで、もとの 55 個について和と同じ 53 個と 55 個を殺している）。
4. **仮説の判定**（主の設定で）:
   - R1（保たれる）: 外れた行がすべて P か K。
   - R2（新しい外れ）: M か U の型が 1 つ以上ある。T は数えず、報告する。
   - R3（殺し方が変わる）: どちらかのブラウザで、K_prev に無い変異体を殺す。あわせて、族ごとに、前の族（gen/、redirect/）では殺せなかったが今回殺せたものを報告する。
5. **型の穴**: 動かした筋書きが実現した型を数える。N は (最上位, 1 段目, 2 段目) の 66 型、R は 5 + 33 + 269 型。すべて実現し、どの筋書きも観測できたら、関係の型の穴は閉じたとする。

## 登録の後で許さないこと

- 凍結したモデル、HoldDecode・HoldMutants・HoldEnum・HoldAllowed とその cfg、パラメータ、COI のモード、変異体の集合、観測の写し方、包含と殺しの規則、分類の区分、種、空間と選び方の定数を変えること。
- 値を見たあとで、筋書きや行を除くこと、繰り返しを足して値を選ぶこと。
- 許すこと（行えば「登録後の変更」に書く）: 試験のファイルが CRASH・ERROR・時間切れで観測を出さなかったとき、そのファイルを 1 回だけ動かし直す。観測を妨げる試験の作りの不具合（スクリプトの誤り）を直す。抜き出しや数えるスクリプトの、規則を変えない不具合を直す。

## 登録の前にしたこと

- 配管の確かめ: 2 つのサイトを足したサーバーで、c と d のホストの https の iframe と、c の http の popup が両方のブラウザで読み込めた（ping のページのオリジンと isSecureContext だけを見た。観測の写し方の値ではない）。
- 空の走り（種 1、空間を縮めたもの）: TLC の構文、選び方、行の書き出しが通ること。N と R の試験のファイルを 1 つずつ両方のブラウザで 1 回動かし、harness の状態（OK か）と OBS の行の数だけを見た。観測値は読んでいない。
- K_prev: [driver/prev.sh](../models/site-isolation/holdout/driver/prev.sh) で、gen/、gen2/、redirect/ のコミット済みの行から数えた（登録の前、2026-11-24）。NMs ∪ RMs の 141 個のうち、K_prev は {concrete, logical} で Chrome 128・Firefox 126、{concrete} で Chrome 131・Firefox 129。{concrete, logical} で K_prev に無いもの（Chrome）: coi-ignore-secure、false:coi-insecure、false:coop-one-unsafe、false:corp-first-pass、false:fetch-cors、true:blank-inherit、true:coep-cl-strips、true:coi-mode、true:hop-accumulate、true:hop-coep、true:hop-same-entry、true:hop-update、true:secure-ctx-top。Firefox はこれに neg:hop-update と false:hop-update を足したもの。{concrete} では coi-ignore-secure、false:coi-insecure、true:coi-mode が K_prev に入る。
- 登録の前の誤り: 上の一覧を数える道具（driver/score.py）を確かめるとき、空の走りの TLC の出力も一緒に渡してしまい、空の走り（種 1、N のファイル 1 つ、R のファイル 1 つ）で殺された変異体の数と、K_prev の外で殺された 2 つ（R の空の走りで coi-ignore-secure と false:coi-insecure）を見た。包含の数と外れの行は見ていない。これを見たあとで、登録の内容（規則、空間、選び方、変異体）は変えていない

## 道具の sha256

<!-- data-source: original（登録の時点の道具のハッシュ） -->
| ファイル（holdout/ からの相対パス） | sha256 |
| --- | --- |
| `HoldAllowed-N-both.cfg` | `d78ec95d130de8508692a6c561d893a56f572d2b26655f7e126bd27a1e3fb817` |
| `HoldAllowed-N-concrete.cfg` | `892918664666c924106d8446fd74a12f986ebfd6cb71ae22449f4f8b2ae0622a` |
| `HoldAllowed-N-noPP-both.cfg` | `c609a0401f66ad9b1c4ffc7c0002e3e1b73f4d4ac93a5337c7c85f819595409e` |
| `HoldAllowed-N-noPP-concrete.cfg` | `f8de062e5f48bf12b05b1bef479529a201630f5d2dbb49ff7073dc656987e9fc` |
| `HoldAllowed-R-both.cfg` | `9f85f4d746bb648aa021a91164143136c6d1a4481636f683e9050892c63b0b3a` |
| `HoldAllowed-R-concrete.cfg` | `76d72ae6eb76d30f6c31bdef6ad13860b9405e5d0e58edd5ca1eb3a0817a78fb` |
| `HoldAllowed.tla` | `284838e2f371ec10f504c6d2d64617d1e510fad0b3694ae3728b60b35ca64e96` |
| `HoldDecode.tla` | `e333b8e782991e0dffd29a05c281b48a12b6dc7cc023b0bed82e77ce6fc047a5` |
| `HoldEnum.tla` | `0f78575a26e8acc0515d32b678e15e3a8a35f21c85f9ed402ddc3364d7ff18e0` |
| `HoldMutants.tla` | `baa78831844f3dd5a5732d8d3253752c11b1102f5b297ac9ed786dbdb2904d80` |
| `HoldPrev-both.cfg` | `ae191b09a0a0dd32a4b26d7a40909322990c2f224987cefb4bde26fc5cbc44a6` |
| `HoldPrev-concrete.cfg` | `86ae342911bf6d800b2fc16e6c5526e771d2ead098fdd454dd9d844ae93313c9` |
| `HoldPrev.tla` | `34f313817b99c1c5d8be2f93ee7546896b189315e53563eb51e16e956e1b41ac` |
| `HoldPrevGen2-both.cfg` | `5014fd39c1f84a0ffb51552beaf5a180a887ba92117c87a9d0e2170afd4e9bcc` |
| `HoldPrevGen2-concrete.cfg` | `b376a661ef5976868a1c01a2e01546e2b78da32874e511b068917b33acc2bd49` |
| `HoldPrevGen2.tla` | `f2985b9ea478cfb04e4e189fce647c6e2de1890a0815471439f1fe8afa1b8d01` |
| `HoldPrevRedir-both.cfg` | `5014fd39c1f84a0ffb51552beaf5a180a887ba92117c87a9d0e2170afd4e9bcc` |
| `HoldPrevRedir-concrete.cfg` | `b376a661ef5976868a1c01a2e01546e2b78da32874e511b068917b33acc2bd49` |
| `HoldPrevRedir.tla` | `b40eed614c963d7bd1cbda40efe3c76edf81f9d39d6a8c24f7e07be69651acc6` |
| `SOURCE.toml` | `b8a00dc942a5d79b41d48b7549a31fa45d027f3d4016b578c8dc2cf802a78a42` |
| `driver/incontainer.sh` | `607ab9f2d9915e7e2f940d892bfbb0b7e243b602147125e3aa47254e0240395d` |
| `driver/mkrows.py` | `1a63f2ef07da26c80f44b530160e6d690e56644d1768c06fd6291f08980d75c9` |
| `driver/prev.sh` | `8bb7e59bb38bcc8423bc7bb7f327d08eae55c0da42c0508555f8c314ea1b6902` |
| `driver/run.sh` | `dbbd4bf762f684c29e604373de0dd6628e633d95066f4ceecc6b1f628def9903` |
| `driver/score.py` | `35b91150739620b7bbf514828dd3a51560792ace77dc5b85973edeb36c8baf15` |
| `driver/tlc.sh` | `fd789bafbd18cb41d9d6b4f45c2065eb8d3c17960fc86fdaf64b2c1afbe56843` |
| `gen_holdout.py` | `6de71f89ffcbbb4c0348af94e8702ab023b5fbaee82129cfba2d80c7f3702814` |
| `tests/resources/frame.py` | `da6c2db4cd1799e3677e15cdc6f20c9bf4aaecdb21503ddea7cce0bb752d8b1f` |
| `tests/resources/hobs.js` | `7df72d6e626817012ff025bc6bcfc3476a24b444f3ffae7f7ca68b80f95303d2` |
| `tests/resources/hop.py` | `303445e63b4c49d9a3da7ebeafd5d82dd93f4d71813f7b1f0a6dfeba594bcfb6` |
| `tests/resources/hrobs.js` | `32e21aafa499ff9b2fbc2559acdcc114ca0ef09bf5d8beab82e72da90faca68a` |
| `tests/resources/res.py` | `1445891bde3d3508e28184aeddb0a6240cb439d057e9f572b10b0ce2a192b456` |

## 限界（登録の時点で分かっていること）

- 軸と変異体はモデルの語彙から来る（C9 で別に扱う）。型はモデルが見る関係（同じオリジン、同じサイト、スキーム）で数え、同じホストの関係（細かい型）は数えない。
- 事前の選別は空間の一部（N は直積の 2 割、R の 2 段は 1/16）で、選別で等価に見える変異体は、その一部の上で等価なだけ。
- Origin-Agent-Cluster の値は、この 2 つの族では効かない。
- サイト c と d はコンテナの中のサーバーの設定で足したもので、証明書のホスト名は合っていない（既定の 2 サイトの扱いと同じく誤りを無視させる）。

## 登録後の変更

（無し）
