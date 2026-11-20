"""Propagate 'runs in parallel' context through calls (callee inherits caller's
in-parallel context). usage: python3 -I parallel_ctx.py <outdir>"""
import sys, pickle, csv, collections
OUT = sys.argv[1]
S = pickle.load(open(OUT + '/state.pkl', 'rb'))
A = S['algos']
CL = set(S['closure'])
rows = list(csv.DictReader(open(OUT + '/closure_steps.tsv'), delimiter='\t', quoting=csv.QUOTE_NONE))
slice_algos = {r['algorithm'] for r in rows if r['in_slice'] == 'True'}
seeds = set()
for k in CL:
    for c in A[k]['cls']:
        if c['reason'] in ('in-parallel', 'inside-in-parallel') or 'in-parallel' in c['markers']:
            seeds.update('%s:%s' % tuple(x) for x in c['local_calls'])
P, st = set(), list(seeds)
while st:
    x = st.pop()
    if x in P or x not in A: continue
    P.add(x); st.extend('%s:%s' % c for c in A[x]['calls'])
P &= CL
n_all = sum(len(A[k]['cls']) for k in P)
n_ext = sum(1 for k in P for c in A[k]['cls'] if c['class'] == 'extractable')
n_slice = sum(1 for k in P if A[k]['name'] in slice_algos for c in A[k]['cls'] if c['class'] == 'extractable')
print('algorithms reachable from in-parallel steps (within closure):', len(P))
print('their steps:', n_all, 'of which currently "extractable":', n_ext, 'in slice:', n_slice)
print(sorted(A[k]['name'] for k in P if A[k]['name'] in slice_algos))
