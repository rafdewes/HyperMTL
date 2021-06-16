# Rafael Dewes  2021
# Process HyMTL

import hypermtl

# return list of quantifiers
def get_trace_quantifiers(mtlTree, quantifiers):

    t = mtlTree.token

    if t in ['FORALL','forall','A']:
        return get_trace_quantifiers(mtlTree.right, quantifiers+'A')
    elif t in ['EXISTS','exists','E']:
        return get_trace_quantifiers(mtlTree.right, quantifiers+'E')
    else:
        return quantifiers


# return top level future operator
def get_unbounded_operator(mtlTree):

    t = mtlTree.token

    if t in ['FORALL','forall','A','EXISTS','exists','E']:
        return get_inner_formula(mtlTree.right)
    elif t in ['G','globally']:
        return 'G'
    elif t in ['F','finally']:
        return 'F'
    else:
        return '0'


# isolate inner 'MTL' spec
def get_inner_formula(mtlTree):

    t = mtlTree.token

    if t in ['FORALL','forall','A','EXISTS','exists','E']:
        return get_inner_formula(mtlTree.right)
    elif t in ['G','F','globally','finally']:
        return mtlTree.right
    else:
        return mtlTree

# find the upper bound on 'temporal depth'
def get_temporal_depth(node):

    t = node.token

    if t in ['G','F','globally','finally']:
        try:
            return int(node.timeR)+get_temporal_depth(node.right)
        except(ValueError):
            print('Not a valid formula! Unbounded interval in %s' % (t))
    elif t in ['U','until']:
        try:
            return int(node.timeR)+max(get_temporal_depth(node.left), get_temporal_depth(node.right))
        except(ValueError):
            print('Not a valid formula! Unbounded interval in %s' % (t))   
    elif t == 'PAREN':
        return get_temporal_depth(node.right)
    elif t in ['NOT','not','!']:
        return get_temporal_depth(node.right)
    elif t in ['EQUIV','equal','<->']:
        return max(get_temporal_depth(node.left), get_temporal_depth(node.right))
    elif t in ['IMPLIES','implies','->']:
        return max(get_temporal_depth(node.left), get_temporal_depth(node.right))
    elif t in ['OR','or','||']:
        return max(get_temporal_depth(node.left), get_temporal_depth(node.right))
    elif t in ['AND','and','&&']:
        return max(get_temporal_depth(node.left), get_temporal_depth(node.right))
    elif t in ['HISTORICALLY','historically','H']:
        return get_temporal_depth(node.right)
    elif t in ['ONCE','once','P']:
        return get_temporal_depth(node.right)
    elif t in ['SINCE','since','S']:
        return max(get_temporal_depth(node.left), get_temporal_depth(node.right))
    elif t == 'AP':
        return 0
    else:
        # raise Exception('Invalid pastMTL formula!')
        print('Invalid pastMTL formula! Found %s.' % (t))
        return get_temporal_depth(node.right)




# read MTL formula 
# find max delay
# recursively rewrite to past MTL

def pastify_mtl(mtlTree):

    root = get_inner_formula(mtlTree)

    d = get_temporal_depth(root)

    return pastify(root, d)
    

def pastify(node, delay):

    if delay == 0:
        return node

    t = node.token

    if t == 'AP':
        return check_delay_ap(node, delay)    
    elif t in ['PAREN','NOT','not','!','HISTORICALLY','historically','H','ONCE','once','P']:
        node.right = check_delay_ap(node.right, delay)
    elif t in ['EQUIV','equal','<->','IMPLIES','implies','->','OR','or','||','AND','and','&&','SINCE','since','S']:
        node.left = check_delay_ap(node.left, delay)
        node.right = check_delay_ap(node.right, delay)
    elif t in ['G','GLOBALLY','globally']:
        node.token = 'H'
        delay = future_to_past(node, delay)
        node.right = check_delay_ap(node.right, delay)
    elif t in ['F','FINALLY','finally']:
        node.token = 'P'
        delay = future_to_past(node, delay)
        node.right = check_delay_ap(node.right, delay)
    elif t in ['U','UNTIL','until']:
        #TODO Translating Until requires auxiliary Operator 'Precedes'
        # this will give wrong results
        node.token = 'S'
        delay = future_to_past(node, delay)
        node.left = check_delay_ap(node.left, delay)
        node.right = check_delay_ap(node.right, delay)
    else:
        # raise Exception('Invalid pastMTL formula!')
        print('Invalid MTL formula! Found %s' % (t))
        node.right = check_delay_ap(node, delay)

    return node


def future_to_past(node, delay):
    delay = delay - int(node.timeR)
    node.timeR = int(node.timeR) - int(node.timeL)
    node.timeL = '0'
    return delay

def check_delay_ap(childnode, delay):
    if (childnode.token == 'AP') and delay > 0:
        return UnOp('PAREN', UnTempOp('P', delay, delay, childnode))
    else:
        pastify(childnode, delay)
        return childnode


