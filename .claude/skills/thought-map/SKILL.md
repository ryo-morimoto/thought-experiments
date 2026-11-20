---
name: thought-map
description: このリポジトリで、思考実験を回しながら地図（maps/<name>/map.toml）を埋める。標準や論文の分類を軸に空白と次の推論方向を出し、ユーザーに選んでもらって1セルずつ進める。「地図」「次どこを考える」「思考実験を進める」「空いているところ」と言われたとき、または新しい問いを地図にしたいときに使う。
---

# 思考実験の地図を埋める

地図は「2つの軸で区切った問いの空間」。1回のループで1セルだけ動かす。結論はユーザーと一緒に出し、根拠のない結論は書かない。

## 0. 地図を選ぶ・作る

- 既存の地図: `ls maps/`。ユーザーが問いだけを持ってきて、合う地図がなければ新しく作る。
- 新しく作るとき（`templates/map.toml` をコピー）:
  1. 問いを1文にする。
  2. 軸を **既存の標準・論文の分類から** 探す（alphaXiv、WebSearch、ISO/W3C/NIST などの用語集）。候補を2〜3個、出典つきで AskUserQuestion で示して選んでもらう。
  3. 出典の本文で値の定義を確かめたら `ref_read = true`。見つからなければ `basis = "own"` で始めてよい（候補に「根拠を探す」が出続ける）。
  4. 調べた内容は `research_notes/<地図名>/` に残す（既存のノートの書き方に合わせる）。

## 1. 候補を出して選んでもらう

引数に `maps/<name> <row>/<col>`（または `axis:rows` / `axis:cols`）があれば、map.html の「コピー」から来た指定なので、選択を飛ばしてそのセルで 2 に進む。理由とモードは `frontier --json` の該当項目を使う。

引数がなければ候補を出す。ユーザーには `maps/<name>/map.html` をブラウザで開くと全体と候補の理由が見られることを伝える。

```sh
python3 tools/thought_map.py frontier maps/<name> --top 6
```

上位から3つを AskUserQuestion の選択肢にする（4つ目は「地図全体を見る」）。各選択肢の description には、セル名・状態・モード・**なぜそこか**（隣のセルのどの結論から推論するのか）を1〜2文で書く。ユーザーが別のセルや新しい軸を言ったらそれに従う。

候補の種類:
- `contested` / `hypothesis`: 反例探し（destructive）
- `open`: 置かれた問いに答える（constructive）
- 空セルで隣に結論がある: 行と列の結論を前提に組み立てる、または隣の結論が移るかを試す
- 軸が自作・出典未確認: 既存の分類と突き合わせる（値が増えたら地図が広がる）

## 2. 思考実験を回す

`running-thought-experiments` スキルがあればそれに従う（問いの枠組み → モード → 条件を変える → 結果を攻撃する）。セルの行と列の値の定義（map.toml の note）を前提条件として明示する。

- 事実が要る箇所は調べて出典をつける。推論だけで出した部分は推論と書く。
- 1回の実験はユーザーとの往復で進める。前提を置く・条件を変えるときはユーザーに確認する。
- 記録は `experiments/YYYY-MM-DD-<slug>.md` に書く（雛形: `templates/experiment.md`）。

## 3. 地図を更新する

map.toml のセルを追加・更新する。

- `status`: 裏付けが取れたら `supported`、仮説が崩れたら `refuted`（崩れたこと自体を claim に書く）、根拠が割れたら `contested`、まだなら `hypothesis`。
- `claim`: そのセルの結論を1〜3文で。
- `evidence`: 実験の記録と出典。
- `mode`: 今回回したモード。`next_question`: 実験中に出てきた次の問い。
- 実験中に、別のセルに効く結論や、軸に足りない値が見つかったら、そのセルに `open` を置くか軸に値を足す（足すときはユーザーに確認する）。

```sh
python3 tools/thought_map.py render maps/<name>   # map.html を再生成
python3 tools/thought_map.py check
python3 tools/check_data_policy.py
```

最後に、変わったセル・埋まり具合（map.html の合計）・次の候補上位3つを短く報告して、続けるか聞く。
