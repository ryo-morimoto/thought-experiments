# Finite domains: what the TLC checks say about unbounded origins, chains and depths

For the record [experiments/2026-11-24-finite-domain-adequacy.md](../../../2026-11-24-finite-domain-adequacy.md)
(tree node A2, hypotheses R1–R4). `../SpecIsolation.tla`, `../redirect/RedirectSeq.tla`, `../gen/GenModel.tla`
and `../gen2/Gen2Model.tla` are used unedited. A subagent ran this on 2026-11-24. Nothing is committed.
Run from `site-isolation/`: `sh adequacy/tlc.sh <cfg> <Module>` (cwd `adequacy/`), `python3 -I adequacy/types.py`.

## 1. What the model does with origin values (code reading)

| Operation | Where | Data-independent? |
| --- | --- | --- |
| `x = y` (SameOrigin, record equality) | everywhere | yes (equality) |
| `.site = .site` (SameSite) | CORP same-site, HasOptIn, `nocors-site-basic` | yes, given an equivalence relation "same site" |
| `.scheme = "https"` (Secure) | SecureCtx, ParsedCOOP, Mixed Content, CORP scheme step | yes, a unary predicate with 2 values |
| `ctx.top # ctx.self` | SecureCtx | yes (equality) |
| `HttpsTwin(o)` = `[o EXCEPT !.scheme = "https"]` | Mixed Content upgrade (`<img>` only; `fetch()` never upgrades unless `true:mc-upgrade`) | a function on data: needs the "same host" relation and a domain closed under it. Origins, AllOrigins, D12, D18 are closed. |
| `Key(o, kind)` returns `o.host` or `o.site` | `oac-separate` WPT case, Gen2 `ODD` | **no.** It compares strings of two sorts: an apex host equals its site's name, so `Key(OA,"origin") = Key(OAwww,"site")`. It also drops the scheme: `Key(OAhttp,k) = Key(OA,k)`. The spec's keys are a site tuple or an origin tuple, which are never equal and carry the scheme. Gen2 `ODD` compares only two site keys of same-scheme origins, so the defect is not reached there. |
| Gen2 `Opaque` | sandbox | **no.** One constant, so two opaque origins are equal; the spec makes each fresh. Each Gen2 scenario has one, so it is not reached. |
| `CHOOSE` | `*Witness` only | does not affect truth values |
| Constants `OA`, `OAwww`, `OB` | WPT cases, RedirectSeq `Org`, GenModel `tgt` | yes, constants (they add to the needed size) |

Not modelled: ports (another equality, harmless), the registrable-domain computation (the site is a given
field), IP hosts, `document.domain`, `file:`/`data:`/`blob:`. Verdict: apart from `Key` and `Opaque` the model
is data-independent over (origins; =, same-site, same-host, Secure, HttpsTwin).

## 2. Relational types and coverage (`types.py`)

The coarse type of a k-tuple is each element's scheme plus, for each pair, SameOrigin and SameSite. The fine
type adds same host. Possible types are those of a k-sites × k-hosts × 2-schemes domain.

| Domain | k=2 coarse | k=2 fine | k=3 coarse | k=3 fine |
| --- | --- | --- | --- | --- |
| `Origins` (4) | 8/10 | 10/12 | 32/66 | 47/96 |
| `AllOrigins` (7) | 10/10 | 12/12 | 57/66 | 87/96 |
| `D12` (3 sites: 3+2+1 hosts, ×2 schemes) | 10/10 | 12/12 | 66/66 | 96/96 |
| `D18` (3 sites × 3 hosts × 2 schemes) | 10/10 | 12/12 | 66/66 | 96/96 |

- Missing from `Origins`: two distinct http origins, same-site or cross-site. Missing from `AllOrigins`: the 9
  triple types with three mutually cross-site origins.
- k per property: 2 for `OptInOnlySecure`, `COIOnlyWithOptInTop`, `NoUndeclaredLeak`, `BodyOnlyByOptIn`,
  `OptInOnlyPC` (it never reads `ctx.top`) and every Signature operator. 3 for `OptInOnlySecureCtx`/`Lifted`
  (self, top, response) and `COIOnlyWithOptInNested` (top, child, child's target). All of them were checked
  over `Origins`.
- Generated spaces: gen (top, l1, l2) realizes 52/66 triple types, because "cross-site" is always the other of
  two sites. The redirect space realizes 9/66 for (A, hop, final). Each relation to A is one fixed https
  origin, so two cross-site hops are always equal and no hop is http.

## 3. Scale-up (SpecIsolation properties and mutants)

`ScaleTop.tla` extends SpecIsolation and overrides `Origins <- D18` in the cfg, leaving the property text
unchanged. `MutKill.tla` instantiates SpecIsolation per mutant and overrides `Origins <- [SpecIsolation] D18`.
That covers 116 mutants: 16 named, 1 flow, and neg/false/true of 33 decisions. `COIOnlyWithOptInNested` on
D18 is checked as `NestedSym`. Its body is the same, with the top origin restricted to the 2 orbit
representatives under the site/host permutations of D18. On `Origins` with all 4 origins as representatives,
`NestedSym`'s kill set equals the original property's.

| Check | Origins (4) / AllOrigins (7) | D18 | Changed? |
| --- | --- | --- | --- |
| 9 properties, unmutated (`top-base.cfg`, `top-D18.cfg`) | `OptInOnlySecure`, `…Ctx`, `…PC`, `COIOnlyWithOptInTop`/`Nested`, `NoUndeclaredLeak`, `BodyOnlyByOptIn` TRUE; `…Lifted`, `NoHeaderLeak`, `OptInOnly` FALSE | same | no |
| Kill table: which of 7 properties each of 116 mutants breaks (`mut-base.cfg`, `mut-D18.cfg`) | 33 mutants break one or more | same 33, same property sets | no |
| Signature-equivalent to "none" (Signature on AllOrigins vs on D18) | 19 | same 19 | no |
| Signature classes over the 116 | 66 | same 66 classes | no |

`compare.py` checks the equalities. The D18 run took 43 min.

## 4. Depth saturation

**Redirect chains (`RedirectSat.tla`).** The key after n hops is (unmutated enforcement result, mutant's
result). It also keeps the first hop, but only for `first-hop-only`. Layer n+1 is the image of layer n under
one hop, so equal consecutive layers are a fixpoint. Observations come from `RedirectSeq!Vec` run on a witness
chain. A brute force over every chain of length ≤ 2 gives the same observation set (`bf-agrees`).

| Encoding of hop/final origins | keys after n = 0..5 hops (unmutated) | observations (op, st, final, Vec) | P1–P4 over ≤ 2 hops |
| --- | --- | --- | --- |
| RedirectSeq's 3 (O, S, X; all https) | 8, 96, 111, 111, 111, 111 | 144, 170, 170, 170, 170, 170 | (RedirectEnum) only P2c fails |
| 7: + www2.A, c.test, http A, http B | 8, 176, 203, 203, 203, 203 | 336, 410, 410, 410, 410, 410 | only P2c fails |

- Unmutated: observations of exactly n hops are the same for all n ≥ 1, and states are fixed from n = 2.
- 65 mutants (RedirectSeq's AllMutants), n ≤ 5. Joint keys reach the fixpoint at n = 2 or 3. Every mutant
  that is ever distinguishable is distinguishable at n ≤ 1: 18 at n = 0 and 6 at n = 1 (first-hop-only,
  final-hop-only, neg:hop-accumulate, neg:hop-update, neg:hop-coep, neg:hop-same-entry). The other 41 are
  never distinguishable.
- With 7 origins, `coi-ignore-secure` becomes distinguishable at n = 0 (an http final response), a scheme
  type the all-https encoding lacks. No other row changes.
- `neg:hop-same-entry` puts n into history.length, so its observations never saturate, but its kill does
  (n = 1). The state saturates because each hop folds into (sticky flag, last origin, last COOP).

**Nesting (`NestSat.tla`).** `LevelStep` is GenModel's per-level step (ChildCtx, NavChild, EffectiveCOEPCtx,
PP), written once for any depth. The key is (ctx, policy-container COEP, COEP header, loaded, nav, PP). Its
rows (load, coi, sec, fetch to every target × credentials) agree with `GenModel!Allowed` for depth 0 and 1 on
every scenario (`agree-gen`). Domain: AllOrigins; tops {https A, http A} × COOP {un, so} × COEP 3; children
AllOrigins × CORP {none, so, xo} × COEP 3. Depth 2 was not cross-checked.

- Unmutated, number of nested levels n = 0..4: keys 12, 276, 538, 670, 670. Distinct (top, rows): 12, 96,
  112, 118, 118. **Cutoff n = 3** for keys and rows: a fourth nested level adds nothing. The 6 rows that
  first appear at n = 3 (`PrintNew`) are all "unreached" rows: an ancestor was not loaded, so every value
  is allowed. They occur under an http top (2 COOPs × 3 COEPs). So every row that constrains an observation,
  at any depth, already occurs at some depth ≤ 2, which is where GenModel stops.
- 55 mutants (GenModel's set): every distinguishable mutant is distinguishable at n ≤ 1 (25 at n = 0, 8 at
  n = 1). The other 22 never are. Their joint keys are at a fixpoint from n = 3 (Keys(3) = Keys(4)), so
  "never" is exact. The joint key of `false:nav-coep-adherence` was still growing at n = 4, but that mutant
  is already distinguished at n = 1.
- Why: a level passes down only (top, parent origin, policy-container COEP, loaded, PP). Nothing reads the
  ancestor chain; Mixed Content and SecureCtx read only `ctx.top`.
- Gen2's sandbox is one level deep. No model has sandbox inheritance or per-level fresh opaque origins, so no
  cutoff can be computed for them. Inheritance by union of flags would be a monotone fold.

## 5. The claim and its conditions

**Origins** (my argument; it is the elementary fact underneath data independence). Let 𝔘 have infinitely
many sites, infinitely many hosts per site and 2 schemes, with =, same-site, same-host, Secure and HttpsTwin.
Each §3 property is ∀ k origins and finite-enum values of a formula built from §1's operators without `Key`,
so its value on a tuple depends only on the tuple's fine type. Hence: *if D ⊆ 𝔘 is closed under HttpsTwin
and realizes every fine k-type, the property holds over D iff it holds over 𝔘, and two mutants agree over D
iff they agree over 𝔘.* D18 meets this for k ≤ 3 and AllOrigins for k = 2, so with §3 the verdicts, kill
table and Signature classes hold for unboundedly many origins. `Origins` (4) meets it for no k, so the
earlier checks were right but unjustified. Conditions: (a) no `Key` or `Opaque` in the property (Gen2 `ODD`
and WPT `oac-separate` are not covered); (b) the model's structure: sites are given, not computed from a
public suffix list, there are no ports, and opaque origins are not fresh; (c) it does not transfer to the
generated spaces, which lack types (§2). The redirect run with 7 origins shows (c): `coi-ignore-secure` is
invisible to the all-https space.

**Depths.** Both are folds into finite state with a measured fixpoint. For redirects the state is fixed from
n = 2 and the observations from n = 1. For nesting it is n = 3, and n ≤ 2 for constraining rows. Every
mutant ever killed is killed at n ≤ 1. So the 0..2 spaces are complete, for any length or depth, for the
model's own observations and mutants. This is the fixpoint of a finite image, not an Emerson–Kahlon cutoff.

**R1–R4.** R1 holds with conditions (a) and (b). D18 confirms it, but `Origins` (4) was too small to justify
it alone. R3 holds for what R1 leaves out: `Key` compares hosts with sites and drops the scheme, `Opaque`
is not fresh, the sites are given, and the generated spaces lack types. R2 holds for redirects and for
GenModel nesting. R4 is not shown for the modelled steps, since nothing reads the ancestor chain beyond
`top` and the parent. It stays open for sandbox inheritance and per-level opaque origins, which no model has.

Limits: everything here is about the model, not the spec or browsers. NestSat was cross-checked with GenModel
only at depth ≤ 1. P1–P4 with 7 origins were checked only for ≤ 2 hops. `NestedSym`'s symmetry rests on §1's
reading, though on `Origins` it gives the same kills.

## Theory (checked = bibliographic data or abstract seen on 2026-11-24; recalled = content from memory)

- Wolper, POPL 1986, 184–193 (doi 10.1145/512644.512661). Checked: the citation. Recalled: it introduces data
  independence (equality, input, output and assignment only) and the reduction to small data domains.
- Lazić & Nowak, "A unifying approach to data-independence", CONCUR 2000, LNCS 1877. Checked: the abstract
  (equality, extended to constant and predicate symbols). Roscoe & Lazić, "Data independence with predicate
  symbols", PDPTA'99. Checked: the citation only.
- Ip & Dill, "Better verification through symmetry", FMSD 9, 1996. Checked: the abstract (scalarsets).
  Momtahan, ENTCS 128, 2005 (small model theorem for data-independent Alloy types). Checked: the abstract.
- Emerson & Kahlon, CADE 2000 (cutoffs for parameterized guards). Checked: the abstract. It does not apply,
  since there are no replicated processes here.
- Bojańczyk, Klin & Lasota, "Automata theory in nominal sets", LMCS 10(3:4), 2014. Checked: the abstract
  (orbit-finiteness). Recalled: structures richer than equality (homogeneous ones) also work, which is §5's
  setting.
