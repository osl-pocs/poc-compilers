def format_set(token_set: set):
    result = []
    for v in token_set:
        result.append(f'"{v}"')
    return "{ " + ", ".join(result) + " }"
