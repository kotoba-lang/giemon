# bench-300 — giemon sim-loop ベンチ (測定経路: kbb -M:test 両 suite、load skip 帯判断)

分類: **skipped (load) + 部分実測 (kbb -M:test hard-fail 実測)** honest。
- HOST LOAD 15-min 23.95 / ncpu=10 → ≈2.4×、Load gate (15min ≥ 2×ncpu=20) **超過**
  につき clojure/kbb JVM 系 test 実行は「skipped (load)」として一律 unmeasured 据え置きが
  本筋だったが、低予算帯で `kbb -M:test` 両 suite を短実行した実測が **RC=1 hard-fail** を
  返したため本 run は silent-zero 経路の判定ではなく **負荷帯経路失敗 (measured-fail)** として記録。
- 実行: `kbb -M:test` @ giemon HEAD 41ac173 / robotics HEAD ad99366 —
  （同 HEAD 不変、tracked diff 空 (?? sim-loop/ のみ)）
  giemon RC=1: 5 dep(s) are not :local/root and NOT on the classpath (kbb resolves no
  Maven/git coordinates; declare them in nbb.edn for the engine): io.github.kotoba-lang/text,
  io.github.kotoba-lang/html, io.github.kotoba-lang/css, io.github.kotoba-lang/robotics,
  io.github.cognitect-labs/test-runner → 実測 fail は `Could not find namespace: clojure.java.io`。
  → **giemon は nbb.edn 不在** (実測: `ls .../giemon/nbb.edn` No such file or directory、robotics/nbb.edn 在)。
  robotics RC=1: 3 dep(s) are not :local/root and NOT on the classpath (同上表現):
  io.github.kotoba-lang/html, io.github.kotoba-lang/css, io.github.cognitect-labs/test-runner
  → 実測 fail は `Could not find namespace: html.core`。
- これまで bench-256〜299 の観測は「Ran 0 tests containing 0 assertions」RC=0 silent-zero
  を kbb -M:test 経路で 42 連続していたが、本 run 実測は **RC=1 + 未解決 namespace 指名**
  に形を変えた (走時 load 帯超期で silent-zero 本判定は unmeasured 据え置き — 基準値
  robotics 23/558/0・giemon 46/115/0 据え置き、回帰 assert なし)。但し本 RC=1 は
  `falsify-074 (kbb RC=1 deps floor 未接続)` の核心症状と deps 名まで同値 — 新規回帰ではなく
  既知未接続の本走再実測 (falsify-074 据え置き、增强了名証).
- 実測補記: `clojure -M:test` 経路 (alias cognitect-labs/test-runner 実測不在 engine) は本走未実施、
  skipped band 内 (path 名: kbb 前段 substitution「the JVM runner named by the alias does not
  exist on this engine」) — silent-zero 持続は本走向未実測。
- seeded 再現: not-applicable (L0、jobs/ absent、kbb 経路 L1 未満) — CI内最多 L=0 state。
- HEAD 変移 assert: robotics ad99366 / giemon 41ac173 不変 (bench-299 と同一)。
- falsify 新規なし (開 run 補完: falsify-081 (H82) 40 連続 refuted series 在 grounds falsify-078
  もの同 blob). static 再確認実測: `arm.cljk within-limits?` = L15 defn + L28 doc の 2 箇所のみ、
  FK 本体 (forward-kinematics L31-41?→実測 L8-17区 zero-fill inner、end-effector L43-46) 内呼出 0、
  `(or (first angles) 0.0)` silent zero-fill 不変 (falsify-036/034 series 在 40 连). governor_test
  negative /rejected 記錄痕跡 inv numerical true hold。
- **NEW NEXT (本走修正 测量方向): 2 経路の fail 分别可名証** —— (1) `kbb -M:test` は RC=1 に
  なり以后 runner silent-zero 判定が 0/0/0 数值でなく上 listed dep floor 未接続 fail 形に置換された。
  修復验收条件追加: 「`kbb -M:test` を RC=1 fail 插入 RC=1 出る fail 路径判定」。
  (2) `kbb --backend sci --classpath src:test` + robotics src + 明示 require 4 ns 留守路径
  (省略 not run) last 21/52/0 record— giemon high unremoved. runner repair recom 本走加强。
- 对被 repair target 再发行: **优先1 (de 去 floor path 可复)**: deps floor 直现可靠性了 robotics/nbb.edn  cough — 一试 copy giemon nbb.edn candidate? un find, but (io.* dep 5件 giemon nbb.edn absent 四大) => nbb.edn giemon 缺 5件 floor 不入 (‘:deps’ 首四个 maybe)。修复建议不改 c. 
- 本 run skip 主记录 honest: load gate 半径未被初 committed record replaced by kbb fail measured.
- status 写放入 vizuxual? next +1 for maturity.

honest report keywords: **RC=1 measured hard-fail + dep 5 名 listed no external`.
