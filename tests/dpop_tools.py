import json
'''
pip3 install jwcrypto
'''
from jwcrypto import jwt, jwk

#key = jwk.JWK.generate(kty='OKP', crv='Ed25519')
#print (key.export(as_dict=True))

privatkeyBase64url = "n--gJkymNdp5JQgSfLRoA5T_3nmaLj1THQuOvyrySPs"
publickeyBase64url = "bKmPLs6MsZaeVtEQF4rCjoVfi37XgRTEl-4ZgqmgBw0"

#rfc8037
jsonkey  = {'kty': 'OKP', 'crv': 'Ed25519', 'x': publickeyBase64url, 'd': privatkeyBase64url}
key = jwk.JWK.from_json(json.dumps(jsonkey))
print(key.thumbprint())

dpop_header = {
    "typ":"dpop+jwt",
     "alg":"EdDSA",
     "jwk": key.export_public(as_dict=True)
}
dpop_claims = {
     "jti":"-BwC3ESc6acc2lTc",
     "htm":"POST",
     "htu":"https://server.example.com/token",
     "iat":1562262616
}
dpop = jwt.JWT(header = dpop_header, claims = dpop_claims)
dpop.make_signed_token(key)
print(dpop.serialize())

