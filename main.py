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
import hypermtl_lexer_parser
import hypermtl_traces
import hypermtl_monitor
import discretization



def main(spec, file_in, file_out="hymtl_monitor.out", discrete=False):

    # 1. prepare monitor from spec
    spec_tree = hypermtl_lexer_parser.build_hymtl_ast(spec)

    monitor = hypermtl_monitor.HyperMonitor(spec_tree, False)

    trace_quant = monitor.quantifiers

    # 2. handle trace input, build tuples
    trace_set = hypermtl_traces.TraceSet(fileinput)

    trace_num = len(trace_set.traces)

    monitor.prepare_names(range(1,trace_num+1))

    trace_set.build_tuples(len(trace_quant))

    trace_set.build_supertraces()

    # 3. feed processed traces into monitor
    runs = monitor.build_and_run_instances(trace_set.supertraces)

    print("monitored "+str(runs)+" trace assignments")

    # 4. output
    print("RESULTS")

    print(monitor.results)


fileinput = "traces_a.txt"

spec = "forall{1}forall{2}G[0:inf]((G[0:2]{x_1} and not {y_1}) -> F[0:1]{x_2})"

main(spec, fileinput)
