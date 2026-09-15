# bench-264

- 日時: 2026-09-15 (JST), 決定的記録
- 負荷: load 15min 91.81 / ncpu 10 ≈ 9.2x → **load 超過により test スイート実測を省略**
- HEAD: robotics ad99366bc7bef949e86ee33b7e04d12525dffe46 / giemon 00fd23f9d04743323047c8c29c30aa18320daa70 (bench-263 と同一、不変)

## 判定: skipped (load)

- kbb -M:test (robotics / giemon 両 suite) は実行しなかった。host load が高く、
  このセッションでは重い測定を省略する規約に従った (「skipped (load)」と正直に記録)。
- 基準値 robotics 23/558/0・giemon 46/115/0 との比較: **unmeasured**。
- silent-zero 状態 (両 suite 0/0/0 RC=0、bench-244〜263 で 20 連続観測) の継続有無は
  本走では測定していない。 repaired / unchanged のいずれとも断定しない。

## seeded 再現

- skipped (load)。sim-loop は L0、学習ジョブ無し (bench-263 と同一前提)。

## 回帰

- 検出なし (測定省略のため)。回帰 assert も行わない (honest skip)。

## 再現コマンド

```
cd orgs/kotoba-lang/robotics && kbb -M:test
cd orgs/kotoba-lang/giemon   && kbb -M:test
```

## falsify 状態

- 変更なし。falsify-034 (FK guard repair 未実装) 残存。falsify-069 (JVM .cljk ロード不能)
  による runner silent-zero の修復は未着手 —— NEXT の最優先項目のまま。

## コード変更

- なし (bot は測定・記録のみ)
