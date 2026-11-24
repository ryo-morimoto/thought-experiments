"""Scan a WHATWG spec source into per-step token sequences.

Companion to ../extract/parse_spec.py: the same list/note state machine, but
each step keeps a token list instead of plain text, so that <var> names,
cross-reference links and <dt> struct-field markers survive.

Token kinds:
  ('t', text)                       plain text
  ('v', name)                       <var>name</var> (or Bikeshed |name|)
  ('l', tag, attrs, text, in_dt)    cross-reference link

Returns {line_of_li: [tokens]} plus, for every <dfn>, the tokens between it
and the next <ol> (the algorithm preamble, used for parameters).

Imported by dataflow.py; reads only the file it is given.
"""
import bisect
import re

ATTR = re.compile(r'''([^\s=/>]+|/)(?:\s*=\s*("[^"]*"|'[^']*'|[^\s>]+))?''')
TAG = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)((?:[^>"\']|"[^"]*"|\'[^\']*\')*)>')
RAW = {'pre', 'xmp', 'script', 'style', 'svg', 'math'}
BLOCK_CLOSES_P = {'p', 'li', 'ol', 'ul', 'dl', 'div', 'pre', 'table',
                  'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'dt', 'dd'}


def parse_attrs(s):
    d = {}
    for m in ATTR.finditer(s):
        v = m.group(2)
        if v is None:
            v = ''
        elif v[:1] in '"\'':
            v = v[1:-1]
        d[m.group(1).lower()] = re.sub(r'\s+', ' ', v).strip()
    return d


def unent(s):
    return (s.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
             .replace('&nbsp;', ' ').replace('&amp;', '&').replace('&mdash;', '-')
             .replace('&#x2014;', '-').replace('&rsquo;', "'"))


def preprocess(src, mode):
    src = re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), src, flags=re.S)
    if mode == 'bikeshed':
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
        # Bikeshed variable shorthand |name|
        src = re.sub(r'(?<![|\w])\|([A-Za-z][\w]*(?: [\w]+)?)\|(?![|\w])', r'<var>\1</var>', src)
    return src


def scan(path, mode):
    src = preprocess(open(path, encoding='utf-8').read(), mode)
    starts = [0] + [m.end() for m in re.finditer('\n', src)]

    def lineno(p):
        return bisect.bisect_right(starts, p)

    steps = {}          # li line -> tokens
    preamble = {}       # dfn line -> tokens up to next <ol>
    open_pre = []       # list of [dfn line, tokens]
    para = []           # tokens of the current paragraph outside steps (round 2: the
                        # preamble also includes the words before the dfn)
    div_stack, list_stack = [], []
    note_p = False
    in_var = None
    links = []          # open links: [tag, attrs, parts, step_tokens]
    in_dt = 0

    def cur():
        for e in reversed(list_stack):
            if e['kind'] == 'ol':
                return e['cur']
        return None

    def in_note():
        return note_p or any(d['note'] for d in div_stack)

    def emit(tok):
        st = cur()
        if st is not None and not in_note():
            st.append(tok)
        if not in_note():
            for p in open_pre:
                p[1].append(tok)
            if st is None:
                para.append(tok)

    pos = 0
    while True:
        m = TAG.search(src, pos)
        text = unent(src[pos:m.start()] if m else src[pos:])
        if text:
            if in_var is not None:
                in_var.append(text)
            elif links:
                links[-1][2].append(text)
            else:
                emit(('t', text))
        if not m:
            break
        closing, name, rest = m.group(1) == '/', m.group(2).lower(), m.group(3)
        attrs = parse_attrs(rest) if not closing else {}
        pos = m.end()
        if not closing and name in RAW:
            e = re.compile(r'</%s\s*>' % name, re.I).search(src, pos)
            if e:
                pos = e.end()
            continue
        if not closing and name in BLOCK_CLOSES_P and note_p:
            note_p = False
        if closing and name == 'p' and note_p:
            note_p = False
            continue
        if not closing and name in ('dd', 'li', 'p', 'dl', 'ol', 'ul'):
            in_dt = 0
        if not closing and name in ('p', 'dt', 'dd', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div') and cur() is None:
            para = []
        if not closing:
            cls = attrs.get('class', '')
            if name == 'p' and re.search(r'\b(note|example|warning|XXX|domintro)\b', cls):
                note_p = True
            if name == 'div':
                div_stack.append({'note': bool(re.search(r'\b(note|example|warning|domintro|status)\b', cls))})
            elif name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                open_pre.clear()
            elif name == 'dfn':
                if not cur():
                    open_pre.append([lineno(m.start()), list(para)])
                    del open_pre[:-30]
            elif name == 'var':
                in_var = []
            elif name == 'dt':
                in_dt = 1
            elif (mode == 'html' and (name in ('span', 'a') or name in ('code', 'i') and 'data-x' in attrs)) \
                    or (name == 'a' and mode == 'bikeshed'):
                links.append([name, attrs, []])
            elif name == 'ol':
                parent = cur()
                if parent is None and not any(e['kind'] == 'ol' for e in list_stack):
                    for p in open_pre:
                        preamble[p[0]] = p[1]
                    open_pre.clear()
                list_stack.append({'kind': 'ol', 'cur': None})
            elif name in ('ul', 'dl'):
                list_stack.append({'kind': name, 'cur': None})
            elif name == 'li':
                if list_stack and list_stack[-1]['kind'] == 'ol':
                    tok = []
                    steps[lineno(m.start())] = tok
                    list_stack[-1]['cur'] = tok
        else:
            if name in ('dt', 'dl'):
                in_dt = 0
            if name == 'div':
                if div_stack:
                    div_stack.pop()
            elif name == 'var' and in_var is not None:
                v = re.sub(r'\s+', ' ', ''.join(in_var)).strip()
                in_var = None
                if links:
                    links[-1][2].append(v)
                else:
                    emit(('v', v))
            elif links and links[-1][0] == name and name in ('span', 'a', 'code', 'i'):
                tag, a, parts = links.pop()
                t = re.sub(r'\s+', ' ', ''.join(parts)).strip()
                tok = ('l', tag, a, t, in_dt > 0)
                if links:
                    links[-1][2].append(t)
                else:
                    emit(tok)
            elif name == 'ol':
                while list_stack and list_stack[-1]['kind'] != 'ol':
                    list_stack.pop()
                if list_stack:
                    list_stack.pop()
            elif name in ('ul', 'dl'):
                while list_stack and list_stack[-1]['kind'] != name:
                    if list_stack[-1]['kind'] == 'ol':
                        break
                    list_stack.pop()
                if list_stack and list_stack[-1]['kind'] == name:
                    list_stack.pop()
    return steps, preamble
