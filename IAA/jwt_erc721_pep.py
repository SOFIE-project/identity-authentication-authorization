import json
try:
    from web3 import Web3
except ImportError:
     print("Couldn't import web3, if you don't need ERC-721 support that's OK")
try:
    import jwt
except ImportError:
     print("Couldn't import jwt, if you don't need JSON web token support that's OK")

class jwt_erc721_pep:
    def __init__(self):
        with open('conf/erc721.conf') as f:
            self.conf = json.load(f)
        try:
            self.w3 = Web3(Web3.HTTPProvider(self.conf['web3provider']))
            with open('conf/contract/build/ERC721Metadata.abi', 'r') as myfile:
                self.abi = myfile.read()
            self.ERC721Contract_instance = self.w3.eth.contract(abi=self.abi, address=Web3.toChecksumAddress(self.conf['iaa_sc_address']))
        except:
            print("Couldn't connect to Ethereum blockchain:" + self.conf['web3provider'])
            pass

    def verify_bearer_erc721(self, token = None, jwt_verification_key = None ):
        try:
            decoded_token = jwt.decode(token, jwt_verification_key, algorithms='RS256', audience='sofie-iot.eu', options={"verify_exp":False})
            token_id = int(decoded_token['jti'], base = 16)
            owner_of_token = self.ERC721Contract_instance.functions.ownerOf(token_id).call()
            if (owner_of_token != 0):
                return True, "0"
            else:
                return False, "101 ERC-721 token has been revoked"
        except:
            return False, "100 Token cannot be decoded"