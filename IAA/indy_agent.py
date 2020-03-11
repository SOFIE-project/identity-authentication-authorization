from indy import did,wallet,crypto
import asyncio
import base64
import random

class Indy:
    @staticmethod
    def create_nonce(length=30):
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    @staticmethod
    async def verify_did(client_did, challenge = None, signature=None, wallet_handle="", pool_handle="", only_wallet_lookup=False, user_generated_challenge=False):
        if (client_did !=None and challenge == None):
            return 401, {'code':401, 'message' : 'Proof required','challenge': Indy.create_nonce()}
        if (client_did != None and challenge != None and signature != None and wallet_handle!= None):
            if (only_wallet_lookup):
                verkey = await did.key_for_local_did(wallet_handle, client_did)
            else:
                verkey = ""
            #Add code to check if verkey exists
            verification = await crypto.crypto_verify(verkey, challenge.encode(), base64.b64decode(signature))
            if(verification):
                return 200, {'code':200,'message':'Success'}
            else:
                return 403, {'code':403, 'message':'Signature verification failed'}
        else:
            return 403, {'code':403, 'message':'Invalide or missing input parameters'}