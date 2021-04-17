
# class traceset:
# - contains list of trace tuples: original trace names + resulting "supertrace"
# - get_next function to return one trace tuple
# - is built from input file

# function rename_aps(trace, ordinate):
# rename APs in trace to include ordinate, return new trace?

# function build_supertrace(traceold, tracenew):
# combine two traces, per timestamps, return supertrace
from operator import itemgetter
import itertools

class TraceSet:
    def __init__(self, inputfile):
        self.traces = read_traces(inputfile)
        self.supertraces = []
        self.tuples = []
        self.quantifier = 0
        self.altquantifier = 0
    
    def build_tuples(self, size):
        helperlist = []
        for i in range(size):
            helperlist.append(self.traces)
        self.tuples = itertools.product(*helperlist)
        return True


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
    # assume traces are sorted by timestamp and aps unique
    i = 0
    j = 0
    supertrace = []
    while (i <= len(traceold) && j <= len(tracenew)):

        if (traceold[i])['time'] < (tracenew[j])['time']:
            supertrace.append((traceold[i])
            i++

        elif (traceold[i])['time'] > (tracenew[j])['time']:
            supertrace.append((traceold[i])
            j++

        elif (traceold[i])['time'] == (tracenew[j])['time']:
            supertrace.append(traceold[i].update(tracenew[j]))
            i++
            j++

    return supertrace

