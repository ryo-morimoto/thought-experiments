# Feature request part

Use instead of the bug part's claim, reproduction, hypothesis, diagnosis and severity.

```toml
[request]
problem = ""            # the problem to solve. Empty → suspect an XY problem; ask this first
proposed_solution = ""  # what was asked for
use_cases = []          # { text, at, source } — borrowed ones need source and date; keep before/after close apart
references = []         # { impl, behavior, checked } — check the cited behaviour yourself
spec_clarity = "未確定"  # 目的不明 | 細部未定 | 明確
agreement = "未確定"     # 合意 | 未確定 | 対立 (then ask the maintainer, not the requester)

[[option]]
id = "O1"               # always include "do nothing" and any workaround
statement = ""
serves = []             # which use cases
changes_default = false
compatibility = ""
tested = false          # was the workaround actually tried
known_gaps = []
rejected_because = ""

[[constraint]]          # the maintainer's criteria, with source
text = ""
source = ""

[[decision_point]]      # details to settle
text = ""
needed_if = "受け入れ"   # do not ask these before acceptance
decided = ""

[interface]             # after acceptance
name = ""
takes_value = false
misuse_check = ""

[judgment.acceptance]
value = "未判断"         # 受け入れ | 却下 | 回避策で足りる | 保留（需要待ち）| 未判断
confidence = ""
based_on = []
demand_evidence = []
reason = ""
```

Why: in vague requests the empty field was the purpose, not the details. Detail questions are easy to write and wasted if the request is rejected. The question that surfaced the real need paired the use ("what do you feed the output into") with a workaround to try. A request can be clear yet contested; marking it 記述不足 sends the wrong question to the requester.
