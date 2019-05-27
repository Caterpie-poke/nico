import sys
from nico_ast import *
from nico_utils import *

def makeSOL(ast,tree):
    ast.setTree(tree)
    ast.precode += 'pragma solidity ^' + ast.version + ';\n'
    (code,tag) = getNode(ast)
    return ast.precode + '\n' + safeMath*(not ast.imported) + code

def debug(tree):
    ast = AST()
    ast.setTree(tree)
    (code,tag) = getNode(ast)
    return code

def Input(ast):
    code = ''
    (title,tag) = getNode(ast)
    code += 'contract ' + title + ' {\n'
    ast.incIndent()
    code += ast.Indent() + 'using SafeMath for uint256;\n'
    code += ast.Indent() + 'using SafeMath for int256;\n'
    for k in ast.struct:
        code += ast.Indent() + ast.structDefWrite(k) + '\n'
    code += '\n'
    while(ast.current()==' '):
        ast.next()
        (ds,tag) = getNode(ast)
        if tag in ['FDecl','Sol']:code+='\n'
        code += ds
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

def IDecl(ast):
    ((cname,alias),tag) = getNode(ast)
    ast.next()
    (cpath,tag) = getNode(ast)
    ast.next()
    (caddr,tag) = getNode(ast)
    ast.precode += 'import \'' + cpath.replace('.nc', '.sol') + '\';\n'
    ast.imported = True
    s_instance = ast.Indent() + cname + ' ' + alias + ' = ' + cname + '(' + caddr + ');\n'
    return s_instance

def CName(ast):
    (title,tag) = getNode(ast)
    ast.next()
    (raw,tag) = getNode(ast)
    return (title, raw)

def CPath(ast):
    (path,tag) = getNode(ast)
    return path

def CAddr(ast):
    (addr,tag) = getNode(ast)
    return addr

def Pair(ast):
    (raw,tag) = getNode(ast)
    ast.next()
    (v,tag) = getNode(ast)
    ast.words[v][0] = raw
    return v

def RAW(ast):
    raw = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        raw += ast.current()
        ast.next()
    ast.next()
    return raw

def VDecl(ast):
    vs = []
    code = ''
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (s,tag) = getNode(ast)
        vs.append(s)
    for v in vs:
        code += ast.Indent() + ast.withType(v,'internal') + ';' + '    /*' + ast.words[v][0] + '*/\n'
        ast.stvar.append(v)
    return code

def DMap(ast,count):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return 'map' + count

def SolBlock(ast):
    code = ''
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (line,tag) = getNode(ast)
        code += ast.Indent() + line + '\n'
    return code

def SolLine(ast):
    code = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        code+=ast.current()
        ast.next()
    ast.next()
    return code

def EDecl(ast):
    code = ''
    codes = {
        'EDName':'',
        'EDInput':'',
    }
    ast.back()
    # ast.funcInfoReset()
    ast.doxygenReset()
    while(ast.current()==' '):
        ast.next()
        (c,tag) = getNode(ast)
        codes[tag] = c
    code += ast.Indent() + '/*\n'
    for dxstmt in ast.doxygen:
        code += ast.Indent() + dxstmt + '\n'
    code += ast.Indent() + '*/\n'
    code += ast.Indent()+'event '+codes['EDName']+'('+codes['EDInput']+');\n'
    return code

def EDName(ast):
    (ename,tag) = getNode(ast)
    ast.reserved[ename] = [ename]
    if ast.current() == ' ':
        ast.next()
        (esname,tag) = getNode(ast)
        ast.reserved[ename] = [esname]
        ename = esname
    return ename

def EName(ast):
    en = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        en+=ast.current()
        ast.next()
    ast.next()
    code = 'e_'+strToByte(en)
    ast.doxygen.append('@event '+code+' '+en)
    return code

def ESName(ast):
    esn = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        esn+=ast.current()
        ast.next()
    ast.next()
    dx = ast.doxygen[-1].split(' ')
    dx[1] = esn
    ast.doxygen[-1] = dx[0]+' '+dx[1]+' '+dx[2]
    return esn

def EDInput(ast):
    inputs = []
    code = ''
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (s,tag) = getNode(ast)
        if(tag != 'ETH'):
            inputs.append(s)
            ast.doxygen.append('@param '+s+' '+ast.words[s][0])
    for i in inputs:
        code += ', '+ast.withType(i,'')
    return code[2:]


def FDecl(ast):
    code = ''
    codes = {
        'FDName':'',
        'FDInput':'',
        'FDBody':'',
    }
    ast.back()
    ast.funcInfoReset()
    ast.doxygenReset()
    ast.incIndent()
    while(ast.current()==' '):
        ast.next()
        (c,tag) = getNode(ast)
        codes[tag] = c
    ast.decIndent()
    isConstructor = (codes['FDName'] == 'constructor')
    code += ast.Indent() + '/*\n'
    for dxstmt in ast.doxygen:
        code += ast.Indent() + dxstmt + '\n'
    code += ast.Indent() + '*/\n'
    code += ast.Indent()+('function ' * (not isConstructor))+codes['FDName']+'('+codes['FDInput']+') '+ast.getFuncInfo()+'{\n'
    code += ast.addrCheck
    code += codes['FDBody']
    code += ast.Indent()+'}\n'
    return code

def FDName(ast):
    (fname,tag) = getNode(ast)
    ast.reserved[fname] = [fname]
    if ast.current() == ' ':
        ast.next()
        (fsname,tag) = getNode(ast)
        ast.reserved[fname] = [fsname]
        fname = fsname
    return fname

def FName(ast):
    fn = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        fn+=ast.current()
        ast.next()
    ast.next()
    code = 'f_'+strToByte(fn)
    ast.doxygen.append('@function '+code+' '+fn)
    return code

def FSName(ast):
    fsn = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        fsn+=ast.current()
        ast.next()
    ast.next()
    dx = ast.doxygen[-1].split(' ')
    dx[1] = fsn
    ast.doxygen[-1] = dx[0]+' '+dx[1]+' '+dx[2]
    return fsn

def FDInput(ast):
    inputs = []
    code = ''
    ast.addrCheck = ''
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (s,tag) = getNode(ast)
        if(tag != 'ETH'):
            inputs.append(s)
            if(ast.typeDetect(s,0) == 'address'):
                ast.addrCheck+=ast.Indent()+'require('+s+' != address(0));\n'
            ast.doxygen.append('@param '+s+' '+ast.words[s][0])
    for i in inputs:
        code += ', '+ast.withType(i,'memory')
    return code[2:]

def ETH(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    ast.funcInfo['B'] = 'payable'
    return None

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
        if(s.startswith('if')):
            code = code[:-2] + '\n'
    return code

def Return(ast):
    code = ''
    tcode = ''
    ext = ''
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (rs,tag) = getNode(ast)
        if(rs in ast.words):
            ext = ' '+ast.words[rs][0]
        ast.doxygen.append('@return '+rs+ext)
        code += ', '+rs
        retType = ast.typeDetect(rs,0)
        if(retType not in ['uint256','address', 'bool']):
            retType+=' memory'
        tcode += ', '+ retType
    ast.funcInfo['C'] += 'returns('+tcode[2:]+')'
    return 'return ('+code[2:]+')'

def ReturnTrue(ast):
    fn = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        fn+=ast.current()
        ast.next()
    ast.next()
    ast.funcInfo['C'] += 'returns(bool)'
    return 'return true'

def FExpr(ast):
    code = ''
    cname = ''
    fname = ''
    params = []
    (n,tag) = getNode(ast)
    if tag == 'FEName':
        return ast.reserved[n][0]+'()'
    elif tag == 'RAW':
        cname = n+'.'
    elif tag == 'FEParam':
        params.append(n)
    ast.next()
    (n,tag) = getNode(ast)
    while(tag == 'FEParam'):
        params.append(n)
        ast.next()
        (n,tag) = getNode(ast)
    code += cname + ast.reserved[n][0] + '('
    for i in range(len(params)):
        if i!=0:
            code+=', '
        code+=params[i]
    code+=')'
    ast.notView()
    return code

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

def EExpr(ast):
    code = ''
    ename = ''
    params = []
    (n,tag) = getNode(ast)
    if tag == 'EEName':
        return 'emit '+ast.reserved[n][0]+'()'
    while(tag == 'EEParam'):
        params.append(n)
        ast.next()
        (n,tag) = getNode(ast)
    code += 'emit ' + ast.reserved[n][0] + '('
    for i in range(len(params)):
        if i!=0:
            code+=', '
        code+=params[i]
    code+=')'
    ast.notView()
    return code

def EEName(ast):
    code = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        code+=ast.current()
        ast.next()
    ast.next()
    return 'e_'+strToByte(code)

def EEParam(ast):
    (inner,tag) = getNode(ast)
    return inner


def IncFunc(ast):
    (base,tag) = getNode(ast)
    ast.next()
    (diff,tag) = getNode(ast)
    if(ast.isStateVar(base)):
        ast.notView()
    return base + ' = ' + base + '.add(' + diff + ')'

def DecFunc(ast):
    (base,tag) = getNode(ast)
    ast.next()
    (diff,tag) = getNode(ast)
    if(ast.isStateVar(base)):
        ast.notView()
    return base + ' = ' + base + '.sub(' + diff + ')'

def PushFunc(ast):
    (to,tag) = getNode(ast)
    ast.next()
    (ct,tag) = getNode(ast)
    if(ast.isStateVar(to)):
        ast.notView()
    return to + '.push(' + ct + ')'

def AddrExistFunc(ast):
    (addr,tag) = getNode(ast)
    return addr + ' != address(0)'

def EthTransfer(ast):
    (target,tag) = getNode(ast)
    ast.next()
    (amount,tag) = getNode(ast)
    ast.next()
    (unit,tag) = getNode(ast)
    return 'address('+target+').transfer(uint256('+amount+' '+unit+'))'

def Ether(ast):
    w = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    return w

def If(ast):
    code = ''
    elfs = []
    els = ''
    (cnd,tag) = getNode(ast)
    ast.next()
    (thn,tag) = getNode(ast)
    if ast.current() != ']':
        ast.next()
        (els,tag) = getNode(ast)
    while(tag=='ElIf'):
        elfs.append(els)
        ast.next()
        (els,tag) = getNode(ast)
    code+='if('+cnd+'){\n'
    code+=thn
    for elf in elfs:
        code+=elf
    code+=els
    code+=ast.Indent()+'}'
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
    return code

def Require(ast):
    (e,tag) = getNode(ast)
    code = 'require('+e+')'
    return code

def Sol(ast):
    code = ''
    ast.requireNext('\'')
    while(ast.current()!='\'' or ast.string[ast.pos+1]!=']'):
        code += ast.current()
        ast.next()
    ast.next()
    code = allReplace(ast,code)
    ast.notView()
    return code

def allReplace(ast,s):
    begin = s.find('「')
    while(begin >= 0):
        end = s.find('」')
        before = s[begin+1:end]
        if before in ast.reserved:
            after = ast.reserved[before][0]
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
        ast.notView()
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

def LVDecl(ast):
    (v,tag) = getNode(ast)
    ast.doxygen.append('@localVar '+v+' '+ast.words[v][0])
    return ast.withType(v,'memory')

def LVDeclAssign(ast):
    (right,tag) = getNode(ast)
    ast.next()
    (left,tag) = getNode(ast)
    ast.doxygen.append('@localVar '+left+' '+ast.words[left][0])
    return ast.withType(left,'memory') + ' = ' + right

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

def MulDiv(ast):
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

def ExpMod(ast):
    code = ''
    (left,tag) = getNode(ast)
    code += left
    if(ast.current()==' '):
        ast.next()
        (op,tag) = getNode(ast)
        code += op
        ast.next()
        (right,tag) = getNode(ast)
        code += right+')'
    return code

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
    ja = ''
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (scmp,tag) = getNode(ast)
        code+='.'+scmp
        ja+='の'+ast.words[scmp][0]
    ast.words[code[1:]] = [ja[1:]]
    ast.words[code[1:]].extend(ast.words[scmp][1:])
    return code[1:]

def Leng(ast):
    code = ''
    (inner,tag) = getNode(ast)
    # code = 'int256('+inner+'.length)'
    code = inner+'.length'
    ja = ast.words[inner][0]
    ast.words[code] = [ja+'のサイズ','int']
    return code

def ArrayRef(ast):
    code = ''
    ja = ''
    (acmp,tag) = getNode(ast)
    code += acmp
    ja += ast.words[acmp][0]
    c = 1
    while(ast.current()==' '):
        ast.next()
        c+=1
        (idx,tag) = getNode(ast)
        code += '[' + idx + ']'
        ja += 'の'+ast.words[idx][0]+'番目'
    ast.words[code] = [ja]
    ast.words[code].extend(ast.words[acmp][c:])
    return code

def Index(ast):
    (idx,tag) = getNode(ast)
    #code = 'uint('+idx+')'
    code = idx
    ast.words[code] = [ast.words[idx][0]]
    return code

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
    code = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    code = 'uint256('+w+')'
    ast.words[code] = [str(w)]
    return code

def String(ast):
    w = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    code = '"'+w+'"'
    ast.words[code] = [ast.words[w][0]]
    return code

def Id(ast):
    w = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    if w in ast.reserved:
        w = ast.reserved[w][0]
    else:
        w = 'v_'+strToByte(w)
    return w

def Map(ast,count):
    code = 'map'+count
    tmap = ast.map[int(count)]
    params = []
    ja = ''
    c = 0
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (p,tag) = getNode(ast)
        params.append(p)
    if len(params)<len(tmap):
        ja+=tmap[0]
        tmap=tmap[1:]
    for p in params:
        code+='['+p+']'
        ja+=ast.words[p][0]+tmap[c]
        c+=1
    ast.words[code] = [ja,ast.words['map'+count][-1]]
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


# ----------------------------------------------------------------------------------------------------
s0 = "[#Input [#Title 'テスト']]"
s1 = "[#Input [#Title 'テスト'] [#VDecl [#Id '単語1'] [#Id '単語2'] [#DMap0 '（ほげげ）の投票者情報']]]"
s2 = "[#Input [#Title 'テスト'] [#FDecl [#FDName [#FName '関数名'] [#FSName 'constructor']] [#FDBody [#Id '単語']]]]"
s3 = "[#Input [#Title 'テスト'] [#VDecl [#Id '単語1'] [#Id '単語2'] [#DMap0 '（ほげげ）の投票者情報'] [#DMap3 '〜の残高']] [#FDecl [#FDName [#FName 'こんにちHADES']] [#FDBody [#Id '単語']]]]"
s4 = "[#Input [#Title 'テストコントラクト'] [#VDecl [#IDecl [#Id '単語1']] [#IDecl [#Id '単語2']] [#MDecl [#DMap0 '（ほげげ）の投票者情報']] [#MDecl [#DMap3 '〜の残高']]] [#FDecl [#FDName [#FName 'こんにちHADES']] [#FDInput [#Id '単語1'] [#Id '単語2']] [#FDRequire [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#String '「こんにちは」']]]] [#EQ '＝'] [#Relational [#AddSub [#MulDiv [#BT 'true']]]]]]] [#FDBody [#LocalVDecl [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Id '単語1']]]]]] [#Id '単語3']]] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Id '単語4']]]]]]]] [#FDecl [#FDName [#FName 'どうなる'] [#FSName 'transferFrom']] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '334']]]]]]]]]"
s5 = "[#Input [#Title 'テストコントラクト'] [#VDecl [#Id '単語1'] [#Id '単語2'] [#DMap0 '（ほげげ）の投票者情報'] [#DMap3 '〜の残高']] [#FDecl [#FDName [#FName '全部'] [#FSName 'allFDBlock']] [#FDInput [#Id '単語1'] [#Id '単語2']] [#FDRequire [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#String '「こんにちは」']]]] [#EQ '＝'] [#Relational [#AddSub [#MulDiv [#BT 'true']]]]]]] [#FDBody [#LocalVDecl [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Id '単語1']]]]]] [#Id '単語3']]] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Id '単語4']]]]]]]] [#FDecl [#FDName [#FName 'どうなる'] [#FSName 'transferFrom']] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDiv [#Int '334']]]]]]]]]"
s6 = "[#Input [#Title 'ERC20に基づくコインに関する契約'] [#VDecl [#Id '総発行量'] [#DMap3 '（参加者）の残高'] [#DMap2 '（対象者）から（送金者）が送金可能な金額']] [#FDecl [#FDName [#FName '契約の開始'] [#FSName 'constructor']] [#FDInput [#Id '総発行量の指定値']] [#FDBody [#Assign [#Id '総発行量'] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '総発行量の指定値'] [#MUL '＊'] [#Int '10']]]]]]] [#Assign [#Map3 [#Id 'あなた']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '総発行量']]]]]]]]] [#FDecl [#FDName [#FName '総発行量の確認'] [#FSName 'totalSupply']] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '総発行量']]]]]]]] [#FDecl [#FDName [#FName '残高の確認'] [#FSName 'balanceOf']] [#FDInput [#Id '対象者']] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id '対象者']]]]]]]]] [#FDecl [#FDName [#FName '送金可能金額の確認'] [#FSName 'allowance']] [#FDInput [#Id '対象者'] [#Id '送金者']] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map2 [#Id '対象者'] [#Id '送金者']]]]]]]]] [#FDecl [#FDName [#FName '送金'] [#FSName 'transfer']] [#FDInput [#Id '対象者'] [#Id '送金額']] [#FDRequire [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '対象者']]]] [#NEQ 'NOT='] [#Relational [#AddSub [#MulDivExpMod [#Addr '0x0']]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id 'あなた']]]] [#GTE '>='] [#AddSub [#MulDivExpMod [#Id '送金額']]]]]]] [#FDBody [#Assign [#Map3 [#Id 'あなた']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id 'あなた']]] [#SUB 'ー'] [#MulDivExpMod [#Id '送金額']]]]]]] [#Assign [#Map3 [#Id '対象者']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id '対象者']]] [#ADD '＋'] [#MulDivExpMod [#Id '送金額']]]]]]]] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#BT 'true']]]]]]]] [#FDecl [#FDName [#FName '第3者による送金の許可'] [#FSName 'approve']] [#FDInput [#Id '対象者'] [#Id '指定額']] [#FDRequire [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '送金者']]]] [#NEQ 'NOT='] [#Relational [#AddSub [#MulDivExpMod [#Addr '0x0']]]]]]] [#FDBody [#Assign [#Map2 [#Id 'あなた'] [#Id '対象者']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '指定額']]]]]]]] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#BT 'true']]]]]]]] [#FDecl [#FDName [#FName '第3者による送金'] [#FSName 'transferFrom']] [#FDInput [#Id '被送金者'] [#Id '対象者'] [#Id '送金額']] [#FDRequire [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Id '対象者']]]] [#NEQ 'NOT='] [#Relational [#AddSub [#MulDivExpMod [#Addr '0x0']]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id '被送金者']]]] [#GTE '>='] [#AddSub [#MulDivExpMod [#Id '送金額']]]]]] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map2 [#Id '被送金者'] [#Id 'あなた']]]] [#GTE '>='] [#AddSub [#MulDivExpMod [#Id '送金額']]]]]]] [#FDBody [#Assign [#Map3 [#Id '被送金者']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id '被送金者']]] [#SUB 'ー'] [#MulDivExpMod [#Id '送金額']]]]]]] [#Assign [#Map3 [#Id '対象者']] [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#Map3 [#Id '対象者']]] [#ADD '＋'] [#MulDivExpMod [#Id '送金額']]]]]]]] [#FDOutput [#Logical [#Equality [#Relational [#AddSub [#MulDivExpMod [#BT 'true']]]]]]]]]"

# print(debug(s6))
