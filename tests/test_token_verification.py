from IAA import iaa
import pytest

def test_valid_bearer():
    type = "Bearer"
    target = 'sofie-iot.eu'
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpZCI6IjM2ZGNlNjBiMzg4YjA2NDUyNmI5MDJhOGRjMzIyM2NhNGMxMWFmNWYiLCJqdGkiOiIzNmRjZTYwYjM4OGIwNjQ1MjZiOTAyYThkYzMyMjNjYTRjMTFhZjVmIiwiaXNzIjoiTktHS3RjTndzc1RvUDVmN3Voc0VzNCIsImF1ZCI6InNvZmllLWlvdC5ldSIsInN1YiI6Im15ZGlkIiwiZXhwIjoxNTgxMzQyNDE4LCJpYXQiOjE1ODEzMzg4MTgsInRva2VuX3R5cGUiOiJiZWFyZXIiLCJzY29wZSI6bnVsbH0.XSyQTgTt1WByT46NJLwrlcU3BUXzWf4MDZE3M4bLAh3HwFAwD6Dhi1IVeLAxNscc0bCgS-3KgyD1fdtiiJH7WktQIc269OLNxhnaXun_LxEYrWQCRHIFb0Je8Eg6CvdOB3shrlNZHmVELe6gaU0tQJ0-cdBbuz0udq_Mou1WLEwe6vp3mfgLiuTe2pT4wVI2PldvmUujeH6IpEop1nESYVA06pK6nV08d1RW7c_sRPgJdpSGGv-QhRcxBjDowkUs9J0OaTtGlExKhMv_17P96EskyOqCHku6RyydFccYbd5tl-Wh-9MqI4Me8z3BBSKPiIvQ2mo5OMcBmI0WwXb6jw"
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