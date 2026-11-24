"""Single-rater review of paths.tsv, precision, and recall.

    python3 -I review.py <paths.tsv> [<reference.tsv>] [<previous sinkpaths_reviewed.tsv>]

Adds the columns kept, category and key to paths.tsv (in place). The
judgement is by structure (one rater, the author of boundary.py), plus a
per-row table for rows that the structure does not decide. It says only
whether a row is a site where response bytes or a result enter or are
stored for reuse; it says nothing about which checks a path passes.
<reference.tsv> (kept outside the repository) holds the hand reference paths
as row matchers; only counts are printed. <previous ...> is the 2026-11-22
inventory table (outside the repository); only counts are printed.
"""
import collections
import csv
import re
import sys

P = sys.argv[1]
REF = sys.argv[2] if len(sys.argv) > 2 else None
PREV = sys.argv[3] if len(sys.argv) > 3 else None

# structure label -> (kept, category, key)
STRUCT = {
    'map of preloaded resources': ('y', 'preload map', 'preload key (URL, destination, mode, credentials mode)'),
    'list of available images': ('y', 'image list', '(absolute URL, CORS mode, origin unless No CORS)'),
    'module map': ('y', 'module map', '(URL, module type)'),
    'module responses map': ('y', 'worklet module responses', 'request URL'),
    'determine the HTTP cache partition': ('y', 'HTTP cache', 'network partition key; selection per HTTP Caching'),
    'preloaded response candidate (for fetch params)': ('y', 'preloaded response candidate', 'per fetch params; filled from the preload map'),
    'document (for document state)': ('y', 'back/forward cache', "session history entry's document state"),
    'commit early hints (for navigation params)': ('y', 'early hints', 'navigation params; commits into the new Document preload map'),
    'owner set': ('n', 'not a result store (worker owners)', ''),
    'scoped document set': ('n', 'not a result store (custom element registry)', ''),
    'image map': ('n', 'not a result store (area map)', ''),
    'ancestor origins list': ('n', 'not a result store (origins)', ''),
    'internal response (for filtered response)': ('n', 'flow field, not reuse', ''),
    'body info (for response)': ('n', 'flow field, not reuse', ''),
    'response (for response)': ('n', 'flow field (Response object), not reuse', ''),
    'response (for navigation params)': ('n', 'flow field, not reuse', ''),
    'document (for link processing options)': ('n', 'flow field (target Document), not reuse', ''),
    'on document ready (for link processing options)': ('n', 'flow field, not reuse', ''),
    'displayed document (for changing navigable continuation state)': ('n', 'flow field, not reuse', ''),
    'Fetch options (for script)': ('n', 'flow field (options), not reuse', ''),
}
# fetch-call rows that link to fetch but do not call it (abort and cancel steps)
NOT_CALL = {('abort the image request', '3'), ('abort', '2')}
# exits that hand a response or its bytes across the spec boundary
EXIT_KEEP = re.compile(r'#(prefetch-record|prefetch-record-still-being-speculated|'
                       r'start-a-referrer-initiated-navigational-prefetch|blob-url-obtain-object)$')

rows = list(csv.DictReader(open(P, encoding='utf-8'), delimiter='\t'))
for r in rows:
    k, cat, key = 'n', '', ''
    s = r['structure_or_callee']
    if r['kind'] == 'fetch-call':
        k, cat = ('n', 'links to fetch, no call') if (r['algorithm'], r['step']) in NOT_CALL else ('y', 'fetch call site')
    elif r['kind'] == 're-entry':
        k, cat = 'y', 'fetch-internal re-entry'
    elif r['kind'] in ('exit-call', 'exit-response'):
        if r['kind'] == 'exit-response' and r['algorithm'] == 'HTTP fetch':
            k, cat = 'y', 'other-spec response (service worker)'
        elif EXIT_KEEP.search(s):
            k, cat = 'y', 'other-spec store or object'
        else:
            k, cat = 'n', 'other-spec call, no response'
    else:
        parts = [x.strip() for x in s.split(';')]
        js = [STRUCT[x] for x in parts if x in STRUCT]
        assert len(js) == len(parts), s
        kept = [j for j in js if j[0] == 'y']
        if kept:
            k, cat, key = kept[0]
        else:
            k, cat = 'n', js[0][1]
    r.update(kept=k, category=cat, key=key)
cols = list(rows[0].keys())
with open(P, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter='\t', lineterminator='\n')
    w.writeheader()
    w.writerows(rows)


def group(r):
    k = r['kind']
    return 'fetch-call' if k == 'fetch-call' else 're-entry' if k == 're-entry' else \
        'exit' if k.startswith('exit') else 'container (R2d)' if r['rule'].startswith('R2d') else 'field (R2f)'


c = collections.Counter((group(r), r['kept']) for r in rows)
for gname in ('fetch-call', 're-entry', 'container (R2d)', 'field (R2f)', 'exit'):
    n, y = c[(gname, 'y')] + c[(gname, 'n')], c[(gname, 'y')]
    print(f'{gname}: rows {n} kept {y} precision {100 * y / n:.0f}%' if n else f'{gname}: 0')
reuse = [r for r in rows if group(r) in ('container (R2d)', 'field (R2f)')]
print('reuse (R2d+R2f): rows', len(reuse), 'kept', sum(r['kept'] == 'y' for r in reuse),
      f"precision {100 * sum(r['kept'] == 'y' for r in reuse) / len(reuse):.0f}%")
st = collections.Counter()
for x in STRUCT:
    st[STRUCT[x][0]] += 1
print('structures discovered (containers, fields, cache-returning algorithms) judged', dict(st))
print('kept categories', dict(collections.Counter(r['category'] for r in rows if r['kept'] == 'y')))

if REF:
    refs = list(csv.DictReader(open(REF, encoding='utf-8'), delimiter='\t'))
    hit, inc = 0, 0
    for x in refs:
        m = [r for r in rows if re.search(x['kind_re'], r['kind']) and re.search(x['algorithm_re'], r['algorithm'])
             and re.search(x['structure_re'], r['structure_or_callee'])]
        hit += bool(m)
        inc += x['in_corpus'] == 'y'
        x['found'] = bool(m)
    print(f'reference paths {len(refs)}, in corpus {inc}; found {hit} '
          f'(in corpus {sum(x["found"] for x in refs if x["in_corpus"] == "y")}, '
          f'outside corpus as exit rows {sum(x["found"] for x in refs if x["in_corpus"] != "y")})')

if PREV:
    prev = list(csv.DictReader(open(PREV, encoding='utf-8'), delimiter='\t'))
    have = {(r['spec'], r['algorithm'], r['step']) for r in rows}
    kept_have = {(r['spec'], r['algorithm'], r['step']) for r in rows if r['kept'] == 'y'}
    for kind in ('fetch-call', 'reuse'):
        pk = [r for r in prev if r['kind'] == kind and r['keep'] == 'y' and r['rule'] != 'hand']
        found = sum((r['spec'], r['algorithm'], r['step']) in kept_have for r in pk)
        print(f'previous inventory {kind} kept rows {len(pk)}: also kept here {found}')
        if kind == 'reuse':
            by = collections.Counter((r['category'].split(' (')[0], (r['spec'], r['algorithm'], r['step']) in kept_have) for r in pk)
            print('  by previous category (category, found here): ', dict(sorted(by.items())))
    ph = [r for r in prev if r['rule'] == 'hand']
    print('previous hand-only rows', len(ph))
