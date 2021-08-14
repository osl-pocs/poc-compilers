# Parsing

## Glosary

* **left-most derivation** [2]: A left-most derivation is
  one in which the left-most non-terminal is
  always chosen as the next non-terminal to expand.
* **right-most derivation** [2]: A right-most derivation is
  one in which the right-most non-terminal is
  always chosen as the next non-terminal to expand.
* **left-factoring** [3]: Parsing conflicts in top-down
  parsers are common, and some ways to modify a grammar to
  eliminate conflicts are known. A simple and natural one is left-factoring. For example, look at the grammar that led to a parsing conflict.

  1. L	→	ε
  2. L	→	N
  3. N	→	E
  4. N	→	E, N
  5. E	→	n

  Two productions, N → E and N → E , N, begin with the same
  prefix. A top-down parser can never predict which one to
  use in that situation. So you factor out the common prefix,
  introducing a new nonterminal to represent what comes after
  the common prefix. Calling that nonterminal R yields the
  following modified grammar.

  1. L	→	ε
  2. L	→	N
  3. N	→	E R
  4. R	→	ε
  5. R	→	, N
  6. E	→	n

  That is the grammar that did not lead to any parsing conflicts.

* **Formal Grammar** [4]:
  A formal grammar is essentially a set of production rules
  that describe all possible strings in a given formal
  language.

* **Production rules** [4]:
  Production rules are simple replacements. There can be
  multiple replacement rules for a given nonterminal symbol

* **CFG** [4]:
  A context-free grammar (CFG) is a formal grammar whose
  production rules are of the form

  A -> $\alpha$

  with A a single nonterminal symbol, and $\alpha$  a string
  of terminals and/or nonterminals ($\alpha$  can be empty).
  A formal grammar is "context free" if its production rules
  can be applied regardless of the context of a nonterminal.
  No matter which symbols surround it, the single nonterminal
  on the left hand side can always be replaced by the right
  hand side.

* **PEG** [5]: Parsing Expression Grammar (PEG), is a type of
  analytic formal grammar, i.e. it describes a formal
  language in terms of a set of rules for recognizing strings
  in the language. It is closely related to the family of
  top-down parsing languages introduced in the early 1970s.
  Syntactically, PEGs also look similar to context-free
  grammars (CFGs), but they have a different interpretation:
  the choice operator selects the first match in PEG, while
  it is ambiguous in CFG. This is closer to how string
  recognition tends to be done in practice, e.g. by a
  recursive descent parser.

* **Left recursion** [6]:
  A nonterminal is left-recursive if the leftmost symbol in one of its productions is itself (in the case of direct left recursion) or can be made itself by some sequence of substitutions (in the case of indirect left recursion).

* **ambiguous grammar** [7]:
  An ambiguous grammar is a context-free grammar for which there exists a string that can have more than one leftmost derivation or parse tree,[1] while an unambiguous grammar is a context-free grammar for which every valid string has a unique leftmost derivation or parse tree.


* **static scope**:
* **dynamic scope**:
* **recursive descent traversal of a tree**:
* **type environment**:
* **subtype**:
* **least upper bond** [8]
* **least common ancestor**
* **inference rule**
* **soundness theorem**


## CFG vs PEG

* https://en.wikipedia.org/wiki/Parsing_expression_grammar#Semantics

## Top-down vs Bottom-up

* https://www.geeksforgeeks.org/difference-between-top-down-parsing-and-bottom-up-parsing/


## LL1 [1]

- if any entry is multiply defined then G is not LL(1)
  - not left factored
  - left recursive
  - ambiguous
  - if the grammar required more than 1 token of look ahead
  - etc ...
- most programming language CFGs are not LL(1)

## Bottom-Up Parsing [1]

- a bottom-up parsing traces a righmost derivation in reverse
- in shift-reduce parsing "handles" appear only
  at the top of the stack, never inside.
- for any grammar, the set of viable prefix is a
  regular language

### Shift-Reduce Parsing [1]

- Idea: Split string into two substrings
  - Right substring is a yet unexamined by parsing
  - Left substring has terminals and non-terminals
  - The dividing point is marded by a "|"

- Bottom-up parsing uses only two kinds of actions:
  - Shift moves: Move "|" one place to right
    - Shifts a terminal to the left string
  - Reduce moves
    - Apply an inverse production at the right end of the left string
      - if A -> xy is a production, then
        - Cbxy|ijk => CbA|ijk

Example:

```
| int * int + int
int | * int + int
int * | int + int
int  * int | + int
int * T | + int
T | + int
T + | int
T + int |
T + T |
T + E |
E |
```

Note: Reduces occurs just at the left side of "|".

- Left string can be implemented by a stack
  - top of the stack in the "|"

- Shift pushes a terminal on the stack

- Reduce
  - pops 0 or more symbols off of the stack (production rhs)
  - pushes a non-terminal on the stack (production lhs)

- In given state, more than one action (shift or reduce) may to lead to
  a valid parse (NOT GOOD, BUT OFTEM EASIER TO REMOVE, E.G. USING PRECEDENCE)

- if it is legal to shift or reduce, there is a shift-reduce conflict

- if it is legal to reduce by two different productions, there is a reduce-reduce conflict (BAD)


### Handle [1]

- A handle is a reduction that also allows
  further reductions back to the start symbol

- A valid handle is a full right-hand side of a
  production at the top of the stack that also sits in a
  context that can be further reduced back to the start symbol.
  Remember that only a single reduction may be done at a time.


## SLR(1)

- If the grammar has shift/reduce or reduce reduce conflict it not SLR(1).

## References:
- [1] https://learning.edx.org/course/course-v1:StanfordOnline+SOE.YCSCS1+3T2020
- [2] https://home.cs.colorado.edu/~bec/courses/csci4555-f11/meetings/meeting06-markednotes.pdf
- [3] http://www.cs.ecu.edu/karl/5220/spr16/Notes/Top-down/leftFactor.html
- [4] https://en.wikipedia.org/wiki/Context-free_grammar
- [5] https://en.wikipedia.org/wiki/Parsing_expression_grammar
- [6] https://en.wikipedia.org/wiki/Left_recursion
- [7] https://en.wikipedia.org/wiki/Ambiguous_grammar
- [8] https://math.hws.edu/eck/math331/guide2020/03-least-upper-bound-axiom.html
