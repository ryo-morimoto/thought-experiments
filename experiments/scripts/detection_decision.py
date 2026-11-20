#!/usr/bin/env python3
"""「検出されていない」を判断に使うときの数値を、気象庁の公開データから再現する。

思考実験 experiments/2026-11-21-non-detection-vs-no-change.md の段階B（操作1・2）と、
手引き briefs/2026-11-21-non-detection-decision-guide.md の表を出す。標準ライブラリだけ。

    python3 -I experiments/scripts/detection_decision.py

方法: 年ごとの数に最小二乗で直線を当てはめ、75年間の変化量の事後分布を
平たい事前分布・正規近似で N(推定, 標準誤差^2) とする。「判断に効く変化」は平均の10%以上の増加。
現状維持が正しいのは P(判断に効く変化) < 空振りの費用 / 見逃しの損失 のとき、
つまり損失比（見逃しの損失 / 空振りの費用）が 1/P 未満のとき。自己相関は補正していない。
"""

from __future__ import annotations

import csv
import math
import statistics as st
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[2]
SERIES = [
    ("発生数", ROOT / "data/jma-typhoon-generation/generation.csv"),
    ("接近数", ROOT / "data/jma-typhoon-accession/accession.csv"),
    ("上陸数", ROOT / "data/jma-typhoon-landing/landing.csv"),
]
RELEVANT = 0.10  # 判断に効く変化：平均の10%以上の増加


def annual(path: Path) -> dict[int, int]:
    rows = csv.reader(path.open(encoding="cp932"))
    return {int(r[0]): int(r[-1]) for r in rows if r and r[0].isdigit() and r[-1]}


def trend(d: dict[int, int]):
    x = sorted(d)
    n, xm, ym = len(x), st.mean(x), st.mean(d.values())
    sxx = sum((a - xm) ** 2 for a in x)
    b = sum((a - xm) * (d[a] - ym) for a in x) / sxx
    s = math.sqrt(sum((d[a] - (ym + b * (a - xm))) ** 2 for a in x) / (n - 2))
    return x, ym, b * (n - 1), s / math.sqrt(sxx) * (n - 1)  # 期間全体の変化量と標準誤差


def main() -> None:
    print("== 指標ごとの検定の力と、現状維持が正しい損失比の上限")
    for name, path in SERIES:
        x, mean, change, se = trend(annual(path))
        p = 1 - NormalDist(change, se).cdf(RELEVANT * mean)
        mde = (1.96 + 0.84) * se
        print(f"{name}: {x[0]}-{x[-1]} 平均{mean:.1f} 変化{change:+.2f}個({change / mean:+.0%}) "
              f"t={change / se:.2f} 95%区間{(change - 1.96 * se) / mean:+.0%}〜{(change + 1.96 * se) / mean:+.0%} "
              f"検出力80%の最小変化{mde / mean:.0%} P(増加≥10%)={p:.3f} 維持が正しいのは損失比<{1 / p:.1f}")

    print("\n== 同じ精度で推定の向きだけ違う場合（発生数の精度を使う）")
    _, mean, change, se = trend(annual(SERIES[0][1]))
    for label, est in [("A 実データ", change), ("B 推定0", 0.0), ("C 増加方向 t=+1.0", se), ("D 増加方向 t=+1.78", 1.78 * se)]:
        p = 1 - NormalDist(est, se).cdf(RELEVANT * mean)
        print(f"{label}: P(増加≥10%)={p:.4f} 維持が正しいのは損失比<{1 / p:.0f}")

    print("\n== 検出の基準に含まれる損失比")
    q = NormalDist().cdf(1.96)
    print(f"「両側 p<0.05 で検出されたら対策」＝ P(増加>0)≥{q:.3f} で対策 ＝ 損失比 {1 / q:.2f}")


if __name__ == "__main__":
    main()
