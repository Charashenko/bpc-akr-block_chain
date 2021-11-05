import time as t
import hashlib as hl
import json

class Block:
    def __init__(self, data, prev_hash, time_stamp, nonce=0):
        self.prev_hash = prev_hash
        self.data = data
        self.time_stamp = time_stamp
        self.nonce = nonce
        self.hash = self.hashBlock()

    def __str__(self):
        return json.dumps({
            "data" : str(self.data), 
            "time_stamp": self.time_stamp,
            "previous_hash" : str(self.prev_hash),
            "hash" : str(self.hash),
            "nonce" : str(self.nonce)}, indent=4)

    def hashBlock(self):
        msg = hl.sha256()
        msg.update(str(self.prev_hash).encode("utf-8"))
        msg.update(str(self.data).encode("utf-8"))
        msg.update(str(self.time_stamp).encode("utf-8"))
        msg.update(str(self.nonce).encode("utf-8"))
        return msg.hexdigest()

    def addToBC(self, block_chain):
        block_chain.append(self)

    def insertToBC(self, block_chain, index):
        block_chain[index] = self 
    
    def mineBlock(self, diff):
        while self.hash[:diff] != diff*"0":
            self.nonce = self.nonce + 1
            self.hash = self.hashBlock()
    
    def changeData(self, data):
        self.data = data
        self.hash = self.hashBlock()


class Wallet:
    def __init__(self, name):
        self.name = name
        self.utxo = []
    
    def sendFunds(self, reciepient, value):
        transaction = Transaction(self, reciepient, value, self.utxo)
        inputs = transaction.checkNeededFunds()
        balance = 0
        if len(inputs) == 0:
            print("Not enough funds!")
            return
        for input_transaction in inputs:
            balance += input_transaction.value
        self.recieveFunds(balance - value, transaction.id)
        reciepient.recieveFunds(value, transaction.id)

    def recieveFunds(self, value, parent_transaction_id):
        output = TransactionOutput(self, value, parent_transaction_id)
        self.utxo.append(output)
    
    def getBalance(self):
        balance = 0
        for transaction in self.utxo:
            balance += transaction.value
        return balance


class Transaction:
    def __init__(self, sender, reciepient, value, inputs):
        self.sender = sender
        self.reciepient = reciepient
        self.value = value
        self.inputs = inputs
        self.id = self.calculateHash()

    def calculateHash(self):
        msg = hl.sha256()
        msg.update(str(self.sender).encode("utf-8"))
        msg.update(str(self.reciepient).encode("utf-8"))
        msg.update(str(self.value).encode("utf-8"))
        return msg.hexdigest()

    def checkNeededFunds(self): # Checks if sender has needed funds and returns required transactions
        needed_inputs = []
        balance = 0
        for input_transaction in self.sender.utxo:
            if input_transaction.reciepient.name == self.sender.name:
                balance += input_transaction.value
                needed_inputs.append(input_transaction)
                if balance >= self.value:
                    break
        if balance >= self.value:
            for input_transaction in needed_inputs:
                self.sender.utxo.remove(input_transaction)
        return needed_inputs


class TransactionInput:
    def __init__(self, transaction_out_id):
        self.transaction_output_id = transaction_out_id


class TransactionOutput:
    def __init__(self, reciepient, value, parent_transaction_id="0"):
        self.reciepient = reciepient
        self.value = value
        self.parent_transaction_id = parent_transaction_id
        msg = hl.sha256()
        msg.update(str(reciepient).encode("utf-8"))
        msg.update(str(value).encode("utf-8"))
        msg.update(str(parent_transaction_id).encode("utf-8"))
        self.id = msg.hexdigest()
