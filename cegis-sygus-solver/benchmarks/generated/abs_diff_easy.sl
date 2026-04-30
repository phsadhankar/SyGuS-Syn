(set-logic LIA)

(synth-fun abs_diff ((x Int) (y Int)) Int

  ((Start Int (
      x
      y
      0
      (- Start Start) (ite StartBool Start Start)
  ))
  (StartBool Bool (
      (>= Start Start) (<= Start Start) (> Start Start) (< Start Start) (= Start Start)
  )))

)

(declare-var x Int)
(declare-var y Int)


(constraint (>= (abs_diff x y) 0))
(constraint (or (= (abs_diff x y) (- x y)) (= (abs_diff x y) (- y x))))


(check-synth)
