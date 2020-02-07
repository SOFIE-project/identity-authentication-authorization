from http.server import BaseHTTPRequestHandler, HTTPServer
from indy import did,wallet,crypto
import cgi
import json
import random
import asyncio
import base64
import sys

conf = ""

class Security:
    @staticmethod
    def create_nonce(length=30):
        return ''.join([str(random.randint(0, 9)) for i in range(length)])

class IAA:
    @staticmethod
    def verify_token(type, token="", proof=""):
        if (type ==  "Bearer"):
            return 200, {'code':200,'message':'Success'}
        return 403, {'code':403, 'message':'Invalide token type'}
    
    @staticmethod
    async def verify_did(client_did, challenge="", signature="", wallet_config = "", wallet_credentials="", only_wallet_lookup=False, user_generated_challenge=False):
        if (client_did !="" and challenge == ""):
            return 401, {'code':401, 'message': 'Proof required','challenge':Security.create_nonce()}
        if (client_did !="" and challenge != "" and signature != "" and wallet_config!=""):
            wallet_handle = await wallet.open_wallet(wallet_config, wallet_credentials)
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
            await wallet.close_wallet(wallet_handle)
        else:
            return 403, {'code':403, 'message':'Invalide or missing input parameters'}

        
        

class IAAHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        path = self.path
        if path == "/verifytoken":
            code = 403
            output = {'code':403, 'message':'Invalide or missing input parameters'}
            form = cgi.FieldStorage(
                fp = self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                        'CONTENT_TYPE':self.headers['Content-Type'],
                        })
            type  = form.getvalue("token-type")
            token = form.getvalue("token")
            challenge = form.getvalue("challenge")
            proof = form.getvalue("proof")
            if (type == "Bearer"):
                code, output = IAA.verify_token(type, token, proof)
            if (type == "DID"):
                loop = asyncio.get_event_loop()
                code, output = loop.run_until_complete(IAA.verify_did(token, challenge, proof, conf['wallet_config'], "", True))#, challenge, proof, conf['wallet_config'], conf['wallet_credentials']))
            self.send_response(code)
            self.send_header('Content-type','application/json'.encode())
            self.end_headers()
            self.wfile.write(json.dumps(output).encode())


def main():
    if len(sys.argv) != 2:
        print ("Usage iaa.py <configuration file>")
        sys.exit()
    with open(sys.argv[1]) as f:
        conf = json.load(f)
    httpd = HTTPServer(('localhost', conf["port"]), IAAHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    main()