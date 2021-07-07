# MoRtHy - Monitor for Real-time Hyperproperties

This is a prototype implementation for sequential monitoring of HyperMTL.

The program will evaluate if a HyperMTL-B specification is satisfied by a list of traces.
To run it, execute file `morthy.py` with two arguments: (1) input file of the HyperMTL specification formatted as described below, (2) input file with list of traces.

Example: `./morthy.py specs/spectest_a traces/traces_a.txt -v`

Other command options: `-v` verbosity, `-d <samplerate>` enable discretization, `-o <outputfile>` set output for full result

## Install Requirements

Written in python 3, the implementation builds on the [reelay package](https://doganulus.github.io/reelay/) from Dogan Ulus.
Additional requirements are the package **sly** and all [inherited requirements](https://doganulus.github.io/reelay/install/) from reelay, namely a C++ compiler, the **boost libraries for C++** and **pybind11**.


## Specification Format

The specification format is based on the rye format for reelay.

Example:
`forall{1}forall{2}G[0:inf](F[0.5:1.5]{x_1} -> F[1:3]{x_2})`

Use the following supported operators:

Trace quantifiers: `forall{n}` or `exists{n}`, with ascending trace variable numbers `n`

Temporal operators: `eventually[a:b] , F[a:b] , once[a:b] , P[a:b] , always[a:b] , G[a:b] , historically[a:b] , H[a:b] , since[a:b] , S[a:b]`

Logic operators: `not , ! , and , && , or , || , implies, -> `

Atomic propositions: `{p_n}`, `n` must be a valid trace variable number

## Trace Format

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

## Acknowledgements

This implementation was built in the process of my thesis *Monitoring Real-Time Hyperproperties*.

Reelay was created by Dogan Ulus ([Online monitoring of metric temporal logic using sequential networks](https://arxiv.org/abs/1901.00175)).
