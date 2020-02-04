from IAA import iaa
import pytest

def test_valid_bearer():
    token = "bearer"
    assert(iaa.IAA.verify_token("Bearer", token) == True)