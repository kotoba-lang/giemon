# bench-338 (giemon sim-loop bench iteration)

judgement: unmeasured — 全経路 skipped (load)。

## HOST LOAD (実測 2026-10-08 04:14–04:17 JST)
uptime: load averages 169.48/163.85/157.72 (04:14)、117.24/149.88/153.56 (04:17)
ncpu: 10 (hw.ncpu 10)
→ 15-min 154–157 / ncpu 10 ≈ 15–16x。ロード gate (~2x ncpu) を大幅超過、かつ
過去の override 許容帯 (3.3–4.3x, bench-327 実績) とも比べ物にならない重負荷。
→ 重い clojure -M:test / seeded 再現は省略し skipped (load) として正直に記録。

## 環境検出
- 実行ホスト: main-2.local / junkawasaki (実 checkout + clojure /opt/homebrew/bin/clojure + kbb あり)。
- 実 checkout: /Users/junkawasaki/github/kotoba-lang/{robotics,giemon} 両在在。
- bot worktree (.itonami-fleet) には giemon のみ (実 checkout は別、本記録は実 checkout 基準)。

## HEADs (gate 判定時点で不変・実測)
- robotics: a1af59c (tree 42c61b444950ad83ec78fa1e34c6bb4aaa952841)
- giemon: cd05afb (tree c3c454d28f3ec503bf9dbce458faceb68a060be5)
- 基準値 HEADs (bench-328 実測 robotics a1af59c / giemon cd05afb) と一致 — HEAD 不変。
  test tree 前進も含む進行なし (前回記録 bench-337 と同一)。

## test スイート
skipped (load) unmeasured — 実行未了。

## seeded 再現
skipped (load) unmeasured — 実行未了。

## 基準値 (bench-066 確定・kbb bench-327/328 進行分を含む)
- robotics: clojure -M:test 0/0/0 RC=0 (silent-zero 持続、falsify-069 根因未修復) / kbb -M:test 57/624/0 RC=0 (bench-328/333 3 連続一致)
- giemon: clojure -M:test 0/0/0 RC=0 (silent-zero 持続) / kbb -M:test 46/115/0 (2 連続一致)
- 本回 unmeasured につき基準値据え置き。

## 回帰判定
regression: なし (HEAD 不変 + unmeasured につき assert せず)。

## falsify status
- falsify-069 (clojure runner silent-zero 根因・JVM require が .cljk をロード不能): 未修復のまま、本回未触。
- falsify-079 (意図的 fail 挿入で RC=1): 検収条件として残す、本回未触。
- 修復先 clojure runner 緑化・負テスト 1 件 (falsify-075/076/077 family) とも本回未触。

## 再現コマンド
uptime / nproc / sysctl -n hw.ncpu
git -C /Users/junkawasaki/github/kotoba-lang/robotics log --oneline -1 && rev-parse 'HEAD^{tree}'
git -C /Users/junkawasaki/github/kotoba-lang/giemon log --oneline -1 && rev-parse 'HEAD^{tree}'
(実行の判決は決定的・タイムスタンプなし・本記録は skipped (load) unmeasured)

no code change.
