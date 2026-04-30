(set-logic LIA)

(synth-fun clamp_nonpositive ((x Int)) Int

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


(constraint (<= (clamp_nonpositive x) 0))
(constraint (<= (clamp_nonpositive x) x))
(constraint (or (= (clamp_nonpositive x) x) (= (clamp_nonpositive x) 0)))


(check-synth)
