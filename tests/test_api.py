from IAA import iaa
import pytest
import requests
import json

@pytest.fixture(autouse=True)
def server():
    import subprocess
    import time
    p1 = subprocess.Popen(['python3', 'IAA/iaa.py'])
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