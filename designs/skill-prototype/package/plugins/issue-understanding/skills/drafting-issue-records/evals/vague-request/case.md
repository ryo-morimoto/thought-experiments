# Case: a feature request with no stated problem

## Setup
A one-line feature request asks a command-line search tool for a new flag ("like `--files` but for directories", or "list only text files"). No use case, no example output. Use only the opening post.

## Prompt
"この要望をトリアージして、記録を下書きして: <issue URL>"

## Gap this case shows
In trials (ripgrep #169, fd #749) the empty field was the problem, not the details. Detail questions are easy to write and were wasted when the request was declined. The question that surfaced the real need paired the use ("what do you feed the output into?") with a workaround to try. One trial also missed a workaround built from the tool's own features.

## Pass criteria
- Uses the request part, not the bug part (no `claim.question` of why-did form, no hypotheses).
- `request.problem` is `不明` or flagged as missing; `spec_clarity = 目的不明`.
- The first question asks for the use and offers a concrete workaround, in one message (`question.form`).
- `option` includes "do nothing" and at least one workaround, including one that combines the tool's own features; workarounds are marked `tested` only if actually run.
- `decision_point` entries, if any, carry `needed_if = 受け入れ` and are not asked yet.
- `dup_search` uses problem terms and solution terms.

## Fail signals
- The first question is about details (naming, flags, output format).
- `spec_clarity` is set to 明確 or the request is treated as a bug.
- `judgment.acceptance` is drafted without `confidence` and `based_on`.
