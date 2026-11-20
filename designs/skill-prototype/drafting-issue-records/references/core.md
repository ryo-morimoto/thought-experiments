# Core fields (every kind)

```toml
[meta]
kind = ""            # bug | request | container | security
stage = 1            # highest stage whose minimum is met (stages.md)
source = []          # issue/thread URLs
as_of = ""           # time + last comment used + versions
versions = {}
reporter_labels = [] # kept apart, not trusted

[[evidence]]
id = "E1"
kind = "主張（未確認）"  # 主張（未確認）| 観測 | 文書
statement = ""
source = ""          # output, log, URL, or commit/tag + path + line
checked_by = ""      # never the reporter
mechanical_check = "" # how it was checked (code match at version, re-run, search)

[[missing]]
item = ""
state = ""           # needs-repro | needs-env | needs-env-info | needs-bisection | needs-spec-check
                     # | needs-runtime-check | needs-reference-check | needs-maintainer-decision
                     # | needs-design | needs-use-case
next = ""            # who does what next

[[question]]
text = ""
to = ""
asks_for = []        # fields the answer must fill; answered only when they are filled
form = ""            # e.g. "what do you feed the output into" + "does this alternative suffice"

[[related]]
link = ""
relation = ""        # same cause | same symptom | prerequisite | test problem | history | split off
                     # | symptom container | known design limit | derived request | external solution
                     # | same claim rejected
differs_in = ""
evidence = ""
merge = "まとめない"  # まとめる | まとめない | 仮に入れる（未判定）| 分ける. Unsure: don't merge.

[[dup_search]]
query = ""
query_kind = ""      # error text | symptom wording | component terms | problem terms | solution terms
where = ""
at = ""
found = []

[[deferral]]
at = ""
reason = ""
missing_then = []
```

Judgments and resolution: `judgments.md`.
