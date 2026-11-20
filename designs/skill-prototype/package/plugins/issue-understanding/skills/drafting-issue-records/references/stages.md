# Who fills what, and what to hand over

Roles:

- **Reporter**: observed behaviour, own environment row, answers, quick tests where `who_can_test` names them.
- **You (investigator)**: evidence, `dup_search`, `related`, `env_axes`, hypotheses with tests, `missing`, questions, draft judgments. Decisive fields (`responsible_party`, `expected_basis`) are usually yours: grep the versioned source; asking the reporter rarely fills them.
- **Tools**: code-citation matching, re-runs, searches, location existence, value checks.
- **Maintainer**: final judgments, merge decisions, resolution, deferral.

Stages are cumulative: a stage counts only if every earlier one is met.

Stage minimums (the only hard rule: no blank fields; `不明` or a `missing` item is fine):

| Stage | Bug | Request | Container |
|---|---|---|---|
| 1 Intake | source, observed, one env row, ≥1 evidence | problem or proposed_solution, ≥1 use case | fingerprint per report |
| 2 To investigate | expected + basis (or 記述不足 + question with asks_for), ≥1 dup_search (error text, else symptom wording), artifact or `needs-repro` | spec_clarity, agreement, references checked or not | same_bug_condition per cluster, reports assigned (仮 ok) |
| 3 To decide | key claims as 観測/文書 with mechanical_check, ≥1 hypothesis tested, env_axes incl. non-reproducing side, drafted judgments | ≥2 options incl. do-nothing/workaround, constraints | resolving_action or missing per cluster, tracked_in |
| 4 Upstream | all upstream gates pass | same gates | gates per cluster |

Upstream gates: minimal reproduction; regression range (or why n/a); not environment-specific; duplicates searched (`dup_search` present); only verifiable claims; safe to disclose.

Close gates, before suggesting invalid or misuse: a receiver result row; if misuse, the source of the broken contract; a duplicate search in component terms.
