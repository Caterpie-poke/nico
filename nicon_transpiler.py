import sys
from pegpy.peg import *
from pegpy.my_eval import *

def parseMain(src_path):
    g = Grammar('body')
    g.load('nicon_body.tpeg')
    parser = nez(g)
    with open(src_path,encoding='utf-8') as f:
        src = f.read()
        ast = repr(parser(src,None))
    return ast

def parseDict(dict_path):
    g = Grammar('dict')
    g.load('nicon-dict.tpeg')
    parser = nez(g)
    with open(dict_path,encoding='utf-8') as f:
        src = f.read()
        ast = repr(parser(src,None))
    return ast

def marge_peg_file():
    file1 = open('./hogege.txt','rb', encoding='utf-8')
    file2 = open('./hogegu.txt','rb', encoding='utf-8')
    peg1 = file1.read()
    peg2 = file2.read()
    return peg1+bytes(b'\n')+peg2

"""
def main():
    argv = sys.argv
    f_src = open(argv[1])
    str_src = f_src.read()
    (str_conf, str_body) = confAndBody(str_src) #str:all -> (str:conf, str:body)
    cd = parseConf(str_conf) #str:conf -> struct:ConfigData
    parseDict(cd) #dict_data, peg
    peg = already + generated
"""
"""
<usage>
$ python3 nicon_transpiler.py <input>.nico <input>.ncdc (<output>.sol)?
(must) 1st arg is main file
(must) 2nd arg is dict file
(arbit) 3rd arg is output file name
"""
#argv
src_path = './input2.txt'
dict_path = './input_dict.txt'
ast_dict = parseDict(dict_path)
(wd, peg) = makeDictPeg(ast_dict)
ast_main = parseMain(src_path, peg)
sol_code = transpile(ast_main,src_path,wd)
print(ast_main)
print(ast_dict)
print(sol_code)

d = {
    'var01':('aaa','string'),
    'var02':('list','int[]','int'),
    'var03':('map','mapping(address=>mapping(address=>int))','mapping(address=>int)','int')
}
print(len(d['var02']))