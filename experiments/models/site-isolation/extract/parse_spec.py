"""Parse a WHATWG spec source (Wattsi 'source' or Bikeshed .bs) into
algorithm definitions with nested step trees anchored to source lines.

usage: python3 -I parse_spec.py <html|bikeshed> <input> <output.json>
"""
import sys, re, json

mode, inp, outp = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(inp, encoding='utf-8').read()

# strip comments, keep newlines so line numbers stay valid
src = re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), src, flags=re.S)

if mode == 'bikeshed':
    # Bikeshed shorthands -> explicit <a> tags. [=for/term|text=]
    def sh(m):
        body = m.group(1)
        disp = None
        if '|' in body:
            body, disp = body.split('|', 1)
        f = None
        if '/' in body and not body.startswith('/'):
            f, body = body.rsplit('/', 1)
        attrs = ' lt="%s"' % body
        if f:
            attrs += ' for="%s"' % f
        return '<a%s>%s</a>' % (attrs, disp or body)
    src = re.sub(r'\[=([^\]=\n]+?)=\]', sh, src)

line_starts = [0]
for m in re.finditer('\n', src):
    line_starts.append(m.end())
import bisect
def lineno(pos):
    return bisect.bisect_right(line_starts, pos)

ATTR = re.compile(r'''([^\s=/>]+|/)(?:\s*=\s*("[^"]*"|'[^']*'|[^\s>]+))?''')
def parse_attrs(s):
    d = {}
    for m in ATTR.finditer(s):
        k = m.group(1)
        v = m.group(2)
        if v is None:
            v = ''
        elif v[:1] in '"\'':
            v = v[1:-1]
        d[k.lower()] = re.sub(r'\s+', ' ', v).strip()
    return d

TAG = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>')
RAW = {'pre', 'xmp', 'script', 'style', 'svg', 'math'}

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def unent(s):
    return (s.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
             .replace('&nbsp;', ' ').replace('&amp;', '&').replace('&mdash;', '-')
             .replace('&#x2014;', '-').replace('&rsquo;', "'"))

dfns = []          # all definitions
algos = []         # algorithm blocks
prose_algos = []   # <div algorithm> without any <ol>
links_global = 0

BLOCK_CLOSES_P = {'p', 'li', 'ol', 'ul', 'dl', 'div', 'pre', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'dt', 'dd'}

# state
div_stack = []      # dicts: {'algo': bool, 'owner': dfnidx or None, 'attr': str, 'note': bool, 'start': line}
list_stack = []     # dicts: {'kind': 'ol'/'ul'/'dl', 'cur': step or None, 'parent': step or None, 'block': algo-block}
note_p = False      # inside <p class=note> (implicitly closed)
open_dfn = None     # [attrs, textparts, pos, in_step]
open_links = []     # [tag, attrs, textparts, step]
last_dfn_toplevel = None   # dfn index eligible as owner of next top-level ol
last_heading_dfn = None
pending_heading = None      # [attrs, textparts, pos] for <hN dfn>

def cur_step():
    for e in reversed(list_stack):
        if e['kind'] == 'ol':
            return e['cur']
    return None

def in_note():
    return note_p or any(d['note'] for d in div_stack)

def new_block(pos):
    # determine owner for a top-level <ol>
    owner = None
    algo_div = None
    for d in reversed(div_stack):
        if d['algo']:
            algo_div = d
            break
    if algo_div is not None:
        owner = algo_div['owner']
        if owner is None and algo_div['attr']:
            owner = ('attr', algo_div['attr'])
        key = ('div', id(algo_div))
    else:
        owner = last_dfn_toplevel
        key = ('ol', pos)
    blk = {'owner': owner, 'line': lineno(pos), 'steps': [], 'divkey': key,
           'in_algo_div': algo_div is not None}
    if algo_div is not None:
        algo_div.setdefault('blocks', []).append(blk)
    algos.append(blk)
    return blk

def add_text(t, raw_pos):
    st = cur_step()
    if st is not None:
        if in_note():
            st['note_text'].append(t)
        else:
            st['text'].append(t)
    if open_dfn is not None:
        open_dfn[1].append(t)
    if pending_heading is not None:
        pending_heading[1].append(t)
    for L in open_links:
        L[2].append(t)

def close_li(entry):
    entry['cur'] = None

def close_note_p():
    global note_p
    note_p = False

pos = 0
n = len(src)
while True:
    m = TAG.search(src, pos)
    if not m:
        add_text(unent(src[pos:]), pos)
        break
    if m.start() > pos:
        add_text(unent(src[pos:m.start()]), pos)
    closing, name, rest = m.group(1) == '/', m.group(2).lower(), m.group(3)
    attrs = parse_attrs(rest) if not closing else {}
    pos = m.end()
    if not closing and name in RAW:
        end = re.compile(r'</%s\s*>' % name, re.I).search(src, pos)
        if end:
            pos = end.end()
        continue
    if not closing and name in BLOCK_CLOSES_P and note_p:
        close_note_p()
    if closing and name == 'p' and note_p:
        close_note_p()
        continue
    if not closing:
        cls = attrs.get('class', '')
        if name == 'p' and re.search(r'\b(note|example|warning|XXX|domintro)\b', cls):
            note_p = True
        if name == 'div':
            div_stack.append({'algo': 'algorithm' in attrs, 'attr': attrs.get('algorithm', ''),
                              'owner': None,
                              'note': bool(re.search(r'\b(note|example|warning|domintro|status)\b', cls)),
                              'start': lineno(m.start())})
        elif name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            last_dfn_toplevel = None
            if 'dfn' in attrs:
                pending_heading = [attrs, [], m.start()]
        elif name == 'dfn':
            open_dfn = [attrs, [], m.start(), cur_step() is not None]
        elif (mode == 'html' and (name in ('span', 'a') or name in ('code', 'i') and 'data-x' in attrs)) or (name == 'a' and mode == 'bikeshed'):
            open_links.append([name, attrs, [], cur_step(), in_note(), m.start()])
        elif name == 'ol':
            parent = cur_step()
            if parent is None and not any(e['kind'] == 'ol' for e in list_stack):
                blk = new_block(m.start())
            else:
                blk = None
                for e in reversed(list_stack):
                    if e['kind'] == 'ol':
                        blk = e['block']
                        break
            list_stack.append({'kind': 'ol', 'cur': None, 'parent': parent, 'block': blk,
                               'in_note': in_note()})
        elif name in ('ul', 'dl'):
            list_stack.append({'kind': name, 'cur': None, 'parent': None, 'block': None})
        elif name == 'li':
            if list_stack and list_stack[-1]['kind'] == 'ol':
                e = list_stack[-1]
                parent = e['parent']
                siblings = parent['children'] if parent else e['block']['steps']
                step = {'line': lineno(m.start()), 'text': [], 'note_text': [], 'links': [],
                        'children': [], 'in_note': e.get('in_note', False)}
                siblings.append(step)
                e['cur'] = step
    else:
        if name == 'div':
            if div_stack:
                dd = div_stack.pop()
                if dd['algo'] and not dd.get('blocks'):
                    prose_algos.append({'owner': dd['owner'], 'owner_attr': dd['attr'], 'line': dd['start'], 'links': dd.get('prose_links', [])})
        elif name == 'dfn' and open_dfn is not None:
            a, parts, p0, in_step = open_dfn
            open_dfn = None
            text = norm(''.join(parts))
            d = {'text': text, 'attrs': a, 'line': lineno(p0), 'in_step': in_step, 'idx': len(dfns)}
            if 'data-x' not in a:
                inner = re.fullmatch(r'<dfn[^>]*>\s*<(?:code|span)[^>]*\bdata-x="([^"]*)"[^>]*>[^<]*</(?:code|span)>\s*', src[p0:m.start()])
                if inner and inner.group(1):
                    a['data-x'] = re.sub(r'\s+', ' ', inner.group(1)).strip()
            dfns.append(d)
            for dd in reversed(div_stack):
                if dd['algo']:
                    if dd['owner'] is None and not in_step:
                        dd['owner'] = d['idx']
                    break
            if not in_step and not list_stack:
                last_dfn_toplevel = d['idx']
        elif name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6') and pending_heading is not None:
            a, parts, p0 = pending_heading
            pending_heading = None
            text = norm(''.join(parts))
            d = {'text': text, 'attrs': a, 'line': lineno(p0), 'in_step': False, 'idx': len(dfns),
                 'heading': True}
            dfns.append(d)
            for dd in reversed(div_stack):
                if dd['algo']:
                    if dd['owner'] is None:
                        dd['owner'] = d['idx']
                    break
            last_dfn_toplevel = d['idx']
        elif open_links and open_links[-1][0] == name and name in ('span', 'a', 'code', 'i'):
            tag, a, parts, st, innote, p0 = open_links.pop()
            text = norm(''.join(parts))
            if st is not None and 'subdfn' not in a:
                off = len(norm(''.join(st['text']))) - len(text)
                st['links'].append({'tag': tag, 'attrs': a, 'text': text, 'note': innote, 'off': off,
                                    'line': lineno(p0)})
            if st is None and 'subdfn' not in a and not innote:
                for dd in reversed(div_stack):
                    if dd['algo']:
                        dd.setdefault('prose_links', []).append({'tag': tag, 'attrs': a, 'text': text, 'note': False, 'off': -1, 'line': lineno(p0)})
                        break
            if tag == 'span' and 'subdfn' in a:
                dfns.append({'text': text, 'attrs': a, 'line': lineno(p0), 'in_step': False,
                             'idx': len(dfns), 'subdfn': True})
        elif name == 'ol':
            while list_stack and list_stack[-1]['kind'] != 'ol':
                list_stack.pop()
            if list_stack:
                list_stack.pop()
            if not any(e['kind'] == 'ol' for e in list_stack):
                last_dfn_toplevel = None
        elif name in ('ul', 'dl'):
            while list_stack and list_stack[-1]['kind'] not in (name,):
                if list_stack[-1]['kind'] == 'ol':
                    break
                list_stack.pop()
            if list_stack and list_stack[-1]['kind'] == name:
                list_stack.pop()
        elif name == 'li':
            pass  # keep li open until next li / </ol> (handles implicit closing uniformly)

def finish(steps):
    out = []
    for s in steps:
        out.append({'line': s['line'], 'text': norm(''.join(s['text'])),
                    'note_text': norm(''.join(s['note_text']))[:300],
                    'in_note': s['in_note'],
                    'links': s['links'], 'children': finish(s['children'])})
    return out

# merge blocks per owner
out_algos = []
for b in algos:
    o = b['owner']
    out_algos.append({'owner': o if not isinstance(o, tuple) else None,
                      'owner_attr': o[1] if isinstance(o, tuple) else None,
                      'line': b['line'], 'in_algo_div': b['in_algo_div'],
                      'steps': finish(b['steps'])})

json.dump({'mode': mode, 'dfns': dfns, 'blocks': out_algos, 'prose_algos': prose_algos}, open(outp, 'w'))
print('dfns', len(dfns), 'ol-blocks', len(out_algos),
      'prose_algos', len(prose_algos), 'owned', sum(1 for b in out_algos if b['owner'] is not None or b['owner_attr']))
