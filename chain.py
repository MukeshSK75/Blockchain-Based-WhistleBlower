import datetime
from hashlib import sha256
import hashlib 

def uphash(*args):
    hash_text=""
    h=sha256()
    for arg in args:
        hash_text += str(arg)
    h.update(hash_text.encode('utf-8'))
    return h.hexdigest()


class Block():
    data=None
    hashs=None
    prev="0"*64
    nonce=0

    def __init__(self,data,num=0):
        self.data=data
        self.num=num
    def hashh(self):
        return uphash(self.prev,self.num,self.data,self.nonce)
    def __str__(self):
        return str("Block: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s" %(self.num,self.hashh(),self.prev,self.data,self.nonce))

class Chain():
    dif=4
    
    def __init__(self,chain=[]):
        self.chain=chain
    def add(self,block):
        self.chain.append({'data':block.data,
                           'hash':block.hashh(),
                           'previous':block.prev,
                           'number':block.num,
                           'nonce':block.nonce})
    def mine(self,block):
        try:
            block.prev=self.chain[-1].get('hash')
        except IndexError:
            pass

        while True:
            if block.hashh()[:4] == "0" * self.dif:
                self.add(block); break
            else:
                block.nonce += 1
    def isvalid(self):
        for i in range(1,len(self.chain)):
            _prev=self.chain[i].get('previous')
            _cur=self.chain[i-1].get('hash')
            if _prev != _cur or _cur[:4] != "0" * self.dif:
                return False
        return True
if __name__=='__main__':
    bk=Chain()
    db=["hi","soma","kk",11]
    num=0

    for data in db:
        num += 1
        bk.mine(Block(data,num))
    for b in bk.chain:
        print(b)

    print(bk.isvalid())