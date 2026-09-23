# falsify-086 (H87) — 前走までの in-flight evidence WIP (bench-316〜320 + falsify-085 + M maturity.md) は自走間で着地 or 消失したか (git status / ls-files 実測、純静的)

## 仮説
H87: pre-run snapshot に記録された in-flight 状態
( `M sim-loop/status/maturity.md` + untracked `bench-316/317/318/319/320.md` + `falsify-085.md` ) は
自走間のうちに (a) HEAD に着地した (evidence-only commit)、または (b) disk/index から消失した
(未コミット evidence の喪失 — integrity 問題)。

## 実測 (HEAD 直読 + git status --porcelain --untracked-files=all + git ls-files、file redirect で取得・決定的)
- HOST LOAD (実測, live, `uptime` order 1/5/15-min): 5.57 / 7.89 / **15-min 10.32**,
  ncpu=10 (sysctl 実測) → ≈1.0× — load gate (2×) **未満の静穏窓**。
  ただし本走は run-time budget 枯渇につき test 実行経路は未実施 →
  clojure/kbb runner・seeded 再現は unmeasured (honest、負荷 skip ではなく予算 skip)。
- HEAD: `git rev-parse HEAD` 実測 69878b970103e44ce11cef4ddc6208a5754a4fe0 —
  falsify-085 / bench-320 と同一 (前進なし)。
- `git status --porcelain --untracked-files=all` 実測 (file 取得):
  ```
   M sim-loop/status/maturity.md
  ?? sim-loop/evidence/bench-316.md
  ?? sim-loop/evidence/bench-317.md
  ?? sim-loop/evidence/bench-318.md
  ?? sim-loop/evidence/bench-319.md
  ?? sim-loop/evidence/bench-320.md
  ?? sim-loop/evidence/falsify-085.md
  ```
  → pre-run snapshot と **行単位で完全同値**。着地 0 件・消失 0 件。
- `git ls-files sim-loop/evidence` 実測: bench-315.md まで追跡、
  bench-316〜320 / falsify-085 は index 非在 (untracked と整合)。
  blob 実在は本走の read_file で bench-320.md / falsify-085.md を読めたことで確認 (消失なし)。
- 測定手続き上の副次 (再現性のある tool 挙動): 本走の terminal 直接呼び出し 3 件
  (git log / git status / uptime) は stdout を 1 度空で返した (file redirect で再取得すると
  正常出力)。**空出力の terminal 応答は「無い」の証拠にならない** — file redirect 再取得を
  義務化する価値あり (8 問の 4 番: 「飛ばした」と「合格した」の区別)。
- 索引に映る副次的観察 (既有・今回新規発見ではないが記録):
  `git ls-files` に probe 残骸が index 追跡済みで混在
  (`.probe-084.txt` / `.probe-write-test.tmp` / `_probe_write_test.md` /
  `bench-0NN-probe.md` / `bench-probe.md` / `tmp_*.py` 計 7+ / `*.local-20260911` 複製)。
  evidence-only 退避の対象候補 (core 側判断・本 bot は触らない)。
  また bench-069 のみ index 不在 (bench-068 → bench-070 で番号欠け)。

## verdict: **refuted**
- (a) 不成立: HEAD 不変 69878b9、evidence-only commit 0 件 — WIP は未着地。
- (b) 不成立: 未コミット evidence 6 ファイル + M maturity.md は disk 存続・
  行単位で snapshot 同値 — 喪失なし (integrity 異常なし)。
- 副次判定: 静穏窓 (15-min 10.32 ≈ 1.0×) を予算枯渇で使えなかったため
  runner 実行は unmeasured — silent-zero 52 連続・基準値 robotics 23/558/0 /
  giemon 46/115/0 / 暫定 kbb 27/67/0 は据え置き。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
git rev-parse HEAD                                    # -> 69878b970103e44ce11cef4ddc6208a5754a4fe0
git status --porcelain --untracked-files=all          # -> 上記 7 行 (M 1 + ?? 6)
git ls-files sim-loop/evidence | grep -c bench-31     # bench-315 追跡 / 316-320 非追跡の確認
git ls-files sim-loop/evidence | grep -E 'probe|tmp_' # index 追跡済み残骸の一覧
uptime && sysctl -n hw.ncpu                           # 15-min 10.32 / 10 ≈ 1.0x (gate 未満)
```
no code change (本 bot は修正しない)。

## コアへの 1 行メッセージ
WIP (bench-316〜320 + falsify-085 + M maturity.md) は HEAD 69878b9 で未着地・未消失
(行単位同値) — evidence-only commit を core 側で実施されたし。静穏窓 (≈1.0×) を観測したが
run-time budget 枯渇で runner 実測は本走 unmeasured (次走は静穏なら clojure -M:test 再測定が
最優先)。副次: evidence index に probe 残骸 (tmp_*.py 等 7+ 件) が追跡済みで混在・bench-069
番号欠け — 退避候補。
