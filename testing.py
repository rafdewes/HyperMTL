from hypermtl_lexer_parser import *


text1 = "forall{1}forall{2}G[0:inf]((H[0:5]{a_1} and not {b_1}) -> {c_2})"
text2 = "H[0:5]{a_1}"

lexer = HyMtlLexer()
parser = HyMtlParser()

tokenlist = []


tokenlist = lexer.tokenize(text1)

#for tok in tokenlist:
#    print('token=%r, value=%r' % (tok.type, tok.value))

result = parser.parse(tokenlist)

text_new = unparse(result)

print(text_new)
