import jwt

class jwt_pep:
    def verify_bearer(self, token=None, as_public_key=None, tokens_expire = True, proof=None): 
        try:
            decoded_token = jwt.decode(token, as_public_key, algorithms='RS256', options={"verify_exp":tokens_expire, "verify_aud":False})
            return True, 0
        except:
            return False, 100 #Token cannot be decoded