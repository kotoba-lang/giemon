(ns kotoba.giemon
  "Giemon — open-hardware robot product line, pure data contracts.

  Otete (6-DOF arm + crawler kit, shipping) / Hitogata (17-axis biped,
  in-design) / Caterpillar (dual-track UGV, in-design) product registry,
  per ADR-2605142200 (brand) and ADR-2605142300 (Giemon Kaigo in-home care
  application).

  Physical execution and safety gating are kotoba-lang/robotics' concern
  (mission / action / governor, ADR-2607011000); this library adds
  Giemon-specific product metadata, articulation kinematics
  (`kotoba.giemon.arm` / `kotoba.giemon.kinematics`) and Kaigo mission
  helpers (`kotoba.giemon.governor`) on top. No network, no I/O.")

(def products
  "The Giemon product line, keyed by product id."
  {:otete
   {:product/name "Giemon Otete"
    :product/kind :arm-crawler
    :product/dof 6
    :product/status :shipping
    :product/kaigo-role "在宅 ADL 支援ロボット"}
   :hitogata
   {:product/name "Giemon Hitogata"
    :product/kind :biped-humanoid
    :product/dof 17
    :product/height-mm 285
    :product/status :in-design
    :product/kaigo-role "リハビリ・交流ロボット"}
   :caterpillar
   {:product/name "Giemon Caterpillar"
    :product/kind :dual-track-ugv
    :product/length-mm 380
    :product/status :in-design
    :product/kaigo-role "自律見守り UGV"
    :product/fixture "fixtures/giemon_caterpillar_facade/giemon_caterpillar_facade.edn"}})

(defn product
  "Look up a product by id (:otete / :hitogata / :caterpillar). nil if
  unknown."
  [id]
  (get products id))
