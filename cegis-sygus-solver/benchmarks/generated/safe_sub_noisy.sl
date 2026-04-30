(set-logic LIA)

(synth-fun safe_sub ((x Int) (y Int)) Int

  ((Start Int (
      x
      y
      0 1 2
      (+ Start Start) (- Start Start) (* Start Start) (ite StartBool Start Start)
  ))
  (StartBool Bool (
      (>= Start Start) (<= Start Start) (> Start Start) (< Start Start) (= Start Start)
  )))

)

(declare-var x Int)
(declare-var y Int)


(constraint (=> (>= x y) (= (safe_sub x y) (- x y))))
(constraint (=> (< x y) (= (safe_sub x y) 0)))


(check-synth)
