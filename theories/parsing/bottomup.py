"""

Grammar:

E ->  T * E | T
T ->  int + T | int |  ( E )

how many shift and how many reduce moves does it take to
accept the input string: ((int + int)*int)

Parsing:
01. .((int + int)*int)
02. (.(int + int)*int) # shift
03. ((.int + int)*int) # shift
04. ((int. + int)*int) # shift NOTE: shift reduce
05. ((int +. int)*int) # shift
06. ((int + int.)*int) # shift
07. ((int + T.)*int) # reduce
08. ((T.)*int) # reduce
09. ((E.)*int) # reduce
10. ((E).*int) # shift
10. (T.*int) # reduce
11. (T*.int) # shift
12. (T*int.) # shift
13. (T*T.) # reduce
14. (T*E.) # reduce
15. (E.) # reduce
15. (E). # shift
16. E # reduce

Expected: shift=9 and reduce=9
Result: shift=9 and reduce=8 note: E' -> E should count?
"""
