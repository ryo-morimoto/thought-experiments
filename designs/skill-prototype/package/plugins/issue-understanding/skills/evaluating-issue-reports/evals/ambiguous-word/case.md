# Case: an ambiguous key word in a bug report

## Setup
A public bug report says diagnostics "disappear when I close" a buffer and reopen it. The editor has several commands that could count as "close" (`:e`, `:bd`, `:bw`, closing a window). The first maintainer reply asked which one was meant. Use only the opening post (as_of = before the first maintainer reply).

## Prompt
"この issue を理解して、記録を下書きして: <issue URL>"

## Gap this case shows
In a trial (neovim/neovim #32247) the agent silently read "close" as `:e`, built hypotheses on that reading, and missed the maintainer's first question. The real cause was among its hypotheses, but the record looked more certain than the report allowed.

## Pass criteria
- Adds a `question` to the reporter naming the readings of the ambiguous word, with `asks_for` pointing to the claim or reproduction fields it would settle.
- Does not pick one reading in `claim.observed` without marking it as an assumption.
- Hypotheses carry `how_to_test`; none is written as an answer or a bare code location.
- `dup_search` has at least one search by symptom wording (there is no error text) and one by component terms, including closed issues.
- Stops at the stage honestly reached and says what would raise it.

## Fail signals
- The ambiguous word is resolved silently.
- `dup_search` is missing or uses only error text.
- A judgment other than `未判断` appears without `reason`, `confidence` and `based_on`.
