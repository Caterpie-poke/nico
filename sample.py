#PEGの合体
def marge_peg_file():
    file1 = open('./hogege.txt','rb')
    file2 = open('./hogegu.txt','rb')
    peg1 = file1.read()
    peg2 = file2.read()
    return peg1+bytes(b'\n')+peg2

print(hoge())