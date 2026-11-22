# Havoc of unmodeled steps: results

For [experiments/2026-11-23-havoc-unmodeled-steps.md](../../../2026-11-23-havoc-unmodeled-steps.md). Written by a subagent. Everything here was classified by one author, and the guards and contracts are that author's reading. Spec text is not committed. `writesets.tsv` holds only algorithm names, step numbers and the author's labels.

## Files and how to run

- `writesets.py` builds `writesets.tsv`: `python3 -I writesets.py <closure_steps.tsv> writesets.tsv [--blind]`. The `--blind` flag skips the per-step hand table `REVIEW`.
- `HavocSpec.tla` extends `SpecIsolation` with havoc slots, the properties `OptInSecH`, `OptInH` and `COIOptInH`, witnesses and controls.
- `Singles-{none,coep-insecure,coep-cl-strips}.cfg` and `Sets.cfg`: run `sh havoc/run.sh Sets Singles-coep-insecure Singles-coep-cl-strips` from `site-isolation/`. `extract.py` keeps only the `havoc-*` prints. TLC evaluates every zero-arity `Print*`, so `Sets` also prints the singles.
- `baseline.py` computes the baselines exactly: `python3 -I baseline.py writesets.tsv 3548`.

## Method

- A havoc point is a slot in the model's data flow: effective COEP, the creds bit seen by the CORP check, the secure bit, parsed COOP, group COI mode, COI capability, response origin or record, tainting, mode, request origin.
- Each write row maps to one point (the `havoc_point` column).
- For a point in `HS`, the slot ranges over its whole type. The value is chosen per context: `v` is quantified inside the property, and each slot has its own field.
- Every range contains the model's value, so breaking is monotone in `HS`.
  - `Sets.cfg` confirms that, for each property, the union of all the points that don't break it still holds.
  - `Conservative` is TRUE: with `HS = {}`, `FetchH` and `COIH` equal `FetchResult` and `CrossOriginIsolated`.
- The properties:
  - `OptInSecH` is OptInOnlySecure.
  - `OptInH` is OptInOnly. It is already false, so it is used only for the positive control.
  - `COIOptInH` is COIOnlyWithOptIn with no DIP. It reads the creds bit the CORP check saw, as `ReqD` does.
- `Omit` is a parameter, so one module runs the model both with and without each omitted step.

## 1. Write set

| measure | count |
|---|---|
| closure steps | 3548 |
| write rows (assign 1356, branch with embedded write 297 incl. 42 guarded early returns, return 26, call 1) | 1680 |
| rows writing a model-read concept | 218 (only 118 = 54% assign-form) |
| ... modeled / unmodeled / composite response / input / outside both properties / out of scope / not read / unmodeled check | 66 / 47 / 35 / 28 / 33 / 5 / 3 / 1 |
| gaps: target undetermined (Let-locals without concept cue 747, collection ops 152, unparsed 57) | 956 (57% of write rows) |
| non-write steps that may write via callee or prose (call 238, external-call 34, remainder 373) | not classified |

Two row labels need defining:
- "Input": the value is upstream of both the property and the read site, so the model's quantification already covers it.
- "Composite": the step writes a whole response record.

A sample of 50 gap rows found 1 missed write to a model-read concept (a policy-container local). I fixed that pattern. Extrapolating, about 2% of gaps (about 20 rows) may still hide such writes.

The 47 unmodeled rows fall into 7 points. Only 27 of them are assign-form.

| point | rows | writers (algorithm / step) |
|---|---|---|
| h-ecoep-inherit | 15 | clone a policy container 3; determine navigation params policy container 1.2, 2.2, 3; new browsing context and document 19.2; navigate 24.8.1, ... |
| h-secure | 9 | secure context 1.2.1, 1.3, 2 (worker owner, worklet, data:); top-level creation URL (set up a window environment settings object 6, ...) |
| h-creds-mode | 9 | HTTP-network-or-cache fetch 8.3 (credentials mode); redirect-taint; COEP allows credentials 5 |
| h-coop | 6 | navigate 24.8.5; srcdoc 4; javascript: URL 13; obtain an opener policy 4.3 (noopener-allow-popups) |
| h-respurl | 4 | HTTP-redirect fetch 18; HTTP-network-or-cache fetch 12; main fetch 10, 16 |
| h-coimode | 3 | obtain a browsing context for a navigation response 2 (nested: group kept), 9.2 (no swap), 10 (new group) |
| h-sw | 1 | HTTP fetch 3.4 (Service Worker response; boundary) |
| h-coicap | 0 | no closure step writes it (getter plus Permissions Policy, outside the closure) |

**Both known omissions are branch-form steps** (obtain an embedder policy step 2; HTTP-network-or-cache fetch 8.4).
- An assign-only write set, which the record's premise proposed, misses both.
- In a blind run (`--blind`), 8.4 is selected with concept creds.
- Step 2 is selected only through a rule added after the fact: a guarded early return in an algorithm that returns a concept counts as a write (42 rows). Before that rule, step 2 was in the table only because I listed it by hand in `REVIEW`.
- Three other rows still come in only through `REVIEW`: new browsing context 11.1 and 11.2, and CORP internal check 4.
- The modeled or unmodeled status of every row is a hand judgement.

## 2. Havoc results (`Omit = "none"`)

Base: OptInSec TRUE, OptIn FALSE (known), COI TRUE. "x" means the point alone breaks the property.

| point | concept | step | OptInSec | COI | witness (o; r; havocked value) |
|---|---|---|---|---|---|
| h-ecoep-inherit | COEP | policy-container inheritance | x | x | https a.test; www1.a.test, CORP none; ecoep := unsafe-none |
| h-secure | secure | secure context, nesting | x | | https a.test; www1.a.test, none; secure := FALSE |
| h-creds-mode | creds | HTTP-network-or-cache 8.3 | | | (holds) |
| h-coop | COOP | navigate 24.8.5, ... | | x | a.test, COOP and COEP unsafe-none; www1, none, creds; coop := same-origin-plus-COEP |
| h-respurl | origin | HTTP-redirect fetch 18 | x | x | a.test; b.test, same-site; final origin := www1.a.test |
| h-coimode | COI mode | obtain a browsing context 2, 9.2 | | x | as h-coop; coimode := concrete |
| h-sw | response | HTTP fetch 3.4 | x | x | a.test; a.test, none; SW response := www1, same-site |
| h-coicap | capability | (none) | | x | as h-coop; cap := TRUE |
| h-tainting (modeled) | tainting | main fetch 12.x | x | x | a.test; a.test, none; taint := opaque |
| h-reqorigin-any (unguarded) | origin | navigation params 5.1 | x | x | b.test; a.test, same-site; request origin := www1.a.test |
| h-ecoep-insecure, h-creds-cl, h-reqorigin (guarded); h-mode; h-coicap-mono | | | | | hold |

Joint run: the real unmodeled set, with or without h-coicap, breaks both properties.

Contract variants limit each point to the values its writers can produce:
- `-c`: a default or the model's own value.
- `-adh`: any COI mode, but only with a compatible COEP.
- `-k`: the property is restated on the delivered response. This holds by construction, because the delivered response becomes just another quantified input.

| variant | OptInSec | COI |
|---|---|---|
| h-secure-c (the bit can only be lowered) | **x** | |
| h-coimode-adh (any mode if COEP is compatible) | | holds |
| h-coop-c, h-coimode-c, h-coicap-mono; h-respurl-k, h-sw-k (by construction) | | |
| unmodeled set with contracts (h-ecoep-inherit has none) / same set without h-ecoep-inherit | x / x | x / holds |

- **h-secure-c is a real gap**, of the same kind as coep-insecure. An https document nested under an http top level, or a data: document, is not a secure context, so its COEP is the default and a cross-origin no-cors response without CORP comes back opaque, even though `Secure(o)` holds. OptInOnlySecure needs "secure context", not "https origin". The contract is approximate (http://localhost is potentially trustworthy, so the bit can also rise); the break comes from lowering, so the finding stands.
- **h-coimode points at an unmodeled check COI relies on.** Type-wide havoc of the mode breaks COI; with the child-navigable embedder-policy adherence check imposed (COEP must be compatible), COI holds. I first labelled that check "outside both properties"; that was wrong, and it is now `unmodeled-guard`.
- **h-ecoep-inherit is a premise mismatch.** The property names the COEP from the header, but the model reads the policy container's COEP.
- **h-coop, h-respurl and h-sw are artifacts of type-wide havoc**, which decouples what the spec couples (COOP with COEP, a header with its response). For h-coop-c, writer 4.3 (noopener-allow-popups) is outside the model's types and the contract; that it cannot make the document cross-origin isolated is reasoning, not a TLC run.

## 3. Controls

**Positive control: coep-insecure.**
- With the step omitted, the base is TRUE, TRUE, TRUE.
- h-ecoep-insecure sits at the identity slot the step writes (EffectiveCOEP), guarded by `~secure`. It turns OptIn FALSE; witness http a.test, ecoep := unsafe-none.
- **The control passes, but the point was seeded by hand.** Without `REVIEW`, the pipeline finds this step only through the early-return rule.
- Side effect: with the step omitted, h-secure and h-secure-c no longer break OptInSec. The omission removes the only place the secure bit is read, and havoc cannot see writes to a slot the model never reads.

**Positive control: coep-cl-strips.**
- The properties keep the same values with or without the step (TRUE, FALSE, TRUE), and h-creds-cl changes nothing.
- Neither safety property depends on this step, so at the property level the positive control has n = 1.
- At the behaviour level it passes for both omissions:
  - `Differs` is TRUE: the omission changes some fetch result.
  - `Recovers` is TRUE: havoc at h-creds-cl covers every result of the full model.

**Negative controls.** None could have failed; each holds for a structural reason.
- Slot never read: report (14 rows), timing (52), sandbox (8), KeyKind (9), PopupSevered (24).
- Guard never fires on this path: h-reqorigin, and h-ecoep-insecure under `Secure(o)`.
- Premise made false: h-mode, and taint := basic or cors, make the result non-opaque. Both properties constrain only opaque results, so they are blind here. This is blindness, not robustness.
- Tautology: h-creds-mode for COI, because the property reads the bit being havocked.

**Baselines** (exact, by monotonicity).
- Point level: a random 8 of the 15 type-wide points breaks OptInSec with P = 0.9986 and COI with P = 1.0.
- Step level: a random 47 of the 3548 steps breaks a property with P ≈ 0.37; 47 of the 1680 write rows, P ≈ 0.63; 47 of the 218 concept rows, P ≈ 1.0.

**At the set level, type-wide havoc is vacuous.** The claim "the property holds for the closure" fails for almost every set as large as the real one. What discrimination there is lies in the step-to-point mapping and in per-point contracts.

## 4. Against R1 to R4

- **R1 (works): partly.** Per point, havoc gave pointers; with contracts three remain: a real gap (secure context versus https origin), an unmodeled check COI relies on (adherence), and a premise mismatch (inherited COEP). The set-level claim did not survive.
- **R2 (vacuous): supported at the set level** for type-wide havoc.
- **R3 (targets undeterminable): supported.** 57% of write rows have no determinable target; 46% of the writes to model-read concepts are not assign-form, including both control steps; the selection needed a rule added after the fact plus hand seeding; the ranges needed hand-written contracts.
- **R4 (boundary): supported.** h-sw (Service Workers) and h-coicap (Permissions Policy, no closure step) had to be added by hand.

## Limits

- One author classified everything. About 100 rows were reviewed step by step (`REVIEW`) and the rest by per-algorithm rules (`second_pass`). Only 50 gap rows were sampled.
- Points are per slot, not per step.
- The guards and contracts are the author's.
- The types are the model's, so havoc never produces values outside them (for example noopener-allow-popups).
- Witnesses are whatever CHOOSE picks first.
- Only safety properties were checked, with `Mutant = "none"` for the shared operators.
