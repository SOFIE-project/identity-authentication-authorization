from IAA import iaa
import pytest
import requests
import json
import asyncio
import json
import base64

@pytest.fixture(autouse=True)
def server():
    import subprocess
    import time
    p1 = subprocess.Popen(['python3', 'IAA/iaa.py', 'tests/conf/test.conf'])
    time.sleep(1) #Otherwise the server is not ready when tests start
    yield
    p1.kill()


def test_valid_bearer():
    payload = {'token-type':'Bearer'}
    response  = requests.post("http://localhost:9000/verifytoken", data = payload).text
    response =json.loads(response)
    assert(response['code'] == 200)

def test_invalid_token_type():
    payload = {'token-type':'Garbage'}
    response  = requests.post("http://localhost:9000/verifytoken", data = payload).text
    response =json.loads(response)
    assert(response['code'] == 403)

@pytest.mark.asyncio
async def test_valid_did():
    user = {
        'wallet_config': json.dumps({'id': 'user_wallet',"storage_config":{"path":"tests/indy_wallets"}}),
        'wallet_credentials': json.dumps({'key': 'user_wallet_key'}),
        'did' : '4qk3Ab43ufPQVif4GAzLUW'
    }
    payload = {'token-type':'DID', 'token':user['did']}
    response  = requests.post("http://localhost:9000/verifytoken", data = payload).text
    response =json.loads(response)
    assert(response['code'] == 401)