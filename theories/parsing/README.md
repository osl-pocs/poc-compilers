# Parsing

## LL1

- if any entry is multiply defined then G is not LL(1)
  - not left factored
  - left recursive
  - ambiguous
  - if the grammar required more than 1 token of look ahead
  - etc ...
- most programming language CFGs are not LL(1)

## Bottom-Up Parsing

- A bottom-up parsing traces a righmost derivation in reverse

### Shift-Reduce Parsing

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


### Handle

## Credits:
- Notes from the Compiler course:
  - https://learning.edx.org/course/course-v1:StanfordOnline+SOE.YCSCS1+3T2020
