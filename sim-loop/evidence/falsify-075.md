# falsify-075 (H76) — governor silent-nil は下流で「許可側」に倒れるか (gate bypass)

## 仮説
H76: falsify-071 (H72) は「nil が gate/action-permitted? に渡れば :invalid→deny と
なるため、actuator 直送は成立しない」を**純静的読取で結論したが、当時 robotics
本体ソースは本 repo から観測不能 (falsify-072) で実測されていない**。nil action
(不正 kind/safety の kaigo-action 戻り値) が gate / action-permitted? で
拒否でなく許可・例外・無視のいずれかに倒れる経路があれば、falsify-071 の
「痕跡喪失のみで権限越境なし」の限定主張は破れる。

## 実測 (実行系, 1 回の軽量 kbb eval — falsify cheaply)
- HOST LOAD: 15min 21.25 ≈ 2.1× ncpu=10。深い実験 (test suite 全体 / seeded 再現) は
  gate 超につき回避し、governor+robotics 2 ns の単発 eval のみ実施 (falsify-074 の
  単発 eval 前例準拠、両 ns 合計 <300 行の純データ契約)。
- giemon HEAD: 41ac173f8e9d… (bench-274 と同一)。robotics worktree HEAD:
  ad99366bc7be… (maturity 基準値の robotics と同一)。
- 新事実: robotics 本体ソースはローカルに実在
  (orgs/kotoba-lang/robotics, .gitlibs/libs/io.github.kotoba-lang/robotics 両方)。
  falsify-072 の「本 repo から観測不能」は worktree 配置を見落とした探索の穴。
  robotics.cljk は (:require clojure.set) のみの自己完結 ns で、giemon classpath に
  robotics src を足すだけで kbb sci から load 可能 (governor ns も同時に load 可)。

1. `(gov/kaigo-action "A" "M" :otete :teleport)` → **nil** (不正 kind、silent nil 実測)。
2. `(gov/kaigo-action "A" "M" :otete :move :safety :nope)` → **nil** (不正 safety、同)。
3. `(rob/gate nil #{:medium})` → **#:gate{:decision :invalid, :reason :not-an-action}**。
4. `(rob/gate (rob/action "a" "m" :teleport :high) #{:high})` → **:invalid / :not-an-action**
   (rob/action が nil を返すため nil と同値経路)。
5. `(rob/gate (rob/action "a" "m" :move :medium) #{:medium})` → **:permit :action "a"**
   (对照: 正 action は素通り — gate は nil を特別扱いせず通常判定)。
6. `(rob/action-permitted? nil #{:medium})` → **false**。
- RC=0。静的整合: robotics.cljk L60-66 `action` は docstring に「Returns nil for an
  unknown kind or safety class」と明記 (silent nil は仕様書記載の挙動)、
  L124-125 `gate` の第 1 分岐 `(not (map? a))` → :invalid が nil を捕捉。

## verdict: **refuted** — H76 (nil が許可側に倒れる bypass) は不成立。
- nil / 不正 action は gate で :invalid(:not-an-action)、action-permitted? は false。
  権限越境経路は実測で存在しない。falsify-071 の限定主張 (痕跡喪失のみ・越境なし)
  は静的推論から**実測確定**に昇格。
- 逆に新規の残存リスク: 決定レコードが :invalid で gate 内に生成されるだけで、
  「作られたが nil になった」ことの audit 記録は依然どこにも無い (falsify-071/072
  の rejected レコード化推奨は実測後も有効・未着手)。
- 併せて測定経路の拡張が可能になった: giemon classpath + robotics src で governor
  ns が load 可能 → 暫定 21/52/0 緑は governor_test (6 tests) を含められる
  (本 run では suite 実行は load gate 上回避、未測定として記録)。

## 再現手順
```
cd /Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/giemon
git rev-parse HEAD        # 41ac173f8e9d...
kbb --backend sci --classpath "src:test:/Users/junkawasaki/github/com-junkawasaki/orgs/kotoba-lang/robotics/src" -e \
  "(require '[kotoba.giemon.governor :as gov] '[kotoba.robotics :as rob]) \
   (println :nil-kind (pr-str (gov/kaigo-action \"A\" \"M\" :otete :teleport))) \
   (println :gate-nil (pr-str (rob/gate nil #{:medium}))) \
   (println :permitted-nil (pr-str (rob/action-permitted? nil #{:medium})))"
# -> :nil-kind nil / :gate-nil #:gate{:decision :invalid, :reason :not-an-action} / :permitted-nil false, RC=0
```
生出力: /tmp/f075_kbb.txt, /tmp/f075_state.txt, /tmp/f075_robo.txt, /tmp/f075_robo2.txt。

no code change (本 bot は修正しない)。

コアへの 1 行メッセージ: silent-nil の権限面は実測で安全 (gate :invalid /
action-permitted? false) — falsify-071 限定主張は実測確定。残る破れは audit
記録不在のまま、rejected レコード化 + 負テスト 1 件を runner repair と同時に core 側へ
(falsify-071/072 推奨の再発行)。robotics src を classpath に足せば governor_test も
kbb 暫定測定経路に含められる。
