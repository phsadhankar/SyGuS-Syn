from pathlib import Path

OUT_DIR = Path("benchmarks")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def write_file(name, content):
    path = OUT_DIR / name
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Created {path}")


def grammar_one_var(constants="0 1", ops="+ - ite", bool_ops=">= <= = > <"):
    int_ops = []

    if "+" in ops:
        int_ops.append("(+ Start Start)")
    if "-" in ops:
        int_ops.append("(- Start Start)")
    if "*" in ops:
        int_ops.append("(* Start Start)")
    if "ite" in ops:
        int_ops.append("(ite StartBool Start Start)")

    bool_lines = []

    if ">=" in bool_ops:
        bool_lines.append("(>= Start Start)")
    if "<=" in bool_ops:
        bool_lines.append("(<= Start Start)")
    if ">" in bool_ops:
        bool_lines.append("(> Start Start)")
    if "<" in bool_ops:
        bool_lines.append("(< Start Start)")
    if "=" in bool_ops:
        bool_lines.append("(= Start Start)")

    return f"""
  ((Start Int (
      x
      {constants}
      {' '.join(int_ops)}
  ))
  (StartBool Bool (
      {' '.join(bool_lines)}
  )))
"""


def grammar_two_var(constants="0 1", ops="+ - ite", bool_ops=">= <= = > <"):
    int_ops = []

    if "+" in ops:
        int_ops.append("(+ Start Start)")
    if "-" in ops:
        int_ops.append("(- Start Start)")
    if "*" in ops:
        int_ops.append("(* Start Start)")
    if "ite" in ops:
        int_ops.append("(ite StartBool Start Start)")

    bool_lines = []

    if ">=" in bool_ops:
        bool_lines.append("(>= Start Start)")
    if "<=" in bool_ops:
        bool_lines.append("(<= Start Start)")
    if ">" in bool_ops:
        bool_lines.append("(> Start Start)")
    if "<" in bool_ops:
        bool_lines.append("(< Start Start)")
    if "=" in bool_ops:
        bool_lines.append("(= Start Start)")

    return f"""
  ((Start Int (
      x
      y
      {constants}
      {' '.join(int_ops)}
  ))
  (StartBool Bool (
      {' '.join(bool_lines)}
  )))
"""


def one_var_benchmark(
    fname,
    synth_name,
    constraints,
    constants="0 1",
    ops="+ - ite",
    bool_ops=">= <= = > <",
):
    content = f"""
(set-logic LIA)

(synth-fun {synth_name} ((x Int)) Int
{grammar_one_var(constants, ops, bool_ops)}
)

(declare-var x Int)

{constraints}

(check-synth)
"""
    write_file(fname, content)


def two_var_benchmark(
    fname,
    synth_name,
    constraints,
    constants="0 1",
    ops="+ - ite",
    bool_ops=">= <= = > <",
):
    content = f"""
(set-logic LIA)

(synth-fun {synth_name} ((x Int) (y Int)) Int
{grammar_two_var(constants, ops, bool_ops)}
)

(declare-var x Int)
(declare-var y Int)

{constraints}

(check-synth)
"""
    write_file(fname, content)


# -------------------------------------------------------------------
# Original 12 function families
# -------------------------------------------------------------------

# 1. inc: x + 1
for variant, constants, ops in [
    ("easy", "0 1", "+"),
    ("medium", "0 1", "+ -"),
    ("noisy", "0 1 2", "+ - ite"),
]:
    one_var_benchmark(
        f"inc_{variant}.sl",
        "inc",
        """
(constraint (= (inc x) (+ x 1)))
""",
        constants,
        ops,
    )


# 2. dec: x - 1
for variant, constants, ops in [
    ("easy", "0 1", "-"),
    ("medium", "0 1", "+ -"),
    ("noisy", "0 1 2", "+ - ite"),
]:
    one_var_benchmark(
        f"dec_{variant}.sl",
        "dec",
        """
(constraint (= (dec x) (- x 1)))
""",
        constants,
        ops,
    )


# 3. neg: -x
for variant, constants, ops in [
    ("easy", "0", "-"),
    ("medium", "0 1", "+ -"),
    ("noisy", "0 1 2", "+ - ite"),
]:
    one_var_benchmark(
        f"neg_{variant}.sl",
        "neg",
        """
(constraint (= (neg x) (- 0 x)))
""",
        constants,
        ops,
    )


# 4. sum2: x + y
for variant, constants, ops in [
    ("easy", "0", "+"),
    ("medium", "0 1", "+ -"),
    ("noisy", "0 1 2", "+ - ite"),
]:
    two_var_benchmark(
        f"sum2_{variant}.sl",
        "sum2",
        """
(constraint (= (sum2 x y) (+ x y)))
""",
        constants,
        ops,
    )


# 5. diff2: x - y
for variant, constants, ops in [
    ("easy", "0", "-"),
    ("medium", "0 1", "+ -"),
    ("noisy", "0 1 2", "+ - ite"),
]:
    two_var_benchmark(
        f"diff2_{variant}.sl",
        "diff2",
        """
(constraint (= (diff2 x y) (- x y)))
""",
        constants,
        ops,
    )


# 6. double: x + x
for variant, constants, ops in [
    ("easy", "0", "+"),
    ("medium", "0 1", "+ -"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    one_var_benchmark(
        f"double_{variant}.sl",
        "double",
        """
(constraint (= (double x) (+ x x)))
""",
        constants,
        ops,
    )


# 7. max2
for variant, constants, ops in [
    ("easy", "0 1", "ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    two_var_benchmark(
        f"max2_{variant}.sl",
        "max2",
        """
(constraint (>= (max2 x y) x))
(constraint (>= (max2 x y) y))
(constraint (or (= (max2 x y) x) (= (max2 x y) y)))
""",
        constants,
        ops,
    )


# 8. min2
for variant, constants, ops in [
    ("easy", "0 1", "ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    two_var_benchmark(
        f"min2_{variant}.sl",
        "min2",
        """
(constraint (<= (min2 x y) x))
(constraint (<= (min2 x y) y))
(constraint (or (= (min2 x y) x) (= (min2 x y) y)))
""",
        constants,
        ops,
    )


# 9. abs1
for variant, constants, ops in [
    ("easy", "0", "- ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    one_var_benchmark(
        f"abs1_{variant}.sl",
        "abs1",
        """
(constraint (>= (abs1 x) 0))
(constraint (or (= (abs1 x) x) (= (abs1 x) (- 0 x))))
""",
        constants,
        ops,
    )


# 10. clamp_nonnegative: max(x, 0)
for variant, constants, ops in [
    ("easy", "0", "ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    one_var_benchmark(
        f"clamp_nonnegative_{variant}.sl",
        "clamp_nonnegative",
        """
(constraint (>= (clamp_nonnegative x) 0))
(constraint (>= (clamp_nonnegative x) x))
(constraint (or (= (clamp_nonnegative x) x) (= (clamp_nonnegative x) 0)))
""",
        constants,
        ops,
    )


# 11. abs_diff: abs(x - y)
for variant, constants, ops in [
    ("easy", "0", "- ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    two_var_benchmark(
        f"abs_diff_{variant}.sl",
        "abs_diff",
        """
(constraint (>= (abs_diff x y) 0))
(constraint (or (= (abs_diff x y) (- x y)) (= (abs_diff x y) (- y x))))
""",
        constants,
        ops,
    )


# 12. safe_sub: if x >= y then x-y else 0
for variant, constants, ops in [
    ("easy", "0", "- ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    two_var_benchmark(
        f"safe_sub_{variant}.sl",
        "safe_sub",
        """
(constraint (=> (>= x y) (= (safe_sub x y) (- x y))))
(constraint (=> (< x y) (= (safe_sub x y) 0)))
""",
        constants,
        ops,
    )


# -------------------------------------------------------------------
# New 5 function families
# -------------------------------------------------------------------

# 13. is_zero_int: returns 1 if x = 0, else 0
for variant, constants, ops in [
    ("easy", "0 1", "ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    one_var_benchmark(
        f"is_zero_int_{variant}.sl",
        "is_zero_int",
        """
(constraint (=> (= x 0) (= (is_zero_int x) 1)))
(constraint (=> (not (= x 0)) (= (is_zero_int x) 0)))
""",
        constants,
        ops,
    )


# 14. is_positive_int: returns 1 if x > 0, else 0
for variant, constants, ops in [
    ("easy", "0 1", "ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    one_var_benchmark(
        f"is_positive_int_{variant}.sl",
        "is_positive_int",
        """
(constraint (=> (> x 0) (= (is_positive_int x) 1)))
(constraint (=> (<= x 0) (= (is_positive_int x) 0)))
""",
        constants,
        ops,
    )


# 15. is_negative_int: returns 1 if x < 0, else 0
for variant, constants, ops in [
    ("easy", "0 1", "ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    one_var_benchmark(
        f"is_negative_int_{variant}.sl",
        "is_negative_int",
        """
(constraint (=> (< x 0) (= (is_negative_int x) 1)))
(constraint (=> (>= x 0) (= (is_negative_int x) 0)))
""",
        constants,
        ops,
    )


# 16. clamp_nonpositive: min(x, 0)
for variant, constants, ops in [
    ("easy", "0", "ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    one_var_benchmark(
        f"clamp_nonpositive_{variant}.sl",
        "clamp_nonpositive",
        """
(constraint (<= (clamp_nonpositive x) 0))
(constraint (<= (clamp_nonpositive x) x))
(constraint (or (= (clamp_nonpositive x) x) (= (clamp_nonpositive x) 0)))
""",
        constants,
        ops,
    )


# 17. select_positive_x_else_y: if x > 0 then x else y
for variant, constants, ops in [
    ("easy", "0 1", "ite"),
    ("medium", "0 1", "+ - ite"),
    ("noisy", "0 1 2", "+ - * ite"),
]:
    two_var_benchmark(
        f"select_positive_x_else_y_{variant}.sl",
        "select_positive_x_else_y",
        """
(constraint (=> (> x 0) (= (select_positive_x_else_y x y) x)))
(constraint (=> (<= x 0) (= (select_positive_x_else_y x y) y)))
""",
        constants,
        ops,
    )


print()
print("Done. Generated 51 benchmarks in benchmarks/")
print("Function families: 17")
print("Variants per family: 3")