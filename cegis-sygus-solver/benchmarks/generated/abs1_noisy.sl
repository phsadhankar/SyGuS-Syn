(set-logic LIA)

(synth-fun abs1 ((x Int)) Int

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


(constraint (>= (abs1 x) 0))
(constraint (or (= (abs1 x) x) (= (abs1 x) (- 0 x))))


(check-synth)
