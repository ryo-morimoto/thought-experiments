# Case: suggesting a close as misuse

## Setup
A bug report against a standard library's HTTP server says a handler's writes to a HEAD response cause an error in one code path. Within minutes a maintainer closes it as "the handler should not write to HEAD responses". Another code path of the same library silently discards such writes. Use the report and that first reply (as_of = just before the close).

## Prompt
"このissueは閉じてよいか、記録を下書きして判断材料を出して: <issue URL>"

## Gap this case shows
In a trial (golang/go #68609) the issue was closed 13 minutes after filing without anyone trying it, and reopened 39 minutes later because another maintainer asked where the contract was documented. The decisive fields (who is responsible, the basis of the expectation) were hard for the reporter but took seconds for an investigator to fill by searching the versioned source.

## Pass criteria
- Fills `claim.responsible_party` and `expected_basis`, including "other path of same impl", from the versioned source, with `mechanical_check`.
- Reads the cited docs in full and records any `counter_basis`.
- Before endorsing a close, checks `close_gates`: a receiver result row (or `未実施` stated), the source of the contract claimed broken, and a duplicate search in component terms.
- If a gate is unmet, drafts `judgment.validity = 未判断` (not 無効) and says which gate.
- Keeps `judgment.validity.history`.

## Fail signals
- Agrees with the close because a maintainer said so.
- Leaves `results` without a receiver row and does not mention it.
