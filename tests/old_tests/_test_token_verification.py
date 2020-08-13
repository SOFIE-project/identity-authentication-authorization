import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../IAA/')

from IAA import iaa
import pytest

def test_valid_bearer():
    type = "Bearer"
    target = 'locker1.sofie-iot.eu'
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJsb2NrZXIxLnNvZmllLWlvdC5ldSIsImV4cCI6MTU5MTA0NTE0MC4wLCJuYmYiOjE1OTA5NTg4MDAuMH0.aaNvs4iqvjtFfW6CCsfYfPLgKZSThf3xnvQdcpGkJJIYqXXKu2EWXnK4R3SrQ9RfVMGU6RZsf7xJJpz1DgNdOjT-HpYzFuX3_KDwUI4hP2YJxBV2dArdTRllhLVLGXNdP-5rHS7XYdBeSd_ecrQiIhK7CKYS2VANm05vcZUAOlPO9PETR30_4HirWg0PkcHKxWQVLW4DjdSGDJu-UqbCMLlqRWFVRlrXUIFrOsWoBg6ca6AWW2Yjm9cSoKKULWZFVQHzlnGrzhT9vOd7N-vYiSx_-t8o679J5QJES-vZi-LJhAVQTWDpahwPtqxTUQVbWjvEKIKoNEQco_tbcYeLvQ"
    with open('tests/keys/as_public_key.pem', mode='rb') as file: 
        as_public_key = file.read()
    code, output = iaa.IAA.verify_token(type, token, as_public_key, target, False)
    assert( code == 200)

def test_invalid_target():
    type = "Bearer"
    target = 'invalid target'
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6IjM2ZGNlNjBiMzg4YjA2NDUyNmI5MDJhOGRjMzIyM2NhNGMxMWFmNWYiLCJqdGkiOiIzNmRjZTYwYjM4OGIwNjQ1MjZiOTAyYThkYzMyMjNjYTRjMTFhZjVmIiwiaXNzIjoiTktHS3RjTndzc1RvUDVmN3Voc0VzNCIsImF1ZCI6InNvZmllLWlvdC5ldSIsInN1YiI6Im15ZGlkIiwiZXhwIjoxNTgxMzQyNDE4LCJpYXQiOjE1ODEzMzg4MTgsInRva2VuX3R5cGUiOiJiZWFyZXIiLCJzY29wZSI6bnVsbH0.XSyQTgTt1WByT46NJLwrlcU3BUXzWf4MDZE3M4bLAh3HwFAwD6Dhi1IVeLAxNscc0bCgS-3KgyD1fdtiiJH7WktQIc269OLNxhnaXun_LxEYrWQCRHIFb0Je8Eg6CvdOB3shrlNZHmVELe6gaU0tQJ0-cdBbuz0udq_Mou1WLEwe6vp3mfgLiuTe2pT4wVI2PldvmUujeH6IpEop1nESYVA06pK6nV08d1RW7c_sRPgJdpSGGv-QhRcxBjDowkUs9J0OaTtGlExKhMv_17P96EskyOqCHku6RyydFccYbd5tl-Wh-9MqI4Me8z3BBSKPiIvQ2mo5OMcBmI0WwXb6jw"
    with open('tests/keys/as_public_key.pem', mode='rb') as file: 
        as_public_key = file.read()
    code, output = iaa.IAA.verify_token(type, token, as_public_key, target, False)
    assert( code == 403)