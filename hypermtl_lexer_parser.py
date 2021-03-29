# Rafael Dewes  2021
# HyperMTL lexer + parser

# Example input logic formula in string form
# "forall{1} forall{2} G[0:inf] ( H[0:5] {a_1} and not {b_1} ) -> {c_2} ) "

from sly import Lexer, Parser
from hypermtl import *
import re

# Lexer for HyperMTL formulae 

class HyMtlLexer(Lexer):
    tokens = { AP, TRACE, EXISTS, FORALL, TRACEVAR, UNTIL, FINALLY, GLOBALLY, SINCE, ONCE, HISTORICALLY, INTERVAL, AND, OR, IMPLIES, EQUIV, NOT, LPAREN, RPAREN }
    ignore = ' \t'

    # Tokens
    AP = r'\{[a-zA-Z_]+\d+\}'
    TRACE = r'\d+'
    TRACEVAR = r'\{\d+\}'
    INTERVAL = r'\[\d+:(\d+|inf)\]'

    # Operators
    EXISTS = r'exists|E'
    FORALL = r'forall|A'
    UNTIL = r'until|U'
    FINALLY = r'finally|eventually|F'
    GLOBALLY = r'globally|always|G'
    SINCE = r'since|S'
    ONCE = r'once|P'
    HISTORICALLY = r'historically|H'
    AND = r'and|&&'
    OR = r'or|\|\|'
    IMPLIES = r'implies|->'
    EQUIV = r'equal|<->'
    NOT = r'not|!'
    LPAREN = r'\('
    RPAREN = r'\)'

    # Ignore Newline
    ignore_newline = r'\n+'

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


# Supplementary functions for Parser

def interval_to_limits(intervalstring):
    limits = [0,0]
    limits = (re.sub(r'\[|\]', '', intervalstring)).split(':')
    return limits

def ap_to_trace(apstring):
    lst = re.findall(r'\d+', apstring)
    return lst[0]


# Parser 

class HyMtlParser(Parser):

    tokens = HyMtlLexer.tokens

    precedence = (
        ('right', FORALL, EXISTS),
        ('right', IMPLIES, EQUIV),
        ('left', AND, OR),
        ('left', UNTIL, SINCE),
        ('right', NOT, GLOBALLY, FINALLY, HISTORICALLY, ONCE),
        ('left', INTERVAL, TRACEVAR, TRACE),
    )

    @_('FORALL TRACEVAR expr',
    'EXISTS TRACEVAR expr')
    def expr(self, p):
        return Quant(p[0],p[1],p.expr)

    @_('FINALLY INTERVAL expr',
       'GLOBALLY INTERVAL expr',
       'ONCE INTERVAL expr',
       'HISTORICALLY INTERVAL expr')
    def expr(self, p):
        l, r = interval_to_limits(p[1])
        return UnTempOp(p[0], l, r, p.expr)

    @_('expr UNTIL INTERVAL expr', 'expr SINCE INTERVAL expr')
    def expr(self, p):
        l, r = interval_to_limits(p[2])
        return BinTempOp(p.expr0, p[1], l, r, p.expr1)

    @_('NOT expr')
    def expr(self, p):
        return UnOp(p[0], p.expr)

    @_('expr AND expr', 'expr OR expr', 
       'expr IMPLIES expr', 'expr EQUIV expr')
    def expr(self, p):
        return BinOp(p.expr0, p[1], p.expr1)

    @_('AP')
    def expr(self, p):
        tr = ap_to_trace(p[0])
        return AP(p[0], tr)

    @_('AP TRACE')
    def expr(self, p):
        return AP(p[0], p[1])
    
    @_('LPAREN expr RPAREN')
    def expr(self,p):
        return UnOp('PAREN', p.expr)


# Unparser - build string from past MTL syntax tree


def unparse(mtlTree):
    t = mtlTree.token
    print(t)
    if t == 'PAREN':
        return '('+unparse(mtlTree.right)+')'
    elif t == 'NOT':
        return 'not '+unparse(mtlTree.right)
    elif t == 'EQUIV':
        return unparse(mtlTree.left)+'<-> '+unparse(mtlTree.right)
    elif t == 'IMPLIES':
        return unparse(mtlTree.left)+'-> '+unparse(mtlTree.right)
    elif t == 'OR':
        return unparse(mtlTree.left)+'or '+unparse(mtlTree.right)
    elif t == 'AND':
        return unparse(mtlTree.left)+'and '+unparse(mtlTree.right)
    elif t == 'HISTORICALLY':
        return write_historically(mtlTree)+unparse(mtlTree.right)
    elif t == 'ONCE':
        return write_once(mtlTree)+unparse(mtlTree.right)
    elif t == 'SINCE':
        return unparse(mtlTree.left)+write_since(mtlTree)+unparse(mtlTree.right)
    elif t == 'AP':
        return write_ap(mtlTree)
    else:
        # raise Exception('Invalid pastMTL formula!')
        print('Invalid pastMTL formula!')
        return unparse(mtlTree.right)

def write_historically(node):
    return 'H['+node.timeL+':'+node.timeR+']'

def write_once(node):
    return 'P['+node.timeL+':'+node.timeR+']'

def write_since(node):
    return 'S['+node.timeL+':'+node.timeR+']'
    
def write_ap(node):
    return node.name





