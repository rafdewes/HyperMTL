#!/usr/bin/env python3

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


from discretization import sample_trace
import sys, getopt
import argparse
import time

import hypermtl_lexer_parser
import hypermtl_traces
import hypermtl_monitor



def main(file_spec, file_traces, file_out="", discrete=False, sample_rate=1.0, Verbose=True):
    # 0. handle spec input
    if Verbose:
        start_time_total = time.time()
        print("Reading from "+file_spec+" ...")
    
    with open(file_spec, 'r') as f:
        spec = f.read()

    if Verbose:
        print("Specification: "+spec)

    # 1. prepare monitor from spec
    spec_tree = hypermtl_lexer_parser.build_hymtl_ast(spec)

    if discrete:
        if Verbose:
            print("Sampling period is "+str(sample_rate))
        monitor = hypermtl_monitor.HyperMonitor(spec_tree, discrete, sample_rate)
    else:
        monitor = hypermtl_monitor.HyperMonitor(spec_tree)

    if file_out != "":
        monitor.prepare_output(file_out)

    trace_quant = monitor.quantifiers

    # 2. handle trace input, build tuples
    if Verbose:
        print("Reading traces from "+file_traces+" ...")
    trace_set = hypermtl_traces.TraceSet(file_traces)

    if Verbose:
        trace_num_old = trace_set.get_trace_num()
        print("Found "+str(trace_num_old)+" traces.")

    if discrete:
        trace_set.discretize_traceset(sample_rate)

    trace_set.remove_duplicates()

    trace_num = trace_set.get_trace_num()

    if Verbose:
        if trace_num_old > trace_num: print("Removed %d redundant traces" %(trace_num_old - trace_num))

    monitor.prepare_names(range(1,trace_num+1))

    trace_set.build_tuples(len(trace_quant))

    trace_set.build_supertraces()

    # 3. feed processed traces into monitor
 
    if Verbose:
        start_time = time.time()
        print("finished preprocessing in %s seconds" % (start_time-start_time_total))
        print("Running "+str(pow(trace_num,len(trace_quant)))+" monitor instances...")
    runs = monitor.build_and_run_instances(trace_set.supertraces, abort=False)

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
            print("trace set does not satisfy specification")
            print("Counterexample: assignment "+str(x))
            break
    
    if a == 0:
        print("specification is satisfied")
    


    #print(monitor.results)


# C-Style Command Line arguments
def command_input(argv):

    input_spec = ""
    input_traces = ""
    outputfile = "hymtl_monitor.out"
    discrete = False
    samplerate = 1.0
    verbose = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["spec=","ifile="])
    except getopt.GetoptError:
        print ('problem with input format')
        print ('morthy.py -s <inputfile spec> -i <inputfile traces> -o <outputfile> -d <discrete> -r <sample rate> -v <VERBOSE>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('morthy.py -s <inputfile spec> -i <inputfile traces> -o <outputfile> -d <discrete> -r <sample rate> -v <VERBOSE>')
            sys.exit()
        elif opt in ("-s", "--spec"):
            input_spec = arg
        elif opt in ("-i", "--ifile"):
            input_traces = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d", "--discrete"):
            discrete = True
        elif opt in ("-r", "--samplerate", "--rate"):
            samplerate = float(arg)
        elif opt in ("-v", "--verbose"):
            verbose = True
    main(input_spec, input_traces, outputfile, discrete, samplerate, verbose)

#if __name__ == "__main__":
#    command_input(sys.argv[1:])

argsparser = argparse.ArgumentParser()
argsparser.add_argument("spec", type=str, help="file with HyperMTL specification")
argsparser.add_argument("traces", type=str, help="file with list of traces")
argsparser.add_argument("-o","--outputfile", type=str, help="set outputfile")
argsparser.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")
argsparser.add_argument("-d","--discretize", type=float, help="enable discretization and set samplerate")
args = argsparser.parse_args()
if args.outputfile:
    if args.discretize:
        main(args.spec, args.traces, file_out=args.outputfile, discrete=True, sample_rate=args.discretize, Verbose=args.verbose)
    else:
        main(args.spec, args.traces, file_out=args.outputfile, Verbose=args.verbose)
else:
    if args.discretize:
        main(args.spec, args.traces, discrete=True, sample_rate=args.discretize, Verbose=args.verbose)
    else:
        main(args.spec, args.traces, Verbose=args.verbose)
