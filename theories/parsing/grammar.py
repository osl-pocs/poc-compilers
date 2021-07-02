def create_grammar(grammar: str):
    result = {}
    for line in grammar.split("\n"):
        if not line or ":" not in line:
            continue

        lhs, rhs = line.split(":")
        lhs = lhs.strip()
        rhs = [v.strip() for v in rhs.split("|")]

        result[lhs] = rhs

    return result
