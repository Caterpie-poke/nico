#!/usr/local/bin/python
import sys, time #,readline*
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pegpy.peg import *
from pegpy.gparser.gnez import nnez
import pegpy.utils as u
from pegpy.my_eval import *

def bold(s):
    return '\033[1m' + str(s) + '\033[0m'

def read_inputs(a):
    try:
        f = open(a, 'rb')
        data = f.read()
        f.close()
        return data
    except:
        return a.encode()

def readlines(prompt):
    s = input(prompt)
    if s != '':
        return s
    else:
        l = []
        while True:
            prev = s
            s = input()
            l.append(s)
            if prev == '' and s == '':
                break
        return '\n'.join(l)

def load_grammar(opt, default = None):
    file = default if not 'grammar' in opt else opt['grammar']
    #file = 'hoge.tpeg'
    if file is None:
        raise CommandError(opt)
    g = Grammar(file)
    g.load(u.find_path(file))
    return g

def switch_generator(opt, default = 'math.tpeg'):
    file = default if not 'grammar' in opt else opt['grammar']
    if file.endswith('.gpeg'):
        return nnez
    return nez

def parse(opt, conv=None):
    g = load_grammar(opt)
    #g = Grammar(hoge).load('hoge.tpeg')
    parser = switch_generator(opt)(g)
    #parser = nez(g)
    inputs = opt['inputs']
    if len(inputs) == 0:
        try:
            while True:
                s = readlines(bold('>>> '))
                print(repr(parser(s, conv)))
        except EOFError:
            pass
    elif len(inputs) == 1:
        print(repr(parser(read_inputs(inputs[0]), conv)))
    else:
        for file in opt['inputs']:
            st = time.time()
            t = parser(read_inputs(file))
            et = time.time()
            print(file, str((et - st) * 1000.0) + "[ms]: ", t.tag)

def json(opt):
    parse(opt, lambda t: t.asJSON())

def example(opt):
    g = load_grammar(opt)
    g.testAll()

def peg(opt):
    g = load_grammar(opt)
    print(g)

def origami(opt):
    from pegpy.origami.origami import transpile
    g = load_grammar(opt, 'konoha6.tpeg')
    parser = switch_generator(opt, 'konoha6.tpeg')(g)
    origami_files = [f for f in opt['inputs'] if f.endswith('.origami')]
    source_files = [f for f in opt['inputs'] if not f.endswith('.origami')]
    if len(source_files) == 0:
        try:
            while True:
                s = readlines(bold('>>> '))
                t = parser(s)
                print(repr(t))
                print(repr(transpile(t, origami_files)))
        except EOFError:
            pass
    else :
        for input in source_files:
            t = parser(read_inputs(input))
            print(repr(transpile(t, origami_files)))

def nezcc(opt):
    pass

def bench(opt):
    pass

def exe(opt, conv=None):
    # g = load_grammar(opt)
    g = Grammar('nicon')
    g.load('nicon_body.tpeg')
    # parser = switch_generator(opt)(g)
    parser = nez(g)
    inputs = opt['inputs']
    if len(inputs) == 0:
        try:
            while True:
                s = readlines(bold('>>> '))
                ast = repr(parser(s, conv))
                print(ast + '\n')
                output = transpile(ast)
                print(output)
        except EOFError:
            pass
    elif len(inputs) == 1:
        ast = repr(parser(read_inputs(inputs[0]), conv))
        print(ast + '\n')
        print(transpile(ast))
    else:
        for file in opt['inputs']:
            st = time.time()
            t = parser(read_inputs(file))
            et = time.time()
            print(file, str((et - st) * 1000.0) + "[ms]: ", t.tag)

def parse_opt(argv):
    def parse_each(a, d):
        if a[0].startswith('-'):
            if len(a) > 1:
                if a[0] == '-g':
                    d['grammar'] = a[1]
                    return a[2:]
                elif a[0] == '-s':
                    d['start'] = a[1]
                    return a[2:]
                elif a[0] == '-X':
                    d['extension'] = a[1]
                    return a[2:]
                elif a[0] == '-D':
                    d['option'] = a[1]
                    return a[2:]
            d['inputs'].extend(a)
            raise CommandError(d)
        else:
            d['inputs'].append(a[0])
            return a[1:]
    d  = {'inputs': []}
    while len(argv) > 0:
        argv = parse_each(argv, d)
    return d

def version():
    print(bold('PEGPY - A PEG-based Parsering Tools for Python'))

def usage(opt):
    print("Usage: pegpy <command> options inputs");
    print("  -g | --grammar <file>      specify a grammar file");
    print("  -s | --start <NAME>        specify a starting rule");
    print("  -D                         specify an optional value");
    print()

    print("Example:");
    print("  pegpy parse -g math.tpeg <inputs>");
    print("  pegpy json -g math.tpeg <inputs>");
    print("  pegpy origami -g konoha6.tpeg common.origami <inputs>")
    print();

    print("The most commonly used nez commands are:");
    print(" parse      run an interactive parser");
    print(" nezcc      generate a cross-language parser");
    print(" origami    transpiler")
    print(" bench      the bench mark")
    print(" json       output tree as json file")

class CommandError(Exception):
    def __init__(self, opt):
        self.opt = opt

def main():
    try:
        argv = sys.argv
        #['parse' '-g', 'hoge.tpeg', 'file.txt']
        if len(argv) < 2:
            raise CommandError({})
        cmd = argv[1]
        d = parse_opt(argv[2:])
        #d = {'inputs':'file.txt', 'grammar':'hoge.tpeg'}
        names = globals()
        if cmd in names:
            names[cmd](d)
            #parse(d)
        else:
            raise CommandError(d)
    except CommandError as e:
        usage(e.opt)

if __name__ == "__main__":
    main()

'''
  st = time.time()
  t = parse(s, len(s)-1, newAST, subAST)
  et = time.time()
  sys.stderr.write(a + " " + str((et-st) * 1000.0) + "[ms]: ")
  sys.stderr.flush()
  sys.stdout.write(str(t))
  sys.stdout.flush()
  sys.stderr.write('\n')
'''