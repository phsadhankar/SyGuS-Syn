(set-logic LIA)

(synth-fun neg ((x Int)) Int

  ((Start Int (
      x
      0
      (- Start Start)
  ))
  (StartBool Bool (
      (>= Start Start) (<= Start Start) (> Start Start) (< Start Start) (= Start Start)
  )))

)

(declare-var x Int)


(constraint (= (neg x) (- 0 x)))


(check-synth)
