#!/usr/bin/env python3
"""治水の費用便益比（B/C）に人命を入れたときの数値を再現する。標準ライブラリだけ。

思考実験 experiments/2026-11-21-life-value-in-flood-bc.md と、
手引き briefs/2026-11-21-life-value-in-flood-bc-guide.md の数値を出す。

    python3 -I experiments/scripts/life_value_bc.py

入力の数値はすべて公開資料から写したもの（出典と sha256 は記録の「具体」）。
評価期間50年・割引率4%（年金現価係数）、災害の発生確率、死亡率は仮定。
"""

from __future__ import annotations

LIFE_NEW = 6.01   # 億円/人。技術指針（共通編）令和6年9月改定（砂防の資料 第5回 資料1 p5 からの孫引き）
LIFE_OLD = 2.26   # 億円/人。改定前の値（技術指針 共通編 2008年版 p20）
YEARS, RATE = 50, 0.04


def annuity(years: int = YEARS, rate: float = RATE) -> float:
    return (1 - (1 + rate) ** -years) / rate


def life_benefit(deaths: float, prob: float, value: float = LIFE_NEW) -> float:
    """1回の災害で回避できる死者 deaths 人、年発生確率 prob のときの人命便益（億円、現在価値）。"""
    return deaths * prob * value * annuity()


def needed_deaths_per_year(benefit: float, cost: float, target: float, value: float = LIFE_NEW) -> float:
    """B/C を target にするのに必要な、年あたりの回避死者の期待値。"""
    return (target * cost - benefit) / (value * annuity())


def main() -> None:
    a = annuity()
    print(f"年金現価係数（{YEARS}年・{RATE:.0%}）= {a:.2f}")

    print("\n== 継続中の直轄事業（令和8年度予算に向けた再評価結果一覧、億円）")
    for name, b, c, cases in [
        ("鳴瀬川総合開発", 1389, 1032, [(41, 1 / 100), (41, 1 / 30)]),   # 回避41人（避難率40%、p22）
        ("川辺川ダム", 4278, 11312, [(91, 1 / 100), (91, 1 / 50)]),      # 回避91人（整備計画規模、p25）
    ]:
        vals = [(b + life_benefit(d, p)) / c for d, p in cases]
        print(f"{name}: B/C {b / c:.2f} → 人命を入れて {min(vals):.2f}〜{max(vals):.2f}"
              f"（回避{cases[0][0]}人、年1/{round(1 / cases[0][1])}〜1/{round(1 / cases[-1][1])}）")
    need = needed_deaths_per_year(4278, 11312, 1.0)
    print(f"川辺川ダムを B/C 1.0 にするのに必要な回避死者の期待値: 年{need:.1f}人（6.01億円/人）")

    print("\n== 小さな事業ほど人命の重みが大きい（B/C 0.8→1.0 に必要な回避死者）")
    for cost in (10, 30, 100):
        n = needed_deaths_per_year(0.8 * cost, cost, 1.0)
        print(f"費用{cost}億円: 年{n:.4f}人（年1/100の災害なら1回{n * 100:.1f}人、1/30なら{n * 30:.1f}人）")

    print("\n== 補助の河川事業で境目にある例：気仙川（岩手県、B 89億円・C 78億円、浸水区域内人口 3,095人）")
    for rate in (0.001, 0.01):
        for prob in (1 / 50, 1 / 30):
            d = round(3095 * rate)
            print(f"  死亡率{rate:.1%}（{d}人）・年1/{round(1 / prob)}: B/C {(89 + life_benefit(d, prob)) / 78:.2f}")

    print("\n== 基準にする避難の割合で、施設が守る命が変わる（鳴瀬川、避難率40%で41人を回避）")
    for evac in (0.0, 0.4, 0.8):
        d = 41 / 0.6 * (1 - evac)   # 想定死者数は (1 - 避難率) に比例する（水害の被害指標分析の手引 p26 の式）
        lo, hi = (1389 + life_benefit(d, 1 / 100)) / 1032, (1389 + life_benefit(d, 1 / 30)) / 1032
        print(f"  避難率{evac:.0%}: 施設が守る命 {d:.1f}人 → B/C {lo:.2f}〜{hi:.2f}")
    print(f"  二重計上の例: 施設の効果（避難0%）68.3人 ＋ 避難の効果（施設なし）27.3人 = 95.7人。正しくは 68.3人")

    print("\n== 境目すれすれの実例：内ケ谷ダム（岐阜県、令和元年度 B 957.70億円・C 909.49億円）")
    b, c = 957.70, 909.49
    for d in (0.0, 0.1):
        extra = (b + d * LIFE_NEW * a) / c - 1
        print(f"  回避死者 年{d}人: 費用が {extra:.1%} 増えるまで B/C≥1")


if __name__ == "__main__":
    main()
