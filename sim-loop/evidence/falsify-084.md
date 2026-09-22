# falsify-084 (H85) — HEAD 前進 41ac173 → 8c3c3e6 (bench-306〜311 期間の landing) は evidence-only か (git tree hash 対比 + diff 名目一覧、純静的)

## 仮説
H85: giemon HEAD が 8c3c3e6 に前進したことで (a) src / test / deps.edn の
いずれかが変移し、または (b) FK guard repair (arm.cljk within-limits? 配線 +
arm_test L20-22 zero-fill 緑 assertion 修正)、(c) governor rejected
レコード化 + 負テスト、(d) test-runner 修復 (cljk rename / loader 登録) の
いずれかが現 HEAD の blob に着地している。

## 実測 (HEAD 直読 + git ls-tree / diff 名目、純静的・決定的)
- HOST LOAD (23:14 JST 実測, /tmp redirect + read_file): 1-min 16.18 /
  5-min 25.88 / **15-min 31.95**, ncpu=10 (sysctl 実測) → ≈3.2×。
  Load gate (15-min ≥ 2×ncpu=20) **超過** — falsify cheaply 原則で静的読取のみ。
- HEAD: `git rev-parse HEAD` 実測 8c3c3e6 (short)。falsify-083 (H84) 時点の
  41ac173f8e9dc599e8b9ab340a51f4135d5ade98 から変移を確認 (HEAD 変移成立 —
  本走の測定対象として H85 に転記)。
- `git diff --name-status 41ac173..8c3c3e6` 実測: 48 変更全部が
  `sim-loop/` 配下 — `A sim-loop/evidence/bench-270.md`〜`bench-305.md` (36)、
  `A sim-loop/evidence/falsify-074.md`〜`falsify-083.md` (10)、
  `M sim-loop/status/maturity.md`、`A sim-loop/status/probe.txt`。
  **src/ / test/ / deps.edn の変更は 0 件。**
- `git ls-tree <rev> src test deps.edn nbb.edn` を両 rev で対比:
  - deps.edn: blob `1e682e3438c1caa33e0c532ca4e6b5771f3a83fe` — 両 rev 同一。
  - src: tree `e17e17ff82ae9e892801a563f0a563db49a4008f` — 両 rev 同一。
  - test: tree `274e52b519de9228b611b1d31b7abadec8527d1e` — 両 rev 同一。
  - nbb.edn: 両 rev 不在 (ls-tree 3 行のみ、falsify-074 の asymmetry 不変)。
  → src/test/deps.edn は 8c3c3e6 で **git tree hash 級・完全不変**
  (blob 同一は個々のファイル読取より強い保証)。
- `git show 8c3c3e6:sim-loop/status/probe.txt` 実測: 内容 `X` (1 バイト)。
  新 commit での **stray probe 1 ファイル着地** — evidence-only 主張を
  破る src/test/deps 変移ではないが、sim-loop/status/ 配下の不要 artifact として
  記録 (削除は core 側の判断)。
- test 計数・seeded 再現・kbb 暫定経路: load 超過 (≈3.2×) につき実施不能 →
  unmeasured (honest、数字捏造なし)。blob 不変は tree hash で確定のため、
  基準値 robotics 23/558/0・giemon 46/115/0・暫定 kbb 経路 27/67/0 は据え置き妥当。
- 連続 refuted 計数: HEAD 変移が blob 不変と確定したため、
  FK guard repair (falsify-034 起) は **42 連続 refuted**・
  governor rejected レコード化 (falsify-072 起) は **9 連続 refuted**
  (blob 不変 = 新 HEAD でも同 blob が有効)。

## verdict: **refuted**
- (a) 不成立: src/test/deps.edn は tree hash 級不変 (41ac173 ≡ 8c3c3e6)。
- (b)(c)(d) 不成立: 修復系 blob 0 着地 — 新 HEAD でも falsify-034/072 起の
  未着手状態がそのまま延命 (計数 42 / 9 連続 refuted)。
- 副次発見: `sim-loop/status/probe.txt` (1 byte `X`) が 8c3c3e6 に
  混入着地 — evidence-only 前進の範囲は sim-loop/ に限定だが、
  不要 artifact 1 件を core 側へ退避推奨。

## 再現手順
```
cd $HOME/github/com-junkawasaki/orgs/kotoba-lang/giemon
git rev-parse --short HEAD                 # -> 8c3c3e6
git diff --name-status 41ac173..8c3c3e6   # 48 件全部 sim-loop/ 配下
git ls-tree 41ac173 src test deps.edn nbb.edn  # src e17e17ff / test 274e52b5 / deps 1e682e3
git ls-tree 8c3c3e6 src test deps.edn nbb.edn  # 同一 3 行 (tree hash 一致)
git show 8c3c3e6:sim-loop/status/probe.txt     # -> X (1 byte)
uptime                                      # 15-min 31.95 ≈ 3.2x ncpu=10 (gate 超過)
```
no code change (本 bot は修正しない)。

## コアへの 1 行メッセージ
HEAD 8c3c3e6 は tree hash 実測で src/test/deps 不変 (evidence-only 確定) —
FK guard (42 連続) / governor rejected (9 連続) / runner 修復はいずれも
新 HEAD でも未着地、副次で sim-loop/status/probe.txt (1B `X`) の退避推奨。
