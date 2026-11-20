# Bug part

```toml
[claim]
question = ""          # "why did X …" / "why didn't Y …" — forces an expected behaviour
responsible_party = "" # whose behaviour is wrong: user code, library, spec
observed = ""
observed_metric = ""   # if a quantity: definition and instrument (tools disagree)
expected = ""
expected_basis = []    # spec text | docs | earlier behaviour | other path of same impl
                       # | other implementation | reporter belief
counter_basis = []     # text that cuts against the expectation (read cited sections in full)
expected_status = "未確定"  # 確定 | 未確定 | 記述不足 (then ask, do not guess)

[reproduction]
artifact = ""          # test, URL, recording; a reporter tool printing "TRIGGERED" does not count
steps = []
same_bug_condition = ""  # by error text, value condition, environment — not by symptom
env_axes = []          # axes to compare, drawn from hypotheses
results = []           # { env = {axis: value or "不明"}, result, at, by, measured_with, evidence }
                       # demand the same detail for the side that did NOT reproduce
regression_range = "未実施"  # name the axis (version | OS | hardware); range | 未実施 | 該当なし（理由）

[[hypothesis]]
id = "H1"
statement = ""
location = ""          # suspected place, versioned; keep its history
how_to_test = ""
proposed_by = ""
who_can_test = ""      # reporters can often test in minutes
result = "未検証"       # 支持 | 棄却 | 未検証
evidence = []

[diagnosis]            # leave empty until reproduced; fill env_axes and missing instead
chain = []             # cause to symptom, each step with evidence ids
confidence = ""
unverified = []

[judgment.severity]    # impact; never mix with priority
value = "未判断"
preconditions = []
mitigations = []
most_general_condition = ""
reason = ""
```

Why: an empty receiver row in `results` showed a bug closed without being tried; the side that did not reproduce usually lacks the axis that matters.
