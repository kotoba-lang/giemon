# falsify-085 (H86) — HEAD 前進 8c3c3e6 → 69878b9 (bench-306〜316 期間の landing) は evidence-only か (git tree hash 対比 + diff 名目一覧、純静的)

## 仮説
H86: giemon HEAD が 8c3c3e6 から 69878b9 に前進したことで
(a) src / test / deps.edn のいずれかが変移し、または
(b) FK guard repair (arm.cljk within-limits? 配線 + arm_test L20-22 zero-fill 緑 assertion 修正)、
(c) governor rejected レコード化 + 負テスト、(d) test-runner 修復
(cljk rename / loader 登録 / nbb.edn deps floor) のいずれかが現 HEAD の blob に着地している、
または (e) falsify-084 副次で記録した stray artifact `sim-loop/status/probe.txt` が退避された。

## 実測 (HEAD 直読 + git ls-tree / diff 名目、純静的・決定的)
- HOST LOAD (実測, live, `uptime` order は 1/5/15-min): 1-min 30.64 /
  5-min 37.01 / **15-min 29.65**, ncpu=10 (sysctl -n hw.ncpu 実測) → ≈3.0×。
  Load gate (15-min ≥ 2×ncpu=20) **超過** — falsify cheaply 原則で静的読取のみ。
- HEAD: `git rev-parse HEAD` 実測 69878b970103e44ce11cef4ddc6208a5754a4fe0。
  `git merge-base --is-ancestor 8c3c3e6 69878b9` 実測: true (merge による clean 前進)。
- `git diff --name-status 8c3c3e6..69878b9` 実測: 12 変更全部が
  `sim-loop/` 配下 — `A sim-loop/evidence/bench-306.md`〜`bench-315.md` (10)、
  `A sim-loop/evidence/falsify-084.md` (1)、`M sim-loop/status/maturity.md` (1)。
  `git diff --stat` 実測: 12 files, +462/−3。
  **src/ / test/ / deps.edn の変更は 0 件。**
- `git ls-tree <rev> src test deps.edn nbb.edn` を両 rev で対比:
  - deps.edn: blob `1e682e3438c1caa33e0c532ca4e6b5771f3a83fe` — 両 rev 同一。
  - src: tree `e17e17ff82ae9e892801a563f0a563db49a4008f` — 両 rev 同一。
  - test: tree `274e52b519de9228b611b1d31b7abadec8527d1e` — 両 rev 同一。
  - nbb.edn: 両 rev 不在 (falsify-074 の giemon/robotics asymmetry 不変)。
  → src/test/deps.edn は 69878b9 でも **git tree hash 級・完全不変**
  (falsify-084 と同一の 3 ハッシュ)。
- `git show 69878b9:sim-loop/status/probe.txt` 実測: 内容 `X` (1 バイト) —
  falsify-084 副次で記録した stray artifact は **退避されていない** (継続)。
- test 計数・seeded 再現・kbb 暫定経路: load 超過 (≈3.0×) につき実施不能 →
  unmeasured (honest、数字捏造なし)。blob 不変は tree hash で確定のため、
  基準値 robotics 23/558/0・giemon 46/115/0・暫定 kbb 経路 27/67/0 は据え置き妥当。
- 連続 refuted 計数: blob 不変が新 HEAD でも確定したため、
  FK guard repair (falsify-034 起) は **43 連続 refuted**・
  governor rejected レコード化 (falsify-072 起) は **10 連続 refuted**
  (blob 同一 = 新 HEAD でも同 blob が有効)。

## verdict: **refuted**
- (a) 不成立: src/test/deps.edn は tree hash 級不変 (8c3c3e6 ≡ 69878b9)。
- (b)(c)(d) 不成立: 修復系 blob 0 着地 — 新 HEAD でも falsify-034/072 起の
  未着手状態がそのまま延命 (計数 43 / 10 連続 refuted)。
- (e) 不成立: probe.txt (1B `X`) は 69878b9 でも存続 — 退避 0 件。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
git rev-parse HEAD                                    # -> 69878b970103e44ce11cef4ddc6208a5754a4fe0
git merge-base --is-ancestor 8c3c3e6 69878b9 && echo YES   # -> YES (clean 前進)
git diff --name-status 8c3c3e6..69878b9               # 12 件全部 sim-loop/ 配下
git diff --stat 8c3c3e6..69878b9                     # 12 files +462/-3
git ls-tree 8c3c3e6 src test deps.edn nbb.edn        # src e17e17ff / test 274e52b5 / deps 1e682e3
git ls-tree 69878b9 src test deps.edn nbb.edn        # 同一 3 行 (tree hash 一致)
git show 69878b9:sim-loop/status/probe.txt           # -> X (1 byte)
uptime && sysctl -n hw.ncpu                          # 15-min 29.65 ≈ 3.0x ncpu=10 (gate 超過)
```
no code change (本 bot は修正しない)。

## コアへの 1 行メッセージ
HEAD 69878b9 は tree hash 実測で src/test/deps 不変 (evidence-only 確定) —
FK guard (43 連続) / governor rejected (10 連続) / runner 修復はいずれも
新 HEAD でも未着地、probe.txt (1B `X`) も 69878b9 で存続 — 退避は core 側の判断。
