# Judgments and resolution

Draft only; defaults stay `未判断`. Each draft needs `reason`, `confidence` and `based_on`.

```toml
[judgment.validity]
value = "未判断"      # 妥当 | 無効 | 重複 | 情報不足 | 範囲が広すぎる | 未判断
reason = ""
confidence = ""
based_on = []        # evidence ids
history = []         # { at, value, by, reason }
decided_by = "下書き（エージェント）"

[judgment.priority]  # when; usually the receiver's call
value = "未判断"

[judgment.owner]
component = ""
root_cause_likely_in = ""
ownership_unclear = false

[judgment.upstream]
gates = {}           # see stages.md
route = ""           # public issue | comment | private security report | none
value = "未判断"

[resolution]         # what happened, not what was judged; empty until it happens
value = ""
basis = []           # evidence the closing rests on
verified_by = ""     # who or what confirmed it (a re-run, a test); "未確認" if nobody did
addresses = []       # hypothesis ids it answers; a fix for another mechanism does not close this
```

Why: separating impact (severity) from scheduling (priority), and an explicit `未判断` default, let reviewers see what was actually assessed. Keeping `history` matters: a closed issue was reopened by a question, not by new evidence.
