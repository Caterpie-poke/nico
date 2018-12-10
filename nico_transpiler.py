import sys
import subprocess
from pegpy.peg import *
from nico_body_process import *
from nico_dict_process import *
from nico_ast import *


def parseMain(tpegPath, src_path):
    g = Grammar('contract')
    g.load(tpegPath)
    parser = nez(g)
    with open(src_path,encoding='utf-8') as f:
        src = f.read()
        ast = repr(parser(src))
    return ast

def parseDict(tpegPath, dict_path):
    g = Grammar('dictionary')
    g.load(tpegPath)
    parser = nez(g)
    with open(dict_path,encoding='utf-8') as f:
        src = f.read()
        ast = repr(parser(src))
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

<usage>
$ python3 nicon_transpiler.py <input>.nico <input>.ncdc (<output>.sol)?
(must) 1st arg is main file
(must) 2nd arg is dict file
(arbit) 3rd arg is output file name
"""

def all_test(mp, dp, gp):
    #Arguments
    main_path = mp
    dict_path = dp
    gen_path  = gp
    #Constant
    main_tpeg_path = './pegpy/grammar/nico_cont.tpeg'
    dict_tpeg_path = './pegpy/grammar/nico_dict.tpeg'

    print('-------------------- NicoDictionary\'s AST --------------------')
    dict_tree = parseDict(dict_tpeg_path, dict_path)
    print(dict_tree + '\n')

    print('-------------------- ExternalPEG from dict_tree --------------------')
    ast = makePD(dict_tree)
    externalPEG = ast.additionalPEG()
    print(externalPEG + '\n')

    print('-------------------- NicoContract\'s AST --------------------')
    complete_tpeg_path = './pegpy/grammar/nico_merge.tpeg'
    f1 = open(main_tpeg_path, mode='r', encoding='utf-8')
    front = f1.read()
    f2 = open(complete_tpeg_path, mode='w', encoding='utf-8')
    f2.write(front+externalPEG)
    f1.close()
    f2.close()

    main_tree = parseMain(complete_tpeg_path, main_path)
    print(main_tree + '\n')

    print('-------------------- Solidity Output --------------------')
    solCode = transpile(ast,main_tree)
    print(solCode + '\n')
    fsol = open(gen_path, mode='w', encoding='utf-8')
    fsol.write(solCode)
    fsol.close()


def command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                universal_newlines=True)
        for line in result.stdout.splitlines():
            yield line
    except subprocess.CalledProcessError:
        print('外部プログラムの実行に失敗しました [' + cmd + ']', file=sys.stderr)
        sys.exit(1)

def mainParserTest(mp,dp):
    main_path = mp
    dict_path = dp
    main_tpeg_path = './pegpy/grammar/nico_cont.tpeg'
    dict_tpeg_path = './pegpy/grammar/nico_dict.tpeg'

    print('-------------------- NicoDictionary\'s AST --------------------')
    dict_tree = parseDict(dict_tpeg_path, dict_path)
    print(dict_tree + '\n')

    print('-------------------- ExternalPEG from dict_tree --------------------')
    ast = makePD(dict_tree)
    externalPEG = ast.additionalPEG()
    print(externalPEG + '\n')

    print('-------------------- NicoContract\'s AST --------------------')
    complete_tpeg_path = './pegpy/grammar/nico_parserTest.tpeg'
    f1 = open(main_tpeg_path, mode='r', encoding='utf-8')
    front = f1.read()
    f2 = open(complete_tpeg_path, mode='w', encoding='utf-8')
    f2.write(front+externalPEG)
    f1.close()
    f2.close()

    main_tree = parseMain(complete_tpeg_path, main_path)
    print(main_tree + '\n')


# 使用例
"""
cmd = 'solc ./hoge.sol'
returncode = subprocess.call(cmd.split())
print(returncode)
"""

mp = './input3.nc'
dp = './input_dict.nd'
gp  = './output.sol'

# all_test(mp,dp,gp)
mainParserTest("input4.nc",dp)