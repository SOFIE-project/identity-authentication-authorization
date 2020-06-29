from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
with open('../conf/contract/build/ERC721Metadata.abi', 'r') as myfile:
  abi = myfile.read()

with open('../conf/contract/build/ERC721Metadata.bin', 'r') as myfile:
  binfile = myfile.read()

account = w3.eth.accounts[0]
PDSContract = w3.eth.contract(abi=abi, bytecode=binfile)
tx_hash = PDSContract.constructor("Sofie Access Token", "SAT").transact({'from': account})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
address = tx_receipt.contractAddress
print(address)
PDSContract_instance = w3.eth.contract(abi=abi, address=address)
tx_hash = PDSContract_instance.functions.mint('0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1', 1234, "metadata").transact({'from': account})
w3.eth.waitForTransactionReceipt(tx_hash)
metadata = PDSContract_instance.functions.getTokenURI(1234).call()
print(metadata)
