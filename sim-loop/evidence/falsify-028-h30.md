# falsify-028 (H30) — NaN/±∞ 角の silent NaN pose 化を検知できる既存面は 0 件 (refuted)

判定: **refuted** (決定的・負荷非依存・純静的行レベル読取。REPL 実行数字は捏造せず。
実行バックエンド (terminal) は date/uptime 空出力 exit 0、search/stat 不能、execute_code は
cron モード blocked、write_file/read_file のみ成立した真の応答不能条件での静的記録。)

仮説 H30: 「NaN/±∞ pose を検知できる既存面は 0 件。void を閉じる最小介入点は FK 自体の
数値 guard か `end-effector` での NaN 検証 (isNaN/isInfinite) の 2 択に収斂する。」
判定規則: 既存 falsify-001〜027 を集計し、角度列数値破れ (NaN/±∞) を参照・検知する面が
1 件でもあれば survived、皆無なら refuted。

## 集計 (行レベル静的読取、単一ソース確認済み)

角度列数値 (NaN/±∞) を消費・検知する面を全 src .cljc から列挙:

| 面 | 場所 | FK/角度数値への接触 | NaN/±∞ 検知 |
|---|---|---|---|
| forward-kinematics | arm.cljc 22–41, loop 38 `(or (first angles) 0.0)` | 消費 (角度から pose) | なし — NaN は truthy で 0.0 にならず |
| end-effector | arm.cljc 43–46 | `last`-only で FK の `:xf/pos` を返す | なし — count 検証も NaN 検証も無し |
| within-limits? | arm.cljc 15–20 | 角度を `<=` 比較のみ (RANGE) | なし — NaN は全 `<=` で false、isNaN 呼びは皆無 |
| axis-angle->rot | kinematics.cljc 42–50, 47 `(Math/cos angle) (Math/sin angle)` | `Math/cos`/`Math/sin` 直接呼び | なし — IEEE-754 で NaN/±∞ を例外なく NaN 化 |
| combine | kinematics.cljc 56–61 | `:xf/pos` に NaN 伝播 | なし |
| torque-headroom | arm.cljc 95–113 | FK も角度列も呼ばず void | — |
| underrated-joints | arm.cljc 115–121 | FK も角度列も呼ばず void | — |
| chain-actuators | arm.cljc 48–64 | FK も角度列も呼ばず void | — |
| bom | arm.cljc 66–93 | FK も角度列も呼ばず void | — |
| export (torque->csv/json) | export.cljc 53–79 | `arm/torque-headroom` のみ・FK 呼ばず | — |
| giemon (products) | giemon.cljc 1–42 | 製品メタデータのみ・FK 接触なし | — |
| governor | governor.cljc 1–68 | mission/action のみ・robotics 使用 | — |

## 結論

- 角度列数値破れ (NaN/±∞) を参照・検知する面は **0 件** — H30 は refuted。
- arm.cljc 1–121 + kinematics.cljc 1–67 全体に isNaN / isInfinite / NaN 比較 / assert **皆無**
  (falsify-027 と同確認)。`<=` 比較 (within-limits?) は NaN を恒常 false にするが false-reject
  側で、NaN pose を生成・伝播する FK/kinematics 経路 (falsify-027) には到達しない。
- void を閉じる最小介入点は (1) FK 入口 (arm.cljc 38) の isNaN/isInfinite guard か
  (2) 唯一の FK consumer (`end-effector`, arm.cljc 43–46) での NaN 検証の 2 択に収斂
  (H28/falsify-026 の「長さ guard or end-effector count 検証」の数値版と同型)。
- 現 API に DOF 実行入力面なしのため現 fixture では非発火、将来径路の numeric contract。
  コード修正はコア (giemon-sim) 側の対象であり本 bot は実施しない。
- 型混在 (string) 角は CCE loud で false-pass にならない (既存 falsify-027 と独立)。