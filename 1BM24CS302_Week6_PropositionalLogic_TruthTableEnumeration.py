def evaluate_propositional_kb(variables, kb_sentences, queries):
    num_vars = len(variables)
    to_tf = lambda val: "T" if val else "F"

    headers = list(variables) + [f"KB{i+1}" for i in range(len(kb_sentences))] + ["KB True?"]
    
    col_widths = [max(len(h), 8) for h in headers]

    header_cols = [f"{headers[i]:^{col_widths[i]}}" for i in range(len(headers))]
    header_line = "|".join(header_cols)
    print(header_line)
    print("-" * len(header_line))

    models = []

    def get_combinations(n):
        if n == 0:
            yield []
            return
        for rest in get_combinations(n - 1):
            for val in [True, False]:
                yield rest + [val]

    for combo in get_combinations(num_vars):
        env = dict(zip(variables, combo))
        kb_results = [func(**env) for func in kb_sentences]
        is_kb_true = all(kb_results)


        if is_kb_true:
            models.append(env)

        values = [to_tf(env[v]) for v in variables] + [to_tf(res) for res in kb_results] + [to_tf(is_kb_true)]
        row_cols = [f"{values[i]:^{col_widths[i]}}" for i in range(len(values))]
        row_line = "|".join(row_cols)
        print(row_line)

    print("\n" + "="*40)
    print("Models where KB is True:")
    if not models:
        print("No models found (KB is inconsistent/unsatisfiable).")
    else:
        for i, m in enumerate(models, 1):
            model_str = ", ".join([f"{k}={to_tf(v)}" for k, v in m.items()])
            print(f"Model {i}: {{{model_str}}}")

    print("\nEntailment Results:")
    for name, query_func in queries.items():
        entails = all(query_func(**m) for m in models) if models else True
        print(f"Does KB entail {name}? -> {'Yes' if entails else 'No'}")

if __name__ == "__main__":
    vars_list = ['P', 'Q', 'R']

    kb = [ 
        lambda P, Q, R: (not Q) or P,
        lambda P, Q, R: (not P) or (not Q),
        lambda P, Q, R: Q or R
    ]

    q_to_check = {
        "R": lambda P, Q, R: R,
        "R -> P": lambda P, Q, R: (not R) or P,
        "Q -> R": lambda P, Q, R: (not Q) or R
    }

    evaluate_propositional_kb(vars_list, kb, q_to_check)
