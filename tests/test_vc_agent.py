import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../IAA/')

import vc_agent
import pytest

sofie_credential_signed = {
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://mm.aueb.gr/contexts/access_control/v1"
  ],
  "id": "https://www.sofie-iot.eu/credentials/examples/1",
  "type": [
    "VerifiableCredential"
  ],
  "issuer": "did:nacl:E390CF3B5B93E921C45ED978737D89F61B8CAFF9DE76BFA5F63DA20386BCCA3B",
  "issuanceDate": "2010-01-01T19:23:24Z",
  "credentialSubject": {
    "id": "did:nacl:A490CF3B5B93E921C45ED978737D89F61B8CAFF9DE76BFA5F63DA20386BCCA62",
    "type": [
      "AllowedURLs"
    ],
    "acl": [
      {
        "url": "http://sofie-iot.eu/device1",
        "methods": [
          "GET",
          "POST"
        ]
      },
      {
        "url": "http://sofie-iot.eu/device2",
        "methods": [
          "GET"
        ]
      }
    ]
  },
  "proof": {
    "type": "Ed25519Signature2018",
    "created": "2020-07-03T15:48:18Z",
    "verificationMethod": "did:example:credential-issuer#key0",
    "proofPurpose": "assertionMethod",
    "jws": "eyJhbGciOiJFZERTQSIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19..c2-MelHsJlKBflENx5HvsN8oe56gPU-mA5hYXybvcMzAuifmTZszdMfo73yfIm4rX-mWAa-aHvUXvk2uSz0MCw"
  }
}

verification_key = {
    'id': 'did:nacl:E390CF3B5B93E921C45ED978737D89F61B8CAFF9DE76BFA5F63DA20386BCCA3B',
    'publicKeyHex': 'E390CF3B5B93E921C45ED978737D89F61B8CAFF9DE76BFA5F63DA20386BCCA3B'
}

def test_valid_vc():
    verification = vc_agent.verify(sofie_credential_signed, verification_key)
    assert (verification == True)
    
def test_filter():
  filters = [
      ["$.@context[*]", "https://mm.aueb.gr/contexts/access_control/v1"],
      ["$.issuer", ["did:nacl:E390CF3B5B93E921C45ED978737D89F61B8CAFF9DE76BFA5F63DA20386BCCA3B","another issuer", "or this issuer"]], # list of valid issuers
      ["$.credentialSubject.acl[*].url", 'http://sofie-iot.eu/device1'],
      ["$.credentialSubject.acl[?@.url='http://sofie-iot.eu/device1'].methods[*]","GET"]
    ]
  verification = vc_agent.filter(sofie_credential_signed, filters)
  assert (verification == True)
  
