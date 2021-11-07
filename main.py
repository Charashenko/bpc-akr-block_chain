import classes as c
import time as t

bc = c.BlockChain("AkrCoin", 4)

walletA = c.Wallet("Alice")
walletB = c.Wallet("Bob")

initial_transaction = c.Transaction(None, walletA, 100, 
        [c.TransactionOutput(walletA, 100, "0")])
initialb = c.Block(initial_transaction, "0", t.time(), 0)
bc.addToBC(initialb)
print(f"A: {walletA.getBalance()}")
print(f"B: {walletB.getBalance()}")

firstb = c.Block(walletA.sendFunds(walletB, 20), bc.getLastHash(), t.time(), 0)
bc.addToBC(firstb)
print(f"A: {walletA.getBalance()}")
print(f"B: {walletB.getBalance()}")

secondb = c.Block(walletA.sendFunds(walletB, 10), bc.getLastHash(), t.time(), 0)
bc.addToBC(secondb)
print(f"A: {walletA.getBalance()}")
print(f"B: {walletB.getBalance()}")

thirdb = c.Block(walletB.sendFunds(walletA, 30), bc.getLastHash(), t.time(), 0)
bc.addToBC(thirdb)
print(f"A: {walletA.getBalance()}")
print(f"B: {walletB.getBalance()}")

fourthb = c.Block(walletB.sendFunds(walletA, 30), bc.getLastHash(), t.time(), 0)
bc.addToBC(fourthb)
print(f"A: {walletA.getBalance()}")
print(f"B: {walletB.getBalance()}")

print(bc)
