# coding: utf-8
import re
p = re.compile('“|”|‘|’\s|’[.!?,]')


case1 = "“something"
case2 = "words”somethingelse"
case3 = "‘thing1"
case4 = "’ anotherthing"
case5 = "wont’t"
case6 = "’.ano’!the’?rth’,ing"
case7 = "”"

a = p.findall(case1)
b = p.findall(case2)
c = p.findall(case3)
d = p.findall(case4)
e = p.findall(case5)
f = p.findall(case6)
g = p.findall(case7)

print(a)
print(b)
print(c)
print(d)
print(e)
print(f)
print(g)

print(len(a))
print(len(b))
print(len(c))
print(len(d))
print(len(e))
print(len(f))
print(len(g))

# if any input is larger than 1 length

# testing
# see the url and the associated quotes check
