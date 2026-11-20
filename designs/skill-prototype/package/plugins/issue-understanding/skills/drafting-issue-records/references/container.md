# Container part (one symptom, many causes)

Use when many reports share a symptom. Judge sameness per cluster, not for the whole issue.

```toml
[[cluster]]
id = "A"
fingerprint = ""        # first error text, volume type, runtime version …
same_bug_condition = ""
resolving_action = ""   # what made it go away; sometimes the only separator
version_range = ""
reports = 0             # "+1 / same here" only adds to this count
tracked_in = ""
state = ""

[[report]]
link = ""
env = {}
fingerprint = ""        # "不明" when no log; do not assign a cluster without one
fixed_claim = ""        # "it's fixed" and any later contradiction
cluster = ""            # or 仮に入れる（未判定）
contributed = []        # evidence ids this report added
```

Steps:

1. Search each fingerprint's exact error text, including closed issues and fix titles; a sibling fix may already exist.
2. Assign reports to clusters only by fingerprint or resolving action, never by symptom alone.
3. Propose splitting a cluster into its own issue (`related.merge = 分ける`); the maintainer decides.
4. Suggest `judgment.validity = 範囲が広すぎる` when no single cause can cover the issue.

Why: a "pods stuck terminating" issue held at least eight causes; grouping by first error text matched the real outcome, and one group's fix had a title equal to the error text.
