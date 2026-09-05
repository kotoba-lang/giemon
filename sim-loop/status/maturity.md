# giemon シミュレーション学習 成熟度 (正本)

現在段階: L0 (URDF→scene 読み込みパリティ未達)

## 7 軸スコア (ADR-2608052000 準拠, 0-5)

| 軸 | score | 根拠 |
|---|---|---|
| spec/契約 | 1 | fixtures/giemon_arm6 EDN は存在するが falsify-1 で refuted: :arm/chain が文字列リテラルで EDN データとして joint/link が存在せず、パリティオラクルとして機能しない。falsify-4 で fixture 未修理を再確認、本 cron (bench-34 時点) でも fixture ファイル mtime が 7 月 24 日のまま未変更 (:arm/chain / :arm/base / :arm/realization の二重エンコード String 形も存続を実測再確認) |
| 実装 | 0 | シミュレーション学習コードなし (bench-7 でも giemon/src/kotoba/giemon/ は arm/chassis/export/governor/kinematics/ui/viewer のみ、src 配下に `seed` を含むファイル 0 件と再確認) |
| テスト | 2 | bench-4〜34 と 31 連続で同一数字を再確認: robotics 14/50 + giemon 46/115, 0 failures 0 errors (bench-20〜34 cron 実測含む、回帰なし)。学習パイプラインのテストは依然なし |
| 反証 | 3 | falsify-1 refuted / falsify-2 survived (2 段階 read で joint 6 数値パリティ) / falsify-3 survived (link 数値パリティ) / falsify-4 survived (ドリフト検査: 2 段階 read で joint 6 / link 6 完全一致のまま、fixture 未修理)。falsify-5 survived: 実コード `kotoba.giemon.arm/torque-headroom` + `underrated-joints` を 2 段階 read の fixture で実行 -> underrated 0 件 (headroom: j1/j2/j5=0, j3+10, j4+6, j6+2.3)、`:arm/realization` の主張 (肩40律速・j5余裕僅少) と数値整合。falsify-6 refuted: `arm/bom` は不明 variant 名 (typo) で nil を返し、`underrated-joints` が例外なく無音 0 件になる fail-open 迂回路を実測 (対照: 違反 actuator を override に仕込んだ本物の入力は正しく 1 件検出、迂回は nil 伝播経路のみ)。付帯観察: `:arm/base` に加え `:arm/realization` も二重エンコード String で、修理対象は 3 キー。bench-1 not-run のまま。falsify-7 refuted: governor facade `kaigo-action`/`ops-action` は未知 product 名 (typo) で例外を出さず `:medium` に黙示降格する action を生成 (ops-roles の :caterpillar=:high が `:caterpilar` typo で :medium になり `#{:low :medium}` 許可セットで通過)、fail-open 迂回路を実測。falsify-8 refuted: falsify-7 と同一クラスの降格が nil product と文字列 product (`"caterpillar"`) でも実測 — `ops-action` は ops-roles の `:caterpillar=:high` を黙示 `:medium` に落とし、許可セット `#{:low :medium}` の gate で `:permit` が通る (対照: keyword `:caterpillar` は `:high`、文字列 safety は rob 側で action 生成 nil → :invalid と fail-closed 正常)。迂回路は facade の `(get-in roles [product :default-safety] :medium)` デフォルト解決に集約され、falsify-6/7 と同一修理箇所。falsify-9 refuted: デフォルト解決に加え明示 `:safety` キーワードも無検査で採用され、`:caterpillar` (posture :high) に `:safety :low` を渡すと同一 gate-set `#{:low :medium}` でデフォルト経路 `:deny` が `:permit` に変わる実測 (kind/params 同一、対照: 正しい ops gate-set では override は `:deny`、default は `:require-sign-off` で rob 側は fail-closed 維持)。迂回面は facade の caller 指定 safety 無検査採用まで拡大、修理は falsify-6/7/8 と同一 facade。falsify-10 refuted: actuator 未割当 joint は `chain-actuators` の `keep` で黙って除外され、`underrated-joints` は truthy な `()` (違反 0 件) を返す fail-open を実測 — joint-count 6 vs BOM 5 の構造的不整合も無検出、nil ガードでも検知不能 (`()` は truthy)。対照: 不良 `:cont-nm` (nil/文字列) は NPE/CCE で fail-closed。falsify-11 refuted: `:cont-nm` / `:effort` の `##NaN`・`##-Inf` は headroom をセンチネルにし `neg?` フィルタを無音通過して違反 0 件で合格 (例外にも違反検出にもならない第 3 経路、`##-Inf` 要件は有限 40N·m で `##Inf` headroom の無音合格)。`##NaN` は合法 EDN リテラルで直接入り得る。falsify-13 refuted: `rob/gate` は allowed-set を無検査 `(set x)` 強制するため、許可セットに nil が混入した構成 (`(conj #{:low :medium} nil)`) では `:action/safety nil` の生マップ action (rob/action 非経由、kind :actuate) が nil メンバーシップ一致で無音 `:permit` を実測 (対照: 許可セット単独破損 nil/空/文字列/数値/map は deny か例外で fail-closed、nil 無しセットでは deny、正規生成 action は rob/action が nil-safety を生成不能のため経路不成立、list/vec セットは set 強制で正常機能)。成立は gate 入力 2 つの組合せ破損 (nil 含みセット ∧ nil-safety 生マップ)。falsify-12 の kind×class 結合欠落と畳なって nil-safety hardware actuate が通る。修理は gate 側: allowed-set の nil/非 keyword 除去検査 + `:action/safety` nil を `:invalid` 化 (両方推奨)。falsify-14 refuted (cron で確定、repl 記録 falsify-14.repl と整合): 運動学入力の縮退化 2 面を実測 — `k/normalize` 零ベクトル通過で axis `[0 0 0]` + θ=π の FK が det −1 鏡映 (`diag(-1,-1,-1)`) を例外無し生成 (対照: 正しい axis は det +1、位置は並進のみで生存し破綻が見えない) ので `normalize` 零ベクトル例外化 (または joint-transform 入口の axis norm 検査) を、`within-limits?` が ±Inf 境界 (`:upper ##Inf` で 1e9 rad 判定 true) を無音受理するため lower/upper の `Double/isFinite` 検査を修理リストに追加 (後者は falsify-11 の有限性検査と同一箇所。対照: `##NaN` は比較の副産物で偶然 fail-closed、nil bounds は deny)。falsify-15 refuted (コア bot 追記分、cron で採点反映): `forward-kinematics` は `:joint/type` を一切見ず (src 参照 0 件、revolute 専用の `k/joint-transform` を type 無視で呼ぶ) — j6 を `:prismatic` にすると 0.5 m 変位が 0.5 rad 回転として適用され `:revolute` と pose 完全一致、未知 type `:screw` も同一 pose。角度列の過不足・nil も 0.0 補完/切捨てで無音完走、`##NaN` 角度は NaN 回転行列が例外無しで pose まで伝播 (対照: 文字列角度のみ CCE で fail-closed)。修理: joint-transform 入口の `:joint/type` 分岐 (prismatic は並進、未知 type は例外) + FK 入口の `(count angles) == (count chain)` 検査 + 角度の `Double/isFinite` 検査 (falsify-11/14 と同一修理箇所)。falsify-16 refuted (cron で確定): chassis track-drive の `twist->track-speeds` は `track-width` を無検査で — 負幅は `:twist/angular` の符号を無音反転 (往復変換は自己無矛盾で `fwd∘inv` セルフチェック不能、統合 pose の theta ±2.0 rad に直流出)、零幅の逆変換は回転コマンドを無音に捨てて直進 speeds を返す (前方変換は Divide by zero で fail-closed、正逆で非対称)。`##NaN`/`##Inf` width・speeds も素通り (`turning-radius` ##NaN 返却、`integrate-pose` NaN 伝播、dt=-1.0 の時間反転も無音通過)。修理: 両関数の track-width 入口で `(pos? width)` かつ `Double/isFinite` 検査 + speeds/dt の有限性検査 (falsify-11/14/15 の有限性検査と同一修理箇所)。falsify-17 refuted (前 cron で採点反映): export.cljc の `torque->json` / `bom->json` は数値を有限性無検査の `(str ...)` 補間で出すため、falsify-11 で無音侵入が実測済みの `##NaN`/`##-Inf` が生 `NaN`/`-Infinity` トークンとして監査 JSON に出力される (RFC 8259 違反: 厳格パーサは例外・cheshire は無音受理で可否がパーサ依存、CSV は NaN 正規装いの無音破壊) — falsify-11 の fail-open が出力層で増幅される第 3 面。falsify-18 refuted (本 cron で確定): export.cljc の `csv-cell` は `,` `"` `\n` `\r` の構文検査のみでフィールドの意味検査を持たず、`:model`/`:buy` 先頭の `=` `+` `-` `@` / タブが CSV formula injection として引用の有無にかかわらず read-back で危険値のまま復元 (5 形状全滅、対照: `bom->json` は同一入力で strict JSON 往復無害、破れは CSV 層のみ)。falsify-19 refuted (本 cron で確定): `rob/gate` は allowed-set と `:action/safety` の型を検査しないため、両側に同一の非 keyword 値 (文字列) が入った構成では無音 `:permit` — 文字列 `"low"` 混入セット ∧ 文字列-safety 生マップ action で `:actuate` が permit (action-permitted? も true)、さらに `safety-classes` 正規集合を一切参照しないため未知クラス文字列 `"not-a-class"` の両側一致でも permit、文字列 `"high"` は `human-sign-off-classes` (keyword のみ) の contains? で false になるためサインオフ要求自体を迂回できる構造的余地も実測 (同一コードパスから従う)。単独破損は fail-closed 維持 (文字列 action + keyword セット → deny、keyword action + 文字列セット → deny)、成立は falsify-13 と同じ gate 入力 2 つの組合せ破損で nil face の文字列版。修理は falsify-13 と同一箇所 (gate L124-129) の拡張: allowed-set の nil/非 keyword 全般の除去 (または検出時例外) + safety 非 keyword (nil 含む) の `:invalid` 化 + (望むなら) gate 内の `safety-classes` 正規集合照合 — falsify-13 案の「nil のみ除去」では不十分。falsify-20 refuted (本 cron で確定): `bom->json` の数値スロット (cont_nm/peak_nm/price_jpy) は型検査なしの `(str ...)` 生補間で、合法 EDN 文字列 `:cont-nm "0,\"audit_injected\":true"` が JSON 構造注入として **厳格パーサ通過で偽キー混入** (`audit_injected: true` が監査レコードに乗る、falsify-17 より深い監査改変面)、`"0}"` は構造破壊の無音不正 JSON 出力 (strict で JSONDecodeError)。対照: torque 経路は `torque-headroom` の減算で CCE fail-closed、csv-cell は `,` 引用で文字列セル往復 (破れは BOM JSON 出力側に集中)。修理: falsify-17 の非有限検査を「Number かつ finite のみ数値スロットに出す」型検査へ拡張 (非数値は例外化または `json-str` 経由引用文字列化) — falsify-17/18 と同一の export 層入口 1 箇所。falsify-21 refuted (本 cron で確定): `arm/torque-headroom` は BOM を `:joint` 名キーの map に潰すため同名 joint 重複 (`:joint/name "j1"` × 2) で required↔rated の位置対応が無音破れ — weak actuator (cont 3.0) の本命 joint1 (required 5.0) に strong の 12.0 が転用され headroom -2.0 (underrated) が +7.0 に変換され `underrated-joints` が無音空、`bom` の variant override も同名 2 件目に届かず検証経路から無音脱落。修理: `chain-actuators` (または torque-headroom 入口) で joint 名 distinct 検査 (重複は例外化) — falsify-6/10/11 の BOM 件数検査と同一箇所に追加可能。falsify-22 refuted (本 cron で確定): `chassis/turning-radius` は非有限速度を無検査で — pivot (+Inf/-Inf) が `(zero? (+ left right))` 判定漏れで `##NaN` 半径、無限大両輪 (±Inf) は `(== left right)` true で**「直進」nil に誤判定** (直進契約の偽陰性)、NaN 速度は無音 `##NaN` 半径; `integrate-pose` は dt/theta 非有限を無音伝播 (全座標 NaN/Inf、例外なし)。対照: nil は NPE で fail-closed、1e308 対・-0.0・微小差は正常 — 破れは非有限のみ。修理: turning-radius 入口の `Double/isFinite` 検査 + integrate-pose の dt `(pos? dt)` かつ finite + linear/angular 有限性検査 — falsify-16 の track-width/dt 検査と同一箇所 (chassis.cljc 入口 1 箇所) |
| 再現性 | 0 | seeded 学習ジョブ未整備 (bench-1〜33: 再現実行 skipped/not-run)。bench-33 でも対象不在のため not-run (`grep -rl seed src` → 0 件、本 cron で実測再確認)。重い追加実験は skipped (load): load 約 43-65 / コア 10 |
| governor 統合 | 1 | kotoba.robotics gate 契約は存在、学習ループ未接続。falsify-7 で gate 単体の fail-closed 性は実測確認 (`rob/gate nil` → `:decision :invalid`, 不明クラス action は nil)、迂回は giemon facade のデフォルト解決経路のみ。falsify-8 でも facade 経由の nil/文字列 product で :permit 到達を再実測 (rob 単体は fail-closed を維持)。falsify-9 では明示 `:safety :low` キーワード指定でも同一 gate-set で :permit 到達を実測 — 迂回面はデフォルト解決に限定されず、caller 指定 safety の無検査採用を含む (rob 側は fail-closed 維持)。falsify-12 では `:actuate :none` が rob/action 直と facade (ops-action/kaigo-action 明示 `:safety :none`) の両方で合法レコードとして生成され、`:none` 含み許可セット (`#{:none :low :medium}`) の gate で無音 :permit を実測 (`:move`/`:grasp`/`:emit` も同型、action-permitted? も gate 委譲で同一)。対照: 未知 class は action 生成 nil で fail-closed、`:sense :none` は正当読み取り経路。入力破損不要の正規 API 経路で、rob 側にも初めて迂路面が確認された (kind×class 結合不変条件の欠落)。falsify-13 では gate 第 2 引数 (allowed-set) 側の破損経路も実測: 許可セットに nil 混入 ∧ nil-safety 生マップの組合せで actuating action が無音 :permit (許可セット単独破損は fail-closed 維持) — gate 修理は allowed-set の nil 除去検査 + nil-safety `:invalid` 化を falsify-12 の kind×class 結合検査と並行で適用すること。falsify-19 では文字列 face も実測 — 両側同一文字列 (`"low"` 混入セット ∧ 文字列-safety 生マップ) で `:actuate` が無音 :permit、未知クラス `"not-a-class"` も通過 (gate は `safety-classes` 正規集合を参照しない)、文字列 `"high"` でサインオフ迂回の構造的余地 — falsify-13 の gate 修理案は「nil のみ」でなく非 keyword 全般の型検査に拡張必須 |
| 運用 | 3 | bench-4〜33 と 30 連続でテスト実行・緑記録 (cron ループが指示に応答して定常稼働)。収集スクリプト giemon_sim_state.sh 存在確認済み。bench-5〜33 は負荷高水準 (bench-29〜33: load 約 27-65 / コア 10) でも軽量テストは維持し重い実験を skipped (load) とする方針を運用できた |

## OPEN 赤

- falsify-1 (refuted): fixtures/giemon_arm6/giemon_arm6.edn の :arm/chain / :arm/realization が
  二重引用符エスケープ済み文字列リテラルであり、EDN リーダで読んでも joint/link データ構造が
  出てこない。パリティオラクルとして不成立。fixture 未修理を bench-18 時点でも再確認
  (bench-17/18 とも falsify-1 の修理は未着手、cron 再確認でも grep 1 のまま)。
  (falsify-2/3 により修理のデータ損失リスクは 0 済み: joint 6 / link 7 とも URDF と数値完全一致。
   falsify-4 で再確認: ドリフトなし、:arm/base も二重エンコードのまま修理対象)
- falsify-6 (refuted): `kotoba.giemon.arm/bom` が不明 variant 名 (typo) で nil を返すと
  `underrated-joints` が例外なく無音 0 件を返す fail-open 迂回路
  (違反 actuator を override に仕込んだ本物の入力は正しく検出されるため、
   修理は bom nil 時の fail-closed 化: 例外 or 明示エラー)。
- falsify-7 (refuted): `kotoba.giemon.governor` の `kaigo-action`/`ops-action` が
  未知 product 名 (typo) で例外を出さず `:medium` に黙示降格する fail-open
  (ops-roles の `:caterpillar` は :high を宣言するが、`:caterpilar` typo の action は
  `:safety :medium` で生成され `#{:low :medium}` 許可セットで gate を素通し)。
  `rob/gate`/`rob/action` 自体は fail-closed で健全 (nil action → `:decision :invalid`)。
  falsify-8 (refuted) で同一クラスの降格が nil product と文字列 product (`"caterpillar"`) でも
  再実測 — いずれも `#{:low :medium}` 許可セットで `:permit` に到達 (文字列 safety は rob 側で
  fail-closed 正常)。修理は facade の `(get-in roles [product :default-safety] :medium)`
  既知 product 以外例外化 (fail-closed) で falsify-7/8 を一括解消。
- falsify-9 (refuted): facade は明示 `:safety` キーワードも無検査で採用する —
  `:caterpillar` (posture :high) に `:safety :low` を渡すと、同一 gate-set `#{:low :medium}` で
  デフォルト経路 `:deny` だった action が `:permit` に変わる
  (対照: 正しい ops gate-set では override `:deny` / default `:require-sign-off`、rob 側は健全)。
  迂回面は caller 指定 safety の無検査採用まで拡大、修理は falsify-6/7/8 と同一 facade
  (明示 `:safety` は product 設定 posture に対し昇格のみ許可、降格は拒否)。

- falsify-10 (refuted): `arm/chain-actuators` は `:joint/actuator` の無い joint を `keep` で
  黙って落とし、`underrated-joints` は truthy な `()` を返して違反 0 件として通過する
  fail-open (joint-count 6 vs BOM 5 の構造的不整合も無検出、nil ガードでも検知不能)。
  design effort 40 の肩関節 j1 が評価対象から消えても検証は「通る」。
  対照: 不良 `:cont-nm` (nil/文字列) は NPE/CCE で fail-closed — 欠落だけが無音で通る。
- falsify-11 (refuted): `:cont-nm` / `:joint/limit :effort` の `##NaN`・`##-Inf` は
  headroom をセンチネルにし `neg?` フィルタを無音通過して違反 0 件で合格する
  (nil/文字列でもない第 3 経路、`##NaN` は合法 EDN リテラルで直接入り得る)。
  `##-Inf` 要件は有限 40N·m レーティングで `##Inf` headroom の無音合格。
  falsify-6/10/11 は同一 fail-open 族 (欠落/未割当/非有限) で、修理箇所は
  `arm/bom` fail-closed 化 + joint/BOM 件数一致検査 + rated/required の isFinite 検査に集約。
- falsify-12 (refuted): `kotoba.robotics/action` は actuating kind (:actuate/:move/:grasp/:emit)
  と `:safety :none` の組み合わせを例外なく合法レコードとして生成する
  (kind×class 結合不変条件の欠落)。gate は class メンバーシップしか見ないため、
  `:none` を含む許可セット (`#{:none :low :medium}`) で無音 `:permit` 直行
  (`action-permitted?` も gate 完全委譲で同一、facade `ops-action`/`kaigo-action` の
  明示 `:safety :none` も同一経路)。入力破損不要の正規 API 使用で成立する点で
  falsify-6〜11 の fail-open 系と別経路。対照: 未知 class は action 生成 nil で fail-closed、
  `:sense :none` の正当読み取り専用経路。修理は rob 側の kind×class 結合検査
  (`actuates-hardware?` かつ `:none` → gate 構造的 deny or 生成時例外、`:sense :none` は温存)。
- falsify-13 (refuted): `rob/gate` は allowed-set を無検査 `(set x)` 強制するため、
  許可セットに nil が混入した構成 (`(conj #{:low :medium} nil)`) では
  `:action/safety nil` の生マップ action (rob/action 非経由、kind :actuate) が
  nil メンバーシップ一致で無音 `:permit` する。
  対照: 許可セット単独破損 (nil/空/文字列/数値/map) は deny か例外で fail-closed、
  nil 無しセットでは deny、正規生成 action は rob/action が nil-safety を
  生成不能のため経路不成立、list/vec セットは set 強制で正常機能。
  成立は gate 入力 2 つの組合せ破損 (nil 含みセット ∧ nil-safety 生マップ) で、
  falsify-12 の kind×class 結合欠落と畳なって nil-safety hardware actuate が通る。
  修理は gate 側: allowed-set の nil/非 keyword 除去検査 +
  `:action/safety` nil の action を `:invalid` 化 (両方推奨)。
- falsify-14 (refuted): 運動学入力の縮退 2 面。`k/normalize` は零ベクトルを素通し
  (kinematics.cljc L22-27) するため、joint `:axis [0 0 0]` の `axis-angle->rot` は
  Rodrigues が `diag(cos θ, cos θ, cos θ)` に縮退し、θ=π で `diag(-1,-1,-1)`
  det −1 の**鏡映**が例外無しで FK pose になる実測 (j6 axis 置換 + θ=π で
  end-effector rot det=-1、正しい axis なら det=+1)。位置は並進のみで生存し
  破綻が見えない。加えて `arm/within-limits?` は lower/upper を `some?` 検査のみで
  有限性を検査しないため `:upper ##Inf` / `:lower ##-Inf` が 1e9 rad を無音
  「制限内」判定 (`##NaN` は比較が false になる偶然 fail-closed、nil bounds は deny)。
  torque 経路 (falsify-6/10/11) と同型の無音不良入力採用が運動学側にも存在。
  修理: `normalize` 零ベクトル例外化 (または joint-transform 入口で axis norm 検査) +
  `within-limits?` の lower/upper `Double/isFinite` 検査 (falsify-11 の有限性検査と
  同一修理箇所で済む)。
- falsify-15 (refuted): `forward-kinematics` は `:joint/type` を一切見ず
  (src 参照 0 件、revolute 専用の `k/joint-transform` を type 無視で呼ぶ)。
  j6 を `:prismatic` にすると 0.5 m の変位が 0.5 rad の回転として適用され、
  `:revolute` と pose 完全一致 (= true)、未知 type `:screw` も同一 pose。
  角度列の過不足・nil も 0.0 補完/切捨てで無音完走 (8 個→余分切捨て、
  2/3 個→0.0 補完、nil→0.0)、`##NaN` 角度は NaN 回転行列が例外無しで
  pose まで伝播。対照: 文字列角度のみ CCE で fail-closed。型契約 (EDN の
  type 宣言) と実装の不一致で、DR 撹拌・呼び出し側バグが誤 pose として静かに流れる。
  修理: joint-transform 入口の `:joint/type` 分岐 (prismatic は並進、
  未知 type は例外) + FK 入口の `(count angles) == (count chain)` 検査 +
  角度の `Double/isFinite` 検査 (falsify-11/14 と同一修理箇所)。
- falsify-16 (refuted): `kotoba.giemon.chassis` track-drive の
  `twist->track-speeds` は `track-width` を無検査で — 負幅は
  `:twist/angular` の符号を無音反転させ、往復変換が自己無矛盾なため
  `fwd∘inv` セルフチェックでも検出不能 (同一 track speeds + 幅符号 1 文字
  違いで統合 pose の theta が +2.0 ↔ -2.0 rad)。零幅の逆変換は回転
  コマンドを無音に捨てて直進 speeds を返す (前方変換は例外で fail-closed、
  正逆で非対称 — ピボット命令が直進として実行され得る)。
  `##NaN`/`##Inf` width・speeds も素通り (`turning-radius` ##NaN 返却、
  `integrate-pose` NaN 伝播、dt=-1.0 の時間反転も無音通過)。
  修理: 両関数の track-width 入口で `(pos? width)` かつ `Double/isFinite`
  検査 + speeds/dt の有限性検査 (falsify-11/14/15 の有限性検査と同一修理箇所)。
- falsify-17 (refuted): `kotoba.giemon.export` の `torque->json` / `bom->json` は
  数値を有限性無検査の `(str ...)` 補間で出すため、falsify-11 で無音侵入が実測済みの
  `##NaN` / `##-Inf` が生 `NaN` / `-Infinity` トークンとして監査 JSON に出力される
  (RFC 8259 違反: 厳格パーサは例外・cheshire は無音受理で可否がパーサ依存)。
  CSV も `NaN` を正規の数値セル装いで出力し下流で無音破壊。修理は rated/required
  読み取り直後の `Double/isFinite` 検査 (falsify-11 と同一箇所) + export 層の
  出力直前の非有限数例外化/正規化。
- falsify-18 (refuted): `export.cljc` の `csv-cell` は `,` `"` `\n` `\r` の
  3 文字構文検査のみでフィールドの意味検査を持たないため、オペレータ供給の
  文字列フィールド (`:model` / `:buy`) 先頭の `=` `+` `-` `@` / タブが
  CSV formula injection として無音通過する — 引用の有無にかかわらず
  read-back で危険値がそのまま復元 (5 形状全滅、Excel/Sheets で数式評価
  される値)。正当 EDN リテラルで成立する点で falsify-6/11/17 と同一の
  「合法入力が無音で危険出力」クラス。対照: `bom->json` は同一入力を
  `json-str` で strict JSON 往復無害、破れは CSV 層のみ。付帯: タブは
  csv-cell の引用対象外のまま (falsify-17 の `\r` 修理で `\r` は入ったが
  タブは未検査)。修理: `csv-cell` に危険接頭辞 (= + - @ タブ) 検出時の
  スプレッドシート安全化 (前置き/例外化) を追加 — falsify-17 の有限性
  検査と同時に export 層入口 1 箇所にまとめられる。
- falsify-19 (refuted): `rob/gate` は allowed-set と `:action/safety` の**型を検査しない**
  ため、許可セットと action 側に同一の非 keyword 値 (文字列) が入った構成では
  無音 `:permit` する (`:actuate` kind のまま — falsify-12 の kind×class 結合欠落と
  畳なって文字列 safety の hardware actuate が gate を通る)。さらに gate は
  `safety-classes` 正規集合を一切参照せず、存在しないクラス `"not-a-class"` でも
  両側一致で permit。`requires-sign-off?` は keyword `#{:high :safety-critical}`
  への `contains?` のみなので文字列 `"high"` は false — 上位クラスを文字列に
  落としてセット側も文字列化すればサインオフ要求自体を迂回できる構造的余地。
  単独破損は fail-closed 維持 (文字列 action + keyword セット → deny、逆も deny)。
  成立は falsify-13 と同じ gate 入力 2 つの組合せ破損の文字列 face。修理は
  falsify-13 案の拡張: allowed-set の nil/非 keyword 全般の除去 + safety 非
  keyword (nil 含む) の `:invalid` 化 + (望むなら) gate 内 `safety-classes` 照合。
- falsify-20 (refuted): `bom->json` の数値スロット (cont_nm / peak_nm / price_jpy)
  は型検査なし生補間のため、合法 EDN 文字列リテラルが JSON 構文トークンとして
  そのまま出る。`:cont-nm "0,\"audit_injected\":true"` は **厳格パーサでも
  PARSED-OK** し、監査レコードに偽キー `"audit_injected": true` が混入
  (RFC 8259 適合装いの監査改変 — falsify-17 の厳格拒否型より深い面)。
  `:cont-nm "0}"` はオブジェクト早期閉鎖で無音不正 JSON 出力 (strict で
  JSONDecodeError)。対照: `torque->json` 経路は `torque-headroom` の減算で
  CCE になり fail-closed、csv-cell は `,` 引用で文字列セル往復 — 破れは
  BOM JSON 出力側に集中。修理: falsify-17 の非有限検査を「Number かつ
  finite のみ数値スロットに出す」型検査へ拡張 (非数値は例外化または
  `json-str` 経由引用文字列化) — falsify-17/18 と同一の export 層入口 1 箇所。
- falsify-21 (refuted): `arm/torque-headroom` は BOM を `:joint` 名キーの map に潰すため
  同名 joint 重複で required↔rated の位置対応が無音破れる — weak actuator の underrated
  -2.0 が +7.0 に変換され `underrated-joints` が無音空 (torque 安全検証の偽陰性)、
  `bom` の variant override も同名 2 件目に届かず検証経路から無音脱落。
 修理: chain 側 joint 名 distinct 検査 (重複は例外化) — falsify-6/10/11 の
  BOM 件数検査と同一箇所に追加可能。
- falsify-22 (refuted): `chassis/turning-radius` は非有限速度を無検査で —
  pivot (+Inf/-Inf) が `(zero? (+ left right))` 判定漏れで `##NaN` 半径、
  無限大両輪は `(== left right)` true で**「直進」nil に誤判定** (直進契約の偽陰性)、
  NaN 速度は無音 `##NaN` 半径; `integrate-pose` は dt/theta 非有限を無音伝播
  (全座標 NaN/Inf、例外なし)。nil は NPE で fail-closed 対照。修理:
  turning-radius 入口の `Double/isFinite` 検査 + integrate-pose の dt `(pos? dt)` かつ
  finite + linear/angular 有限性検査 — falsify-16 の track-width/dt 検査と同一箇所
  (chassis.cljc 入口 1 箇所)。

## NEXT

- falsify-21 (refuted): `arm/torque-headroom` は BOM を `:joint` 名キーの map
  に潰すため、`:arm/chain` の同名 joint 重複 (DR 撹拌・fixture 編集ミス) で
  required↔rated の位置対応が無音破れ — weak actuator の underrated -2.0 が
  別 joint の strong actuator で +7.0 に変換され `underrated-joints` が無音空
  (偽陰性)。`bom` の variant override も同名 2 件目に届かず、override した
  actuator が検証経路から無音脱落。重複名への警告 (例外・返却値) は一切なし。
  修理: chain-actuators (または torque-headroom 入口) で
  `(count (distinct (map :joint actuators))) == (count actuators)` と chain 側
  `:joint/name` の distinct 一致検査 (重複は例外化) — falsify-6/10/11 の
  BOM 件数検査と同一箇所に追加可能。
- falsify-22 (refuted): `chassis/turning-radius` は非有限速度を無検査で —
  pivot (+Inf/-Inf) が `(zero? (+ left right))` 判定漏れで `##NaN` 半径、
  無限大両輪は `(== left right)` true で**「直進」nil に誤判定**
  (直進契約の偽陰性)、NaN 速度は無音 `##NaN` 半径。
  `integrate-pose` は dt/theta 非有限を無音伝播 (全座標 NaN/Inf、例外なし)。
  対照: nil pose フィールド / nil width は NPE で fail-closed、破れは非有限のみ。
  修理: turning-radius 入口の
  `(every? #(Double/isFinite %) [track-width left right])` 検査 +
  integrate-pose の dt `(pos? dt)` かつ `Double/isFinite` + linear/angular
  有限性検査 — falsify-16 の track-width/dt 検査と同一箇所 (chassis.cljc 入口)。
- falsify-23 (refuted): `rob/mission` は `:max-steps` を無検査で
  0 / 負 / `##NaN` / `##Inf` / 文字列すべて無音受理し、「1 mission = bounded
  operation」契約が NaN/Inf で実質無限に抜け得る (ループ消費者が
  `(> i max-steps)` で比較すると NaN 比較 false / Inf で上限に届かない)。
  nil id/robot/objective も `:planned` で正規化され、監査キーが空のまま運用可能。
  `telemetry-proof` も nil sensor/reading を無音受理 (実体無し proof が台帳に乗る)。
  対照: `rob/safety-stop` は不明 reason で nil を返し fail-closed 維持 —
  同一 namespace 内で検査の有無が一貫しない。修理: mission 入口の `:max-steps`
  `(pos? x)` かつ `Double/isFinite` 検査 + id/robot/objective の some? 検査 +
  telemetry-proof の sensor/reading some? 検査 — falsify-11/14〜17 と同一の
  有限性検査パターンで rob 側入口 1 箇所にまとめられる。
- falsify-24 (refuted): `rob/gate` は actuation payload (`:action/params`) を
  一切検査せず (ソース参照 0 件) — `:params {:velocity ##Inf :torque ##NaN}` /
  `"not-a-map"` (文字列) / nil / `{:force -1000000}` のいずれも actuating action
  として無音 `:permit` (action-permitted? も true)。falsify-12 (kind×class 結合)・
  falsify-13/19 (set/safety 型) に続く第 4 の無検査面: クラスが正しくても
  中身が任意の actuation が通る (gate docstring の「hardware に届く前に unsafe
  actuation を拒む」は payload 面では何も担保していない)。`rob/action` も
  nil id/mission を無音正規化 (falsify-23 の action 版)。対照: `:safety-critical`
  は params `##NaN` でも `:require-sign-off` 維持 — 破れは params 面と
  id/mission 面に限定。修理: gate の permit 経路に actuating kind の params
  有限性/map 型検査 (最低限) を追加 (falsify-12 の kind×class 検査と同一箇所) +
  rob/action 入口の id/mission some? 検査 (falsify-23 と同一パターンで
  rob 側入口 1 箇所)。

NEXT: falsify-1 の修理 — fixtures/giemon_arm6/giemon_arm6.edn の :arm/chain / :arm/realization / :arm/base のダブルエンコードを解いて 1 段階 clojure.edn で joint/link (と actuator/variant) が EDN データとして出る形に展開する (データ損失リスク 0 済み: falsify-2 で joint 6、falsify-3 で link 7 の URDF 数値完全一致、falsify-4 で現時点でもドリフトなし確認済み、falsify-5 で torque 経路も underrated 0 の数値一致)。修理後は 1 段階 read で同数値が出ることの再測定 + falsify-5 の torque-headroom を 1 段階 read で再実行が残る。副: falsify-6/10/11 の torque 検査 fail-closed 化 (コア側コード修正) — `arm/bom` nil 時例外化に加え、joint-count と BOM 件数の一致検査 (未割当 joint の無音スキップ塞ぎ、truthy `()` は nil/empty ガードで検知不能のため)、rated/required 読み取り直後の `Double/isFinite` 検査 (非有限は例外化)。falsify-9 で迂回面が明示 `:safety` キーワードにまで拡大したため、facade 修理時は既知 product 以外例外化に加え、明示 `:safety` 指定が product 設定 posture より低いクラスへの降格でないことを検査する必要がある (falsify-9 実測: `:caterpillar` :high に `:safety :low` で `:permit` 到達)。falsify-12 で rob 側 (`kotoba.robotics`) 自体にも迂回路が確認されたため修理リストに追加: rob 側 kind×class 結合検査 — actuating kind (:actuate/:move/:grasp/:emit) かつ `:safety :none` を gate 構造的 deny (または action 生成時例外) にする (`:sense :none` の正当読み取り経路は温存。falsify-12 実測: `:actuate :none` が `#{:none :low :medium}` 許可セットで無音 `:permit`)。falsify-13 で gate 第 2 引数側の迂回路も確認されたため修理リストに追加: rob/gate の allowed-set 検査 — 許可セットから nil/非 keyword を除去 (または検出時例外) し、`:action/safety` nil の action は `:invalid` に落とす (falsify-13 実測: `(conj #{:low :medium} nil)` セットで nil-safety 生マップ action が無音 `:permit`、許可セット単独破損は fail-closed 維持)。falsify-19 で文字列 face も実測されこの修理案は拡張必須: 両側同一文字列 (`"low"` 混入セット ∧ 文字列-safety 生マップ) で `:actuate` が無音 :permit、未知クラス `"not-a-class"` も `safety-classes` 正規集合を gate が参照しないため通過、文字列 `"high"` でサインオフ迂回の構造的余地 — allowed-set 除去は「nil のみ」でなく非 keyword 全般に広げ、safety 側も非 keyword (nil 含む) を `:invalid` 化する (gate L124-129 同一箇所)。falsify-14 で運動学入力の縮退化 2 面を実測 — `k/normalize` 零ベクトル通過で axis `[0 0 0]` + θ=π の FK が det −1 鏡映 (`diag(-1,-1,-1)`) を例外無し生成するため `normalize` 零ベクトル例外化 (または joint-transform 入口の axis norm 検査) を、`within-limits?` が ±Inf 境界を無音受理するため lower/upper の `Double/isFinite` 検査を修理リストに追加 (後者は falsify-11 の有限性検査と同一箇所)。falsify-15 で運動学の意味論面 3 件を実測 — `forward-kinematics` は `:joint/type` を無視し (src 参照 0 件) prismatic 変位 (m) が rad 回転として適用 (j6 :prismatic 化で :revolute と pose 完全一致、未知 type :screw も同一)、角度列の過不足・nil は 0.0 補完/切捨てで無音完走、`##NaN` 角度は NaN 回転行列が pose まで伝播。修理リストに追加: joint-transform 入口の `:joint/type` 分岐 (prismatic は並進、未知 type は例外) + FK 入口の `(count angles) == (count chain)` 検査 + 角度の `Double/isFinite` 検査 (falsify-11/14 と同一修理箇所)。falsify-16 で chassis track-drive の縮退面を実測 — `twist->track-speeds` は `track-width` を無検査で、負幅は `:twist/angular` の符号を無音反転 (往復変換自己無矛盾でセルフチェック不能、統合 pose の theta ±2.0 rad に直流出)、零幅の逆変換は回転コマンドを無音に捨てて直進 speeds を返す (前方は Divide by zero で fail-closed、非対称)、`##NaN`/`##Inf` width・speeds・dt も素通り。修理リストに追加: track-width 入口の `(pos? width)` かつ `Double/isFinite` 検査 + speeds/dt の有限性検査 (falsify-11/14/15 と同一修理箇所)。falsify-17 で export 層の非有限数流出を実測 — `torque->json` / `bom->json` は有限性無検査の `(str ...)` 補間で `##NaN`/`##-Inf` を生 `NaN`/`-Infinity` トークンとして監査 JSON に出力 (RFC 8259 違反、厳格パーサは例外・cheshire は無音受理)、CSV も `NaN` を正規数値セル装いで出力。修理リストに追加: rated/required 読み取り直後の `Double/isFinite` 検査 (falsify-11 と同一箇所) + export 出力直前の非有限例外化/正規化。falsify-18 で CSV formula injection を実測 — `csv-cell` は `,` `"` `\n` `\r` の構文検査のみで `:model`/`:buy` 先頭の `=` `+` `-` `@` / タブが引用の有無にかかわらず read-back で危険値のまま復元 (5 形状全滅、対照: `bom->json` は同一入力で strict JSON 往復無害、破れは CSV 層のみ)。修理リストに追加: `csv-cell` に危険接頭辞検出時のスプレッドシート安全化 (前置き/例外化) — falsify-17 の有限性検査と同時に export 層入口 1 箇所にまとめられる。falsify-19 で gate の型無検査の文字列 face を実測 — 許可セットと action 側に同一非 keyword 値 (文字列) で無音 `:permit` (未知クラス文字列 `"not-a-class"` も通過、`requires-sign-off?` は文字列 `"high"` に false でサインオフ迂回の構造的余地)、修理は falsify-13 案の拡張 (allowed-set の nil/非 keyword 全般除去 + safety 非 keyword の `:invalid` 化 + gate 内 `safety-classes` 照合)。falsify-20 で export 層の数値スロット型無検査を実測 — `bom->json` の cont_nm/peak_nm/price_jpy 生補間に合法 EDN 文字列 `"0,\"audit_injected\":true"` が **厳格 JSON パーサ通過で偽キー混入** (falsify-17 より深い監査改変面)、`"0}"` は無音不正 JSON 出力、対照: torque 経路は CCE fail-closed。修理リスト追加: falsify-17 の非有限検査を「Number かつ finite のみ数値スロット」型検査へ拡張 (export 層入口 1 箇所)。falsify-23 で rob/mission 契約の入力無検査を実測 — 修理リスト追加: mission 入口の `:max-steps` (pos? x) かつ Double/isFinite 検査 + id/robot/objective の some? 検査 + telemetry-proof の sensor/reading some? 検査 (rob 側入口 1 箇所)。falsify-25 で ui/viewer 層の非有限伝播終点を実測 — 修理リスト追加: ui/torque-table の分類は `neg?` 1 点でなく有限性確認後の比較に変更 (生 NaN/Infinity の HTML 補間も防ぐ、falsify-17 の export 検査と同一パターン。torque-headroom 入口の Double/isFinite 検査で ui/viewer/export 3 面同時に塞げる)。

- falsify-25 (refuted): `ui/torque-table` は headroom を `neg?` 1 点だけで
  :err/:ok 分類し、falsify-11 で無音侵入する `##NaN` headroom が **:ok 表示**
  でオペレータコンソールに乗る (生 `NaN`/`Infinity` トークンも HTML 補間 —
  falsify-17 の HTML 版)。`##Inf` required は headroom `##-Inf` で偶然 err
  になるが NaN 面は完全無防備。`viewer/arm-scene-ir` も falsify-14/15 の
  NaN 角度を全 ##NaN 回転行列のまま無音 scene-IR 化 (伝播終点を実測)。
  対照: HTML エスケープ (html.core/esc) 自体は正常、破れは neg? 意味分類と
  非有限検査の欠落に限定。修理: torque-headroom 入口の `Double/isFinite`
  検査 (falsify-11/17 と同一箇所) で ui/viewer/export 3 面同時に塞ぎ、
  ui 分類は有限性確認後の比較に変更。
