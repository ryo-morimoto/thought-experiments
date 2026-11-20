"""Resolve links, classify steps, compute call-graph closure from isolation roots.

usage: python3 -I analyze.py <html.json> <fetch.json> <outdir>
"""
import sys, re, json, collections

H = json.load(open(sys.argv[1]))
F = json.load(open(sys.argv[2]))
OUT = sys.argv[3]
SPECS = {'html': H, 'fetch': F}

def norm(s):
    return re.sub(r'\s+', ' ', s or '').strip().lower()

def slug(s):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')

# ---------------------------------------------------------------- dfn index
index = {'html': collections.defaultdict(list), 'fetch': collections.defaultdict(list)}
by_id = {'html': {}, 'fetch': {}}
for spec, D in SPECS.items():
    for d in D['dfns']:
        a = d['attrs']
        if spec == 'html':
            keys = [norm(a['data-x'])] if a.get('data-x') else [norm(d['text'])]
        else:
            keys = [norm(x) for x in a['lt'].split('|')] if a.get('lt') else [norm(d['text'])]
        d['keys'] = [k for k in keys if k]
        d['for'] = [norm(x) for x in a.get('for', '').split(',') if x.strip()]
        d['external'] = a.get('data-x-href') if spec == 'html' else None
        for k in d['keys']:
            index[spec][k].append(d['idx'])
        if a.get('id'):
            by_id[spec][a['id']] = d['idx']
        for k in d['keys']:
            by_id[spec].setdefault(slug(k), d['idx'])
            for f in d['for']:
                by_id[spec].setdefault(slug(f + '-' + k), d['idx'])

# ---------------------------------------------------------------- algorithms
# algorithm id = (spec, dfn idx)
algos = {}
for spec, D in SPECS.items():
    for b in D['blocks']:
        if b['owner'] is None:
            continue
        aid = (spec, b['owner'])
        A = algos.setdefault(aid, {'spec': spec, 'dfn': b['owner'],
                                   'name': D['dfns'][b['owner']]['text'],
                                   'line': D['dfns'][b['owner']]['line'], 'steps': [],
                                   'prose': False, 'prose_links': []})
        A['steps'].extend(b['steps'])
    for p in D['prose_algos']:
        if p['owner'] is None:
            continue
        aid = (spec, p['owner'])
        if aid not in algos:
            algos[aid] = {'spec': spec, 'dfn': p['owner'], 'name': D['dfns'][p['owner']]['text'],
                          'line': D['dfns'][p['owner']]['line'], 'steps': [], 'prose': True,
                          'prose_links': p['links']}

def variants(k):
    out = [k]
    w = k.split(' ')
    def forms(x):
        r = []
        if x.endswith('ies'): r.append(x[:-3] + 'y')
        if x.endswith('es'): r.append(x[:-2])
        if x.endswith('s'): r.append(x[:-1])
        if x.endswith('ing'): r += [x[:-3], x[:-3] + 'e', x[:-4] if len(x) > 5 and x[-4] == x[-5] else x[:-3]]
        if x.endswith('ed'): r += [x[:-2], x[:-1], x[:-3] if len(x) > 4 and x[-3] == x[-4] else x[:-2]]
        return r
    for f in forms(w[0]):
        out.append(' '.join([f] + w[1:]))
    if len(w) > 1:
        for f in forms(w[-1]):
            out.append(' '.join(w[:-1] + [f]))
    return out

def pick(spec, cands, for_):
    D = SPECS[spec]['dfns']
    cands = [c for c in cands if not D[c].get('in_step')] or cands
    if for_ and for_ != '/':
        c2 = [c for c in cands if for_ in D[c]['for']]
        if c2: cands = c2
    elif for_ == '/':
        c2 = [c for c in cands if not D[c]['for']]
        if c2: cands = c2
    # prefer algorithm owners
    c3 = [c for c in cands if (spec, c) in algos]
    return (c3 or cands)[0]

def lookup(spec, key, for_=None):
    for v in variants(key):
        if v in index[spec]:
            return pick(spec, index[spec][v], for_)
    return None

stats_links = collections.Counter()
def resolve(spec, L):
    """returns ('local', spec, idx) | ('external', url_or_None) | ('unresolved',)"""
    a = L['attrs']
    if spec == 'html':
        if L['tag'] == 'a':
            href = a.get('href', '')
            if href.startswith('#'):
                i = by_id['html'].get(href[1:])
                return ('local', 'html', i) if i is not None else ('unresolved',)
            if href.startswith('http'):
                return ('external', href)
            return ('unresolved',)
        key = norm(a['data-x']) if 'data-x' in a else norm(L['text'])
        if not key:
            return ('none',)
        i = lookup('html', key)
        if i is None:
            return ('unresolved',)
        d = H['dfns'][i]
        if d['external']:
            url = d['external']
            m = re.match(r'https://fetch\.spec\.whatwg\.org/#(.+)$', url)
            if m and m.group(1) in by_id['fetch']:
                return ('local', 'fetch', by_id['fetch'][m.group(1)])
            return ('external', url)
        return ('local', 'html', i)
    else:
        if a.get('href', '').startswith('http'):
            return ('external', a['href'])
        key = norm(a['lt'].split('|')[0]) if a.get('lt') else norm(L['text'])
        for_ = norm(a.get('for', '')) or None
        if a.get('spec'):
            return ('external', 'spec:' + a['spec'])
        i = lookup('fetch', key, for_)
        if i is not None:
            return ('local', 'fetch', i)
        i = lookup('html', key, for_)
        if i is not None and not H['dfns'][i]['external']:
            return ('local', 'html', i)
        return ('external', None)

# ---------------------------------------------------------------- classifier
R_PARALLEL = re.compile(r'\bin parallel\b')
R_TASK = re.compile(r'\bqueue (a|an) ([a-z-]+ )*?(task|microtask)\b|\bqueue a (global|element|fetch|navigation|networking) task')
R_WAIT = re.compile(r'\b(wait|waits|waiting|await|spin the event loop|pause)\b')
R_UA = re.compile(r'implementation-defined|implementation-specific|user[- ]agent-defined|\buser agents? (may|should|can|could|might|must choose|is encouraged)|\bmay choose\b|\boptionally\b|discretion|\bheuristic|\bat any (time|point)\b')
R_HOOK = re.compile(r'other (applicable )?specifications|applicable specifications|specifications may|\bhooks?\b')
F_ASSERT = re.compile(r'^assert\b')
F_BRANCH = re.compile(r'^(if|otherwise|else|when|unless|switch on|depending on|based on)\b')
F_LOOP = re.compile(r'^(for each|for every|for all|while|repeat|for)\b')
F_RETURN = re.compile(r'^return\b')
F_ABORT = re.compile(r'^(throw|abort|terminate|fail)\b')
F_CONTROL = re.compile(r'^(continue|break|advance|jump|skip|go to|proceed|do nothing|ignore)\b')
F_ASSIGN = re.compile(r'^(let|set|increment|decrement|append|prepend|remove|extend|insert|replace|clear|empty|initialize|add|enqueue|dequeue|push|pop|unset|update|store)\b')
F_CALLVERB = re.compile(r'^(run|perform|invoke|call|execute|process|fire|resolve|reject|report|start|finalize|handle|apply)\b')
EXT_CALLCTX = re.compile(r'(the result of|\brun|\brunning|\binvoke|\binvoking|\bperform|\bperforming|\bcalling|\bcall)\s*$')

def classify(step, inherited, spec):
    t = norm(step['text'])
    t = re.sub(r'^(otherwise,\s*|then,?\s*|finally,\s*)', lambda m: m.group(0), t)
    links = [L for L in step['links'] if not L['note']]
    res = [resolve(spec, L) for L in links]
    local_calls, ext_calls, ext_any = [], [], []
    for L, r in zip(links, res):
        if r[0] == 'local' and (r[1], r[2]) in algos:
            local_calls.append((r[1], r[2]))
        elif r[0] == 'external':
            ext_any.append(r[1])
            before = norm(step['text'])[:max(L['off'], 0)]
            if L['off'] <= 1 or EXT_CALLCTX.search(before) or re.match(r'^\s*(with|given|on|for)\b', norm(step['text'])[L['off'] + len(L['text']):][:8]):
                ext_calls.append(r[1])
    markers = []
    if R_PARALLEL.search(t): markers.append('in-parallel')
    if R_TASK.search(t): markers.append('async-task')
    if R_WAIT.search(t): markers.append('wait')
    if R_UA.search(t): markers.append('ua-choice')
    if R_HOOK.search(t): markers.append('extension-hook')
    if inherited and not markers: markers.append('inside-in-parallel')
    form = None
    for name, rx in (('assert', F_ASSERT), ('branch', F_BRANCH), ('loop', F_LOOP),
                     ('return', F_RETURN), ('abort', F_ABORT), ('control', F_CONTROL), ('assign', F_ASSIGN)):
        if rx.search(t):
            form = name
            break
    if form is None and (local_calls or F_CALLVERB.search(t) or 'the result of' in t):
        form = 'call'
    if form is None and ext_calls:
        form = 'external-call'
    if form is None and not t:
        form = 'empty'
    if markers:
        cls, reason = 'remainder', markers[0]
    elif form is None:
        cls, reason = 'remainder', 'prose-only'
    elif form == 'external-call':
        cls, reason = 'boundary', 'external-call-only'
    elif form == 'empty':
        cls, reason = 'remainder', 'empty'
    else:
        cls, reason = 'extractable', form
    return {'line': step['line'], 'text': step['text'][:240], 'form': form, 'markers': markers,
            'class': cls, 'reason': reason, 'local_calls': local_calls,
            'ext_calls': ext_calls, 'ext_refs': len(ext_any)}

def walk(steps, spec, path='', inherited=False, out=None):
    if out is None: out = []
    for i, s in enumerate(steps, 1):
        if s.get('in_note'):
            continue
        p = f'{path}{i}'
        c = classify(s, inherited, spec)
        c['path'] = p
        out.append(c)
        walk(s['children'], spec, p + '.', inherited or 'in-parallel' in c['markers'], out)
    return out

for aid, A in algos.items():
    A['cls'] = walk(A['steps'], A['spec'])
    calls = set()
    for c in A['cls']:
        calls.update(map(tuple, c['local_calls']))
    if A['prose']:
        for L in A['prose_links']:
            r = resolve(A['spec'], L)
            if r[0] == 'local' and (r[1], r[2]) in algos:
                calls.add((r[1], r[2]))
    calls.discard(aid)
    A['calls'] = calls

# ---------------------------------------------------------------- roots
def find(spec, key):
    i = lookup(spec, norm(key))
    if i is None or (spec, i) not in algos:
        cands = [ (spec, j) for j in index[spec].get(norm(key), []) if (spec, j) in algos]
        return cands[0] if cands else None
    return (spec, i)

ROOTS = [
    ('html', 'obtain-similar-origin-window-agent'),
    ('html', 'obtain a site'),
    ('html', 'determining the origin'),
    ('html', 'obtain-browsing-context-navigation'),
    ('html', 'check-browsing-context-group-switch-coop-value'),
    ('html', 'check-browsing-context-group-switch-coop-value-popup'),
    ('html', 'matching-coop'),
    ('html', 'creating a new browsing context and document'),
    ('html', 'create-the-document-object'),
    ('html', 'dom-crossoriginisolated'),
    ('html', 'navigate'),
    ('fetch', 'main fetch'),
    ('fetch', 'scheme fetch'),
    ('fetch', 'http fetch'),
    ('fetch', 'http-network-or-cache fetch'),
    ('fetch', 'cross-origin resource policy check'),
    ('fetch', 'cross-origin resource policy internal check'),
    ('fetch', 'cross-origin-embedder-policy allows credentials'),
]
roots = []
for spec, k in ROOTS:
    r = find(spec, k)
    print('root', spec, k, '->', r and (algos[r]['name'], algos[r]['line'], 'prose' if algos[r]['prose'] else len(algos[r]['cls'])))
    if r: roots.append(r)

def closure(starts):
    seen, stack = set(), list(starts)
    while stack:
        a = stack.pop()
        if a in seen: continue
        seen.add(a)
        stack.extend(algos[a]['calls'] - seen)
    return seen

CL = closure(roots)

def summarize(aset, label):
    c = collections.Counter(); reasons = collections.Counter(); forms = collections.Counter()
    nprose = 0
    for a in aset:
        A = algos[a]
        if A['prose']:
            nprose += 1
            continue
        for s in A['cls']:
            c[s['class']] += 1
            if s['class'] != 'extractable': reasons[s['reason']] += 1
            else: forms[s['form']] += 1
    tot = sum(c.values())
    return {'label': label, 'algorithms': len(aset), 'prose_algorithms_no_ol': nprose,
            'html': sum(1 for a in aset if a[0] == 'html'), 'fetch': sum(1 for a in aset if a[0] == 'fetch'),
            'steps': tot, 'classes': dict(c), 'remainder_reasons': dict(reasons.most_common()),
            'extractable_forms': dict(forms.most_common()),
            'pct_extractable': round(100 * c['extractable'] / tot, 1) if tot else None,
            'pct_extractable_incl_boundary': round(100 * (c['extractable'] + c['boundary']) / tot, 1) if tot else None}

# path slice: reachable from navigate/main fetch AND reaching a decision algorithm
DECISION = [find(*x) for x in [('html', 'obtain-similar-origin-window-agent'), ('html', 'determining the origin'),
            ('html', 'obtain-browsing-context-navigation'), ('html', 'check-browsing-context-group-switch-coop-value'),
            ('html', 'check-browsing-context-group-switch-coop-value-popup'), ('html', 'matching-coop'),
            ('html', 'create-the-document-object'), ('fetch', 'cross-origin resource policy check'),
            ('fetch', 'cross-origin resource policy internal check'), ('fetch', 'cross-origin-embedder-policy allows credentials'),
            ('html', 'obtain a site')]]
DECISION = [d for d in DECISION if d]
fwd = closure([find('html', 'navigate'), find('fetch', 'main fetch')])
rev = collections.defaultdict(set)
for a in CL:
    for b in algos[a]['calls']:
        rev[b].add(a)
back, st = set(), list(DECISION)
while st:
    x = st.pop()
    if x in back: continue
    back.add(x); st.extend(rev[x])
SLICE = (fwd & back) | set(DECISION)

results = {
    'whole_html': summarize({a for a in algos if a[0] == 'html'}, 'all HTML algorithms'),
    'whole_fetch': summarize({a for a in algos if a[0] == 'fetch'}, 'all Fetch algorithms'),
    'closure': summarize(CL, 'closure from roots'),
    'roots': summarize(set(roots), 'roots only'),
    'slice': summarize(SLICE, 'navigate/main-fetch -> origin/COOP/CORP/COEP decision slice'),
}
# per-root table
per_root = []
for r in roots:
    s = summarize({r}, algos[r]['name'])
    s['closure_size'] = len(closure([r]))
    per_root.append(s)
results['per_root'] = per_root

# external boundary stats in closure
ext = collections.Counter()
for a in CL:
    for s in algos[a]['cls']:
        for u in s['ext_calls']:
            host = re.sub(r'^https?://([^/#]+).*', r'\1', u) if u else '(bikeshed-xref, unknown spec)'
            ext[host] += 1
results['closure_external_call_targets'] = dict(ext.most_common(25))
# unresolved / non-algorithm local link stats in closure
lk = collections.Counter()
unk = collections.Counter()
for a in CL:
    A = algos[a]
    def rec(steps):
        for s in steps:
            for L in s['links']:
                if L['note']: continue
                r = resolve(A['spec'], L)
                if r[0] == 'unresolved' or (r[0] == 'external' and r[1] is None):
                    unk[(r[0], A['spec'], L['attrs'].get('data-x') or L['attrs'].get('lt') or L['text'])] += 1
                if r[0] == 'local':
                    lk['local-algorithm' if (r[1], r[2]) in algos else 'local-non-algorithm(term/field/prose)'] += 1
                else:
                    lk[r[0]] += 1
            rec(s['children'])
    rec(A['steps'])
results['closure_link_resolution'] = dict(lk)
results['closure_unresolved_or_unknown_top'] = [list(k) + [v] for k, v in unk.most_common(80)]
results['slice_algorithms'] = sorted(f"{a[0]}:{algos[a]['name']}" for a in SLICE)
results['roots_resolved'] = [f"{a[0]}:{algos[a]['name']}@{algos[a]['line']}" for a in roots]
json.dump(results, open(OUT + '/results.json', 'w'), indent=1)

with open(OUT + '/closure_steps.tsv', 'w') as f:
    f.write('spec\talgorithm\talgo_line\tstep\tline\tclass\treason\tform\tmarkers\tin_slice\ttext\n')
    for a in sorted(CL, key=lambda a: (a[0], algos[a]['line'])):
        A = algos[a]
        if A['prose']:
            f.write(f"{a[0]}\t{A['name']}\t{A['line']}\t-\t{A['line']}\tremainder\tprose-algorithm(no ol)\t\t\t{a in SLICE}\t\n")
        for s in A['cls']:
            f.write(f"{a[0]}\t{A['name']}\t{A['line']}\t{s['path']}\t{s['line']}\t{s['class']}\t{s['reason']}\t{s['form']}\t{','.join(s['markers'])}\t{a in SLICE}\t{s['text']}\n")
with open(OUT + '/closure_algorithms.tsv', 'w') as f:
    for a in sorted(CL, key=lambda a: (a[0], algos[a]['line'])):
        A = algos[a]
        f.write(f"{a[0]}\t{A['line']}\t{A['name']}\t{'prose' if A['prose'] else len(A['cls'])}\t{a in SLICE}\n")

# expose for spot-check script
import pickle
pickle.dump({'algos': {f'{k[0]}:{k[1]}': {kk: vv for kk, vv in v.items() if kk != 'steps'} for k, v in algos.items()},
             'closure': [f'{a[0]}:{a[1]}' for a in CL], 'roots': [f'{a[0]}:{a[1]}' for a in roots]},
            open(OUT + '/state.pkl', 'wb'))
print(json.dumps({k: v for k, v in results.items() if k not in ('per_root', 'slice_algorithms')}, indent=1))
for s in per_root:
    print(s['label'][:60], s['steps'], s['classes'], s['remainder_reasons'], 'closure', s['closure_size'], 'prose' if s['prose_algorithms_no_ol'] else '')
