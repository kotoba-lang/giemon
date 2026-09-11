(ns kotoba.giemon.viewer
  "EDN scene-IR contract for the Giemon 3D viewer
  (giemon.gftd.ai/viewer.htm?model=arm|hitogata|caterpillar, ADR-2605142200
  and ADR-2605142300's kaigo.gftd.ai iframe share).

  This namespace is the domain authority for the viewer scene; a WASM/wgpu
  render adapter (`kami.render`, ADR-2607010000) loads this IR and owns no
  scene semantics of its own — the migration-unit successor to the
  never-implemented `kami-app-giemon` Rust crate."
  (:require [kotoba.giemon.arm :as arm]
            [kotoba.giemon.kinematics :as k]))

(defn arm-scene-ir
  "Scene-IR for the `:arm` (Otete) viewer model: one instance per link,
  each positioned at its forward-kinematics world transform."
  [giemon-arm6 angles]
  {:scene/model :arm
   :scene/instances
   (vec (map-indexed
          (fn [i xf] {:instance/link (str "link" (inc i))
                      :instance/pos (:xf/pos xf)
                      :instance/rot (:xf/rot xf)})
          (arm/forward-kinematics giemon-arm6 angles)))})

(defn product-scene-ir
  "Scene-IR stub for a product with no articulation fixture yet
  (`:hitogata` / `:caterpillar` are `:in-design`, ADR-2605142200) — a
  single named instance at the origin."
  [model]
  {:scene/model model
   :scene/instances [{:instance/link (name model)
                       :instance/pos [0.0 0.0 0.0]
                       :instance/rot k/identity-rot}]})
