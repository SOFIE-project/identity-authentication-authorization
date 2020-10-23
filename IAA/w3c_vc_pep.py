from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse
try:
    import nacl.signing
    import nacl.encoding
except ImportError:
     print("Couldn't import nacl, if you don't need W3C-VC support that's OK")
try:
    from pyld import jsonld
    from pyld.jsonld import JsonLdProcessor
except ImportError:
     print("Couldn't import pyld, if you don't need W3C-VC support that's OK")
import hashlib
import json

class w3c_vc_pep:
    def verify_w3c_vc(self, vc=None, signing_key=None, filter=None, documentloader=None): 
        singed_credential = json.loads(vc)
        jws_header = b'{"alg":"EdDSA","b64":false,"crit":["b64"]}'
        proof =  singed_credential['proof']
        proof['@context'] = 'https://w3id.org/security/v2'
        encodedSignature = proof['jws'].split("..",1)[1] + "==" 
        del singed_credential['proof']
        del proof['jws']

        normalized_doc   = jsonld.normalize(singed_credential , {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
        normalized_proof = jsonld.normalize(proof, {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
        doc_hash         = hashlib.sha256()
        proof_hash       = hashlib.sha256()

        doc_hash.update(normalized_doc.encode('utf-8'))
        proof_hash.update(normalized_proof.encode('utf-8'))
        ver_key       = nacl.signing.VerifyKey(signing_key,nacl.encoding.HexEncoder)
        signature     = nacl.encoding.URLSafeBase64Encoder.decode(encodedSignature)
        encodedHeader = nacl.encoding.URLSafeBase64Encoder.encode(jws_header)
        to_verify     = encodedHeader + b'.' + proof_hash.digest() + doc_hash.digest()
        try:
            ver_key.verify(to_verify, signature)
            if(filter):
                if(self._filter(singed_credential, filter)):
                    return True, "0"
                else:
                    return False, "101 Filter failed"
            return True
        except:
            return False, "100 VC signature verification failed"
    
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
                print("Not found:")
                print(filter)
                return False 
        return True