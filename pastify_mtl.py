# Rafael Dewes  2021
# Pastify MTL

from hypermtl import *


def get_inner_formula(mtlTree):

    t = mtlTree.token
    print(t)

    if t in ['FORALL','forall','A','EXISTS','exists','E']:
        return get_inner_formula(mtlTree.right)
    elif t in ['G','F','globally','finally']:
            return mtlTree.right
    else:
        return mtlTree


def get_temporal_depth(node):

    t = node.token
    print(t)

    if t in ['G','F','globally','finally']:
        return int(node.timeR)+get_temporal_depth(node.right)
    elif t in ['U','until']:
        return int(node.timeR)+max(get_temporal_depth(node.left), get_temporal_depth(node.right))
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

    return pastify(root, root, d)
    
#TODO
def pastify(current, root, delay):

    t = current.token
    print(t)

    if t == 'AP':
        return root
    elif t == 'PAREN':
        return pastify(current.right, root, delay)
    elif t in ['NOT','not','!']:
        return pastify(current.right, root, delay)
    elif t in ['EQUIV','equal','<->','IMPLIES','implies','->','OR','or','||','AND','and','&&']
        return pastify(current.right, root, delay)
    else:
        # raise Exception('Invalid pastMTL formula!')
        print('Invalid MTL formula! Found %s' % (current.token))
        return pastify(current.right)
