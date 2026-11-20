# データポリシーの規約準拠は、正しい意味で証明できるか

- 状態: 結論済み
- 開始: 2026-11-20
- 更新: 2026-11-21（さかのぼって記録）
- 関連: [DATA_POLICY.md](../DATA_POLICY.md)、[報告書：データライセンス準拠ツールの限界](../reports/データライセンス準拠ツールの限界.md)、[調査メモ](../research_notes/データライセンス準拠ツールの限界/)、[続き：著作物でないデータに、ライセンスの義務は及ぶか](2026-11-21-non-copyrightable-obligations.md)

## 問い

このリポジトリがライセンスと利用規約を守っていることを、「証明できた」なら実際に守れている、という保証付きで示せるか。

## 前提

- **規約準拠** は3つの層に分ける。①内部整合（リポジトリが宣言と矛盾しない）、②事実整合（宣言が現実と合う。提供者が権利者である）、③法的評価（争いになったときに準拠と判断される）。
- **証明** は前提からの形式的な導出。**正しい意味で** は健全性（誤って OK を出さない）と読む。完全性は問わない。
- モード: 破壊的（どの層で証明が壊れるかを探す）。

対立仮説:

- P1 原理的に不可能。示せるのは「宣言が正しければ準拠」という条件付きの命題だけ。
- P2 部分的に可能。判定できる部分は証明し、残りは証拠で支える。
- P3 形式ライセンスと提供者の署名を揃えれば、②まで証明できる。
- P4 仕様に相対的な証明なら、ソフトウェアの正しさと同じ意味で可能。
- P5 ①ですら不可能。データの検出を拡張子に頼ると漏れる。

設定の欠陥: 「正しい意味」がひとつに決まることを前提にしている。証明の定義次第で結論が決まってしまう。

## 条件を変える

1. **証明の定義を動かす。** 形式証明では①しか届かない。法的立証（高度の蓋然性）では「許諾があったこと」は立証できるが、くつがえり得る。監査可能性では、証拠を残せば②の手前まで届く。判定を分けるのは「結論がくつがえり得る経験的な命題であってよいか」。署名が示すのは「鍵の持ち主が主張した」ことまでなので、**P3 は脱落**。P4 は P1 に吸収された。
2. **条件付き命題「宣言が正しければ準拠」を試す。** そのままでは証明できない。網羅性（宣言されていないデータがない）と、忠実性（検査の規則がライセンスの義務を含意する）の2つの前提が要る。ODbL 4.6（派生データベースの提供義務）が反例になった。忠実性は同値でなくてよく、**規則がライセンス本文より厳しければ十分**（含意で足りる）。
3. **実装を積み上げる（L0〜L4）。** 網羅性（L1）、忠実性（L2）、証拠（L3）、監査（L4）。L4 まで実装しても、提供者が権利者であること、規則が義務を含意すること、法的評価の3つは残る。
4. **既存の製品を調べる。** どの製品・標準も、機械で守れるのは層①まで。層②は人手の仕組み（Wikimedia Commons の License review など）でしか埋まっていない。アグリゲータのライセンス表記は約7割が未指定で、16〜29%は実際より緩く表示されていた（報告書を参照）。

## 結果を攻撃する

- **A1:** カタログと規約ページはどちらも同じ提供者が出している。2系統の独立した裏付けではなく、「提供者の表示どうしに矛盾がない」にすぎない。
- **A2:** `.csv` を `.txt` に変えて置くと、拡張子で判定する検査をすり抜けた。ルートの REUSE.toml の一括宣言も同じ穴を作っていた。
- **A3:** タイムスタンプが示すのは「ある時刻より前に存在した」だけ。取得元を示すのは Internet Archive の保存だけで、手元の写しとの一致を照合していなかった。

## 結論

| 前提 | 種類 |
| --- | --- |
| 証明は健全な導出、準拠は層①〜③に分けて考える | 定義上 |
| 層①は、ファイルの形をしたデータについて、規則集 R に照らして証明できる | 論証 |
| R はライセンス本文より厳しいので、R を満たせば義務も満たす | 論証（形式化はしていない） |
| 組んだ仕組み（REUSE、RFC 3161、Internet Archive、attestation）は実際に動く | 経験的（確認済み） |
| 提供者が権利者であること、日本での証拠としての重み | 未検証 |

**答え:** 正しい意味で証明できるのは、層①を規則集 R に照らした範囲まで。層②は証拠で支えることしかできず、層③は証明の対象にならない。

生き残り: P2。脱落: P3（署名が示すのは主張まで）、「2系統の独立した裏付け」（A1）。P4 は P1 に吸収。

## 具体

### 調査の材料

- 既存製品の調査（層①〜③・網羅性・忠実性・証拠保全の対応表、誤表示率の数値と出典）: [reports/データライセンス準拠ツールの限界.md](../reports/データライセンス準拠ツールの限界.md)、調査メモ: [research_notes/データライセンス準拠ツールの限界/](../research_notes/データライセンス準拠ツールの限界/)
- 忠実性の突き合わせで読んだ条文: CC BY 4.0（https://creativecommons.org/licenses/by/4.0/legalcode.en ）、CC BY-SA 4.0（https://creativecommons.org/licenses/by-sa/4.0/legalcode.en ）、ODbL 1.0（https://opendatacommons.org/licenses/odbl/1-0/ ）、PDL1.0（https://www.digital.go.jp/resources/open_data/public_data_license_v1.0 ）

ODbL 1.0 4.6 の要旨（反例の根拠）: 派生データベースか、そこから作った制作物を公衆に利用させるときは、派生データベース全体か変更点のファイルを機械可読な形で提供しなければならない。元のデータベースから直接作った制作物は対象外。

### 既製品を動かして分かったこと（実行の記録）

`reuse spdx` は確認値（LicenseConcluded）を出さない。REUSE 6.3.0 で、宣言を書いたファイルを出力した結果:

```
FileName: ./data/osm/roads.csv
LicenseConcluded: NOASSERTION
LicenseInfoInFile: ODbL-1.0
```

RFC 3161（FreeTSA）は openssl だけで発行・検証まで完結した:

```
Status: Granted.
Time stamp: Nov 20 14:20:45 2026 GMT
Verification: OK
```

Internet Archive の保存内容（`id_` 付き URL）は gzip で返ることがあり、そのまま比べると不一致になった。CC の規約ページで、保存側 12,786 バイト（gzip）に対し、手元は 54,711 バイト。展開すると sha256 が一致した（`8a0bd54c7eb714d6…`）。

attestation は、gzip した tar ではハッシュが git のバージョンで変わり、第三者が再現できなかった（CI `a67803a2…`、手元 `0b3a5c93…`）。圧縮しない tar に変えると一致した:

- タグ v0.1.1、署名対象 `repo-v0.1.1.tar` の sha256 `10c68b8be6bdc82108404d43b0415f7f415aa2c1af8a579826d85b7e2c776ce8`
- attestation: https://github.com/ryo-morimoto/thought-experiments/attestations/70179845 （CI 実行 https://github.com/ryo-morimoto/thought-experiments/actions/runs/44754767341 ）
- 検証: `git archive --format=tar -o repo.tar v0.1.1 && gh attestation verify repo.tar --repo ryo-morimoto/thought-experiments --predicate-type https://github.com/ryo-morimoto/thought-experiments/data-policy-check/v1` は終了コード 0、1 バイト変えた tar は終了コード 1
- 予測型の URL にアンダースコアを含めると、GitHub API の絞り込みが `HTTP 422: predicate_type invalid predicate type provided` を返した

### 攻撃（A2・A3）の再現と、塞いだ後の検査の出力

A2（拡張子を変える）を塞いだ後、CSV を `notes.txt` として置いた結果:

```
  - notes.txt: 自作物の拡張子・パス（data-policy.toml の [own]）でなく、SOURCE.toml の管轄下にもない。データなら出所を宣言する
notes.txt: no license identifier
notes.txt: no copyright notice
```

A3（取得元の照合）の実データでの結果は、江戸川区のデータ（参照は [2026-11-21-non-copyrightable-obligations.md](2026-11-21-non-copyrightable-obligations.md) の「具体」）と気象庁のデータ（[data/jma-typhoon-generation/EVIDENCE/evidence.json](../data/jma-typhoon-generation/EVIDENCE/evidence.json)）の両方で、データ本体・規約とも保存内容が手元の写しと一致した。

### 判例（著作権法13条により権利の対象外）

知財高裁 平成18年(行ケ)10358号（平成19年3月26日判決）は、Internet Archive の記録の証明力を否定した（利用規約が正確性を保証していないこと、誤表示の例があることを理由とする）。同じ判決は、自己申告の日付も退けている。調査メモ: [provenance_and_evidence.md](../research_notes/データライセンス準拠ツールの限界/provenance_and_evidence.md)

## 経過

- 2026-11-20 段階A〜C。結論を受けて、L1〜L4 を実装した（REUSE、`SOURCE.toml`、証拠の取得、確認値、attestation）。
- 2026-11-20 Software Heritage への保存依頼を入れたが、時刻の記録は attestation と重なり、「違反に気づいたら履歴から削除する」方針と衝突するので外した。
- 2026-11-20〜21 A2（拡張子の穴、ルートの一括宣言）と A3（Internet Archive の照合）を塞いだ。A1 は原理的に消えないので、提供者の種別の制限、第三者の権利の確認、表現の訂正で確率を下げた。

## 次の問い

- 著作物でないデータに、そもそもライセンスの義務は及ぶか → [2026-11-21-non-copyrightable-obligations.md](2026-11-21-non-copyrightable-obligations.md)
- 未検証: 日本で、RFC 3161 タイムスタンプや Internet Archive の保存がどれだけ証拠として認められるか（知財高裁 平成19年3月26日判決は Wayback の証明力を否定している）。
