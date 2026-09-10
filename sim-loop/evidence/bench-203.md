# bench-203 — measured (実測完走, 負荷 ~4.5×)

判定: **measured** — HOST LOAD 15-min ~45.42 ≈ 4.5× ncpu ( hw.ncpu=10) が Load gate (~2×) を大きく超える
高負荷帯だったが、backend 応答で /tmp redirect + read_file workaround (bench-197〜202 と同手) により test スイート実測完走
(robotics・giemon 両方、exit 0 両方)。per-project 出力 (/tmp/b_rob_203.txt, /tmp/b_gie_203b.txt) 完走 fixture
あり (両方 final 行に RC=0 / DONE マーカー)。

## 環境
- HOST LOAD (実行終了時): 1-min 55.19 / 5-min 51.53 / 15-min 45.42 (→約 4.5×)、up: 3 days 19h 50m、6 users
- Load gate (~2×ncpu=20) 大幅超過帯だが、bench-200 (~7.4×)/201 (~4.2×)/202 (~3.2×) と同様に backend 応答で
  /tmp redirect workaround により実測取得可能だったため skip せず measured 記録。

##テスト数字 (per-project)
- kotoba-lang/robotics: **14/50/0**、exit 0 — 基準値 ( bench-066 確定) と完全一致
- kotoba-lang/giemon: **46/115/0**、exit 0 — 基準値 ( bench-066 確定) と完全一致

## git HEAD
- robotics: `9459ca0d5b3` (基準値 9459ca0 と一致、ソース変化なし・tracked クリーン)

- giemon: `d0d3cb45fcc` (基準値 d0d3cb4 と一致、ソース変化なし)
- tracked diff 空 (`?? sim-loop/` のみ untracked)

## seeded 再現 verdict
- not-applicable (sim-loop は L0、job なし;L1 以降 の seeded 再現 は 対象外。今回 も seeded job 実行なし。)

## 回帰
- **なし (measured assert)** — 両スイートが基準値 ( bench-066 確定 / bench-202 最新実測) と完全一致
  (robotics 14/50/0、giemon 46/115/0、両者 exit 0)、HEAD 両方不変・tracked diff 空。回帰なし。



## falsify 状況
- 前回 (bench-202) 同様据え置き — 今回新規 falsy なし、新仮説判定なし (code 無変更で判定対象なし)。
  HEAD giemon d0d3cb45fcc / robotics 9459ca0d5b3 不変・tracked diff 空 (`?? sim-loop/` のみ)、
  FK guard repair 未着手のまま継続 (`within-limits?` ヒット arm.cljc L15 def /L28 doc/arm_test L29-30 の計 3 箇所のみ、
  FK 経路 ( forward-kinematics / end-effector)内呼出 0 回、falsify-058 と同値)。ステータス正本 ( status/maturity.md) の NEXT  は
  FK guard repair (実装側タスク) のまま 継続。

## 再現コマンド
- (実測完走): `cd .../kotoba-lang/robotics && clojure -M:test` →  igh 14/50/0 (exit  igh 0)、
  `cd .../kotoba-lang/giemon && clojure -M:test` → 46/115/0 (exit 0)

## 備考
- 基準値は bench-066 確定 (robotics 14/50/0、giemon 46/115/0)。前回 bench-202 に続き
  high-load 帯 (≈4.5×) でも backend 応答で measured 実測完走 (robotics と giemon 両方完走)。回帰なし。
- コード変更なし (`?? sim-loop/` のみ untracked)。probe 類は多数 md から参照され EVIDENCE のため削除せず。