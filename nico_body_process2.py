import sys
from nico_ast2 import *
from nico_utils import *

def makeSOL(ast,tree):
    ast.setTree(tree)
    (code,tag) = getNode(ast)
    # tagMatch(tag,['Input'])
    return code

def debug(tree):
    ast = AST()
    ast.setTree(tree)
    (code,tag) = getNode(ast)
    # tagMatch(tag,['Input'])
    return code

def Input(ast):
    code = ''
    (title,tag) = getNode(ast)
    # tagMatch(tag,['Title'])
    version = 'pragma solidity ^0.4.24;\n'
    code += ast.Indent() + version + safeMath
    code += ast.Indent() + 'contract ' + title + ' {\n'
    ast.incIndent()
    code += ast.Indent() + 'using SafeMath for int256;\n\n'
    while(ast.current()==' '):
        ast.next()
        (s,tag) = getNode(ast)
        # tagMatch(tag,['VDecl','FDecl'])
        if tag in ['FDecl','Sol']:code+='\n'
        code += s
    ast.decIndent()
    code += ast.Indent() + '}\n'
    return code

def Title(ast):
    title = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        title+=ast.current()
        ast.next()
    ast.next()
    return 'c_'+strToByte(title)

def VDecl(ast):
    vs = []
    code = ''
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (s,tag) = getNode(ast)
        vs.append(s)
    for v in vs:
        code += ast.Indent() + ast.withType(v,'internal') + ';\n'
        ast.stvar.append(v)
    return code

def DMap(ast,count):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return 'map' + count

def FDecl(ast):
    code = ''
    codes = {
        'FDName':'',
        'FDInput':'',
        'FDRequire':'',
        'FDBody':'',
        'FDOutput':''
    }
    ast.back()
    ast.funcInfoReset()
    ast.incIndent()
    while(ast.current()==' '):
        ast.next()
        (c,tag) = getNode(ast)
        # tagMatch(tag, ['FDName','FDInput','FDRequire','FDBody','FDOutput'])
        codes[tag] = c
    ast.decIndent()
    code += ast.Indent()+'function '+codes['FDName']+'('+codes['FDInput']+') '+ast.getFuncInfo()+'{\n'
    code += codes['FDRequire'] + codes['FDBody'] + codes['FDOutput']
    code += ast.Indent()+'}\n'
    return code

def FDName(ast):
    (fname,tag) = getNode(ast)
    # tagMatch(tag,['FName'])
    if ast.current() == ' ':
        ast.next()
        (fname,tag) = getNode(ast)
        # tagMatch(tag,['FSName'])
    return fname

def FName(ast):
    fn = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        fn+=ast.current()
        ast.next()
    ast.next()
    return 'f_'+strToByte(fn)

def FSName(ast):
    fsn = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        fsn+=ast.current()
        ast.next()
    ast.next()
    return fsn

def FDInput(ast):
    inputs = []
    code = ''
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (s,tag) = getNode(ast)
        # tagMatch(tag,['Id'])
        inputs.append(s)
    for i in inputs:
        code += ', '+ast.withType(i,'')
    return code[2:]

def FDRequire(ast):
    code = ''
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (e,tag) = getNode(ast)
        code+=ast.Indent()+'require('+e+');\n'
    return code

def FDBody(ast):
    code = ''
    stmts = []
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (s,tag) = getNode(ast)
        stmts.append(s)
    for s in stmts:
        code += ast.Indent() + s + ';\n'
    return code

def FDOutput(ast):
    code = ''
    tcode = ''
    exprs = []
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (e,tag) = getNode(ast)
        code += ', '+e
        tcode += ', '+ast.typeDetect(e,0)
    ast.funcInfo['C'] += 'returns('+tcode[2:]+')'
    return ast.Indent()+'return ('+code[2:]+');\n'

def FExpr(ast):
    code = ''
    params = []
    (s,tag) = getNode(ast)
    while(tag != 'FEName'):
        params.append(s)
        ast.next()
        (s,tag) = getNode(ast)
    code += s + '('
    for i in range(len(params)):
        if i!=0:
            code+=', '
        code+=params[i]
    code+=')'
    ast.funcInfo['B'] = ''
    return code

def If(ast):
    code = ''
    (cnd,tag) = getNode(ast)
    ast.next()
    (thn,tag) = getNode(ast)
    ast.next()
    (els,tag) = getNode(ast)
    while(tag=='ElIf'):
        elf.append(els)
        ast.next()
        (els,tag) = getNode(ast)
    code+=ast.Indent()+'if('+cond+'){\n'
    code+=thn
    for elf in elfs:
        code+=elf
    code+=els
    return code

def Cond(ast):
    (code,tag) = getNode(ast)
    return code

def Then(ast):
    code = ''
    stmts = []
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (s,tag) = getNode(ast)
        stmts.append(s)
    ast.incIndent()
    for s in stmts:
        code+=ast.Indent()+s+';\n'
    ast.decIndent()
    return code

def ElIf(ast):
    code = ''
    (cond,tag) = getNode(ast)
    ast.next()
    (thn,tag) = getNode(ast)
    code+=ast.Indent()+'} else if('+cond+'){\n'
    code+=thn
    code+=ast.Indent()+'}\n'

def Else(ast):
    code = ''
    stmts = []
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (s,tag) = getNode(ast)
        stmts.append(s)
    code+=ast.Indent()+'} else {\n'
    ast.incIndent()
    for s in stmts:
        code+=ast.Indent()+s+';\n'
    ast.decIndent()
    code+=ast.Indent()+'}'
    return code

def Sol(ast):
    code = ''
    ast.requireNext('\'')
    while(ast.current()!='\'' or ast.string[ast.pos+1]!=']'):
        code += ast.current()
        ast.next()
    ast.next()
    code = allReplace(ast,code)
    ast.funcInfo['B'] = ''
    return code

def allReplace(ast,s):
    begin = s.find('「')
    while(begin >= 0):
        end = s.find('」')
        before = s[begin+1:end]
        if before in ast.reserved:
            after = ast.reserved[before]
        else:
            after = 'v_' + strToByte(before)
        s = s.replace('「'+before+'」', after)
        begin = s.find('「')
    return s




def Assign(ast):
    (left,tag) = getNode(ast)
    ast.next()
    (right,tag) = getNode(ast)
    if ast.isStateVar(left):
        ast.funcInfo['B'] = ''
    return left+' = '+right

def Tuple(ast):
    code = ''
    ps = []
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (p,tag) = getNode(ast)
        ps.append(p)
    code += '('
    for i in range(len(ps)):
        if i != 0:
            code+=', '
        code+=ps[i]
    code += ')'
    return code

def LocalVDecl(ast):
    (right,tag) = getNode(ast)
    ast.next()
    (left,tag) = getNode(ast)
    return ast.withType(left,'memory')+' = '+right

def FEName(ast):
    code = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        code+=ast.current()
        ast.next()
    ast.next()
    return 'f_'+strToByte(code)

def FEParam(ast):
    (inner,tag) = getNode(ast)
    return inner

def Logical(ast):
    code = ''
    (left,tag) = getNode(ast)
    code += left
    while(ast.current()==' '):
        ast.next()
        (op,tag) = getNode(ast)
        code += op
        ast.next()
        (right,tag) = getNode(ast)
        code += right
    return code

def AND(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return ' && '

def OR(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return ' || '

def Equality(ast):
    code = ''
    (left,tag) = getNode(ast)
    code += left
    while(ast.current()==' '):
        ast.next()
        (op,tag) = getNode(ast)
        code += op
        ast.next()
        (right,tag) = getNode(ast)
        code += right
    return code

def EQ(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return ' == '

def NEQ(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return ' != '

def Relational(ast):
    code = ''
    (left,tag) = getNode(ast)
    code += left
    while(ast.current()==' '):
        ast.next()
        (op,tag) = getNode(ast)
        code += op
        ast.next()
        (right,tag) = getNode(ast)
        code += right
    return code

def GTE(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return ' >= '

def LTE(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return ' <= '

def GT(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return ' > '

def LT(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return ' < '

def AddSub(ast):
    code = ''
    (left,tag) = getNode(ast)
    code += left
    while(ast.current()==' '):
        ast.next()
        (op,tag) = getNode(ast)
        code += op
        ast.next()
        (right,tag) = getNode(ast)
        code += right+')'
    return code

def ADD(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return '.add('

def SUB(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return '.sub('

def MulDivExpMod(ast):
    code = ''
    (left,tag) = getNode(ast)
    code += left
    while(ast.current()==' '):
        ast.next()
        (op,tag) = getNode(ast)
        code += op
        ast.next()
        (right,tag) = getNode(ast)
        code += right+')'
    return code

def MUL(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return '.mul('

def DIV(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return '.div('

def MOD(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return '.mod('

def EXP(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return '.exp('

def StructRef(ast):
    code = ''
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (scmp,tag) = getNode(ast)
        code+='.'+scmp
    return code[1:]

def ArrayRef(ast):
    code = ''
    (acmp,tag) = getNode(ast)
    code += acmp
    while(ast.current()==' '):
        (idx,tag) = getNode(ast)
        code += '[' + idx + ']'
    return code

def Index(ast):
    (idx,tag) = getNode(ast)
    return idx

def BT(ast):
    w = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    return 'true'

def BF(ast):
    w = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    return 'false'

def Addr(ast):
    w = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    return w

def Int(ast):
    w = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    return 'int('+w+')'

def String(ast):
    w = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    return '"'+w+'"'

def Id(ast):
    w = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    if w in ast.reserved:
        w = ast.reserved[w]
    else:
        w = 'v_'+strToByte(w)
    return w

def Map(ast,count):
    code = 'map'+count
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (p,tag) = getNode(ast)
        code+='['+p+']'
    return code

def getNode(ast):
    tag = ''
    ast.requireNext('[')
    ast.next()
    while(ast.current() != ' '):
        tag += ast.current()
        ast.next()
    ast.next()
    if tag.startswith('Map'):
        inner = Map(ast,tag[3:])
        tag = 'Map'
    elif tag.startswith('DMap'):
        inner = DMap(ast,tag[4:])
        tag = 'DMap'
    else:
        inner = globals()[tag](ast)
    ast.requireNext(']')
    return (inner,tag)

"""
def tagMatch(tag,tags):
    if tag not in tags:
        print(tag+' not find in '+str(tags))
        sys.exit()
"""

# ----------------------------------------------------------------------------------------------------
s0 = "[#Input [#Title 'テスト']]"
s1 = "[#Input [#Title 'テスト'] [#VDecl [#Id '単語1'] [#Id '単語2'] [#DMap0 '（ほげげ）の投票者情報']]]"
s2 = "[#Input [#Title 'テスト'] [#FDecl [#FDName [#FName '関数名'] [#FSName 'constructor']] [#FDBody [#Id '単語']]]]"
s3 = "[#Input [#Title 'テスト'] [#VDecl [#Id '単語1'] [#Id '単語2'] [#DMap0 '（ほげげ）の投票者情報'] [#DMap3 '〜の残高']] [#FDecl [#FDName [#FName 'こんにちHADES']] [#FDBody [#Id '単語']]]]"
s4 = "[#Input [#Title 'テストコントラクト'] [#VDecl [#IDecl [#Id '単語1']] [#IDecl [#Id '単語2']] [#MDecl [#DMap0 '（ほげげ）の投票者情報']] [#MDecl [#DMap3 '〜の残高']]] [#FDecl [#FDName [#FName 'こんにちHADES']] [#FDInput [#Id '単語1'] [#Id '単語2']] [#FDRequire [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#String '「こんにちは」']]]] [#EQ '＝'] [#Relational [#AddSub [#MulDiv [#BT 'true']]]]]]] [#FDBody [#LocalVDecl [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Id '単語1']]]]]] [#Id '単語3']]] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Id '単語4']]]]]]]] [#FDecl [#FDName [#FName 'どうなる'] [#FSName 'transferFrom']] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '334']]]]]]]]]"
s5 = "[#Input [#Title 'テストコントラクト'] [#VDecl [#Id '単語1'] [#Id '単語2'] [#DMap0 '（ほげげ）の投票者情報'] [#DMap3 '〜の残高']] [#FDecl [#FDName [#FName '全部'] [#FSName 'allFDBlock']] [#FDInput [#Id '単語1'] [#Id '単語2']] [#FDRequire [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#String '「こんにちは」']]]] [#EQ '＝'] [#Relational [#AddSub [#MulDiv [#BT 'true']]]]]]] [#FDBody [#LocalVDecl [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Id '単語1']]]]]] [#Id '単語3']]] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Id '単語4']]]]]]]] [#FDecl [#FDName [#FName 'どうなる'] [#FSName 'transferFrom']] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '334']]]]]]]]]"
s6 = "[#Input [#Title 'ERC20に基づくコインに関する契約'] [#VDecl [#Id '総発行量'] [#DMap3 '（参加者）の残高'] [#DMap2 '（対象者）から（送金者）が送金可能な金額']] [#FDecl [#FDName [#FName '契約の開始'] [#FSName 'constructor']] [#FDInput [#Id '総発行量の指定値']] [#FDBody [#Assign [#Id '総発行量'] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '総発行量の指定値'] [#MUL '＊'] [#Int '10']]]]]]] [#Assign [#Map3 [#Id 'あなた']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '総発行量']]]]]]]]] [#FDecl [#FDName [#FName '総発行量の確認'] [#FSName 'totalSupply']] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '総発行量']]]]]]]] [#FDecl [#FDName [#FName '残高の確認'] [#FSName 'balanceOf']] [#FDInput [#Id '対象者']] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id '対象者']]]]]]]]] [#FDecl [#FDName [#FName '送金可能金額の確認'] [#FSName 'allowance']] [#FDInput [#Id '対象者'] [#Id '送金者']] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map2 [#Id '対象者'] [#Id '送金者']]]]]]]]] [#FDecl [#FDName [#FName '送金'] [#FSName 'transfer']] [#FDInput [#Id '対象者'] [#Id '送金額']] [#FDRequire [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '対象者']]]] [#NEQ 'NOT='] [#Relational [#AddSub [#MulDivExpMod [#Addr '0x0']]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id 'あなた']]]] [#GTE '>='] [#AddSub [#MulDivExpMod [#Id '送金額']]]]]]] [#FDBody [#Assign [#Map3 [#Id 'あなた']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id 'あなた']]] [#SUB 'ー'] [#MulDivExpMod [#Id '送金額']]]]]]] [#Assign [#Map3 [#Id '対象者']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id '対象者']]] [#ADD '＋'] [#MulDivExpMod [#Id '送金額']]]]]]]] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#BT 'true']]]]]]]] [#FDecl [#FDName [#FName '第3者による送金の許可'] [#FSName 'approve']] [#FDInput [#Id '対象者'] [#Id '指定額']] [#FDRequire [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '送金者']]]] [#NEQ 'NOT='] [#Relational [#AddSub [#MulDivExpMod [#Addr '0x0']]]]]]] [#FDBody [#Assign [#Map2 [#Id 'あなた'] [#Id '対象者']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '指定額']]]]]]]] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#BT 'true']]]]]]]] [#FDecl [#FDName [#FName '第3者による送金'] [#FSName 'transferFrom']] [#FDInput [#Id '被送金者'] [#Id '対象者'] [#Id '送金額']] [#FDRequire [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '対象者']]]] [#NEQ 'NOT='] [#Relational [#AddSub [#MulDivExpMod [#Addr '0x0']]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id '被送金者']]]] [#GTE '>='] [#AddSub [#MulDivExpMod [#Id '送金額']]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map2 [#Id '被送金者'] [#Id 'あなた']]]] [#GTE '>='] [#AddSub [#MulDivExpMod [#Id '送金額']]]]]]] [#FDBody [#Assign [#Map3 [#Id '被送金者']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id '被送金者']]] [#SUB 'ー'] [#MulDivExpMod [#Id '送金額']]]]]]] [#Assign [#Map3 [#Id '対象者']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id '対象者']]] [#ADD '＋'] [#MulDivExpMod [#Id '送金額']]]]]]]] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#BT 'true']]]]]]]]]"

# print(debug(s6))