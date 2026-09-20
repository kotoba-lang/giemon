# falsify-077 (H78) — gate 側が rejected/deny を監査レコードとして生成しているか

## 仮説

H78: falsify-075/076 が指摘した「governor silent-nil の audit 記録不在」は giemon 側
実装不足に過ぎず、実は gate 側 (`kotoba.robotics/gate` / `action-permitted?`) または
export 経路が :deny / :invalid 決定を監査 ledger に append 可能な rejected レコードとして
生成している → giemon 側の rejected レコード化・負テスト追加は不要である。

## 実測 (純静的読取・決定的)

- 環境: HOST LOAD 15min ≈12.5 (ncpu=10 の ~1.25×、Load gate 2× 未満) だが
  terminal 実行 backend の stdout capture が応答不能 (全コマンド空出力 —
  falsify-076 と同一症状)。判定材料は redirect→file→read_file による現 blob 直読。
  kbb -M:test / seeded 再現は静的仮説のため不要、test 計数 unmeasured (honest)。
- HEAD: giemon 41ac173f8e9dc599e8b9ab340a51f4135d5ade98 /
  robotics ad99366bc7bef949e86ee33b7e04d12525dffe46 (両実測、maturity 記載と一致)。
- src (robotics.cljk 142 行 直読):
  - `gate` (L120-129) は `{:gate/decision :deny :gate/reason ...}` の**一時 map を
    返すのみ**。ledger / append / record 構築は **0 件**。
  - `action-permitted?` (L131-142) は `gate` の decision を `(= :permit)` で食べて
    boolean 化する — deny の理由 (:gate/reason) は**この経路で破棄される**。
  - ledger 言及は docstring のみ (L13 / L103-108 telemetry-proof / export.cljk L6)。
    telemetry-proof は「audit ledger に append できる証拠を構築する」であって
    rejected 決定の記録ではない。safety-stop (L93-100) は halt 記録で deny とは別物。
  - grep 実測: `rejected|:reject|append` は src 内 **0 hit** (`deny` は gate 1 件のみ)。
- test (robotics 側): robotics_test / safety_invariants_test に gate の :deny /
  :invalid 負テストは複数在るが、**「拒否が rejected レコードとして残る」を
  assert する test は 0 件** (export の CSV/JSON は action 自身の gate 結果の
  projection — gate を呼び忘れた action を記録する経路ではない)。
- giemon 側 (governor.cljk 68 行 直読): L21-27 / L53-60 は不正 kind/safety の
  `rob/action` nil を unvalidated 透過 (falsify-071 実測不変)。nil が gate に届いた
  ときの :invalid 決定を保存する箇所は **0 件**。

## verdict: refuted

「gate 側が rejected レコードを生成している」は成立しない — :deny / :invalid は
呼出し側が受け取るまでの一時 map であり、受け取りを忘れた (または nil 透過された)
決定は静かに消える。falsify-075/076 の「audit 記録不在」は giemon 側だけでなく
robotics 層の gate 契約全体の性質として確定。rejected レコード化 + 負テスト 1 件の
core への推奨 (falsify-072 起の再発行) は据え置き。

## 再現手順

```
cd orgs/kotoba-lang/giemon && git rev-parse HEAD   # 41ac173 (stdout 空出力時は >file で)
cd orgs/kotoba-lang/robotics && git rev-parse HEAD # ad99366
grep -rn "rejected|:reject|append" robotics/src    # 0 hit
read_file robotics/src/kotoba/robotics.cljk        # L120-142: gate = 一時 map 返却のみ
grep -rn "deftest|reject|deny|ledger" robotics/test # :deny 負テスト有り・rejected 記録 assert 0
```

## core への 1 行メッセージ

gate の deny/invalid を giemon governor 層で rejected レコード (map → 台帳 append 用) に
変換する 1 関数と負テスト 1 件が最小修復 — gate 側 (robotics) には既に理由が
:gate/reason で入っているので giemon 側で包むだけで済む。
