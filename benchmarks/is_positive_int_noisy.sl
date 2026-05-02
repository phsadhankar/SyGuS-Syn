(set-logic LIA)

(synth-fun is_positive_int ((x Int)) Int

  ((Start Int (
      x
      0 1 2
      (+ Start Start) (- Start Start) (* Start Start) (ite StartBool Start Start)
  ))
  (StartBool Bool (
      (>= Start Start) (<= Start Start) (> Start Start) (< Start Start) (= Start Start)
  )))

)

(declare-var x Int)


(constraint (=> (> x 0) (= (is_positive_int x) 1)))
(constraint (=> (<= x 0) (= (is_positive_int x) 0)))


(check-synth)
