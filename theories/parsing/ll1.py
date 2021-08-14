"""
Construct a parsing table T for CFG G.

For each production "A -> \\alpha" in G do:

- For each terminal t "is an element of" First(\\alpha) do:
  - T[A, t] = \\alpha

- i \\varepsilon "is an element of" First(\\alpha),
  for each t "element of" Follow(A) do
  - T[A, t] = \\alpha

- If \\varepsilon "is an element of" First(\\alpha) and
  $ "is an element of" Follow(A) do:
  - T[A, $] = \\alpha
"""
from copy import deepcopy

import pandas as pd

from firstsets import FirstSet
from followsets import FollowSet
from utilsets import format_set


class LL1:
    def __init__(self, grammar):
        self.firstset = FirstSet(grammar)
        self.followset = FollowSet(grammar)
        self.grammar: dict = self.firstset.grammar
        self.terminals = None
        self.non_terminals = None

    def _get_terminals(self):
        if self.terminals:
            return self.terminals

        non_terminals = self._get_non_terminals()
        terminals = []

        for productions in self.grammar.productions.values():
            for alternatives in productions:
                for p in alternatives.split(" "):
                    if p == "\\varepsilon":
                        continue
                    if p not in non_terminals:
                        terminals.append(p)
        self.terminals = terminals
        return self.terminals

    def _get_non_terminals(self):
        if not self.non_terminals:
            self.non_terminals = list(self.grammar.productions.keys())
        return self.non_terminals

    def compute(self):
        terminals = self._get_terminals()
        terminals_map = {k: set() for k in terminals}
        terminals_map["$"] = set()

        non_terminals = self._get_non_terminals()
        parsing_table = {k: deepcopy(terminals_map) for k in non_terminals}

        # For each production "A -> \\alpha" in G do:

        for non_terminal, productions in self.grammar.productions.items():
            non_terminal_followset = self.followset.compute(non_terminal)

            for alternatives in productions:
                for p in alternatives.split(" "):
                    p_has_epsilon = "\\varepsilon" in self.firstset.compute(p)

                    # - If \\varepsilon "is an element of" First(\\alpha) and
                    #   $ "is an element of" Follow(A) do:
                    #   - T[A, $] = \\alpha
                    if p_has_epsilon and "$" in non_terminal_followset:
                        parsing_table[non_terminal]["$"] |= {alternatives}

                    for t in terminals:
                        # - For each terminal t "is an element of" First(\\alpha) do:
                        #   - T[A, t] = \\alpha
                        # - if \\varepsilon "is an element of" First(\\alpha),
                        #   for each t "element of" Follow(A) do
                        #   - T[A, t] = \\alpha
                        if t in self.firstset.compute(p):
                            parsing_table[non_terminal][t] |= {alternatives}
                        elif p_has_epsilon and t in non_terminal_followset:
                            parsing_table[non_terminal][t] |= {alternatives}

        return pd.DataFrame(parsing_table).T


def test_ll1():
    grammar = """
    E -> T X
    T -> ( E ) | int Y
    X -> + E | \\varepsilon
    Y -> * T | \\varepsilon
    """

    expected = pd.DataFrame(
        {
            "E": {
                "(": "T X",
                ")": "",
                "+": "",
                "*": "",
                "int": "T X",
                "$": "",
            },
            "T": {
                "(": "( E )",
                ")": "",
                "+": "",
                "*": "",
                "int": "int Y",
                "$": "",
            },
            "X": {
                "(": "",
                ")": "\\varepsilon",
                "+": "+ E",
                "*": "",
                "int": "",
                "$": "\\varepsilon",
            },
            "Y": {
                "(": "",
                ")": "\\varepsilon",
                "+": "\\varepsilon",
                "*": "* T",
                "int": "",
                "$": "\\varepsilon",
            },
        }
    )

    ll1 = LL1(grammar)
    parsing_table = ll1.compute()
    print(parsing_table)


def test_ll1_2():
    grammar = """
    S -> b A b | b B a
    A -> a S | C B
    B -> b | B c
    C -> c | c C
    """
    ll1 = LL1(grammar)
    parsing_table = ll1.compute()
    print(parsing_table)


if __name__ == "__main__":
    # test_ll1()
    test_ll1_2()
