import sys
from nico_ast2 import *
from nico_utils import *

def makePD(tree):
    ast = AST()
    ast.setTree(tree)
    (none,tag) = getNode(ast)
    return ast, ast.additionalPEG()

def Input(ast):
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (df,tag) = getNode(ast)
    return 'success'

def StructDef(ast):
    fcts = []
    (sname,tag) = getNode(ast)
    while(ast.current()==' '):
        ast.next()
        (fct,tag) = getNode(ast)
        fcts.append(fct)
    ast.struct[sname] = []
    for f in fcts:
        ast.struct[sname].append(f)

def SName(ast):
    sn = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        sn+=ast.current()
        ast.next()
    ast.next()
    return strToByte(sn)

def Dict(ast):
    (w,tag) = getNode(ast)
    ast.next()
    (t,tag) = getNode(ast)
    if isinstance(t,str):
        ast.words[w].append(t)
    elif isinstance(t,list):
        ast.words[w].extend(t)
    else:
        print(str(w) + ' is not str or list')
        sys.exit()
    return w

def Array(ast):
    #return ['int[][]', 'int[]', 'int']2
    count = 0
    ats = []
    (at,tag) = getNode(ast)
    while(ast.current()==' '):
        ast.next()
        (none,tag) = getNode(ast)
        count+=1
    for i in range(count):
        br = '[]'*(count-i)
        ats.append(at+br)
    ats.append(at)
    return ats

def Map(ast):
    tlist = []
    ast.back()
    n = 0
    while(ast.current()==' '):
        n+=1
        ast.next()
        (t,tag) = getNode(ast)
        if isinstance(t,str):
            tlist.append(t)
        elif isinstance(t,list):
            tlist.extend(t)
        else:
            print(str(t) + ' :Map Err')
            sys.exit()
    for i in range(n-1):
        later = tlist[n-i-1]
        curr = tlist[n-2-i]
        tlist[n-2-i] = 'mapping('+ curr +'=>'+ later +')'
    return tlist

def B(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return '[]'

def W(ast):
    w = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        w+=ast.current()
        ast.next()
    ast.next()
    bw = 'v_'+strToByte(w)
    ast.words[bw] = [w]
    return bw

def MW(ast):
    mw = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        mw+=ast.current()
        ast.next()
    ast.next()
    mw = mapTrim(mw)
    mn = 'map' + str(len(ast.map))
    ast.words[mn] = [mn]
    ast.map.append(mw)
    return mn

def T(ast):
    tp = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        tp+=ast.current()
        ast.next()
    ast.next()
    if tp == 'int':
        tp = 'int256'
    return tp

def ST(ast):
    st = ''
    ast.requireNext('\'')
    while(ast.current()!='\''):
        st+=ast.current()
        ast.next()
    ast.next()
    return 's_'+strToByte(st)

def getNode(ast):
    tag = ''
    ast.requireNext('[')
    ast.next()
    while(ast.current() != ' '):
        tag += ast.current()
        ast.next()
    ast.next()
    if tag.startswith('Map'):
        inner = Map(ast)
        tag = 'Map'
    else:
        inner = globals()[tag](ast)
    ast.requireNext(']')
    return (inner,tag)


s00 = "[#Input [#StructDef [#SName 'ほげほげ'] [#Dict [#W 'ID'] [#T 'int']] [#Dict [#W 'Name'] [#T 'string']]] [#Dict [#W 'メッセージ'] [#T 'string']] [#Dict [#W '数値'] [#T 'int']] [#Dict [#W 'チェック'] [#T 'bool']] [#Dict [#W '管理者'] [#T 'address']] [#Dict [#W 'Alice'] [#ST '生徒情報']] [#Dict [#W 'ナンバーズ'] [#Array [#T 'int'] [#B 'のリスト']]] [#Dict [#W '◯×テーブル'] [#Array [#T 'bool'] [#B 'のリスト'] [#B 'のリスト']]] [#Dict [#W 'クラス名簿'] [#Array [#ST '生徒情報'] [#B 'のリスト']]] [#Array [#T 'int'] [#B 'のリスト']]]]]"
s01 = "[#Input [#Dict [#W '〜の投票者情報'] [#Map [#T 'address'] [#ST '投票者情報']]] [#Dict [#W '〜が〜から動かせる金額'] [#Map [#T 'address'] [#T 'address'] [#T 'int']]] [#Dict [#W '〜の数字表'] [#Map [#T 'address']]]]"
s02 = "[#Input [#StructDef [#SName 'ほげほげ'] [#Dict [#W 'ID'] [#T 'int']] [#Dict [#W 'Name'] [#T 'string']]] [#Dict [#W 'メッセージ'] [#T 'string']] [#Dict [#W '数値'] [#T 'int']] [#Dict [#W 'チェック'] [#T 'bool']] [#Dict [#W '管理者'] [#T 'address']] [#Dict [#W 'Alice'] [#ST '生徒情報']] [#Dict [#W 'ナンバーズ'] [#Array [#T 'int'] [#B 'のリスト']]] [#Dict [#W '◯×テーブル'] [#Array [#T 'bool'] [#B 'のリスト'] [#B 'のリスト']]] [#Dict [#W 'クラス名簿'] [#Array [#ST '生徒情報'] [#B 'のリスト']]] [#Dict [#MW '〜の投票者情報'] [#Map [#T 'address'] [#ST '投票者情報']]] [#Dict [#MW '〜が〜から動かせる金額'] [#Map [#T 'address'] [#T 'address'] [#T 'int']]] [#Dict [#MW '〜の数字表'] [#Map [#T 'address'] [#Array [#T 'int'] [#B 'のリスト']]]]]"

"""
ast = makePD(s02)
print(ast.string+'\n')
print(str(ast.struct)+'\n')
print(str(ast.words)+'\n')
print(str(ast.map))
"""
