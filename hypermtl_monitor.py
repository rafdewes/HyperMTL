# Rafael Dewes  2021
# Process HyMTL

from hypermtl import *
from processing_hymtl import *
from hypermtl_lexer_parser import *
import reelay 

class DenseMonitorInstance:

    def __init__(self, name, topop, innerspec):
        self.name = name
        self.topop = topop
        self.monitor = reelay.dense_timed_monitor(pattern=innerspec)
        self.out = []

    def run(self, trace, abort=False):
        output = {}
        sat = True
        if self.topop == "F":
            sat = False
        for i in trace:
            output = self.monitor.update(i)
            self.out.extend(output)
            if (self.topop == "G"):
                if (output["value"] is False):
                    print('Violation detected at {err_time} on {monitorname}!'.format(err_time=self.monitor.now(),monitorname=self.name))
                    sat = False
                    if abort:
                        return sat
            elif (self.topop == "F"):
                if (output["value"] is True):
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

    def run(self, trace, abort=False):
        output = {}
        sat = True
        if self.topop == "F":
            sat = False
        for i in trace:
            output = self.monitor.update(i)
            self.out.extend(output)
            if (self.topop == "G"):
                if (output["value"] is False):
                    print('Violation detected at {err_time} on {monitorname}!'.format(err_time=self.monitor.now(),monitorname=self.name))
                    sat = False
                    if abort:
                        return sat
            elif (self.topop == "F"):
                if (output["value"] is True):
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
    def __init__(self, spec_ast):
        self.spec_ast = spec_ast
        self.topop = get_unbounded_operator(spec_ast)
        self.innerspec = unparse(get_inner_formula(spec_ast))


