#!/bin/bash
# Shared coordination signal for giemon sim-loop cowork bots.
cd ~/github/com-junkawasaki/orgs/kotoba-lang/giemon || exit 1
echo "=== MATURITY (status/maturity.md) ==="
cat sim-loop/status/maturity.md 2>/dev/null | head -20 || echo "none"
echo "=== NEXT ==="
grep -m1 "NEXT:" sim-loop/status/maturity.md 2>/dev/null || echo "none"
echo "=== EVIDENCE (recent files) ==="
ls sim-loop/evidence/ 2>/dev/null | tail -5 || echo "none"
echo "=== HOST LOAD ==="
uptime
echo "=== IN-FLIGHT (uncommitted) ==="
git status --porcelain | head -10
