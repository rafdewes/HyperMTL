# Rafael Dewes 2021

# function discretize_MTL on formula
# takes inner formula, sampling period
# approximate intervals

# discretize traces by sampling
# take trace, sampling period
# sample and hold

import hypermtl

class TraceSampler:
    def __init__(self, sampling_period):
        self.s = sampling_period
        
    # from trace (list of dicts)
    # build new trace (list of dicts)
    def sample_trace(self, trace):
        # take every timestamp, round up to multiple of self.s, then divide by self.s
        # afterwards fuse all entries with equal timestamps
        
        return trace




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
    return (int(time) // s)

