import reelay 
from hypermtl_lexer_parser import *
from pastify_mtl import *

correct_sys_behavior = [
    dict(time=0, x_1=True, y_1=False),
	dict(time=2, x_1=False, y_1=True),
	dict(time=3, x_1=True, y_1=False),
	dict(time=4.5, x_1=True, y_1=False),
	dict(time=5, x_1=True, y_1=True),
	dict(time=7, x_1=False, y_1=True),
]

faulty_sys_behavior = [
    dict(time=0, x=True, y=True),
	dict(time=2, x=False, y=False),
	dict(time=2.5, x=True, y=True),
	dict(time=4, x=False, y=True),
	dict(time=4.5, x=True, y=False),
	dict(time=5, x=True, y=True),
]

text = "((F[0:2]{x_1}) and not {y_1})"

lexer = HyMtlLexer()
parser = HyMtlParser()

mtlTree = parser.parse(lexer.tokenize(text))

text_n = unparse(mtlTree)

print(text_n)

mtlTreePast = pastify_mtl(mtlTree)

text_p = unparse(mtlTreePast)

print(text_p)


my_monitor = reelay.dense_timed_monitor(
    pattern=text_p)

ar1 = []

for i in correct_sys_behavior:  
    ar1.extend(my_monitor.update(i))

print("SYS-REQ-1 correct behavior:")
print(ar1)
