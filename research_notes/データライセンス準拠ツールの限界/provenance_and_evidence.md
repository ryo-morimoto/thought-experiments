# 来歴・真正性・証拠保全メカニズムとその限界（「公開ソースから、所定の条件で、所定の時点に取得した」主張の裏付け）

調査日: 2026-11-20。各項目に出典URLを付す。一次資料を取得できなかった項目は「未検証」と明記する。

## Q1. 各メカニズムは「時刻・出所・完全性・権利」について何を証明し、何を明示的に証明しないか

### Takeaway
どの仕組みも証明できるのは基本的に「あるハッシュ値のデータが時刻T以前に存在した」（タイムスタンプ系）、「鍵/ID保持者Kがこのデータについて主張した」（署名・来歴系）、「第三者アーカイブがURL UからT時点にこの内容を取得した」（ウェブアーカイブ系）の3種に限られる。「その主張が真実である」「Kが権利者である」「そのライセンスが有効に付与された」はどの仕組みも証明しない。仕様自体がこれを明言している例も多い（C2PA、RFC 3161、SLSA）。

### Cited Findings

**RFC 3161（Trusted Timestamp / TSA）**
- 目的は「あるデータが特定時刻より前に存在したという主張の証明」を支えること。TSAの役割は「データがある時刻以前に存在したことを示す証拠を確立するためにタイムスタンプを付すこと」 — [RFC 3161 §1](https://www.rfc-editor.org/rfc/rfc3161)
- TSAは、タイムスタンプ対象のimprint（ハッシュ）を長さ確認以外「いかなる形でも検査してはならない」。TSAが受け取るのはハッシュのみで文書そのものではない — [RFC 3161 §2.1](https://www.rfc-editor.org/rfc/rfc3161)
- 要求者の識別はリクエストに含まれず、TSAはそれを検証しない — [RFC 3161 §2.4.1](https://www.rfc-editor.org/rfc/rfc3161)
- 信頼モデル: TSAは「信頼できる時刻源」を使い、専用鍵で署名する。RFCはTSA運用の全体的なセキュリティ要件を定めず、利用者はTSAの公開ポリシーを確認したうえで依拠すべきとする。TSA秘密鍵が漏洩した場合、その鍵で署名されたトークンは「もはや信頼できない」 — [RFC 3161 §1, §2.1, §4](https://www.rfc-editor.org/rfc/rfc3161)

**OpenTimestamps**
- 公式サイトの主張: 「タイムスタンプは、あるデータがある時点より前に存在したことを証明する」。ハッシュはブラウザ側で計算される — [opentimestamps.org](https://opentimestamps.org/)
- Bitcoinブロックチェーンにアンカーし、カレンダーサーバが無料・登録不要でまとめて記録を代行する。検証結果には「Bitcoin Attestation」「Pending/Other Attestation」などの種別がある — [opentimestamps.org](https://opentimestamps.org/)
- 作成者・出所・権利については公式ページに記述がない（したがって証明しない）— [opentimestamps.org](https://opentimestamps.org/)

**Sigstore（cosign / Fulcio / Rekor）**
- Rekorは「ソフトウェアサプライチェーンで生成されたメタデータの不変・改ざん耐性のある台帳」を目指し、監査者はログが追記専用でエントリが改変・削除されていないことを確認できる。CLIで包含証明（inclusion proof）を取得できる — [Sigstore docs: Rekor overview](https://docs.sigstore.dev/logging/overview/)
- 署名者はOIDCでIDプロバイダのアカウント支配を証明し、そのIDが短命のFulcio証明書に埋め込まれる。Rekorエントリは「データがある時刻以前に存在した」という単一当事者による証明（single-party attestation）を与える — [Sigstore docs: Security](https://docs.sigstore.dev/about/security/)
- 「What Sigstore Doesn't Guarantee」: OIDC IDやプロバイダが侵害されればFulcioは不正な証明書を発行しうる。第三者がログを監視しなければRekor/Fulcioの不正は検出されない可能性がある。短期間であればRekor運営者が時刻を偽装しやすい — [Sigstore docs: Security](https://docs.sigstore.dev/about/security/)
- 公式ページは「有効な署名＝成果物が安全」とは述べていない。扱うのは「誰が・いつ署名したか」のみ — [Sigstore docs: Security](https://docs.sigstore.dev/about/security/)

**SLSA Provenance / in-toto attestation**
- SLSAは来歴を「ソフトウェア成果物がどこで・いつ・どのように作られたかを記述する検証可能な情報」と定義する。in-toto Statement（`_type: https://in-toto.io/Statement/v1`、`subject`、`predicateType: https://slsa.dev/provenance/v1`）の形式をとる — [SLSA v1.0 Provenance](https://slsa.dev/spec/v1.0/provenance)
- `resolvedDependencies` はビルドに必要な成果物を `uri` と `digest` で列挙する。完全性は「best effort」 — [SLSA v1.0 Provenance](https://slsa.dev/spec/v1.0/provenance)
- 信頼はビルダー（`builder.id`）に依存する。利用者は「特定の署名者とビルダーの組み合わせのみ」を受け入れなければならない。`externalParameters` は信頼されない入力で、下流で検証する必要がある — [SLSA v1.0 Provenance](https://slsa.dev/spec/v1.0/provenance)
- 補足: in-toto.io本体の仕様ページは今回取得していない（in-toto Statementの構造はSLSAページ経由でのみ確認）。

**W3C PROV / PROV-O**
- PROV-Oは2013年4月30日のW3C勧告。異なるシステム間で来歴情報を表現・交換するためのオントロジー。中核クラスは Entity / Activity / Agent。プロパティには `wasDerivedFrom`、`wasAttributedTo`、`generatedAtTime`、`hadPrimarySource` などがある — [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- 取得した範囲（先頭約10万字）では署名・ハッシュなどの完全性メカニズムは記述されていなかった — [W3C PROV-O](https://www.w3.org/TR/prov-o/)（全文は未読のため「PROV-Oに完全性機構がない」は推論扱い。Inferences参照）

**C2PA / Content Credentials**
- マニフェストが証明するのは「来歴データが整形式で、改変されておらず、資産に結び付いていること」と「署名者が既知の信頼リストにつながること」。署名者に帰属するのは `created_assertions` のみで、`gathered_assertions` は署名者に帰属しない — [C2PA 2.2 Explainer §2, §7.5.2](https://spec.c2pa.org/specifications/specifications/2.2/explainer/Explainer.html)
- 明示的に証明しないこと: 「来歴情報だけでは、デジタルコンテンツが真実か・正確か・事実かは分からない」。コア仕様は人や組織のアイデンティティを直接扱わない（CAWG identity assertion等の拡張が必要） — [C2PA 2.2 Explainer §2, §7.2.2, §7.2.4](https://spec.c2pa.org/specifications/specifications/2.2/explainer/Explainer.html)
- Content CredentialsはアクセスやDRM的な利用制限を課さない。AI学習可否などはあくまで拡張的なアサーションの例として挙げられている — [C2PA 2.2 Explainer](https://spec.c2pa.org/specifications/specifications/2.2/explainer/Explainer.html)
- 信頼モデル: 署名者証明書、C2PA Trust List（ブラウザ・PDFの信頼リストに類似）、IPTCリストや個人の信頼リスト。資格情報がないことは、それだけで資産が信頼できないことを意味しない — [C2PA 2.2 Explainer §7.1.2, §7.5](https://spec.c2pa.org/specifications/specifications/2.2/explainer/Explainer.html)

**Software Heritage / SWHID**
- SWHIDは ISO/IEC 18670:2025「SoftWare Hash IDentifier (SWHID) Specification V1.2」として2025年4月に国際標準化された — [ISO](https://www.iso.org/standard/89985.html); [OpenChain news](https://openchainproject.org/news/2025/04/29/from-heritage-to-hash-swhid-becomes-a-global-iso-iec-standard)
- SWHIDはデジタルオブジェクトから暗号学的ハッシュ（Merkle DAG）で直接計算でき、中央レジストリなしで独立に完全性を検証できる。SWHIDからコピーを得る「解決」は仕様の範囲外 — [Software Heritage: SWHID](https://www.softwareheritage.org/?p=45638); [Wikipedia: SWHID](https://en.wikipedia.org/wiki/SoftWare_Hash_IDentifier)
- 未検証: Software Heritage FAQ（Save Code Now、ライセンスを確認するか、取り下げ方針）は取得時にTLSエラーで読めなかった — [softwareheritage.org/faq](https://www.softwareheritage.org/faq/)

**Wayback Machine / Perma.cc / archive.today（ウェブアーカイブ）**
- Internet Archive: 「robots exclusionsのためにアーカイブされないページがあり、サイト所有者の直接の要請で除外されたサイトもある」。権利侵害が疑われるコンテンツを裁量で削除・アクセス停止しうる — [Internet Archive Help: Wayback Machine general information](https://help.archive.org/help/wayback-machine-general-information/)
- Perma.cc: BluebookとChicago Manual of Styleが利用を推奨。裁判所とその職員は無料。個人の毎月10件の無料リンクは2019年1月に終了したと報じられる（公式料金ページは今回直接取得できず、最新条件は未検証） — [Perma.cc user guide: accounts](https://perma.cc/docs/accounts); [Perma blog 2018](https://archive.blogs.harvard.edu/perma/2018/09/20/now-you-can-pay-for-unlimited-perma-links-yes-you); [Wikipedia: Perma.cc](https://en.wikipedia.org/wiki/Perma.cc)
- archive.today: Wikipedia系の情報ではrobots.txtに従わない（「ユーザーの直接のエージェントとして動作する」ため）とされるが、archive.today自身の一次資料は見つからなかった（未検証） — [Wikipedia mirror: Archive.ph](https://wikiless.lunar.icu/wiki/Archive_Today?lang=en)

**Git コミット署名**
- GitHubは、GPG/SSH/S/MIME署名を検証できたコミットを「Verified」と表示する。push時に検証すると、編集不可で永続する検証記録を保存し、鍵のローテーションや失効後も「Verified」のまま残る（遡って再検証しない） — [GitHub Docs: About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
- 同ページが言及するタイムスタンプは検証完了時刻 `verified_at` だけで、コミットの author/committer 日付が検証されるかについては記述がない — [GitHub Docs](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
- gitは `GIT_AUTHOR_DATE` / `GIT_COMMITTER_DATE` 環境変数で任意の日付を指定できる — [git-commit docs: DATE FORMATS](https://git-scm.com/docs/git-commit#_date_formats)

**利用規約ページの自動スナップショット**
- Open Terms Archive: 宣言（取得URL＋CSSセレクタ）ごとに規約ページを1日数回取得してスナップショットを記録し、そこから「version」を抽出してコレクション別のGitHubリポジトリに公開する。表示ではハイパーリンクや文字スタイルの変化が見えない場合がある — [Open Terms Archive docs: Main concepts](https://docs.opentermsarchive.org/concepts/main/); [OpenTermsArchive GitHub](https://github.com/OpenTermsArchive)

### Inferences
- 対応表（推論。上記出典の組み合わせ）:
  - 時刻: RFC 3161 / OpenTimestamps / Rekor は「T以前に存在した」（上限）のみを示す。「T以降に作られた」（下限）や「Tに取得した」は示さない。Waybackのキャプチャ時刻はアーカイブ運営者の記録に依存する。
  - 出所（URL）: 第三者ウェブアーカイブ（Wayback, Perma.cc）だけが「URL UからこのバイトがTに返された」をある程度第三者として裏付ける。署名・タイムスタンプは自己申告のURLを固定するだけ。
  - 完全性: SHA-256などのハッシュ、SWHID、Rekor/OTSでのハッシュ固定はいずれも有効。
  - 権利: どれも証明しない。C2PAやSLSAの来歴も「署名者が主張した」ことの証明にとどまり、ユーザーの思考実験の結論（署名は「鍵保持者KがハッシュHについてライセンスLを主張した」だけを示す）と整合する。
- PROV-Oは語彙（データモデル）であって証拠ではない。SOURCE.toml を PROV で書き直しても証明力は増えず、相互運用性が上がるだけ（`hadPrimarySource`、`generatedAtTime` 等で既存フィールドを写像できる）。
- C2PAは主に画像・動画などのメディア資産向けで、CSV/JSONデータセットの取得証跡として個人が使う実益は小さいと考えられる。

### Gaps
- in-toto.io の仕様本体、Software Heritage FAQ、Perma.cc の about/料金ページ、Wayback の Save Page Now ヘルプは取得できず未検証。
- W3C PROV が信頼・セキュリティを範囲外と明言しているかは、PROV-O 後半とPROV-DMを読んでいないため未確認。
- git の署名対象にコミットオブジェクトの日付ヘッダが含まれる（日付も改ざん検知される）が「日付の真正性」は保証しない、という点は一般的理解だが、今回は一次資料で確認していない。

## Q2. 既知の失敗モード（アーカイブからの除外、アーカイブ改ざん・リプレイ問題、C2PAメタデータ除去、鍵侵害）

### Takeaway
ウェブアーカイブは「除外・削除されうる」「再生時に現在のウェブが混入しうる」「運営主体の信頼性が揺らぐ（archive.today）」。C2PAはメタデータ除去が最大の弱点で、普及率も低い。署名・タイムスタンプ系は鍵やIDアカウントの侵害に弱いが、透明性ログと「タイムスタンプが失効より前」の証明で一部を緩和できる。

### Cited Findings
- **アーカイブ除外**: Waybackはrobots除外やサイト所有者の要請で除外されることがあり、権利侵害が疑われる内容は裁量で削除しうる — [Internet Archive Help](https://help.archive.org/help/wayback-machine-general-information/)
- Internet Archiveは2017年に、robots.txtは主に検索エンジン向けで、アーカイブ目的には必ずしも適さないとの立場を示した（政府・軍のサイトでは以前からrobots.txtを無視していた） — [Internet Archive blog 2017-04-17](https://blog.archive.org/2017/04/17/robots-txt-meant-for-search-engines-dont-work-well-for-web-archives/)
- **アーカイブ再生の改ざん**: Lerner, Kohno, Roesner「Rewriting History」(ACM CCS 2017)は、アーカイブのサーバを侵害せずに、ドメイン所有者がWayback上の過去スナップショットの見え方を変えられることを示した（archive-escape: 再生時にライブのウェブコンテンツが混入する）。2011年のreuters.comスナップショットを完全に制御する概念実証を行った。開示を受けてInternet ArchiveはCSPヘッダを導入した — [論文PDF](https://homes.cs.washington.edu/~franzi/pdf/Lerner-RewritingHistory-CCS17.pdf); [UW Security Lab](https://seclab.cs.washington.edu/2017/10/30/rewriting-history-manipulating-the-archived-web-from-the-present); [DSHR's blog](https://blog.dshr.org/2017/09/attacking-users-of-wayback-machine.html)
- **archive.today の信頼性問題**: 2026年、Wikipediaの編集者はarchive.todayへのリンク（約70万件）を除去する方針を決めた。理由はセキュリティブロガーへのDDoS関与の疑いと、スナップショットに名前を挿入する改変が行われたように見える事例。Wikipediaは原典かWayback等の他アーカイブへの置換を推奨している。FBIが2025年10月30日付でレジストラTucowsに召喚状を出したとの報道もある — [TechSpot](https://www.techspot.com/news/111296-wikipedia-may-remove-almost-700000-links-amid-archivetoday.html); [Tom's Hardware](https://www.tomshardware.com/software/search-engines/archive-today-allegedly-leads-bizarre-ddos-campaign-against-security-blogger-wikipedia-considers-removing-all-links-to-the-archive); [Wikipedia Signpost 2026-03-10](https://signpost.news/2026-03-10/Technology_report)（いずれも報道・二次情報。改変の事実関係は未検証）
- **C2PAメタデータ除去**: CAIは「SNSやコンテンツプラットフォームがメタデータを除去することは依然として一般的」と認める。対策として metadata＋不可視透かし（TrustMark）＋フィンガープリントの「durable Content Credentials」を提示しているが、除去後の検索は現状Adobe実装に結び付いている — [CAI blog: Three pillars of provenance](https://contentauthenticity.org/blog/three-pillars-of-provenance)
- C2PA仕様自体も、メタデータは除去されうるため、ハードバインディング（暗号ハッシュ）とソフトバインディング（透かし・フィンガープリント）を組み合わせると説明している — [C2PA 2.2 Explainer §6.2, §7.2.3](https://spec.c2pa.org/specifications/specifications/2.2/explainer/Explainer.html)
- 普及: CDNはリサイズ時にC2PA/IPTCメタデータを消しがちとの報告（CBC） — [IPTC PHMDC 2025 発表資料](https://iptc.org/download/events/phmdc2025/IPTC-PHMDC-2025-Marcos_Armstrong.pdf)。報道画像・映像のうちC2PAメタデータを含むのは1%未満（Reuters Institute引用。二次資料経由で未検証） — [SoftwareSeni](https://www.softwareseni.com/c2pa-adoption-in-2026-hardware-platforms-and-verification-reality)
- **鍵/ID侵害**: Sigstoreでは、OIDCアカウントが盗まれれば有効な証明書が発行されうる。緩和策は証明書透明性ログだが、Fulcioは自分では監視しないため、利用者が自分のIDへの不正発行を監視する必要がある — [Sigstore docs: Security](https://docs.sigstore.dev/about/security/)
- RFC 3161: TSA鍵が漏洩すれば、その鍵で署名された全トークンが信頼できなくなる。一方で、タイムスタンプは「署名が証明書失効より前に作られた」ことを示し、失効後も検証可能にする用途を持つ — [RFC 3161 §1, §4](https://www.rfc-editor.org/rfc/rfc3161)
- GitHubの永続的検証記録は、後で鍵を失効させても過去コミットの「Verified」表示を維持する（逆に、漏洩鍵で作られた過去の署名も遡って無効化されない） — [GitHub Docs](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)

### Inferences
- 利用規約ページを第三者アーカイブに残すだけでは、後でそのサイトが除外を求めれば閲覧できなくなりうる。ローカルにも原本（WARC/HTML）とハッシュを保持する二重化が必要。
- Rewriting Historyの攻撃は「再生時の見え方」を変えるもので、保存済みバイトを変えるものではない。キャプチャ時にハッシュをローカル記録しておけば、後の再生結果との差異を検出できる。
- archive.todayの事例は、アーカイブ運営主体の信頼性そのものが証拠価値の前提であることを示す。単一アーカイブ依存は避けるべき。

### Gaps
- 2017年以降のWaybackのリプレイ脆弱性の現状（CSPの完全適用など）は確認できず。
- OpenTimestampsのカレンダーサーバ停止時の扱い（pendingのまま失われるリスク）を一次資料で確認できなかった。

## Q3. 証拠価値（ウェブアーカイブの裁判での受容、宣誓供述書要件、日本の例）

### Takeaway
米国ではWaybackキャプチャは自己認証的ではなく、Internet Archive職員の宣誓供述書、関係者証言、または相手方の合意・裁判所の職権認知（judicial notice）で認証されるのが通例。日本では知財高裁平成19年3月26日判決が、Wayback記録の証明力を利用規約の免責と誤表示例を理由に否定した例がある。一方、自己申告の日付やメール記録も容易に改変できるとして同判決で排斥されており、現状の「自己申告日付のみ」は証拠としてほぼ無価値と考えるべき。

### Cited Findings
- **米国**: *Sensory Path Inc. v. Fit & Fun Playscapes LLC*（N.D. Miss. 2022年12月20日）では、Internet Archiveの「Records Request Processor」による宣誓供述書（Waybackの仕組みを説明し、2枚のスクリーンショットの真正性を証明）を証拠から排除する申立てが却下された。宣誓供述書は真正性のみに関わり、実体的証言は含まない。原告は第5巡回区 *Weinhoffer v. Davie Shoring* を「Wayback証拠は自己認証的でない」とした判例として引用した — [eDiscovery Today](https://ediscoverytoday.com/2023/02/09/motion-to-strike-trial-exhibit-which-was-wayback-machine-affidavit-denied-ediscovery-case-law/)
- 必要な宣誓供述書を出さずにWaybackの印刷物を提出し、排除された連邦裁判所の例がある。一方で、キャプチャ者の宣誓供述書と状況証拠（URL、印刷日等）で足りるとした裁判所もある。Internet Archive自身が結果の正確性を保証しないと免責していることを理由に、職権認知を拒んだ例もある — [Cullen LLP blog](https://cullenllp.com/blog/can-i-use-archive-org-to-authenticate-electronic-evidence); [GFR Law](https://www.gfrlaw.com/what-we-do/insights/admitting-evidence-internet-authentication-still-required); [ABA Litigation 2015](https://www.americanbar.org/groups/litigation/committees/commercial-business/practice/2015/recent-federal-court-ruling-admissibility-online-evidence/)（法律事務所ブログ等の二次資料。個別判決原文は未確認）
- Fordham Law Reviewの論文は、アーカイブされたウェブページには認証に加えて最良証拠（best evidence）の問題があると論じる — [Fordham Law Review vol.78](https://ir.lawnet.fordham.edu/flr/vol78/iss1/15/)
- **Internet Archiveの宣誓供述書サービス**: 2013年版の方針（アーカイブ経由）では1件$250＋拡張URLごとに$20（ダウンロード可能ファイルは$30）、公証は別途$100、所要は支払い後5営業日。Internet Archiveはまず職権認知か相手方との合意を求めるよう勧めている。2023年に450件の宣誓供述書を発行した。現行の料金は未検証 — [archive.org/legal.html（2013年アーカイブ）](https://webarchive.di.uminho.pt/web.archive.org/web/20130716152143/http:/www.archive.org/legal.html); [LexisNexis 2019](https://www.lexisnexis.com/community/insights/legal/b/thought-leadership/posts/internet-archive-wayback-machine-helps-lawyers-go-back-in-time-to-strengthen-cases)
- **日本**: 知的財産高等裁判所 平成18年(行ケ)10358号、平成19年3月26日判決（第3部、商標「EIGOTOWN」の不使用取消し）。商標権者はウェブサイト上での使用を主張し、社内メール記録とWaybackの保存データを提出した。裁判所は以下を判示した:
  - メールについて「作成日は、作成者が使用するコンピュータで設定した日時に依存して記録されるものであって、容易に真実と異なる日時を表示することができる」。
  - Waybackについて「利用規約に記録内容の正確性について保証しないことが記載されている上、現に、ウェイバック・マシンに記録されている日経新聞のウェブサイトの内容について、真実と異なる内容が表示されている例が存在することに照らせば…直ちに…閲覧可能な状態となっていたことを認めることはできない」。
  - 審決も「コンピューターの画面上に表されている作成日やアドレス、ファイル名等は、これを書き換えたり…差し替えることも容易」としていた。
  — [裁判所 判例要旨PDF](https://www.courts.go.jp/assets/hanrei/hanrei-point_pdf-34406.pdf)
- 特許のインターネット公知とWaybackの扱いに関する国内の動向を論じた論文がある（日本大学） — [日本大学 知財ジャーナル](https://www.publication.law.nihon-u.ac.jp/pdf/property/property_18/each/04.pdf)（本文は未読）
- Perma.ccは法律分野の引用規範（Bluebook）で推奨されている — [Perma.cc docs](https://perma.cc/docs/accounts); [Wikipedia: Perma.cc](https://en.wikipedia.org/wiki/Perma.cc)

### Inferences
- 個人リポジトリのライセンス主張が実際に争われる場面（DMCA通知、権利者からの削除要請など）で求められるのは厳密な証明ではなく「善意で合理的に確認した」ことの説明であることが多いと考えられる。その目的なら「第三者アーカイブURL＋ローカル原本＋ハッシュ＋外部タイムスタンプ」で十分強い。裁判レベルの立証にはInternet Archiveの宣誓供述書など別の手当てが必要。
- 日本の知財高裁の判断は2007年のもので、Waybackの信頼性評価は事案依存。複数の独立証拠（第三者アーカイブ＋外部タイムスタンプ＋ローカル原本）を相互に補強させることが、単一証拠への依存より有効と考えられる。
- 日本でのRFC 3161系タイムスタンプ（認定タイムスタンプ事業者）の証拠価値は今回調査していない。

### Gaps
- 日本でWayback記録の証明力を肯定した裁判例は見つけられなかった（存在しないとは言えない）。
- OpenTimestamps（Bitcoinアンカー）を証拠として採用・検討した裁判例は見つからなかった。
- 日本の総務大臣認定タイムスタンプ制度（RFC 3161準拠）の法的効果は未調査。
- Internet Archive宣誓供述書の現行料金・手続ページは取得できず未検証。

## Q4. 個人リポジトリで実現可能な軽量な組み合わせ

### Takeaway
費用ゼロでできる現実的な最小構成は「(1) 取得したデータと利用規約/ライセンスページの原本をローカルに保存してSHA-256を記録、(2) Save Page Nowで第三者キャプチャを作りURLを記録、(3) ハッシュ一覧をOpenTimestamps（または無料のRFC 3161 TSA / Rekor）で固定、(4) 署名付きコミット」。これで「T以前にこのバイト列を保持していた」「第三者がTごろにこのURLからこの内容を見た」までは裏付けられる。「掲載者が権利者である」は依然として証明できない。

### Cited Findings
- OpenTimestampsは無料・登録不要のカレンダーサーバ経由でハッシュをBitcoinにアンカーでき、ハッシュはクライアント側で計算されるのでファイル内容は送信されない — [opentimestamps.org](https://opentimestamps.org/)
- RFC 3161 TSAはハッシュのみを受け取り、内容を検査せず、要求者も識別しない（プライバシー面は有利、出所証明としては無力） — [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161)
- Rekorは追記専用の透明性ログで、包含証明を取得できる。公開インスタンスのSLOは可用性99.5% — [Sigstore docs: Rekor](https://docs.sigstore.dev/logging/overview/)
- SWHIDはファイル/ディレクトリ単位でgit互換の内容ハッシュを与え、誰でも独立に再計算できる — [Software Heritage: SWHID](https://www.softwareheritage.org/?p=45638)
- Open Terms Archiveは「URL＋CSSセレクタ」の宣言で規約ページを定期取得し、版をgitリポジトリで公開する。自前で同様の仕組みを使うか、既存コレクションに追跡対象を提案できる — [Open Terms Archive docs](https://docs.opentermsarchive.org/concepts/main/); [GitHub](https://github.com/OpenTermsArchive)
- Waybackはrobots/所有者要請で除外されうるため、第三者アーカイブ単独には依存できない — [Internet Archive Help](https://help.archive.org/help/wayback-machine-general-information/)
- GitHubの検証記録は鍵失効後も永続する — [GitHub Docs](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)

### Inferences
- SOURCE.toml への追加フィールド案（推論・設計提案）:
  - `retrieved_at`（自己申告。単独では証拠価値なし）
  - `data_sha256` / `swhid`（取得データの内容ハッシュ）
  - `terms_url`、`terms_snapshot_sha256`、`terms_snapshot_path`（ローカル保存した規約HTML/WARC）
  - `terms_archive_urls`（`web.archive.org/web/<timestamp>/...` 等。複数可）
  - `ots_proof_path`（`.ots` ファイル。Bitcoin確定後に `ots upgrade` で完全証明に更新）
  - 任意で `rekor_log_index` や RFC 3161 `.tsr`
- 検査器（checker）で機械的に確認できるのは「ハッシュ一致」「.otsの検証（Bitcoin attestationの有無）」「アーカイブURLの到達性」まで。「ライセンスが真に有効か」は検査できないことを、DATA_POLICY で明示するのが誠実。
- タイムスタンプが示すのは「T以前に存在」だけなので、「取得時点」を下から抑えるには、第三者アーカイブのキャプチャ時刻（Wayback）が唯一の外部ソースになる。両者を組み合わせると、取得時点を「Waybackキャプチャ時刻ごろ〜OTSアンカー時刻以前」の区間で主張できる（ただしWayback時刻は運営者の自己申告）。
- C2PA、SLSA/in-toto、PROV-Oは個人の思考実験リポジトリにはオーバースペック。SLSA/in-toto形式は「データ取得をビルドとみなし、`resolvedDependencies` に uri＋digest を記録する」形に流用できるが、証明力はOTS＋ハッシュと本質的に同じで、署名者（自分）を信頼する前提は変わらない。
- 費用面: Perma.ccは個人の無料枠が実質なく（2019年以降）、Internet Archiveの宣誓供述書は有償（2013年時点$250〜）。平時は無料のSave Page Now＋OTSで記録だけしておき、紛争時に初めて有償手段を検討するのが現実的。

### Gaps
- Save Page Nowのレート制限・API認証要件（2026年時点）は一次資料を取得できず未検証。
- ArchiveBox等のセルフホスト型アーカイブツールや、`ots` CLIの現行バージョンは調査していない。
- 無料で使える公開RFC 3161 TSA（例: FreeTSA）の信頼性・継続性は未調査。
