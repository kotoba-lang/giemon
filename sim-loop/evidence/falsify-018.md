# falsify-018 — torque-headroom / BOM の joint 名対応契約 (重複名で静かに誤対応)

## 仮説 (1 iteration = 1 hypothesis)
H20: 「`kotoba.giemon.arm` の `torque-headroom` / `underrated-joints` / `bom` は
chain joint と actuator を joint 名で正しく対応づけ、joint 名の重複・override の
未知名・actuator データの異常 (nil/文字列) があっても rating の誤対応や静かな
誤判定 (false-pass) は起きない」。
反証対象の背景: falsify-010〜015 は governor/gate 面 (payload 検査) を入力空間全面
から潰したが、arm 側の torque/BOM 照合面 (actuator 割当の正当性の数字そのもの) は
未反証だった。

## 実測
probe (実装は REPL 経由で読むだけ、コード修正なし):
- `sim-loop/evidence/probe_bom_name_parity.cljk` — 重複名 / override / 未知名
- `sim-loop/evidence/probe_bom_nil_fields.cljk` — nil / 型不一致
- `sim-loop/evidence/probe_bom_real_fixture.cljk` — 実 fixture (giemon_arm6) への重複名攻撃
- `sim-loop/evidence/probe_bom_false_pass.cljk` — false-pass 方向の実証

主要数字 (すべて clojure -M で kotoba.giemon.arm を直接実行):

```
(a) 重複 joint 名 (j2 ×2, cont-nm 40 と 10):
  torque-headroom => 両行とも {:torque/rated 10, :torque/headroom -30}
  → 先頭行の真の rating 40 が by-name map 衝突で 10 に上書き (last-wins)

(b) 重複名への variant :override (cont-nm 10 を 1 件指定):
  bom => [{j2 model X cont-nm 10} {j2 model B cont-nm 10}]
  → keep-indexed が先頭 1 件だけ置換、2 件目は元のまま。BOM が
    variant 意図と食い違う状態で headroom が計算される

(c) override の未知 joint 名 (j99):
  bom は j99 を黙って BOM 末尾に追加 (エラーなし)
  torque-headroom は chain に無い行を無視 (エラーなし)

(d) actuator データ異常:
  cont-nm nil / effort nil / :joint/limit 欠落
    => NullPointerException (arm.cljc:113, "Object.getClass() x is null")
  effort/cont-nm が文字列
    => ClassCastException (String → Number)
  → 例外は出るが、呼び出し側が try で包めば「検査不能」を握り潰せる形

(e) 実 fixture giemon_arm6 (j1..j6, 正常読み):
  headroom = j1 0 / j2 0 / j3 +10 / j4 +6 / j5 0 / j6 +2.3、underrated=()
  (= arm_edn_test の契約と一致 — 基準線の確認)

(f) 実 fixture への重複名攻撃 (j2 の弱いコピー cont-nm 10 を chain 末尾に追加):
  両 j2 行とも rated 10 / headroom -30 に変化
  → 真の 40 N·m アクチュエータの行が静かに -30 と誤評価される

(g) false-pass 方向 (弱い j2=10 の後により強い j2=100 を重複):
  weak 単独: underrated = [{j2 rated 10 headroom -30}]  (正しく検出)
  弱い→強いの順で重複: headroom 両行 rated 100 / +60、underrated = ()
  → 実際に 10 N·m しかない j2 が検証を静かに通過する
```

決定的確認: 各 probe 2 回実行、測定出力は diff 0 行
(/tmp/f18a vs /tmp/f18a2 の差分は crash-report の tmp ファイル名のみ、
測定行は同一。/tmp/f18h, /tmp/f18i は cmp 一致)。

到達性: 現 fixture は joint 名が一意 (j1..j6) で赤は顕在化しない。
赤は「joint 名を key にした対応が last-wins で衝突を黙って解決する」という
契約として、DR / variant パイプライン / importer が chain を再構築・複製する
将来経路 (duplicated names、variant override の部分適用) で発火する。
false-pass (g) は underrated-joints が安全側ではなく危険側に落ちる点で、
arm_edn_test `default-bom-meets-chain-torque-test` 同種の検証を無効化しうる。

## verdict
**refuted** — H20 の「重複名・異常入力でも誤対応 / false-pass は起きない」は破れた。
(a) 重複名は last-wins で rating を誤対応 (40 の行が -30 と誤評価)、
(g) 弱い→強い重複で実際に under-rated な joint が underrated-joints を
空で通過 (false-pass)。現 fixture では発火しない (名前一意)。

## コア (giemon-sim) への 1 行メッセージ
falsify-018: H20 refuted — torque-headroom/bom の joint 名対応は by-name map の
last-wins で重複名を黙って衝突解決し、弱い→強い重複では実際に under-rated な
joint が underrated-joints を空で通過する (false-pass、weak 単独なら正しく
-30 検出)。重複 joint 名の検出 (error か dedup) と nil/型不一致の明示的
バリデーションが要修理 (現 fixture は名前一意で顕在化せず)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
clojure -M -e '(load-file "sim-loop/evidence/probe_bom_name_parity.cljk")'    # (a)-(d)
clojure -M -e '(load-file "sim-loop/evidence/probe_bom_nil_fields.cljk")'     # (d) 分離
clojure -M -e '(load-file "sim-loop/evidence/probe_bom_real_fixture.cljk")'   # (e)(f)
clojure -M -e '(load-file "sim-loop/evidence/probe_bom_false_pass.cljk")'     # (g)
```
2 回実行して測定出力が一致することを確認済み (決定的)。

## 補足
- コード修正なし (probe は evidence 配下の測定専用、実装は読むだけ)。
- 決定的・タイムスタンプなしで記載。
- HOST LOAD 高 (load averages 27.59 21.90 27.12) につき軽量 REPL 数値 probe
  のみで完了 (falsify cheaply、数値積分・長時間 sim は省略)。
- ツール環境メモ: terminal stdout が空で返る障害が継続中のため、出力は
  /tmp ファイルへのリダイレクト + read_file で取得した (falsify-009 と同じ回避策)。
