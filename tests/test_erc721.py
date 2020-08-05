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
import jwt



ganache_accounts = [
    {
    'address':'0x1df62f291b2e969fb0849d99d9ce41e2f137006e',
    'public_key':'0x9c691b945b14656b98edbf4d3657290c65cad377bca44da4d54e88cd2bbdefb2e063267b06183029fea5017567653c0fb6c4e3426843381ad7e09014b2d384cf'
    },
    {
    'address':'0xaca94ef8bd5ffee41947b4585a84bda5a3d3da6e',
    'public_key':'0xe57bc4cf2a3acee734d852bac655bad61d4f8ebf57751cf8f398f03a8e48b1e7e4a20d35193a87b273e8c7420a57fed3ecb4a041c2d79e15638c633a20b6f8a7'
    },
    {
    'address':'0xe11ba2b4d45eaed5996cd0823791e0c93114882d',
    'public_key':'0x78b7e11a2b1b66504963ba9cfcccc69a37b6fc8138e51b6e82effba9dc6f8d8110892e9aab67621bd770eeccb9bd9397e3c5ca3be9a04423e51950ed679f887a'
    },
    {
    'address':'0x3e5e9111ae8eb78fe1cc3bb8915d5d461f3ef9a9',
    'public_key':'0x36d6456fbea76a92d395f74dce8a37c453ebbdd0c0682aa328372ec2170e20779465b6f64a8e932820bda82c7868e9c216a82d21f0c1777111f9f08ffa110a8b'
    },
    {
    'address':'0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1',
    'public_key':'0xe68acfc0253a10620dff706b0a1b1f1f5833ea3beb3bde2250d5f271f3563606672ebc45e0b7ea2e816ecb70ca03137b1c9476eec63d4632e990020b7b6fba39'
    },
    {
    'address':'0xffcf8fdee72ac11b5c542428b35eef5769c409f0',
    'public_key':'0x94d3137ac5561a2f7b7909f3304c678bbe5c628c4156e1f9ef40c521b41b9d27632903767d1ba736eac8d1c37bcb9d663fb7786bc6c8dafcb122293743b221d8'
    },
    {
    'address':'0x28a8746e75304c0780e011bed21c72cd78cd535e',
    'public_key':'0x20b38ff0dba283e8f390f36dfb2699f9d5dd26e5a9fa079dbccd8d7281da97c37a24f14f6bb3bc86fc154e76b72f31dbb50f1152ada8671c4acd63cdc45215da'
    },
    {
    'address':'0xd03ea8624c8c5987235048901fb614fdca89b117',
    'public_key':'0x925b36d9c2b031d0f6c259d9744d9582b021a34cc37bc437c2d74a6e63cb334f12272afc08f5552163139ea1cc81ed69949c02214e6a4d87f7f2c5953f87c729'
    },
    {
    'address':'0x22d491bde2303f2f43325b2108d26f1eaba1e32b',
    'public_key':'0x56e12fd39278e33cd2df2aaa0acd57974a1ce5637e2231903dc0bf45aeffb9a3e5a20314a70b9f1de7e347f9f098254375abd81e7d63da7c742967761e36952b'
    },
    {
    'address':'0x95ced938f7991cd0dfcb48f0a06a40fa1af46ebc',
    'public_key':'0xc41cbfc96c0784c87fc6257d45d82ff022e89f8b170ab0155de2be400bca00c30fd9170ba3cd9b3743e88bef593f603aa95f95ab74fa1b4b0ad59216ffb924f2'
    }
]

@pytest.fixture(autouse=True, scope="module")
def server():
    import subprocess
    import time
    global w3, abi, account, address, jwt_verification_key, ERC721Contract_instance, ganache_accounts, jwt_token_enc
    
    p3 = subprocess.Popen(['ganache-cli', '-m', 'myth like bonus scare over problem client lizard pioneer submit female collect']) #use this mnemonic to much the contract address in configuration
    time.sleep(10)
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
    with open('conf/contract/build/ERC721Metadata.bin', 'r') as myfile:
        binfile = myfile.read()
    with open('conf/contract/build/ERC721Metadata.abi', 'r') as myfile:
        abi = myfile.read()
    account = w3.eth.accounts[0]
    ERC721Contract = w3.eth.contract(abi=abi, bytecode=binfile)
    tx_hash = ERC721Contract.constructor("Sofie Access Token", "SAT").transact({'from': account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    address = tx_receipt.contractAddress
    with open('tests/keys/as_private_key.pem', mode='rb') as file: 
        jwt_signing_key = file.read()
    with open('tests/keys/as_public_key.pem', mode='rb') as file: 
        jwt_verification_key = file.read()
    
    jwt_metadata = {
        'aud': 'sofie-iot.eu',
        'jti': 'c0097d06511a91ffd05912862dca06f5bd428886dd3b9534d863947a1aa3e5c4'
    }
    
    ERC721Contract_instance = w3.eth.contract(abi = abi, address = address)
    
    token_id = int('c0097d06511a91ffd05912862dca06f5bd428886dd3b9534d863947a1aa3e5c4', base=16)
    jwt_token_enc = jwt.encode(jwt_metadata,jwt_signing_key, algorithm='RS256')
    tx_hash = ERC721Contract_instance.functions.mint(w3.toChecksumAddress(ganache_accounts[0]['address']), token_id, jwt_token_enc).transact({'from': account}) 

    yield
    p3.kill()


@pytest.mark.asyncio
async def test_metadata():
    global w3, abi, account, address, jwt_verification_key, ERC721Contract_instance

    token_id = int('c0097d06511a91ffd05912862dca06f5bd428886dd3b9534d863947a1aa3e5c4', base=16)

    metadata = ERC721Contract_instance.functions.getTokenURI(token_id).call()
    jwt_token_dec = jwt.decode(metadata, jwt_verification_key, algorithms='RS256', audience='sofie-iot.eu', options={"verify_exp":False})

    assert(int(jwt_token_dec['jti'], base=16) == token_id)
    

@pytest.mark.asyncio
async def test_ownerOf():
    global w3, abi, account, address, jwt_verification_key, ERC721Contract_instance, ganache_accounts, jwt_token_enc

    jwt_token_dec1 = jwt.decode(jwt_token_enc, jwt_verification_key, algorithms='RS256', audience='sofie-iot.eu', options={"verify_exp":False})
    ownerOfToken1 = ERC721Contract_instance.functions.ownerOf(jwt_token_dec1['jti']).call()
    hash1 = w3.keccak(hexstr=ganache_accounts[0]['public_key'])
    client_address1 = w3.toHex(hash1[-20:])

    assert(ownerOfToken1 == w3.toChecksumAddress(client_address1))

@pytest.mark.asyncio
async def test_revocation():
    global w3, abi, account, address, jwt_verification_key, ERC721Contract_instance, ganache_accounts, jwt_token_enc

    jwt_token_dec = jwt.decode(jwt_token_enc, jwt_verification_key, algorithms='RS256', audience='sofie-iot.eu', options={"verify_exp":False})
    tx_hash = ERC721Contract_instance.functions.burn1(jwt_token_dec['jti']).transact({'from': account}) 

    ownerOfToken = ERC721Contract_instance.functions.ownerOf(jwt_token_dec['jti']).call()
    print(ownerOfToken)

    assert(ownerOfToken == '0x0000000000000000000000000000000000000000')
