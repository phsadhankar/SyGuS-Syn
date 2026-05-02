(set-logic LIA)

(synth-fun is_zero_int ((x Int)) Int

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


(constraint (=> (= x 0) (= (is_zero_int x) 1)))
(constraint (=> (not (= x 0)) (= (is_zero_int x) 0)))


(check-synth)
