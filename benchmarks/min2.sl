(set-logic LIA)

(synth-fun min2 ((x Int) (y Int)) Int
  ((Start Int (
      x
      y
      0
      1
      (+ Start Start)
      (- Start Start)
      (ite StartBool Start Start)
  ))
  (StartBool Bool (
      (>= Start Start)
      (<= Start Start)
      (= Start Start)
  )))
)

(declare-var x Int)
(declare-var y Int)

(constraint (<= (min2 x y) x))
(constraint (<= (min2 x y) y))
(constraint (or (= (min2 x y) x) (= (min2 x y) y)))

(check-synth)