from hypermtl_lexer_parser import *
from processing_hymtl import *


text1 = "forall{1}forall{2}G[0:inf]((G[0:5]{a_1} and not {b_1}) -> {c_2})"
text2 = "H[0:5]{a_1}"
text3 = "F[0:inf]((G[0:1]{a_1} or G[0:2]{b_1})U[0:1](F[2:3]{c_1}))"

lexer = HyMtlLexer()
parser = HyMtlParser()

tokenlist = []


tokenlist = lexer.tokenize(text1)

#for tok in tokenlist:
#    print('token=%r, value=%r' % (tok.type, tok.value))

result = parser.parse(tokenlist)

inner = get_inner_formula(result)

text_new = unparse(result)

delay = get_temporal_depth(inner)

print(delay)
pastified = pastify_mtl(result)

text_p = unparse(pastified)

print(text_new)
print(text_p)
