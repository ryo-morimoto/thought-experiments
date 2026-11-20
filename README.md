# thought-experiments

思考実験の記録。自作物は [CC0-1.0](LICENSES/CC0-1.0.txt)。

扱うデータは、公開されていて、利用条件が明確で、二次利用が許可されているものに限り、ライセンスを守って使う。詳しくは [DATA_POLICY.md](DATA_POLICY.md)（保証の範囲と、証明できない前提も書いてある）、利用中のデータのクレジットは [NOTICE.md](NOTICE.md) にある。

## 思考実験の地図

問いの空間を2つの軸で区切った表を `maps/<name>/map.toml` に書き、思考実験で1セルずつ埋めていく。軸にはなるべく既存の標準や論文の分類を使う（自作の軸には「既存の分類に置き換える」候補が出る）。空いているセルについては、同じ行・列の結論からどう推論するかの候補をツールが出す。

```sh
python3 tools/thought_map.py frontier maps/<name>   # 次に考える候補（理由と推論モードつき）
python3 tools/thought_map.py render                 # map.toml から MAP.md を生成
python3 tools/thought_map.py check                  # 形式と MAP.md の鮮度（pre-commit と CI でも実行）
```

Claude Code では `/thought-map` で、候補の提示 → 選択 → 思考実験 → 地図の更新、の1ループを回す（[.claude/skills/thought-map/SKILL.md](.claude/skills/thought-map/SKILL.md)）。雛形は [templates/map.toml](templates/map.toml) と [templates/experiment.md](templates/experiment.md)、最初の地図は [maps/data-license-assurance/MAP.md](maps/data-license-assurance/MAP.md)。

## セットアップ

```sh
git config core.hooksPath .githooks   # コミット前にデータ利用ポリシーを検査する
pipx install reuse                    # 全ファイルのライセンス宣言の検査（なくても CI で検査される）
```

## データを追加するとき

```sh
cp templates/SOURCE.toml data/<name>/SOURCE.toml   # 埋める
python3 tools/fetch_evidence.py data/<name>        # 証拠（ハッシュ・タイムスタンプ・Internet Archive）
python3 tools/check_data_policy.py --fix           # REUSE.toml と NOTICE.md を生成して検査
```
