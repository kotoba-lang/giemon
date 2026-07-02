# kotoba-giemon

[![CI](https://github.com/kotoba-lang/giemon/actions/workflows/ci.yml/badge.svg)](https://github.com/kotoba-lang/giemon/actions/workflows/ci.yml)

**Giemon open-hardware robot product line, in pure Clojure.** A
[kotoba-lang](https://github.com/kotoba-lang) capability library for the
Giemon brand (ADR-2605142200): **Otete** (6-DOF arm + crawler kit,
shipping), **Hitogata** (17-axis biped, in design) and **Caterpillar**
(dual-track UGV, in design), plus their **Giemon Kaigo** in-home-care
application (ADR-2605142300).

This library owns Giemon's product metadata, articulation forward
kinematics/torque validation, and the viewer scene-IR contract. It does
**not** own mission/action safety governance — that generic, cross-cutting
concern belongs to [`kotoba-lang/robotics`](https://github.com/kotoba-lang/robotics)
(ADR-2607011000), the same governor contract all 26 cloud-itonami
industry blueprints depend on. `kotoba.giemon.governor` is a thin,
Giemon-Kaigo-specific wrapper over it.

No network, no I/O. Portable `.cljc` across JVM / ClojureScript / SCI /
GraalVM.

## Test

```bash
clojure -M:test
clojure -M:lint
```

## Maturity

| | |
|---|---|
| Role | capability |
| Tests | green |
| Operator console (UI/UX) | yes |
| Export (CSV/JSON) | yes |
| Shared CSS design system | yes (css.core/operator-theme) |

## Contract

```clojure
(require '[kotoba.giemon :as giemon]
         '[kotoba.giemon.arm :as arm]
         '[kotoba.giemon.governor :as gov]
         '[kotoba.giemon.viewer :as viewer])

(giemon/product :otete)
;; => {:product/name "Giemon Otete" :product/dof 6 :product/status :shipping ...}

;; forward kinematics + torque validation over the giemon_arm6 fixture
;; (fixtures/giemon_arm6/giemon_arm6.edn — caller reads/parses it, no I/O here)
(arm/forward-kinematics giemon-arm6 [0.0 0.2 -0.3 0.0 0.5 0.0])
(arm/underrated-joints giemon-arm6)   ; joints whose actuator is under-rated

;; actuator BOM by :arm/realization variant (ported from kami-articulated-scene)
(arm/bom giemon-arm6 :all-qdd)             ; the inline chain actuators (default)
(arm/bom giemon-arm6 :harmonic-shoulder)   ; :all-qdd with j2's :override applied
(arm/underrated-joints giemon-arm6 (arm/bom giemon-arm6 :harmonic-shoulder))

;; Kaigo mission/action, delegating the safety gate to kotoba-lang/robotics
(gov/kaigo-action "A1" "M1" :otete :move)
(gov/fall-detected-alert "A2" "M1" :params {:location "hallway"})

;; scene-IR for the giemon.gftd.ai / kaigo.gftd.ai 3D viewer
(viewer/arm-scene-ir giemon-arm6 [0.0 0.2 -0.3 0.0 0.5 0.0])
```

## Fixtures

`fixtures/giemon_arm6/` — the canonical 6-DOF Otete arm articulation, as
both EDN (`giemon_arm6.edn`, the source of truth) and URDF
(`giemon_arm6.urdf`, a parity oracle: `from_edn(edn) == parse_urdf(urdf)`).
Moved here from `kotoba-lang/kami-engine` — Hitogata and Caterpillar have
no articulation fixture yet (still `:in-design`, ADR-2605142200).

## Operator console (UI/UX)

A read-only HTML dashboard renders the product registry and Otete arm
torque headroom, built on
[`kotoba-lang/html`](https://github.com/kotoba-lang/html) (Hiccup→HTML) +
[`kotoba-lang/css`](https://github.com/kotoba-lang/css) (EDN→CSS).

```clojure
(require '[kotoba.giemon.ui :as ui])

(ui/dashboard {:arm-spec giemon-arm6})
```

## Export (CSV / JSON)

```clojure
(require '[kotoba.giemon.export :as export])

(export/products->csv)
(export/torque->csv giemon-arm6)
```

## Provider catalog

The WASM/wgpu 3D viewer adapter that renders `kotoba.giemon.viewer`'s
scene-IR (`giemon.gftd.ai/viewer.htm?model=arm|hitogata|caterpillar`) lives
in `kotoba-lang/kami-engine`, per `orgs/kotoba-lang/kami-contracts`'
provider catalog — Giemon has its own dedicated `:giemon` provider family
there (split from the generic `:app-fixtures` bucket the never-implemented
`kami-app-giemon`/`kami-app-giemon-factory` crates were previously listed
under).

`kami-articulated-scene` (nominally a `:scene-domains` sibling of the
crates ported into `kotoba-lang/kami-scene-contracts`) was folded into
`kotoba.giemon.arm` here instead — its content (`from_edn`/BOM-variant/
torque-validation) is entirely about the giemon_arm6 arm specifically,
not a generic "-scene" data table, so it belongs with the rest of the
Otete arm contract rather than in the generic scene-domains repo.

## Why

Giemon products act as the robotics substrate for `cloud-itonami`'s
robotics-premise design (ADR-2607011000): an actor proposes actions, an
independent governor gates them, and a Giemon robot performs the physical
work. This library keeps product/kinematics data separate from that
generic safety-governance contract so either can evolve independently.

## License

Apache License 2.0.
