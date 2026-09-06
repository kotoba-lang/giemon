# -*- coding: utf-8 -*-
""" maturity.md を falsify-009 の結果で更新する (決定的、タイムスタンプなし)。"""
from pathlib import Path

P = Path("/Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon/sim-loop/status/maturity.md")
t = P.read_text(encoding="utf-8")
orig = t

def sub(old, new):
    global t
    if old not in t:
        raise SystemExit("ANCHOR NOT FOUND: %r" % old[:60])
    t = t.replace(old, new, 1)

# 1. L0 段階の falsify 範囲を 009 まで広げる
sub("falsify-002〜falsify-008 は測定 probe のみで",
    "falsify-002〜falsify-009 は測定 probe のみで")

# 2. 7 軸表の対象 evidence 範囲
sub("falsify-001〜008.md から決定的計算)",
    "falsify-001〜009.md から決定的計算)")

# 3. falsify-009 を軸 5 (ベンチ計測) の末尾に追記
old5 = "静的 (falsify-001: 2.73 N·m / payload 3 kg で 18.6 N·m < cont 40) を含め静的→quasi-dynamic→full dynamic→宣言範囲制約付き→モデル形式検証→評価形式 (熱的 RMS) 検証→対象関節拡大 (j1/j5)→fixture 表現契約検証 の 8 段階計測。"
new5 = ("falsify-009 (probe_caterpillar_wf.py — caterpillar URDF の ill-formedness は"
        "XML コメント内 `--` の 1 箇所のみ: コメント除去後は well-formed (links=5/joints=4) "
        "かつ EDN boom chain と 0-default 読みで mismatch=0 の数値完全一致 — "
        "fixture 修正は 1 行で済むことを特定)、"
        "静的 (falsify-001: 2.73 N·m / payload 3 kg で 18.6 N·m < cont 40) を含め"
        "静的→quasi-dynamic→full dynamic→宣言範囲制約付き→モデル形式検証→"
        "評価形式 (熱的 RMS) 検証→対象関節拡大 (j1/j5)→fixture 表現契約検証→"
        "fixture 修正の最小範囲特定 の 9 段階計測。")
sub(old5, new5)

# 4. 軸 6 に falsify-009 の判定を追記
old6 = "caterpillar 側 parity oracle は fixture 修正しない限り成立不能 (新規構造的赤)。DR 質量スケール破れ点の記録あり |"
new6 = ("caterpillar 側 parity oracle は fixture 修正しない限り成立不能 (新規構造的赤)。"
        "falsify-009: H11 (コメント除去後も parse 不成立・数値不一致が残る) **refuted** — "
        "ill-formedness はコメント内 `--` の 1 箇所のみで、コメント除去後は well-formed かつ "
        "EDN と mismatch=0。ただし標準 XML parser はコメントで落ちるため、"
        "fixture 修正しない限り parity oracle 成立不能の記録自体は survived "
        "(修正は 1 行: `--` を `:` 等へ置換)。DR 質量スケール破れ点の記録あり |")
sub(old6, new6)

# 5. 軸 7 の evidence 件数と probe 一覧
sub("bench-001〜022 / falsify-001〜008 の 30 件",
    "bench-001〜022 / falsify-001〜009 の 31 件")
sub("probe_offdiag_inertia.py 同梱。",
    "probe_offdiag_inertia.py / probe_caterpillar_wf.py 同梱。")

# 6. OPEN の caterpillar 赤に falsify-009 の精緻化を追記
sub("falsify-008 により caterpillar URDF は well-formed でないことが判明 — fixture 修正しない限り caterpillar 側は成立不能)",
    "falsify-008 により caterpillar URDF は well-formed でないことが判明、falsify-009 により原因はコメント内 `--` の 1 箇所のみと特定 (コメント除去後は well-formed・EDN と mismatch=0) — fixture 修正しない限り caterpillar 側は成立不能)")

# 7. NEXT の更新
old_next = t[t.index("## NEXT"):t.index("## 判定原則")]
new_next = (
    "## NEXT\n"
    "- NEXT: (a) giemon_caterpillar_facade.urdf の XML コメント内 `--` 修正\n"
    "  (falsify-009 により最小修正 1 行と特定 — fixture 修正のためコード修正が必要で\n"
    "  本 bot ではなくコア側の対応対象) と parity oracle (from_edn==parse_urdf) の\n"
    "  Clojure 実装、または (b) falsify-002 の gate↔arm torque 照合未接続赤を深掘りする\n"
    "  probe (governor が `:action/params` の torque を検査しないことを input 空間の\n"
    "  網羅で機械測定)。コード修正を伴う (a) の本体対応は本 bot の役割外のため、\n"
    "  本 bot は (b) を優先候補とする。\n\n"
)
t = t.replace(old_next, new_next, 1)

assert t != orig
P.write_text(t, encoding="utf-8")
print("maturity.md updated OK, %d chars" % len(t))
