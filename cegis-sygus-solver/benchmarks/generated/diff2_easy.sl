(set-logic LIA)

(synth-fun diff2 ((x Int) (y Int)) Int

  ((Start Int (
      x
      y
      0
      (- Start Start)
  ))
  (StartBool Bool (
      (>= Start Start) (<= Start Start) (> Start Start) (< Start Start) (= Start Start)
  )))

)

(declare-var x Int)
(declare-var y Int)


(constraint (= (diff2 x y) (- x y)))


(check-synth)
