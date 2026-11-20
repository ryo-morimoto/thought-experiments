# Output

Produce two things, in the user's language.

1. **The record**, as TOML, with only the parts for the kind. Field names stay as defined; values in the user's language.
2. **A summary of at most 8 lines**:
   - kind and stage reached, and the stage minimum still unmet
   - the claim in why-did / why-didn't form (request: the problem, and the proposed solution)
   - the strongest evidence and its check
   - the top two open hypotheses with how to test (request: the top options, incl. workarounds)
   - the one question to ask next, and to whom
   - drafted judgments with confidence, marked as drafts
   - what a human must decide

Rules:

- Quote the issue sparingly (a sentence or two) with its URL; summarise the rest.
- Refer to people by role (reporter, maintainer), not by name.
- Mark every inference as an inference.
- If you checked code or re-ran something, say exactly what, at which version.
- If you stopped below stage 3, say what would raise it.
