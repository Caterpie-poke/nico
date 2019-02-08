import sys

safeMath = '\
library SafeMath {\n\
    function mul(int256 a, int256 b) internal pure returns(int256){\n\
        if (a == 0) {\n\
            return 0;\n\
        }\n\
        int256 c = a * b;\n\
        require(c / a == b, \'Mul Err\');\n\
        return c;\n\
    }\n\
    function div(int256 a, int256 b) internal pure returns(int256){\n\
        require(b != 0, \'Div Err\');\n\
        int256 c = a / b;\n\
        return c;\n\
    }\n\
    function sub(int256 a, int256 b) internal pure returns(int256){\n\
        int256 c = a - b;\n\
        if(b >= 0){\n\
            require(c <= a, \'Sub Err\');\n\
        } else {\n\
            require(c > a, \'Sub Err\');\n\
        }\n\
        return c;\n\
    }\n\
    function add(int256 a, int256 b) internal pure returns(int256){\n\
        int256 c = a + b;\n\
        if(b >= 0){\n\
            require(c >= a, \'Add Err\');\n\
        } else {\n\
            require(c < a, \'Add Err\');\n\
        }\n\
        return c;\n\
    }\n\
    function mod(int256 a, int256 b) internal pure returns(int256){\n\
        require(b != 0, \'Mod Err\');\n\
        return a % b;\n\
    }\n\
    function exp(int256 a, int256 b) internal pure returns(int256){\n\
        require(b >= 0, \'Exp Err\');\n\
        int256 c = 1;\n\
        for(int256 i = 0 ; i < b ; i++){\n\
            c = mul(c, a);\n\
        }\n\
        return c;\n\
    }\n\
}\n\n'

def mapTrim(word):
    word = rmBracket(word)
    word = word.replace('X','〜').replace('Y','〜').replace('Z','〜')
    if word[0] == '〜':word=word[1:]
    return word.split('〜')

def rmBracket(word):
    w = ''
    ps = False
    for c in word:
        if (c=='(' or c=='（') and (not ps):
            ps = True
        elif (c==')' or c=='）') and ps:
            ps = False
            w+='〜'
        elif (c=='(' or c=='（') and ps:
            print('Bracket in Bracket is disallowed')
            sys.exit()
        elif (c==')' or c=='）') and (not ps):
            print('Not find Bracket left')
            sys.exit()
        elif ps:
            continue
        else:
            w+=c
    return w

def toMapStr(l):
    if len(l) == 1:
        return str(l[0])
    elif len(l) >= 2:
        left = str(l[0])
        right = toMapStr(l[1:])
        return 'mapping('+left+'->'+right+')'
    else:
        print('Map component should be more than 1')
        sys.exit()

def err(ast):
    ast.requireNext('\'')
    while(ast.current()!='\''):
        ast.next()
    ast.next()
    return 'AST ERROR'

def charToByte(c):
    return format(ord(c), '04x')
def strToByte(s):
    hex_str = ""
    for c in s:
        hex_str+=charToByte(c)
    return hex_str
    # return s

