# falsify-067 (H68) — FK guard repair 配線有無の本回再実測 (純静的読取)

## 仮説
H68: `within-limits?` が FK 本体 (`forward-kinematics` / `end-effector`) から
呼ばれるようになった (FK guard repair 実装済み)、または silent zero-fill /
arm_test 緑 assertion が変更された — 28 連続 refuted の 29 回目が反転するか。

## 実測 (純静的読取, 本回ファイル読取実測)
- `src/kotoba/giemon/arm.cljc` 全 122 行読取:
  - `within-limits?` は L15-20 の defn のみ (L16-17 docstring)、FK 本体
    (`forward-kinematics` L22-41) からは呼出 0 回。L38
    `(angle (or (first angles) 0.0))` silent zero-fill 不変。
  - `end-effector` L43-46 も forward-kinematics の last のみ、limit 検査なし。
  - docstring L27-29 「This is pure kinematics, not the safety gate … Check
    `within-limits?` first」自白のまま。
- `src/kotoba/giemon/kinematics.cljc` 全 68 行読取: `joint-transform`
  (L63-67) は origin + axis-angle 回転のみ、limit/effort 概念なし。
- `test/kotoba/giemon/arm_test.cljc` 全 40 行読取: L20-22
  「missing angles default to 0.0」silent zero-fill 緑 assertion 期待値変更なし。
- HEAD 実測: giemon `d0d3cb45fcc8c42d94f6a370b5a1f19d51938abe` 不変・
  tracked diff 空 (`git status --porcelain` → `?? sim-loop/` のみ、/tmp
  redirect + read_file workaround で取得)。governor 層の FK/limit 接続は
  maturity.md 集計 (falsify-057: gate 迂回 shortcut src 内不存在) と一致。

## 負荷判定
HOST LOAD 15min ≈119-121 (≈12× ncpu=10, 1min 102.93 / 5min 132.34) — Load
gate (15min ≥ 2×ncpu=20) 大幅超過のため kbb -M:test / seeded 再現は
省略、test 計数 unmeasured (honest, 数字捏造ゼロ)。本判定は純静的読取で
負荷非依存。

## verdict
**refuted** — FK guard repair は依然未配線。`within-limits?` は定義・
docstring のみで FK 経路内部から呼出 0 回、L38 silent zero-fill 不変、
arm_test L20-22 緑固定不変、HEAD 不変・tracked diff 空 (?? sim-loop/ のみ)。
falsify-034/036/039〜066 と同根・29 連続 refuted。

## 再現手順
1. `cd orgs/kotoba-lang/giemon && git rev-parse HEAD` → d0d3cb45fcc8…
2. `src/kotoba/giemon/arm.cljc` を読む: `within-limits?` は L15 defn のみ、
   `forward-kinematics` L31-41 loop 内に呼出なし、L38
   `(angle (or (first angles) 0.0))`。
3. `test/kotoba/giemon/arm_test.cljc` L20-22 「missing angles default to
   0.0」緑固定を確認。

コアへの 1 行メッセージ: FK guard repair (forward-kinematics 本体への
within-limits? 配線 + arm_test L20-22 期待値変更) は 29 連続未着手 —
HEAD 不変のまま NEXT 再発行継続。
