from src.block import Block
import time
import requests
import threading
# Noobcash Blockchain:
#  The list of blocks which are verified
minings = threading.Event()
minings.clear()

class Blockchain:
    def __init__(self, maxTransactions=1):
        self.maxTransactions = maxTransactions # Max transactions in block
        self.blockchain = []
        self.transactions = []                 # Storage of transactions till 
        self.stopMine = threading.Event()
        self.stopMine.clear()

    def genBlock(self):
        return self.blockchain[0]

    def addBlock(self, block):
        self.blockchain.append(block)

    def getLastHash(self):
        return self.blockchain[-1].current_hash

    def convert_chain(self):
        res = []
        for bl in self.blockchain:
            res.append(bl.convert_block())
        return res

    def mine(self, newBlock, ipList, id):
        print('Starting to mine.')
        begin = time.time()
        newBlock.mine_block(self.stopMine)
        if self.stopMine.isSet():
            minings.clear()
            print('Quitting mine.')
            exit(1)
        self.blockchain.append(newBlock)
        self.broadcastBlock(newBlock, time.time(), ipList, id)
        minings.clear()
        end = time.time() - begin
        fd = open('distributed_systems-main/noobcash/times/mining' + '.txt', 'a')
        fd.write(str(end) + '\n')
        fd.close()

    def broadcastBlock(self, block, startTime, ipList, id):
        print('...................................Broadcasting Block...................................................')
        tmp = {'lb': block.convert_block(), 'mt': startTime}
        for ip in ipList:
            if ip[0] !=  id:
                requests.post(ip[1] + "/mine", json=tmp, headers={
                              'Content-type': 'application/json', 'Accept': 'text/plain'})
        return
