# 台風（熱帯低気圧）に関する未解決の科学的課題：社会的価値の高い思考実験の候補

調査日: 2026-11-21。北西太平洋（WNP）と日本への関係を優先した。
一次資料（IPCC AR6 WG1 の PDF、論文の abstract、Crossref の書誌情報、行政文書の PDF）を優先した。今回のセッションで本文や abstract を直接確認できず、検索結果の要約にだけ頼った項目には【未検証】と付けた。
引用は DATA_POLICY.md 1.3 に従い、論じるのに必要な数文に限った。

確認に使った PDF の sha256（ダウンロード日 2026-11-21）:

- IPCC AR6 WG1 第11章 PDF（[URL](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)）: `d0dc4fae531a7b6a76a456cb12db9c7d68099265e377973d508484c3289ddce1`
- IPCC AR6 WG1 SPM PDF（[URL](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf)）: `37c9fa760757524c8d69630a89cecab9ebcacb66786970a3439da0619875e446`
- 国土交通省「高潮浸水想定区域図作成の手引き Ver.2.11」（[URL](https://www.mlit.go.jp/river/shishin_guideline/kaigan/takashioshinsui_manual.pdf)）: `86bf32fe90a87cbc6d4f2f1ad5d71edfedd36ad33320ca2bc78877ca7c72388e`
- 国土交通省「気候変動を踏まえた治水計画のあり方 提言（改訂版）」（[URL](https://www.mlit.go.jp/river/shinngikai_blog/chisui_kentoukai/pdf/r0304/01_teigen.pdf)）: `4a9a49fd97e05db14439c283a8c59321469d8969d9337cc3337bbe0dd6bb2027`
- ESCAP/WMO Typhoon Committee「Harmonization of Tropical Cyclone Intensity Analysis」最終報告（[URL](https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Final_Report_Harmonization_Tropical_Cyclone_Intensity_Estimate.pdf)）: `b92615bceb9b36a44b75bdd8c7ade99edcf92107202482ca80392f0be53c1af9`

---

## 0. 出発点：IPCC AR6 WG1 の確信度

以下は第11章 PDF と SPM PDF の本文から直接確認した。ページ番号は報告書の通し番号。

### 観測（過去）

- SPM A.3.4。全カテゴリーの発生数の長期傾向は「低確信度」。強い台風の割合と WNP の最大強度緯度は likely / very likely だが、「内部変動だけでは説明できない」部分は medium confidence にとどまる — [SPM PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf)
  > "It is likely that the global proportion of major (Category 3–5) tropical cyclone occurrence has increased over the last four decades, and it is very likely that the latitude where tropical cyclones in the western North Pacific reach their peak intensity has shifted northward; these changes cannot be explained by internal variability alone (medium confidence). There is low confidence in long-term (multi-decadal to centennial) trends in the frequency of all-category tropical cyclones."
- SPM A.3.4 の続き。台風の豪雨は人為的に増えている（high confidence）が、全球のトレンド検出はデータの制約で妨げられている — [SPM PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf)
  > "...human-induced climate change increases heavy precipitation associated with tropical cyclones (high confidence), but data limitations inhibit clear detection of past trends on the global scale."
- 11.7.1.2（p.1585）。best-track の長期トレンドの大半は低確信度。トレンドが無いという意味ではない、と明記している — [第11章 PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
  > "There is low confidence in most reported long-term (multi-decadal to centennial) trends in TC frequency- or intensity-based metrics due to changes in the technology used to collect the best-track data. This should not be interpreted as implying that no physical (real) trends exist..."
- 11.7.1.2 のまとめ（p.1587）。Cat 3–5 の割合と急速強化（RI）の頻度の増加は likely。WNP の最大強度位置の極向き移動は very likely。米国での移動速度の低下は likely — [第11章 PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- 第11章 Executive Summary（p.1519）。上の変化について「自然変動だけでは説明できない」は medium confidence。米国以外の地域で同様の傾向があるという証拠は「robust ではない」 — [第11章 PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
  > "Evidence of similar trends in other regions is not robust. The global frequency of TC rapid intensification events has likely increased over the past four decades. None of these changes can be explained by natural variability alone (medium confidence)."
- 11.7.1.4 のまとめ（p.1589）。個別の強い台風のイベントアトリビューションは、強化（intensification）については「限られた証拠（limited evidence）」、豪雨については high confidence。米国の移動速度低下に人為的寄与があるのは more likely than not — [第11章 PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
  > "Event attribution studies of specific strong TCs provide limited evidence for anthropogenic effects on TC intensifications so far, but high confidence for increases in TC heavy precipitation."
- 図11.20 の説明文（p.1586）。各項目の過去と将来の確信度が並んでいる。過去の雨量増加は「low confidence due to lack of reliable data」。WNP の極向き移動は過去・将来とも medium。移動速度の低下は過去が medium、将来が「low confidence due to lack of directed studies」 — [第11章 PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)

### 予測（将来）

- SPM B.2.4。強い台風（Cat 4–5）の割合と最強台風の最大風速は増加する（high confidence） — [SPM PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf)
- 第11章 ES（p.1519）。全球の発生数は「減少するか変わらない」（medium confidence） — [第11章 PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- 11.7.1.5（p.1590）。発生数の将来変化を説明する理論がない。符号すらモデル間で割れている — [第11章 PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
  > "There is not an established theory for the drivers of future changes in the frequency of TCs."
- 11.7.1.5 のまとめ（p.1592）。WNP の一部の領域で Cat 4–5 の頻度が増えるのは likely。WNP の最大強度位置の極向き移動の継続も likely — [第11章 PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- 11.7.1.5（p.1591）。移動速度の将来変化には「明確なコンセンサスがない」。台風のサイズの変化は大きさも符号も不確実 — [第11章 PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- ES の複合事象（p.1519）。複合洪水（高潮・豪雨・河川流量）の確率は一部地点で増加（medium confidence）。海面上昇と台風降雨の強化により今後も増加（high confidence） — [第11章 PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)

### 日本の評価（文部科学省・気象庁『日本の気候変動2025』第7章）

検索結果と WebFetch の要約から確認した。原文の一字一句は確認していない【一部未検証】。

- 台風の発生数と日本への接近数には、1951年以降で長期的な変化傾向が確認できない — [日本の気候変動2025 本編 第7章](https://www.data.jma.go.jp/cpdinfo/ccj/2025/html_honpen/cc2025_honpen_7.html)
- 日本付近の台風強度は強まり、台風に伴う降水量も増加すると予測される（確信度は中程度） — 同上
- 4℃上昇の実験（5km メッシュ）では、10年に1回の台風による最大24時間降水量が約800mmから約1000mmに増える（図7-2.1）【数値は要約経由で、未検証】 — 同上

---

## 1. 観測データの問題（すべての課題の土台）

### 1.1 航空機観測の終了と Dvorak 法への切り替え

- WNP では1987年に航空機観測が終了した。それ以降、JMA と JTWC は静止衛星画像による Dvorak 法で最大風速を推定している — Kawabata, Shimada, Yamaguchi (2023) JMSJ 101(6), 435–443, [doi:10.2151/jmsj.2023-025](https://www.jstage.jst.go.jp/article/jmsj/101/6/101_2023-025/_html/-char/en)
- 同論文によると、JMA の Dvorak 再解析（1987〜2016年）では、強い台風に統計的に有意な増加傾向は見られなかった。再解析の時間的均質性は best-track より「much better」と期待される — 同上
- 同論文では、best-track の生涯最大強度（LMI）が 80±10 kt の台風のうち約79%が、再解析ではより高い LMI になった。強い台風の割合は 43.7%（1987〜2001年）から 49.6%（2002〜2016年）に変化した。いずれも WebFetch の要約から取った数値【原文の表で未照合】 — 同上
- Mei and Xie (2016) が使ったデータは、1977〜1986年が主に航空機観測、1987〜2014年が主に Dvorak 推定に基づくため、時間的に不均質だという指摘がある【未検証：検索要約のみ。Knaff の未公刊原稿】 — [Knaff, pressure-based analysis 原稿](https://ramsdis.cira.colostate.edu/rammb/resources/docs/Knaff_WP-Reanalysis-Pressure-v03.docx)

### 1.2 予報機関の間の不一致（JMA / JTWC / CMA / HKO）

- ESCAP/WMO 台風委員会の報告（2017年1月、JMA の小出直久が提出）は、2010年の評価報告書の結論を引用している。「best-track データセット間の違いのため、WNP の強度の長期トレンドは自然変動と比べて説得力をもって検出できない」 — [Harmonization 最終報告 PDF](https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/Final_Report_Harmonization_Tropical_Cyclone_Intensity_Estimate.pdf)
- 同報告によると、2010年の Typhoon Megi（1013）の事例研究では、最大風速の大きな差は主に CI 数から最大風速への換算表の違いによるものだった — 同上
- 同報告は 2004〜2013年の CI 数を4機関で比較した。結果は次のとおり — 同上
  > "In most cases, CI-number differences are within 0.5. HKO and JTWC have positive biases in comparison to RSMC Tokyo, while little bias is found between CMA and RSMC Tokyo. ... discrepancies as large as 1.5 or greater were occasionally observed."
- 同報告によると、CMA は2012年まで簡易 Dvorak 法を使っていた。そのため 2013年以降だけを個別解析に使った。CI 数の差が 2.0 以上の 17 個の台風を個別に再解析している — 同上
- 1970年代以降の強度トレンドは、JTWC を使うと増加、RSMC Tokyo と HKO を使うと減少と、符号が逆になる。Wu, Yeung, Chang (2006) は RSMC Tokyo と HKO のデータでは PDI の増加が見られないと報告した — Eos 87, 537–538, [doi:10.1029/2006EO480001](https://doi.org/10.1029/2006EO480001)【本文未確認。書誌は Crossref で確認、内容は検索要約】
- 2026年7月のプレプリント TyRA（Ito, Aizawa, Shimada, Kawabata, Yamaguchi）は、1981〜1986年の航空機観測で Dvorak の CI 数から中心気圧への推定式を較正し、1987〜2024年を再解析した。結果は次のとおり — [arXiv:2607.11220](https://arxiv.org/abs/2607.11220)【プレプリント、査読前】
  - 強い台風の数は「わずかに減少」したが、統計的に有意ではない
  - 1980年代後半〜2000年代半ばは、JTWC が TyRA より強い台風を多く、RSMC Tokyo が少なく記録している
  - WNP 東部では近年弱まっており、ある程度有意。台風の発生後の平均年齢の低下によると説明している
  - 急速強化（RI）については3つのデータセットの間で差が大きい
  - 2000年代半ばに RSMC Tokyo の強度予報誤差が増えたことの一部は、best-track の品質の変化で説明できる

### 1.3 統合データセットの注意書き

- IBTrACS（v04r01、2024年6月）は、v03r01 以降、各機関の値を共通の 10 分平均風速に換算せずにそのまま収録している。風速の平均時間は機関ごとに異なる — [NOAA NCEI IBTrACS](https://www.ncei.noaa.gov/products/international-best-track-archive)
- 1950年より前の一部の台風は、出典間で照合されておらず、一つの台風が複数のトラックとして現れることがある — 同上

### 1.4 「データ問題に強い指標」も争点になっている

- IPCC は、最大強度の緯度と移動速度を「frequency や intensity よりデータ問題の影響を受けにくい」指標として紹介している（11.7.1.2）。ただし移動速度の低下については、Moon et al. (2019) と Lanzante (2019) が衛星データの導入による経路の南北シフトのアーティファクトだと反論した、とも書いている — [第11章 PDF p.1587](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)

---

## 2. 課題ごとのノート

各課題に次の4項目を書く。(a) 何が未解決か、(b) 誰が何を決めるのに使うか、(c) どんな推論で進められるか、(d) 関係する公開データ。

### 課題A：WNP の「強い台風の割合」は本当に増えているのか（データセット依存）

(a) 未解決の点

- IPCC は全球の Cat 3–5 の割合の増加を likely とした。根拠の中心は Kossin et al. (2020) PNAS（1979〜2017年の均質化データで、major TC の超過確率が10年あたり約6%増加）である — [第11章 PDF p.1585](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf), [doi:10.1073/pnas.1920849117](https://doi.org/10.1073/pnas.1920849117)
- 一方、WNP に限ると、JMA の Dvorak 再解析では有意な増加がない（Kawabata et al. 2023）。TyRA では有意でない減少になった（プレプリント）。全球の結論と、日本に直接関わる海域の結論が食い違っている — [doi:10.2151/jmsj.2023-025](https://doi.org/10.2151/jmsj.2023-025), [arXiv:2607.11220](https://arxiv.org/abs/2607.11220)
- 『日本の気候変動2025』は、1980年代半ば以降の北西太平洋で Cat 4–5 の発生数が増加していると評価している（確信度は中程度）。ただし評価が十分ではないとの注意書きがある【要約経由、未検証】 — [日本の気候変動2025 第7章](https://www.data.jma.go.jp/cpdinfo/ccj/2025/html_honpen/cc2025_honpen_7.html)

(b) 社会的価値

- 「強い台風が増えた」という認識は、高潮・暴風の設計外力、損害保険の料率（再保険のカタストロフモデル）、自治体の避難計画の想定の改訂を正当化する根拠として引用されやすい。強度の観測値が機関によって 0.5〜2.0 CI 数ずれるなら、どのデータを採るかで政策の根拠が変わる。

(c) 思考実験の進め方

- 同じ台風に対して、機関ごとの換算表（CI 数から風速、10 分平均と 1 分平均）を入れ替えたとき、「猛烈な台風」の数とトレンドの符号がどう変わるかを推論する。
- 「1987年に観測手段が変わった」という条件を固定したとき、どの統計量（割合、LMI の分位点、強度を経ない中心気圧）なら変化を越えて比較できるかを攻める。
- 全球では増加、WNP では有意でないという食い違いは、(i) WNP の自然変動（PDO など）、(ii) 機関間の較正差、(iii) 全球と海域で検出力が違うことのどれで説明できるか。仮説ごとに観測されるはずの痕跡を書き出す。

(d) 公開データ

- IBTrACS — [NCEI](https://www.ncei.noaa.gov/products/international-best-track-archive)
- RSMC Tokyo best track — [JMA](https://www.jma.go.jp/jma/jma-eng/jma-center/rsmc-hp-pub-eg/besttrack.html)
- JTWC best track【2026-11-21 時点で metoc.navy.mil へのアクセスは 403。入手経路は未検証】
- CMA best track（tcdata.typhoon.org.cn）【このセッションでは接続できず、未検証】
- HURSAT（均質化の基礎になった衛星画像） — [NCEI](https://www.ncei.noaa.gov/products/hurricane-satellite-data)
- JMA の Dvorak 再解析と TyRA のデータが公開されているかは【未確認】。

### 課題B：台風の発生数は減っているのか、将来どうなるのか

(a) 未解決の点

- Chand et al. (2022, Nature Climate Change 12, 655–661) は、20世紀再解析（20CR）から再構成した年間発生数をもとに、20世紀に全球と6海域で発生数が減少したと報告した（北大西洋は例外）。NOAA の紹介記事では、全球の年間発生数は1850〜1900年と比べて約13%減少している — [doi:10.1038/s41558-022-01388-4](https://doi.org/10.1038/s41558-022-01388-4), [NOAA Research](https://research.noaa.gov/?p=1072)【NOAA 記事は検索要約経由】
- Emanuel (2024, Nature Climate Change 14, 143–145, Matters Arising)「Limitations of reanalyses for detecting tropical cyclone trends」は、この減少は主に第二次世界大戦後に地上気圧観測の密度が増えたことによるアーティファクトだと反論した。Chand et al. の Reply（同 14, 146–147）は、Emanuel の方法は弱すぎ・小さすぎ・短命すぎる循環まで拾ってしまうと応じた — [doi:10.1038/s41558-023-01879-y](https://doi.org/10.1038/s41558-023-01879-y), [doi:10.1038/s41558-023-01880-5](https://doi.org/10.1038/s41558-023-01880-5)【書誌は Crossref で確認。双方の主張は検索要約経由】
- 理論面では、Sobel et al. (2021, Earth's Future) が「地球上で年に平均いくつの台風が発生するか、温暖化でそれがどう変わるかを説明する受け入れられた理論はない」と述べている — [doi:10.1029/2021EF002275](https://doi.org/10.1029/2021EF002275)【abstract の要約経由】
- 予測面では、高解像度モデルの多くは減少を予測する。一方、Emanuel の統計力学的ダウンスケーリング（seed 率一定を仮定）は増加を示す。IPCC は符号の不一致と、その仕組みを説明できないこと自体を「process understanding の欠如」としている — [第11章 PDF p.1590](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf), Emanuel (2021) J. Climate [doi:10.1175/JCLI-D-20-0367.1](https://doi.org/10.1175/JCLI-D-20-0367.1)
- d4PDF（60km、5000年規模のアンサンブル）では、4K 昇温で全球の発生数が33%減少する。一方で、Cat 4–5 の発生数も全球で有意に減少した。これは「強い台風の割合が増える」とは別の話で、絶対数としては先行研究と逆の結果になっている。ただし日本の南を含む広い範囲で Cat 4–5 の出現は増える — Yoshida et al. (2017) GRL [doi:10.1002/2017GL075058](https://doi.org/10.1002/2017GL075058)（abstract を Crossref で確認）

(b) 社会的価値

- 「数は減るが強いものは増える（fewer but stronger）」が正しいかどうかで、「年に何回備えるか」（訓練の頻度、毎年の運用コスト）と「1回の最悪にどう備えるか」（設計外力）の配分が変わる。数が減ることが市民の油断（正常性バイアス）を強める、という論点も立つ（これは推論であり、出典はない）。

(c) 思考実験の進め方

- 「数の減少」と「強いものの割合の増加」は、両方が真でも、強い台風の絶対数は増える場合も減る場合もある（Yoshida et al. 2017 は減少）。防災上意味があるのは割合か絶対数か、地点ごとの再現期間か。指標の選び方で結論がどう逆転するかを詰める。
- 観測密度が増えると発生数が見かけ上変わる、という Emanuel の批判を一般化する。「観測網の変化が単調なら、どの指標にどちら向きのバイアスが乗るか」を推論で整理する。

(d) 公開データ

- NOAA-CIRES-DOE 20CR — [PSL](https://psl.noaa.gov/data/20thC_Rean/)
- IBTrACS
- d4PDF — [d4PDF 公式](https://www.miroc-gcm.jp/d4PDF/)。配布は DIAS — [DIAS](https://diasjp.net/)【利用規約は未確認】

### 課題C：急速強化（RI）、特に沿岸近くでの RI を予測できるか、増えているのか

(a) 未解決の点

- IPCC は、全球の RI の頻度が過去40年で増加したことを likely とした — [第11章 PDF p.1519, p.1587](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- Li, Tang, Wang, Toumi (2023, Nature Communications 14, 5167) は、海岸から 400km 以内の RI 件数が1980年代の年5件未満から2020年頃に約15件へ増え、外洋では有意な変化がなかったと報告した。ただし、全体に占める沿岸 RI の割合の増加は有意ではない（p=0.09）という記述もある — [doi:10.1038/s41467-023-40605-2](https://doi.org/10.1038/s41467-023-40605-2)【数値は検索要約経由で、本文未照合】
- WNP の RI は、データセットによって大きく異なる（TyRA） — [arXiv:2607.11220](https://arxiv.org/abs/2607.11220)。RI の「増加」の検出そのものが、課題Aのデータ問題を引き継いでいる。
- 予報面では、JTWC の RI 予報支援ツールは RI を過小に予測する傾向がある【未検証：NOAA リポジトリの文書を検索要約で見ただけ】 — [NOAA IR](https://repository.library.noaa.gov/view/noaa/64228)
- AI 気象モデル（GraphCast、Pangu-Weather など）は進路の精度は高いが、強度を系統的に過小評価すると複数の評価研究が報告している — 例: [arXiv:2409.06735](https://arxiv.org/abs/2409.06735)【abstract 要約経由】

(b) 社会的価値

- 上陸の直前に強まる台風は、避難指示のリードタイムを削る。気象庁の強度予報、自治体の避難指示の発令タイミング、鉄道の計画運休の判断が、「24〜48時間後の強度」の誤差に直接さらされる。

(c) 思考実験の進め方

- 「沿岸 RI が増えた」という観測は、(i) 実際の物理変化、(ii) 沿岸近くの観測（レーダーや陸上観測）が密になったことによる検出率の向上、(iii) 経路の変化のどれから生じうるか。各仮説が予言する、外洋 RI との比、時期、海域を比べる。
- 予報が RI を過小予測すると知っているとき、避難判断で使う閾値をどう補正するのが合理的か。見逃しと空振りのコスト比をどう置くかで、決定がどう変わるかを詰める。

(d) 公開データ

- IBTrACS（6時間ごとの強度から RI を定義できる。ただし機関ごとの定義の差に注意）
- RSMC Tokyo best track
- JMA の過去の予報精度の公開資料【所在は未確認】

### 課題D：台風の移動速度は遅くなっているのか（降雨の継続時間）

(a) 未解決の点

- Kossin (2018, Nature 558, 104–107) は、1949〜2016年の best-track で全球の移動速度が低下していると報告した。これに対して Moon et al. (2019) と Lanzante (2019) は、衛星データ導入による経路シフトのアーティファクトだと反論した。IPCC は、米国については1900〜2017年で17%低下（likely）とし、ほかの地域の証拠は robust ではないとした — [doi:10.1038/s41586-018-0158-3](https://doi.org/10.1038/s41586-018-0158-3), [第11章 PDF p.1587](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- 日本では、Yamaguchi and Maeda (2020, JMSJ 98, 1321–1334) が、9月の日本・東シナ海付近で過去40年に移動速度が有意に低下し、それが PDO と温暖化の両方による、と報告した。IPCC 11.7.1.4 もこれを引いている — [doi:10.2151/jmsj.2020-068](https://doi.org/10.2151/jmsj.2020-068)
- 予測については IPCC が「no clear consensus」とし、地域によっては加速もありうるとした。将来の移動速度の確信度は「low（専用の研究が少ない）」 — [第11章 PDF p.1586, p.1591](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- 『日本の気候変動2025』第7章の本文は、移動速度に触れていない（WebFetch の要約による）【未検証】 — [第7章](https://www.data.jma.go.jp/cpdinfo/ccj/2025/html_honpen/cc2025_honpen_7.html)

(b) 社会的価値

- 総降雨量は「雨の強さ×継続時間」で決まる。治水計画の降雨量変化倍率（後述の課題F）は雨量の比で設定されている。移動速度の変化が、この倍率の中で暗黙に扱われているのか、扱われていないのかが問題になる。高潮も、継続時間が満潮と重なる確率に効く。

(c) 思考実験の進め方

- 「移動速度は変わらず、雨の強さだけ 7%/℃ 増える」世界と、「雨の強さは変わらず、速度だけ 10% 落ちる」世界で、流域の総雨量と洪水ピークがどう違うか。流域の大きさを変えて推論する。
- 「中緯度での速度低下」は、極向き移動（課題E）と独立か。経路が北にずれるだけで、平均速度は見かけ上変わるのではないか（Moon/Lanzante の論点を日本域で再検討する）。

(d) 公開データ

- RSMC Tokyo best track（6時間ごとの位置から速度を計算できる）
- IBTrACS
- ERA5 の指向流【入手条件は未確認】

### 課題E：最大強度の緯度の北上と、日本（特に太平洋側・首都圏）への接近

(a) 未解決の点

- WNP の最大強度位置の極向き移動は、IPCC で very likely（1940年代以降）。人為的影響の寄与は、SROCC では「low confidence」、AR6 では「自然変動だけでは説明しきれない（likely）」へ評価が強まった。ただし Knutson et al. (2019, BAMS Part I) の著者チームは「少なくとも low〜medium confidence で検出可能」としつつ、人為的影響を認めるかについて意見が割れたと明記している — [第11章 PDF p.1585, p.1589](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf), [doi:10.1175/BAMS-D-18-0189.1](https://doi.org/10.1175/BAMS-D-18-0189.1)
- 北半球の極向き移動の一部は、海域ごとの発生数の変化によるもので、期間の選び方や強度での絞り込み方に左右される（IPCC 11.7.1.2） — [第11章 PDF p.1585](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- Yamaguchi and Maeda (2020, JMSJ 98, 775–786) は、1980年以降、東京を含む日本の南岸に接近する台風が増え、接近時の強度も増していると報告した。原因としては太平洋高気圧の強化と偏西風ジェットの弱化を挙げ、温暖化との関係は不明とした。PDO の位相の影響の可能性にも触れている — [doi:10.2151/jmsj.2020-039](https://doi.org/10.2151/jmsj.2020-039)
- 『日本の気候変動2025』は、東京への接近数が後半20年で前半20年の約1.5倍になったという研究を紹介している（確信度の記載なし）【要約経由、未検証】 — [第7章](https://www.data.jma.go.jp/cpdinfo/ccj/2025/html_honpen/cc2025_honpen_7.html)

(b) 社会的価値

- 首都圏は、これまで「台風の最盛期の後」に影響を受ける地域だった。最大強度の位置が北上すると、強いまま接近する確率が上がる。東京湾の高潮対策、首都圏の広域避難計画（江東5区など）、インフラの設計に効く。
- 日本全体の接近数に変化がなくても、どこに接近するかの分布が変わる可能性がある。この場合、全国平均の統計は地域の意思決定を誤らせうる。

(c) 思考実験の進め方

- 「日本全体の接近数は不変、関東への接近だけ増加」という状態は、どんな経路分布の変化と両立するか。全国の統計しか見ない意思決定者は何を見落とすか。
- 40年という観測期間は PDO の1〜2周期にあたる。「40年のトレンド」を「温暖化」と読むことの検出力を推論で見積もる（課題H とつながる）。

(d) 公開データ

- RSMC Tokyo best track
- 気象庁「台風の統計資料」（発生数・接近数・上陸数） — [気象庁](https://www.data.jma.go.jp/yoho/typhoon/statistics/index.html)
- デジタル台風（衛星画像アーカイブ） — [NII](http://agora.ex.nii.ac.jp/digital-typhoon/)【データの利用規約は未確認】

### 課題F：台風による雨はどれだけ増えたのか（イベントでは言えるが、トレンドでは言えない）

(a) 未解決の点

- IPCC では、イベントアトリビューションによる人為的な豪雨の増加は high confidence だが、全球のトレンド検出はデータの制約で妨げられている（SPM A.3.4）。過去の雨量増加は「low confidence due to lack of reliable data」（図11.20） — [SPM PDF](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf), [第11章 PDF p.1586](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- 令和元年東日本台風（Hagibis 2019）では、ストーリーライン型（Kawase et al. 2021 SOLA 17A, 7–13）が1980〜2019年の温暖化で中部日本の総降水量が約10.9%増えたと推定した。確率型（Li and Otto 2022 Climatic Change 172）は、同規模の事象の発生確率が15〜150%増え、被害のうち約40億ドルが人為的気候変動によるものと推定した — [doi:10.2151/sola.17A-002](https://doi.org/10.2151/sola.17A-002), [doi:10.1007/s10584-022-03344-9](https://doi.org/10.1007/s10584-022-03344-9)【数値は検索要約経由。書誌は Crossref で確認】
- 2つの手法の推定値の幅（10.9% と「確率15〜150%増」）は、問いの立て方の違い（その台風が来たという条件付きか、気候全体での確率か）を反映している。どちらを政策に使うべきかは未整理（これは推論）。
- d4PDF の大規模アンサンブルでは、WNP の年最大1日降水量の変化は小さいか、むしろ減少しうる。台風の数が減るためである。一方、ハワイから日本の南にかけて、台風起因の Rx1day の10年再現値は大きく増える（Kitoh and Endo 2019、IPCC 11.7.1.5 での要約） — [第11章 PDF p.1591](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)

(b) 社会的価値

- 国土交通省は、治水計画の降雨量に気候変動の倍率をかけている。2℃上昇時は北海道1.15倍、それ以外の地域1.1倍。流量は約1.2倍、洪水の発生頻度は約2倍とされる。倍率は d4PDF/d2PDF（5km）の年超過確率1/100の降雨量の比で設定されている — [国交省 提言 改訂版](https://www.mlit.go.jp/river/shinngikai_blog/chisui_kentoukai/pdf/r0304/01_teigen.pdf)
- この倍率は台風の降雨と前線の降雨を区別しない。台風の数が減り1回あたりの雨が増えるという構造変化が、倍率の中でどう相殺されているかは、提言から読み取れない（推論。原文の別紙は未確認）。

(c) 思考実験の進め方

- 「台風の数 −30%、1回あたりの雨 +15%」のとき、1/100 年の雨量は増えるか減るか。答えが、台風が年最大値に占める寄与率（地域差）にどう依存するかを推論する。
- 「個別のイベントでは言えるのにトレンドでは言えない」という状況で、政策が依拠すべきなのはどちらか。Knutson et al. (2019) の type I/type II エラーの枠組み（課題H）につなげる。

(d) 公開データ

- 気象庁のアメダス、解析雨量【利用条件は未確認】
- d4PDF（DIAS）
- RSMC Tokyo best track（降雨を台風起因に割り当てるのに使う）

### 課題G：高潮と河川洪水の複合災害の外力をどう設定するか

(a) 未解決の点

- IPCC ES では、複合洪水の確率は一部地点で増加（medium confidence）、今後も増加（high confidence） — [第11章 PDF p.1519](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- 東アジア（中国・日本・韓国）の高潮の予測研究は、台風による高潮が深刻化することを示している（IPCC 11.7.1.5 が Mori et al. 2019, 2021 などを引用）。ただし台風のサイズの変化は大きさも符号も不確実とされる — [第11章 PDF p.1591](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)
- Toyoda, Mori, Tanaka, Yorozu (2023, 土木学会論文集 79(17)) は、d4PDF で三大湾の河口を評価した。同じ台風で大きな高潮と大きな出水が同時に起きる事例は将来やや増える。両者のピークの時間差は約0.7時間短くなる。最悪経路でなくてもピークが重なりやすくなる — [J-STAGE](https://www.jstage.jst.go.jp/article/jscejj/79/17/79_23-17042/_article/-char/en)
- Hagibis を基にした擬似温暖化実験（伊勢湾・三河湾、RCP8.5 の世紀末）では、高潮と河川流量を合わせて考えると、高潮単独の場合に比べて浸水面積が約40%、平均浸水深が約20%大きくなった【検索要約経由で、論文の特定は未完了：Springer Natural Hazards s11069-023-06362-7 と推定】 — [Springer](https://link.springer.com/article/10.1007/s11069-023-06362-7)

(b) 社会的価値

- 国土交通省「高潮浸水想定区域図作成の手引き Ver.2.11」（2023年4月）は、想定する台風の中心気圧を室戸台風（1934年、上陸時911.6hPa）を基本とし、移動速度などは伊勢湾台風を基本とする。室戸台風の中心気圧は三大湾で1/500〜1/数千年程度と評価している — [国交省 手引き PDF](https://www.mlit.go.jp/river/shishin_guideline/kaigan/takashioshinsui_manual.pdf)
- 同じ手引きは、気候変動の扱いを次のように書いている — [国交省 手引き PDF](https://www.mlit.go.jp/river/shishin_guideline/kaigan/takashioshinsui_manual.pdf)
  > 「高潮浸水想定区域における外力条件は、現段階においては、気候変動による将来予測を直ちに高潮浸水想定に反映させる制度とはなっていないが、（中略）気候変動に伴う海面上昇や台風の将来変化を見込んで設定する必要がある。」
- つまり、ハザードマップと避難計画の前提となる外力は「過去最大」で固定されており、将来の変化は制度の見直し待ちになっている。

(c) 思考実験の進め方

- 「過去最大（室戸台風の気圧＋伊勢湾台風の経路と速度）」という外力は、課題A（強度データの不確実性）、課題D（移動速度）、課題E（北上）を前提にしても保守側に立つのか。どの条件が崩れたら保守的でなくなるかを列挙する。
- 高潮と洪水の同時生起の確率が「独立の積」ではなく「同じ台風による相関」で決まるとき、両者を別々に想定する現行の作り方はどれだけ過小評価になりうるか。

(d) 公開データ

- d4PDF
- 気象庁の潮位観測【所在は未確認】
- 国土交通省の水文水質データベース（河川流量）【URL は未確認】

### 課題H（メタ課題）：「検出された」と言うための基準をどこに置くか

(a) 未解決の点

- Knutson et al. (2019, BAMS Part I) は、type I エラー（人為的影響の過大評価）を避ける従来の基準では、著者チームの意見が割れたと述べている。そこで、type II エラー（見逃し）を減らす弱い「balance of evidence」基準で評価し直した。この基準による結論は誤警報の可能性が大きいが、リスク評価には役立つ、としている — [doi:10.1175/BAMS-D-18-0189.1](https://doi.org/10.1175/BAMS-D-18-0189.1)（abstract を Crossref で確認）
  - 【一次資料で確認できず（2026-11-21）】この記述の一次資料（doi:10.1175/BAMS-D-18-0189.1）は、出版社・大学・NOAA のサイトが自動取得を拒否し、原文を確認できていない。結論や手引きの根拠には使わない。
- IPCC も「低確信度はトレンドがないことを意味しない」と明記している（11.7.1.2） — [第11章 PDF p.1585](https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_Chapter11.pdf)

(b) 社会的価値

- 科学的な「検出」の基準（type I を避ける）と、防災の意思決定の基準（見逃しのコストが大きい）は一致しない。どの確信度の知見から設計外力に入れるかは、科学の問題ではなく決定の問題であり、その線引きが明示されていない。

(c) 思考実験の進め方

- 同じ証拠を、type I 重視と type II 重視の2つの基準で読んだとき、課題A〜Gの結論がそれぞれどう変わるかを並べる。
- 「低確信度の増加傾向」に対して、何もしない、可逆的な対策（運用・避難計画）だけ先に打つ、不可逆な投資（堤防のかさ上げ）まで打つ、の3つの選択肢の期待損失を比べる。

---

## 3. 社会的価値による順位づけ（Claude の判断）

基準は3つ。(1) 意思決定が今まさにその知見に依存しているか、(2) 誤ったときの損失が大きいか、(3) 公開データと推論で前進できる余地があるか。

1. 課題G（高潮と洪水の複合、外力設定）: 浸水想定と避難計画に直結する。制度が「過去最大」で固定されているという構造的な論点がある。
2. 課題A（WNP の強い台風の割合とデータ依存）: すべての外力設定の土台になる。機関間の差という具体的な数値（CI 数 0.5〜2.0）がある。
3. 課題C（沿岸 RI と予報）: 避難のリードタイムに直結する。AI モデルの過小評価という新しい論点もある。
4. 課題F（台風降雨、治水倍率1.1）: 全国の治水計画に適用済みの数値がある。台風の数と強さの構造変化との整合が未検証。
5. 課題E（北上と首都圏への接近）: 影響を受ける人口が大きい。ただし原因の帰属が不明。
6. 課題H（検出基準）: 上のすべてに横断的に効く。思考実験との相性は最もよい。
7. 課題D（移動速度）: 降雨と高潮の継続時間に効く。WNP の観測結果はあるが、将来予測の確信度は低い。
8. 課題B（発生数）: 学術的な論争としては最も活発。ただし防災の決定への直接の効き方は、課題A・F を経由する間接的なもの。

---

## 4. 未検証事項のまとめ

- 『日本の気候変動2025』第7章の記述（WebFetch の要約。原文の一字一句は未照合）
- Kawabata et al. (2023) の 79%、43.7%、49.6% という数値（WebFetch の要約。表は未照合）
- TyRA（arXiv:2607.11220）は査読前のプレプリント。データの公開状況は未確認
- Li et al. (2023) の沿岸 RI の件数と p=0.09（検索要約）
- Chand/Emanuel の論争の各主張の中身（書誌は Crossref で確認、内容は検索要約）
- Wu, Yeung, Chang (2006) の本文
- Hagibis の複合災害研究の論文の特定（Springer s11069-023-06362-7 と推定）
- JTWC と CMA の best track の入手経路（このセッションでは 403 か接続失敗）
- JTWC の RI 予報の過小予測の傾向（NOAA 文書の検索要約のみ）
- AI 気象モデルの強度過小評価の定量値
