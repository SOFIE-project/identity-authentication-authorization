from IAA import iaa
import pytest

def test_valid_bearer():
    token = "bearer"
    code, output = iaa.IAA.verify_token("Bearer", token)
    assert( code == 200)