from http.server import BaseHTTPRequestHandler, HTTPServer
from indy_agent import Indy
from indy import pool, wallet
import cgi
import json
import sys
import jwt
import asyncio

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
    

class IAAHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global conf
        global wallet_handle
        global pool_handle
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
                with open(conf['as_public_key'], mode='rb') as file: 
                    as_public_key = file.read()
                code, output = IAA.verify_token(type, token, as_public_key, conf['target'],conf['tokens_expire'])
            if (type == "DID"):
                loop = asyncio.get_event_loop()
                code, output = loop.run_until_complete(
                    Indy.verify_did(token, challenge, proof, wallet_handle,"", True))
            self.send_response(code)
            self.send_header('Content-type','application/json'.encode())
            self.end_headers()
            self.wfile.write(json.dumps(output).encode())


def main():
    global conf
    global wallet_handle
    global pool_handle
    if len(sys.argv) != 2:
        print ("Usage iaa.py <configuration file>")
        sys.exit()
    with open(sys.argv[1]) as f:
        conf = json.load(f)
    httpd = HTTPServer(('', conf["port"]), IAAHandler)
    loop = asyncio.get_event_loop()
    wallet_handle = loop.run_until_complete(wallet.open_wallet(json.dumps(conf['wallet_config']), json.dumps(conf['wallet_credentials'])))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    loop.run_until_complete(wallet.close_wallet(wallet_handle))

if __name__ == '__main__':
    main()
