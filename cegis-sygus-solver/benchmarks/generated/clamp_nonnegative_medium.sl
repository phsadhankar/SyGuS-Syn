(set-logic LIA)

(synth-fun clamp_nonnegative ((x Int)) Int

  ((Start Int (
      x
      0 1
      (+ Start Start) (- Start Start) (ite StartBool Start Start)
  ))
  (StartBool Bool (
      (>= Start Start) (<= Start Start) (> Start Start) (< Start Start) (= Start Start)
  )))

)

(declare-var x Int)


(constraint (>= (clamp_nonnegative x) 0))
(constraint (>= (clamp_nonnegative x) x))
(constraint (or (= (clamp_nonnegative x) x) (= (clamp_nonnegative x) 0)))


(check-synth)
