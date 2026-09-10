# bench-083 — skipped (load: backend unresponsive)

- host load (pre-run): 29.90 / 45.61 / 70.65 (1min/5min/15min), ncpu=10
- test suite (robotics, giemon): SKIPPED (load) — execution backend (terminal/search) unresponsive
- seeded reproduction: SKIPPED (load) — same unresponsive backend
- verdict: no measurement possible (skipped, load)
- regression: N/A (no measurement)
- command: N/A
- note: falsify-027 (H29) recorded via static line-level read (REPL-independent, IEEE-754 deterministic); git head /基准値保持の判定は bench-066 確定値 (robotics 14/50/0, giemon 46/115/0) のまま変更なし。新規 refute は falsify-027 (H29 refuted) の 1 件、基準値テスト数字に回帰なし (未測定、スキップのため数字は捏造せず)。