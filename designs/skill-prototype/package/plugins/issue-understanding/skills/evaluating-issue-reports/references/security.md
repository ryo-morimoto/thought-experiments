# Security part (add to the bug part)

```toml
[taint_path]
steps = []             # { text, kind = data | state | config, location = commit-or-tag + path + line }
guards = []            # { check (location), why_bypassed } — existing checks on the path
value_condition = ""   # the values that trigger the defect
always_wrong_if_reached = false  # e.g. freeing stack memory: path detail then goes to severity
```

Validity needs **an observation, or a mechanically checked path with a value condition**:

- Check each `location` exists at the stated version and the quoted code matches. Accept tags as well as commits.
- Trace the first step's data back in the source: attacker-controlled (redirect target, input) or internal (the program's own random value). Internal → the path fails.
- Accept `why_bypassed` only as (a) a concrete value that passes the guard's expression and satisfies `value_condition` — substitute it; if the two cannot hold together, the claim fails on that path; or (b) a state step, with location, where the guard's effect is lost. Anything else is `未回答`.
- Ask a question only when stated numbers differ from constants in the source; do not ask when the conditions contradict each other.
- A reproduction made by changing timing only (inserting a delay) counts as an observation.
- Look for the same claim already rejected (`related.relation = same claim rejected`).

Route: a bypass of a protection is a possible security bug. Draft `judgment.upstream.route = private security report`; never post details publicly.

Why: demanding receiver-side observations rejected genuine reports. Free-text guard reasons were faked cheaply; tracing the first value and testing joint satisfiability stopped both bogus reports and passed both genuine ones.
