# ORB verdict leakage under an adaptive attacker (self-composition)

For [experiments/2026-11-24-selfcomp-orb-leak.md](../../../2026-11-24-selfcomp-orb-leak.md)
(tree node B5). A subagent wrote and ran this on 2026-11-24 and committed nothing.
`../ORBExtension.tla` (`ORBAllows`) is reused unedited. Raw TLC output: `out/<cfg>.txt`.
Rerun from `site-isolation/`: `sh selfcomp/gencfg.sh; sh selfcomp/runall.sh` (N4: 24 min).

## Abstraction

- Body = `A0 s1 A1 s2 ... sN AN`. Secret bit `si` is one byte: 1 -> `"` (q), 0 -> a
  letter (a). `Ai` are attacker-reflected snippets: empty or one byte from `"`, `/`,
  newline; `A0` may also be `g`, a magic byte that sniffs as an image.
- Attacker control: **none** (server's own body), **ends** (reflected prefix and
  suffix `A0`, `AN`), **all** (attacker fields interleaved with secret fields, e.g.
  a list of records where each line mixes a user-supplied field and a secret field).
- "Parses as JS and not JSON" (PR #1442 step 15) at the lexer level: strings `".."`,
  line comments `// ..` to newline, a raw newline inside a string is a syntax error,
  code bytes always compose (as if the template put operators between them). JSON =
  exactly one string literal with surrounding whitespace. Then `ORBAllows` decides.
- 1024-byte sniff class: `img` iff the body starts with `g`, else `text`. The toy
  body fits in 1024 bytes; secret bytes never form a signature, so the sniff class
  depends on the attacker's prefix only.
- Headers fixed to the leaky combination of ORB-NOTES (mime `block`, e.g. text/html
  or application/json, no nosniff, 200), no CORP, requester without require-corp:
  the page sees exactly the verdict (error vs opaque). The attacker also picks the
  media state. For N = 2, the header combinations under which some query separates
  secrets are exactly mime block/plain/other without nosniff and status 200, plus
  plain/other with 206 (`leaky-headers` in `out/Count-N2.txt`).
- Why this is enough for the question (ORB-NOTES, "Limits"): ORB-NOTES treats
  `parse` as a fixed body predicate and says reflection turns it into an oracle.
  Here `parse` is computed from bytes that both sides write, which is the dependence
  the earlier objection said the fixed predicate hides. The lexer is a strict
  under-approximation of JS syntax, so counts are lower bounds for a real attacker
  with this snippet alphabet; the bit oracle and the any-predicate oracle give the
  upper bound (one binary observation per query: at most 2^k classes).

## Counting (`SelfCompORB.tla`, `Count-*.cfg`)

`Best(P, k, Secrets)` = maximum, over adaptive strategies of depth k (decision
trees whose nodes are queries), of the number of non-empty leaves, i.e. secret
classes distinguished by the observation sequence. `kernel` = classes for unbounded
k. Bits = log2(classes).

| N | control | k=1 | k=2 | k=3 | k=4 | kernel | bits at k=N |
|---|---|---|---|---|---|---|---|
| 2 | none | 2 | 2 | | | 2 | 1 |
| 2 | ends | 2 | 4 | | | 4 | 2 |
| 2 | all | 2 | 4 | | | 4 | 2 |
| 3 | none | 2 | 2 | 2 | | 2 | 1 |
| 3 | ends | 2 | 4 | 6 | | 6 | 2.58 |
| 3 | all | 2 | 4 | 8 | | 8 | 3 |
| 4 | none | 2 | 2 | 2 | 2 | 2 | 1 |
| 4 | ends | 2 | 4 | 6 | 6 | 6 | 2.58 |
| 4 | all | 2 | 4 | 8 | 16 | 16 | 4 |
| 3 | all, ORB without step 15 (`sniffonly`) | 1 | 1 | 1 | | 1 | 0 |
| 2..4 | bit oracle (any predicate: N <= 3), reference | 2 | 4 | 8 | 16 | | k |

Distinct query predicates: none 3, ends 8, all 14 / 56 / 180 (N = 2 / 3 / 4).

## Declassification policies (delimited release)

A policy is an escape hatch `Hatch(s)`, a function of the secret alone. It holds
iff secrets with equal hatch give equal observations on every query; by induction
this equals "equal observation sequences for every adaptive strategy and every k".
Checked by `DR` for N = 2, 3, 4 (same verdicts at every N):

| policy | none | ends | all |
|---|---|---|---|
| nothing declared (SpecIsolation `Declared`) | fails | fails | fails |
| verdict of the server's own body, per media state | **holds** | fails | fails |
| 1024-byte sniff class of the server's body | fails | fails | fails |
| sniff class + parse of the server's body (ORB-NOTES `DHdrBoth`) | holds | fails | fails |
| kernel (coarsest policy that holds) | holds, 2 classes | holds, 6 classes | holds, = the secret |
| ORB without step 15, nothing declared (`sniffonly`) | holds | holds | holds |

"Declare the verdict bit" (ORB-NOTES `DVerdict`): the declared value is the
observation itself, so `NoUndeclaredLeak` holds by definition, but the verdict is a
function of the secret alone only with no control (`verdict-is-secret-fn`: none TRUE,
ends FALSE, all FALSE).

## Self-composition state machine (`SelfCompRun.tla`, `SC-*.cfg`, N = 3)

Two runs share the attacker; `s1 # s2` start with equal hatch. While histories are
equal a deterministic strategy picks the same query in both runs, so one shared
nondeterministic query per round covers every adaptive strategy. `SCNI`: histories
equal after K rounds (2-safety). `VIEW` drops the trace-only `lastq`.

| cfg (control, policy, K) | result | witness (bytes `A0 s1 A1 s2 A2 s3 A3`) |
|---|---|---|
| none, nothing, 1 | violated | 000 vs 001: `aaa` is JS (opaque), `aa"` unterminated (error) |
| all, nothing, 1 | violated | same pair, empty snippets |
| ends, fixedverdict, 3 | violated | 000 vs 011 (`aaa`, `a""`: both JS, same fixed verdict): prefix and suffix `"` give `"aaa"` (JSON, error) vs `"a"""` (JS, opaque) |
| all, fixedverdict, 3 | violated | 000 vs 011: `A2 = /`, `A3 = "` gives `aa/a"` (comment, opaque) vs `a"/""` (unterminated string, error) |
| all, sniffparse, 3 | violated | same as above |
| none, fixedverdict, 3 | holds (390 states) | |
| none, sniffparse, 3 | holds (270 states) | |
| ends, kernel, 3 | holds (60 states) | merged classes {010, 111}, {011, 110} |
| all, kernel, 3 | holds vacuously | kernel separates all 8 secrets: no initial pair |
| all, nothing, 3, sniffonly | holds (840 states) | |

## Reading

- R1 (one bit per query, all after N queries): **holds when the attacker controls
  positions inside the secret** (all: 2^k classes, the optimum for a binary
  observation, reached at k = N for N = 2, 3, 4).
- R2 (leak limited): **holds for no control** (1 bit total, whatever k) and **in part
  for prefix/suffix control** (saturates at 6 classes, 2.58 bits, for N = 3 and 4;
  more queries do not help); a richer snippet alphabet may raise it.
- R3 (a fixed-function list exists): **only without attacker content** (verdict of
  the server's own body) or by removing step 15. With attacker content the only
  fixed function that holds is the kernel, which depends on the attacker's
  capability and, with full control, is the secret itself.

## Limits
- Lexer-level JS only (strings, comments, newlines; no charset). Snippets of length
  <= 1; one byte per bit; secret never in a sniff signature; N <= 4.
- ORB cannot tell attacker bytes from server bytes, so "verdict of bodies without
  attacker content" restricts the threat model; ORB cannot enforce it.
- No timing or size channel, no media state machine, no engine behaviour.
