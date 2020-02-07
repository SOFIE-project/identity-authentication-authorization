from IAA import iaa
from indy import did,wallet,crypto
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
    challenge = response['challenge']
    wallet_handle = await wallet.open_wallet(user['wallet_config'], user['wallet_credentials'])
    verkey = await did.key_for_local_did(wallet_handle, user['did'])
    signature = await crypto.crypto_sign(wallet_handle, verkey, challenge.encode())
    signature64 = base64.b64encode(signature)
    payload = {'token-type':'DID', 'token':user['did'], 'challenge': challenge, 'proof':signature64}
    response  = requests.post("http://localhost:9000/verifytoken", data = payload).text
    response =json.loads(response)
    assert(response['code'] == 200)
    await wallet.close_wallet(wallet_handle)