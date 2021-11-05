import classes as c
import time as t

def isValid(block_chain):
    first_block = block_chain[0]
    prev_block = first_block
    for current_block in block_chain[1:]:
        checked_block = c.Block(current_block.data, prev_block.hash, 
                current_block.time_stamp, current_block.nonce)
        if current_block.hash != checked_block.hash:
            return False
        prev_block = current_block
    return True


block_chain = []
difficulty = 4

"""
start_timer = t.time()
fb = c.Block("First", "0", t.time())
print("Mining first")
fb.mineBlock(difficulty)
end_timer = t.time()
fb.addToBC(block_chain)
print(f"Mining of block with {difficulty} zeros in hash took: {end_timer - start_timer}s")


sb = c.Block("Second", fb.hash, t.time())
print("Mining second")
sb.mineBlock(difficulty)
sb.addToBC(block_chain)

tb = c.Block("Third", sb.hash, t.time())
print("Mining third")
tb.mineBlock(difficulty)
tb.addToBC(block_chain)

for block in block_chain:
    print(block)

print(f"Checking blockchain validity: {isValid(block_chain)}")

print(f"Changing data of one block in blockchain")

eb = sb
eb.changeData("Evil data")
eb.mineBlock(difficulty)
eb.insertToBC(block_chain, 1)

print(f"Checking blockchain validity: {isValid(block_chain)}")
"""

walletA = c.Wallet("Alice")
walletB = c.Wallet("Bob")
walletA.recieveFunds(10, "0")
print(f"A: {walletA.getBalance()}")
print(f"B: {walletB.getBalance()}")
walletA.sendFunds(walletB, 2)
print(f"A: {walletA.getBalance()}")
print(f"B: {walletB.getBalance()}")
walletB.sendFunds(walletA, 1)
print(f"A: {walletA.getBalance()}")
print(f"B: {walletB.getBalance()}")
walletB.sendFunds(walletB, 1)
print(f"A: {walletA.getBalance()}")
print(f"B: {walletB.getBalance()}")
