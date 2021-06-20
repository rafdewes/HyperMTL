# Rafael Dewes 2021

# function discretize_MTL on formula
# takes inner formula, sampling period
# approximate intervals

# discretize traces by sampling
# take trace, sampling period
# sample and hold

import hypermtl
import math


# from trace (list of dicts)
# sample and hold by s
# return sampled trace
def sample_trace(trace, s):

    # take every timestamp, divide by s, then round up to integer
    for x in trace:
        x["time"] = math.ceil(x["time"]/s)

    # afterwards fuse all entries with equal timestamps
    i = 0
    for y in trace:
        i = trace.index(y,i)
        try:
            if (y["time"] == (trace[i+1])["time"]):
                y.update(trace.pop(i+1))
        except IndexError:
            pass
    
    return trace
    
    
# take formula (syntax tree)
# iterate over all branches
# discretize all interval bounds
# return modified formula
def discretize_MTL(node, s):

    if s == 0:
        return node

    t = node.token

    if t == 'AP':
        return node
    elif t in ['PAREN','NOT','not','!']:
        node.right = discretize_MTL(node.right, s)
    elif t in ['EQUIV','equal','<->','IMPLIES','implies','->','OR','or','||','AND','and','&&']:
        node.left = discretize_MTL(node.left, s)
        node.right = discretize_MTL(node.right, s)
    elif t in ['G','GLOBALLY','globally','HISTORICALLY','historically','H','ONCE','once','P','F','FINALLY','finally']:
        node.timeL = discretize_time(node.timeL, s)
        node.timeR = discretize_time(node.timeR, s)
        node.right = discretize_MTL(node.right, s)
    elif t in ['U','UNTIL','until','SINCE','since','S']:
        node.timeL = discretize_time(node.timeL, s)
        node.timeR = discretize_time(node.timeR, s)
        node.left = discretize_MTL(node.left, s)
        node.right = discretize_MTL(node.right, s)
    else:
        # raise Exception('Invalid pastMTL formula!')
        print('Invalid MTL formula! Found %s' % (t))
        node.right = discretize_MTL(node.right, s)

    return node

def discretize_time(time, s):
    if time == "inf":
        return time 
    return str(int(float(time) // s))

