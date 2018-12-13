import sys

class AST:
    __slots__ = ['string','pos','output','struct','words','stvar','reserved','map','indentLevel','temp','write_to_temp','funcInfo']
    def __init__(self):
        self.string = ''
        self.pos = 0
        self.output = ''
        self.struct = {}
        self.words = {
            'true':['built-in','bool'],
            'false':['built-in','bool'],
            'msg.sender':['built-in','address'],
            'now':['built-in','int256'],
        }
        self.stvar = []
        self.reserved = {
            'あなた':'msg.sender',
            '今':'now',
        }
        self.map = []
        self.indentLevel = 0
        self.temp = ''
        self.write_to_temp = False
        self.funcInfo = {'A':'public ', 'B':'view ', 'C':''}
    def temp_reset(self):
        self.temp = ""
    def setTree(self,tree):
        self.string = tree
        self.pos = 0
        self.output = ''
        self.indentLevel = 0
        self.temp = ''
    def funcInfoReset(self):
        self.funcInfo = {'A':'public ', 'B':'view ', 'C':''}
    def getFuncInfo(self):
        return self.funcInfo['A'] + self.funcInfo['B'] + self.funcInfo['C']
    def get_tag(self):
        tag = ""
        self.require('[')
        self.pos+=1
        while(self.current() != ' '):
            tag += self.current()
            self.pos+=1
        self.pos+=1
        return tag
    def require(self,ch):
        if self.current() != ch:
            print('pos:'+str(self.pos)+' require "'+ch+'", but found "'+self.current()+'"')
            sys.exit()
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
    def makeIndent(self):
        self.output+=('    ' * self.indentLevel)
    def Indent(self):
        return '    '*self.indentLevel
    def withType(self,word,mdf):
        if len(mdf) > 0:
            mdf+=' '
        return self.typeDetect(word,0) + ' ' + mdf + word
    def typeDetect(self,w,count):
        #w = 'owner'
        #w = 'map02[hogege]'
        #w = 'map02'
        #w = 'numbers[index][i2][i3]'
        #w = 'data.param'
        #w = 'int(123)'
        if w in self.words:
            return self.words[w][count+1]
        elif w.rfind('.') > 0:
            return self.typeDetect(w[w.rfind('.')+1:],0)
        elif w.rfind('[') > 0:
            return self.typeDetect(w[:w.rfind('[')],count+1)
        elif w.startswith('int('):
            return 'int256'
        elif w.startswith('"') and w.endswith('"'):
            return 'string'
        else:
            print('Not find '+w+' in dict');
            sys.exit()
            return 'Unknown'
    def isStateVar(self,w):
        if w.find('.') > 0:
            return self.isStateVar(w[:w.find('.')])
        elif w.find('[') > 0:
            return self.isStateVar(w[:w.find('[')])
        else:
            return w in self.stvar
    def structDef(self,key):
        st = ''
        st+=('struct ' + key + ' {')
        for p in self.struct[key]:
            st+=(self.withType(p)+';')
        st+='}\n'
        return st
    def wordsToPEG(self):
        word_list = []
        for k in self.words:
            word_list.append(self.words[k][0])
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

