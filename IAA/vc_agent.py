import hashlib
import datetime
import nacl.signing
import nacl.encoding
from pyld import jsonld
from pyld.jsonld import JsonLdProcessor
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse


def issue(credential, signing_key, documentloader=None):
    """ It signs a credential using Ed25519Signature2018 JSON-LD Signature

    :param credential: a python dict representing the credential
    :param [signing_key]:  the signing key 
        [id] the key id
        [privateKeyHex] a Hex encoded Ed25519 private key
    :param documentloader: a custom documentloader

    :return: the credential with the singature appended
    """
    credential = credential.copy()
    jws_header = b'{"alg":"EdDSA","b64":false,"crit":["b64"]}'
    proof= {
        '@context':'https://w3id.org/security/v2',
        'type': 'Ed25519Signature2018',
        'created': datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z',#'2020-06-17T17:51:12Z',
        'verificationMethod': signing_key['id'],
        'proofPurpose': 'assertionMethod'
    }

    normalized_doc   = jsonld.normalize(credential , {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
    normalized_proof = jsonld.normalize(proof, {'algorithm': 'URDNA2015', 'format': 'application/n-quads'})
    doc_hash         = hashlib.sha256()
    proof_hash       = hashlib.sha256()

    doc_hash.update(normalized_doc.encode('utf-8'))
    proof_hash.update(normalized_proof.encode('utf-8'))
    signing_key   = nacl.signing.SigningKey(signing_key['privateKeyHex'],nacl.encoding.HexEncoder)
    encodedHeader = nacl.encoding.URLSafeBase64Encoder.encode(jws_header)
    to_sign       = encodedHeader + b'.' + proof_hash.digest() + doc_hash.digest()
    signed_data   = signing_key.sign(to_sign)
    jws           = encodedHeader + b'..' + nacl.encoding.URLSafeBase64Encoder.encode(signed_data.signature)
    proof['jws']  = jws.decode()[:-2]
    del proof['@context']
    credential['proof'] = proof
    return credential

def verify(singed_credential, verification_key, documentloader=None):
    """ It signs a credential using Ed25519Signature2018 JSON-LD Signature

    :param singed_credential: a python dict representing the credential
    :param [verification_key]:  the verification key 
        [id] the key id
        [publicKeyHex] a Hex encoded Ed25519 public key
    :param documentloader: a custom documentloader

    :return: True or False
    """
    singed_credential = singed_credential.copy()
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
    ver_key       = nacl.signing.VerifyKey(verification_key['publicKeyHex'],nacl.encoding.HexEncoder)
    signature     = nacl.encoding.URLSafeBase64Encoder.decode(encodedSignature)
    encodedHeader = nacl.encoding.URLSafeBase64Encoder.encode(jws_header)
    to_verify     = encodedHeader + b'.' + proof_hash.digest() + doc_hash.digest()
    try:
        ver_key.verify(to_verify, signature)
        return True
    except:
        return False
    
    
def filter(credential, filters):
    """ It verifies if a credential a some particular fieds/value pairs

    :param credential: a python dict representing the credential
    :param [filters]:  pairs of  
        a json path query,
        optinal, the value, or a list of values to serach

    :return: True or False
    """
    
    for filter in filters:
        jsonpath_expr = parse(filter[0])
        found = False
        for match in jsonpath_expr.find(credential):
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