# Assume-guarantee contracts between the fragments, and their cycles

For [experiments/2026-11-24-cross-fragment-assume-guarantee.md](../../../2026-11-24-cross-fragment-assume-guarantee.md)
(tree node D2, hypotheses R1–R3). `../SpecIsolation.tla`, `../DIPExtension.tla` and `../redirect/RedirectSeq.tla`
are used unedited (Gen/Gen2's permissions-policy step is restated in `Contracts.tla`). A subagent ran this on
2026-11-24. Nothing is committed. Run from `site-isolation/`: `sh compose/tlc.sh <cfg> <Module>`.

## 1. Fragments and contracts

`contracts.tsv` has one row per fragment: what it assumes, what it guarantees, who uses the guarantee. In
`Contracts.tla` each guarantee is a predicate on a committed document `d` of a group with COI mode `g`:

| Guarantee | Fragment | Predicate |
| --- | --- | --- |
| `G_PC` | policy container COEP | not a secure context ⇒ pc COEP = unsafe-none |
| `G_DIP` | DIP | DIP ≠ none ⇒ top-level and secure origin |
| `G_BCG` | COOP / group / popup switch | top-level member: parsed COOP = same-origin-plus-COEP ⇔ g concrete |
| `G_MEM` | COOP match (popups), COEP adherence (children) | g concrete ⇒ pc COEP ∈ {require-corp, credentialless} |
| `G_AC`, `G_CL`, `G_HIST` | agent cluster | cluster mode = (DIP ? concrete : g); mode ≠ none ⇒ origin-keyed; map entry consistent |
| `G_CAP` | crossOriginIsolated getter (PP 'self') | cap = cluster mode concrete ∧ PP |
| `G_FETCH` | fetch, CORP, Mixed Content, DIP upgrade | (pc COEP compatible ∨ DIP) ∧ opaque ⇒ no credentials sent ∨ CORP opt-in |

Global property `Prop(d, s)`: a crossOriginIsolated document gets cross-origin no-cors bytes only without
credentials or with a CORP opt-in, and is origin-keyed. The state (`Compose.tla`): one browsing context group
(mode fixed at creation), its documents, agent clusters and historical key map. Steps: top-level commit (creates
the group), nested navigation of a child of any member, popup from a top-level member through 0..1 redirects.

## 2. The assumption graph and its cycles

Edges "X assumes Y" split by when Y was established (from the step definitions):

| Cycle | Kind | How it is handled |
| --- | --- | --- |
| C1 `F_NAV` ↔ `F_PC` | across steps: a child's navigation reads the parent's pc COEP (earlier commit); the child's pc COEP is then read when it is a parent. Within the step: `ChildCtx` → `SecureCtx` → child pc COEP → adherence check | a same-step cycle between *fragments*, but a DAG between *values*. Taken as one step; the across-step part is temporal induction |
| C2 `F_MEM` → itself | via the parent (nesting) or the opener (popups), always an earlier commit | temporal induction (`StepChild`, `StepPopup`) |
| C3 `F_BCG` → itself | over redirect hops (`RedirectSeq` `Chain`, RECURSIVE on `Tail(rs)`) and over openers | induction on hop index inside the step (well-founded recursion); across openers by temporal induction |
| C4 `F_AC` → itself | the historical map and existing clusters, written by earlier commits | temporal induction (`G_CL`, `G_HIST` in the pre-state) |
| C5 `F_FETCH` → `F_AC` → `F_DIP` | the capability comes from the cluster, the CORP upgrade from the document's own DIP | holds only if the cluster key carries the DIP: a gap (section 4), not a cycle problem |

The cycle named in the record ("COEP semantics assumes agent-cluster keying") is not in the model or, as far as
the steps read, in the spec: keying reads the COI mode, which reads COOP and COEP; COEP's semantics never read
the key. The only edge from keying back into fetch is C5, through DIP.

No same-time cycle between values: SANY rejects circular definitions that are not RECURSIVE, and the only
RECURSIVE operator reached is `Chain`, which recurses on a shorter sequence. So every same-step dependency is
acyclic, and every cycle passes through an earlier step (C1–C4). R2 holds only at fragment granularity (C1).

## 3. Rule and TLC results

Rule (McMillan-style circular AG for safety, as temporal induction): (a) the first commit establishes every
guarantee; (b) from *any* pre-state element satisfying all guarantees (not only reachable ones), each step
establishes every guarantee on what it adds, using the others' guarantees only at earlier steps; existing
elements and g never change (append-only frame, by construction); (c) the guarantees imply `Prop`. Then □G and
□Prop. A step reads one earlier document, g, one map entry and one cluster, so one pre-document suffices.
Theory: McMillan, "A compositional rule for hardware design refinement" (CAV 1997) and "Circular compositional
reasoning about liveness" (CHARME 1999), checked only through their abstracts and Rushby's PVS check of the rule
(https://www.csl.sri.com/~rushby/papers/mcmillan.pdf; https://link.springer.com/doi/10.1007/3-540-48153-2_30).
Abadi–Lamport "Conjoining specifications" (TOPLAS 1995; the −▷ operator) and Namjoshi–Trefler (CAV 2000,
completeness of circular rules): recalled, not checked. The check here is (b) as a TLC quantifier over all
pre-states, which is the "consecution" obligation of those rules.

`Contracts.tla` (constant level, TLC 1.8.0, cfgs in this directory):

| cfg | top (a) | child (b) | popup (b) | `CapPrem` (c) | `G ⇒ Prop` (c) | time |
| --- | --- | --- | --- | --- | --- | --- |
| `Steps-none` (key with DIP) | TRUE | TRUE | TRUE | TRUE | TRUE | 1m31 |
| `Steps-nodipkey` | TRUE | **FALSE** (`G_AC`) | **FALSE** | TRUE | TRUE | 2m42 |
| `Steps-mut-adherence` (`false:nav-coep-adherence`) | TRUE | **FALSE** (`G_MEM`) | TRUE | TRUE | TRUE | 4m28 |

`G_FETCH` alone over all 18 432 document records is FALSE (`Fetch.cfg`): an `http:` child under an `https:` top
with a DIP field is a secure context by `SecureCtx` but `EffectiveDIP` drops the DIP by `Secure(origin)`. With
`G_DIP` assumed it is TRUE. So `F_FETCH` assumes `F_DIP`'s guarantee, and the two fragments read "secure"
differently (section 4).

`Steps-drops` (23m18): each guarantee is dropped from the pre-state assumption in turn. Every one is
needed by some obligation, so no contract is vacuous:

| dropped | child | popup | `CapPrem` | `G ⇒ Prop` | which cycle needs it |
| --- | --- | --- | --- | --- | --- |
| none | TRUE | TRUE | TRUE | TRUE | |
| `G_PC` | TRUE | TRUE | TRUE | FALSE | fetch reads pc COEP (C1, at fetch time) |
| `G_DIP` | TRUE | TRUE | TRUE | FALSE | fetch's DIP reading |
| `G_BCG` | TRUE | FALSE | TRUE | TRUE | C3 (opener) |
| `G_MEM` | FALSE | TRUE | FALSE | FALSE | C2 (parent) |
| `G_AC` | TRUE | TRUE | FALSE | FALSE | C5 |
| `G_CAP` | TRUE | TRUE | FALSE | FALSE | getter |
| `G_CL` | FALSE | FALSE | TRUE | TRUE | C4 (cluster joined) |
| `G_HIST` | FALSE | FALSE | TRUE | TRUE | C4 (historical map) |

`Compose.tla` (monolithic, reachable states, no induction): invariants `PropInv`, `GInv`, `KeyConsistent`.

| cfg | result |
| --- | --- |
| `Compose-2` (2 documents) | no error; 2 489 distinct states |
| `Compose-3` (3 documents) | no error; 66 684 distinct states, 8m22 |
| `Compose-nodipkey` | `PropInv` violated at depth 2: top `https://a.test` with DIP isolate-and-require-corp and COOP unsafe-none (g none); same-origin child with no COEP joins the top's cluster (key without DIP), gets cap TRUE with pc COEP unsafe-none |
| `Compose-mut-adherence` | `PropInv` violated at depth 2: COI top, same-origin child with COEP unsafe-none loads, cap TRUE |

The stepwise check and the monolithic check agree on every cfg, and the stepwise one names the broken contract.

## 4. Premises no fragment guarantees (gaps)

1. **The agent cluster key and DIP.** `F_FETCH` under DIP assumes the document's cluster was created with its own
   DIP. `SpecIsolation`'s key (`KeyKindCtx`, `Key`) has no DIP part, and `DIPExtension` has no agent clusters.
   Without the DIP in the key, both checks fail (above). That the DIP draft's key carries the isolation
   (its "cross-origin isolation key") is recalled from the `DIPExtension` header, not re-read.
2. **"Secure" in DIP.** `EffectiveDIP` uses `Secure(origin)`; the policy container uses `SecureCtx` (top-level
   creation URL). Latent while DIP is top-level only; any nested DIP must choose.
3. **DIP is top-level only**, and nested documents of a DIP document get no adherence check: `NavChild` reads the
   parent's COEP, not its DIP. Not reached here because the key keeps a non-DIP child out of the DIP cluster.
4. **`DIPExtension` `Conservative` is FALSE** since the Mixed Content fix (`FetchResultD` has no Mixed Content).
   Already in `fixes/FIXES.md`; confirmed with `DIP.cfg`. `F_DIP`'s contract was written against the old fetch.
5. **Local-scheme and inherited documents** (about:blank, srcdoc, workers): `G_MEM` for them needs policy
   container inheritance, which no fragment models. Popups opened by nested documents are not modelled.
6. **Permissions Policy** lives only in Gen/Gen2 (no allow attribute). By the derivation (not a separate TLC
   run), it is not load-bearing for `Prop`: `cap ⇒ cluster mode concrete` is enough for `CapPrem`, and `G_MEM`
   (COEP adherence) carries the rest. PP only narrows cap, so an allow attribute would not break `Prop`.
7. **Key equality**: `SpecIsolation`'s `Key` confuses an apex host with a site name (adequacy/RESULTS.md); clusters
   here use a tuple key instead.

## 5. Verdict

- R1 (the cycles break at time steps and the checks compose): **holds for the modelled fragments**, with the
  key carrying the DIP. C1–C4 all pass through an earlier step; the stepwise checks give the global property.
- R2 (same-time cycle): **only at fragment granularity** (C1, `F_NAV` ↔ `F_PC` inside one commit). At value
  granularity there is none; it is handled by taking the commit as the step, not by the circular rule.
- R3 (premises no fragment guarantees): **holds**: gap 1 is load-bearing (TLC counterexample); gaps 2–5 are
  latent or out of the modelled steps.
