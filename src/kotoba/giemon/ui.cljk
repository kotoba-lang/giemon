(ns kotoba.giemon.ui
  "Operator-facing console for the Giemon product line — read-only.

  Renders the product registry and Otete arm torque headroom using
  kotoba-lang/html + css, in the same pattern as `kotoba.robotics.ui`.
  Pure data -> markup: no network, no DOM, never dispatches hardware."
  (:require [html.core :as html]
            [css.core :as css]
            [kotoba.giemon :as giemon]
            [kotoba.giemon.arm :as arm]))

(def ^:private sheet (css/merge-theme {}))
(defn- stylesheet [] (html/->html (css/style-node sheet)))

(defn products-table []
  [:table
   [:thead [:tr [:th "Product"] [:th "Kind"] [:th "DOF"] [:th "Status"] [:th "Kaigo role"]]]
   [:tbody (for [[_ p] giemon/products]
             [:tr [:td (:product/name p)]
                  [:td (name (:product/kind p))]
                  [:td (str (or (:product/dof p) "—"))]
                  [:td (name (:product/status p))]
                  [:td (:product/kaigo-role p)]])]])

(defn torque-table [arm-spec]
  [:table
   [:thead [:tr [:th "Joint"] [:th "Required (N·m)"] [:th "Rated (N·m)"] [:th "Headroom"]]]
   [:tbody (for [t (arm/torque-headroom arm-spec)]
             [:tr [:td (:joint/name t)]
                  [:td (str (:torque/required t))]
                  [:td (str (:torque/rated t))]
                  [:td {:class [(if (neg? (:torque/headroom t)) :err :ok)]}
                   (str (:torque/headroom t))]])]])

(defn dashboard
  "Render a full HTML operator console page. `arm-spec` (the parsed
  giemon_arm6 EDN fixture, or another `:arm/chain` spec) is optional —
  when given, its torque headroom table is rendered too."
  [{:keys [arm-spec]}]
  (html/->html
    [:html
     [:head [:meta {:charset "utf-8"}] [:title "Giemon — Operator Console"]
      [:hiccup/raw (stylesheet)]]
     [:body
      [:header.bar
       [:h1 "Giemon — Product & Torque Console"]
       [:span.badge "read-only · governor-gated · never dispatches"]]
      [:main
       [:section.card [:h2 "Products"] (products-table)]
       (when arm-spec
         [:section.card [:h2 "Otete arm — torque headroom"] (torque-table arm-spec)])]]]))
