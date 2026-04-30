(set-logic LIA)

(synth-fun dec ((x Int)) Int

  ((Start Int (
      x
      0 1
      (- Start Start)
  ))
  (StartBool Bool (
      (>= Start Start) (<= Start Start) (> Start Start) (< Start Start) (= Start Start)
  )))

)

(declare-var x Int)


(constraint (= (dec x) (- x 1)))


(check-synth)
