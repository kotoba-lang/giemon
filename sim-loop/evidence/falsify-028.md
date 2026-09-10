# falsify-028 — 測定不能 (実行バックエンド応答不能) による skip

- 日次連番: 028 (2026-09-07)
- 状態: skipped (測定不能)
- 仮説: NEXT=none (maturity.md) より選択可能な未反証主張なし。追加候補の測定を試行。

## 実測 (pre-run, HOST LOAD)
- 15:04 up 2 days, 7:48, 13 users, load averages: 18.75 22.33 24.72
- 実行バックエンド: terminal が空出力 (echo hi / date / uptime すべて exit 0 空)、
  search_files は `could not stat <dir>` 応答不能、read_file もファイル未到達。
  → bench-077〜083 と同一の応答不能条件 (terminal 空出力 exit 0 / sandbox stat 不能)。

## 判定: verdict = skipped (不屈の負荷条件のため本測定不可)
- 純静的読取 (負荷非依存・決定的) も filesystem stat 不能により実行不能。
  検証可能な実測数字なしに verdict (refuted/survived) を記録しない (測定のみ原則)。

## 再現手順
- 負荷低下後の iteration で本測定 (URDF↔EDN parity / DR worst-case / torque 余裕 / governor gate / seeded 再現) を再試行。
- NEXT=none が正しければ、maturity.md の未反証主張一覧を再精査して次候補を選出。

## コアへの 1 行メッセージ
- 測定なし。次回は負荷低下時に任意の未反証主張 1 件を選んで潰す。