# bench-088 — SKIPPED (load & unresponsive backend) + falsify-030 (H32 refuted)

## verdict
- test スイート (robotics / giemon `kbb -M:test`): **skipped (load & backend 応答不能)**
- seeded 再現 (sim-loop L1 以降, 同一 seed 2 回): **skipped (load & backend 応答不能)**
- 回帰: **判定不能**（測定できず）— unmeasured のため assert しない (honesty-first)
- 本イテレーション falsify: **falsify-030 (H32) refuted** (静的読取)

## 理由
- HOST LOAD (pre-run 時点): 24.34 / 22.70 / 25.33 (1min/5min/15min), ncpu=10
  → 1min load (24.34) > ncpu (10)。重い実験は省略 (bench ルール、HOST LOAD 高)。
- 実行バックエンド応答不能: terminal が空出力 (exit 0) を返すまま応答せず
  (`uptime`/`date`/`pwd`/`echo` すべて空)。search_files は
  `could not stat .../giemon (sandbox may still be starting or was removed)`
  を返し evidence/fixtures/sandbox stat 不能。execute_code は cron モード blocked。
  → bench-069〜087 と同じ応答不能条件。write_file / read_file のみ成立。

## 測定手段
- clojure test、seeded 再現いずれも実行不能（実行数字を捏造せず skipped 記録）。
- 一方 falsify-030 (H32) は parity probe と fixture の **静的読取のみで完全に確定** する
  仮説のため、負荷非依存・決定的に実施し refuted と記録した。

## 静的読取 (read_file のみ成立、負荷非依存・決定的)
- `sim-loop/evidence/probe_parity_arm6.py` (1–98):
  - 行 16 `<origin xyz="([^"]+)" rpy="([^"]+)"` で **xyz と rpy の両方を capture**。
  - 行 20-21 `origin=xyz[0].split()` — **rpy (xyz[1]) を破棄**、以後未参照。
  - 行 26-32 link inertial.origin は rpy を受けない (`org.split()` のみ)。
  - 行 75-92 比較ループは translation xyz のみ、**rpy 比較呼び出し 0 件**。
- `fixtures/giemon_arm6/giemon_arm6.edn` (1–13): 全 `:joint/origin` は 3 値ベクトル
  (並進のみ)、`:inertial {:origin [x y z]}` も 3 値。**回転キー (:rpy/:rotation/
  :orient/:quat) 0 件**。
- `fixtures/giemon_arm6/giemon_arm6.urdf` (1–115): 全 `<origin ... rpy="0 0 0">`
  (回転なし)。
→ **URDF↔EDN parity の回転 (rpy) 成分を検証する既存面 = 0 件** (falsify-030)。

## 再現コマンド (今回実行不可。負荷収束・backend 回復後に実行すべき)
- kbb -M:test   # orgs/kotoba-lang/robotics と orgs/kotoba-lang/giemon 両方
- seeded 再現: sim-loop 学習ジョブを同一 seed で 2 回実行し結果一致を検査

## 索引・NEXT
- falsify-001〜029 (H1〜H31) + **falsify-030 (H32 refuted)** が盤上確定。
- NEXT: H32 の確定 (falsify-030) をもって next を進めて可。次候補は回転込み parity
  oracle の導入判断 (コア側, probe の rpy 比較追加 or `from_edn==parse_urdf` Clojure
  oracle を回転込みで実装) と、backend 復旧後の test スイート + seeded 再現の本測定
  (bench-089 で実施予定)。
- 基準値 (robotics 14/50/0, giemon 46/115/0) は bench-066 確定値のまま — 回帰は
  unmeasured のため assert せず（honesty-first）。コード修正なし（測定専用・読むだけ）。