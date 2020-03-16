from indy import did, wallet, crypto, IndyError
import asyncio
import base64
import random



class Indy:
    @staticmethod
    def create_nonce(length=30):
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

    @staticmethod
    async def verify_did(client_did, challenge=None, signature=None, wallet_handle="", pool_handle="",
                         only_wallet_lookup=False, user_generated_challenge=False):
        if client_did is not None and challenge is None:
            return 401, {'code': 401, 'message': 'Proof required', 'challenge': Indy.create_nonce()}
        if client_did is not None and challenge is not None and signature is not None and wallet_handle is not None:
            if only_wallet_lookup:
                try:
                    verkey = await did.key_for_local_did(wallet_handle, client_did)

                    print("____verkey:", verkey, "wallet handle:", wallet_handle,"did:",client_did)
                except IndyError:
                    return 404, {'code': 404, 'message': 'DID doesn\'t exist'}
            else:
                verkey = ""
            # Add code to check if verkey exists
            verification = await crypto.crypto_verify(verkey, challenge.encode(), base64.b64decode(signature))
            if verification:
                return 200, {'code': 200, 'message': 'Signature verified'}
            else:
                return 403, {'code': 403, 'message': 'Signature verification failed'}
        else:
            return 403, {'code': 403, 'message': 'Invalide or missing input parameters'}
