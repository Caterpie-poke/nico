import sys
from nico_ast import *
from nico_utils import *


def debug_transpile(tree):
    ast = AST()
    ast.setTree(tree)
    tag = ast.get_tag()
    tag_exe(tag,ast)
    return ast.output

def transpile(ast,tree):
    ast.setTree(tree)
    tag = ast.get_tag()
    tag_exe(tag,ast)
    return ast.output

def Input(ast):
    tag = ast.get_tag()#Title
    ast.output+=safeMath
    ast.output+='contract '
    tag_exe(tag,ast)
    ast.output+=' {\n'
    ast.incIndent()
    ast.makeIndent()
    ast.output+='using SafeMath for int256;\n\n'
    #Structs
    for k in ast.struct:
        ast.makeIndent()
        ast.output+=ast.structDef(k)
    ast.pos+=1
    while(True):
        tag = ast.get_tag()
        ast.makeIndent()
        tag_exe(tag,ast)
        ast.output+='\n'
        if ast.current() == ']':break
        ast.pos+=1
    ast.decIndent()
    ast.output+='}'

def Title(ast):
    ast.require('\'')
    ast.pos+=1
    w = ""
    while(ast.current() != '\''):
        w += ast.current()
        ast.pos+=1
    ast.output+=('c_'+strToByte(w))
    ast.pos+=1

def Test(ast):
    ast.output = '{AST_TEST'
    ast.pos = len(ast.string) - 1

#------------------------VarDecl--------------------------
def VDecl(ast):
    ast.write_to_temp = True
    tag = ast.get_tag()
    tag_exe(tag,ast)
    w = ast.temp
    ast.temp_reset()
    ast.write_to_temp = False
    ast.output+=(ast.withType(w)+';')

def MDecl(ast):
    tag = ast.get_tag()
    tag_exe(tag,ast)
def DMap(ast, tag):
    w = 'map'+tag[4:]
    ast.output+=ast.withType(w)
    ast.require('\'')
    ast.pos+=1
    while(ast.current()!='\''):
        ast.pos+=1
    ast.pos+=1

#------------------------FuncDecl--------------------------
def FDecl(ast):
    fparams = ''
    fname = ''
    ast.write_to_temp = True
    tag = ast.get_tag()#Name
    tag_exe(tag,ast)
    ast.output+='function f_' + strToByte(ast.temp) + '('
    ast.temp_reset()
    ast.pos+=1
    tag = ast.get_tag()
    if tag == '#FDInput':
        tag_exe(tag,ast)#Param
        ast.output+=ast.temp
        ast.temp_reset()
        ast.write_to_temp = False
        ast.pos+=1
        tag = ast.get_tag()
    ast.output+=') <pA><pB><pC>{\n'
    ast.incIndent()
    tag_exe(tag,ast)#Body
    ast.decIndent()
    ast.makeIndent()
    ast.output+='}'
    setFuncMod(ast)
    ast.funcInfo_reset()

def FDInput(ast):
    params = ''
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)
        params+=(' ,'+ast.withType(ast.temp))
        ast.temp_reset()
        if ast.current() == ']':break
        ast.pos+=1
    ast.temp = params[2:]

def OldFDecl(ast):
    fparams = []
    advs = ""
    fname = ""
    ast.write_to_temp = True
    tag = ast.get_tag()
    if tag == '#FDParam':
        tag_exe(tag,ast)#FDParam
        fparams.append(ast.temp)
        ast.temp_reset()
        ast.pos+=1
        tag = ast.get_tag()
    while(tag in ['#FDParam', '#Adv']):
        tag_exe(tag,ast)#Adv
        advs+=ast.temp
        ast.temp_reset()
        ast.pos+=1
        tag = ast.get_tag()
        tag_exe(tag,ast)#FDParam
        fparams.append(ast.temp)
        ast.temp_reset()
        ast.pos+=1
        tag = ast.get_tag()
    ast.output+='function '
    tag_exe(tag,ast)#FDName
    ast.write_to_temp = False
    fname = advs+ast.temp
    if fname in ast.reserved:
        ast.output+=ast.reserved[fname]
    else:
        ast.output+=('f_'+strToByte(fname))
    ast.temp_reset()
    ast.output+='('
    for fp in fparams:
        ast.output+=(ast.withType(fp) + ',')
    if len(fparams) > 0:
        ast.output = ast.output.rstrip(',')
    ast.output+=') <pA><pB><pC>{'
    if ast.current() == ' ':
        ast.pos+=1
        ast.output+='\n'
        ast.incIndent()
        tag = ast.get_tag()
        tag_exe(tag,ast)#FBody
        ast.decIndent()
        ast.makeIndent()
    ast.output+='}'
    setFuncMod(ast)
    ast.funcInfo_reset()

def FDBody(ast):
    semi_colon_cancel = False
    while(True):
        tag = ast.get_tag()
        if tag == '#If':
            semi_colon_cancel = True
        ast.makeIndent()
        tag_exe(tag,ast)
        if semi_colon_cancel:
            ast.output+='\n'
        else:
            ast.output+=';\n'
        if ast.current() == ']':break
        ast.pos+=1

def FDParam(ast):
    tag = ast.get_tag()
    tag_exe(tag,ast)

def FDName(ast):
    ast.require('\'')
    ast.pos+=1
    w = ""
    while(ast.current() != '\''):
        w+=ast.current()
        ast.pos+=1
    if ast.write_to_temp:
        ast.temp+=w
    else:
        ast.output+=w
    ast.pos+=1

#------------------------Statement--------------------------
def Return(ast):
    ast.write_to_temp = True
    ast.output+='return ('
    ast.funcInfo['returns']+='returns('
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)
        ast.output+=ast.temp
        ast.funcInfo['returns']+=ast.typeDetect(ast.temp,0)
        ast.temp_reset()
        if ast.current() == ']':break
        ast.pos+=1
        ast.funcInfo['returns']+=(', ')
        ast.output+=', '
    ast.funcInfo['returns']+=')'
    ast.output+=')'
    ast.write_to_temp = False

def Require(ast):
    while(True):
        ast.output+='require('
        tag = ast.get_tag()
        tag_exe(tag,ast)
        ast.output+=')'
        if ast.current() == ']':break

#Experimental
def Event(ast):
    ast.output+='emit '
    tag = ast.get_tag()
    tag_exe(tag,ast)
    ast.output+='('
    while(True):
        if ast.current() == ']':break
        ast.pos+=1
        tag = ast.get_tag()
        tag_exe(tag,ast)
        ast.output+=', '
    ast.output+=')'

def If(ast):
    ast.output+='if('
    #Condition
    tag = ast.get_tag()
    tag_exe(tag,ast)
    ast.output+='){\n'
    ast.pos+=1
    #Then
    ast.incIndent()
    tag = ast.get_tag()
    tag_exe(tag,ast)
    ast.decIndent()
    ast.makeIndent()
    ast.output+='}'
    ast.pos+=1
    #ElIf or Else
    tag = ast.get_tag()
    tag_exe(tag,ast)
    if ast.current() != ']':
        ast.pos+=1
        #Else
        tag = ast.get_tag()
        tag_exe(tag,ast)

def Cond(ast):
    tag = ast.get_tag()
    tag_exe(tag,ast)

def Then(ast):
    while(True):
        ast.makeIndent()
        tag = ast.get_tag()
        tag_exe(tag,ast)
        ast.output+=';\n'
        if ast.current() == ']':break
        ast.pos+=1

def ElIf(ast):
    ast.output+=' else if('
    #Condition
    tag = ast.get_tag()
    tag_exe(tag,ast)
    ast.output+='){\n'
    ast.pos+=1
    #Then
    ast.incIndent()
    tag = ast.get_tag()
    tag_exe(tag,ast)
    ast.decIndent()
    ast.makeIndent()
    ast.output+='}'

def Else(ast):
    ast.output+=' else {\n'
    ast.incIndent()
    while(True):
        ast.makeIndent()
        tag = ast.get_tag()
        tag_exe(tag,ast)
        ast.output+=';\n'
        if ast.current() == ']':break
        ast.pos+=1
    ast.decIndent()
    ast.makeIndent()
    ast.output+='}'

def Assign(ast):
    tag = ast.get_tag()
    tag_exe(tag,ast)
    ast.output+=' = '
    ast.pos+=1
    tag = ast.get_tag()
    tag_exe(tag,ast)

def Tuple(ast):
    ast.output+='('
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)
        if ast.current() == ']':break
        ast.output+=', '
        ast.pos+=1
    ast.output+=')'

def LocalVDecl(ast):
    tag = ast.get_tag()
    ast.output+='<LEFT>'
    if tag != '#Word':
        ast.output+=' = '
        tag_exe(tag,ast)
        if ast.write_to_temp:
            ast.output+=ast.temp
            ast.temp_reset()
        ast.pos+=1
        tag = ast.get_tag()
    ast.write_to_temp = True
    tag_exe(tag,ast)
    left = (ast.typeDetect(ast.temp,0)+' '+ast.temp)
    ast.write_to_temp = False
    ast.temp_reset()
    ast.output = ast.output.replace('<LEFT>',left)

#------------------------Expression--------------------------
def FExpr(ast):
    fparams = []
    fname = ""
    ast.write_to_temp = True
    tag = ast.get_tag()
    while(tag == '#FEParam'):
        tag_exe(tag,ast)
        fparams.append(ast.temp)
        ast.temp_reset()
        if ast.current() == ']':break
        ast.pos+=1
        tag = ast.get_tag()
    tag_exe(tag,ast)
    fname = ast.temp
    ast.temp_reset()
    ast.write_to_temp = False
    ast.output+=('f_'+strToByte(fname)+'(')
    for fp in fparams:
        ast.output+=(fp+',')
    if len(fparams) > 0:
        ast.output = ast.output.rstrip(',')
    ast.output+=')'


def OldFExpr(ast):
    fparams = []
    advs = ""
    fname = ""
    ast.write_to_temp = True
    tag = ast.get_tag()
    if tag == '#FEParam':
        tag_exe(tag,ast)#FParam
        fparams.append(ast.temp)
        ast.temp_reset()
        ast.pos+=1
        tag = ast.get_tag()
    while(tag in ['#Adv','#FEParam']):
        tag_exe(tag,ast)#Adv
        advs+=ast.temp
        ast.temp_reset()
        ast.pos+=1
        tag = ast.get_tag()
        tag_exe(tag,ast)#FParam
        fparams.append(ast.temp)
        ast.temp_reset()
        ast.pos+=1
        tag = ast.get_tag()
    tag_exe(tag,ast)#FName
    ast.output+=('f_'+strToByte(advs+ast.temp))
    ast.write_to_temp = False
    ast.temp_reset()
    ast.output+='('
    for fp in fparams:
        ast.output+=(fp+',')
    if len(fparams) > 0:
        ast.output = ast.output.rstrip(',')
    ast.output+=')'

def Adv(ast):
    ast.require('\'')
    ast.pos+=1
    w = ""
    while(ast.current() != '\''):
        w+=ast.current()
        ast.pos+=1
    if ast.write_to_temp:
        ast.temp+=w
    else:
        ast.output+=w
    ast.pos+=1

def FEParam(ast):
    tag = ast.get_tag()
    tag_exe(tag,ast)

def FEName(ast):
    ast.require('\'')
    ast.pos+=1
    w = ""
    while(ast.current() != '\''):
        w+=ast.current()
        ast.pos+=1
    if ast.write_to_temp:
        ast.temp+=w
    else:
        ast.output+=w
    ast.pos+=1

def Logical(ast):
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)
        if ast.current()==']':break
        ast.pos+=1

def Equality(ast):
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)
        if ast.current()==']':break
        ast.pos+=1

def Relational(ast):
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)
        if ast.current()==']':break
        ast.pos+=1

def AddSub(ast):
    tag = ast.get_tag()
    tag_exe(tag,ast)#Left
    while(ast.current()!=']'):
        ast.pos+=1
        tag = ast.get_tag()
        tag_exe(tag,ast)#Operator
        ast.output+='('
        ast.pos+=1
        tag = ast.get_tag()
        tag_exe(tag,ast)#Right
        ast.output+=')'

def MulDiv(ast):
    tag = ast.get_tag()
    tag_exe(tag,ast)#Left
    while(ast.current()!=']'):
        ast.pos+=1
        tag = ast.get_tag()
        tag_exe(tag,ast)#Operator
        ast.output+='('
        ast.pos+=1
        tag = ast.get_tag()
        tag_exe(tag,ast)#Right
        ast.output+=')'

def OldAddSub(ast):
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)
        if ast.current()==']':break
        ast.pos+=1

def OldMulDiv(ast):
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)
        if ast.current() == ']':break
        ast.pos+=1

def AND(ast):
    ast.pos+=4
    ast.output+=' && '

def OR(ast):
    ast.pos+=5
    ast.output+=' || '

def EQ(ast):
    ast.pos+=3
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
    ast.output+='.add'

def SUB(ast):
    ast.pos+=3
    ast.output+='.sub'

def MUL(ast):
    ast.pos+=3
    ast.output+='.mul'

def DIV(ast):
    ast.pos+=3
    ast.output+='.div'

def Map(ast, tag):
    if ast.write_to_temp:ast.temp+=('map'+tag[3:])
    else:ast.output+=('map'+tag[3:])
    while(True):
        if ast.write_to_temp:ast.temp+='['
        else:ast.output+='['
        tag = ast.get_tag()
        tag_exe(tag,ast)
        if ast.write_to_temp:ast.temp+=']'
        else:ast.output+=']'
        if ast.current() == ']':break

def StructRef(ast):
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)
        if ast.current() == ']':break
        ast.pos+=1
        if ast.write_to_temp:ast.temp+='.'
        else:ast.output+='.'

def ArrayRef(ast):
    tag = ast.get_tag()
    tag_exe(tag,ast)
    while(True):
        if ast.current() == ']':break
        if ast.write_to_temp:ast.temp+='['
        else:ast.output+='['
        ast.pos+=1
        tag = ast.get_tag()
        tag_exe(tag,ast)
        if ast.write_to_temp:ast.temp+=']'
        else:ast.output+=']'

def Index(ast):
    tag = ast.get_tag()
    tag_exe(tag, ast)

def Int(ast):
    ast.require('\'')
    ast.pos+=1
    w = ""
    while(ast.current() != '\''):
        w += ast.current()
        ast.pos+=1
    w = 'int256('+w+')'
    if ast.write_to_temp:
        ast.temp += w
    else:
        ast.output += w
    ast.pos+=1

def Addr(ast):
    ast.require('\'')
    ast.pos+=2
    w = ""
    while(ast.current() != '\''):
        w += ast.current()
        ast.pos+=1
    if ast.write_to_temp:
        ast.temp += w
    else:
        ast.output += w
    ast.pos+=1

def BT(ast):
    ast.require('\'')
    if ast.write_to_temp:
        ast.temp += 'true'
    else:
        ast.output += 'true'
    ast.pos+=4#1+2(はい)+1

def BF(ast):
    ast.require('\'')
    if ast.write_to_temp:
        ast.temp += 'false'
    else:
        ast.output += 'false'
    ast.pos+=5#1+3(いいえ)+1

def Word(ast):
    ast.require('\'')
    ast.pos+=1
    s = ""
    while(ast.current() != '\''):
        s += ast.current()
        ast.pos+=1
    if s in ast.reserved:
        if ast.write_to_temp:
            ast.temp += ast.reserved[s]
        else:
            ast.output += ast.reserved[s]
    else:
        if ast.write_to_temp:
            ast.temp += ('v_'+strToByte(s))
        else:
            ast.output += ('v_'+strToByte(s))
    ast.pos+=1

def tag_exe(tag,ast):
    if tag[1:].startswith('Map'):
        Map(ast, tag[1:])
    elif tag[1:].startswith('DMap'):
        DMap(ast, tag[1:])
    else:
        globals()[tag[1:]](ast)
    ast.require(']')
    ast.pos+=1

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
s20 = "[#Input [#Title '仮想通貨に関する契約'] [#VDecl [#Word 'おはようから']] [#VDecl [#Word 'おやすみまで']] [#VDecl [#Word 'ライオン']] [#FDecl [#FDParam [#Word 'あ']] [#Adv 'を'] [#FDParam [#Word 'い']] [#FDName 'に送る'] [#FDBody [#Return [#Word 'なんでも']] [#Assign [#Word 'ANS'] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '1']] [#ADD '+'] [#MulDiv [#Int '2'] [#MUL '*'] [#Int '3']]]]]]] [#LocalVDecl [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '123']]]]]] [#Word '仮']] [#FExpr [#FEParam [#Int '12']] [#Adv 'を'] [#FEParam [#Int '45']] [#FEName 'におくる']] [#Tuple [#Int '1'] [#Int '2']] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word 'あなた'] [#ArrayRef [#Word 'わたし'] [#Index [#Int '3']]]]]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#ArrayRef [#Map00 [#Word '貴様']] [#Index [#Int '3']]] [#Word '親']]]] [#GT '>'] [#AddSub [#MulDiv [#Int '12']]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word 'HIP'] [#Word 'YOU']]]]]] [#AND 'かつ'] [#Equality [#Relational [#AddSub [#MulDiv [#Int '1']] [#ADD '+'] [#MulDiv [#Int '2']] [#ADD '+'] [#MulDiv [#Int '3']] [#ADD '+'] [#MulDiv [#Int '4']]]]]] [#FExpr [#FEParam [#StructRef [#Word 'ぱら'] [#Word 'めーた']]] [#Adv 'を'] [#FEParam [#StructRef [#Word 'たい'] [#Word 'しょう']]] [#FEName 'に送ってしまえ']] [#Assign [#Word '現在'] [#FExpr [#FEParam [#Word '対象者']] [#FEName 'がもつ金額の確認']]] [#If [#Cond [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'A']]]]]]] [#Then [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'B']]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'C']]]]]]] [#ElIf [#Cond [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'D']]]]]]] [#Then [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'E']]]]]]]] [#Else [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'F']]]]]]]] [#If [#Cond [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'AAA']]]]]]] [#Then [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'BBB']]]]]]] [#Else [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'CCC']]]]]]]]]]]"
s21 = "[#Input [#VDecl [#Word '総発行量']] [#VDecl [#Word '〜の残高']] [#VDecl [#Word '創設者']] [#FDecl [#FDParam [#Word '指定量']] [#FDName 'で初期化'] [#FDBody [#Assign [#StructRef [#Word '総発行量']] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word '指定量']]]]]]]] [#Assign [#StructRef [#Word '創設者']] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word '操作実行者']]]]]]]] [#Assign [#StructRef [#Map02 [#Word '創設者']]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word '総発行量']]]]]]]]]] [#FDecl [#FDParam [#Word '対象者']] [#Adv 'に'] [#FDParam [#Word '送金額']] [#FDName 'を送る'] [#FDBody [#Require [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Map02 [#Word '操作実行者']]]]] [#GT '>'] [#AddSub [#MulDiv [#StructRef [#Word '送金額']]]]]]]] [#Assign [#StructRef [#Map02 [#Word '対象者']]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Map02 [#Word '対象者']]]] [#ADD '+'] [#MulDiv [#StructRef [#Word '送金額']]]]]]]] [#Assign [#StructRef [#Map02 [#Word '実行者']]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Map02 [#Word '実行者']]]] [#SUB '-'] [#MulDiv [#StructRef [#Word '送金額']]]]]]]]]] [#FDecl [#FDName '所持金の確認'] [#FDBody [#Return [#StructRef [#Map02 [#Word '対象者']]]]]]]"
s22 = "[#Input [#Title '仮想通貨に関する契約'] [#VDecl [#Word 'おはようから']] [#VDecl [#Word 'おやすみまで']] [#VDecl [#Word 'ライオン']] [#MDecl [#DMap00 '（参加者）の投票者情報']] [#FDecl [#FDParam [#Word 'あ']] [#Adv 'を'] [#FDParam [#Word 'い']] [#FDName 'に送る'] [#FDBody [#Return [#Word 'なんでも']] [#Assign [#Word 'ANS'] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '1']] [#ADD '+'] [#MulDiv [#Int '2'] [#MUL '*'] [#Int '3']]]]]]] [#LocalVDecl [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '123']]]]]] [#Word '仮']] [#FExpr [#FEParam [#Int '12']] [#Adv 'を'] [#FEParam [#Int '45']] [#FEName 'におくる']] [#Tuple [#Int '1'] [#Int '2']] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word 'あなた'] [#ArrayRef [#Word 'わたし'] [#Index [#Int '3']]]]]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#ArrayRef [#Map00 [#Word '貴様']] [#Index [#Int '3']]] [#Word '親']]]] [#GT '>'] [#AddSub [#MulDiv [#Int '12']]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#StructRef [#Word 'HIP'] [#Word 'YOU']]]]]] [#AND 'かつ'] [#Equality [#Relational [#AddSub [#MulDiv [#Int '1']] [#ADD '+'] [#MulDiv [#Int '2']] [#ADD '+'] [#MulDiv [#Int '3']] [#ADD '+'] [#MulDiv [#Int '4']]]]]] [#FExpr [#FEParam [#StructRef [#Word 'ぱら'] [#Word 'めーた']]] [#Adv 'を'] [#FEParam [#StructRef [#Word 'たい'] [#Word 'しょう']]] [#FEName 'に送ってしまえ']] [#Assign [#Word '現在'] [#FExpr [#FEParam [#Word '対象者']] [#FEName 'がもつ金額の確認']]] [#If [#Cond [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'A']]]]]]] [#Then [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'B']]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'C']]]]]]] [#ElIf [#Cond [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'D']]]]]]] [#Then [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'E']]]]]]]] [#Else [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'F']]]]]]]] [#If [#Cond [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'AAA']]]]]]] [#Then [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'BBB']]]]]]] [#Else [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Word 'CCC']]]]]]]]]]]"

#---------------------------------------------------
# print(debug_transpile(s22))
# print(viewAST(ss))
# print(strToByte('hello'))