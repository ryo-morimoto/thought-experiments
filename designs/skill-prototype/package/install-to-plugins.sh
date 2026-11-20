#!/usr/bin/env bash
# issue-understanding を ryo-morimoto/plugins の新しいブランチに入れる。
# 使い方: bash install-to-plugins.sh
# 何をするか: origin/main から feat/issue-understanding の worktree を作り、
# plugin を複写し、marketplace.json に足し、生成物を作り直し、検査を通してから
# commit と push をする。検査に落ちたら commit せずに止まる。main には触らない。
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/plugins/issue-understanding"
REPO="$HOME/ghq/github.com/ryo-morimoto/plugins"
BRANCH="feat/issue-understanding"
WT="$REPO/.claude/worktrees/issue-understanding"

test -d "$SRC" || { echo "package not found: $SRC" >&2; exit 1; }
git -C "$REPO" fetch origin
if git -C "$REPO" show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "branch $BRANCH already exists; remove it or rename BRANCH" >&2; exit 1
fi
git -C "$REPO" worktree add -b "$BRANCH" "$WT" origin/main

test ! -e "$WT/plugins/issue-understanding" || { echo "plugin already exists on main" >&2; exit 1; }
cp -r "$SRC" "$WT/plugins/"

python3 - "$WT/.claude-plugin/marketplace.json" <<'PY'
import json, sys
p = sys.argv[1]
d = json.load(open(p, encoding="utf-8"))
if not any(x["name"] == "issue-understanding" for x in d["plugins"]):
    d["plugins"].append({
        "name": "issue-understanding",
        "description": "課題やバグ報告を理解し評価する記録を下書きする。報告者の主張と確かめた証拠を分け、判断は人に任せる",
        "source": "./plugins/issue-understanding",
        "category": "development",
    })
open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
PY

cd "$WT"
python3 tools/catalog.py render
python3 tools/catalog.py check
for c in plugins/*/skills/*/scripts/check_limits.py; do
  echo "== $c"; python3 "$c"
done
for t in plugins/*/tests; do
  echo "== $t"; python3 -m unittest discover -s "$t"
done

git add -A
git commit -F - <<'MSG'
feat(issue-understanding): 課題とバグ報告の記録を下書きする skill を追加 (experimental)

課題（issue）やバグ報告を、主張と確かめた証拠に分けて記録する skill
drafting-issue-records を追加する。種類（バグ・要望・症状の入れ物・セキュリティの
主張）ごとの欄、担い手と段階ごとの最低限、試用から作った評価ケース 4 件を含む。
設計の根拠は ryo-morimoto/thought-experiments の designs/ にある。

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
MSG
git push -u origin "$BRANCH"
echo "pushed $BRANCH. worktree: $WT"
