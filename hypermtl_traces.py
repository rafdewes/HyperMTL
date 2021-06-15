
# Rafael Dewes  2021

# class traceset:
# - contains list of trace tuples: original trace names + resulting "supertrace"
# - get_next function to return one trace tuple
# - is built from input file

# function rename_aps(trace, ordinate):
# rename APs in trace to include ordinate, return new trace

# function build_supertrace(traceold, tracenew):
# combine two traces, per timestamps, return supertrace

from operator import itemgetter
import itertools
import ast

class TraceSet:
    def __init__(self, inputfile):
        self.traces = read_traces(inputfile)
        self.supertraces = []
        self.tuples = []
        self.quantifier = 0
        self.altquantifier = 0
    
    def build_tuples(self, size):
        self.tuples = itertools.product(self.traces, repeat=size)
        return True


def read_traces(file):
    with open(file, 'r') as f:
        traces = f.read()
        d = ast.literal_eval(traces)
        return d


def rename_aps(trace, ordinate):
    for i in range(len(trace)):
        timestampnew = {}
        timestampold = trace[i]
        for k,v in timestampold.items():
            if k == 'time':
                timestampnew['time'] = v
            else:
                timestampnew[str(k)+'_'+str(ordinate)] = v
        trace[i] = timestampnew
    return trace


def build_supertrace(traceold, tracenew):
    # assume aps are unique
    supertrace = []
    supertrace.extend(traceold)

    for tstamp in tracenew:
        t = x[time] 

        to_merge = next((i for i, item in enumerate(supertrace) if item['time'] == t), False)

        if to_merge == False:
            supertrace.append(tstamp)
        else:
            supertrace[to_merge].update(tstamp)

    
    return sorted(supertrace, key= lambda o: o['time'])

