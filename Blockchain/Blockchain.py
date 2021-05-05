from datetime import datetime
from hashlib import sha256

def calculmyhash(blockdata):
        b = str(blockdata.index) + str(blockdata.previousHash) + str(blockdata.data) + str(blockdata.timestamp) + str(blockdata.nonce)
        hash = sha256(b.encode('utf-8')).hexdigest()
        return (hash)


class Block:
    def __init__(self, index, previousHash, data):
        self.index = index
        self.previousHash = previousHash
        self.data = data
        self.timestamp = datetime.now()
        self.nonce = 0
        self.createBlock()

    def createBlock(self):
        self.blockHash = calculmyhash(self)

        while self.blockHash[0:4] != "0000":
            self.nonce += 1
            self.blockHash = calculmyhash(self)


class Blokchain:
    def __init__(self):
        self.blockhain = []

        firstBlock = Block(0, None, "Genisis Block")
        self.blockhain.append(firstBlock)
    
    def addNewBlock(self, data):
        lastBlock = self.blockhain[-1]
        newBlock = Block(lastBlock.index + 1, lastBlock.blockHash, data)
        self.blockhain.append(newBlock)
    
    def VerifBlockhain(self):
        for b in range(1, len(self.blockhain)):
            pb = self.blockhain[b-1]
            pa = self. blockhain[b]

            if pb.index + 1 != pa.index or pb.blockHash != pa.previousHash or pa.blockHash != calculmyhash(pa):
                print("Error")
                return False
        print("OK")
        return True

    def __str__(self):
        s = "Blockchain\n\n\n"
        for el in self.blockhain:
            s = s + "id: " + str(el.index) + "\nprevioushash: " + str(el.previousHash) + "\n Hash: " + str(el.blockHash) + "\n Data: " + str(el.data) + "\n\n\n"
        return s



bb = Blokchain()
bb.addNewBlock("Test")

print(bb)
bb.VerifBlockhain()