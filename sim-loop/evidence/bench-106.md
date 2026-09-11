# bench-106 (日次 bench) — skipped (load + backend 応答不能)

状態: giemon sim-loop bench イテレーション (robotics / giemon の kbb -M:test、
seeded 再現) を実行不可。以下を正直に記録する。

## 実行不能の理由
- HOST LOAD: 1min 9.71 / 5min 18.56 / 15min 24.87 (ncpu=10)。
  15min 平均は約2.5×で高負荷継続。1min は 9.71 で下降傾向も、基準値を
  measured で更新するだけの余力は確認できず。
- 実行バックエンド応答不能:
  - `echo hello` / `echo alive; date` が空出力 (exit 0 のまま結果なし)。
  - `echo probe && ls /tmp` が 60s timeout (exit 124)。
  - search_files / read_file が "could not stat ... (sandbox may still be
    starting or was removed)" で失敗。filesystem そのものが応答不能。

## verdict
- テスト数 / assertion 数 / failures: **未計測 (skipped (load))** — test スイート
  実行不能のため記録なし。基準値 bench-066 確定 (robotics 14/50/0、
  giemon 46/115/0)、bench-102 にて実測一致済み。今回 unmeasured のため
  回帰 assert は行わず (honest)。
- seeded 再現: **skipped (load + backend 応答不能)**
- 回帰: **未判定 (unmeasured)**

## 再現コマンド (実行不可だったもの)
- `kbb -M:test` (orgs/kotoba-lang/robotics)
- `kbb -M:test` (orgs/kotoba-lang/giemon)
- sim-loop seeded 再現 (同一 seed 2 回走行)

## 継続
翌イテレーションで backend 回復時に test スイートを実測し、基準値と比較する。