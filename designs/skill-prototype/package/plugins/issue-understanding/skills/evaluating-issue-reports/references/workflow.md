# Workflow

1. **Fix `as_of`**: time, last comment used, versions. Use nothing later. Check the timeline up to `as_of` too (labels, edits, links).
2. **Pick the kind** from the content, not the labels: bug, request, container (one symptom, many causes), security (add to bug). Labels go in `reporter_labels`; a third of tracker labels are wrong.
3. **Take every reporter statement as `主張（未確認）`.** Promote to `観測` or `文書` only after you or a tool checked it; text, steps and real-looking locations are cheap to fake.
4. **Ask about ambiguous words.** If a key word can mean two things ("close", "doesn't work"), add a question; do not silently pick one.
5. **Check mechanically, cheapest first.** Match quoted code at the stated version. Re-run given tests if you can. Search duplicates twice and log both in `dup_search`: by error text, or by symptom wording when there is none (requests: problem terms and solution terms); and by component terms. Include closed issues.
6. **Settle the expected behaviour before the cause** (bug), or the problem before the solution (request). Read a cited spec or doc section in full and keep sentences that cut the other way (`counter_basis`). If you cannot settle it, mark it and ask with `asks_for`.
7. **Write causes as hypotheses with how to test**, not answers or locations; for requests write options, including "do nothing" and workarounds built from the tool's own features. Test cheap ones yourself; name `who_can_test`. Keep refuted ones.
8. **Never leave a field blank.** Write `不明` or a `missing` item with `next`.
9. **Draft judgments last**, with `reason`, `confidence`, `based_on`. Before suggesting a close, meet `close_gates`; a claimed fix elsewhere must name what it fixed and be checked against your hypotheses.
10. **Stop at the stage you honestly reach**; never invent facts. Do not post or contact anyone.
