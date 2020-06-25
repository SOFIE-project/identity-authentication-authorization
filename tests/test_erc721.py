import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../IAA/')

from indy import did,wallet,crypto
from web3 import Web3
import pytest
import requests
import json
import asyncio
import json
import base64

@pytest.fixture(autouse=True, scope="module")
def server():
    import subprocess
    import time
    global w3, abi, account, address
    p3 = subprocess.Popen(['ganache-cli', '-m', 'myth like bonus scare over problem client lizard pioneer submit female collect']) #use this mnemonic to much the contract address in configuration
    time.sleep(10)
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
    with open('conf/contract/build/ERC721Metadata.abi', 'r') as myfile:
        abi = myfile.read()
    with open('conf/contract/build/ERC721Metadata.bin', 'r') as myfile:
        binfile = myfile.read()
    account = w3.eth.accounts[0]
    ERC721Contract = w3.eth.contract(abi=abi, bytecode=binfile)
    tx_hash = ERC721Contract.constructor("Sofie Access Token", "SAT").transact({'from': account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    address = tx_receipt.contractAddress
    yield
    p3.kill()

@pytest.mark.asyncio
async def test_valid_auth_code_ecn_token_with_logging():
    global w3, abi, account, address
    ERC721Contract_instance = w3.eth.contract(abi=abi, address=address)
    tx_hash = ERC721Contract_instance.functions.mint('0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1', 1234, "metadata").transact({'from': account})
    w3.eth.waitForTransactionReceipt(tx_hash)
    metadata = ERC721Contract_instance.functions.getTokenURI(1234).call()
    assert(metadata == "metadata")
