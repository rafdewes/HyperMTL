# Rafael Dewes  2021
# Auxiliary Tree Structure and functions for HyperMTL expressions


class Expr:
    pass

class Quant(Expr):
    def __init__(self, op, var, right):
        self.token = self.op = op
        self.trace = self.var = var
        self.right = right

class UnOp(Expr):
    def __init__(self, op, right):
        self.token = self.op = op
        self.right = right

class BinOp(Expr):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class UnTempOp(Expr):
    def __init__(self, op, timeL, timeR, right):
        self.token = self.op = op
        self.timeL = timeL
        self.timeR = timeR
        self.right = right

class BinTempOp(Expr):
    def __init__(self, left, op, timeL, timeR, right):
        self.token = self.op = op
        self.timeL = timeL
        self.timeR = timeR
        self.left = left
        self.right = right

class AP(Expr):
    def __init__(self, name, trace):
        self.token = 'AP'
        self.name = name
        self.trace = trace


def get_children(node):
    return 0