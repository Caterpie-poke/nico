import sys
from nico_ast import *
from nico_utils import *

def makePD(tree):
    ast = AST()
    ast.setTree(tree)
    (none,tag) = getNode(ast)
    return ast

def Input(ast):
    ast.back()
    while(ast.current()==' '):
        ast.next()
        (df,tag) = getNode(ast)
    return

def StructDef(ast):
    pass

def SName(ast):
    pass

def SFactor(ast):
    pass

def Dict(ast):
    pass

def Array(ast):
    code = ''
    count = 0
    (aname,tag) = getNode(ast)
    while(ast.current()==' '):
        ast.next()
        (none,tag) = getNode(ast)
        count+=1
    for i in range(count):
        count

def Map(ast):
    pass

def B(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return '[]'

def W(ast):
    pass

def MW(ast):
    pass

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
    return st

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


s00 = "[#Input [#StructDef [#SName 'ほげほげ'] [#SFactor [#W 'ID'] [#T 'int']] [#SFactor [#W 'Name'] [#T 'string']]] [#Dict [#W 'メッセージ'] [#T 'string']] [#Dict [#W '数値'] [#T 'int']] [#Dict [#W 'チェック'] [#T 'bool']] [#Dict [#W '管理者'] [#T 'address']] [#Dict [#W 'Alice'] [#ST '生徒情報']] [#Dict [#W 'ナンバーズ'] [#Array [#T 'int'] [#B 'のリスト']]] [#Dict [#W '◯×テーブル'] [#Array [#T 'bool'] [#B 'のリスト'] [#B 'のリスト']]] [#Dict [#W 'クラス名簿'] [#Array [#ST '生徒情報'] [#B 'のリスト']]] [#Array [#T 'int'] [#B 'のリスト']]]]]"
s01 = "[#Input [#Dict [#W '〜の投票者情報'] [#Map [#T 'address'] [#ST '投票者情報']]] [#Dict [#W '〜が〜から動かせる金額'] [#Map [#T 'address'] [#T 'address'] [#T 'int']]] [#Dict [#W '〜の数字表'] [#Map [#T 'address']]]]"
s02 = "[#Input [#StructDef [#SName 'ほげほげ'] [#SFactor [#W 'ID'] [#T 'int']] [#SFactor [#W 'Name'] [#T 'string']]] [#Dict [#W 'メッセージ'] [#T 'string']] [#Dict [#W '数値'] [#T 'int']] [#Dict [#W 'チェック'] [#T 'bool']] [#Dict [#W '管理者'] [#T 'address']] [#Dict [#W 'Alice'] [#ST '生徒情報']] [#Dict [#W 'ナンバーズ'] [#Array [#T 'int'] [#B 'のリスト']]] [#Dict [#W '◯×テーブル'] [#Array [#T 'bool'] [#B 'のリスト'] [#B 'のリスト']]] [#Dict [#W 'クラス名簿'] [#Array [#ST '生徒情報'] [#B 'のリスト']]] [#Dict [#W '〜の投票者情報'] [#Map [#T 'address'] [#ST '投票者情報']]] [#Dict [#W '〜が〜から動かせる金額'] [#Map [#T 'address'] [#T 'address'] [#T 'int']]] [#Dict [#W '〜の数字表'] [#Map [#T 'address'] [#Array [#T 'int'] [#B 'のリスト']]]]]"

# ast = makePD(s02)
# print(ast.struct)

