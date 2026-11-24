# Step-level dataflow over HTML and Fetch steps: results

For [experiments/2026-11-24-write-target-semantics.md](../../../2026-11-24-write-target-semantics.md) (tree nodes B2b, B2c). Written by a subagent. One author wrote the rules, the criteria and the groups. Spec text is not committed. The tables hold algorithm names, step numbers, source line numbers, variable and field names, and the author's labels.

## Files and how to run

- `specscan.py` turns a spec source into one token list per step. It uses the same list and note state machine as `../extract/parse_spec.py`, but it keeps `<var>`, links and `<dt>` markers.
- `dataflow.py` runs the analysis: `python3 -I dataflow.py <extract/out> <html.src> <fetch.bs> ../havoc/writesets.tsv <outdir>`. Inputs: html.json, fetch.json and closure_steps.tsv from `../extract`, plus the sources at the commits in `../extract/commits.txt`.
- `flows.tsv` has one row per closure step: its defs, its calls with the argument-mapping kind, its holes and its slice roles.
- `closed-list.tsv` has one row per closure step in the slice: its roles, slice level, distance, concepts, the havoc status and the verdict.
- `holes.tsv` lists every hole in the closure and every unbound relevant local. `summary.json` holds all the counts below.

## Analysis design

- **Cells.** A local `(algorithm, var)`, which includes parameters; a global cell per non-algorithm dfn (struct fields, getters, concepts), shared by all objects, so the analysis is field-based and does not tell objects apart; and `RET(algorithm)`.
- **Cross-references.** Links resolve to dfns, with the resolver from `../extract/analyze.py`. Two additions: a `for=` must match, and a Fetch link to a field that HTML defines is matched by its for and text.
- **External fields.** A link after `'s` to an external struct (URL, Infra) becomes a global cell.
- **Aliases.** Two derived getters are aliased by hand: request/current URL is treated as URL list, and so is response/URL.
- **Defs.** These forms write a cell: `let V be`; `set LV to`, including chained `and LV to`, and `it` resolved to the previous left side or the condition's last `x's F` chain; `for each V of`; struct literals (`whose F is`, `<dt>F</dt>`); collection verbs (append, remove, extend and the like) on LV; `return`; callback parameters (`steps given V`). A write to `x's A's B` also weakly writes A.
- **Uses.** A def reads the tokens in its own value region. Left sides are left out, and so are base pointers: a var or field directly followed by `'s <link>`.
- **Calls.** A call reads `RET(callee)`. Arguments flow to parameters by name (`X set to Y`), else by position (the chunks after the link, against the parameter vars in the dfn's preamble), else to every parameter (fallback). Of 727 closure call sites, 640 are positional or named and 87 use the fallback.
- **Control.** A step depends on its enclosing steps and on any earlier step in the same algorithm that can exit (return, abort, throw, continue, break).
- **Slices.** Each slice is a backward worklist over all 10198 parsed HTML and Fetch steps, then restricted to the 3445 closure steps:
  - **data**: data dependence only;
  - **ctrl**: data plus control. This is the primary slice.
  - **full**: ctrl plus object identity (base pointers and left sides).
- **Criteria.** 24 cells for the 13 model-read concepts of `havoc/writesets.tsv`, listed in `CRITERIA` and in `summary.json`. Examples: the policy container's embedder policy, the embedder policy's value, `RET` of the CORP checks and of COEP allows credentials, `RET(secure context)`, request origin, mode and response tainting, response URL list, the response given to fetch response handover, the BCG cross-origin isolation mode, the cross-origin isolated capability, and `RET` of the COOP-match and BCG-switch algorithms.
- **Holes.** A step in the closure is a hole when the rules cannot place a write or a read: an untagged or unresolved target, a collection op with no target, another write verb, a prose-only step, an indirect call through an algorithm-valued variable, or an unresolved link or callback-bound var in a slice step. A hole is **on a relevant path** if the step is in the slice, or if it is a write hole in an algorithm that has a slice step. Relevant locals that have no writer and are not parameters are counted separately, as unbound.
- **Boundary.** A call to another spec counts as a pure function of its arguments. This is an assumption, not a hole.

## 1. Resolution of the havoc gap rows

Of the havoc gap rows, 954 are matched here. Two keys repeat in `writesets.tsv`.

| havoc gap kind | rows | target resolved by rule | relevant (data) | relevant (control only) | irrelevant |
|---|---|---|---|---|---|
| Let local | 746 | 701 (94.0%) | 226 | 361 | 114 |
| collection op | 152 | 104 (68.4%) | 31 | 50 | 23 |
| unparsed | 56 | 32 (57%) | 6 | 13 | 13 |
| total | 954 | 837 (87.7%) | 263 | 424 | 150 |

## 2. Slices (closure steps, of 3445)

| slice | steps | algorithms | modeled | unmodeled (known / gap / non-write) | excluded by havoc (notread / nocone / outscope) |
|---|---|---|---|---|---|
| data | 917 | | 97 | 37 / 317 / 266 = 620 | 167 / 29 / 4 |
| ctrl | 2218 | | 120 | 47 / 674 / 1006 = 1727 | 337 / 30 / 4 |
| full | 2469 | 253 | 126 | | |

- "Non-write" means the havoc table had no row for the step: guards, calls and returns of non-concept algorithms.
- Of the 173 havoc rows that the model reads (modeled, unmodeled, input, composite, unmodeled-guard), the data slice holds 134, ctrl 165 and full 172. The one row that full misses is CORP check step 2, which reads a criterion and does not write one.
- **The relation saturates.**
  - The ctrl slice from each concept alone has 2217 or 2218 steps, for all 13 concepts.
  - Data-only slices split into two groups:
    - small: corp, creds, mode, tainting, secure and coicap each have 5 to 7 steps (their values are constants chosen by guards); bcgswitch has 11 and coop 20;
    - large: origin, response, akey, coimode and coep have about 880 each, all through the URL list and the response.
  - Being in the slice says little about how near a step is. Distance from the criteria (ctrl, in edges) helps: there are 572 unmodeled steps at distance 2 or less, and 1155 further away.
- Unmodeled steps at distance 2 or less, by group (author's buckets by algorithm name):

| group | steps |
|---|---|
| navigation and history | 148 |
| redirect and network | 132 |
| document and browsing-context creation | 90 |
| URL and parsing | 65 |
| policy (COEP, COOP, sandbox, X-Frame-Options) | 57 |
| fetch core | 46 |
| script and events | 6 |
| other | 28 |

The algorithms with the most such steps: HTTP-network-or-cache fetch 42, navigate 37, create navigation params by fetching 31, scheme fetch 27, apply the history step 20, main fetch 20, HTTP-network fetch 19 and fetch 16.

## 3. Holes on relevant paths

| | ctrl | data |
|---|---|---|
| hole steps in the closure | 172 | 167 |
| ... on relevant paths | **144** | **93** |
| unbound relevant locals | 48 | 16 |
| entry parameters with no caller (HTML `append` and `set`) | 5 | 3 |
| slice steps that read external-spec results (boundary) | 401 | |

Kinds of hole on ctrl paths:

| kind | steps |
|---|---|
| collection op with an unresolved target | 35 |
| indirect call (processResponse and similar callbacks, `run V`) | 34 |
| prose-only | 28 |
| collection op with no target | 21 |
| other write verb (update, mark, store) | 12 |
| unresolved link | 8 |
| ambiguous local, untagged let, unresolved target, callback-bound | 6 |

- Only 12 hole steps sit at ctrl distance 2 or less. Examples: main fetch 23.2 and 23.3.1 (callbacks), apply the history step 12.8 and 12.8.7, evaluate a javascript: URL 15, download the hyperlink 9.
- The unbound locals come in three kinds:
  - parameters of prose-defined algorithms (same origin A and B, secure context's environment);
  - callback parameters that are bound outside the `steps given` form (create navigation params by fetching earlyResponse and fetchedResponse);
  - untagged loop bindings.
- Boundary targets: Infra 133, unresolved Bikeshed xref 99, W3C 59, ECMAScript 50, DOM 49, Web IDL 40, URL 35.

## 4. Positive controls

| step | data | ctrl | ctrl distance | how it is reached |
|---|---|---|---|---|
| obtain an embedder policy 2 | yes | yes | 0 | exit guard of the writer of embedder policy's value; `RET` flows into the policy container's embedder policy |
| HTTP-network-or-cache fetch 8.4 | yes (distance 14, via the response) | yes | 2 | includeCredentials, then response's request-includes-credentials (step 14), then the guard in CORP internal check 4 |

- Both controls pass. Neither is seeded by hand.
- In the per-concept data slices, 8.4 is missing from corp and creds. Their results are constants, so control dependence is needed to reach it.
- Each control is in all 13 per-concept ctrl slices. That shows saturation, not discrimination.

## 5. Against R1 to R3

- **R1 (closes): not supported.** Write targets are mostly determined by rule (94% of Let locals). But 144 hole steps and 48 unbound locals remain on relevant paths, so the list is not closed.
- **R2 (the flow breaks): supported, but not by natural-language conditions.** Conditions only feed control dependence, and reading their tokens is enough for that. The flow breaks where values are handed off:
  - callbacks (34 indirect calls plus the unbound callback parameters);
  - collection ops with no target or an untagged one (56);
  - prose-only steps (28);
  - 401 steps that rely on other specs being pure functions of their arguments.
- **R3 (many unmodeled relevant steps): supported, with a caveat.** The model transcribes 120 of the 2218 ctrl-slice steps; 1727 are unmodeled, 572 of them at distance 2 or less. Part of this count is an artifact: field-based, context-insensitive control slicing makes every concept reach the same 64% of the closure.

## 6. B2b and B2c

- **B2c (write targets determinable by rule): mostly met, not done.**
  - 837 of 954 (87.7%) previously undetermined targets are now determined.
  - Still undetermined: 45 Let locals (non-var targets), 48 collection ops (targets inside StructuredSerialize, parsers and the navigation API) and 24 unparsed rows.
- **B2b (the list of unmodeled property-relevant steps is closed): not met.** The candidate list exists (`closed-list.tsv`, 1727 ctrl steps), but it is open at 144 hole steps and 48 unbound locals (`holes.tsv`). Closing it needs three things:
  - a binding rule for callbacks stored in fetch params (processResponse and the other process* callbacks), and for callback parameters outside the `steps given` form;
  - targets for the remaining collection ops;
  - a decision on the 401 boundary steps (summaries for other specs, or declare them inputs).

  Even when it is closed, the list will not discriminate unless the analysis tells objects or contexts apart (for example, one cell per request and response object, or the model's own input cut).

## Limits

- The rules read prose by form, so a misread meaning is not measured. No sample audit of the defs was done beyond the controls and the 173 havoc rows.
- Parameters come from the vars in the preamble, which can include non-parameters.
- In the fallback mapping (87 sites), every argument goes to every parameter.
- Struct field defaults ("unless stated otherwise") are not steps, so they are not seen.
- The criteria, aliases and groups are the author's. W1 was not used.
