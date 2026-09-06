;; falsify-018 probe part 3 (diag) — the EDN uses #:link{...} namespaced map
;; and the file's first element parse: inspect structure before concluding.
;; Usage: clojure -M -e '(load-file "sim-loop/evidence/probe_bom_diag.clj")'
(def raw (slurp "fixtures/giemon_arm6/giemon_arm6.edn"))
(def body (clojure.string/replace raw #"(?m)^;;.*\n" ""))
(def fixture (read-string body))
(println "R0 class" (type fixture) "count" (count fixture))
(println "R1 first" (pr-str (first fixture)))
(println "R2 keys" (pr-str (keys (first fixture))))
