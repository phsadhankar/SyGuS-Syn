(set-logic LIA)

(synth-fun sum2 ((x Int) (y Int)) Int

  ((Start Int (
      x
      y
      0 1 2
      (+ Start Start) (- Start Start) (ite StartBool Start Start)
  ))
  (StartBool Bool (
      (>= Start Start) (<= Start Start) (> Start Start) (< Start Start) (= Start Start)
  )))

)

(declare-var x Int)
(declare-var y Int)


(constraint (= (sum2 x y) (+ x y)))


(check-synth)
