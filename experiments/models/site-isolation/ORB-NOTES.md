# ORB extension: what must be declassified

Model: `ORBExtension.tla` (EXTENDS SpecIsolation), config `ORB.cfg`
(`INVARIANT PrintORB`). Run time about 70 s.

## Source

- Fetch Standard at commit d7fc0fd (`fetch.bs`) does **not** contain ORB. No
  "opaque-response" or "ORB" text; the only related steps are "blocked due to
  its MIME type" (fetch.bs:3463, script-like destinations only), "blocked due to
  nosniff" (fetch.bs:4369) and the range-status check in main fetch
  (fetch.bs:5152). HTML only links the proposal (html.src:96814, in the
  credentialless warning).
- ORB text used: whatwg/fetch PR #1442 preview, https://whatpr.org/fetch/1442.html,
  section `#orb-algorithm` ("opaque-response-safelist check"), fetched
  2026-11-21, sha256 `927537e85c39c2406430ace6e841f54962aa8c2cc46aea55c89d367db72c8138`.
  Cross-checked with https://github.com/annevk/orb README (commit 61c1be7,
  lines 82-106), which says the PR "is in a more advanced state".
- Integration (PR, HTTP fetch, `ref-for-opaque-response-safelist-check③`): if
  response tainting is "opaque", status is not a redirect, and the check returns
  false, "then return a network error". This is **before** the CORP check, not
  after it. Both give a network error, so the order does not change observations.
- Output to the page: network error or the usual opaque response. The PR has
  no empty-body opaque variant (some engines do that; not modelled).

## ORB steps (PR #orb-algorithm), as modelled

Inputs: extracted MIME type, nosniff, status, the request's "no-cors media
request state" (N/A / initial / subsequent), the first 1024 bytes, and the whole
body. The request destination is **not** read.

1. MIME safelisted (JavaScript, text/css, image/svg+xml): allow.
2. MIME never-sniffed (pdf, zip, csv, ...): block.
3. 206 and MIME blocklisted (HTML/JSON/XML): block.
4. nosniff and MIME blocklisted or text/plain: block.
5. Media state "subsequent": allow.
6. 206 failing "validate a partial response": block (model: always valid).
7. Read first 1024 bytes (failure blocks; model: never fails).
8. Bytes sniff as audio/video: allow only if state "initial" and status 200/206.
9. State not "N/A": block.
10. Bytes sniff as image: allow.
11. nosniff: block. 12. Status not ok: block. 13. MIME failure: allow.
14. MIME essence audio/, image/, video/: block.
15. "determine if response is JavaScript and not JSON": read the whole body;
    JSON parse succeeds -> block; script parse succeeds -> allow; else block.

## Abstraction

New response fields: `mime` (safe, block, never, plain, avimg, other, none),
`nosniff`, `status` (200, 206, 404). The body is a record
`[secret, head, parse]`: `head` = what the first 1024 bytes sniff as (av, img,
text), `parse` = js / json / neither. `head` and `parse` are functions of the
bytes, so they are part of the secret, not declarations. The requester picks
the media state. `ObserveORB` inserts ORB on the cross-origin no-cors path;
CORS and same-origin are unchanged. `NI(D)` is NoUndeclaredLeak with
declaration function D, checked per context as "no declared value maps to two
observations" (equivalent to the pairwise form, cheaper).

## Results (Mutant = "none")

| property | Declared variant | result | witness / note |
|---|---|---|---|
| NI | D0 = SpecIsolation `Declared` | FALSE | B no-cors, no CORP, mime none, 200: body sniffing av -> error, img -> opaque (state N/A) |
| NI | D0 (JS witness) | FALSE | mime "block" (e.g. text/html), no nosniff, 200: body parses as JS -> opaque, as JSON -> error |
| NI | D0 + mime, nosniff, status | FALSE | same witnesses (only the body differs) |
| NI | D0 + headers + head sniff | FALSE | JS vs JSON witness |
| NI | D0 + headers + parse | FALSE | av vs img witness |
| NI | D0 + headers + head + parse | TRUE | |
| NI | D0 + headers + BodyBit | TRUE | BodyBit = verdict when ORB reached the body steps, else n/a |
| NI | D0 + ORB verdict bit only | TRUE | minimal addition |
| ORB only adds blocks | - | TRUE | ORB opaque => old Observe opaque |
| OptInOnlySecure with ORB | - | TRUE | |
| BodyOnlyByOptIn with ORB | - | TRUE | |
| secret irrelevant | - | TRUE | verdict depends on body only via head, parse |
| max body classes per header combo | - | 3 | |

## Declassification list

- Declared by the target (headers it chose): Content-Type class, nosniff,
  status (status is a server choice, so it is treated as declared). These alone
  are not enough.
- Genuine declassification (function of the body): one bit per request, the
  ORB verdict when it is reached past step 5. Its inputs are two body
  predicates: first-1024-byte sniff class (av / image / neither) and "parses as
  JavaScript and not JSON". The secret value itself does not flow (in this
  abstraction).
- More than one bit per response: the requester chooses the media state, so it
  can ask the question twice (N/A and initial). For one header combination,
  bodies fall into at most 3 classes (vectors over N/A, initial, subsequent:
  e.g. TFT for image or JS, FTT for audio/video, FFT for anything else), i.e.
  up to log2 3 ~ 1.58 bits per response. "subsequent" is body-independent and
  the PR says it should only be set by a trusted process.

## Limits

- Timing and size: step 15 waits for the whole body; the README note says
  this "might end up leaking the size". Not modelled (no time).
- Range and media: "validate a partial response" is assumed to pass; the
  main-fetch range-status check and media element state machine are not
  modelled; the media state is a free requester input.
- Partial bodies / stream errors (1024-byte read failure, body read failure)
  are not modelled; both block in the PR.
- JS parse depends on the encoding (charset, fallback encoding); folded into
  `parse`. A polyglot body that the attacker partly controls (reflection) turns
  `parse` into an oracle on the secret; the model's fixed predicates hide that.
- Engines that return an empty-body opaque response instead of a network
  error are not modelled; for those the page may not see error vs opaque in
  `fetch()` but still can through script/img load events.
- ORB is a PR, not the standard at d7fc0fd; results are about the PR text.
