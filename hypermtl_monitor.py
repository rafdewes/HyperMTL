# Rafael Dewes  2021
# Process HyMTL

import itertools
from hypermtl import *
from processing_hymtl import *
from hypermtl_lexer_parser import *
import discretization
import reelay 
from output_handler import WriteOutput

verbose = False

class DenseMonitorInstance:

    def __init__(self, name, topop, innerspec):
        self.name = name
        self.topop = topop
        self.monitor = reelay.dense_timed_monitor(pattern=innerspec)
        self.out = []

    def run(self, trace, abort=True):
        output = {}
        sat = True
        if self.topop == "F":
            sat = False
        for i in trace:
            update = self.monitor.update(i)
            if len(update) > 0:
                output = update[0]
                self.out.extend(update)
                if (self.topop == "G"):
                    if not (output['value']):
                        print('Violation detected at {err_time} on {monitorname}!'.format(err_time=self.monitor.now(),monitorname=self.name))
                        sat = False
                        if abort:
                            return sat
                elif (self.topop == "F"):
                    if (output['value']):
                        sat = True
                        if abort:
                            return sat
                else:
                    sat = output["value"]
        return sat
            
    

class DiscreteMonitorInstance:

    def __init__(self, name, topop, innerspec):
        self.name = name
        self.topop = topop
        self.monitor = reelay.discrete_timed_monitor(pattern=innerspec)
        self.out = []

    def run(self, trace, abort=True):
        output = {}
        sat = True
        if self.topop == "F":
            sat = False
        for i in trace:
            update = self.monitor.update(i)
            if len(update) > 0:
                output = update
                self.out.extend(update)
                if (self.topop == "G"):
                    if not (output['value']):
                        print('Violation detected at {err_time} on {monitorname}!'.format(err_time=self.monitor.now(),monitorname=self.name))
                        sat = False
                        if abort:
                            return sat
                elif (self.topop == "F"):
                    if (output['value']):
                        sat = True
                        if abort:
                            return sat
                else:
                    sat = output["value"]

        return sat


class MonitorBuilder:
    def __init__(self, topop, innerspec, discrete=True):
        self.discrete = discrete
        self.topop = topop
        self.innerspec = innerspec
    
    def build_monitor(self, name):
        if (self.discrete):
            return DiscreteMonitorInstance(name, self.topop, self.innerspec)
        else:
            return DenseMonitorInstance(name, self.topop, self.innerspec)


class HyperMonitor:
    def __init__(self, spec_ast, discrete=False, sample_rate=1.0):
        self.results = []
        topop = get_unbounded_operator(spec_ast)
        if discrete:
            innerspec = unparse(discretization.discretize_MTL(pastify_mtl(spec_ast), sample_rate))
        else:
            innerspec = unparse(pastify_mtl(spec_ast))
        self.quantifiers = get_trace_quantifiers(spec_ast, "")
        self.builder = MonitorBuilder(topop, innerspec, discrete)
        self.names = []
        self.output = False
            
    def prepare_output(self, outputfile):
        self.to_write = True
        self.output = WriteOutput(outputfile)
        self.output.write_header("## MONITORING RESULTS")

    def prepare_names(self, names):
        nameslist = itertools.product(names, repeat=len(self.quantifiers))
        for name in nameslist:
            self.names.append(name)
        return True

    def build_and_run_instances(self, tuples, abort=False):
        i = 0
        for traces in tuples:
            name = self.names[i]
            if verbose:
                print("running monitor over trace assignment "+ str(name))
            monitor = self.builder.build_monitor(name)
            result = (monitor.run(traces))
            if self.output:
                self.output.output(str(monitor.out),"Monitor output for trace assignment "+str(name))
            if verbose:
                print("result:"+ str(result))
            self.results.append((name,result))
            if abort and not result:
                break
            # output run to file?
            i += 1
        if self.output:
            self.output.output(str(self.results),"\n Complete output for all assignments:")
        return i
    
    def evaluate_runs(self):
        #TODO: handle Alternation

        for n,v in self.results:
            if v == False:
                return False
        
        return True


        



