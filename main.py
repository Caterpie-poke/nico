import sys
import subprocess
from pegpy.peg import *
from nico_body_process import *
from nico_dict_process import *
from nico_ast import *

def parse(tpeg, src_path):
    g = Grammar(tpeg)
    g.load(tpeg)
    parser = nez(g)
    with open(src_path,encoding='utf-8') as f:
        src = f.read()
        tree = repr(parser(src))
    return tree

def parse2(tpeg, src_txt):
    g = Grammar(tpeg)
    g.load(tpeg)
    parser = nez(g)
    tree = repr(parser(src_txt))
    return tree

def transpile(src_path, sol_path):
    nc_tpeg = './pegpy/grammar/nico_cont.tpeg'
    nd_tpeg = './pegpy/grammar/nico_dict.tpeg'
    merge_tpeg = './pegpy/grammar/nico_merge.tpeg'
    dict_tree = parse(nd_tpeg, src_path)
    (ast, ext_tpeg) = makePD(dict_tree)
    with open(nc_tpeg, mode='r', encoding='utf-8') as f1:
        with open(merge_tpeg, mode='w', encoding='utf-8') as f2:
            base_tpeg = f1.read()
            f2.write(base_tpeg + ext_tpeg)
    main_tree = parse(merge_tpeg, src_path)
    sol_code = makeSOL(ast, main_tree)
    with open(sol_path, mode='w', encoding='utf-8') as f3:
        f3.write(sol_code)

def main():
    argv = sys.argv
    if len(argv) < 2 or not argv[1].endswith('.nc'):
        print("Please Specify Nico Contract File")
        print("usage: python3 main.py <contract>.nc\n")
        sys.exit()
    nc_path = argv[1]
    sol_path = nc_path[:-3]+'.sol'
    transpile(nc_path, sol_path)

if __name__ == "__main__":
    # main()
    pass

# Future Work: Combine Nico with Solidity Compiler
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
