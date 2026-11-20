"""Print samples for manual audit. usage: python3 -I audit.py <outdir> <seed>"""
import sys, csv, random, collections
OUT = sys.argv[1]
random.seed(int(sys.argv[2]))
rows = list(csv.DictReader(open(OUT + '/closure_steps.tsv'), delimiter='\t', quoting=csv.QUOTE_NONE))
by = collections.defaultdict(list)
for r in rows:
    by[r['reason'] if r['class'] != 'extractable' else 'EXTRACTABLE'].append(r)
for k, v in sorted(by.items()):
    n = 30 if k == 'EXTRACTABLE' else 4
    print('=====', k, len(v))
    for r in random.sample(v, min(n, len(v))):
        print(f"  [{r['spec']}:{r['line']} {r['algorithm'][:40]} {r['step']} {r['form']}] {r['text'][:200]}")
