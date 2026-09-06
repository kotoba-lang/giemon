# -*- coding: utf-8 -*-
"""maturity.md の bench 集計範囲を bench-054 まで進める (決定的、タイムスタンプなし)。"""
from pathlib import Path

P = Path("/Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon/sim-loop/status/maturity.md")
t = P.read_text(encoding="utf-8")
orig = t
t = t.replace("bench-001〜053 / falsify-001〜018", "bench-001〜054 / falsify-001〜018")
t = t.replace("bench-053 で機械再確認済み", "bench-054 で機械再確認済み")
t = t.replace("bench-001→053 で同一数字", "bench-001→054 で同一数字")
t = t.replace("負荷 5〜184 でも同一性 51 点確認", "負荷 5〜184 でも同一性 52 点確認")
t = t.replace("SEED-PARITY true を bench-002〜053 で 52 点確認", "SEED-PARITY true を bench-002〜054 で 53 点確認")
t = t.replace("bench-001〜053 + falsify-001〜018 の 71 件", "bench-001〜054 + falsify-001〜018 の 72 件")
assert t != orig
# verify every anchor applied
for a in ["bench-001〜054", "bench-054 で機械再確認済み", "bench-001→054", "52 点確認", "bench-002〜054 で 53 点確認", "72 件"]:
    assert a in t, a
assert "bench-053" not in t, "bench-053 residue"
P.write_text(t, encoding="utf-8")
print("OK", len(t))
