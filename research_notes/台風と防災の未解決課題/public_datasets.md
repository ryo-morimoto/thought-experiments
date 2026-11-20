# 台風・防災の思考実験に使える公開データの調査と、データポリシーへの適合

調査日: 2026-11-21。判定の基準は [DATA_POLICY.md](../../DATA_POLICY.md) と [data-policy.toml](../../data-policy.toml) である。

- 許可ライセンス（CC0, CC BY, PDL1.0, 政府標準 2.0 など）に入っているか
- 提供者が `publisher_types`（国・自治体・国際機関・学術機関・公的機関）に当たるか
- 規約に求償条項（弁償・求償・費用負担）がないか
- 著作物の部分（文章・画像・PDF など）を含むなら、提供者の権利処理済の明示があるか

規約本文は curl で取得し、タグを除いてから「弁償・求償・費用・賠償・損害・責任」で grep した。条文の引用は判断に要る数文に限る（DATA_POLICY 1.3）。

## 結論の一覧

- **取り込める**: 気象庁 台風の接近数・上陸数（CSV）、台風位置表（CSV）、RSMC ベストトラック（テキスト）、e-Stat 経由の水害統計調査（Excel）
- **条件付き**: 気象庁 過去の気象データ（フォーム経由の取得で、取得 URL を固定できない）、国土数値情報 洪水浸水想定区域（ライセンス表記の食い違いと都道府県ごとの条件）、消防庁 被害報（PDF のみ）
- **不可**: IBTrACS（ライセンス識別子がない）、防災白書 附属資料（防災庁サイトに利用許諾の表示がない。形式も PDF）、日本損害保険協会（民間で許諾の表示がない）、損害保険料率算出機構（民間で、転載に事前連絡が必要）

---

## 1. 気象庁

規約は登録済みの `jma-pdl-1.0` を使う（https://www.jma.go.jp/jma/kishou/info/coment.html ）。取り込み済みの `data/jma-typhoon-generation` と同じ扱いでよい。

### 1.1 台風の接近数・上陸数（・発生数は取り込み済み）

- 統計ページ: https://www.data.jma.go.jp/typhoon/statistics/index.html （1951 年以降）
- 直接 URL（`/yoho/typhoon/...` は `/typhoon/...` へ 301 で転送される。正規の URL は後者）
  - 接近数（全国）: https://www.data.jma.go.jp/typhoon/statistics/accession/accession.csv （2,014 B、Last-Modified 2026-02-27）
  - 上陸数: https://www.data.jma.go.jp/typhoon/statistics/landing/landing.csv （1,719 B、Last-Modified 2026-02-27）
  - 発生数: https://www.data.jma.go.jp/typhoon/statistics/generation/generation.csv （2,279 B。取り込み済み）
- 形式: CSV、**Shift_JIS**。列は「年, 1月…12月, 年間」。1951 年から。
- 更新: 年 1 回（3 ファイルとも 2026-02-27 更新。前年分の確定時と見られる）
- 接近数の地方別（沖縄・九州南部・関東甲信など）は HTML の表だけで、CSV がない（https://www.data.jma.go.jp/typhoon/statistics/accession/index.html のリンクは `okinawa.html` などの HTML と `kanshotou.pdf` だけ）。地方別を使うなら HTML から表を起こすことになるので、取得手段の記録に注意する。
- 発行者: 気象庁 → `government`。数値の表で `content_kind = ["table"]`、著作物の部分なし。PDL1.0 では数値データは規約の適用外（`non_copyrightable = "excluded"`）。
- **判定: 取り込める**

### 1.2 台風位置表

- 一覧: https://www.data.jma.go.jp/typhoon/position_table/index.html （2001 年以降、年ごと）
- 直接 URL: `https://www.data.jma.go.jp/typhoon/position_table/table{YYYY}.csv`（例: table2024.csv は 57,380 B）。台風ごとの PDF（`../data/T2401.pdf` など）もあるが、CSV を使う。
- フォーマット: https://www.data.jma.go.jp/typhoon/position_table/format_csv.html 。列は年・月・日・時（UTC）・台風番号・台風名・階級・緯度・経度・中心気圧・最大風速（ノット）・50KT/30KT 暴風域・上陸フラグ。CSV、**Shift_JIS**。
- 修正履歴: https://www.data.jma.go.jp/typhoon/position_table/syuusei_rireki.csv 。一覧ページに「データについては、見直しにより修正されることがあります」とある。sha256 で固定するなら、取得日と修正履歴の版を記録する。
- 更新: 当年分は台風の発生に応じて随時、過去分は修正があったとき。
- **判定: 取り込める**（`table`、jma-pdl-1.0）。PDF 版は画像・PDF の扱いになるので使わない。

### 1.3 RSMC Tokyo ベストトラック

- ページ: https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/besttrack.html
- 直接 URL
  - 全期間: https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst_all.zip （748,952 B。中身は `bst_all.txt` 6,046,926 B、73,743 行。1951〜2026 年）
  - 当年: https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/bst2026.txt （56,826 B）
  - いずれも Last-Modified 2026-11-16
- フォーマット: https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/e_format_bst.html 。固定長テキスト、**ASCII**（ヘッダ行 `66666 ...` とデータ行）。修正履歴 CSV: https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Besttracks/history_of_revision.csv
- 更新: 台風シーズン中は随時（当年分）。過去分は再解析で修正される。
- **規約**: ページ末尾の「Legal Notice」は https://www.jma.go.jp/jma/en/copyright.html を指す（RSMC 独自の条件はない。https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/trackarchives.html も同じリンク）。英語版の規約は日本語版と同じ PDL1.0 準拠で、次の文言がある。

  > Information made available on the Japan Meteorological Agency website (hereinafter referred to as "Content") may be used in accordance with the terms and conditions of use stipulated in Public Data License (Version 1.0), unless otherwise indicated by a specific rights notice.

  （https://www.jma.go.jp/jma/en/copyright.html ）。indemnify・reimburse・compensat の語はなく、damage は Google Analytics に関する気象庁の免責 1 件だけ（日本語版と同じ）。気象業務法 17 条・23 条の注意も日本語版と同じ。
- 注意: 規約の URL が日本語版と別なので、`jma-pdl-1.0` の `url`（coment.html）と `license_url` が一致しない。英語版を根拠にするなら `[terms]` に英語版を登録するか、日本語版の規約を根拠に書く（同じ気象庁サイトの規約なので後者で足りると考えるが、判断が要る）。
- **判定: 取り込める**（`table`、jma-pdl-1.0）。ベストトラックは国内の台風位置表と値が一致しない部分がある（RSMC は国際向け）ので、どちらを使うかを実験側で決める。

### 1.4 過去の気象データ（降水量など）

- 検索（HTML）: https://www.data.jma.go.jp/stats/etrn/index.php
- ダウンロード: https://www.data.jma.go.jp/risk/obsdl/index.php 。CSV の形式説明は https://www.data.jma.go.jp/risk/obsdl/top/help3.html （1 行目にダウンロード時刻、表題行が複数行、品質情報・均質番号の列が付く）。CSV は Shift_JIS。
- 規約は気象庁サイトの規約（jma-pdl-1.0）。数値データで著作物の部分なし。
- 問題: ダウンロードは画面で地点・項目・期間を選んでからフォーム送信する方式で、ファイルごとの固定 URL がない。`SOURCE.toml` の `url` と証拠（規約ページとデータのバイト列）をどう残すかを決める必要がある。また 1 行目にダウンロード時刻が入るので、同じ条件でも取得ごとに sha256 が変わる。
- 一覧ページに観測所ごとの欠測・修正のお知らせが載る（例: 「アメダスの郡家観測所（兵庫県）において、湿度計の不具合により…湿度データを欠測としました」https://www.data.jma.go.jp/stats/etrn/index.php ）。
- **判定: 条件付き**（規約上は問題なし。取得 URL と証拠の残し方を決めてから）

## 2. IBTrACS（NOAA NCEI）

- ページ: https://www.ncei.noaa.gov/products/international-best-track-archive
- 直接 URL（CSV）: https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/
  - 北西太平洋: `ibtracs.WP.list.v04r01.csv`（114,737,486 B、Last-Modified 2026-11-17）
  - 全球: `ibtracs.ALL.list.v04r01.csv`（333,282,096 B）
  - ほかに `since1980`・`last3years`・netCDF・shapefile
- 形式: CSV（ASCII、1 行目が列名 `SID,SEASON,NUMBER,BASIN,...`、2 行目が単位行）。更新: 「updated three times a week」（同ページ）。
- **規約**: 同ページの Terms of Use は

  > The IBTrACS data usage policy follows the World Data Center for Meteorology (WDC), which provides full and open access to the data. … We also use the World Meteorological Organization's Resolution 40 policy as the guide for commercial use of IBTrACS data.

  （https://www.ncei.noaa.gov/products/international-best-track-archive ）。ISO メタデータ（https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C01552/xml ）の `useConstraints` は `otherRestrictions` で、中身は引用の依頼（Gahtan et al. 2024, doi:10.25921/82ty-9e16 と Knapp et al. 2010）と免責（"Users assume responsibility to determine the usability of these data"）だけ。**CC0 などのライセンス識別子はどこにもない**。弁償・求償にあたる条項はない。
- 発行者: NOAA NCEI（米国の国の機関）だが、中身は各国の RSMC（気象庁を含む）のデータを合成したもの。「We have agreements from the Regional Specialized Meteorological Centers … to make IBTrACS data open for distribution」とあり、権利の出所は各機関に分かれる。商用利用は WMO 決議 40 に委ねている。
- **判定: 不可**（許可リストのライセンスに当たる表示がない。「full and open access」は二次利用・再配布の条件を明文化していない）。北西太平洋の経路は気象庁ベストトラック（1.3）で代替できる。使いたい場合は、米国連邦政府の著作物（17 U.S.C. §105）として扱えるか、他機関由来の部分をどう扱うかを別に検討してから、規約を登録する単独のコミットが要る。

## 3. 消防庁 災害情報（被害報）

- 一覧: https://www.fdma.go.jp/disaster/info/ （年別アーカイブ `/disaster/info/1995/` から）
- 形式: 報ごとの PDF のみ。例: 「令和8年台風第15号による被害及び消防機関等の対応状況（第5報）」 https://www.fdma.go.jp/disaster/info/items/20260810taifu15gou5.pdf （80,026 B、1 ページ、画像なし、都道府県別の人的・住家被害の表）。冒頭に「これは速報であり、数値等は今後も変わることがある」。
- 規約: https://www.fdma.go.jp/about/others/post3.html#copyright 。「特記されていない限り消防庁に帰属し、権利表記の記載がない限り『公共データ利用規約（第1.0版）』（PDL1.0）が適用されています」。弁償・求償・費用・賠償の語なし。第三者の権利は利用者の責任（PDL1.0 の 1.2 と同文）。
- 発行者: 消防庁 → `government`。
- 問題: (1) PDF は `content_kind` にかかわらず著作物の部分として扱われ、PDL1.0 は第三者の権利処理を利用者に任せるので、提供者の権利処理済の明示（`third_party_evidence`）が要る。消防庁の規約ページにそうした明示はない。(2) 規約の URL が消防庁独自なので、`[terms]` に消防庁版を登録する必要がある。
- **判定: 条件付き（現行ルールでは PDF のままは取り込めない）**。表の数値は著作物でないので、少量を文中で出典つきで参照するのは可。ファイルとして使うなら、PDF の扱いをポリシー側で決める（数値表だけの PDF の例外を設けるか）必要がある。

## 4. 防災白書（内閣府 → 防災庁）

- 2026-11-02 に防災庁が設置され、https://www.bousai.go.jp/ は「防災庁ウェブサイト」になった（https://www.bousai.go.jp/notice.html ）。旧「内閣府防災情報のページ」は WARP で見られる（https://www.bousai.go.jp/juyou/content_migration.html ）。
- 附属資料: https://www.bousai.go.jp/kaigirep/hakusho/r7fuzoku.html 。「自然災害による死者・行方不明者数」（`pdf/r7_fuzoku2.pdf`、76.0KB）、「施設関係等被害額及び同被害額の国内総生産に対する比率の推移」（`pdf/r7_fuzoku3.pdf`）など。**PDF のみ**。
- 規約: 「このホームページについて」 https://www.bousai.go.jp/notice.html には、リンク・免責・プライバシーの記載だけがあり、**コンテンツの利用許諾（PDL・政府標準利用規約・CC BY）の記載がない**。旧 URL https://www.bousai.go.jp/site/policy.html は 404。免責の文に「内閣府としては責任を負いかねます」と旧組織名が残っており、移行中と見られる。弁償・求償の条項はない。
- **判定: 不可**（利用条件が明文化されていない。DATA_POLICY の表明 2）。防災庁の利用規約が公開されたら再確認する。死者・行方不明者数の元は消防庁などの資料なので、元の統計を当たる方がよい。

## 5. e-Stat と 国土交通省 水害統計調査

### 5.1 e-Stat の規約

- https://www.e-stat.go.jp/terms-of-use 。「政府標準利用規約（第2.0版）に準拠しています」「CC BY と互換性があり」。「数値データ、簡単な表・グラフ等は著作権の対象ではありませんので、これらについては本利用ルールの適用はなく、自由に利用できます」。弁償・求償・費用・賠償の語なし（免責は「国は…何ら責任を負うものではありません」だけ）。第三者の権利は利用者の責任。
- 注意: 登録済みの `jp-gov-std-2.0` の `url` はデジタル庁のページなので、e-Stat の規約を `license_url` にするなら `[terms]` に e-Stat 版を登録する（内容は政府標準 2.0 と同じ性質）。API と統計地理情報システムには別ルールがある（同ページ別紙）。

### 5.2 水害統計調査

- e-Stat: https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00600590 （政府統計コード 00600590）。年ごとに 76〜79 ファイル。例: 令和5年は https://www.e-stat.go.jp/stat-search/files?page=1&toukei=00600590&tstat=000001222080 、全国の被害の表は Excel 28 件・PDF 12 件。
- 直接 URL の例: https://www.e-stat.go.jp/stat-search/file-download?statInfId=000040301907&fileKind=0 （`hyo1.xlsx`、31,285 B、「令和５年水害被害一覧（表-1）」）。`fileKind=0` が Excel、`fileKind=2` が PDF。
- 国交省の説明ページ: https://www.mlit.go.jp/river/toukei_chousa/kasen/suigaitoukei/index.html （規約は国交省サイトの PDL1.0。https://www.mlit.go.jp/link.html 。弁償・求償の語なし）。昭和 36 年から毎年。
- 更新: 年 1 回の確報。過去分の訂正が多い（「『平成14年水害統計』～『令和3年水害統計』の基本表について、令和6年9月18日修正しました」など、同ページ）。令和6年分の確報は公表遅延中（同ページ）。
- 発行者: 国土交通省 → `government`。Excel の数値表で `content_kind = ["table"]`。
- **判定: 取り込める**（e-Stat から Excel を取り、`[terms]` に e-Stat の規約を登録してから）。PDF の表は使わない。訂正が多いので取得日と公開（更新）日を必ず記録する。

## 6. 国土数値情報（洪水浸水想定区域など）

- 規約: https://nlftp.mlit.go.jp/ksj/other/agreement.html 。「権利表記の記載がない限り…『公共データ利用規約（第1.0版）』（PDL1.0）が適用されています」。2026-03-23 施行。弁償・求償・費用・賠償の語なし。
- 旧約款準拠版（「商用可」「非商用」と、条件の記載がないデータに適用）: https://nlftp.mlit.go.jp/ksj/other/agreement_02.html 。第5条は「国土数値情報を利用することにより生じた利用者又は第三者の損害については、利用者がその全ての責任を負うものとし、国土交通省及び原典資料の提供者は一切の責任を負いません」で、免責であって求償（提供者の費用を利用者に負担させる）ではない。費用は「通信費等の費用は、利用者の負担」だけ。ただし「非商用」区分は許可リストに入らない。
- 洪水浸水想定区域（河川単位）: https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A31a-2025.html 。2021〜2025 年度は「オープンデータ（CC_BY_4.0）」、2019・2020 年度は整備局・一部の道県が CC BY 4.0、島根県・岡山県は「CC_BY_4.0（一部制限）」、2012 年度は「非商用」。ページ冒頭に「国土数値情報ダウンロードサイトコンテンツ利用規約のほか、都道府県毎に定められた利用条件を必ず遵守するようにしてください」。全国ファイルの例: `data/A31a/A31a-25/A31a-25_81_10_GML.zip`（336.6MB）。GML・Shapefile、座標系 JGD2011。
- 洪水浸水想定区域（メッシュ）: https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A31b-2025.html 。「オープンデータ（CC_BY_4.0）」。例: `data/A31b/A31b-25/A31b-25_10_3927_GML.zip`（1.28MB、メッシュ単位）。
- 発行者: 国土交通省 → `government`。ただし原典は地方整備局と都道府県で、都道府県の部分は国から見て第三者。
- 問題:
  1. 個別ページの表示は「CC BY 4.0」、サイト規約は「PDL1.0」で、宣言値の付け方が二通りある。PDL1.0 は CC BY 4.0 互換なので矛盾ではないが、`license` と `[concluded]` をどちらで揃えるか決める必要がある（`license_url` は規約ページなので PDL1.0 で揃えるのが素直）。
  2. 都道府県ごとの条件（島根県オープンデータポータルの規約など）は別途読む必要がある。島根・岡山を含む年度・範囲は避けるのが簡単。
  3. `content_kind` は `geo-vector` で著作物の種類には入らないが、ポリゴンが地図表現として著作物性を問われる余地は残る（ポリシー上は geo-vector は creative_kinds 外）。
- **判定: 条件付き**（国管理河川・CC BY 4.0 表示の範囲に限り、都道府県の条件を確認してから。2012 年度の「非商用」は不可）。サイズが大きいので `committed = false`（DVC）にする候補。

## 7. 損害保険の統計（民間）

### 7.1 日本損害保険協会「自然災害での支払額」

- https://www.sonpo.or.jp/report/statistics/disaster/ 。「過去の風水害等による高額支払保険金事例」などは PDF（例: `/report/statistics/disaster/ctuevu000000530r-att/c_fusuigai.pdf`）。
- 規約: https://www.sonpo.or.jp/notice/index.html 「著作権・リンク等について」。免責とリンクの記載だけで、利用許諾の記載はない。
- 発行者: 一般社団法人（民間）→ `publisher_types` に入らない。
- **判定: 不可**（提供者の種別が対象外、利用許諾の記載がない、PDF）。被害額の規模感を文中で 1〜2 件、出典つきで触れる程度にとどめる。

### 7.2 損害保険料率算出機構（GIROJ）

- 調査時、https://www.giroj.or.jp/ は「緊急メンテナンスのため、当機構のウェブサイトは現在利用できない」状態だった。サイトポリシーは Internet Archive の 2026-06-14 の写し（https://web.archive.org/web/20260614200549/https://www.giroj.or.jp/sitepolicy.html ）で確認した。

  > 本サイトに掲載されているコンテンツ（文字・写真・画像や情報など、作成・編集された内容すべて）の著作権は、当機構その他の著作権者に帰属しています。コンテンツの使用・転載等を行う場合には、事前に当機構の問合せ先へご連絡ください。

- 発行者: 損害保険料率算出団体に関する法律に基づく民間の法人 → `publisher_types` に入らない。
- **判定: 不可**（二次利用の許諾がなく、事前連絡が必要）。

---

## 補足: 規約の登録が要るもの

取り込むときに `data-policy.toml` の `[terms]` へ単独のコミットで登録が要りそうなもの（このノートでは編集していない）。

- e-Stat 利用規約（政府標準 2.0 準拠、求償なし）: https://www.e-stat.go.jp/terms-of-use
- 気象庁英語版規約（RSMC ベストトラックの Legal Notice の先）: https://www.jma.go.jp/jma/en/copyright.html 。日本語版で足りるなら不要
- 国土数値情報ダウンロードサイト利用規約（PDL1.0 準拠、求償なし）: https://nlftp.mlit.go.jp/ksj/other/agreement.html
- 消防庁（PDL1.0 準拠、求償なし）: https://www.fdma.go.jp/about/others/post3.html （PDF の扱いが決まった場合）
