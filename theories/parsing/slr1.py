"""
gramar 1:

S ->  A ( S ) B | \\varepsilon
A ->  S | S B | x | \\varepsilon
B ->  S B | y

Items n the initial state of the SLR(1) parsing automaton
for the previous grammar

S: .A ( S ) B
S: .
A: .S
A: .S B
A: .x
A: .
B: .S B
B: .y


gramar 2:

S -> E
E -> E + T | T
T -> T * F | F
F -> id


grammar 3:

S -> a B S | a a | a
B -> a

Parsing:

1.
S' -> .S
S  -> .a B S
S  -> .a a
S  -> .a
B  -> .a

2. (1) --S-->
S' -> S.

3. (1) --a-->
S  -> a. B S
S  -> a. a
S  -> a.
B  -> a.

f. (3) --a-->
S  -> a a.

5. (3) --B-->
S  -> a B. S

6. (5) --S-->
S  -> a B S.


grammar 4:

S -> (T)
T -> T + int | int

String input: (int + int + int + int + int)

Parsing

00. .(int + int + int + int + int)
01. (.int + int + int + int + int)  # shift
02. (int. + int + int + int + int)  # shift
03. (T. + int + int + int + int)  # reduce
04. (T +. int + int + int + int)  # shift
05. (T + int. + int + int + int)  # shift
06. (T. + int + int + int)  # reduce
07. (T +. int + int + int)  # shift
08. (T + int. + int + int)  # shift
09. (T. + int + int)  # reduce
10. (T +. int + int)  # shift
11. (T + int. + int)  # shift
12. (T. + int)  # reduce
13. (T +. int)  # shift
14. (T + int.)  # shift
15. (T.)  # reduce
16. (T).  # shift
17. S.  # reduce

n (number of "int"s) = 5
shift = 11
reduce = 6

grammar 5:

S -> (T)
T -> int + T | int

String input: (int + int + int + int + int)

Parsing

00. .(int + int + int + int + int)
01. (.int + int + int + int + int)  # shift
02. (int. + int + int + int + int)  # shift
03. (int +. int + int + int + int)  # shift
04. (int + int. + int + int + int)  # shift
05. (int + int +. int + int + int)  # shift
06. (int + int + int. + int + int)  # shift
07. (int + int + int +. int + int)  # shift
08. (int + int + int + int. + int)  # shift
09. (int + int + int + int +. int)  # shift
10. (int + int + int + int + int.)  # shift
11. (int + int +. int + int + T.)  # reduce
12. (int + int +. int + T.)  # reduce
13. (int + int +. T.)  # reduce
14. (int + T.)  # reduce
15. (T.)  # reduce
16. (T).  # shift
17. S.  # reduce

n (number of "int"s) = 5
shift = 11
reduce = 6



grammar 6:

S -> b a S a b | b a S | b

Parsing:

S' -> S
S -> b a S a b
S -> b a S
S -> b

Resources:
- https://www.javatpoint.com/slr-1-parsing
- http://jsmachines.sourceforge.net/machines/slr.html

"""
