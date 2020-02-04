from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import json

class IAA:
    @staticmethod
    def verify_token(type, token="", proof=""):
        if (type ==  "Bearer"):
            return 200, "Success"
        return 403, "Invalide token type"

class IAAHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        path = self.path
        if path == "/verifytoken":
            form = cgi.FieldStorage(
                fp = self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                        'CONTENT_TYPE':self.headers['Content-Type'],
                        })
            type  = form.getvalue("token-type")
            token = form.getvalue("token")
            proof = form.getvalue("proof")
            code,message = IAA.verify_token(type, token, proof)
            if (code == 200):
                self.send_response(200)
                self.send_header('Content-type','application/json'.encode())
                self.end_headers()
                output = {"result": "Success"}
                self.wfile.write(json.dumps(output).encode())
                return
            self.send_response(code)
            self.send_header('Content-type','application/json'.encode())
            self.end_headers()
            output = {"result": "Failure", "message": message}
            self.wfile.write(json.dumps(output).encode())


def main():
    print ("Starting Agent at port 9000")
    httpd = HTTPServer(('localhost', 9000), IAAHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    main()