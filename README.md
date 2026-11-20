# thought-experiments

思考実験の記録。自作物は [CC0-1.0](LICENSES/CC0-1.0.txt)。

扱うデータは、公開されていて、利用条件が明確で、二次利用が許可されているものに限り、ライセンスを守って使う。思考実験の記録は [experiments/](experiments/README.md) にあり、段階ごとに書き残す。詳しくは [DATA_POLICY.md](DATA_POLICY.md)（保証の範囲と、証明できない前提も書いてある）、利用中のデータのクレジットは [NOTICE.md](NOTICE.md) にある。

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
