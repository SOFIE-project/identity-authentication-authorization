import random
try:
    import jwt
except ImportError:
     print("Couldn't import jwt, if you don't need JSON web token support that's OK")
try:
    import nacl.signing
    import nacl.encoding
except ImportError:
     print("Couldn't import nacl, if you don't need Proof of possesion support that's OK")

class pop_pep:
    def __init__(self):
        self.challenges = {}

    def _create_nonce(self, length=30):
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    def verify_proof_of_possesion(self, public_key, challenge=None, proof=None): 
        if (challenge == None):
            nonce = self._create_nonce()
            return False, nonce
        if (challenge and challenge in self.challenges): #dublicate
            return False, 401
