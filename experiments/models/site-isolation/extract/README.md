# HTML と Fetch の算法を段ごとに取り出す試み

思考実験 [experiments/2026-11-20-browser-semantics-soundness.md](../../../2026-11-20-browser-semantics-soundness.md) の「(a) 仕様の版に対しては、段ごとの機械的な取り出しで相対的な健全性が立つ」を確かめるために、subagent が書いたスクリプト。筆者は結果の要約を読み、スクリプトがローカルのファイルしか読み書きしないことを確かめた。仕様の原稿と、取り出した段の本文（仕様の文の引用になる）はコミットしていない。

## 使った仕様の版

[commits.txt](commits.txt)（WHATWG の各リポジトリのコミットと、取得した原稿の sha256）。

## 動かし方

```sh
python3 -I parse_spec.py html <html の source> out/html.json
python3 -I parse_spec.py bikeshed <fetch.bs> out/fetch.json
python3 -I analyze.py out/html.json out/fetch.json out
python3 -I audit.py out <乱数の種>        # 分類の抜き取り検査
python3 -I spot.py out <算法名> <行番号>   # 個別の段の確認
```

`parse_spec.py` の第 1 引数（html か bikeshed）は、原稿の書式の違いを選ぶ。HTML は Wattsi、Fetch は Bikeshed で書かれている。

## 分類の規則

段の本文を小文字にして、順に照合する。

1. 残り（取り出せない段）: `in parallel`、`queue a … task`、`wait` などの待ち、`implementation-defined`・`optionally`・`user agent may` などの実装の選択、`applicable specifications` などの他の仕様からの差し込み。並行の段の中の段も残りに数える。
2. 取り出せる形: assert、分岐、繰り返し、return、中断、制御、代入、呼び出し。
3. HTML と Fetch の外の算法だけを呼ぶ段は「境界」。
4. どれにも当たらなければ「散文だけ」（残り）。

「取り出せる」は形の判定で、段の中の条件の文は自然言語のまま残る。
