import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../IAA/')

import pytest
import requests
import json 
from web3 import Web3
import jwt

@pytest.fixture(autouse=True, scope="module")
def server():
    import subprocess
    import time

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

    ganache_accounts = {
        'address':'0x1df62f291b2e969fb0849d99d9ce41e2f137006e',
        'public_key':'0x9c691b945b14656b98edbf4d3657290c65cad377bca44da4d54e88cd2bbdefb2e063267b06183029fea5017567653c0fb6c4e3426843381ad7e09014b2d384cf'
    }

    jwt_metadata = {
        'aud': 'sofie-iot.eu',
        'jti': 'c0097d06511a91ffd05912862dca06f5bd428886dd3b9534d863947a1aa3e5c4'
    }
    
    ERC721Contract_instance = w3.eth.contract(abi = abi, address = address)
    token_id = int('c0097d06511a91ffd05912862dca06f5bd428886dd3b9534d863947a1aa3e5c4', base=16)
    jwt_token_enc = jwt.encode(jwt_metadata,jwt_signing_key, algorithm='RS256')
    tx_hash = ERC721Contract_instance.functions.mint(w3.toChecksumAddress(ganache_accounts['address']), token_id, jwt_token_enc).transact({'from': account})

    p1 = subprocess.Popen(['python3', 'IAA/iaa.py'])
    time.sleep(5) #Otherwise the server is not ready when tests start

    yield
    p3.kill()
    p1.kill()


def test_valid_bearer_get():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6IjM2ZGNlNjBiMzg4YjA2NDUyNmI5MDJhOGRjMzIyM2NhNGMxMWFmNWYiLCJqdGkiOiIzNmRjZTYwYjM4OGIwNjQ1MjZiOTAyYThkYzMyMjNjYTRjMTFhZjVmIiwiaXNzIjoiTktHS3RjTndzc1RvUDVmN3Voc0VzNCIsImF1ZCI6InNvZmllLWlvdC5ldSIsInN1YiI6Im15ZGlkIiwiZXhwIjoxNTgxMzQyNDE4LCJpYXQiOjE1ODEzMzg4MTgsInRva2VuX3R5cGUiOiJiZWFyZXIiLCJzY29wZSI6bnVsbH0.XSyQTgTt1WByT46NJLwrlcU3BUXzWf4MDZE3M4bLAh3HwFAwD6Dhi1IVeLAxNscc0bCgS-3KgyD1fdtiiJH7WktQIc269OLNxhnaXun_LxEYrWQCRHIFb0Je8Eg6CvdOB3shrlNZHmVELe6gaU0tQJ0-cdBbuz0udq_Mou1WLEwe6vp3mfgLiuTe2pT4wVI2PldvmUujeH6IpEop1nESYVA06pK6nV08d1RW7c_sRPgJdpSGGv-QhRcxBjDowkUs9J0OaTtGlExKhMv_17P96EskyOqCHku6RyydFccYbd5tl-Wh-9MqI4Me8z3BBSKPiIvQ2mo5OMcBmI0WwXb6jw"
    headers = {'Authorization':'Bearer-ERC721 ' + token, 'Accept': 'application/json'}
    response  = requests.get("http://localhost:9000/things/virtual-things-0/properties/", headers = headers)
    print(response.text)
    assert(response.status_code == 200)

def test_valid_bearer_put():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6IjM2ZGNlNjBiMzg4YjA2NDUyNmI5MDJhOGRjMzIyM2NhNGMxMWFmNWYiLCJqdGkiOiIzNmRjZTYwYjM4OGIwNjQ1MjZiOTAyYThkYzMyMjNjYTRjMTFhZjVmIiwiaXNzIjoiTktHS3RjTndzc1RvUDVmN3Voc0VzNCIsImF1ZCI6InNvZmllLWlvdC5ldSIsInN1YiI6Im15ZGlkIiwiZXhwIjoxNTgxMzQyNDE4LCJpYXQiOjE1ODEzMzg4MTgsInRva2VuX3R5cGUiOiJiZWFyZXIiLCJzY29wZSI6bnVsbH0.XSyQTgTt1WByT46NJLwrlcU3BUXzWf4MDZE3M4bLAh3HwFAwD6Dhi1IVeLAxNscc0bCgS-3KgyD1fdtiiJH7WktQIc269OLNxhnaXun_LxEYrWQCRHIFb0Je8Eg6CvdOB3shrlNZHmVELe6gaU0tQJ0-cdBbuz0udq_Mou1WLEwe6vp3mfgLiuTe2pT4wVI2PldvmUujeH6IpEop1nESYVA06pK6nV08d1RW7c_sRPgJdpSGGv-QhRcxBjDowkUs9J0OaTtGlExKhMv_17P96EskyOqCHku6RyydFccYbd5tl-Wh-9MqI4Me8z3BBSKPiIvQ2mo5OMcBmI0WwXb6jw"
    headers = {'Authorization':'Bearer-ERC721 ' + token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    data = {'on': False}
    response  = requests.put("http://localhost:9000/things/virtual-things-0/properties/on", headers = headers, data = json.dumps(data))
    print(response.text)
    assert(response.status_code == 200)

