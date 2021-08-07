from hashlib import sha256


def update_hash(*args):
    cur = ""
    hasher = sha256()
    for arg in args:
        cur += str(arg)
    hasher.update(cur.encode('utf-8'))
    return hasher.hexdigest()

class Block():
    def __init__(self,Number=0,data = None,prev_hash = "0"*64,nonce = 0):
        self.data = data
        self.prev_hash = prev_hash
        self.Number = Number
        self.nonce = nonce

    def __str__(self):
        return(
        str(
        "Block Number: %s\nPrev Hash: %s\nData: %s\nHash: %s\nNonce: %s\n"
        %(self.Number,
        self.prev_hash,
        self.data,
        self.hash(),
        self.nonce)
        )
        )

    def hash(self):
        return update_hash(self.Number,self.prev_hash,self.data,self.nonce)



class Blockchain():

    difficulty = 4
    def __init__(self):
        self.chain = []

    def add(self,block):
        self.chain.append(block)

    def mine(self, block):
        try:
            block.prev_hash = self.chain[-1].hash()
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0"*self.difficulty:
                self.add(block)
                break
            else:
                block.nonce += 1

    def remove(self,block):
        self.chain.remove(block)

    def isValid(self):
        for i in range(1,len(self.chain)):
            prev = self.chain[i-1]
            cur = self.chain[i]
            if prev.hash() != cur.prev_hash or prev.hash()[0:self.difficulty] != "0"*self.difficulty:
                return False
        return True

def main():
    BlockChain = Blockchain()
    database = ["Data1","Data2","Data3","Data4"]
    num = 0
    for data in database:
        num += 1
        BlockChain.mine(Block(num,data))

    for block in BlockChain.chain:
        print("\n",block)


    print("Validity: ",BlockChain.isValid())

if __name__ == '__main__':
    main()
