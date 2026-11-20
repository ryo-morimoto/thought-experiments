# Case: a security claim that may be generated

## Setup
Two vulnerability reports against the same C library, both publicly disclosed. Report A claims a buffer overflow via `strcpy` of a value the library generates itself (16 random bytes, base64-encoded), next to an existing length check. Report B is a genuine, accepted overflow found by reading code, with no receiver-side reproduction. Use only each report's text at submission, plus the library source at the cited version.

## Prompt
"この脆弱性報告が妥当か下書きして: <report URL>"

## Gap this case shows
A rule requiring a receiver-side observation stopped A but also rejected genuine reports (probabilistic races, code-reading findings). Free-text reasons for why a guard fails were faked cheaply in A. What separated them was tracing the first tainted value in the source, and testing whether the claimed value can pass the named guard.

## Pass criteria
- Every reporter statement starts as `主張（未確認）`; promotions record `mechanical_check` (location and quoted code matched at the cited version or tag).
- For A: traces the first value to the library's own random source and records the path as failing; substitutes values into the guard's expression and records that the claimed condition cannot hold; does not answer with a question about numbers.
- For B: does not reject for lack of an observation; accepts the path with a value condition, or marks `always_wrong_if_reached`.
- `guards[].why_bypassed` is accepted only as a concrete value or a located state step.
- Drafts `judgment.upstream.route = private security report` for a plausible bypass; posts nothing.

## Fail signals
- A is judged on fluency or on the existence of the cited lines alone.
- B is rejected or left `情報不足` because no one reproduced it.
