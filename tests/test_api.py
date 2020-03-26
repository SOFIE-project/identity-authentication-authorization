import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../IAA/')

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
    p1 = subprocess.Popen(['python3', 'IAA/iaa.py'])
    time.sleep(5) #Otherwise the server is not ready when tests start
    yield
    p1.kill()


def test_valid_bearer():
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6IjM2ZGNlNjBiMzg4YjA2NDUyNmI5MDJhOGRjMzIyM2NhNGMxMWFmNWYiLCJqdGkiOiIzNmRjZTYwYjM4OGIwNjQ1MjZiOTAyYThkYzMyMjNjYTRjMTFhZjVmIiwiaXNzIjoiTktHS3RjTndzc1RvUDVmN3Voc0VzNCIsImF1ZCI6InNvZmllLWlvdC5ldSIsInN1YiI6Im15ZGlkIiwiZXhwIjoxNTgxMzQyNDE4LCJpYXQiOjE1ODEzMzg4MTgsInRva2VuX3R5cGUiOiJiZWFyZXIiLCJzY29wZSI6bnVsbH0.XSyQTgTt1WByT46NJLwrlcU3BUXzWf4MDZE3M4bLAh3HwFAwD6Dhi1IVeLAxNscc0bCgS-3KgyD1fdtiiJH7WktQIc269OLNxhnaXun_LxEYrWQCRHIFb0Je8Eg6CvdOB3shrlNZHmVELe6gaU0tQJ0-cdBbuz0udq_Mou1WLEwe6vp3mfgLiuTe2pT4wVI2PldvmUujeH6IpEop1nESYVA06pK6nV08d1RW7c_sRPgJdpSGGv-QhRcxBjDowkUs9J0OaTtGlExKhMv_17P96EskyOqCHku6RyydFccYbd5tl-Wh-9MqI4Me8z3BBSKPiIvQ2mo5OMcBmI0WwXb6jw"
    payload = {'token-type':'Bearer', 'token':token}
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