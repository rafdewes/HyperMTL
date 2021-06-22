# HyperMTL Monitoring 

This is a prototype implementation for sequential monitoring of HyperMTL.

The program will evaluate if a HyperMTL-B specification is satisfied by a list of traces.
To run it, execute file `morthy.py` with two arguments: (1) input file of the HyperMTL specification formatted as described below, (2) input file with list of traces.

Example: `morthy.py specs/spectest_a traces/traces_a.txt -v`

Other command options: `-v` verbosity, `-d <samplerate>` enable discretization, `-o <outputfile>` set output

## Install requirements

Written in python 3, the implementation builds on the [reelay package](https://doganulus.github.io/reelay/) from Dogan Ulus.
Additional requirements are packages sly and all [inherited requirements](https://doganulus.github.io/reelay/install/) from reelay, namely a C++ compiler, the boost libraries for C++ and pybind11.


## Specification format

The specification format is based on the rye format for reelay.

Example:
`forall{1}forall{2}G[0:inf](F[0.5:1.5]{x_1} -> F[1:3]{x_2})`

Use the following operators:

Trace quantifiers: `forall{n}` or `exists{n}`

Temporal operators: `G[a:b] , F[a:b] , H[a:b] , P[a:b] , S[a:b] `

Logic operators: `not , ~ , and , && , or , || , -> , <->`

Atomic propositions: `{p_n}`

## Trace format

Traces are implemented as lists of dicts, each dict represents a timestamp:

    [
      {'time':0, 'x':True},
      {'time':0.6, 'x':False},
      {'time':1.5, 'x':True},
      {'time':2.2, 'x':False},
      {'time':2.67, 'x':True},
      {'time':5, 'x':False},
    ]

The input file for the trace set is then a list of traces.

## Semantics

We assume interval semantics for the traces, meaning the value of `x` is constant until the next timestamp.

## Acknolewdgements

This implementation was built for my thesis Monitoring Real-Time Hyperproperties.

Reelay was created by Dogan Ulus ([Online monitoring of metric temporal logic using sequential networks](https://arxiv.org/abs/1901.00175)).
