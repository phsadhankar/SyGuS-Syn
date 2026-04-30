(set-logic LIA)

(synth-fun select_positive_x_else_y ((x Int) (y Int)) Int

  ((Start Int (
      x
      y
      0 1
      (+ Start Start) (- Start Start) (ite StartBool Start Start)
  ))
  (StartBool Bool (
      (>= Start Start) (<= Start Start) (> Start Start) (< Start Start) (= Start Start)
  )))

)

(declare-var x Int)
(declare-var y Int)


(constraint (=> (> x 0) (= (select_positive_x_else_y x y) x)))
(constraint (=> (<= x 0) (= (select_positive_x_else_y x y) y)))


(check-synth)
