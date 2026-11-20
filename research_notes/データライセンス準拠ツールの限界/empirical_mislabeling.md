# 宣言ライセンスの誤表示・ライセンスロンダリング・不整合に関する実証データ

調査日: 2026-11-20。2026年11月時点で到達できた一次資料（主に arXiv abstract と HTML 版）をもとにしている。WebFetch で本文や abstract を直接確認できなかった項目には【未検証】と付けた。

---

## Q1. Longpre et al.「A Large-Scale Audit of Dataset Licensing & Attribution in AI」（Data Provenance Initiative）

### Takeaway
アグリゲータ（GitHub / Hugging Face / Papers with Code）に載っているデータセットのライセンスは、約70%が「未指定」だった。指定がある場合も、人手で再確認した結果と一致したのは35〜54%にとどまる。16〜29%は実際より緩い（より許容的な）用途カテゴリで表示されていた。主な原因は、コードのライセンスをデータのライセンスと取り違えることだった。

### Cited Findings
- 監査対象は1,800件を超えるテキストデータセット（表2では n=1,858）。abstract はホスティングサイトについて「license omission of 70%+ and error rates of 50%+」と要約している — [arXiv:2310.16787](https://arxiv.org/abs/2310.16787)
- 「Unspecified」の割合はプラットフォームごとに GitHub 72%、Hugging Face 69%、Papers with Code 70%だった。DPI が再アノテーションした後は 30.7%（1,858件中570件）まで下がった — [arXiv HTML 版 2310.16787 表2](https://arxiv.org/html/2310.16787)
- プラットフォームによって異なるが、データセットライセンスの46〜65%を人手で付け直した — [arXiv HTML 版 §3.1](https://arxiv.org/html/2310.16787)
- アグリゲータのライセンスが DPI の判定と一致した割合は GitHub 43%、Hugging Face 35%、Papers with Code 54%。実際より緩く表示されていた割合は GitHub 29%、HF 27%、PwC 16%だった — [arXiv HTML 版](https://arxiv.org/html/2310.16787)
- Hugging Face では、分析したライセンスの66%が別の用途カテゴリに分類されており、多くは実際より緩い表示だった（66%は不一致の全体、27%はそのうち緩すぎる側だけを数えた値） — [arXiv HTML 版](https://arxiv.org/html/2310.16787)
- 著者は誤りの原因を「contributors on these platforms often mistaking licenses attached to code in GitHub repositories for licenses attached to data」としている — [arXiv HTML 版](https://arxiv.org/html/2310.16787)
- ライセンスの再導出手順（§2.2）は次の5段階。
  1. GitHub、arXiv、HF、PwC、コレクション本体から自己申告ライセンスを集める
  2. コードではなくデータに固有のライセンスを探す
  3. ライセンスの種別（一般的なライセンス、Custom、利用申請フォーム、Unspecified）を判定する
  4. Permitted Use、Attribution、Share-Alike の観点で分類する。ライセンスが複数ある場合は最も厳しいものを採る
  5. 来歴メタデータを集める

  ライセンスの注釈は法律の専門家が人手で行う「time-intensive human annotation protocol」とされている — [arXiv HTML 版](https://arxiv.org/html/2310.16787)
- 再判定後の内訳は Commercial 46.1%、Unspecified 30.7%、Non-Commercial 19.0%、Academic-Only 4.3%。2023年に作られたデータセットでは NC と Academic-Only を合わせて61%に達し、前年までの平均は約20%だった — [arXiv HTML 版](https://arxiv.org/html/2310.16787)
- 本文は「85% of dataset licenses request attribution」「30% include a share alike clause」と書いているが、Figure 2 のキャプションは73%と33%になっている。論文内で数値が食い違っている — [arXiv HTML 版](https://arxiv.org/html/2310.16787)
- 序論には「Our work points to a crisis in license laundering」とある。ただし laundering を定義して直接測定してはいない — [arXiv HTML 版](https://arxiv.org/html/2310.16787)
- 【未検証】Nature Machine Intelligence 版（2024）は [nature.com/articles/s42256-024-00878-8](https://www.nature.com/articles/s42256-024-00878-8)。URL は記憶によるもので、本セッションでは取得していない。

### Inferences
- アグリゲータの表示を信じると、半分以上のケースで用途判断を誤る計算になる。その誤りは「緩すぎる」方向に偏っており、利用者が違反する側に倒れる。したがって、メタデータのライセンスフィールドを機械的に読むだけの準拠ツールは、層(2)の検証にはほぼ役に立たない。
- DPI は人手で追跡しても30%が Unspecified のまま残った。原典まで遡っても「真のライセンス」が確定しないケースが相当数あることになる。

### Gaps
- 「アグリゲータの誤り」と「原典そのものの誤り（公開者が権利を持っていない）」を分けた定量値は、この論文にはない。DPI は原典の宣言を正解として扱っている。

---

## Q2. Longpre et al.「Consent in Crisis」（2024）: ToS と robots.txt の不整合

### Takeaway
14,000ドメインを監査した結果、ToS と robots.txt は互いに整合していないことが多かった。反クローリングの ToS があっても robots.txt は存在しない、またはその逆というドメインが2〜3割あった。同意シグナルは1年で急増しており、取得した時点のスナップショットはすぐ古くなる。

### Cited Findings
- 監査対象は14,000ウェブドメイン。2023〜2024年の1年間で、C4 トークンの約5%以上、C4 の重要ソースの28%以上が完全に制限された。ToS のクローリング制限は C4 の45%に及んでいた — [arXiv:2407.14933](https://arxiv.org/abs/2407.14933)
- 不整合: 反クローリングの規約があるのに robots.txt がないドメインが35.1%、ToS がないのに制限的な robots.txt を持つドメインが20.3%あった — [arXiv HTML 版 2407.14933v2](https://arxiv.org/html/2407.14933v2)
- robots.txt による制限は、2023年半ばから2024年4月にかけて C4 / RefinedWeb / Dolma 全体で約1%から5〜7%に増えた。最重要ドメイン（HeadAll）では3%未満から20〜33%に増えた。相対的な増加率は500%以上（head 部分では1000%以上） — [arXiv HTML 版](https://arxiv.org/html/2407.14933v2)
- ToS のクローリング制限は1年で相対26〜53%増えた。トークンの45〜55%について、規約ページに何らかの利用制限があった — [arXiv HTML 版](https://arxiv.org/html/2407.14933v2)
- 制限はエージェントごとに非対称だった（HeadC4、2024年4月、制限されたトークンの割合）: OpenAI 25.9%、Anthropic / Common Crawl 13.3%、Google-Extended 9.8%、Google Search 1.0%。全体の4.5%は、存在しないエージェント名（anthropic-ai / Claude-Web）だけをブロックし、実在する ClaudeBot はブロックしていなかった — [arXiv HTML 版](https://arxiv.org/html/2407.14933v2)
- 論文内で見出しの数値がそろっていない。abstract は28%以上、序論は約25%以上、§3.1 は20〜33%としている — [arXiv HTML 版](https://arxiv.org/html/2407.14933v2)

### Inferences
- 機械可読なシグナル（robots.txt）と法的文書（ToS）が食い違うのは例外ではなく、ドメインの2〜3割で起きている。片方だけを確認する準拠チェックは原理的に見落とす。
- 1年で数倍に変化する状況では、「取得時点で許可されていた」という証跡を残さない限り、後から準拠を立証できない。

### Gaps
- ドメインごとに ToS や robots.txt がどれくらいの頻度で書き換わるか（個別ドメインの変更頻度）は、この論文では報告されていない。報告されているのは月次の集計トレンドだけ。

---

## Q3. OSS とデータセットのライセンス不整合・ロンダリング

### Takeaway
OSS では次のことが一貫して観察されている。
- 大半のリポジトリにライセンスがない
- ライセンスを宣言していても、半数はコード内の全ライセンスを宣言していない
- 依存関係を通じた非互換が数%〜10%程度ある

AI のサプライチェーンでは、さらに極端な結果が出ている。データセットからモデル、アプリケーションへと渡る過程で、ライセンス本文と帰属表示はほぼ失われる。モデルからアプリへの移行の約1/3では、制限条項が緩いライセンスに置き換えられている（permissive-washing）。

### Cited Findings
**GitHub のライセンス欠如**
- Williamson（2013）: 1,692,135リポジトリのうち、ライセンスを明示していたのは219,326件（14.9%）。ただし API 制限のため、調べたのは最古の28%のリポジトリだけ — [The Register](https://www.theregister.com/2013/04/18/github_licensing_study/)
- GitHub 自身の2015年の報告: ライセンスがあるリポジトリは約20%（fork を含めると約30%）で、割合は減少傾向にあった — [GitHub Blog 2015](https://github.blog/2015-03-09-open-source-license-usage-on-github-com/)

**宣言と実態の不一致**
- Wolter et al.（TOSEM 2023）: 1,000の GitHub リポジトリのうち約半数は、コード内で見つかったライセンスをすべて宣言してはいなかった。そのうち約10%は permissive と copyleft の食い違いだった。既存のツールではライセンスを完全には特定できない、と結論している — [FAU OSR 紹介記事](https://osr.cs.fau.de/2022/10/13/research-paper-open-source-license-inconsistencies-on-github) / [PDF](https://oss.cs.fau.de/wp-content/uploads/2022/10/wolter-2022-open.pdf)

**PyPI の依存関係とライセンス**
- Xu et al.（ASE 2023）: PyPI のリリースの7.27%にライセンス非互換があり、その61.3%は推移的依存が原因だった — [ASE 2023 プロフィール](https://www.se.cs.uni-saarland.de/conferences/ASE/ase2023/profile/ase-2023/haohe.html) / [arXiv:2308.05942](https://arxiv.org/abs/2308.05942v1)（数値は検索結果の要約から取ったもので、本文では未確認）
- PyPI のライセンス変種の研究（2025）: 554,079パッケージ、6,193,233リリースを分析。条文の変種のうち実質的な改変は2%だったが、それに依存する下流パッケージの約10.7%がライセンス非互換になっていた — [arXiv:2507.14594](https://arxiv.org/html/2507.14594v1)（数値は検索結果の要約から取ったもの）

**Stack Overflow スニペットの帰属**
- Baltes & Diehl（EMSE 2019）: SO のコードを含む GitHub リポジトリのうち、CC BY-SA 3.0 と両立する形で使っていたのは最大でも1.8%。必要な帰属表示が付いていたのは、コピーされたスニペットの最大1/4程度と推定している。プレプリント版では「Java では少なくとも2/3が無帰属」と書かれていた — [Springer EMSE](https://link.springer.com/doi/10.1007/s10664-018-9650-5) / [arXiv:1802.02938](https://arxiv.org/abs/1802.02938)
- 開発者調査では、62%が SO からコピーしたコードに一度も帰属を付けたことがないと回答した（自己申告） — [arXiv:1806.08149](https://arxiv.org/pdf/1806.08149.pdf)

**AI サプライチェーン（Hugging Face と GitHub）**
- Jewitt et al.「Permissive-Washing in the Open AI Supply Chain」（arXiv 2026年2月）: 124,278本のデータセット→モデル→アプリのチェーン（データセット3,338、モデル6,664、アプリ28,516）を調べた。
  - permissive と表示されたものでも、必要なライセンス本文がないものがデータセットの96.5%、モデルの95.8%を占めた
  - ライセンス本文と著作権表示の両方を満たして完全に準拠していたのは、データセットの2.3%、モデルの3.2%だけ
  - データセットの準拠した表示をモデルが保持していた割合は27.59%、モデルの表示をアプリが保持していた割合は5.75%
  - 上流の表示を一つでも保持していたアプリは6.38%

  — [arXiv:2602.08816](https://arxiv.org/abs/2602.08816)
- Jewitt et al.（arXiv 2025年9月、2026年7月改訂）: データセット約364k、モデル約1.6M、GitHub プロジェクト約140k を分析した。モデルからアプリへの移行の約35.5%で、制限条項が permissive な再ライセンスによって消えていた。約200の SPDX 条項とモデル固有の条項を符号化したルールエンジンは、アプリ内のライセンス衝突の86.4%を解決できた — [arXiv:2509.09873](https://arxiv.org/abs/2509.09873)
- HF 上のモデル760,460件とデータセット175,000件を対象にした研究（TOSEM 2025 / FSE 2026 journal-first）は、ドキュメントの不整合とライセンス準拠の問題を報告している — [arXiv:2502.04484](https://arxiv.org/html/2502.04484)（具体的な数値は未取得）

**The Stack のオプトアウト**
- 2022年10月31日の締め切り前に届いたオプトアウト申請は9件で、対象の299リポジトリを v1.1 から除去した — [SantaCoder 論文 arXiv:2301.03988](https://arxiv.org/pdf/2301.03988)
- 【未検証】HF のディスカッションでは「GitHub Issues だけで1,700件以上」「約4,000件が保留中」という書き込みがある。どちらも日付がなく、BigCode の公式な数値でもない。また「v2.1 では除去済みと表示されるのに v2.0.1 には残っている」との指摘がある — [HF discussion 9](https://huggingface.co/datasets/bigcode/the-stack/discussions/9) / [HF discussion 43](https://huggingface.co/datasets/bigcode/the-stack/discussions/43)

### Inferences
- 層(2)の誤りは、上流で「ライセンスがない・不完全」という形で生じることが多い。その後は再配布の段階ごとに表示が失われ、緩い方向へ書き換えられていく。下流で宣言されているライセンスの信頼度は、ホップ数に応じて急速に落ちる。
- 帰属を正しく伝播できているのは一桁%で、「ライセンス表示に従えば準拠になる」という前提はほとんど成り立たない。

### Gaps
- LAION-5B、Common Crawl、ImageNet について、個々のサンプルのライセンス表示が正しい割合を示した定量研究は、今回の調査範囲では取得できなかった（調査呼び出し数の制約による）。
- Debian / Maven / npm の不整合率（例: Wu et al. の Debian 研究）の具体的な数値は未取得。

---

## Q4. 公開者が権利を持っていないのに公開した事例（オープンデータ、Wikimedia、Flickr、copyfraud）

### Takeaway
Wikimedia Commons では、Flickr を経由したライセンスロンダリングがよくあるため「Flickr washing」という名前が付き、検出の手引きと一括削除の手続きが用意されている。政府のオープンデータでは、オープンライセンスと確認できたのは38%で、著作権表示がデータではなくウェブサイトを指しているケースが多い。権利のないライセンスを付与する事例の頻度について、体系的な統計は見つからなかった。

### Cited Findings
- Commons には「License laundering」の方針ページがある。アップローダー本人が権利者でない限り、権利者が当該ライセンスで公開したことの証明を求める。laundering が疑われるファイルは、出典ユーザーが権利者だと主張していても削除依頼の対象になる — [Commons:License laundering](https://commons.wikimedia.org/wiki/Commons:License_laundering)
- 「Flickr washing」は、Flickr がライセンスロンダリングされたファイルの最も多い出所であることから付いた呼び名。Commons には、問題のある出典の一覧と検出の手引きがある。手引きが挙げる兆候は、Commons に出る直前に Flickr へアップロードされていること、プロが撮ったような画像であること、など — [Commons:Flickr files](https://commons.wikimedia.org/wiki/Commons:Flickr_images) / [Commons:Problematic sources（ミラー）](https://c.enwp.org/wiki/Commons:PRS) / [How to detect copyright violations（ミラー）](https://c.enwp.org/wiki/Commons:How_to_detect_copyright_violations)
- Flickr ではアップロードした後でもライセンスを変更できる。CC-BY で取り込まれて License review で検証されたファイルは、その後 Flickr 側で All Rights Reserved に変わっても、Commons では CC-BY のまま残せる。このため、取得した時点のライセンスを検証して記録する「License review」の仕組みがある — [Commons:Flickr files](https://commons.wikimedia.org/wiki/Commons:Flickr_images) / [Commons:License review](https://commons.wikimedia.org/wiki/Commons:LR)
- Commons には DMCA 削除通知の記録ページがある — [Commons:Office actions/DMCA notices](https://commons.wikimedia.org/wiki/Commons:Office_actions/DMCA_notices)
- Global Open Data Index 2016/17 では、対象の政府データセットのうちオープンライセンスだったのは38%だった（暫定値）。条件が見つからないケースもあった。著作権表示は「simply a standard copyright notice referring to the website」であることが多く、データ自体を指していないとされている — [OKFN blog 2017](https://blog.okfn.org/2017/06/08/the-state-of-open-licensing-in-2017/)
- data.europa.eu の180万件を超えるデータセットでは、400種類以上のライセンスが使われていた — [data.europa.eu](https://data.europa.eu/en/news-events/news/understanding-open-data-licensing-insights-18-million-datasets)
- Copyfraud の事例（Highsmith 対 Getty、2016年）: 写真家 Highsmith は、パブリックドメインとして寄贈した写真について Getty などがライセンス料を請求したと訴え、DMCA 違反18,755件を主張した。連邦法上の請求は同年中に取り下げられ、with prejudice で終結した。Getty は「パブリックドメイン作品の販売は違法ではない」と反論している — [Hyperallergic](https://hyperallergic.com/photographer-files-1-billion-suit-against-getty-for-licensing-her-public-domain-images) / [TorrentFreak](https://torrentfreak.com/1bn-getty-images-public-domain-photograph-dispute-is-over-161125/)
- 2019年にも、CixxFive Concepts が Getty を相手に同種の訴訟を起こしている — [Techdirt](https://www.techdirt.com/articles/20190329/15352641901/getty-images-sued-yet-again-trying-to-license-public-domain-images.shtml)

### Inferences
- 世界最大級の自由ライセンスのリポジトリ（Commons）でさえ、層(2)は自動では守れず、人によるレビュー（License review、削除依頼）に頼っている。個人がツールだけで代替するのは難しい。
- ライセンスは後から変わり得る。そのため、Commons と同じく「取得時点の宣言と、その証跡（アーカイブ URL やスクリーンショット）」を残すことが、現実的に取れる唯一の防御になる。
- 公開者が権利を持たない形のロンダリングには「緩すぎる表示」だけでなく、逆向きの誤りもある。Getty の件のように、PD 作品に権利を主張して制限を付けるケースである。

### Gaps
- Commons の削除依頼のうち、著作権侵害やロンダリングが理由のものの割合や件数は見つからなかった。
- 政府のオープンデータに第三者の著作物が混ざっていた具体的な事件と、その頻度を示す統計は見つからなかった。

---

## Q5. CC-BY の再利用で帰属がどれだけ守られているか

### Takeaway
帰属の遵守率を直接測った研究は少ない。ある分野で測られた値はどれも、遵守が少数派であることを示している。違反率は、Flickr の CC 画像で78〜94%（誤検出が多い）、SO スニペットで少なくとも3/4（帰属付きは最大1/4）、AI モデルとアプリへの伝播では帰属の保持が5〜28%。

### Cited Findings
- Seneviratne（MIT、2009）: Flickr の CC 画像を埋め込んでいるサイトの3サンプル（67〜70サイト、241〜466画像）で、誤帰属の判定は78%、80%、94%だった。ただし人手で確認した precision は55%、42%、39%と低い。自分の写真に帰属を付けない例を違反と誤判定したためで、補正後の真の違反率は算出できない。recall も算出されていない — [MIT DIG thesis ch.3](https://groups.csail.mit.edu/dig/2009/oshani-thesis/chap3.tex) / [Oxford 論文ページ](https://www.cs.ox.ac.uk/publications/publication13259-abstract.html)
- SO のスニペット: 必要な帰属があるのは最大1/4、CC BY-SA と両立していたリポジトリは最大1.8% — [Springer EMSE](https://link.springer.com/doi/10.1007/s10664-018-9650-5)
- AI サプライチェーン: データセットの表示をモデルが保持していた割合は27.59%、モデルの表示をアプリが保持していた割合は5.75% — [arXiv:2602.08816](https://arxiv.org/abs/2602.08816)
- Hietanen, Athukorala & Salovaara（MindTrek 2011）「What's with the free images? A study of Flickr's creative commons attribution images」という研究がある。【未検証】内容と数値は確認できていない — [CC Wiki 参照ページ](https://wiki.creativecommons.org/Grants/Images_of_People,_Networks_of_Sharing:_How_Does_Creative_Commons_Impact_Flickr)

### Inferences
- 「帰属付きで再利用できる」というライセンスは、実際には大半の再利用で守られていない。準拠を保証したい側としては、帰属のテンプレートを自動で生成し、CI で検証する仕組みが必要になる。

### Gaps
- 一般のウェブや出版物で CC-BY がどれだけ遵守されているかについて、最近の大規模な定量研究（2015年以降）は見つからなかった。

---

## Q6. ライセンスや規約ページの変化（terms drift）

### Takeaway
ToS や robots.txt は集計レベルで1年に数割から数倍の規模で変化している（Consent in Crisis）。ただし、個々のドメインの規約がどれくらいの頻度で変わるかを測った研究は、プライバシーポリシーの分野にしか見つからなかった。

### Cited Findings
- C4 の head ドメインで robots.txt がない割合は、2016年の約20%からほぼ0に下がった。ToS がない割合も約80%からほぼ0に下がった（Wayback の欠損のため値はやや高めに出ている可能性がある）。ToS の制限は1年で相対26〜53%増えた — [arXiv HTML 版 2407.14933v2](https://arxiv.org/html/2407.14933v2)
- Amos et al.: 130,000以上のサイトから集めた1,071,488件の英語プライバシーポリシー（約20年分）を分析した。GDPR が過去10年で最も広範な改訂を引き起こしていた。2019年の中央値の長さは1,522語 — [arXiv:2008.09159](https://arxiv.org/pdf/2008.09159)
- Adhikari et al.（PETS 2023）: データ利用の慣行のカテゴリによって、改訂の頻度に差があった — [PoPETs 2023](https://www.petsymposium.org/popets/2023/popets-2023-0074.php)
- LLM 事業者11社のプライバシーポリシー（74版）と補足文書115件を2025年8月まで追跡した研究では、製品の発表に合わせて改訂される傾向があった — [arXiv:2511.21758](https://arxiv.org/abs/2511.21758v1)
- Flickr ではアップロード後もライセンスを変更でき、Commons は取得時点の検証記録を根拠にしている — [Commons:Flickr files](https://commons.wikimedia.org/wiki/Commons:Flickr_images)
- GitHub のライセンス変更（Vendome et al., EMSE 2017「License Usage and Changes」）。【未検証】変更頻度の数値は取得していない — [EMSE'16 PDF](https://www.cs.wm.edu/~denys/pubs/EMSE'16-Licensing.pdf)

### Inferences
- ライセンスや規約は動く対象として扱う必要がある。準拠ツールには、取得時点のスナップショット（ハッシュ、アーカイブ URL、取得日）を記録する機能が欠かせない。

### Gaps
- データセットのライセンスページ（HF の dataset card、政府ポータル）が改訂される頻度を直接測った研究は見つからなかった。
- ToS（プライバシーポリシーではないもの）の個別ドメインでの変更頻度に関する研究は見つからなかった。
