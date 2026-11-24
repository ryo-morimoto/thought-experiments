#!/usr/bin/env python3
"""Step-level dataflow over WHATWG HTML and Fetch algorithm steps
(experiments/2026-11-24-write-target-semantics.md, tree nodes B2b and B2c).

    python3 -I dataflow.py <extract/out> <html.src> <fetch.bs> <havoc/writesets.tsv> <outdir>

Inputs are not committed (spec text): extract/out holds html.json, fetch.json
and closure_steps.tsv from ../extract. Outputs hold only algorithm names, step
numbers, source line numbers, variable and field names, and the author's labels.

Model of the analysis (see RESULTS.md):
  cells   local (algorithm, var) incl. parameters; global (dfn) for every
          non-algorithm cross-reference (struct fields, concepts), shared by all
          objects (field-insensitive); RET(algorithm).
  defs    let V be / set LV to / for each V / whose F is / <dt>F</dt> in a struct
          literal / collection verbs on LV / return.
  uses    every var/link token of the step outside the def's left side, minus
          base pointers (a var directly followed by "'s <link>").
  calls   a link to an algorithm: uses RET(callee); arguments (tokens after the
          link) flow to every parameter of the callee (all-to-all).
  control enclosing steps and preceding steps with an exit (return, abort,
          throw, continue, break) in the same algorithm.
"""
import collections
import csv
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import specscan  # noqa: E402

OUT_IN, HTML_SRC, FETCH_BS, WRITESETS, OUTDIR = sys.argv[1:6]
H = json.load(open(os.path.join(OUT_IN, 'html.json')))
F = json.load(open(os.path.join(OUT_IN, 'fetch.json')))
SPECS = {'html': H, 'fetch': F}


def norm(s):
    return re.sub(r'\s+', ' ', s or '').strip().lower()


def slug(s):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')


# ------------------------------------------------ dfn index (as ../extract/analyze.py)
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

BY_FOR_TEXT = {'html': {}, 'fetch': {}}
for spec, D in SPECS.items():
    for d in D['dfns']:
        if d['for'] and not d.get('external') and not d.get('in_step'):
            for f in d['for']:
                BY_FOR_TEXT[spec].setdefault(f + '/' + norm(d['text']), d['idx'])

# derived getters that the dfn defines as another field (hand-written, 2 entries)
ALIAS = {('G', 'fetch', by_id['fetch']['concept-request-current-url']): ('G', 'fetch', by_id['fetch']['concept-request-url-list']),
         ('G', 'fetch', by_id['fetch']['concept-response-url']): ('G', 'fetch', by_id['fetch']['concept-response-url-list'])}

algos = {}
for spec, D in SPECS.items():
    for b in D['blocks']:
        if b['owner'] is None:
            continue
        aid = (spec, b['owner'])
        A = algos.setdefault(aid, {'spec': spec, 'name': D['dfns'][b['owner']]['text'],
                                   'line': D['dfns'][b['owner']]['line'], 'steps': []})
        A['steps'].extend(b['steps'])


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
    c3 = [c for c in cands if (spec, c) in algos]
    return (c3 or cands)[0]


def lookup(spec, key, for_=None):
    for v in variants(key):
        if v in index[spec]:
            return pick(spec, index[spec][v], for_)
    return None


def resolve(spec, tag, a, text):
    if spec == 'html':
        if tag == 'a':
            href = a.get('href', '')
            if href.startswith('#'):
                i = by_id['html'].get(href[1:])
                return ('local', 'html', i) if i is not None else ('unresolved',)
            if href.startswith('http'):
                return ('external', href)
            return ('unresolved',)
        key = norm(a['data-x']) if 'data-x' in a else norm(text)
        if not key:
            return ('none',)
        i = lookup('html', key)
        if i is None:
            return ('unresolved',)
        d = H['dfns'][i]
        if d['external']:
            m = re.match(r'https://fetch\.spec\.whatwg\.org/#(.+)$', d['external'])
            if m and m.group(1) in by_id['fetch']:
                return ('local', 'fetch', by_id['fetch'][m.group(1)])
            return ('external', d['external'])
        return ('local', 'html', i)
    if a.get('href', '').startswith('http'):
        return ('external', a['href'])
    key = norm(a['lt'].split('|')[0]) if a.get('lt') else norm(text)
    for_ = norm(a.get('for', '')) or None
    if a.get('spec'):
        return ('external', 'spec:' + a['spec'])
    # strict "for": a link scoped to a struct that neither spec defines is external
    # (e.g. Infra's list/clone must not resolve to Fetch's request/clone)
    i = lookup('fetch', key, for_)
    if i is not None and (not for_ or for_ == '/' or for_ in F['dfns'][i]['for']):
        return ('local', 'fetch', i)
    i = lookup('html', key, for_)
    if i is not None and not H['dfns'][i]['external'] and (not for_ or for_ == '/' or for_ in H['dfns'][i]['for']):
        return ('local', 'html', i)
    return ('external', None)


def dfn_label(spec, i):
    d = SPECS[spec]['dfns'][i]
    f = d['for'][0] + '/' if d['for'] else ''
    return f"{spec}:{f}{d['text']}"


# ------------------------------------------------ token streams
SCAN = {'html': specscan.scan(HTML_SRC, 'html'), 'fetch': specscan.scan(FETCH_BS, 'bikeshed')}

EXIT = re.compile(r'\b(return|abort|throw|terminate|continue|break)\b')
COLL_TO = re.compile(r'\b(append|prepend|insert|add|enqueue|push)\b')
COLL_FROM = re.compile(r'\b(remove|dequeue|pop)\b')
COLL_SELF = re.compile(r'\b(extend|empty|clear|sort|increment|decrement|replace|unset)\b')
OTHER_W = re.compile(r'\b(initialize|store|update|modify|change|mark|record)\b')


class Step:
    __slots__ = ('aid', 'spec', 'path', 'line', 'parent', 'order', 'toks', 'skel', 'cells',
                 'defs', 'holes', 'calls', 'indirect', 'exits', 'ua', 'base', 'lvs', 'names', 'argids')


steps = []
by_alg = collections.defaultdict(list)
missing_tokens = 0


def cell_of(spec, aid, tok):
    if tok[0] == 'v':
        return ('L', aid, tok[1])
    r = resolve(spec, tok[1], tok[2], tok[3])
    if r[0] == 'local' and r[2] is not None:
        if (r[1], r[2]) in algos:
            return ('C', (r[1], r[2]))
        c = ('G', r[1], r[2])
        return ALIAS.get(c, c)
    if r[0] == 'external':
        if tok[2].get('for') and tok[2]['for'] != '/':
            k = norm(tok[2]['for'] + '/' + (tok[2].get('lt') or tok[3]).split('|')[0])
            # a Fetch xref to a field HTML defines (matched by for + text)
            if k in BY_FOR_TEXT['html']:
                i = BY_FOR_TEXT['html'][k]
                if ('html', i) in algos:
                    return ('C', ('html', i))
                return ('G', 'html', i)
            return ('G', 'ext', k)
        return ('X', r[1] or '?', norm(tok[3]))
    if r[0] == 'none':
        return ('K', tok[3])        # <code data-x=""> : a literal, not a reference
    return ('U', tok[3])


def build(aid, A):
    global missing_tokens
    spec = aid[0]
    stepmap = SCAN[spec][0]

    def walk(ss, path, parent):
        global missing_tokens
        for i, s in enumerate(ss, 1):
            if s.get('in_note'):
                continue
            st = Step()
            st.aid, st.spec, st.path, st.line, st.parent = aid, spec, f'{path}{i}', s['line'], parent
            st.toks = stepmap.get(s['line'])
            if st.toks is None:
                missing_tokens += 1
                st.toks = [('t', s['text'])]
            st.order = len(by_alg[aid])
            steps.append(st)
            by_alg[aid].append(st)
            walk(s['children'], st.path + '.', st)
    walk(A['steps'], '', None)


for aid, A in algos.items():
    build(aid, A)

# parameters: vars in the preamble of the owner dfn
params = {}
for aid, A in algos.items():
    pre = SCAN[aid[0]][1].get(A['line'], [])
    seen = []
    for t in pre:
        if t[0] == 'v' and t[1] not in seen:
            seen.append(t[1])
    params[aid] = seen


# ------------------------------------------------ def/use extraction
LV_RE = r"((?:the )?(?:⟨\d+⟩(?:'s? |’s |\[[^\]]*\]| of | )?){1,6})"
# links whose text is a collection verb are read as the verb, not as a cell
VERB_LINKS = {'append', 'extend', 'remove', 'prepend', 'insert', 'enqueue', 'dequeue', 'push',
              'pop', 'clear', 'empty', 'replace', 'sort', 'set', 'for each', 'continue', 'break',
              'iterate', 'appending', 'removing', 'extending', 'setting', 'prepending', 'inserting',
              'remove all', 'removed', 'appended', 'sorting in ascending order', 'sort in ascending order',
              'sorting in descending order', 'sort in descending order'}
SENT_END = re.compile(r"(?:\.(?= |$)|; |:(?= |$)|\bthen\b|\botherwise\b)")


def parse_lv(st, lv):
    """Left side -> (cell, kind) or (None, reason)."""
    ids = [int(x) for x in re.findall(r'⟨(\d+)⟩', lv)]
    if not ids:
        return None, 'untagged-target'
    cells = [st.cells[i] for i in ids]
    if '[' in lv:
        c = cells[0] if len(cells) == 1 else cells[-1]
        return (c, 'collection') if c[0] in 'LG' else (None, 'unresolved-target')
    last = cells[-1]
    if len(ids) > 1 and " of " in lv and cells[0][0] in 'GUX':
        last = cells[0]          # "the F of V"
    if last[0] == 'L':
        return (last, 'local') if len(ids) == 1 else (last, 'local?')
    if last[0] == 'G':
        return last, 'field'
    if last[0] == 'C' and len(ids) > 1:
        # a field whose dfn also owns steps (a getter with an algorithm): the field
        return ('G',) + last[1], 'field'
    if last[0] == 'C':
        return None, 'call-as-target'
    return None, 'unresolved-target'


def ids_in(s):
    return [int(x) for x in re.findall(r'⟨(\d+)⟩', s)]


def region(sk, start):
    m = SENT_END.search(sk, start)
    return sk[start:m.start() if m else len(sk)]


def analyse(st):
    toks = st.toks
    st.cells, parts = {}, []
    for t in toks:
        if t[0] == 't':
            parts.append(t[1])
        elif t[0] == 'l' and norm(t[3]) in VERB_LINKS:
            parts.append(t[3])
        else:
            i = len(st.cells)
            st.cells[i] = cell_of(st.spec, st.aid, t)
            st.cells[i] = st.cells[i] + (('name', norm(t[1] if t[0] == 'v' else t[3])),)
            parts.append(f'⟨{i}⟩')
            if t[0] == 'l' and t[4]:
                parts.append('⟨dt⟩')
    # strip the trailing name marker into a side table
    st.names = {i: c[-1][1] for i, c in st.cells.items()}
    st.cells = {i: c[:-1] for i, c in st.cells.items()}
    sk = norm(''.join(parts))
    # "x's <external link>" is a field or getter of an external struct
    for m in re.finditer(r"(?:'s?|’s) ⟨(\d+)⟩", sk):
        i = int(m.group(1))
        if st.cells[i][0] == 'X':
            st.cells[i] = ('G', 'ext', st.names.get(i, '?'))
    st.skel = sk
    st.defs, st.holes, st.lvs = [], [], set()
    st.calls, st.indirect = [], []
    st.ua = bool(re.search(r'implementation-defined|user agent may|\boptionally\b|user agents? (may|should|can)', sk))
    st.exits = bool(EXIT.search(sk)) and bool(re.search(r'\b(if|otherwise|when|unless|while)\b', sk) or st.parent)
    st.base = {int(m.group(1)) for m in re.finditer(r"⟨(\d+)⟩(?=(?:'s?|’s) ⟨\d+⟩)", sk)}

    def add(cell, kind, span, vals):
        st.defs.append((cell, kind, tuple(vals)))
        ids = ids_in(span)
        st.lvs.update(ids)
        # a write to x's A's B also changes the value held in A (weak def)
        if kind in ('field', 'collection') and len(ids) > 2:
            for j in ids[1:-1]:
                if st.cells[j][0] == 'G' and st.cells[j] != cell:
                    st.defs.append((st.cells[j], 'weak', tuple(vals)))

    # let V be <value>
    for m in re.finditer(r"\blet (?:the )?(.{0,80}?) be\b", sk):
        tgt = m.group(1)
        ids = ids_in(tgt)
        vs = [v for v in ids if st.cells[v][0] == 'L']
        vals = ids_in(region(sk, m.end()))
        if vs and len(vs) == len(ids):
            for v in vs:
                add(st.cells[v], 'local', f'⟨{v}⟩', vals)
        elif ids:
            c, k = parse_lv(st, tgt)
            if c:
                add(c, k, tgt, vals)
            else:
                st.holes.append(k)
        else:
            st.holes.append('untagged-let')
    # set LV to <value> (with chained "and LV to")
    for m in re.finditer(r"(?<!is )(?<!are )(?<!been )(?<!be )\bset ((?:(?!\bset\b|, then\b|\bis\b|\bare\b).){1,120}?) to\b", sk):
        lv = m.group(1)
        if lv.startswith('up ') or lv.startswith('aside'):
            continue
        vals = ids_in(region(sk, m.end()))
        if lv.strip() in ('it', 'them', 'this'):
            # pronoun: the previous left side in this step, else the last
            # "x's F" chain in the condition before this clause
            prev = [d for d in st.defs if d[1] in ('field', 'local', 'collection')]
            chains = list(re.finditer(r"⟨\d+⟩(?:'s ⟨\d+⟩)+|⟨\d+⟩", sk[:m.start()]))
            cand = None
            if prev:
                cand = (prev[-1][0], 'pronoun')
            elif chains:
                c, k = parse_lv(st, chains[-1].group(0))
                cand = (c, 'pronoun') if c else None
            if cand:
                add(cand[0], cand[1], '', vals)
            else:
                st.holes.append('untagged-set')
            continue
        if '⟨' in lv:
            c, k = parse_lv(st, lv)
            if c:
                add(c, k, lv, vals)
            else:
                st.holes.append(k)
        else:
            st.holes.append('untagged-set')
        tail = region(sk, m.end())
        for m2 in re.finditer(r"\band ((?:⟨\d+⟩(?:'s ⟨\d+⟩)*)) to\b", tail):
            c, k = parse_lv(st, m2.group(1))
            if c:
                add(c, k, m2.group(1), ids_in(tail[m2.end():]))
    # struct literals: whose F is X / with its F set to X / <dt>F</dt><dd>X
    for kw in ('whose', 'with its', 'with'):
        if kw in sk and re.search(r'\b(new|copy|clone|whose)\b', sk):
            seg0 = sk.find(kw)
            for m in re.finditer(r"⟨(\d+)⟩ (?:is|are|set to)\b", sk[seg0:]):
                c = st.cells[int(m.group(1))]
                if c[0] == 'G' and int(m.group(1)) not in st.lvs:
                    rest = sk[seg0 + m.end():]
                    nxt = re.search(r", (?:and )?(?:its )?⟨\d+⟩ (?:is|are|set to)\b|\.(?= |$)|;", rest)
                    add(c, 'field-init', m.group(0), ids_in(rest[:nxt.start() if nxt else len(rest)]))
            break
    dts = list(re.finditer(r"⟨(\d+)⟩⟨dt⟩", sk))
    for n, m in enumerate(dts):
        c = st.cells[int(m.group(1))]
        if c[0] == 'G' and re.search(r'\b(new|whose|with|following)\b', sk[:m.start()]):
            end = dts[n + 1].start() if n + 1 < len(dts) else len(sk)
            add(c, 'field-init', m.group(0), ids_in(sk[m.end():end]))
    # for each V of/in X
    for m in re.finditer(r"\bfor each (?:[a-z\- ]*?)?⟨(\d+)⟩ (?:of|in|from)\b", sk):
        c = st.cells[int(m.group(1))]
        if c[0] == 'L':
            add(c, 'local', f'⟨{m.group(1)}⟩', ids_in(region(sk, m.end())))
    # collection verbs
    for clause in re.split(r'(?<=\.) |; ', sk):
        cl_ids = ids_in(clause)
        for m in COLL_TO.finditer(clause):
            rest = clause[m.end():]
            mm = list(re.finditer(r"\b(?:to|into|onto) " + LV_RE, rest))
            if mm:
                c, k = parse_lv(st, mm[-1].group(1))
                tgt = ids_in(mm[-1].group(1))
                if c:
                    add(c, 'collection', mm[-1].group(1), [i for i in cl_ids if i not in tgt])
                else:
                    st.holes.append('collection-' + k)
            else:
                st.holes.append('collection-no-target')
        for m in COLL_FROM.finditer(clause):
            rest = clause[m.end():]
            mm = re.search(r"\bfrom " + LV_RE, rest) or re.match(r'\s*' + LV_RE, rest)
            if mm and '⟨' in mm.group(1):
                c, k = parse_lv(st, mm.group(1))
                tgt = ids_in(mm.group(1))
                if c:
                    add(c, 'collection', mm.group(1), [i for i in cl_ids if i not in tgt])
                else:
                    st.holes.append('collection-' + k)
            else:
                st.holes.append('collection-no-target')
        for m in COLL_SELF.finditer(clause):
            mm = re.match(r'\s*' + LV_RE, clause[m.end():])
            if mm and '⟨' in mm.group(1):
                c, k = parse_lv(st, mm.group(1))
                tgt = ids_in(mm.group(1))
                if c:
                    add(c, 'collection', mm.group(1), [i for i in cl_ids if i not in tgt])
                else:
                    st.holes.append('collection-' + k)
            elif m.group(1) not in ('replace', 'sort', 'unset', 'empty'):
                st.holes.append('collection-no-target')
    for m in re.finditer(r"\breturn\b", sk):
        add(('R', st.aid), 'return', '', ids_in(region(sk, m.end())))
    # callback parameters: "the following steps given V (and V)*"
    for m in re.finditer(r"\b(?:following |these )?(?:steps|algorithm)(?: [a-z]+)?,? given ((?:⟨\d+⟩(?:,? (?:and )?)?)+)", sk):
        for v in ids_in(m.group(1)):
            if st.cells[v][0] == 'L':
                add(st.cells[v], 'callback-param', f'⟨{v}⟩', [])
    if not st.defs and not st.holes and OTHER_W.match(sk):
        st.holes.append('other-write-verb')
    # calls with argument mapping
    order = sorted(st.cells)
    for i in order:
        c = st.cells[i]
        if c[0] != 'C':
            continue
        callee = c[1]
        pos = sk.find(f'⟨{i}⟩') + len(f'⟨{i}⟩')
        nxt = re.search(r'⟨(\d+)⟩', sk[pos:])
        end = len(sk)
        for m in re.finditer(r'⟨(\d+)⟩', sk[pos:]):
            if st.cells[int(m.group(1))][0] == 'C':
                end = pos + m.start()
                break
        se = SENT_END.search(sk, pos)
        if se and se.start() < end and not re.match(r'\s*(the following|these) steps', sk[se.end():]):
            end = se.start()
        reg = sk[pos:end]
        ps = params.get(callee, [])
        pl = [p.lower() for p in ps]
        mapping = []
        named = set()
        # named arguments: NAME set to X
        for m in re.finditer(r"(?:⟨(\d+)⟩|\b([a-z][\w]*)) set to (.*?)(?=,? (?:and )?(?:⟨\d+⟩|\b[a-z][\w]*) set to |$)", reg):
            nm = st.names.get(int(m.group(1))) if m.group(1) else m.group(2)
            nm = (nm or '').replace(' ', '').lower()
            if nm in pl:
                mapping.append((ps[pl.index(nm)], ids_in(m.group(3))))
                named.add(ps[pl.index(nm)])
                if m.group(1):
                    st.lvs.add(int(m.group(1)))
                reg = reg.replace(m.group(0), ' ')
        rest_ps = [p for p in ps if p not in named]
        chunks = [ids_in(ch) for ch in re.split(
            r",\s*and\s+|,\s*|\s+and\s+|\s+(?:given|with|from|to|using|on|for|in|at|into|against|of|as)\s+", reg)]
        chunks = [[j for j in ch if st.cells[j][0] in 'LGC'] for ch in chunks]
        chunks = [ch for ch in chunks if ch]
        if len(chunks) <= len(rest_ps):
            for p, ch in zip(rest_ps, chunks):
                mapping.append((p, ch))
            kind = 'positional'
        else:
            allids = [j for ch in chunks for j in ch]
            for p in rest_ps:
                mapping.append((p, allids))
            kind = 'fallback'
        st.calls.append((callee, mapping, kind))
    st.argids = {j for _, mp, kd in st.calls for _, ids in mp for j in ids}
    for m in re.finditer(r"\b(?:run|call|invoke|perform)\s+(?:the )?⟨(\d+)⟩", sk):
        c = st.cells[int(m.group(1))]
        if c[0] == 'L' or c[0] == 'G' and not re.search(r'⟨%s⟩(?:\'s)' % m.group(1), sk):
            st.indirect.append(int(m.group(1)))


for st in steps:
    analyse(st)


def tok_uses(st, ids, data_only=True):
    out = set()
    for i in ids:
        c = st.cells[i]
        if data_only and (i in st.base or i in st.lvs):
            continue
        if c[0] in 'LG':
            out.add(c)
        elif c[0] == 'C':
            out.add(('R', c[1]))
    return out


def all_uses(st):
    return tok_uses(st, st.cells, data_only=False)


# writers index
writers = collections.defaultdict(list)       # cell -> [(step, kind, value ids)]
callsites = collections.defaultdict(list)     # callee aid -> [(step, mapping)]
for st in steps:
    for c, k, vals in st.defs:
        # a value read through a call in the value region also reads that call's result
        writers[c].append((st, k, vals))
    for callee, mapping, kind in st.calls:
        callsites[callee].append((st, mapping))
for aid, ps in params.items():
    for st, mapping in callsites.get(aid, []):
        for p, ids in mapping:
            writers[('L', aid, p)].append((st, 'arg', tuple(ids)))


def ctrl_steps(st):
    out = []
    p = st.parent
    while p is not None:
        out.append(p)
        p = p.parent
    for e in by_alg[st.aid][:st.order]:
        if e.exits and e is not st:
            out.append(e)
    return out

# ------------------------------------------------ criteria (model-read concepts)
def G(spec, key):
    exact = index[spec].get(norm(key))
    i = exact[0] if exact else by_id[spec].get(key)
    if i is None:
        i = lookup(spec, norm(key))
    assert i is not None, (spec, key)
    return ('G', spec, i)


def R(spec, key):
    i = by_id[spec].get(key)
    if i is None or (spec, i) not in algos:
        cands = [j for j in index[spec].get(norm(key), []) if (spec, j) in algos]
        i = cands[0] if cands else lookup(spec, norm(key))
    assert (spec, i) in algos, (spec, key)
    return ('R', (spec, i))


def P(spec, key, var):
    r = R(spec, key)
    return ('L', r[1], var)


CRITERIA = [
    ('coep', G('html', 'policy-container-embedder-policy')),
    ('coep', G('html', 'embedder-policy-value')),
    ('coop', G('html', 'concept-document-coop')),
    ('coop', G('html', 'navigation-params-coop')),
    ('coop', G('html', 'coop-struct-value')),
    ('corp', R('fetch', 'cross-origin resource policy check')),
    ('corp', R('fetch', 'cross-origin resource policy internal check')),
    ('creds', R('fetch', 'cross-origin-embedder-policy allows credentials')),
    ('secure', R('html', 'secure context')),
    ('origin', G('fetch', 'concept-request-origin')),
    ('origin', G('fetch', 'concept-response-url-list')),
    ('origin', G('html', 'concept-document-origin')),
    ('origin', R('html', 'determining the origin')),
    ('akey', R('html', 'obtain-similar-origin-window-agent')),
    ('coimode', G('html', 'bcg-cross-origin-isolation')),
    ('coimode', R('html', 'obtain-browsing-context-navigation')),
    ('coicap', G('html', 'concept-settings-object-cross-origin-isolated-capability')),
    ('tainting', G('fetch', 'concept-request-response-tainting')),
    ('mode', G('fetch', 'concept-request-mode')),
    ('bcgswitch', R('html', 'check-browsing-context-group-switch-coop-value')),
    ('bcgswitch', R('html', 'check-browsing-context-group-switch-coop-value-popup')),
    ('bcgswitch', R('html', 'matching-coop')),
    ('response', G('fetch', 'concept-response-type')),
    ('response', P('fetch', 'fetch response handover', 'response')),
]


def cell_label(c):
    if c[0] == 'L':
        return f"{algos[c[1]]['name']}::{c[2]}"
    if c[0] == 'G':
        return 'ext:' + c[2] if c[1] == 'ext' else dfn_label(c[1], c[2])
    if c[0] == 'R':
        return f"RET({algos[c[1]]['name']})"
    return str(c)


PARENT = {}
DIST = {}


def slice_from(crit, control, identity=False):
    rel = {}                # cell -> concept set
    role = {}               # step -> set of roles
    via = {}                # step -> one relevant cell it writes / guards
    work = collections.deque()
    dist = {}
    sdist = DIST.setdefault((control, identity, len(crit)), {})
    for con, c in crit:
        rel.setdefault(c, set()).add(con)
        dist[c] = 0
        work.append(c)

    def push(u, cons, why=None):
        before = rel.get(u)
        if before is None:
            PARENT.setdefault(control, {})[u] = why
            dist[u] = dist[why[0]] + 1 if why else 0
            rel[u] = set(cons)
            work.append(u)
        elif not cons <= before:
            before |= cons
            work.append(u)

    while work:
        c = work.popleft()
        cons = set(rel[c])
        for st, k, vals in writers.get(c, []):
            role.setdefault(st, set()).add('arg' if k == 'arg' else 'def')
            via.setdefault(st, c)
            sdist.setdefault(st, dist[c])
            uses = tok_uses(st, [i for i in vals if k == 'arg' or i not in st.argids])
            if identity:
                # which object is written or read: base pointers and left sides too
                uses |= tok_uses(st, [i for i in st.cells if i not in st.argids], data_only=False)
            if control:
                for cs in [st] + ctrl_steps(st):
                    if cs is not st:
                        role.setdefault(cs, set()).add('control')
                        via.setdefault(cs, c)
                        sdist.setdefault(cs, dist[c])
                    uses |= tok_uses(cs, [i for i in cs.cells if i not in cs.argids], data_only=not identity)
            for u in uses:
                push(u, cons, (c, st))
    return rel, role, via


def slice_concepts(crit, **kw):
    """Per-concept slice sizes (closure steps), run separately per concept."""
    out = {}
    for con in sorted({c for c, _ in crit}):
        _, role, _ = slice_from([x for x in crit if x[0] == con], **kw)
        ctl = [key_of.get(k) for k in CONTROL_KEYS]
        out[con] = (sum(1 for st in role if (st.spec, st.line) in closure),
                    ''.join('x' if st in role else '.' for st in ctl))
    return out


# the two known omissions (positive controls)
CONTROL_KEYS = [('html', 'obtain an embedder policy', '2'), ('fetch', 'HTTP-network-or-cache fetch', '8.4')]


thin_rel, thin_role, _ = slice_from(CRITERIA, control=False)
ctrl_rel, ctrl_role, _ = slice_from(CRITERIA, control=True)
full_rel, full_role, full_via = slice_from(CRITERIA, control=True, identity=True)

# ------------------------------------------------ closure, writesets
closure = {}
for x in csv.DictReader(open(os.path.join(OUT_IN, 'closure_steps.tsv'), encoding='utf-8'), delimiter='\t'):
    closure[(x['spec'], int(x['line']))] = x
ws = {}
for x in csv.DictReader(open(WRITESETS, encoding='utf-8'), delimiter='\t'):
    ws[(x['spec'], x['algorithm'], x['step'])] = x

key_of = {}
for st in steps:
    key_of[(st.spec, algos[st.aid]['name'], st.path)] = st
in_closure = [st for st in steps if (st.spec, st.line) in closure]
closure_aids = {st.aid for st in in_closure}

# ------------------------------------------------ holes
WRITE_HOLES = {'untagged-let', 'untagged-set', 'untagged-target', 'unresolved-target', 'local?',
               'collection-no-target', 'collection-untagged-target', 'collection-unresolved-target',
               'collection-call-as-target', 'call-as-target', 'other-write-verb'}


def hole_kinds(st, rel, role):
    """Reasons the rules cannot place st's writes or the cells it reads."""
    out = [h for h in st.holes]
    if any(k == 'local?' for _, k, _ in st.defs):
        out.append('local?')
    if st.indirect:
        out.append('indirect-call')
    x = closure.get((st.spec, st.line), {})
    if not st.defs and not st.holes and not st.calls and x.get('reason') == 'prose-only':
        out.append('prose-only')
    if st in role and any(c[0] == 'U' for c in st.cells.values()):
        out.append('unresolved-link')
    if st in role and any(k == 'callback-param' and c in rel for c, k, _ in st.defs):
        out.append('callback-bound')
    return out


def holes_for(rel, role):
    rel_aids = {st.aid for st in role}
    out = []
    for st in in_closure:
        hk = hole_kinds(st, rel, role)
        if not hk:
            continue
        on = st in role or (st.aid in rel_aids and any(h in WRITE_HOLES or h in ('prose-only', 'indirect-call')
                                                        for h in hk))
        out.append((st, hk, on))
    # relevant locals with no writer at all (not a parameter, not bound by a rule)
    unbound = []
    for c in rel:
        if c[0] == 'L' and c[1] in closure_aids and not writers.get(c) and c[2] not in params.get(c[1], []):
            unbound.append(c)
    entry = [c for c in rel if c[0] == 'L' and c[2] in params.get(c[1], []) and not callsites.get(c[1])
             and c[1] in closure_aids]
    return out, unbound, entry


holes, unbound, entry = holes_for(full_rel, full_role)
holes_ctrl, unbound_ctrl, entry_ctrl = holes_for(ctrl_rel, ctrl_role)
holes_thin, unbound_thin, entry_thin = holes_for(thin_rel, thin_role)

# boundary: external calls read by a relevant step
boundary = []
for st in full_role:
    if (st.spec, st.line) not in closure:
        continue
    ext = sorted({c[1] for c in st.cells.values() if c[0] == 'X'})
    if ext:
        boundary.append((st, ext))

# ------------------------------------------------ resolution of the havoc gap rows
gap = collections.Counter()
gap_res = collections.Counter()
gap_rel = collections.Counter()
for k, x in ws.items():
    if x['status'] != 'gap':
        continue
    kind = x['write_kind'].split('-')[-1]
    gap[kind] += 1
    st = key_of.get(k)
    if st is None:
        gap_res[(kind, 'no-step')] += 1
        continue
    bad = [h for h in st.holes if h in WRITE_HOLES]
    if kind == 'local':
        ok = any(d[1] == 'local' for d in st.defs)
    elif kind == 'collection':
        ok = any(d[1] == 'collection' for d in st.defs)
    else:
        ok = bool(st.defs)
    ok = ok and not bad
    gap_res[(kind, 'resolved' if ok else 'unresolved')] += 1
    if ok:
        r = any(d[0] in full_rel for d in st.defs)
        t = any(d[0] in thin_rel for d in st.defs)
        gap_rel[(kind, 'relevant-data' if t else ('relevant-control-only' if r else 'irrelevant'))] += 1

# ------------------------------------------------ comparison with the model
MODELED = {'modeled', 'input', 'composite'}


def ws_row(st):
    return ws.get((st.spec, algos[st.aid]['name'], st.path))


def concepts_of(st, rel, via):
    cons = set()
    for c, k, _ in st.defs:
        cons |= rel.get(c, set())
    if st.calls:
        for callee, mp, _ in st.calls:
            for p, _ in mp:
                cons |= rel.get(('L', callee, p), set())
    if not cons and st in via:
        cons |= rel.get(via[st], set())
    return cons


rows = []
for st in in_closure:
    if st not in full_role:
        continue
    r = ws_row(st)
    cons = concepts_of(st, full_rel, full_via)
    rows.append({
        'spec': st.spec, 'algorithm': algos[st.aid]['name'], 'step': st.path, 'line': st.line,
        'roles': ','.join(sorted(full_role[st])),
        'slice': 'data' if st in thin_role else ('control' if st in ctrl_role else 'identity'),
        'dist': DIST[(True, False, len(CRITERIA))].get(st, ''),
        'n_concepts': len(cons), 'concepts': ','.join(sorted(cons)),
        'writes': ';'.join(sorted({cell_label(c) for c, k, _ in st.defs if c in full_rel}))[:160],
        'ws_status': r['status'] if r else '-', 'model_ref': r['model_ref'] if r else '',
        'holes': ','.join(hole_kinds(st, full_rel, full_role)),
    })

for r in rows:
    s = r['ws_status']
    if s in MODELED:
        r['verdict'] = 'modeled'
    elif s in ('outscope', 'notread', 'nocone'):
        r['verdict'] = 'excluded:' + s
    elif s in ('unmodeled', 'unmodeled-guard'):
        r['verdict'] = 'unmodeled-known'
    elif s == 'gap':
        r['verdict'] = 'unmodeled-gap'
    elif s == 'auto-unreviewed':
        r['verdict'] = 'unmodeled-unreviewed'
    else:
        r['verdict'] = 'unmodeled-nonwrite'


def group(r):
    """Coarse group of an unmodeled relevant step (author's buckets, by algorithm)."""
    a = r['algorithm'].lower()
    buckets = [
        ('url-and-parsing', r'url|pars|serializ|integer|floating|structured|mime|header|range|srcset|sizes|encod|decod|infra'),
        ('redirect-and-network', r'redirect|network|connection|cache|preflight|cors|http fetch|scheme fetch|partition|port|cookie|quota|data: url'),
        ('fetch-core', r'^fetch$|main fetch|handover|override|populate request|determine the environment|tao|nosniff|blocked'),
        ('policy-coep-coop', r'policy|opener|embedder|coop|coep|sandbox|csp|adherence|x-frame'),
        ('navigation-history', r'navigat|history|traverse|session|unload|beforeunload|pageswap|activate|fragment|scroll|entry|entries|document state|snapshot'),
        ('document-and-bc-creation', r'browsing context|document|realm|agent|environment|origin|site|load'),
        ('script-and-events', r'script|event|focus|microtask|parser|speculation|import map|exception|link|preload|download|lazy|iframe|activation'),
    ]
    for name, rx in buckets:
        if re.search(rx, a):
            return name
    return 'other'


for r in rows:
    r['group'] = group(r) if r['verdict'].startswith('unmodeled') else ''

os.makedirs(OUTDIR, exist_ok=True)
cols = ['spec', 'algorithm', 'step', 'line', 'roles', 'slice', 'dist', 'n_concepts', 'concepts', 'writes',
        'ws_status', 'model_ref', 'verdict', 'group', 'holes']
with open(os.path.join(OUTDIR, 'closed-list.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, cols, delimiter='\t', lineterminator='\n')
    w.writeheader()
    for r in sorted(rows, key=lambda r: (r['spec'], r['algorithm'], r['line'])):
        w.writerow(r)

with open(os.path.join(OUTDIR, 'flows.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['spec', 'algorithm', 'step', 'line', 'defs', 'n_value_uses', 'calls', 'holes', 'slice'])
    for st in in_closure:
        w.writerow([st.spec, algos[st.aid]['name'], st.path, st.line,
                    ';'.join(f"{k}:{cell_label(c)}" for c, k, _ in st.defs)[:240],
                    sum(len(tok_uses(st, v)) for _, _, v in st.defs),
                    ';'.join(f"{algos[c]['name']}[{kd}]" for c, _, kd in st.calls)[:200],
                    ','.join(hole_kinds(st, full_rel, full_role)),
                    ','.join(sorted(full_role.get(st, ())))])

with open(os.path.join(OUTDIR, 'holes.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['spec', 'algorithm', 'step', 'line', 'hole_kinds', 'on_relevant_path_ctrl', 'in_ctrl_slice',
                'ctrl_dist', 'detail'])
    on_ctrl = {st: o for st, _, o in holes_ctrl}
    for st, hk, o in holes:
        # unresolved link labels, cut to 4 words so that no spec sentence is copied
        det = ';'.join(sorted({' '.join(st.names.get(i, '').split()[:4])
                               for i, c in st.cells.items() if c[0] == 'U'}))[:80]
        w.writerow([st.spec, algos[st.aid]['name'], st.path, st.line, ','.join(hk),
                    'yes' if on_ctrl.get(st) else 'no', 'yes' if st in ctrl_role else 'no',
                    DIST[(True, False, len(CRITERIA))].get(st, ''), det])
    for c in sorted(unbound_ctrl, key=cell_label):
        w.writerow([c[1][0], algos[c[1]]['name'], '-', '-', 'unbound-relevant-local', 'yes', '-', '', c[2]])

# ------------------------------------------------ summary
S = {}
S['steps_parsed_total'] = len(steps)
S['steps_without_tokens'] = missing_tokens
S['closure_steps_matched'] = len(in_closure)
S['closure_steps_tsv'] = sum(1 for k, x in closure.items() if x['step'] != '-')
S['closure_algorithms'] = len(closure_aids)
S['closure_algorithms_with_params'] = sum(1 for a in closure_aids if params[a])
cs_kinds = collections.Counter(kd for st in in_closure for _, _, kd in st.calls)
S['closure_call_sites_by_mapping'] = dict(cs_kinds)
S['criteria'] = [(con, cell_label(c), len(writers.get(c, []))) for con, c in CRITERIA]
S['relevant_cells_thin'] = len(thin_rel)
S['relevant_cells_full'] = len(full_rel)
S['slice_thin_closure'] = sum(1 for st in thin_role if (st.spec, st.line) in closure)
S['slice_full_closure'] = len(rows)
S['slice_full_outside_closure'] = sum(1 for st in full_role if (st.spec, st.line) not in closure)
S['slice_algorithms_closure'] = len({(r['spec'], r['algorithm']) for r in rows})
S['roles'] = dict(collections.Counter(r['roles'] for r in rows))
S['verdicts_full'] = dict(collections.Counter(r['verdict'] for r in rows))
S['slice_ctrl_closure'] = sum(1 for st in ctrl_role if (st.spec, st.line) in closure)
S['verdicts_thin'] = dict(collections.Counter(r['verdict'] for r in rows if r['slice'] == 'data'))
S['verdicts_ctrl'] = dict(collections.Counter(r['verdict'] for r in rows if r['slice'] in ('data', 'control')))
S['unmodeled_groups_thin'] = dict(collections.Counter(
    r['group'] for r in rows if r['slice'] == 'data' and r['verdict'].startswith('unmodeled')))
S['per_concept_thin'] = slice_concepts(CRITERIA, control=False)
dd = DIST[(True, False, len(CRITERIA))]
S['ctrl_dist_hist'] = dict(sorted(collections.Counter(
    min(v, 10) for st, v in dd.items() if (st.spec, st.line) in closure).items()))
S['ctrl_unmodeled_by_dist'] = dict(sorted(collections.Counter(
    min(r['dist'], 10) for r in rows if r['dist'] != '' and r['verdict'].startswith('unmodeled')).items()))
S['ctrl_unmodeled_dist_le2_groups'] = dict(collections.Counter(
    r['group'] for r in rows if r['dist'] != '' and r['dist'] <= 2 and r['verdict'].startswith('unmodeled')))
S['ctrl_unmodeled_dist_le2_algos'] = collections.Counter(
    r['algorithm'] for r in rows if r['dist'] != '' and r['dist'] <= 2 and r['verdict'].startswith('unmodeled')).most_common(40)
S['per_concept_ctrl'] = slice_concepts(CRITERIA, control=True)
S['unmodeled_groups_full'] = dict(collections.Counter(r['group'] for r in rows if r['verdict'].startswith('unmodeled')))
S['n_concepts_hist_full'] = dict(collections.Counter(r['n_concepts'] for r in rows))
S['gap_rows'] = dict(gap)
S['gap_resolution'] = {f'{a}/{b}': v for (a, b), v in gap_res.items()}
S['gap_relevance'] = {f'{a}/{b}': v for (a, b), v in gap_rel.items()}


def hsum(hs):
    hk, on = collections.Counter(), collections.Counter()
    for st, kinds, o in hs:
        for k in set(kinds):
            hk[k] += 1
            if o:
                on[k] += 1
    return len(hs), sum(1 for h in hs if h[2]), dict(hk), dict(on)


for lab, hs, ub, en in (('full', holes, unbound, entry), ('ctrl', holes_ctrl, unbound_ctrl, entry_ctrl),
                        ('thin', holes_thin, unbound_thin, entry_thin)):
    n, non, hk, on = hsum(hs)
    S[f'holes_{lab}'] = {'steps_with_hole_closure': n, 'on_relevant_paths': non, 'kinds_closure': hk,
                         'kinds_on_path': on, 'unbound_relevant_locals': len(ub),
                         'entry_params_without_callers': len(en)}
S['unbound_examples'] = sorted(cell_label(c) for c in unbound)[:40]
S['entry_params'] = sorted(cell_label(c) for c in entry)[:40]
S['boundary_steps_in_slice'] = len(boundary)
S['boundary_targets'] = collections.Counter(re.sub(r'^https?://([^/#]+).*', r'\1', u)
                                            for _, e in boundary for u in e).most_common(12)
ws_read = [x for x in ws.values() if x['status'] in ('modeled', 'unmodeled', 'composite', 'input', 'unmodeled-guard')]
missed = []
for x in ws_read:
    st = key_of.get((x['spec'], x['algorithm'], x['step']))
    if st is None or st not in full_role:
        missed.append((x['algorithm'], x['step'], x['status'], x['concept'],
                       'ctrl' if st in ctrl_role else '', ','.join(st.holes) if st else 'nostep'))
S['havoc_read_rows'] = len(ws_read)
S['havoc_read_rows_missed_by_full_slice'] = len(missed)
S['havoc_read_rows_in_thin_slice'] = sum(1 for x in ws_read if key_of.get((x['spec'], x['algorithm'], x['step'])) in thin_role)
S['havoc_read_rows_in_ctrl_slice'] = sum(1 for x in ws_read if key_of.get((x['spec'], x['algorithm'], x['step'])) in ctrl_role)
S['missed'] = sorted(missed)
for k in [('html', 'obtain an embedder policy', '2'), ('fetch', 'HTTP-network-or-cache fetch', '8.4'),
          ('fetch', 'HTTP-network-or-cache fetch', '8.3')]:
    st = key_of.get(k)
    S['control ' + '/'.join(k)] = {'full_roles': sorted(full_role.get(st, [])), 'thin': st in thin_role,
                                   'ctrl_dist': DIST[(True, False, len(CRITERIA))].get(st),
                                   'thin_dist': DIST[(False, False, len(CRITERIA))].get(st),
                                   'ctrl': st in ctrl_role,
                                   'defs': [(kk, cell_label(c)) for c, kk, _ in st.defs],
                                   'concepts': sorted(concepts_of(st, full_rel, full_via))}
json.dump(S, open(os.path.join(OUTDIR, 'summary.json'), 'w'), indent=1, default=str)
print(json.dumps({k: v for k, v in S.items() if k not in ('missed', 'unbound_examples', 'entry_params')},
                 indent=1, default=str))

if os.environ.get('DF_DEBUG'):
    top = sorted(((len(writers.get(c, [])), cell_label(c)) for c in thin_rel), reverse=True)[:30]
    for n, l in top:
        print(n, l)
    for want in os.environ.get('DF_WHY', '').split('|'):
        if not want:
            continue
        sp, al, sn = want.split('/')
        st = key_of.get((sp, al, sn))
        c = next((d[0] for d in st.defs if d[0] in thin_rel), None) if st else None
        print('WHY', want, cell_label(c) if c else None)
        n = 0
        while c is not None and n < 25:
            w = PARENT[False].get(c)
            if not w:
                break
            c, s2 = w
            print('    <-', cell_label(c), 'via', algos[s2.aid]['name'], s2.path)
            n += 1
    for want in os.environ.get('DF_SHOW', '').split('|'):
        if not want:
            continue
        sp, al, sn = want.split('/')
        st = key_of.get((sp, al, sn))
        if st is None:
            print('no step', want)
            continue
        print('==', want, st.line, st.skel[:600])
        print('   cells', {i: cell_label(c) if c[0] in 'LGR' else c for i, c in st.cells.items()})
        print('   defs', [(k, cell_label(c), v) for c, k, v in st.defs], 'holes', st.holes,
              'roles', full_role.get(st), 'thin', st in thin_role,
              'calls', [(algos[c]['name'], m, kd) for c, m, kd in st.calls])
