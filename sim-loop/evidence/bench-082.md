# bench-082 — skipped (load: backend unresponsive)

- host load (pre-run): 80.95 / 78.00 / 101.17 (1min/5min/15min), ncpu=10
- test suite (robotics, giemon): SKIPPED (load) — execution backend (terminal/search) unresponsive
- seeded reproduction: SKIPPED (load) — same unresponsive backend
- verdict: no measurement possible (skipped, load)
- regression: N/A (no measurement)
- command: N/A
- note: write_file backend itself returned double-path (cwd is already .../orgs/kotoba-lang/giemon); bench-082 written via absolute path to avoid ambiguity