"""
First(X) = {t | X -> * t \\alpha } U { \\varepsilon | X -> * \\varepsilon }
"""
from grammar import create_grammar
from utilsets import format_set


class FirstSet:
    def __init__(self, grammar):
        self.grammar: dict = create_grammar(grammar)

    def check_is_terminal(self, input_string: str):
        return input_string not in self.grammar.keys()

    def compute(self, input_string: str):
        """
        Rules:

        - First(t) = {t}, where t is a terminal
        - \\varepsilon "is element of" First(X)
          - if X -> \\varepsilon
          - if X -> A_1 ... A_n and \\varepsilon "is element of" First(A_i)
        - First(\\alpha) "is a subset of" First(X) if X -> A_1 ... A_n \\alpha
          - and \\varepsilon "is element of" First(A_i)

        """
        if self.check_is_terminal(input_string):
            return set([input_string])

        result = []
        for tokens in self.grammar[input_string]:
            token = tokens.split(" ")[0]
            # get just the first
            result.extend(self.compute(token))
        return set(result)


def test_first_set():
    grammar = """
    E: T X
    T: ( E ) | int Y
    X: + E | \\varepsilon
    Y: * T | \\varepsilon
    """
    firstset = FirstSet(grammar)
    for s, expected in [
        ("+", {"+"}),
        ("*", {"*"}),
        ("int", {"int"}),
        ("(", {"("}),
        (")", {")"}),
        ("T", {"(", "int"}),
        ("E", {"(", "int"}),
        ("X", {"+", "\\varepsilon"}),
        ("Y", {"*", "\\varepsilon"}),
    ]:
        print(f'FirstSet("{s}") = {format_set(expected)}', end=" >>> ")
        result = firstset.compute(s)
        print(f"Result: {result}, Expected: {expected}")
        assert result == expected


if __name__ == "__main__":
    test_first_set()
