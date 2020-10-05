try:
    import jwt
except ImportError:
     print("Couldn't import jwt, if you don't need JSON web token support that's OK")
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse

class jwt_pep:
    def verify_bearer(self, token=None, signing_key=None, tokens_expire = True, filter=None, proof=None): 
        try:
            decoded_token = jwt.decode(token, signing_key, algorithms='RS256', options={"verify_exp":tokens_expire, "verify_aud":False})
            if(filter):
                if(self._filter(decoded_token, filter)):
                    return True, 0
                else:
                    return False, 101 #Filter failed
            return True, 0
        except:
            return False, 100 #Token cannot be decoded
    
    def _filter(self, json_obj, filters):  
        for filter in filters:
            jsonpath_expr = parse(filter[0])
            found = False
            for match in jsonpath_expr.find(json_obj):
                if len(filter) == 2 and isinstance(filter[1], list):
                    if match.value in filter[1]:
                        found = True
                elif len(filter) == 2:
                    if match.value == filter[1]:
                        found = True
                else: #no value is required
                    found = True
            if not found:
                return False 
        return True