import time as t
import hashlib as hl
import json

class BlockChain:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        self.blocks = []

    def isValid(self):
        first_block = self.blocks[0]
        prev_block = first_block
        for current_block in self.blocks[1:]:
            checked_block = c.Block(current_block.data, prev_block.hash, 
                current_block.time_stamp, current_block.nonce)
            if current_block.hash != checked_block.hash:
                return False
            prev_block = current_block
        return True
    
    def addToBC(self, block):
        if(block.mineBlock(self.difficulty)):
            self.blocks.append(block)

    def insertToBC(self, block, index):
        self.blocks[index] = block

    def getLastHash(self):
        return self.blocks[-1].hash

    def __str__(self):
        return json.dumps(self.dict(), indent=4)
    
    def dict(self):
        blocks = []
        for block in self.blocks:
            blocks.append(block.dict())
        return blocks

class Block:
    def __init__(self, data, prev_hash, time_stamp, nonce=0):
        self.prev_hash = prev_hash
        self.data = data
        self.time_stamp = time_stamp
        self.nonce = nonce
        self.hash = self.hashBlock()

    def dict(self):
        return {
            "data" : self.data.dict(), 
            "time_stamp": str(self.time_stamp),
            "previous_hash" : str(self.prev_hash),
            "hash" : str(self.hash),
            "nonce" : str(self.nonce)
        }

    def hashBlock(self):
        msg = hl.sha256()
        msg.update(str(self.prev_hash).encode("utf-8"))
        msg.update(str(self.data).encode("utf-8"))
        msg.update(str(self.time_stamp).encode("utf-8"))
        msg.update(str(self.nonce).encode("utf-8"))
        return msg.hexdigest()

    def mineBlock(self, diff):
        if not self.data:
            print("Invalid transaction")
            return False
        while self.hash[:diff] != diff*"0":
            self.nonce = self.nonce + 1
            self.hash = self.hashBlock()
        outputs = self.data.outputs
        if len(outputs) == 2:
            self.data.sender.recieveFunds(outputs[0])
            self.data.reciepient.recieveFunds(outputs[1])
        else:
            self.data.reciepient.recieveFunds(outputs[0])
        return True

    def changeData(self, data):
        self.data = data
        self.hash = self.hashBlock()


class Wallet:
    def __init__(self, name):
        self.name = name
        self.utxo = []
   
    def __str__(self):
        return self.name

    def checkNeededFunds(self, value): 
        needed_inputs = []
        balance = 0
        for input_transaction in self.utxo:
            if input_transaction.reciepient.name == self.name:
                balance += input_transaction.value
                needed_inputs.append(input_transaction)
                if balance >= value:
                    break
        if balance >= value:
            for input_transaction in needed_inputs:
                self.utxo.remove(input_transaction)
            return needed_inputs
        else:
            return []

    def sendFunds(self, reciepient, value):
        inputs = self.checkNeededFunds(value)
        if not inputs:
            print("Not enough funds!")
            return
        transaction = Transaction(self, reciepient, value, inputs)
        return transaction

    def recieveFunds(self, output):
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
        self.generateOutputs()

    def calculateHash(self):
        msg = hl.sha256()
        msg.update(str(self.sender).encode("utf-8"))
        msg.update(str(self.reciepient).encode("utf-8"))
        msg.update(str(self.value).encode("utf-8"))
        return msg.hexdigest()

    def generateOutputs(self):
        balance = 0
        for input_transaction in self.inputs:
            balance += input_transaction.value
        return_to_sender = balance - self.value
        reciepient_output = TransactionOutput(self.reciepient, self.value, self.id)
        if return_to_sender != 0:
            sender_output = TransactionOutput(self.sender, return_to_sender, self.id)
            self.outputs = [sender_output, reciepient_output]
        else:
            self.outputs = [reciepient_output]

    def dict(self):
        inputs = []
        for inp in self.inputs:
            inputs.append(inp.dict())
        outputs = []
        for out in self.outputs:
            outputs.append(out.dict())
        return {
            "id" : str(self.id),
            "sender" : str(self.sender),
            "reciepient": str(self.reciepient),
            "value" : str(self.value),
            "inputs" : inputs,
            "outputs" : outputs
        }


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
    
    def dict(self):
        return {
            "id" : str(self.id),
            "reciepient" : str(self.reciepient),
            "value" : str(self.value),
            "parent_transaction_id" : str(self.parent_transaction_id)
        }

