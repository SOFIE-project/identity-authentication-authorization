'''
pip3 install jwcrypto
'''
from jwcrypto import jwt, jwk

key = jwk.JWK.generate(kty='OKP', crv='Ed25519')
token_header = {
    "typ":"dpop+jwt",
     "alg":"EdDSA",
     "jwk": key.export_public(as_dict=True)
}
token_claims = {
     "jti":"-BwC3ESc6acc2lTc",
     "htm":"POST",
     "htu":"https://server.example.com/token",
     "iat":1562262616
}
token = jwt.JWT(header = token_header, claims = token_claims)
token.make_signed_token(key)
print(token.serialize()[:-1])

token2 = jwt.JWT(key=key, jwt = token.serialize()[:-1])
print(token2.claims)
