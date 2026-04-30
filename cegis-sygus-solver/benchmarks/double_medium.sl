(set-logic LIA)

(synth-fun double ((x Int)) Int

  ((Start Int (
      x
      0 1
      (+ Start Start) (- Start Start)
  ))
  (StartBool Bool (
      (>= Start Start) (<= Start Start) (> Start Start) (< Start Start) (= Start Start)
  )))

)

(declare-var x Int)


(constraint (= (double x) (+ x x)))


(check-synth)
