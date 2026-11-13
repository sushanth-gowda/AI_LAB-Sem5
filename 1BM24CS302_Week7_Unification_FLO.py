import re


def is_variable(x):
  return isinstance(x, str) and "(" not in x and x[0].islower()


def is_compound(x):
  return isinstance(x, str) and "(" in x and x.endswith(")")


def parse_expression(expr):
  expr = expr.strip()
  idx = expr.index("(")
  predicate = expr[:idx].strip()
  args_str = expr[idx + 1 : -1].strip()

  args = []
  depth = 0
  current = []
  for ch in args_str:
    if ch == "(":
      depth += 1
      current.append(ch)
    elif ch == ")":
      depth -= 1
      current.append(ch)
    elif ch == "," and depth == 0:
      args.append("".join(current).strip())
      current = []
    else:
      current.append(ch)
  if current:
    args.append("".join(current).strip())

  return predicate, args


def occurs_check(var, expr):
  if var == expr:
    return True
  if is_compound(expr):
    _, args = parse_expression(expr)
    return any(occurs_check(var, arg) for arg in args)
  return False


def apply_substitution(expr, subst):
  for replacement, var in subst:
    if expr == var:
      expr = replacement
    elif is_compound(expr):
      pred, args = parse_expression(expr)
      new_args = [apply_substitution(arg, [(replacement, var)]) for arg in args]
      expr = f"{pred}({', '.join(new_args)})"
  return expr


def unify(psi1, psi2):
  psi1, psi2 = psi1.strip(), psi2.strip()

  if not is_compound(psi1) or not is_compound(psi2):
    if psi1 == psi2:
      return []
    elif is_variable(psi1):
      if occurs_check(psi1, psi2):
        return "FAILURE"
      return [(psi2, psi1)]
    elif is_variable(psi2):
      if occurs_check(psi2, psi1):
        return "FAILURE"
      return [(psi1, psi2)]
    else:
      return "FAILURE"

  pred1, args1 = parse_expression(psi1)
  pred2, args2 = parse_expression(psi2)

  if pred1 != pred2:
    return "FAILURE"

  if len(args1) != len(args2):
    return "FAILURE"

  subst = []

  for i in range(len(args1)):
    s = unify(args1[i], args2[i])

    if s == "FAILURE":
      return "FAILURE"

    if s:
      for j in range(i + 1, len(args1)):
        args1[j] = apply_substitution(args1[j], s)
        args2[j] = apply_substitution(args2[j], s)
      subst.extend(s)

  return subst


def format_subst(subst):
  if subst == "FAILURE":
    return "FAILURE"
  if not subst:
    return "NIL"
  return "{ " + ", ".join(f"({val}/{var})" for val, var in subst) + " }"


if __name__ == "__main__":
    expr1 = input("Expr 1 : ").strip()
    expr2 = input("Expr 2 : ").strip()

    result = unify(expr1, expr2)
    print(f"\nResult : {format_subst(result)}")
    if result != "FAILURE" and result:
        unified = apply_substitution(expr1, result)
        print(f"Unified: {unified}")
