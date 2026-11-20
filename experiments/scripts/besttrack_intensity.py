"""思考実験 experiments/2026-11-21-non-detection-vs-no-change.md の段階B：強い台風の割合の傾向。

気象庁 RSMC Tokyo ベストトラック（data/jma-besttrack/）から、台風ごとの生涯最低中心気圧と
生涯最大風速を求め、強い台風の割合の傾き・検出力・判断のしきい値を計算する。標準ライブラリだけ。
実行: python3 experiments/scripts/besttrack_intensity.py（リポジトリのルートで）
"""
import zipfile, csv, math, statistics as st
from statistics import NormalDist as N

t = zipfile.ZipFile('data/jma-besttrack/bst_all.zip').read('bst_all.txt').decode('ascii').splitlines()
storms, cur = [], None
for l in t:
    if l.startswith('66666'):
        cur = {'id': l[6:10], 'rows': []}
        storms.append(cur)
    else:
        yy = int(l[0:2]); y = 1900 + yy if yy >= 51 else 2000 + yy
        g = int(l[13]); p = l[24:28].strip(); w = l[33:36].strip()
        cur['rows'].append((y, g, int(p) if p else None, int(w) if w else 0))

recs = []
for s in storms:
    ts = [r for r in s['rows'] if r[1] in (3, 4, 5, 9)]
    if not ts:
        continue
    year = ts[0][0]  # 初めて TS 以上になった年（UTC）
    pmin = min(r[2] for r in s['rows'] if r[2])
    wmax = max(r[3] for r in s['rows'])
    recs.append((year, pmin, wmax))

gen = {int(r[0]): int(r[-1]) for r in csv.reader(open('data/jma-typhoon-generation/generation.csv', encoding='cp932'))
       if r and r[0].isdigit() and r[-1]}
cnt = {}
for y, _, _ in recs:
    cnt[y] = cnt.get(y, 0) + 1
diff = [(y, cnt.get(y, 0), gen[y]) for y in sorted(gen) if cnt.get(y, 0) != gen[y]]
print(f"照合: ベストトラックで TS 以上に達した台風の年別の数が発生数 CSV と一致しない年 = {len(diff)} 年 {diff[:8]}")


def trend(name, frac):
    x = sorted(frac); n = len(x); L = x[-1] - x[0]
    xm = st.mean(x); ym = st.mean(frac.values()); sxx = sum((a - xm) ** 2 for a in x)
    b = sum((a - xm) * (frac[a] - ym) for a in x) / sxx
    res = [frac[a] - (ym + b * (a - xm)) for a in x]
    s = math.sqrt(sum(r * r for r in res) / (n - 2)); se = s / math.sqrt(sxx)
    r1 = st.correlation(res[:-1], res[1:])
    ch, sech = b * L, se * L
    rel, serel = ch / ym, sech / ym
    mde = (1.96 + 0.84) * serel
    P = 1 - N(rel, serel).cdf(0.10)
    lim = f"{1 / P:.1f}" if P > 1e-9 else "∞"
    print(f"{name}: {x[0]}-{x[-1]} 平均割合{ym * 100:.1f}% 傾き{L}年で{ch * 100:+.1f}ポイント（相対{rel * 100:+.0f}%） "
          f"t={b / se:.2f} 95%区間 相対{(rel - 1.96 * serel) * 100:+.0f}%〜{(rel + 1.96 * serel) * 100:+.0f}% "
          f"検出力80%の最小変化 相対{mde * 100:.0f}% P(相対増加≥10%)={P:.3f} 維持が正しいのは L_miss/C<{lim} 残差自己相関{r1:.2f}")


def yearly(pred, y0, y1):
    tot, hit = {}, {}
    for y, p, w in recs:
        if y0 <= y <= y1:
            tot[y] = tot.get(y, 0) + 1
            hit[y] = hit.get(y, 0) + (1 if pred(p, w) else 0)
    return {y: hit[y] / tot[y] for y in sorted(tot)}, sum(hit.values())


defs = [("最低気圧≤930hPa", lambda p, w: p <= 930, [(1951, 2025), (1977, 2025), (1987, 2025)]),
        ("最大風速≥85kt（非常に強い以上）", lambda p, w: w >= 85, [(1977, 2025), (1987, 2025)]),
        ("最大風速≥105kt（猛烈な）", lambda p, w: w >= 105, [(1977, 2025), (1987, 2025)])]
for name, pred, periods in defs:
    for y0, y1 in periods:
        frac, k = yearly(pred, y0, y1)
        trend(f"{name} 件数{k}", frac)
