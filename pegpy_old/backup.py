import sys

node_Num = ['#Int']
node_Word = ['#Word']
node_PrimaryExpr = node_Num + node_Word
node_Index = node_Num
node_ArrayRef = node_Word + ['#Index']
node_StructComponent = ['#ArrayRef'] + node_Word
node_StructRef = node_StructComponent
node_MapRef = node_Word
node_PostfixExpr = ['#Map00'] + ['#StructRef'] + node_PrimaryExpr
node_MulDivExpr = node_PostfixExpr + ['#MUL', '#DIV']
node_AddSubExpr = ['#MulDiv'] + ['#ADD', '#SUB']
node_RelationalExpr = ['#AddSub'] + ['#GT', '#LT', '#GTE', '#LTE']
node_EqualityExpr = ['#Relational'] + ['#EQ', '#NEQ']
node_LogicalExpr = ['#Equality'] + ['#AND', '#OR']
node_FParam = ['#']
node_FunctionCall = ['#FParam', '#Adv', '#FName']
node_Expression = ['#Logical'] + ['#FCall']
node_Assign = node_PostfixExpr + node_Expression
node_Input = ['#Assign'] + node_Expression
node_Source = ['#Input']

class AST:
    __slots__ = ['string','pos','output','indentLevel']
    def __init__(self, ast_str):
        self.string = ast_str
        self.pos = 0
        self.output = ""
        self.indentLevel = 0

def transpile(param_ast):
    ast = AST(param_ast)
    if(Source(ast)==False):sys.exit()
    return ast.output

def Source(ast):
    tag = get_tag(ast)
    ast.output+='contract Sample {\n'
    incIndent(ast)
    if tag in node_Source:
        tag_exe(tag,ast)
    ast.output+='}\n'
    return True

def Input(ast):
    while(True):
        tag = get_tag(ast)
        makeIndent(ast)
        if tag in node_Input:
            tag_exe(tag,ast)
            ast.output+='\n'
        if ast.string[ast.pos] == ']':break
        ast.pos+=1
    return True

def Assign(ast):
    tag = get_tag(ast)
    if tag in node_PostfixExpr:
        tag_exe(tag,ast)
    ast.output+=' = '
    ast.pos+=1
    tag = get_tag(ast)
    if tag in node_Expression:
        tag_exe(tag,ast)
    return True

def AddSub(ast):
    while(True):
        tag = get_tag(ast)
        if tag in node_AddSubExpr:
            tag_exe(tag,ast)
        if ast.string[ast.pos]==']':break
        ast.pos+=1
    return True

def MulDiv(ast):
    while(True):
        tag = get_tag(ast)
        if tag in node_MulDivExpr:
            tag_exe(tag,ast)
        if ast.string[ast.pos] == ']':break
        ast.pos+=1
    return True

def ADD(ast):
    ast.pos+=3
    ast.output+='+'

def SUB(ast):
    ast.pos+=3
    ast.output+='-'

def MUL(ast):
    ast.pos+=3
    ast.output+='*'

def DIV(ast):
    ast.pos+=3
    ast.output+='/'

def Map00(ast):
    tag = get_tag(ast)
    if tag in node_Word:
        ast.output+='map00['
        tag_exe(tag,ast)
        ast.output+=']'
    return True

def StructRef(ast):
    while(True):
        tag = get_tag(ast)
        if tag in node_StructComponent:
            tag_exe(tag,ast)
        if ast.string[ast.pos] == ']':break
        ast.pos+=1
        ast.output+='.'
    return True

def ArrayRef(ast):
    tag = get_tag(ast)
    if tag in node_Word:
        tag_exe(tag,ast)
    while(True):
        if ast.string[ast.pos] == ']':break
        ast.output+='['
        ast.pos+=1
        tag = get_tag(ast)
        if tag in ['#Index']:
            tag_exe(tag,ast)
        ast.output+=']'
    return True

def Index(ast):
    tag = get_tag(ast)
    if tag in node_Num:
        tag_exe(tag, ast)
    return True


def Int(ast):
    require(ast, '\'')
    ast.pos+=1
    while(ast.string[ast.pos] != '\''):
        ast.output += ast.string[ast.pos]
        ast.pos+=1
    ast.pos+=1
    return True

def Word(ast):
    require(ast, '\'')
    ast.pos+=1
    while(ast.string[ast.pos] != '\''):
        ast.output += ast.string[ast.pos]
        ast.pos+=1
    ast.pos+=1
    return True


def get_tag(ast):
    tag = ""
    require(ast,'[')
    ast.pos+=1
    while(ast.string[ast.pos] != ' '):
        tag += ast.string[ast.pos]
        ast.pos+=1
    ast.pos+=1
    return tag

def tag_exe(tag,ast):
    globals()[tag[1:]](ast)
    require(ast, ']')
    ast.pos+=1

def require(ast,ch):
    if ast.string[ast.pos] != ch:
        sys.exit()

def incIndent(ast):
    ast.indentLevel+=1
def decIndent(ast):
    ast.indentLevel-=1
def makeIndent(ast):
    ast.output+=('    ' * ast.indentLevel)




#---------------------------------------------------
s1 = "[#AddSub [#MulDiv [#Int '12']] [#SUB '+'] [#MulDiv [#Int '34']] [#ADD '+'] [#MulDiv [#Word '残高']]]"
s2 = "[#Int '123']"
s3 = "[#AddSub [#MulDiv [#Word 'hello']]]"
s4 = "[#AddSub [#MulDiv [#Int '12']]]"
s5 = "[#Input [#AddSub [#MulDiv [#Map00 [#Word 'msg.sender']]]]]"
s6 = "[#Input [#Assign [#StructRef [#Word 'w']] [#AddSub [#MulDiv [#Int '2']] [#ADD '+'] [#MulDiv [#Int '3']]]]]"
s7 = "[#Input [#AddSub [#MulDiv [#StructRef [#Word 'w'] [#Word 'e']]]]]"
s8 = "[#Input [#AddSub [#MulDiv [#StructRef [#ArrayRef [#Word 'w'] [#Index [#Int '2']]]]]]]"
s9 = "[#Input [#Assign [#StructRef [#Word 'w']] [#AddSub [#MulDiv [#Int '12']]]] [#Assign [#StructRef [#Word 'message']] [#AddSub [#MulDiv [#StructRef [#Word 'hello']]]]]]"
#---------------------------------------------------
print(transpile(s9))

"""
Input = $({AddSubExpr #AddSub})
AddSubExpr = {$MulDivExpr ($({'+' #ADD}/{'-' #SUB}) $MulDivExpr)* #AddSub}
MulDivExpr = {$PrimaryExpr ($({'*' #MUL}/{'/' #DIV}) $PrimaryExpr)* #MulDiv}
PrimaryExpr = Num / Word
Num = {[0-9]+ #Int}
Word = '[' {Identifier #Word} ']'
Identifier = (!'[' !']' .)+
"""