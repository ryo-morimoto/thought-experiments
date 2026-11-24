# Dataflow round 2: callbacks, residual targets, contracts, sensitivity

Round 2 of [../RESULTS.md](../RESULTS.md), for [experiments/2026-11-24-write-target-semantics.md](../../../../2026-11-24-write-target-semantics.md) (tree nodes B2b, B2c). Written by a subagent. One author wrote the rules and the readings in `contracts.py`. Spec text is not committed.

## Files and how to run

- `dataflow2.py` is round 1's `dataflow.py` plus the changes below. `specscan2.py` adds the words before the dfn to an algorithm's preamble, so prose-defined parameters are found.
- `contracts.py` holds the stated contracts C1 to C7 and the author's reading of every residual item.
- Run: `python3 -I dataflow2.py <extract/out> <html.src> <fetch.bs> ../../havoc/writesets.tsv <outdir>`. It takes about 2 minutes. `DF_FAST=1` skips the per-concept runs with object sensitivity.
- Outputs:
  - `closed-list.tsv`, `flows.tsv`, `holes.tsv`: the round 1 tables, recomputed.
  - `holes2.tsv`: every hole on a relevant path, with its contract, whether it writes a value, whether it may write a model-read concept, and why.
  - `residual-targets.tsv`: havoc gap rows that no rule places, each with its contract.
  - `inputs.tsv`: the calls to other specs, as a stated input contract.
  - `summary.json`: all counts.

## 1. Callback binding

- **Registration.** A callback is named by what it is assigned to: `let X be (an algorithm that runs) the following steps|algorithm|substeps given …`, `NAME set to the following steps given …`, `let X given … be`, or `return the following substeps given …`. Its parameters are the vars after `given`. A registered callback var that is passed as an argument is also registered under the callee parameter's name.
- **Indirect calls.** `run|call|invoke|perform X` or `x's F`, with the argument chunks after `given|with|on`. They bind by the callback's normalized name, and positionally to its parameters. When the callee is a parameter, they also bind to the registrations at the call sites of its algorithm.
- **Result.** There are 77 indirect calls in the closure:

| status | calls |
|---|---|
| bound | 19 |
| no value arguments | 17 |
| bound, callback has no parameters | 1 |
| per-type hooks (contract C4) | 15 |
| WebDriver BiDi hooks (contract C3) | 25 |
| **unbound** | **0** |

- Indirect-call holes on relevant paths went from 34 to 0. The preloaded-response flow (fetch 11.2 to consume a preloaded resource 8) is now bound by rule.
- Four callbacks are still not bound by rule: process early hint headers 5, Speculation-Rules 3.4.2.2, fully read 2, HTTP fetch 3.2.2. Each was read; none writes a model-read concept.
- Unbound relevant locals went from 48 to 10: prose lambdas, an existential binding, named arguments of RFC 9651, and the network body. All 10 are under C6 or C7 and were read.

## 2. Residual write targets (B2c)

New rules:
- flag sets (`set x's F`), Infra map sets (`set (k, v) in m`), `set \`Name\` to v in list`;
- `let V have|point`, `change|initialize X to`, `mark X as Y`, `update|increase|decrease|multiply X`;
- `otherwise, let it be`, `set A and B to`;
- verbs used as quoted values (`"push"`) or as infinitives are not writes;
- `empty` used as an adjective is not a write;
- collection targets after `on`, `in`, `the user agent's`, and `the start and end of`;
- a gap row that calls a parsed algorithm is resolved through that callee;
- for each with type words, tuples and `k → v` pairs.

| havoc gap kind | rows | round 1 | round 2 |
|---|---|---|---|
| Let local | 746 | 701 | **746 (100%)** |
| collection op | 152 | 104 | 141 |
| unparsed | 56 | 32 | 47 |
| total | 954 | 837 (87.7%) | **934 (97.9%)** |

The 20 residual rows are listed in `residual-targets.tsv`. Every one falls under a stated contract:
- C1 (10): URL username and password setters 6, Streams set-up 3, Fetch Metadata headers 1;
- C5 (9): JS execution context stack and event loop 6, queued tasks whose steps are analysed in place 2, DOM tree 1;
- C6 (1): HTTP cache store.

## 3. Other-spec calls as inputs (contract C1)

Of the round 1 "boundary" references, 414 are terms: types, predicates and constants such as list, exists, map, record or DataCloneError. They are not calls.

What remains is 73 distinct call-like external algorithms on 103 slice steps (`inputs.tsv`):

| contract | algorithms | meaning |
|---|---|---|
| C1 | 60 | pure functions of their arguments; Infra's "collect a sequence of code points" also advances the caller's position variable, a parser local |
| C2 | 5 | DOM event creation and firing, Web IDL invoke and wait-for-all: these run script |
| C3 | 6 | WebDriver BiDi hooks |
| C6 | 2 | HTTP semantics |

- **Checking the top 20.** Three were checked against url.bs offline: URL parsing, URL parser and URL serializer. No closure step passes a state override, and without one the parser returns a new URL. The other 17 are from memory (Infra, DOM, Web IDL, CSP, Secure Contexts, Permissions Policy, HR Time, BiDi).
- **Model-read concepts.** None of these calls writes one, with two exceptions:
  - BiDi network interception can rewrite a request and supply a response. Contract C3 excludes it.
  - Event firing and callbacks act only through script. Contract C2 covers that.

## 4. Prose-only steps

- The arithmetic rule resolves the counters (redirect count, unload counter, nesting level, divisor). That leaves 19 prose-only steps on control paths.
- 6 steps write no value: two editorial notes, a label, a rethrow, a readiness statement, and "scripts may run" (C2).
- 13 steps write a value, but none writes a model-read concept: focus and scroll state, CSS, the filename, parser positions, a proxy-authentication entry, a deserialized attachment, user-agent page content, and multipart. For multipart, html.src was checked: the part documents reuse the copied navigation params or go back through navigate.

## 5. Discrimination: object and context sensitivity

- **1-call-site context.** Each local or `RET` state carries the call site through which its algorithm was entered. Going back from a parameter visits only that call site.
- **Allocation-site heap.** Points-to is Andersen style and context-insensitive. A site is any step with `new`, `copy`, `clone` or `whose`, which gives 300 sites. A heap cell is (site, field). `ANY` stands for an object the rules cannot place and aliases every site; 3322 of the 5466 pointer variables include it.
- Closure steps, of 3445:

| slice | data | data+control |
|---|---|---|
| round 2, field-based | 1007 | 2375 |
| + 1-call-site context | 971 | 2276 |
| + allocation sites | 978 | 2276 |

- Per concept, the data+control slice with objects and context has 2275 or 2276 steps for all 13 concepts. **It still saturates.**
- Per concept, the data-only slice with objects and context has 5 to 20 steps for corp, creds, mode, tainting, secure, coicap, bcgswitch and coop, and 924 to 941 for coep, origin, response, coimode and akey.
- **Why it still saturates.** The `request` of main fetch, HTTP fetch and fetch points to 97 allocation sites, which is every request in the two specs. So the guards in the shared fetch pipeline read every request's fields, and every writer of those fields becomes relevant. A deeper call-string context would be needed (navigate to create navigation params to fetch to main fetch is at least 4 calls), or a cut at the inputs the model quantifies.
- **Positive controls.** Both are in every slice and in all 13 per-concept data+control slices. obtain an embedder policy 2 is at distance 0, and HTTP-network-or-cache fetch 8.4 at distance 2.

## 6. Answers

- **B2c: done, under contracts.**
  - 934 of 954 havoc gap rows (97.9%) are now determined by rule.
  - The 20 left are each explained by a stated contract: C1 10, C5 9, C6 1. None is unexplained.
  - The hole kinds that came from targets the rules could not place are now 0 on relevant paths, apart from items that were read one by one.
- **B2b: closed under C1 to C7. The list does not discriminate.**
  - After the contracts, 38 hole steps, 10 unbound locals and 5 entry parameters remain on relevant paths, and all were read. None is left at "may write a model-read concept: ?". One ("scripts may run") depends on C2.
  - The unmodeled property-relevant list (data+control) has **1864** steps: 721 havoc gap, 1096 non-write, 47 known. The data-only list has 696.

| group | data+control | data only |
|---|---|---|
| URL and parsing | 558 | 223 |
| navigation and history | 464 | 145 |
| redirect and network | 273 | 114 |
| document and browsing-context creation | 176 | 89 |
| script and events | 100 | 10 |
| fetch core | 88 | 43 |
| policy | 75 | 14 |
| other | 130 | 58 |

  - 641 of the 1864 are at distance 2 or less.
- **Caveats.**
  - Closure rests on one author's reading of about 50 items and on contracts C1 to C7.
  - 17 of the top 20 inputs were recalled, not checked.
  - Per-concept relevance still saturates, so the list is a sound superset, not a ranking.
