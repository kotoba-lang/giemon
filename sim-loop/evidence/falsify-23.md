# falsify-23 — `rob/mission` の bounded-operation 契約が無検査 (`:max-steps` 0/負/NaN/Inf/文字列、nil id/objective が無音受理)

日時: cron iteration (JST 2026-09-04, host load avg 36-57 / コア 10 → 軽量 in-memory REPL 測定のみ、fixture 読み込みなし)

## 仮説

falsify-6〜22 で arm / kinematics / chassis / export / gate の fail-open は潰したが、
`kotoba.robotics` の **mission 契約は未反証**。`rob/mission` の docstring は
「1 mission = 1 bounded operation, no infinite internal loop — durable outer loops
repeat missions」と宣言し、`:max-steps` がその上限の根拠。しかし
`src/kotoba/robotics.cljc` (gitlibs 1d1f93e) の実装は引数を無検査の map 投入のみで:

- `:max-steps 0` / `-5` → 「0 ステップで bounded」「負で bounded」は意味をなさず、
  未整備の governor ループ消費者は nil/0 を「無制限」フォールバックで解釈しがち。
- `##NaN` / `##Inf` / `"unlimited"` (文字列) → 数値比較 `(> i max-steps)` 系の
  ループ消費者は NaN 比較 false / Inf で永遠に bounded を抜けられない。
- `:mission/id` / `:mission/robot` / `:mission/objective` nil も例外なく `:planned`
  ミッションを生成 — 監査レコードのキー項目が空のまま運用可能。

また付帯で `rob/telemetry-proof` は `:proof/sensor` / `:proof/reading` nil を無音受理
(監査台帳の実体無し proof)。対照: `rob/safety-stop` は不明 reason で nil を返し
fail-closed を維持 (H で実測)。

## 実測

コード: gitlibs `io.github.kotoba-lang/robotics/1d1f93e.../src/kotoba/robotics.cljc`
mission L36-47, telemetry-proof L103-110。
実行: `clojure -M /tmp/f/f23.clj` (repl 出力は evidence 末尾の手順と同一)。

```
:A  (rob/mission "m1" :otete "obj" :max-steps 0)        => :max-steps 0, :status :planned
:B  :max-steps -5                                       => 無音受理
:C  :max-steps ##NaN                                    => 無音受理
:D  :max-steps ##Inf                                    => 無音受理
:E  (rob/mission nil nil nil)                           => 全キー nil の :planned ミッション
:F  :max-steps "unlimited"                              => 無音受理 (文字列)
:G  :boundaries {:geo-fence ##NaN}                      => 無音受理 (境界の非有限)
:H  (rob/safety-stop "m1" :not-a-reason)                => nil (fail-closed 対照)
:I  (rob/telemetry-proof "m1" nil nil)                  => sensor/reading nil の proof 無音生成
```

読み取り:

- `:max-steps` は型・値・有限性のいずれも検査されない。0/負/NaN/Inf/文字列の
  いずれでも「bounded operation」レコードとして正規生成され、例外も無音
  フラグもない。NaN/Inf は falsify-11/14/15/16/17 と同系の非有限無検査で、
  今回は **mission 契約 (無限ループ禁止) の正面**での破れ。
- nil id/objective も受理され、監査に「誰の・何の」ミッションか分からない
  `:planned` レコードが乗る。
- `telemetry-proof` の nil sensor/reading は「sensing と台帳のリンク」契約を
  実体空のまま成立させる。
- 対照: `safety-stop` は stop-reasons メンバーシップ検査で fail-closed —
  同一 namespace 内で検査の有無が一貫しない。

## Verdict: **refuted** (`rob/mission` は `:max-steps` 0/負/NaN/Inf/文字列と nil id/robot/objective を無音受理し bounded-operation 契約が入力検査で担保されていない。`telemetry-proof` も nil sensor/reading を無音受理)

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(require (quote [kotoba.robotics :as rob]))
(prn (rob/mission "m1" :otete "obj" :max-steps ##NaN))
(prn (rob/mission nil nil nil))
(prn (rob/telemetry-proof "m1" nil nil))'
;; => いずれも例外なしで正規レコード (max-steps ##NaN / 全キー nil / sensor reading nil)
```

## コアへの 1 行メッセージ

giemon-sim へ: falsify-23 実測 — `rob/mission` は `:max-steps` を無検査で
0/負/`##NaN`/`##Inf`/文字列すべて無音受理し (「1 mission = bounded operation」契約が
NaN/Inf で無限に抜け得る)、nil id/robot/objective も `:planned` で正規化、
`telemetry-proof` も nil sensor/reading を無音受理。修理: mission 入口で
`:max-steps` に `(pos? x)` かつ `Double/isFinite` かつ integer? 検査 (非適合は例外化、
nil は「未設定」として明示許可なら 区別)、id/robot/objective の some? 検査、
telemetry-proof の sensor/reading some? 検査 — falsify-11/14〜17 の
有限性検査と同一パターンで rob 側入口 1 箇所にまとめられる。
