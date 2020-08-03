from werkzeug.wrappers       import Request, Response
from werkzeug.datastructures import Headers
from jwt_pep                 import jwt_pep
from jwt_erc721_pep          import jwt_erc721_pep
from http_proxy              import http_proxy

import json
import sys
import asyncio
import requests

  

class IAAHandler():
    def __init__(self):
        with open('conf/iaa.conf') as f:
            self.conf = json.load(f)
        self.jwt_pep = jwt_pep()
        self.jwt_erc721_pep = jwt_erc721_pep()
        self.http_proxy = http_proxy()

    def wsgi_app(self, environ, start_response):
        req      = Request(environ)
        path     = environ.get('PATH_INFO')
        code     = 403
        resource = {}
        output = 'Invalide or missing input parameters'
        output_header = {}
        auth    = req.headers.get('Authorization')
        if (path in self.conf['resources']):
            resource = self.conf['resources'][path]
        if (auth):
            auth_type, auth_grant = auth.split(" ",1)
            '''
            if (auth_type == 'VC'):
                proof = req.headers.get('VC-proof')
                if (proof):
                    verification = vc_agent.verify_token(auth_grant + proof, self.as_public_key)
                    print(verification)
                else:
                    code = 401
                    nonce = Indy.create_nonce()
                    output_header['WWW-Authenticate'] = "VC challenge=" + nonce
            if (auth_type == "DID"):
                loop = asyncio.get_event_loop()
                code, output = loop.run_until_complete(
                    Indy.verify_did(token, challenge, proof, self.wallet_handle, self.pool_handle, True))
            '''
            #*********JWT***********
            if (resource['authorization']['type'] == "jwt" and auth_type == "Bearer"):
                if (not ('signing_key' in resource['authorization'])):
                    with open(resource['authorization']['signing_key_file'], mode='rb') as file: 
                        resource['authorization']['signing_key'] = file.read()
                result, error_code = self.jwt_pep.verify_bearer(auth_grant, resource['authorization']['signing_key'], resource['authorization']['tokens_expire'])
                if (result == True):
                    code, output = self.http_proxy.forward(environ, resource['proxy']['proxy_pass'], resource['proxy']['header_rewrite'])
                else:
                    code = 401
                    output = str(error_code)

            #*********JWT+ERC721*********** 
            if (resource['authorization']['type'] == "jwt-erc721" and auth_type == "Bearer-ERC721"):
                if (not ('signing_key' in resource['authorization'])):
                    with open(resource['authorization']['signing_key_file'], mode='rb') as file: 
                        resource['authorization']['signing_key'] = file.read()
                result, error_code = self.jwt_erc721_pep.verify_bearer_erc721(auth_grant, resource['authorization']['signing_key'])
                if (result == True):
                    code, output = self.http_proxy.forward(environ, resource['proxy']['proxy_pass'], resource['proxy']['header_rewrite'])
                else:
                    code = 401
                    output = str(error_code)

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

if __name__ == '__main__':
    main()
