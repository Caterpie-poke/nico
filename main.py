import sys
import subprocess
from pegpy.peg import *
from nico_body_process2 import *
from nico_dict_process2 import *
from nico_ast2 import *


def parseCont(tpegPath, src_path):
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

def transpile(nc,nd,sn):
    cont_tpeg_path = './pegpy/grammar/nico_cont.tpeg'
    dict_tpeg_path = './pegpy/grammar/nico_dict.tpeg'
    merge_tpeg_path = './pegpy/grammar/nico_merge.tpeg'

    dict_tree = parseDict(dict_tpeg_path, nd)
    (ast, ext_tpeg) = makePD(dict_tree)

    with open(cont_tpeg_path, mode='r', encoding='utf-8') as f1:
        with open(merge_tpeg_path, mode='w', encoding='utf-8') as f2:
            base_tpeg = f1.read()
            f2.write(base_tpeg + ext_tpeg)

    main_tree = parseCont(merge_tpeg_path, nc)
    sol_code = makeSOL(ast, main_tree)

    with open(sn, mode='w', encoding='utf-8') as f3:
        f3.write(sol_code)

def main():
    try:
        # argv = sys.argv
        argv = ['main', 'tests/input4.nc', 'tests/input_dict.nd', 'tests/hoge.sol']
        if len(argv) < 3:
            raise Exception()
        nc = argv[1]
        nd = argv[2]
        if len(argv) > 3:
            sn = argv[3]
        else:
            sn = nc.replace('.nc', '.sol')
        transpile(nc,nd,sn)
    except Exception:
        print("Specify 2 or 3 arguments")
        print("  first  : nico_contract filePath")
        print("  second : nico_dictionary filePath")
        print("  third  : output filePath (OPTIONAL)")
        print()

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
    (ast, externalPEG) = makePD(dict_tree)
    print(externalPEG + '\n')

    print('-------------------- NicoContract\'s AST --------------------')
    complete_tpeg_path = './pegpy/grammar/nico_merge.tpeg'
    with open(main_tpeg_path, mode='r', encoding='utf-8') as f1:
        with open(complete_tpeg_path, mode='w', encoding='utf-8') as f2:
            front = f1.read()
            f2.write(front+externalPEG)

    main_tree = parseCont(complete_tpeg_path, main_path)
    print(main_tree + '\n')

    print('-------------------- Solidity Output --------------------')
    solCode = makeSOL(ast,main_tree)
    print(solCode + '\n')
    with open(gen_path, mode='w', encoding='utf-8') as fsol:
        fsol.write(solCode)

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


mp = 'tests/input4.nc'
dp = 'tests/input_dict.nd'
gp  = 'tests/output.sol'

# all_test(mp,dp,gp)
main()