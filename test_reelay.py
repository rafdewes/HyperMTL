import reelay 
from hypermtl_lexer_parser import *
from processing_hymtl import *
from hypermtl_traces import *


#correct_sys_behavior = [
#    dict(time=0, x=True, y=False),
#	dict(time=2, x=False, y=True),
#	dict(time=3, x=True, y=False),
#	dict(time=4.5, x=True, y=False),
#	dict(time=5, x=True, y=True),
#	dict(time=7, x=False, y=True),
#]

#faulty_sys_behavior = [
#    dict(time=0, x=True, y=True),
#	dict(time=2, x=False, y=False),
#	dict(time=2.5, x=True, y=True),
#	dict(time=4, x=False, y=True),
#	dict(time=4.5, x=True, y=False),
#	dict(time=5, x=True, y=True),
#]

text = "((F[0:2]{x_1}) and not {x_2})"

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


with open('traces/traces_a.txt', 'r') as f:
	traces = f.read()
	print(traces)
	d = ast.literal_eval(traces)
	print(d)

#traceset = TraceSet('traces/traces_a.txt')

#tuples = traceset.build_tuples()

ar1 = []

#for i in correct_sys_behavior:  
#    ar1.extend(my_monitor.update(i))

print("SYS-REQ-1 correct behavior:")
print(ar1)
