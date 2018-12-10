import sys
from nico_ast import *
from nico_utils import *


def makePD(tree):
    ast = AST()
    ast.setTree(tree)
    tag = ast.get_tag()
    tag_exe(tag,ast)
    return ast

def Input(ast):
    tag = ast.get_tag()
    while(True):
        tag_exe(tag,ast)
        if ast.current()==']':break
        ast.pos+=1
        tag = ast.get_tag()

def StructDef(ast):
    #ast.struct[s_ほげげ] = ['v_ID','v_名前']
    tag = ast.get_tag()
    tag_exe(tag,ast)#SName
    sn = ast.temp
    ast.struct[sn] = []
    ast.temp_reset()
    ast.pos+=1
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)#SFactor
        ast.struct[sn].append(ast.temp)
        ast.temp_reset()
        if ast.current()==']':break
        ast.pos+=1

def SName(ast):
    ast.pos+=1
    t=''
    while(ast.current()!='\''):
        t+=ast.current()
        ast.pos+=1
    ast.temp='s_'+strToByte(t)
    ast.pos+=1

def SFactor(ast):
    tag = ast.get_tag()
    tag_exe(tag,ast)
    w = ast.temp
    ast.temp_reset()
    ast.pos+=1
    tag = ast.get_tag()
    tag_exe(tag,ast)
    t = ast.temp #str or list
    ast.temp = w
    #append to dict
    if isinstance(t,str):
        ast.words[w].append(t)
    else:
        ast.words[w].extend(t)

def Dict(ast):
    tag = ast.get_tag()
    tag_exe(tag,ast)
    w = ast.temp
    ast.temp_reset()
    ast.pos+=1
    tag = ast.get_tag()
    tag_exe(tag,ast)
    t = ast.temp #str or list
    #append to dict
    if isinstance(t,str):
        ast.words[w].append(t)
    else:
        ast.words[w].extend(t)

def Array(ast):
    at = []
    tag = ast.get_tag()
    tag_exe(tag,ast)
    t = ast.temp
    at.insert(0,t)
    ast.temp_reset()
    ast.pos+=1
    while(True):
        tag = ast.get_tag()
        tag_exe(tag,ast)
        t+='[]'
        at.insert(0,t)
        if ast.current() == ']':break
        ast.pos+=1
    ast.temp = at

def Map(ast):
    tlist = []
    mcount = 1
    tag = ast.get_tag()
    tag_exe(tag,ast)
    tlist.append(ast.temp)
    ast.temp_reset()
    while(ast.current() != ']'):
        ast.pos+=1
        mcount+=1
        tag = ast.get_tag()
        tag_exe(tag,ast)
        if isinstance(ast.temp,str):
            tlist.append(ast.temp)
            ast.temp_reset()
        elif isinstance(ast.temp,list):
            tlist.extend(ast.temp)
            ast.temp_reset()
    #tlist = ['address', 'address', 'int']
    #tlist = ['address', 'Voter']
    #tlist = ['address', 'int[]', 'int']
    for i in range(mcount-1):
        later = tlist[mcount-i-1]
        curr = tlist[mcount-2-i]
        tlist[mcount-2-i] = 'mapping('+ curr +'=>'+ later +')'
    ast.temp = tlist

def B(ast):
    ast.pos+=6

def W(ast):
    ast.pos+=1
    w = ''
    while(ast.current() != '\''):
        w+=ast.current()
        ast.pos+=1
    ast.temp = 'v_'+strToByte(w)
    ast.words[ast.temp] = [w]
    ast.pos+=1

def MW(ast):
    ast.pos+=1
    w = ''
    while(ast.current() != '\''):
        w+=ast.current()
        ast.pos+=1
    # w = '〜の投票者情報'
    mpl = mapTrim(w) #->['の投票者情報']
    map_name = 'map'+str(len(ast.map))
    ast.words[map_name] = [map_name]
    ast.pos+=1
    ast.map.append(mpl)
    ast.temp = map_name

def T(ast):
    ast.pos+=1
    t = ''
    while(ast.current() != '\''):
        t+=ast.current()
        ast.pos+=1
    if t == 'int':
        t = 'int256'
    ast.temp = t
    ast.pos+=1

def ST(ast):
    ast.pos+=1
    t = ''
    while(ast.current() != '\''):
        t+=ast.current()
        ast.pos+=1
    ast.temp = 's_'+strToByte(t)
    ast.pos+=1

def tag_exe(tag,ast):
    if tag[1:].startswith('Map'):
        Map(ast)
    else:
        globals()[tag[1:]](ast)
    ast.require(']')
    ast.pos+=1

s00 = "[#Input [#StructDef [#SName 'ほげほげ'] [#SFactor [#W 'ID'] [#T 'int']] [#SFactor [#W 'Name'] [#T 'string']]] [#Dict [#W 'メッセージ'] [#T 'string']] [#Dict [#W '数値'] [#T 'int']] [#Dict [#W 'チェック'] [#T 'bool']] [#Dict [#W '管理者'] [#T 'address']] [#Dict [#W 'Alice'] [#ST '生徒情報']] [#Dict [#W 'ナンバーズ'] [#Array [#T 'int'] [#B 'のリスト']]] [#Dict [#W '◯×テーブル'] [#Array [#T 'bool'] [#B 'のリスト'] [#B 'のリスト']]] [#Dict [#W 'クラス名簿'] [#Array [#ST '生徒情報'] [#B 'のリスト']]] [#Array [#T 'int'] [#B 'のリスト']]]]]"
s01 = "[#Input [#Dict [#W '〜の投票者情報'] [#Map [#T 'address'] [#ST '投票者情報']]] [#Dict [#W '〜が〜から動かせる金額'] [#Map [#T 'address'] [#T 'address'] [#T 'int']]] [#Dict [#W '〜の数字表'] [#Map [#T 'address']]]]"
s02 = "[#Input [#StructDef [#SName 'ほげほげ'] [#SFactor [#W 'ID'] [#T 'int']] [#SFactor [#W 'Name'] [#T 'string']]] [#Dict [#W 'メッセージ'] [#T 'string']] [#Dict [#W '数値'] [#T 'int']] [#Dict [#W 'チェック'] [#T 'bool']] [#Dict [#W '管理者'] [#T 'address']] [#Dict [#W 'Alice'] [#ST '生徒情報']] [#Dict [#W 'ナンバーズ'] [#Array [#T 'int'] [#B 'のリスト']]] [#Dict [#W '◯×テーブル'] [#Array [#T 'bool'] [#B 'のリスト'] [#B 'のリスト']]] [#Dict [#W 'クラス名簿'] [#Array [#ST '生徒情報'] [#B 'のリスト']]] [#Dict [#W '〜の投票者情報'] [#Map [#T 'address'] [#ST '投票者情報']]] [#Dict [#W '〜が〜から動かせる金額'] [#Map [#T 'address'] [#T 'address'] [#T 'int']]] [#Dict [#W '〜の数字表'] [#Map [#T 'address'] [#Array [#T 'int'] [#B 'のリスト']]]]]"

# ast = makePD(s02)
# print(ast.struct)

