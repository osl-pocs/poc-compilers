"""
First(X) = {t | X -> * t \\alpha } U { \\varepsilon | X -> * \\varepsilon }
"""
from grammar import Grammar
from utilsets import format_set


class FirstSet:
    def __init__(self, grammar):
        self.grammar: dict = Grammar(grammar)

    def check_is_terminal(self, input_string: str):
        return input_string not in self.grammar.productions.keys()

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
        for tokens in self.grammar.productions[input_string]:
            token = tokens.split(" ")[0]
            # get just the first
            result.extend(self.compute(token))
        return set(result)


def test_first_set():
    grammar = """
    E -> T X
    T -> ( E ) | int Y
    X -> + E | \\varepsilon
    Y -> * T | \\varepsilon
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


def test_first_set2():
    # TODO,fix error
    grammar = """
    S ->  A ( S ) B | \\varepsilon
    A ->  S | S B | x | \\varepsilon
    B ->  S B | y
    """
    firstset = FirstSet(grammar)
    result = firstset.compute("S")
    print("First(S) = ", result)


def test_first_set3():
    # TODO,fix error
    grammars = []
    grammars.append("""
        E ->  id T | ( E ) T
        T ->  + id | * id
    """)
    grammars.append("""
        S -> b S b | A | \\varepsilon
        A -> a A | \\varepsilon
    """)
    grammars.append("""
        R -> a R' | ( R ) R'
        R' -> \\varepsilon | X R'
        X -> . R | + R | *
    """)
    for i, grammar in enumerate(grammars):
        print(f"Grammar {i}")
        firstset = FirstSet(grammar)
        for non_terminal in firstset.grammar.productions.keys():
            result = firstset.compute(non_terminal)
            print(f"First({non_terminal}) = ", result)


def test_first_set4():
    """
    Expected:

    - First(U) = {a, b, c}
    """
    grammar = """
    S -> a T U b | \\varepsilon
    T -> c U c | b U b | a U a
    U -> S b | c c
    """
    firstset = FirstSet(grammar)
    for non_terminal in firstset.grammar.productions.keys():
        result = firstset.compute(non_terminal)
        print(f"First({non_terminal}) = ", result)


if __name__ == "__main__":
    # test_first_set()
    # test_first_set2()
    # test_first_set3()
    test_first_set4()
