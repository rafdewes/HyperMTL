# Rafael Dewes 2021

# Input:
# - HyperMTL specification as a string
# - A file with a list of traces
# - Output file location
# - flag discrete
#
# Output:
# - If a violation was found: Respective Traces and Time
# - Else: The trace set satisfies the specification
# - Write selected output to file?


import sys
import ast
import time

import hypermtl_lexer_parser
import hypermtl_traces
import hypermtl_monitor
import discretization


Verbose = True


def main(spec, file_in, file_out="hymtl_monitor.out", discrete=False):

    # 1. prepare monitor from spec
    if Verbose:
        print("Processing specification...")
    spec_tree = hypermtl_lexer_parser.build_hymtl_ast(spec)

    monitor = hypermtl_monitor.HyperMonitor(spec_tree, False)

    trace_quant = monitor.quantifiers

    # 2. handle trace input, build tuples
    if Verbose:
        print("Processing traces...")
    trace_set = hypermtl_traces.TraceSet(fileinput)

    trace_num = len(trace_set.traces)

    monitor.prepare_names(range(1,trace_num+1))

    trace_set.build_tuples(len(trace_quant))

    trace_set.build_supertraces()

    # 3. feed processed traces into monitor
    if Verbose:
        start_time = time.time()
        print("Running monitors...")
    runs = monitor.build_and_run_instances(trace_set.supertraces)

    if Verbose:
        runtime = time.time() - start_time
        print("monitored %d trace assignments in %s seconds" % (runs, runtime))

    # 4. output
    print("RESULTS")

#    foralls = 0
#    for q in trace_quant:
#        if q == "A":
#            foralls += 1

    a = 0
    for x,v in monitor.results:
        if v is False:
            a += 1
            print("does not satisfy")
            print("Counterexample: assignment"+str(x))
            break
    
    if a == 0:
        print("spec is satisfied")
    


    #print(monitor.results)


fileinput = "traces/traces_b.txt"

spec = "forall{1}forall{2}forall{3}G[0:inf]((G[0:1.5]{x_1} and {y_2}) -> F[0:2]{z_3})"

main(spec, fileinput)
