"""Spot-check: find target algorithm/step, show classification, and whether
closure from the other roots (target removed from roots) reaches it, with path.
usage: python3 -I spot.py <outdir> <algorithm name> <step line>"""
import sys, pickle, collections
OUT, NAME, LINE = sys.argv[1], sys.argv[2], int(sys.argv[3])
S = pickle.load(open(OUT + '/state.pkl', 'rb'))
A = S['algos']
tgt = [k for k, v in A.items() if v['name'] == NAME]
print('target', tgt, [(A[k]['spec'], A[k]['line']) for k in tgt])
t = tgt[0]
for c in A[t]['cls']:
    mark = '  <==' if c['line'] == LINE else ''
    print(f"  step {c['path']} L{c['line']} {c['class']}/{c['reason']} form={c['form']} markers={c['markers']}{mark}\n     {c['text'][:200]}")
def bfs(starts):
    par = {s: None for s in starts}
    q = collections.deque(starts)
    while q:
        x = q.popleft()
        for c in A[x]['calls']:
            y = '%s:%s' % tuple(c)
            if y not in par:
                par[y] = x; q.append(y)
    return par
for label, starts in (('roots minus target', [r for r in S['roots'] if r != t]),
                      ('navigate only', [k for k, v in A.items() if v['name'] == 'navigate' and k.startswith('html')]),
                      ('main fetch only', [k for k, v in A.items() if v['name'] == 'main fetch'])):
    par = bfs(starts)
    if t in par:
        path, x = [], t
        while x is not None:
            path.append(A[x]['name']); x = par[x]
        print(f'{label}: REACHED via', ' <- '.join(path))
    else:
        print(f'{label}: NOT reached')
