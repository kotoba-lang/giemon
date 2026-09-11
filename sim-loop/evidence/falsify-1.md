# falsify-1 — EDN 正本の :arm/chain が EDN データではなく文字列リテラル

## 仮説

maturity spec/契約軸 (score 2) の根拠「URDF パリティオラクルは既存 (fixtures/giemon_arm6/)」を反証する。
giemon_arm6.edn は正本 EDN として `from_edn(edn) == parse_urdf(urdf)` 検証に耐えるはず、
すなわち EDN リーダが読んだ結果に joint/link データが EDN 構造として存在するはず。

## 実測

- `clojure.edn/read-string` で fixtures/giemon_arm6/giemon_arm6.edn を実際に読んだ。
- top-level: PersistentVector, count 1。先頭 map の値の型:
  - `:arm/chain` -> **java.lang.String** (長さ 3312, 中に `:joint/name` 6 回)
  - `:arm/realization` -> **java.lang.String** (中身 `{:status :gate0-resolved, ...}`)
  - `:arm/solver` `:arm/units` `:arm/convention` `:arm/base` -> String (想定どおり)
  - `:arm/dof` -> Long (=6)
- つまり joint chain (j1..j6 の axis/origin/limit/inertial/actuator 全部) と
  realization 変種が **二重引用符でエスケープされた文字列リテラル** として埋め込まれており、
  EDN リーダの結果には joint/link の EDN 構造が 1 つも存在しない。
- ファイル grep も同結果: `grep -c ':joint/name "j1"'` -> 0 (実ファイルは `\"j1\"`)。
- URDF 側は正常にパース可能 (joint 6 / revolute, limit 6, link 7)。
- URDF↔EDN の数値比較は実施不能 (比較対象の EDN 側データ構造が存在しないため)。

## verdict

**refuted** — 「EDN 正本が from_edn/parity-oracle 検証に耐える」主張は、
EDN リーダで読んだ時点で破れている。現状の EDN は人間可読ドキュメントであって、
データとしての正本になっていない。kami-genesis 側の from_edn は
chain 文字列をさらに read-string する回避ルートを持たない限り joint を取得できない。

## 再現手順

```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
kbb -M -e "(require '[clojure.edn]) (prn (mapv (comp type val) (first (clojure.edn/read-string (slurp \"fixtures/giemon_arm6/giemon_arm6.edn\")))))"
# => :arm/chain が java.lang.String であることを確認
grep -c ':joint/name "j1"' fixtures/giemon_arm6/giemon_arm6.edn   # => 0
```

## コアへの 1 行メッセージ

giemon-sim へ: fixtures/giemon_arm6/giemon_arm6.edn の :arm/chain と :arm/realization が
文字列リテラルで、EDN として joint データが存在しない — chain を実際の EDN ベクタに展開しないと
URDF パリティ (L0) は定義上達成できない。
