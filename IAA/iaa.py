from werkzeug.wrappers import Request, Response
from werkzeug.datastructures import Headers
from indy_agent import Indy
from indy import pool, wallet

import json
import sys
import jwt
import asyncio
import requests

conf = {}
wallet_handle = ""
pool_handle = ""

class IAA:
    @staticmethod
    def verify_token(type, token=None, as_public_key=None, target=None, tokens_expire = True, proof=None):
        if (type ==  "Bearer"):
            #decoded_token = jwt.decode(token, as_public_key, algorithms='RS256', audience=target, verify_expiration = False)
            try:
                decoded_token = jwt.decode(token, as_public_key, algorithms='RS256', audience=target, options={"verify_exp":tokens_expire})
                return 200, {'code':200,'message':'Success'}
            except:
                return 403, {'code':403,'message':'Token validation failed'}
        return 403, {'code':403, 'message':'Invalide token type'}
    

class IAAHandler():
    def __init__(self):
        with open('conf/iaa.conf') as f:
            self.conf = json.load(f)
        with open(self.conf['as_public_key'], mode='rb') as file: 
            self.as_public_key = file.read()
        loop = asyncio.get_event_loop()
        self.wallet_handle = loop.run_until_complete(wallet.open_wallet(json.dumps(self.conf['wallet_config']), json.dumps(self.conf['wallet_credentials'])))
        self.pool_handle = None
    
    def wsgi_app(self, environ, start_response):
        req  = Request(environ)
        code = 403
        output = {'code':403, 'message':'Invalide or missing input parameters'}
        output_header = {}
        form = req.form
        type  = form.get("token-type")
        token = form.get("token")
        challenge = form.get("challenge")
        proof = form.get("proof")
        auth = req.headers.get('Authorization')
        if (auth):
            auth_type, auth_grant = auth.split(" ",1)
            if (auth_type == 'VC'):
                proof = req.headers.get('VC-proof')
                if (proof):
                    verification = vc_agent.verify_token(auth_grant + proof, self.as_public_key)
                    print(verification)
                else:
                    code = 401
                    nonce = Indy.create_nonce()
                    output_header['WWW-Authenticate'] = "VC challenge=" + nonce
            if (auth_type == "Bearer"):
                code, output = IAA.verify_token("Bearer", auth_grant, self.as_public_key, self.conf['target'],self.conf['tokens_expire'])
                if (code == 200):
                    gateway_path = "http://195.251.234.21:8080"
                    gateway_token = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNjNTIxZDQzLWE3YzEtNDUzOS04ODY2LWRlMmEyNDQyNDU5OSJ9.eyJjbGllbnRfaWQiOiJsb2NhbC10b2tlbiIsInJvbGUiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZSI6Ii90aGluZ3M6cmVhZHdyaXRlIiwiaWF0IjoxNTk0OTkxOTUxLCJpc3MiOiJOb3Qgc2V0LiJ9.Q4X5Z4u2sE_Wq0aggkXnL95EoceJHY4UZjmdKkIFrp28-Cp1sK7tuQ6IdwqhesnAJVDBASvR3UOF3Y8oXSBBUw" 
                    path = environ.get('PATH_INFO')
                    print ("Contacting " + path)
                    print (gateway_path + path)
                    if (req.method == "GET"):
                        gateway_get_headers = {'Authorization':'Bearer ' + gateway_token, 'Accept': 'application/json'}
                        response  = requests.get(gateway_path + path, headers = gateway_get_headers)
                        print(response.text)
                        print("get")
                    elif (req.method == "PUT"):
                        gateway_put_headers = {'Authorization':'Bearer ' + gateway_token, 'Content-Type': 'application/json', 'Accept': 'application/json'}
                        put_data = req.data
                        print(put_data)
                        response  = requests.put(gateway_path + path, headers = gateway_put_headers, data = put_data.decode())
                        print(response.text)
                    code = 200
                    output = response.text 
        
        if (type == "Bearer"):
            code, output = IAA.verify_token(type, token, self.as_public_key, self.conf['target'],self.conf['tokens_expire'])
        if (type == "DID"):
            loop = asyncio.get_event_loop()
            code, output = loop.run_until_complete(
                Indy.verify_did(token, challenge, proof, self.wallet_handle, self.pool_handle, True))
        response = Response(output.encode(), status=code, mimetype='application/json')
        if output_header:
            for key,value in output_header.items():
                response.headers.add(key, value)
        return response(environ, start_response)
        
    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app():
    app = IAAHandler()
    return app

def main(): 
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('', 9000, app)
    #loop.run_until_complete(wallet.close_wallet(wallet_handle))

if __name__ == '__main__':
    main()
