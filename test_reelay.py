import reelay 
from hypermtl_lexer_parser import *
from processing_hymtl import *
from hypermtl_traces import *


correct_sys_behavior = [
    dict(time=0, x=True, y=False),
	dict(time=2, x=False, y=True),
	dict(time=3, x=True, y=False),
	dict(time=4.5, x=True, y=False),
	dict(time=5, x=True, y=True),
	dict(time=7, x=False, y=True),
]

faulty_sys_behavior = [
    dict(time=0, x=True, y=True),
	dict(time=2, x=False, y=False),
	dict(time=2.5, x=True, y=True),
	dict(time=4, x=False, y=True),
	dict(time=4.5, x=True, y=False),
	dict(time=5, x=True, y=True),
]



text = "forall{1}forall{2}((F[0:2]{x_1}) and not {x_2})"

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


traceset = TraceSet('traces_a.txt')

traceset.build_tuples(2)

traceset.build_supertraces()

traces = traceset.supertraces[1]

new_trace = build_supertrace(rename_aps(correct_sys_behavior,1), rename_aps(faulty_sys_behavior,1))

print(new_trace)
print(traces)

ar1 = []

for i in traces:  
    update = my_monitor.update(i)
    print(update)
    ar1.extend(update)
    print(ar1)

print("SYS-REQ-1 correct behavior:")
print(ar1)
