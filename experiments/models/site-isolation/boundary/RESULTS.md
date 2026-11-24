# Closure boundary by rule, and the path inventory rebuilt from it: results

For [experiments/2026-11-24-closure-boundary-rule.md](../../../2026-11-24-closure-boundary-rule.md) (tree nodes B2a and B2d). Written by a subagent. One author made every judgement here. No spec text is committed. The tables hold only algorithm names, step numbers, definition ids, external anchors and the author's labels.

## Files and how to run

- `boundary.py` computes the closures and the path inventory. It writes `closure-rule.txt` (the rule and the measured numbers), `compare.tsv` (each node, with its membership and its role in the rule) and `paths.tsv`. Run it as `python3 -I boundary.py <extract out dir> <spec data dir> <out dir> [<scratch dir>]`. It reuses the link resolution of `../extract/analyze.py` and the write rules of `../havoc/writesets.py`.
- `review.py <paths.tsv> [<reference.tsv>] [<previous table>]` adds the `kept`, `category` and `key` columns, then prints precision and recall. The reference set and the 2026-11-22 table are kept outside the repository. The script prints only counts for them.
- Inputs: HTML 0e292f4 and Fetch d7fc0fd, parsed by `../extract/parse_spec.py`. See `../extract/commits.txt`.

## 1. The rule

The full text is in `closure-rule.txt`. In short:

- **Nodes.** The 1,995 algorithms, plus 347 unowned `<ol>` blocks named by their section. The earlier closure left these blocks out. Two of them are the setter steps of `document.domain` and `opener`.
- **Seeds S.** Every node with a step that writes a model-read concept. These come from the write rules of `writesets.py`, run blind on the whole corpus rather than on the hand closure. S' is the subset that writes a field or a collection.
- **Sinks K.** The getters `crossOriginIsolated` and `originAgentCluster`, the getter and setter of `document.domain` and of `opener`, and fetch response handover.
- **Stop rules.** Links to other specs are not followed. They are counted as exits: primitives (Infra, DOM, URL, WebIDL, Encoding, MIME Sniffing, Streams), or other-spec exits.
- **Rule T (chosen).**
  1. Walk back from K + S' through callers. The walk continues past a caller only if that caller is a seed or a fetch wrapper (a node named fetch or preload that reaches fetch).
  2. Add the argument producers of the callers that were included.
  3. Take the forward closure of S + K + producers.

| rule (whole-corpus seeds: 80 + 7 sinks) | nodes | share of 2,342 | hand closure inside | rule only | hand only |
|---|---|---|---|---|---|
| naive: forward closure of the full backward closure | 950 | 41% | 415 | 535 | 0 |
| cone: full backward + forward from seeds and producers | 829 | 35% | 415 | 414 | 0 |
| **T** | **610** | **26%** | **415** | **195** | **0** |
| T with the seeds of `havoc/writesets.tsv` (hand closure only, 46) | 533 | 23% | 415 | 118 | 0 |

The naive rule does not explode to the whole spec (41%), but it doubles the closure for no benefit. Most of what it adds are callees of callers that merely start a fetch or a navigation: element processing (img, source, iframe), directionality, and DOM and serialization helpers. T is the tighter, justified rule. A caller that writes no model-read concept can affect a seed in only two ways:
- through its arguments, which step 2 covers;
- by deciding whether to call it, which the model already quantifies over.

Writes in callers are seeds by themselves, because seeding covers the whole corpus.

## 2. Comparison with the hand closure (415)

- **Hand only: 0.** Every rule contains the hand closure, so no hand root was needed beyond what the rule finds.
- **Rule only: 195** (`compare.tsv`, column `rule_role`):
  - **36 seeds** that the blind write rules find outside the hand closure: Fetch API constructors (Request, Response, redirect), link-type and preload blocks, and preconnect. Some of these may be false matches of the `origin` and `response` concept patterns; they were not reviewed one by one.
  - **4 sinks** that the hand roots missed: the `originAgentCluster` getter, the `opener` getter, and both setter blocks.
  - **58 callers**: fetch call sites (images, media, text tracks, embed and object, scripts, workers, worklets, EventSource, deferred fetch) and navigation initiators (`window.open`, Location, following hyperlinks, form submission).
  - **25 argument producers** and **72 callees** of those.
- **Robustness.** Leaving out one seed loses at most 34 nodes (median 0). Three seeds each carry more than 10. The boundary depends on the stopping choice: letting the walk go one more caller up (44 callers) and adding their producers would add 170 nodes. The boundary is therefore set by the rule's parameters, not by the spec alone.
- **Parameters that are still the author's.** The concept patterns in `writesets.py`, the sink list, the wrapper name pattern, and the stop-at-non-seed choice.

## 3. Exits to other specs (R3)

- From T, 707 external call links: 452 to primitives and 255 to other specs.
- Of the other-spec links, 136 are Bikeshed cross-references whose target spec cannot be resolved offline. Service Worker handle fetch is among them.
- The rest go to W3C specs (79: CSP, timing, WebDriver BiDi, File API, Permissions Policy, ...), CSS (16), ECMAScript (11), WICG (4: prefetch), Storage (3), HTTP (2), URLPattern (2) and WebAssembly (1).
- T also has 4 steps that defer to other specifications.
- Calls into HTML or Fetch from other specs cannot be seen at all, because the corpus holds only these two specs.

## 4. Path inventory rebuilt from T (`paths.tsv`)

The rules, restricted to the steps of nodes in T:

- **R1a / R1b.** A step links to fetch, or to a fetch wrapper.
- **R1c (re-entry).** Inside the fetch-internal cycle, a step calls main fetch or its own algorithm.
- **R2d (container).** A step links to a structure found from definitions, not from step keywords. Such a structure is a definition whose own clause gives a result type (response, script, module script, Document, image) or says it *is a* structure already found, together with an untyped map defined next to a struct that holds a response. A step also counts when it uses that structure through a variable: a `Let`/`Set` alias, a camel-case variable named after the structure, or an algorithm returning "the unique ... cache". **R2v** marks the steps that use a value taken from such a structure.
- **R2f (field).** A step links to a field whose clause types it as a response, Document or module script.
- **X (exit).** A step calls another spec.

| group | rows | kept | precision |
|---|---|---|---|
| fetch calls (R1a/R1b) | 51 | 49 | 96% |
| re-entry (R1c) | 5 | 5 | 100% |
| container sites (R2d, R2v) | 55 | 39 | 71% |
| field sites (R2f) | 104 | 41 | 39% |
| reuse total (R2d + R2f) | 159 | 80 | 50% |
| other-spec exits (X, R2x) | 121 | 5 | 4% |

- **Structures.** Discovery found 20 candidates: 11 containers, 7 fields and 2 algorithms that return a cache. 8 of them are result stores: preload map, preloaded response candidate, early hints, image list, module maps, worklet module responses, HTTP cache, and bfcache documents. The other 12 are flow fields or stores of other things: worker owners, origins, area maps.
- **Reuse precision.** It rose from 8.6% (keyword rules on the whole corpus) to 50%. For named containers it is 71%.
- **The 2 dropped fetch-call rows** link to fetch from abort or cancel steps.
- **The kept exits** are the Service Worker response, prefetch records and blob URL objects. Most exits are timing or WebDriver hooks.

**Recall.** The reference is the 9 hand-chosen paths of the 2026-11-21 experiment. Its list is kept outside the repository, and the matchers used here reconstruct it from the public parts of the two records. 8 of the 9 are in the corpus.

| measure | found |
|---|---|
| reference paths in the corpus | 7 / 8 |
| reference path outside the corpus (found as an exit row at its use sites) | 1 / 1 |
| 2026-11-22 kept fetch call sites | 48 / 48 |
| 2026-11-22 kept reuse rows, strictly fetch-skipping (51, minus 7 decoded copies, minus 3 re-entries) | 31 / 41 (76%) |
| 2026-11-22 re-entry rows | 3 / 3 |
| 2026-11-22 hand-only rows (found only by hand then) | 5 / 6 |

The 2026-11-22 hand-only rows came in through three new mechanisms:
- variable subscripts on a module map and on the worklet module responses map, through the camel-case name rule;
- the Service Worker response, through the external call whose result is bound to a response variable;
- prefetch records, as exits at their use sites.

The one in-corpus reference path that is still not found is written as a prose paragraph about what user agents may do, not as steps.

## 5. What the rules still cannot find

- **Prose permissions.** "User agents may ..." paragraphs are not steps, so no step rule sees them (1 reference path).
- **Continuation steps that name neither the structure nor a variable bound from it** (10 of the 41 strict rows in section 4):
  - image list: 1 ("that entry");
  - early hints: 2 (the 103 handling inside HTTP-network fetch, and its commit in navigation);
  - bfcache: 3, phrased through the session history entry's `document` (a different definition from the document state's) or through prose decisions;
  - preloaded response candidate: 1, a call to the consuming algorithm rather than a link to the store;
  - HTTP cache: 3 cache-mode branches of HTTP-network-or-cache fetch.
- **Decoded copies.** Copies into ImageBitmap and canvas are outside T, and outside the strict definition of reuse.
- **Paths inside other specs.** Service Workers, Prefetch, File API, ECMAScript module loading, the HTTP cache selection itself, and extension rewrites. They show up only as exit rows, and Bikeshed exits without a resolvable spec cannot be classified.
- **Unowned blocks.** They are named by their section, so `compare.tsv` cannot tell them apart beyond their anchor.
- **Single rater.** The `kept` judgements are by structure plus a small per-row table, with no agreement measure.

## 6. Verdict on the record's hypotheses

- **R1 (the rule closure contains the hand closure, and the differences can be explained): holds.** Under all three rules the hand closure is inside the rule closure, with 0 hand-only nodes. The 195 rule-only nodes are seeds outside the hand closure, sinks, fetch callers, and their producers and callees.
- **R2 (the closure becomes nearly the whole spec): rejected for these rules.** The naive closure is 41% of nodes and T is 26%. The size does depend on the stop rule: going one more caller up adds 170 nodes.
- **R3 (insertions from other specs stay outside the boundary): holds alongside R1.** 255 other-spec exit links leave T, 136 of them to specs that cannot be resolved offline. Calls into HTML and Fetch from other specs are invisible.

**B2a (boundary decided by rule, not by hand): met for the roots.** The closure is derived from the write rules and the sinks, with no hand-picked roots. It contains the old closure, and the differences are explained. The parameters listed in section 2 are still the author's.

**B2d (inventory built mechanically, with measured recall): met.**
- Fetch calls: 96% precision.
- Reuse: 50% precision overall, 71% for containers.
- Recall: 7/8 of the in-corpus reference paths, 48/48 of the earlier call sites, and 76% of the earlier strict reuse rows.
- What the rules cannot find is listed in section 5.
