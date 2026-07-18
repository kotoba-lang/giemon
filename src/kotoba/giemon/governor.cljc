(ns kotoba.giemon.governor
  "Giemon Kaigo (in-home care) mission/action helpers layered on
  kotoba-lang/robotics' generic mission/action/governor contract
  (ADR-2607011000). This library never drives hardware — it only shapes
  Giemon-specific missions and actions into the safety classes
  `kotoba.robotics/gate` checks. See ADR-2605142300."
  (:require [kotoba.robotics :as rob]))

(def kaigo-roles
  "Per-product Kaigo application role and default action safety posture,
  from ADR-2605142300."
  {:otete       {:role "在宅 ADL 支援ロボット" :default-safety :medium}
   :hitogata    {:role "リハビリ・交流ロボット" :default-safety :medium}
   :caterpillar {:role "自律見守り UGV" :default-safety :low}})

(defn kaigo-mission
  "A Giemon Kaigo mission for `product` (:otete / :hitogata / :caterpillar)."
  [id product objective & opts]
  (apply rob/mission id (name product) objective opts))

(defn kaigo-action
  "A Giemon Kaigo action for `product`. Defaults `:safety` to the product's
  posture in `kaigo-roles` unless explicitly given."
  [id mission-id product kind & {:keys [safety params]}]
  (rob/action id mission-id kind
              (or safety (get-in kaigo-roles [product :default-safety] :medium))
              :params params))

(defn fall-detected-alert
  "Fall-detection / emergency-notification escalation
  (Caterpillar autonomous patrol, Hitogata companion) — always
  `:safety-critical`, so `kotoba.robotics/gate` always routes it to human
  sign-off before any dispatch (ADR-2605142300)."
  [id mission-id & {:keys [params]}]
  (rob/action id mission-id :emit :safety-critical :params params))

(def ops-roles
  "Per-product commercial/municipal cleaning-service role and default
  action safety posture, parallel to `kaigo-roles` but for non-Kaigo ops
  missions. :caterpillar defaults to :high (NOT kaigo-roles' :low for the
  same product id): the facade/street-cleaning configuration dispenses
  chemical fluid and operates near pedestrians/buildings in public space,
  materially more hazardous than the indoor elder-watch UGV framing
  kaigo-roles assumes for the same product."
  {:caterpillar {:role "街並み・外壁清掃 UGV" :default-safety :high}})

(defn ops-mission
  "A Giemon ops (commercial/municipal cleaning-service) mission for
  `product`, parallel to `kaigo-mission`."
  [id product objective & opts]
  (apply rob/mission id (name product) objective opts))

(defn ops-action
  "A Giemon ops action for `product`. Defaults `:safety` to the product's
  posture in `ops-roles` unless explicitly given, parallel to
  `kaigo-action`."
  [id mission-id product kind & {:keys [safety params]}]
  (rob/action id mission-id kind
              (or safety (get-in ops-roles [product :default-safety] :medium))
              :params params))

(defn chemical-dispense-alert
  "Chemical-fluid-dispense escalation (Caterpillar facade-cleaning
  wet-spray variant) — always `:safety-critical`, so
  `kotoba.robotics/gate` always routes it to human sign-off before any
  dispatch, mirroring `fall-detected-alert`'s hardcoded posture."
  [id mission-id & {:keys [params]}]
  (rob/action id mission-id :emit :safety-critical :params params))
