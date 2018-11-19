import sys

class AST:
    __slots__ = ['string','pos','output','indentLevel','temp','write_to_temp','funcInfo']
    def __init__(self, ast_str):
        self.string = ast_str
        self.pos = 0
        self.output = ""
        self.indentLevel = 0
        self.temp = ""
        self.write_to_temp = False
        self.funcInfo = {'view':'public ', 'mutability':'', 'returns':''}
    def temp_reset(self):
        self.temp = ""
    def funcInfo_reset(self):
        self.funcInfo = {'view':'public ', 'mutability':'', 'returns':''}

class WD:
    __slots__ = []


def err(ast):
    ast.output = '{AST_ERROR'
    ast.pos = len(ast.string) - 1

def transpile(tree,filePath):
    ast = AST(tree)
    tag = get_tag(ast)
    fileName = filePath[(filePath.rfind('/')+1):(filePath.rfind('.'))]
    ast.output+='contract '+fileName+' {\n'
    incIndent(ast)
    tag_exe(tag,ast)
    decIndent(ast)
    ast.output+='}'
    return ast.output

def Input(ast):
    while(True):
        tag = get_tag(ast)
        makeIndent(ast)
        tag_exe(tag,ast)
        ast.output+='\n'
        if current_pos(ast) == ']':break
        ast.pos+=1
    return True

def Test(ast):
    ast.output = '{AST_TEST'
    ast.pos = len(ast.string) - 1

#------------------------VarDecl--------------------------
def VDecl(ast):
    tag = get_tag(ast)
    tag_exe(tag,ast)

#------------------------FuncDecl--------------------------
def FDecl(ast):
    fparams = []
    advs = ""
    fname = ""
    ast.write_to_temp = True
    tag = get_tag(ast)
    if tag == '#FDParam':
        tag_exe(tag,ast)#FDParam
        fparams.append(ast.temp)
        ast.temp_reset()
        ast.pos+=1
        tag = get_tag(ast)
    while(tag in ['#FDParam', '#Adv']):
        tag_exe(tag,ast)#Adv
        advs+=ast.temp
        ast.temp_reset()
        ast.pos+=1
        tag = get_tag(ast)
        tag_exe(tag,ast)#FDParam
        fparams.append(ast.temp)
        ast.temp_reset()
        ast.pos+=1
        tag = get_tag(ast)
    ast.write_to_temp = False
    ast.output+='function '
    ast.output+=advs
    tag_exe(tag,ast)#FDName
    ast.output+='('
    for fp in fparams:
        ast.output+=(typeDetect(fp,0) + ' ' + fp + ',')
    if len(fparams) > 0:
        ast.output = ast.output.rstrip(',')
    ast.output+=') <pA><pB><pC>{'
    if current_pos(ast) == ' ':
        ast.pos+=1
        ast.output+='\n'
        incIndent(ast)
        tag = get_tag(ast)
        tag_exe(tag,ast)#FBody
        decIndent(ast)
        makeIndent(ast)
    ast.output+='}'
    setFuncMod(ast)
    ast.funcInfo_reset()

def withType(word):
    return wd[word][1] + ' ' + word

def setFuncMod(ast):
    a = ast.funcInfo['view']
    b = ast.funcInfo['mutability']
    c = ast.funcInfo['returns']
    ast.output = ast.output.replace('<pA>',a).replace('<pB>',b).replace('<pC>',c)

def FDBody(ast):
    semi_colon_cancel = False
    while(True):
        tag = get_tag(ast)
        if tag == '#If':
            semi_colon_cancel = True
        makeIndent(ast)
        tag_exe(tag,ast)
        if semi_colon_cancel:
            ast.output+='\n'
        else:
            ast.output+=';\n'
        if current_pos(ast) == ']':break
        ast.pos+=1

def FDParam(ast):
    tag = get_tag(ast)
    tag_exe(tag,ast)

def FDName(ast):
    require(ast, '\'')
    ast.pos+=1
    while(current_pos(ast) != '\''):
        ast.output+=current_pos(ast)
        ast.pos+=1
    ast.pos+=1

#------------------------Statement--------------------------
def Return(ast):
    ast.write_to_temp = True
    ast.output+='return ('
    ast.funcInfo['returns']+='returns('
    while(True):
        tag = get_tag(ast)
        tag_exe(tag,ast)
        ast.output+=ast.temp
        ast.funcInfo['returns']+=typeDetect(ast.temp,0)
        ast.temp_reset()
        if current_pos(ast) == ']':break
        ast.pos+=1
        ast.funcInfo['returns']+=(', ')
        ast.output+=', '
    ast.funcInfo['returns']+=')'
    ast.output+=')'
    ast.write_to_temp = False

def typeDetect(s,count):
    #s = 'owner'
    #s = 'map02[hogege]'
    #s = 'numbers[index][i2][i3]'
    #s = 'data.param'
    if s in wd:
        return wd[s][count+1]
    elif s.rfind('.') > 0:
        return typeDetect(s[s.rfind('.')+1:],0)
    elif s.rfind('['):
        return typeDetect(s[:s.rfind('[')],count+1)
    else:
        sys.exit()

def Require(ast):
    while(True):
        ast.output+='require('
        tag = get_tag(ast)
        tag_exe(tag,ast)
        ast.output+=')'
        if current_pos(ast) == ']':break
    return True

def Event(ast):
    ast.output+='emit '
    tag = get_tag(ast)
    tag_exe(tag,ast)
    ast.output+='('
    while(True):
        if current_pos(ast) == ']':break
        ast.pos+=1
        tag = get_tag(ast)
        tag_exe(tag,ast)
        ast.output+=', '
    ast.output+=')'
    return True

def If(ast):
    ast.output+='if('
    #Condition
    tag = get_tag(ast)
    tag_exe(tag,ast)
    ast.output+='){\n'
    ast.pos+=1
    #Then
    incIndent(ast)
    tag = get_tag(ast)
    tag_exe(tag,ast)
    decIndent(ast)
    makeIndent(ast)
    ast.output+='}'
    ast.pos+=1
    #ElIf or Else
    tag = get_tag(ast)
    tag_exe(tag,ast)
    if current_pos(ast) == ']':return True
    ast.pos+=1
    #Else
    tag = get_tag(ast)
    tag_exe(tag,ast)
    return True

def Cond(ast):
    tag = get_tag(ast)
    tag_exe(tag,ast)

def Then(ast):
    while(True):
        makeIndent(ast)
        tag = get_tag(ast)
        tag_exe(tag,ast)
        ast.output+=';\n'
        if current_pos(ast) == ']':break
        ast.pos+=1
    return True

def ElIf(ast):
    ast.output+=' else if('
    #Condition
    tag = get_tag(ast)
    tag_exe(tag,ast)
    ast.output+='){\n'
    ast.pos+=1
    #Then
    incIndent(ast)
    tag = get_tag(ast)
    tag_exe(tag,ast)
    decIndent(ast)
    makeIndent(ast)
    ast.output+='}'

def Else(ast):
    ast.output+=' else {\n'
    incIndent(ast)
    while(True):
        makeIndent(ast)
        tag = get_tag(ast)
        tag_exe(tag,ast)
        ast.output+=';\n'
        if current_pos(ast) == ']':break
        ast.pos+=1
    decIndent(ast)
    makeIndent(ast)
    ast.output+='}'
    return True

def Assign(ast):
    tag = get_tag(ast)
    tag_exe(tag,ast)
    ast.output+=' = '
    ast.pos+=1
    tag = get_tag(ast)
    tag_exe(tag,ast)
    return True

def LocalVDecl(ast):
    tag = get_tag(ast)
    ast.output+='<LEFT>'
    if tag == '#Logical':
        ast.output+=' = '
        tag_exe(tag,ast)
        ast.pos+=1
        tag = get_tag(ast)
    ast.write_to_temp = True
    tag_exe(tag,ast)
    left = (typeDetect(ast.temp,0)+' '+ast.temp)
    ast.write_to_temp = False
    ast.temp_reset()
    ast.output = ast.output.replace('<LEFT>',left)


#------------------------Expression--------------------------
def FExpr(ast):
    fparams = []
    advs = ""
    fname = ""
    ast.write_to_temp = True
    tag = get_tag(ast)
    if tag == '#FEParam':
        tag_exe(tag,ast)#FParam
        fparams.append(ast.temp)
        ast.temp_reset()
        ast.pos+=1
        tag = get_tag(ast)
    while(tag in ['#Adv','#FEParam']):
        tag_exe(tag,ast)#Adv
        advs+=ast.temp
        ast.temp_reset()
        ast.pos+=1
        tag = get_tag(ast)
        tag_exe(tag,ast)#FParam
        fparams.append(ast.temp)
        ast.temp_reset()
        ast.pos+=1
        tag = get_tag(ast)
    ast.write_to_temp = False
    ast.output+=advs
    tag_exe(tag,ast)#FName
    ast.output+='('
    for fp in fparams:
        ast.output+=(fp+',')
    if len(fparams) > 0:
        ast.output = ast.output.rstrip(',')
    ast.output+=')'

def Adv(ast):
    require(ast, '\'')
    ast.pos+=1
    while(current_pos(ast) != '\''):
        if ast.write_to_temp:ast.temp+=current_pos(ast)
        else:ast.output+=current_pos(ast)
        ast.pos+=1
    ast.pos+=1

def FEParam(ast):
    tag = get_tag(ast)
    tag_exe(tag,ast)

def FEName(ast):
    require(ast, '\'')
    ast.pos+=1
    while(current_pos(ast) != '\''):
        ast.output+=current_pos(ast)
        ast.pos+=1
    ast.pos+=1

def Logical(ast):
    while(True):
        tag = get_tag(ast)
        tag_exe(tag,ast)
        if current_pos(ast)==']':break
        ast.pos+=1
    return True

def Equality(ast):
    while(True):
        tag = get_tag(ast)
        tag_exe(tag,ast)
        if current_pos(ast)==']':break
        ast.pos+=1
    return True

def Relational(ast):
    while(True):
        tag = get_tag(ast)
        tag_exe(tag,ast)
        if current_pos(ast)==']':break
        ast.pos+=1
    return True

def AddSub(ast):
    while(True):
        tag = get_tag(ast)
        tag_exe(tag,ast)
        if current_pos(ast)==']':break
        ast.pos+=1
    return True

def MulDiv(ast):
    while(True):
        tag = get_tag(ast)
        tag_exe(tag,ast)
        if current_pos(ast) == ']':break
        ast.pos+=1
    return True

def AND(ast):
    ast.pos+=5
    ast.output+=' && '

def OR(ast):
    ast.pos+=4
    ast.output+=' || '

def EQ(ast):
    ast.pos+=4
    ast.output+=' == '

def NEQ(ast):
    ast.pos+=6
    ast.output+=' != '

def GT(ast):
    ast.pos+=3
    ast.output+=' > '

def GTE(ast):
    ast.pos+=4
    ast.output+=' >= '

def LT(ast):
    ast.pos+=3
    ast.output+=' < '

def LTE(ast):
    ast.pos+=4
    ast.output+=' <= '

def ADD(ast):
    ast.pos+=3
    ast.output+=' + '

def SUB(ast):
    ast.pos+=3
    ast.output+=' - '

def MUL(ast):
    ast.pos+=3
    ast.output+=' * '

def DIV(ast):
    ast.pos+=3
    ast.output+=' / '

def Map(ast, tag):
    if ast.write_to_temp:ast.temp+=('map'+tag[3:])
    else:ast.output+=('map'+tag[3:])
    while(True):
        if ast.write_to_temp:ast.temp+='['
        else:ast.output+='['
        tag = get_tag(ast)
        tag_exe(tag,ast)
        if ast.write_to_temp:ast.temp+=']'
        else:ast.output+=']'
        if current_pos(ast) == ']':break
    return True

def StructRef(ast):
    while(True):
        tag = get_tag(ast)
        tag_exe(tag,ast)
        if current_pos(ast) == ']':break
        ast.pos+=1
        if ast.write_to_temp:ast.temp+='.'
        else:ast.output+='.'
    return True

def ArrayRef(ast):
    tag = get_tag(ast)
    tag_exe(tag,ast)
    while(True):
        if current_pos(ast) == ']':break
        if ast.write_to_temp:ast.temp+='['
        else:ast.output+='['
        ast.pos+=1
        tag = get_tag(ast)
        tag_exe(tag,ast)
        if ast.write_to_temp:ast.temp+=']'
        else:ast.output+=']'
    return True

def Index(ast):
    tag = get_tag(ast)
    tag_exe(tag, ast)
    return True

def Int(ast):
    require(ast, '\'')
    ast.pos+=1
    if ast.write_to_temp:
        while(current_pos(ast) != '\''):
            ast.temp += current_pos(ast)
            ast.pos+=1
    else:
        while(current_pos(ast) != '\''):
            ast.output += current_pos(ast)
            ast.pos+=1
    ast.pos+=1

def Word(ast):
    require(ast, '\'')
    ast.pos+=1
    w = ""
    while(current_pos(ast) != '\''):
        w += current_pos(ast)
        ast.pos+=1
    if ast.write_to_temp:
        ast.temp += w
    else:
        ast.output += w
    ast.pos+=1

#------------------------Word Dictionary--------------------------
wd = {
    'name':('006e0061006d0065', 'string'),
    '名前':('540d524d', 'string'),
    '実行者':('実行者', 'address'),
    '対象者':('対象者', 'address'),
    '送金額':('送金額', 'int'),
    '総発行量':('総発行量', 'int'),
    '創設者':('創設者', 'address'),
    '指定量':('指定量', 'int'),
    '操作実行者':('操作実行者', 'address'),
    '〜の残高':('〜の残高', 'mapping(address=>int)', 'int'),
    'map02':('map02', 'mapping(address=>int)', 'int')
}

#------------------------Utilities--------------------------
def get_tag(ast):
    tag = ""
    require(ast,'[')
    ast.pos+=1
    while(current_pos(ast) != ' '):
        tag += current_pos(ast)
        ast.pos+=1
    ast.pos+=1
    return tag

def tag_exe(tag,ast):
    if tag[1:].startswith('Map'):
        Map(ast, tag[1:])
    else:
        globals()[tag[1:]](ast)
    require(ast, ']')
    ast.pos+=1

def require(ast,ch):
    if current_pos(ast) != ch:
        sys.exit()

def current_pos(ast):
    return ast.string[ast.pos]

def incIndent(ast):
    ast.indentLevel+=1
def decIndent(ast):
    ast.indentLevel-=1
def makeIndent(ast):
    ast.output+=('    ' * ast.indentLevel)

def viewAST(ast):
    sss = ""
    tab = 0
    for c in ast:
        if c=='[':
            sss+='\n'
            sss+=('    '*tab)
            tab+=1
            sss+=c
        elif c==']':
            tab-=1
            sss+='\n'
            sss+=('    '*tab)
            sss+=c
        else:
            sss+=c
    return sss[1:]

def charToByte(c):
    return format(ord(c), '04x')
def strToByte(s):
    hex_str = ""
    for c in s:
        hex_str+=charToByte(c)
    return hex_str


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
s10 = "[#Input [#Assign [#StructRef [#Word 'w']] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#ArrayRef [#Word 'r'] [#Index [#Int '2']]]]]]]]]]]"
s11 = "[#Input [#Assign [#StructRef [#Word 'requirement']] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word 'balance']]]] [#GTE '>='] [#AddSub [#MulDiv [#Int '100']]]]] [#AND 'AND'] [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word 'target']]]]] [#NEQ 'NOT='] [#Relational [#AddSub [#MulDiv [#StructRef [#Word 'caller']]]]]]]]]"
s12 = "[#Input [#If [#Cond [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '1']]]]]]] [#Then [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '2']]]]]]] [#ElIf [#Cond [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '3']]]]]]] [#Then [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '4']]]]]]]] [#Else [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '5']]]]]]]]]"
s13 = "[#Input [#If [#Cond [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '1']]]]]]] [#Then [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '2']]]]]]] [#Else [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '3']]]]]]]]]"
s14 = "[#Input [#FCall [#FParam [#StructRef [#Word 'money']]] [#FName 'wosend']]]"
s15 = "[#Input [#FDecl [#FDParam [#Word 'w']] [#FDName 'woSend'] [#FBody [#Assign [#StructRef [#Word 'a']] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word 'b']]]]]]]]]]]"
s16 = "[#Input [#FDecl [#FDParam [#Word 'w']] [#FDName 'woSend']]]"
s17 = "[#Test [#FDecl [#FDParam [#Word 'w']] [#FDName 'woSend']]]"
s18 = "[#Input [#FDecl [#FDName 'hogege'] [#FDBody [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#FExpr [#FEParam [#StructRef [#Word 'name']]] [#FEName 'wofuyasu']]]]]]]]]]"
s19 = "[#Input [#VDecl [#Word '実行者']] [#FDecl [#FDName 'ほげげ'] [#FDBody [#LocalVDecl [#Word '対象者']] [#LocalVDecl [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '1']] [#ADD '+'] [#MulDiv [#Int '2']]]]]] [#Word '送金額']]]]]"
ss = "[#Input [#VDecl [#Word '総発行量']] [#VDecl [#Word '〜の残高']] [#VDecl [#Word '創設者']] [#FDecl [#FDParam [#Word '指定量']] [#FDName 'で初期化'] [#FDBody [#Assign [#StructRef [#Word '総発行量']] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word '指定量']]]]]]]] [#Assign [#StructRef [#Word '創設者']] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word '操作実行者']]]]]]]] [#Assign [#StructRef [#Map02 [#Word '創設者']]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word '総発行量']]]]]]]]]] [#FDecl [#FDParam [#Word '対象者']] [#Adv 'に'] [#FDParam [#Word '送金額']] [#FDName 'を送る'] [#FDBody [#Require [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Map02 [#Word '操作実行者']]]]] [#GT '>'] [#AddSub [#MulDiv [#StructRef [#Word '送金額']]]]]]]] [#Assign [#StructRef [#Map02 [#Word '対象者']]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Map02 [#Word '対象者']]]] [#ADD '+'] [#MulDiv [#StructRef [#Word '送金額']]]]]]]] [#Assign [#StructRef [#Map02 [#Word '実行者']]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Map02 [#Word '実行者']]]] [#SUB '-'] [#MulDiv [#StructRef [#Word '送金額']]]]]]]]]] [#FDecl [#FDName '所持金の確認'] [#FDBody [#Return [#StructRef [#Map02 [#Word '対象者']]]]]]]"

#---------------------------------------------------
print(transpile(ss,'./hoge/baku/sample.txt'))
# print(viewAST(ss))
# print(strToByte('hello'))