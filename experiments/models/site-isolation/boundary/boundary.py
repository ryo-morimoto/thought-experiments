"""Rule-based closure boundary and path inventory (W6, nodes B2a and B2d).

For experiments/2026-11-24-closure-boundary-rule.md. Reads the parsed spec
JSON written by ../extract/parse_spec.py (not committed: spec text) and the
raw sources, and writes only labels and anchors.

    python3 -I boundary.py <extract_out_dir> <spec_data_dir> <outdir> [<scratch_dir>]

<extract_out_dir> holds html.json, fetch.json and closure_algorithms.tsv (the
hand-picked closure). <spec_data_dir> holds html.src and fetch.bs.
Writes <outdir>/closure-rule.txt (rule and measured sizes), compare.tsv and
paths.tsv (labels and anchors only; then run review.py on paths.tsv).
With <scratch_dir>, also writes step-level evidence (spec text) there.
"""
import collections
import contextlib
import csv
import importlib.util
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SI = os.path.dirname(HERE)
EXO, DATA, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SCRATCH = sys.argv[4] if len(sys.argv) > 4 else None

# ------------------------------------------------------------ load extract
code = open(os.path.join(SI, 'extract/analyze.py')).read()
code = code.split('# ---------------------------------------------------------------- roots')[0]
sys.argv = ['analyze.py', os.path.join(EXO, 'html.json'), os.path.join(EXO, 'fetch.json'), OUT]
g = {'__name__': 'analyze_prefix'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code, 'analyze_prefix', 'exec'), g)
algos, SPECS, resolve, norm, by_id = g['algos'], g['SPECS'], g['resolve'], g['norm'], g['by_id']
SRC = {'html': open(os.path.join(DATA, 'html.src'), encoding='utf-8').read().split('\n'),
       'fetch': open(os.path.join(DATA, 'fetch.bs'), encoding='utf-8').read().split('\n')}



def heading_before(spec, line):
    L = SRC[spec]
    for k in range(line - 1, -1, -1):
        m = re.search(r'<h[2-6][^>]*?(?:id="?([^" >]+))?[^>]*>(.*)', L[k])
        if m:
            return re.sub(r'<[^>]+>', '', m.group(2)).strip(), m.group(1) or ''
    return '?', ''


# unowned <ol> blocks (no defining dfn before them) become call-graph nodes named by their
# section, so that a step there that calls fetch is a caller like any other.
N_ALGOS = len(algos)
for spec, D in SPECS.items():
    for b in D['blocks']:
        if b['owner'] is not None or b['owner_attr']:
            continue
        h, hid = heading_before(spec, b['line'])
        intro = ' '.join(SRC[spec][max(0, b['line'] - 5):b['line']])
        mset = re.search(r'data-x="([^"]+)"[^>]*>[^<]*</code>\s*(setter|getter|method) steps', intro)
        nm = ('(%s steps of %s)' % (mset.group(2), mset.group(1)) if mset else '(unowned block in section: %s)' % h)
        A = {'spec': spec, 'dfn': None, 'name': nm, 'line': b['line'], 'steps_of': mset.group(1) if mset else None,
             'steps': b['steps'], 'prose': False, 'prose_links': [], 'anchor': '%s@%d' % (hid, b['line'])}
        A['cls'] = g['walk'](b['steps'], spec)
        A['calls'] = {tuple(c) for x in A['cls'] for c in x['local_calls']}
        algos[(spec, 'block@%d' % b['line'])] = A
N_BLOCKS = len(algos) - N_ALGOS

calls = {a: set(A['calls']) for a, A in algos.items()}
rev = collections.defaultdict(set)
for a, cs in calls.items():
    for b in cs:
        rev[b].add(a)


def name(a):
    return algos[a]['name']


def anchor(a):
    if isinstance(a[1], str):
        return algos[a]['anchor']
    d = SPECS[a[0]]['dfns'][a[1]]
    return d['attrs'].get('id') or d['attrs'].get('data-x') or d['text']


def aid(spec, ident):
    i = by_id[spec].get(ident)
    assert i is not None and (spec, i) in algos, ident
    return (spec, i)


# hand-picked closure (extract/closure-algorithms.txt; same 415 ids)
HAND = set()
for row in open(os.path.join(EXO, 'closure_algorithms.tsv'), encoding='utf-8'):
    sp, line, nm = row.split('\t')[:3]
    m = [a for a, A in algos.items() if a[0] == sp and A['line'] == int(line) and A['name'] == nm]
    assert len(m) == 1
    HAND.add(m[0])

# ------------------------------------------------------------ seeds
spec_ = importlib.util.spec_from_file_location('writesets', os.path.join(SI, 'havoc/writesets.py'))
W = importlib.util.module_from_spec(spec_)
spec_.loader.exec_module(W)
READ = W.READ
byname = collections.defaultdict(set)
for a, A in algos.items():
    byname[(a[0], A['name'])].add(a)

# S_ws: writers of model-read concepts listed in havoc/writesets.tsv (hand closure only)
S_ws = set()
for r in csv.DictReader(open(os.path.join(SI, 'havoc/writesets.tsv'), encoding='utf-8'), delimiter='\t'):
    if r['concept'] in READ:
        S_ws |= byname[(r['spec'], r['algorithm'])] & HAND

# S_all: the same write rules (writesets.py, --blind) applied to every algorithm of both specs
tmp_steps = os.path.join(SCRATCH or OUT, '_all_steps.tsv')
tmp_writes = os.path.join(SCRATCH or OUT, '_all_writes.tsv')
with open(tmp_steps, 'w', encoding='utf-8') as f:
    f.write('spec\talgorithm\talgo_line\tstep\tline\tclass\treason\tform\tmarkers\tin_slice\ttext\n')
    for a, A in algos.items():
        for s in A['cls']:
            f.write('\t'.join([a[0], A['name'], str(A['line']), s['path'], str(s['line']), s['class'],
                               s['reason'], str(s['form']), ','.join(s['markers']), 'False',
                               s['text'].replace('\t', ' ').replace('\n', ' ')]) + '\n')
with contextlib.redirect_stdout(io.StringIO()):
    W.main(tmp_steps, tmp_writes, blind=True)
S_all, STATE_all = set(), set()
for r in csv.DictReader(open(tmp_writes, encoding='utf-8'), delimiter='\t'):
    if r['concept'] in READ:
        S_all |= byname[(r['spec'], r['algorithm'])]
        if r['write_kind'].split('-')[-1] in ('field', 'collection'):
            STATE_all |= byname[(r['spec'], r['algorithm'])]
STATE_ws = set()
for r in csv.DictReader(open(os.path.join(SI, 'havoc/writesets.tsv'), encoding='utf-8'), delimiter='\t'):
    if r['concept'] in READ and r['write_kind'].split('-')[-1] in ('field', 'collection'):
        STATE_ws |= byname[(r['spec'], r['algorithm'])] & HAND
if not SCRATCH:
    os.remove(tmp_steps)
    os.remove(tmp_writes)

# observable sinks
K = set()
for a, A in algos.items():
    if a[0] == 'html' and isinstance(a[1], str) and A.get('steps_of') in ('dom-document-domain', 'dom-opener'):
        K.add(a)   # setter steps written as an unowned block after the attribute's getter
        continue
    if isinstance(a[1], str):
        continue
    d = SPECS[a[0]]['dfns'][a[1]]['attrs']
    if a[0] == 'html' and d.get('data-x') in ('dom-crossOriginIsolated', 'dom-originAgentCluster',
                                                'dom-document-domain', 'dom-opener'):
        K.add(a)
K.add(aid('fetch', 'fetch-finale'))  # fetch response handover: delivers the response to the caller
assert len(K) == 7, K
FETCH = aid('fetch', 'concept-fetch')
# fetch wrappers (rule R1b of the 2026-11-22 inventory): name contains fetch/preload and the
# algorithm reaches fetch. They hand the response or its parsed result to their caller.
WRAPPERS = {a for a in algos if a != FETCH and re.search(r'fetch|preload', norm(algos[a]['name']))}


RULE_TEXT = '''Closure boundary rule T (chosen), for HTML 0e292f4 and Fetch d7fc0fd.

Nodes: algorithms of HTML and Fetch (a defining dfn owns an ol or a prose
paragraph), plus unowned ol blocks named by their section. Edges: a step
links to another node (extract/analyze.py link resolution).

Stop rules: links to other specs (Infra, DOM, URL, WebIDL, Encoding,
MIME Sniffing, Streams = primitives; all others = other-spec exits) are not
followed. Every such link from a closure step is counted; other-spec exits are
listed in paths.tsv (kind exit-call).

S  (seeds): nodes with a step that writes a model-read concept, by the write
   rules of ../havoc/writesets.py run blind (--blind) on every node.
S' (state-writing seeds): seeds whose write is to a field or a collection
   (not a local or the return value).
K  (sinks): crossOriginIsolated getter, originAgentCluster getter,
   document.domain getter and setter steps, opener getter and setter steps
   (the setters are unowned blocks introduced as "setter steps"), fetch
   response handover.
W  (fetch wrappers): nodes whose name contains fetch or preload and that
   reach fetch (rule R1b of the 2026-11-22 inventory).

1. Backward: BT = callers of K and S', to fixpoint, but the walk continues
   past a caller only if that caller is in S or W.
2. Argument producers PT: in a caller in BT that is not a seed, a callee
   called in the same step as a BT member, or bound by Let/Set to a variable
   that such a step mentions.
3. T = BT + forward closure (callees, to fixpoint) of S + K + PT.

Why the backward walk stops: a caller that writes no model-read concept
reaches the seed only through its arguments (step 2) or by deciding whether
to call (the model quantifies over what pages do). Writes in any caller are
seeds by themselves, because seeding is whole-corpus.

Compared rules: naive = forward closure of the full backward closure of
S + K; cone = full backward closure + forward closure of S + K + producers.
[ws] rows use the seeds of ../havoc/writesets.tsv (hand closure only) instead
of the whole-corpus seeds [all].
'''

# ------------------------------------------------------------ closures
def back(starts):
    seen, st = set(), list(starts)
    while st:
        x = st.pop()
        if x not in seen:
            seen.add(x)
            st.extend(rev[x] - seen)
    return seen


def fwd(starts):
    seen, st = set(), list(starts)
    while st:
        x = st.pop()
        if x not in seen:
            seen.add(x)
            st.extend(calls[x] - seen)
    return seen


BIND = re.compile(r'\b(?:[Ll]et|[Ss]et) (\w+)(?: and \w+)? (?:be|to)\b')
WORD = re.compile(r'\b[A-Za-z_]\w*\b')
STOPW = {'this', 'the', 'a', 'an', 'it', 'up', 'result'}


def arg_producers(B, targets):
    """Callees of a caller in B whose result reaches a step that calls a target:
    either called in that step, or bound (Let/Set x ... the result of P) to a
    variable that the step mentions. Intra-algorithm, by variable name."""
    prod = collections.defaultdict(set)
    for a in B:
        A = algos[a]
        if A['prose']:
            continue
        bound = collections.defaultdict(set)
        for s in A['cls']:
            lc = set(map(tuple, s['local_calls']))
            m = BIND.search(s['text'])
            if m and m.group(1).lower() not in STOPW and lc:
                bound[m.group(1)] |= lc
            if lc & targets:
                p = lc - targets
                for w in set(WORD.findall(s['text'])):
                    p |= bound.get(w, set())
                for x in p - targets:
                    prod[x].add(a)
    return prod


def back_through(starts, through):
    """Callers of starts; continue past a caller only if it is in `through`."""
    seen, st = set(), list(starts)
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        if x in starts or x in through:
            st.extend(rev[x] - seen)
    return seen


def rule(S, state):
    """Returns the three rules' sets.
    naive: fwd(back(S+K)) to fixpoint.
    cone:  back(S+K) + fwd(S+K+producers).
    T (chosen): backward from sinks and state-writing seeds, passing through a
       caller only if it is itself a seed or a fetch wrapper; plus forward from seeds, sinks and
       the argument producers of the included callers."""
    wrappers_ = {a for a in WRAPPERS if FETCH in fwd({a})}
    seeds = S | K
    B = back(seeds)
    naive = fwd(B)
    P = arg_producers(B - seeds, B)
    cone = B | fwd(seeds | set(P))
    BT = back_through(K | state, seeds | wrappers_)
    PT = arg_producers(BT - seeds, BT)
    T = BT | fwd(seeds | set(PT))
    return dict(seeds=seeds, B=B, naive=naive, P=P, cone=cone, BT=BT, PT=PT, T=T)


R = {'ws': rule(S_ws, STATE_ws), 'all': rule(S_all, STATE_all)}
X = R['all']   # chosen: whole-spec seeds, rule T
seeds, B, NAIVE, P, CL = X['seeds'], X['BT'], X['naive'], X['PT'], X['T']

# exits: links from closure steps to other specs, by host
def exits(aset):
    host = collections.Counter()
    hook = collections.Counter()
    for a in aset:
        for s in algos[a]['cls']:
            if 'extension-hook' in s['markers']:
                hook['extension-hook step'] += 1
            for u in s['ext_calls']:
                h = re.sub(r'^https?://([^/#]+).*', r'\1', u) if u else '(bikeshed xref, spec unknown)'
                host[h] += 1
    return host, hook


# ------------------------------------------------------------ sizes and comparison
lines = []
def say(*x):
    lines.append(' '.join(map(str, x)))

say('nodes in corpus', len(algos), '= algorithms', N_ALGOS, '+ unowned blocks', N_BLOCKS,
    '; html', sum(a[0] == 'html' for a in algos), 'fetch', sum(a[0] == 'fetch' for a in algos))
say('hand closure', len(HAND))
say('sinks', len(K), sorted(name(a) for a in K))
def ov(Sx):
    return f'{len(Sx)} ({100 * len(Sx) / len(algos):.0f}% of corpus); both {len(HAND & Sx)} rule-only {len(Sx - HAND)} hand-only {len(HAND - Sx)}'


for lab in ('ws', 'all'):
    Y = R[lab]
    st = STATE_ws if lab == 'ws' else STATE_all
    say(f'[{lab}] seeds {len(Y["seeds"]) - len(K)} (+{len(K)} sinks), state-writing {len(st)}; seeds in hand {len((Y["seeds"] - K) & HAND)}')
    say(f'[{lab}] naive  backward {len(Y["B"])}; fwd(back) {ov(Y["naive"])}')
    say(f'[{lab}] cone   producers {len(Y["P"])}; {ov(Y["cone"])}')
    say(f'[{lab}] T      backward {len(Y["BT"])}, producers {len(Y["PT"])}; {ov(Y["T"])}')
# sensitivity of T: producers of depth-2 callers (callers of included non-seed callers)
d2 = set()
for c in B - seeds:
    d2 |= rev[c]
d2 -= CL
P2 = arg_producers(d2, B)
extra = fwd(set(P2) | d2) - CL
say('T sensitivity: depth-2 callers not in T', len(d2), '; adding them and their producers would add', len(extra))
# stability: drop one seed at a time (chosen rule)
sizes = []
for s in sorted(seeds - K, key=str):
    t = rule((seeds - K) - {s}, STATE_all - {s})['T']
    sizes.append(len(CL) - len(t))
say('leave-one-seed-out (T): algorithms lost, max', max(sizes), 'median', sorted(sizes)[len(sizes) // 2],
    'seeds whose removal loses >10:', sum(x > 10 for x in sizes))
HO = HAND - CL
say('hand-only under T by spec', dict(collections.Counter(a[0] for a in HO)),
    '; reached from a hand root that is not a seed or sink:', len(HO))
host, hook = exits(CL)
say('exits from tight closure (external call targets by host):', dict(host.most_common()))
say('extension-hook steps in tight closure:', sum(hook.values()))
hh, _ = exits(HAND)
say('exits from hand closure:', sum(hh.values()), 'tight:', sum(host.values()))


FS = fwd(seeds | set(P))
def why2(a):
    r = []
    if a in K: r.append('sink')
    if a in seeds - K: r.append('seed')
    if a in B and a not in seeds: r.append('caller')
    if a in P: r.append('arg-producer')
    if a in FS and a not in seeds and a not in P and a not in B: r.append('callee')
    return '+'.join(r)


with open(os.path.join(OUT, 'compare.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['spec', 'algorithm', 'anchor', 'membership', 'rule_role', 'in_naive'])
    for a in sorted(CL | HAND | NAIVE, key=lambda a: (a[0], algos[a]['line'])):
        m = 'both' if a in CL and a in HAND else 'rule-only' if a in CL else 'hand-only' if a in HAND else 'naive-only'
        w.writerow([a[0], name(a), anchor(a), m, why2(a) if a in CL else '', 'y' if a in NAIVE else 'n'])

# ------------------------------------------------------------ path inventory
# (1) fetch call sites: steps linking to fetch (R1a) or to a wrapper (R1b: an algorithm
#     whose name contains fetch/preload and that reaches fetch); (1c) re-entry: a step in an
#     algorithm reachable from fetch that calls an algorithm on a call-graph cycle through it.
FWD_FETCH = fwd({FETCH})
wrappers = {a for a in algos if a != FETCH and re.search(r'fetch|preload', norm(name(a))) and FETCH in fwd({a})}


MAIN = aid('fetch', 'concept-main-fetch')
SCC_MAIN = fwd({MAIN}) & back({MAIN})   # fetch-internal algorithms that re-enter main fetch


def on_cycle(caller, callee):
    return caller in fwd({callee})


# (2) result holders: dfns whose type clause names a result type, propagated through
#     references between holder definitions (structure discovery, not step keywords).
TYPE = re.compile(r'\b(?:a|an|or|of|each|either|null or a)\s+(responses?|module scripts?|classic scripts?|'
                  r'scripts?|documents?|images?)\b(?!\s+elements?)', re.I)
NONCONCEPT = re.compile(r'^(attr|event|dom|handler|selector|element)-')
CONTAINER = re.compile(r'\b(map|list|cache|set|records?|table|store)\b')


def strip(t):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t))


def clause(spec, d):
    L = SRC[spec]
    i = d['line'] - 1
    first = L[i]
    buf = []
    if re.match(r'\s*<dt', first):
        buf.append(first)
        for j in range(i + 1, min(i + 12, len(L))):
            if re.match(r'\s*(<dt|</dl)', L[j]):
                break
            buf.append(L[j])
    else:
        k = first.find('<dfn')
        buf.append(first[k:] if k >= 0 else first)
        for j in range(i + 1, min(i + 10, len(L))):
            if '</p>' in L[j - 1] and j > i + 0 and '</p>' in ''.join(buf):
                break
            buf.append(L[j])
    raw = '\n'.join(buf)
    raw = raw.split('</p>')[0]
    k1 = raw.find('<dfn')
    dt = bool(re.match(r'\s*<dt', first))
    cut = [x for x in (raw.find('<dfn', k1 + 4), -1 if dt else raw.find('<p', k1 + 4), -1 if dt else raw.find('\n\n', k1)) if x > k1 >= 0]
    if cut:  # stop at the next definition or paragraph
        raw = raw[:min(cut)]
    return raw


def clause_links(spec, raw):
    out = set()
    if spec == 'html':
        for m in re.finditer(r'<span(?: data-x="([^"]*)")?[^>]*>([^<]*)</span>', raw):
            key = norm(m.group(1) if m.group(1) is not None and m.group(1) != '' else m.group(2))
            i = g['lookup']('html', key)
            if i is not None:
                out.add(('html', i))
    else:
        for m in re.finditer(r'<a(?: for=[^ >]*)?>([^<]*)</a>|\[=([^=]*)=\]', raw):
            key = norm(m.group(1) or m.group(2) or '')
            i = g['lookup']('fetch', key)
            if i is not None:
                out.add(('fetch', i))
    return out


CL_TEXT = {}
for spec, D in SPECS.items():
    for d in D['dfns']:
        a_ = d['attrs']
        if d.get('external') or d.get('in_step') or (spec, d['idx']) in algos or NONCONCEPT.match(a_.get('data-x', '')) \
                or any(x in a_ for x in ('element-attr', 'attribute', 'event', 'method', 'element', 'interface', 'dict-member')):
            continue
        raw = clause(spec, d)
        CL_TEXT[(spec, d['idx'])] = (strip(raw), clause_links(spec, raw))


def first_sentences(t, n=3):
    return '. '.join(re.split(r'(?<!e\.g)(?<!i\.e)\.\s+(?=[A-Z])', t)[:n])


def own(k):
    t = CL_TEXT[k][0]
    nm = SPECS[k[0]]['dfns'][k[1]]['text']
    i = t.find(nm)
    return first_sentences(t[i + len(nm):] if 0 <= i < 40 else t)


holders = {k for k in CL_TEXT if TYPE.search(own(k))}
changed = True
while changed:
    changed = False
    for k, (t, ls) in CL_TEXT.items():
        if k in holders:
            continue
        for h in ls & holders:
            ht = re.escape(norm(SPECS[h[0]]['dfns'][h[1]]['text']))
            if re.search(r'(\b(is|which is|be)\s+an?\s+|^\s*an?\s+)' + ht, norm(first_sentences(t))):
                holders.add(k)
                changed = True
                break
# struct rule: an untyped container defined within 40 lines before a holder struct, no algorithm between
for k, (t, ls) in CL_TEXT.items():
    spec, i = k
    d = SPECS[spec]['dfns'][i]
    if k in holders or not CONTAINER.search(norm(d['text'])) or 'ordered map' not in t:
        continue
    L = SRC[spec]
    for j in range(d['line'], min(d['line'] + 40, len(L))):
        if 'algorithm>' in L[j] or '<div algorithm' in L[j]:
            break
        m = re.search(r'<dfn[^>]*>([^<]*)</dfn> is a <span>struct', L[j])
        if m:
            ks = [x for x in g['index'][spec].get(norm(m.group(1)), [])]
            sub = [kk for kk in CL_TEXT if kk[0] == spec and SPECS[spec]['dfns'][kk[1]]['line'] in range(j + 1, j + 20)]
            if any(s in holders for s in sub):
                holders.add(k)
                break
CNAME = re.compile(r'(^|\s)(map|list|cache|set|records|table|store)s?$|^(list|map|set) of\b')
containers = {k for k in holders if CNAME.search(norm(SPECS[k[0]]['dfns'][k[1]]['text']))}
# tier F: fields (dfn with for=) whose own clause types them as a response, Document or module script
FTYPE = re.compile(r'\b(?:a|an|or|either|null or a)\s+(responses?|module scripts?|document)\b', re.I)
fields = {k for k in holders - containers if SPECS[k[0]]['dfns'][k[1]]['for']
          and FTYPE.search(own(k).split('. ')[0])}
# algorithms returning a container (Return ... <container noun>): their results are containers
ret_containers = set()
for a in algos:
    for s in algos[a]['cls']:
        if s['form'] == 'return' and re.search(r'\bcache\b|\bmap\b|\blist\b', norm(s['text'])) \
                and re.search(r'unique|associated', norm(s['text'])):
            ret_containers.add(a)

READV = re.compile(r'\b(contains?|exists?|get|getting|for each|is not null|is null|consum\w*|take|remove|'
                   r'whose|matching|matches|from|is non-null|the value of)\b|\[')
WRITEV = re.compile(r'^(set|append|add|insert|extend|prepend)\b|\bset \S+(?:\'s \S+)* to\b')

paths, nid = [], 0


def add(kind, rule_, a, p, structure, key=''):
    global nid
    nid += 1
    paths.append([f'P{nid:04d}', kind, rule_, a[0], name(a), anchor(a), p, structure, key])


ext_resp = 0
for a in sorted(CL, key=lambda a: (a[0], algos[a]['line'])):
    A = algos[a]
    if A['prose']:
        continue
    alias = {}
    for s in A['cls']:
        lc = set(map(tuple, s['local_calls']))
        t = s['text']
        if FETCH in lc:
            add('fetch-call', 'R1a', a, s['path'], 'fetch')
        elif lc & wrappers - {a}:
            add('fetch-call', 'R1b', a, s['path'], '; '.join(sorted(name(x) for x in lc & wrappers - {a})))
        if a in SCC_MAIN:
            cyc = [x for x in lc if x == a or x == MAIN]   # self-retry or back to main fetch
            if cyc and not (FETCH in lc):
                add('re-entry', 'R1c', a, s['path'], '; '.join(sorted(name(x) for x in cyc)))


# reuse pass: needs the raw step dicts (links to non-algorithm dfns)
def iter_steps(A):
    def rec(steps, path):
        for i, s in enumerate(steps, 1):
            if s.get('in_note'):
                continue
            p = f'{path}{i}'
            yield p, s
            yield from rec(s['children'], p + '.')
    yield from rec(A['steps'], '')


def camel(n):
    w = re.findall(r'[a-z0-9]+', n.lower())
    return w[0] + ''.join(x.capitalize() for x in w[1:]) if w else ''


CAMEL = collections.defaultdict(set)
for k in containers | ret_containers:
    n = SPECS[k[0]]['dfns'][k[1]]['text'] if k in CL_TEXT else name(k)
    CAMEL[camel(n)].add(k)
PRIMITIVE = {'infra.spec.whatwg.org', 'dom.spec.whatwg.org', 'url.spec.whatwg.org', 'webidl.spec.whatwg.org',
             'encoding.spec.whatwg.org', 'mimesniff.spec.whatwg.org', 'streams.spec.whatwg.org'}
exit_hosts = collections.Counter()

for a in sorted(CL, key=lambda a: (a[0], algos[a]['line'])):
    A = algos[a]
    if A['prose']:
        continue
    alias, vals = {}, {}
    for p, s in iter_steps(A):
        t = re.sub(r'\s+', ' ', s['text'])
        refs = set()
        for L in s['links']:
            if L['note']:
                continue
            r = resolve(a[0], L)
            if r[0] == 'local' and r[2] is not None:
                refs.add((r[1], r[2]))
        hit = refs & containers
        hitf = refs & fields
        rc = refs & ret_containers
        m = BIND.search(t)
        if m and (hit or rc):
            alias[m.group(1)] = sorted(hit | rc)
        via_alias = [v for v in alias if re.search(r'\b' + re.escape(v) + r'\b', t) and not (m and m.group(1) == v and (hit or rc))]
        struct = set(hit) | rc
        if a in ret_containers and re.match(r'(?i)return\b', t):
            struct.add(a)
        for v in via_alias:
            struct |= set(alias[v])
        by_name = [c for c in CAMEL if c and re.search(r'\b' + c + r'\b', s['text'])]
        for c in by_name:
            struct |= CAMEL[c]
        if by_name and not via_alias and not hit:
            via_alias = ['name']
        if struct:
            labels = '; '.join(sorted(SPECS[x[0]]['dfns'][x[1]]['text'] if x in CL_TEXT else name(x) for x in struct))
            kind = 'reuse-write' if WRITEV.search(t.lower()) and not READV.search(t.lower().split(' to ')[-1] if ' to ' in t.lower() else '') else 'reuse-read'
            if m and (hit or rc) and not via_alias:
                kind = 'reuse-bind'
            add(kind, 'R2d' + ('+name' if via_alias == ['name'] else '+alias' if via_alias else ''), a, p, labels)
            if m and kind != 'reuse-bind' and m.group(1) not in alias:
                vals[m.group(1)] = struct   # a value taken from the store
        else:
            used = [v for v in vals if re.search(r'\b' + re.escape(v) + r'\b', t)]
            if used:
                sv = set().union(*(vals[v] for v in used))
                labels = '; '.join(sorted(SPECS[x[0]]['dfns'][x[1]]['text'] if x in CL_TEXT else name(x) for x in sv))
                add('reuse-use', 'R2v', a, p, labels)
        if hitf and not struct:
            labels = '; '.join(sorted(SPECS[x[0]]['dfns'][x[1]]['text'] + ' (for ' + ', '.join(SPECS[x[0]]['dfns'][x[1]]['for']) + ')' for x in hitf))
            kind = 'field-write' if WRITEV.search(t.lower()) else 'field-read'
            add(kind, 'R2f', a, p, labels)
        # external call whose result is bound to a response-like variable
        cl = [c for c in A['cls'] if c['path'] == p]
        for u in (cl[0]['ext_calls'] if cl else []):
            h = re.sub(r'^https?://([^/#]+).*', r'\1', u) if u else '(bikeshed xref, spec unknown)'
            exit_hosts[h] += 1
            if h not in PRIMITIVE and u:
                add('exit-call', 'X', a, p, h + '#' + u.split('#')[-1])
        if cl and cl[0]['ext_calls'] and m and re.search(r'response', m.group(1), re.I):
            add('exit-response', 'R2x', a, p, 'external: ' + ', '.join(sorted({re.sub(r'^https?://([^/#]+).*', r'\1', u or '?') for u in cl[0]['ext_calls']})))

with open(os.path.join(OUT, 'paths.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['id', 'kind', 'rule', 'spec', 'algorithm', 'anchor', 'step', 'structure_or_callee', 'key'])
    w.writerows(paths)

say('holders discovered', len(holders), 'containers', len(containers), sorted(SPECS[k[0]]['dfns'][k[1]]['text'] for k in containers))
say('field holders (tier F)', len(fields))
say('exit calls in T: primitive', sum(v for h, v in exit_hosts.items() if h in PRIMITIVE),
    'other-spec', sum(v for h, v in exit_hosts.items() if h not in PRIMITIVE), dict(exit_hosts.most_common()))
say('algorithms returning a container', sorted(name(a) for a in ret_containers))
say('wrappers', len(wrappers), '; fetch-internal re-entry component', sorted(name(x) for x in SCC_MAIN))
say('paths by kind', dict(collections.Counter(p[1] for p in paths)))
with open(os.path.join(OUT, 'closure-rule.txt'), 'w', encoding='utf-8') as f:
    f.write(RULE_TEXT + '\nMeasured (written by boundary.py):\n' + '\n'.join(lines) + '\n')
print('\n'.join(lines))
if SCRATCH:
    with open(os.path.join(SCRATCH, 'holders_evidence.tsv'), 'w', encoding='utf-8') as f:
        for k in sorted(containers | fields):
            d = SPECS[k[0]]['dfns'][k[1]]
            f.write('\t'.join([k[0], str(d['line']), 'C' if k in containers else 'F', d['text'], ','.join(d['for']),
                               first_sentences(CL_TEXT[k][0])[:300]]) + '\n')
