import sys

class AST:
    __slots__ = ['string','pos','version','precode','struct','enum','words','stvar','reserved','map','addrCheck','indentLevel','funcInfo', 'imported', 'doxygen']
    def __init__(self):
        self.string = ''
        self.pos = 0
        self.version = '0.4.24'
        self.precode = ''
        self.struct = {}
        self.enum = []
        self.words = {}
        self.stvar = []
        self.reserved = {
            '当事者':['msg.sender', 'address'],
            '今':['int256(now)', 'int256'],
            'true':['true', 'bool'],
            'false':['false', 'bool'],
            '本契約':['address(this)', 'address'],
            '受け取ったETH':['int256(msg.value)', 'int256'],
            '販売中':['Enum0.v_8ca958f24e2d', 'Enum0'],
            '販売休止':['Enum0.v_8ca958f24f116b62', 'Enum0']
        }
        self.map = []
        self.addrCheck = ''
        self.indentLevel = 0
        self.funcInfo = {'A':'public ', 'B':'view ', 'C':''}
        self.imported = False
        self.doxygen = []
    def setTree(self,tree):
        self.string = tree
        self.pos = 0
        self.indentLevel = 0
    def funcInfoReset(self):
        self.funcInfo = {'A':'public ', 'B':'view ', 'C':''}
    def doxygenReset(self):
        self.doxygen = []
    def notView(self):
        if(self.funcInfo['B'] == 'view '):
            self.funcInfo['B'] = ''
    def getFuncInfo(self):
        return self.funcInfo['A'] + self.funcInfo['B'] + self.funcInfo['C']
    # def require(self,ch):
    #     if self.current() != ch:
    #         print('pos:'+str(self.pos)+' require "'+ch+'", but found "'+self.current()+'"')
    #         sys.exit()
    def requireNext(self,ch):
        if self.current() != ch:
            print('pos:'+str(self.pos)+' require "'+ch+'", but found "'+self.current()+'"')
            sys.exit()
        self.next()
    def current(self):
        return self.string[self.pos]
    def next(self):
        self.pos+=1
    def back(self):
        self.pos-=1
    def toString(self):
        sss = ""
        tab = 0
        for c in self.string:
            if c=='[':
                sss+=('\n'+('    '*tab)+c)
                tab+=1
            elif c==']':
                tab-=1
                sss+=('\n'+('    '*tab)+c)
            else:
                sss+=c
        return sss[1:]
    def incIndent(self):
        self.indentLevel+=1
    def decIndent(self):
        self.indentLevel-=1
    def Indent(self):
        return '    '*self.indentLevel
    def withType(self,word,mdf):
        typ = self.typeDetect(word,0)
        if(typ in ['uint256','int256','address', 'bool'] and mdf == 'memory'):
            mdf = ''
        return typ + ' ' + mdf + (' '*(mdf!='')) + word
    def typeDetect(self,w,count):
        #w = 'owner'
        #w = 'map02[hogege]'
        #w = 'map02'
        #w = 'numbers[index][i2][i3]'
        #w = 'data.param'
        #w = 'int256(123)'
        #w = 'map3[msg.sender]'
        if w in self.words:
            return self.words[w][count+1]
        elif w.rfind('[') > 0:
            return self.typeDetect(w[:w.rfind('[')],count+1)
        elif w.rfind('.') > 0:
            return self.typeDetect(w[w.rfind('.')+1:],0)
        elif w.startswith('int('):
            return 'int256'
        elif w.startswith('"') and w.endswith('"'):
            return 'string'
        else:
            print('Not find '+w+' in dict');
            sys.exit()
            return 'Unknown'
    """
    def recovery(s):
        if(s in self.words):
            return self.words[s][0]
        else:
            point = min(s.find('.'),s.find('['))
            left = self.words[s[:point]]
            if(s[point]=='.'):
                return left+'の'+self.recovery(s[point+1:])
            elif(s[point]=='['):
    """
    def isStateVar(self,w):
        if w.find('.') > 0:
            return self.isStateVar(w[:w.find('.')])
        elif w.find('[') > 0:
            return self.isStateVar(w[:w.find('[')])
        else:
            return w in self.stvar
    def structDefWrite(self,key):
        st = ''
        st+=('struct ' + key + ' {')
        for p in self.struct[key]:
            st+=(self.withType(p,'')+';')
        st+='}'
        return st
    def reservedToWords(self):
        for k in self.reserved:
            key = self.reserved[k][0]
            self.words[key] = [k]
            self.words[key].extend(self.reserved[k][1:])
    def wordsToPEG(self):
        word_list = []
        for k in self.words:
            word_list.append(self.words[k][0])
        for r in self.reserved:
            word_list.append(r)
        word_list.sort(key=len)
        word_list.reverse()
        fromdict = 'FromDict\n    = '
        count=0
        for w in word_list:
            if count!=0:
                fromdict+='    / '
            fromdict+=('\''+w+'\''+'\n')
            count+=1
        return fromdict
    def mapToPEG(self):
        mapref = 'MapRef\n    = '
        mapdecl = 'MapDecl\n    = '
        count = 0
        for l in self.map:
            single_mapref = '{'
            single_mapdecl = '{'
            for p in l:
                single_mapref+=('$PrimaryExpr '+'\''+p+'\' ')
                single_mapdecl+=('MapParam '+'\''+p+'\' ')
            single_mapref += ('#Map'+str(count)+'}')
            single_mapdecl += ('#DMap'+str(count)+'}')
            if count != 0:
                mapref+='    / '
                mapdecl+='    / '
            mapref+=single_mapref+'\n'
            mapdecl+=single_mapdecl+'\n'
            count+=1
        return mapref+'\n'+mapdecl
    def additionalPEG(self):
        return self.mapToPEG()+'\n'+self.wordsToPEG()

"""---------- ASTの要素 ----------
# string
パース結果のASTを保持する文字列
最初はndのASTを受け取って、ncのASTで上書きされる

# pos
上記stringを読み進めた位置を保持する数値
ncの処理前に初期化

# struct
ndの処理を通して構造体を記録する辞書
key   : structの名前、バイト文字
value : 要素名のバイト文字の配列
ex) struct['s_ログデータ'] = ['v_名前', '価格', '販売中']

# words
ndの処理を通して名詞を記録する辞書
key   : 単語名、バイト文字
value : 文字列の配列、0番目は変換前の文字列、1番目以降は型名、複合型の場合は1ステップずつ評価した型も追加
ex) words['対象者'] = ['対象者', 'address']
ex) words['msg.sender'] = ['あなた', 'address']
ex) words['v_テーブル'] = ['テーブル', 'bool[][]', 'bool[]', 'bool']
ex) words['map0'] = ['map0', 'mapping(address=>int)', 'int']

# stvar
ncのVDeclで状態変数を記録する文字列の配列
Assignの左辺がstvarに存在する場合にviewを外す
ex) stvar = ['v_オーナー', 'v_総発行量', 'map1']

# reserved
予約語を記録する辞書
key   : 予約語にあたる日本語、変換しない
value : 変換される特有の文字列と型の文字列配列
ex) reserved['あなた'] = ['msg.sender', 'address']

# map
mapを記録する文字列の動的2次元配列、配列長=総map数
index : mappingの識別番号
value : 〜で分割した文字列の配列
これを用いてPEGを書き足す
ex) map[0] = ['の残高']
ex) map[1] = ['から', 'が動かせる金額']

# indentLevel
コード生成用のインデントレベルを保持する数値

# funcInfo
関数の情報を保持する辞書
keyはABCの3種類
A -> publicかどうか、現状はpublic固定
B -> viewかどうか、初期値がviewで状態変数への代入やSolidity埋め込みや関数呼び出しがあれば空文字に上書き
C -> returnの有無、return文があれば返される変数の型を追加する
関数定義に入ったらまず初期化、コード生成時に呼び出す
"""