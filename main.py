import sys
import subprocess
from pegpy.peg import *
from nico_body_process2 import *
from nico_dict_process2 import *
from nico_ast2 import *

def parse(tpeg, src_path):
    g = Grammar(tpeg)
    g.load(tpeg)
    parser = nez(g)
    with open(src_path,encoding='utf-8') as f:
        src = f.read()
        tree = repr(parser(src))
    return tree

def transpile(nc_path, nd_path, sol_path):
    nc_tpeg = './pegpy/grammar/nico_cont_tab2.tpeg'
    nd_tpeg = './pegpy/grammar/nico_dict.tpeg'
    merge_tpeg = './pegpy/grammar/nico_merge.tpeg'
    dict_tree = parse(nd_tpeg, nd_path)
    (ast, ext_tpeg) = makePD(dict_tree)
    with open(nc_tpeg, mode='r', encoding='utf-8') as f1:
        with open(merge_tpeg, mode='w', encoding='utf-8') as f2:
            base_tpeg = f1.read()
            f2.write(base_tpeg + ext_tpeg)
    main_tree = parse(merge_tpeg, nc_path)
    sol_code = makeSOL(ast, main_tree)
    with open(sol_path, mode='w', encoding='utf-8') as f3:
        f3.write(sol_code)

def main():
    argv = sys.argv
    if len(argv) != 3:
        print("Please Specify 2 arguments")
        print("  1st : nico_contract   file_path")
        print("  2nd : nico_dictionary file_path\n")
        sys.exit()
    nc_path = argv[1]
    nd_path = argv[2]
    sol_path = nc_path.replace('.nc', '.sol')
    transpile(nc_path, nd_path, sol_path)

if __name__ == "__main__":
    pass
    # main()

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

# -------------------- Test Code --------------------
def all_test(nc_path, nd_path):
    sol_path  = nc_path.replace('.nc', '.sol')
    nc_tpeg = './pegpy/grammar/nico_cont_tab2.tpeg'
    nd_tpeg = './pegpy/grammar/nico_dict.tpeg'

    print('-------------------- NicoDictionary\'s AST --------------------')
    dict_tree = parse(nd_tpeg, nd_path)
    print(dict_tree, '\n')

    print('-------------------- ExternalPEG from dict_tree --------------------')
    (ast, externalPEG) = makePD(dict_tree)
    print(externalPEG, '\n')

    print('-------------------- AST check --------------------')
    print('----- struct -------\n', ast.struct)
    print('----- words --------\n', ast.words)
    print('----- stvar --------\n', ast.stvar)
    print('----- reserved -----\n', ast.reserved)
    print('----- map ----------\n', ast.map, '\n')

    print('-------------------- NicoContract\'s AST --------------------')
    merged_tpeg = './pegpy/grammar/nico_merge.tpeg'
    with open(nc_tpeg, mode='r', encoding='utf-8') as f1:
        with open(merged_tpeg, mode='w', encoding='utf-8') as f2:
            front = f1.read()
            f2.write(front+externalPEG)
    main_tree = parse(merged_tpeg, nc_path)
    print(main_tree, '\n')

    print('-------------------- Solidity Output --------------------')
    solCode = makeSOL(ast,main_tree)
    print(solCode, '\n')
    with open(sol_path, mode='w', encoding='utf-8') as fsol:
        fsol.write(solCode)

nc = 'sample_eval/trade_erc.nc'
nd = 'sample_eval/sample.nd'

# all_test(nc,nd)